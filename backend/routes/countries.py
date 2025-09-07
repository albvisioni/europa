from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from ..database import DatabaseOperations
from ..auth import get_current_user, get_current_admin_user
from ..models import Country

router = APIRouter(prefix="/countries", tags=["countries"])

@router.get("/", response_model=dict)
async def get_all_countries():
    """Get all countries with statistics"""
    
    countries = await DatabaseOperations.get_all_countries()
    
    # Convert ObjectIds to strings
    for country in countries:
        country["_id"] = str(country["_id"])
        if country.get("current_president"):
            country["current_president"] = str(country["current_president"])
    
    return {"countries": countries}

@router.get("/{country_code}", response_model=dict)
async def get_country_details(country_code: str):
    """Get detailed country information"""
    
    country = await DatabaseOperations.get_country_by_code(country_code)
    if not country:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Country not found"
        )
    
    # Get country users
    users = await DatabaseOperations.get_users_by_country(country_code.lower(), 20)
    
    # Convert ObjectIds to strings
    country["_id"] = str(country["_id"])
    if country.get("current_president"):
        country["current_president"] = str(country["current_president"])
    
    # Convert user ObjectIds
    for user in users:
        user["_id"] = str(user["_id"])
    
    # Get top users in this country
    users_collection = await DatabaseOperations.Collections.get_users()
    top_users_cursor = users_collection.find({"country": country_code.lower()}).sort("experience", -1).limit(10)
    top_users = await top_users_cursor.to_list(10)
    
    for user in top_users:
        user["_id"] = str(user["_id"])
    
    return {
        "country": country,
        "recent_users": users,
        "top_users": top_users
    }

@router.get("/{country_code}/users", response_model=dict)
async def get_country_users(country_code: str, limit: int = 50):
    """Get users from a specific country"""
    
    country = await DatabaseOperations.get_country_by_code(country_code)
    if not country:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Country not found"
        )
    
    users = await DatabaseOperations.get_users_by_country(country_code.lower(), limit)
    
    # Convert ObjectIds to strings and return public info
    public_users = []
    for user in users:
        public_user = {
            "_id": str(user["_id"]),
            "username": user["username"],
            "level": user["level"],
            "experience": user["experience"],
            "strength": user["strength"],
            "rank": user["rank"]
        }
        public_users.append(public_user)
    
    return {"users": public_users, "country": country["name"]}

@router.put("/{country_code}/stats", response_model=dict)
async def update_country_stats(
    country_code: str,
    current_user: dict = Depends(get_current_admin_user)
):
    """Update country statistics (admin only)"""
    
    success = await DatabaseOperations.update_country_stats(country_code)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Country not found"
        )
    
    # Get updated country
    country = await DatabaseOperations.get_country_by_code(country_code)
    country["_id"] = str(country["_id"])
    
    return {"message": "Country stats updated", "country": country}

@router.post("/{country_code}/president", response_model=dict)
async def elect_president(
    country_code: str,
    president_id: str,
    current_user: dict = Depends(get_current_admin_user)
):
    """Elect a new president for a country (admin only)"""
    
    # Verify the user exists and is from this country
    president = await DatabaseOperations.get_user_by_id(president_id)
    if not president:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if president["country"] != country_code.lower():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not from this country"
        )
    
    # Update country president
    countries_collection = await DatabaseOperations.Collections.get_countries()
    result = await countries_collection.update_one(
        {"code": country_code.upper()},
        {"$set": {"current_president": president["_id"]}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Country not found"
        )
    
    return {
        "message": f"{president['username']} elected as president of {country_code.upper()}",
        "president": {
            "_id": str(president["_id"]),
            "username": president["username"],
            "country": president["country"]
        }
    }