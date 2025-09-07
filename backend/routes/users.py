from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from ..models import UserUpdate
from ..database import DatabaseOperations
from ..auth import get_current_user
from bson import ObjectId

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/profile", response_model=dict)
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    """Get current user profile"""
    
    # Convert ObjectId to string
    current_user["_id"] = str(current_user["_id"])
    if current_user.get("political_party"):
        current_user["political_party"] = str(current_user["political_party"])
    current_user["companies"] = [str(c) for c in current_user.get("companies", [])]
    
    return {"user": current_user}

@router.put("/profile", response_model=dict)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update current user profile"""
    
    update_data = {}
    if user_update.username:
        # Check if username is taken
        users_collection = await DatabaseOperations.Collections.get_users()
        existing = await users_collection.find_one({
            "username": user_update.username,
            "_id": {"$ne": ObjectId(current_user["_id"])}
        })
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        update_data["username"] = user_update.username
    
    if user_update.email:
        # Check if email is taken
        existing = await DatabaseOperations.get_user_by_email(user_update.email)
        if existing and str(existing["_id"]) != current_user["_id"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        update_data["email"] = user_update.email
    
    if user_update.country:
        old_country = current_user.get("country")
        update_data["country"] = user_update.country
        
        # Update country stats for both old and new countries
        if old_country and old_country != user_update.country:
            await DatabaseOperations.update_country_stats(old_country)
        await DatabaseOperations.update_country_stats(user_update.country)
    
    if update_data:
        success = await DatabaseOperations.update_user(current_user["_id"], update_data)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update profile"
            )
    
    # Get updated user
    updated_user = await DatabaseOperations.get_user_by_id(current_user["_id"])
    updated_user["_id"] = str(updated_user["_id"])
    if updated_user.get("political_party"):
        updated_user["political_party"] = str(updated_user["political_party"])
    updated_user["companies"] = [str(c) for c in updated_user.get("companies", [])]
    
    return {"user": updated_user}

@router.get("/{user_id}", response_model=dict)
async def get_user_by_id(user_id: str):
    """Get user by ID (public profile)"""
    
    user = await DatabaseOperations.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Return only public information
    public_user = {
        "_id": str(user["_id"]),
        "username": user["username"],
        "country": user["country"],
        "level": user["level"],
        "experience": user["experience"],
        "strength": user["strength"],
        "rank": user["rank"],
        "achievements": user.get("achievements", []),
        "created_at": user["created_at"]
    }
    
    return {"user": public_user}

@router.get("/", response_model=dict)
async def get_users(
    country: Optional[str] = Query(None, description="Filter by country"),
    limit: int = Query(50, ge=1, le=100, description="Number of users to return")
):
    """Get users list with optional country filter"""
    
    if country:
        users = await DatabaseOperations.get_users_by_country(country, limit)
    else:
        users = await DatabaseOperations.get_user_rankings(limit)
    
    # Convert ObjectIds to strings and return only public info
    public_users = []
    for user in users:
        public_user = {
            "_id": str(user["_id"]),
            "username": user["username"],
            "country": user["country"],
            "level": user["level"],
            "experience": user["experience"],
            "strength": user["strength"],
            "rank": user["rank"],
            "achievements": user.get("achievements", [])
        }
        public_users.append(public_user)
    
    return {"users": public_users}

@router.get("/rankings/top", response_model=dict)
async def get_user_rankings(
    limit: int = Query(100, ge=1, le=500, description="Number of top users to return")
):
    """Get top user rankings by experience"""
    
    users = await DatabaseOperations.get_user_rankings(limit)
    
    # Convert ObjectIds to strings and return public info with ranking
    rankings = []
    for index, user in enumerate(users):
        ranking = {
            "rank": index + 1,
            "_id": str(user["_id"]),
            "username": user["username"],
            "country": user["country"],
            "level": user["level"],
            "experience": user["experience"],
            "strength": user["strength"],
            "title": user["rank"]
        }
        rankings.append(ranking)
    
    return {"rankings": rankings}