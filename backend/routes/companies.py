from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from ..database import DatabaseOperations
from ..auth import get_current_user
from ..models import CompanyCreate, Company
from bson import ObjectId
import random

router = APIRouter(prefix="/companies", tags=["companies"])

@router.get("/", response_model=dict)
async def get_companies(
    country: Optional[str] = Query(None, description="Filter by country"),
    limit: int = Query(50, ge=1, le=100, description="Number of companies to return")
):
    """Get companies list with optional country filter"""
    
    if country:
        companies = await DatabaseOperations.get_companies_by_country(country.lower(), limit)
    else:
        companies_collection = await DatabaseOperations.Collections.get_companies()
        cursor = companies_collection.find({}).sort("created_at", -1).limit(limit)
        companies = await cursor.to_list(limit)
    
    # Convert ObjectIds to strings and get owner details
    for company in companies:
        company["_id"] = str(company["_id"])
        company["owner"] = str(company["owner"])
        
        # Get owner username
        owner = await DatabaseOperations.get_user_by_id(company["owner"])
        if owner:
            company["owner_username"] = owner["username"]
        
        # Convert employee IDs
        company["employees"] = [str(emp_id) for emp_id in company.get("employees", [])]
    
    return {"companies": companies}

@router.get("/my", response_model=dict)
async def get_my_companies(current_user: dict = Depends(get_current_user)):
    """Get current user's companies"""
    
    companies = await DatabaseOperations.get_companies_by_owner(current_user["_id"])
    
    # Convert ObjectIds to strings
    for company in companies:
        company["_id"] = str(company["_id"])
        company["owner"] = str(company["owner"])
        company["employees"] = [str(emp_id) for emp_id in company.get("employees", [])]
        
        # Get employee details
        employee_details = []
        for emp_id in company.get("employees", []):
            employee = await DatabaseOperations.get_user_by_id(emp_id)
            if employee:
                employee_details.append({
                    "_id": str(employee["_id"]),
                    "username": employee["username"],
                    "strength": employee["strength"]
                })
        company["employee_details"] = employee_details
    
    return {"companies": companies}

@router.get("/{company_id}", response_model=dict)
async def get_company_details(company_id: str):
    """Get detailed company information"""
    
    companies_collection = await DatabaseOperations.Collections.get_companies()
    company = await companies_collection.find_one({"_id": ObjectId(company_id)})
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    # Convert ObjectIds to strings
    company["_id"] = str(company["_id"])
    
    # Get owner details
    owner = await DatabaseOperations.get_user_by_id(str(company["owner"]))
    if owner:
        company["owner_details"] = {
            "_id": str(owner["_id"]),
            "username": owner["username"],
            "country": owner["country"]
        }
    
    # Get employee details
    employee_details = []
    for emp_id in company.get("employees", []):
        employee = await DatabaseOperations.get_user_by_id(str(emp_id))
        if employee:
            employee_details.append({
                "_id": str(employee["_id"]),
                "username": employee["username"],
                "strength": employee["strength"],
                "rank": employee["rank"]
            })
    
    company["employee_details"] = employee_details
    company["employees"] = [str(emp_id) for emp_id in company.get("employees", [])]
    company["owner"] = str(company["owner"])
    
    return {"company": company}

@router.post("/", response_model=dict)
async def create_company(
    company_data: CompanyCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new company"""
    
    # Check if user has enough gold (cost: 100 * quality)
    cost = 100 * company_data.quality
    if current_user["gold"] < cost:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not enough gold. Cost: {cost}, Available: {current_user['gold']}"
        )
    
    # Check if user already has a company with the same name
    existing_companies = await DatabaseOperations.get_companies_by_owner(current_user["_id"])
    for company in existing_companies:
        if company["name"].lower() == company_data.name.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You already have a company with this name"
            )
    
    # Create company
    new_company = {
        "name": company_data.name,
        "type": company_data.type,
        "owner": ObjectId(current_user["_id"]),
        "country": company_data.country.lower(),
        "quality": company_data.quality,
        "employees": [],
        "daily_profit": company_data.quality * random.randint(50, 150),
        "productivity": 100
    }
    
    company_id = await DatabaseOperations.create_company(new_company)
    
    # Deduct gold from user
    await DatabaseOperations.update_user(current_user["_id"], {
        "gold": current_user["gold"] - cost
    })
    
    # Add company to user's companies list
    await DatabaseOperations.update_user(current_user["_id"], {
        "companies": current_user.get("companies", []) + [ObjectId(company_id)]
    })
    
    return {
        "message": "Company created successfully",
        "company_id": company_id,
        "cost": cost
    }

@router.post("/{company_id}/work", response_model=dict)
async def work_in_company(
    company_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Work in a company to earn money"""
    
    companies_collection = await DatabaseOperations.Collections.get_companies()
    company = await companies_collection.find_one({"_id": ObjectId(company_id)})
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    # Check if user is already an employee
    user_id = ObjectId(current_user["_id"])
    if user_id not in company.get("employees", []):
        # Add user as employee
        await companies_collection.update_one(
            {"_id": ObjectId(company_id)},
            {"$addToSet": {"employees": user_id}}
        )
    
    # Calculate work reward based on company quality and user strength
    base_reward = company["quality"] * 10
    strength_bonus = current_user["strength"] // 10
    total_reward = base_reward + strength_bonus + random.randint(5, 15)
    
    # Give reward to user
    exp_gain = total_reward // 3
    await DatabaseOperations.update_user(current_user["_id"], {
        "gold": current_user["gold"] + total_reward,
        "experience": current_user["experience"] + exp_gain
    })
    
    # Update company productivity (simulate work impact)
    new_productivity = min(100, company.get("productivity", 100) + 1)
    await companies_collection.update_one(
        {"_id": ObjectId(company_id)},
        {"$set": {"productivity": new_productivity}}
    )
    
    return {
        "message": "Work completed successfully",
        "gold_earned": total_reward,
        "experience_gained": exp_gain,
        "company_productivity": new_productivity
    }

@router.put("/{company_id}", response_model=dict)
async def update_company(
    company_id: str,
    update_data: dict,
    current_user: dict = Depends(get_current_user)
):
    """Update company (owner only)"""
    
    companies_collection = await DatabaseOperations.Collections.get_companies()
    company = await companies_collection.find_one({"_id": ObjectId(company_id)})
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    # Check if user is the owner
    if company["owner"] != ObjectId(current_user["_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the owner can update this company"
        )
    
    # Update allowed fields
    allowed_fields = ["name", "type"]
    update_fields = {}
    
    for field in allowed_fields:
        if field in update_data:
            update_fields[field] = update_data[field]
    
    if update_fields:
        await companies_collection.update_one(
            {"_id": ObjectId(company_id)},
            {"$set": update_fields}
        )
    
    return {"message": "Company updated successfully"}

@router.delete("/{company_id}", response_model=dict)
async def delete_company(
    company_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete company (owner only)"""
    
    companies_collection = await DatabaseOperations.Collections.get_companies()
    company = await companies_collection.find_one({"_id": ObjectId(company_id)})
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    # Check if user is the owner
    if company["owner"] != ObjectId(current_user["_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the owner can delete this company"
        )
    
    # Delete company
    await companies_collection.delete_one({"_id": ObjectId(company_id)})
    
    # Remove from user's companies list
    user_companies = current_user.get("companies", [])
    if ObjectId(company_id) in user_companies:
        user_companies.remove(ObjectId(company_id))
        await DatabaseOperations.update_user(current_user["_id"], {
            "companies": user_companies
        })
    
    return {"message": "Company deleted successfully"}