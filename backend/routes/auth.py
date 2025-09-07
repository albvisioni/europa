from fastapi import APIRouter, HTTPException, status, Depends
from datetime import timedelta
from models import UserCreate, UserLogin, UserProfile
from database import DatabaseOperations
from auth import create_access_token, authenticate_user, get_password_hash, get_current_user
from bson import ObjectId

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=dict)
async def register_user(user_data: UserCreate):
    """Register a new user"""
    
    # Check if user already exists
    existing_user = await DatabaseOperations.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists
    users_collection = await DatabaseOperations.Collections.get_users()
    existing_username = await users_collection.find_one({"username": user_data.username})
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create user
    user_dict = user_data.dict()
    user_dict["password"] = get_password_hash(user_data.password)
    user_dict["level"] = 1
    user_dict["experience"] = 0
    user_dict["gold"] = 100
    user_dict["strength"] = 10
    user_dict["rank"] = "Recruit"
    user_dict["political_party"] = None
    user_dict["companies"] = []
    user_dict["achievements"] = []
    user_dict["is_admin"] = False
    user_dict["is_banned"] = False
    
    user_id = await DatabaseOperations.create_user(user_dict)
    
    # Update country stats
    await DatabaseOperations.update_country_stats(user_data.country)
    
    # Create access token
    access_token_expires = timedelta(minutes=30 * 24 * 60)  # 30 days
    access_token = create_access_token(
        data={"sub": user_id}, expires_delta=access_token_expires
    )
    
    # Get created user
    created_user = await DatabaseOperations.get_user_by_id(user_id)
    created_user["_id"] = str(created_user["_id"])
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": created_user
    }

@router.post("/login", response_model=dict)
async def login_user(user_credentials: UserLogin):
    """Login user"""
    
    # Get user by email
    user = await DatabaseOperations.get_user_by_email(user_credentials.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is banned
    if user.get("is_banned", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is banned"
        )
    
    # Authenticate user
    if not authenticate_user(user_credentials.email, user_credentials.password, user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=30 * 24 * 60)  # 30 days
    access_token = create_access_token(
        data={"sub": str(user["_id"])}, expires_delta=access_token_expires
    )
    
    # Convert ObjectId to string
    user["_id"] = str(user["_id"])
    if user.get("political_party"):
        user["political_party"] = str(user["political_party"])
    user["companies"] = [str(c) for c in user.get("companies", [])]
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.get("/me", response_model=dict)
async def get_current_user_profile(current_user: dict = Depends(get_current_user)):
    """Get current user profile"""
    
    # Convert ObjectId to string
    current_user["_id"] = str(current_user["_id"])
    if current_user.get("political_party"):
        current_user["political_party"] = str(current_user["political_party"])
    current_user["companies"] = [str(c) for c in current_user.get("companies", [])]
    
    return {"user": current_user}

@router.post("/logout")
async def logout_user():
    """Logout user (client should remove token)"""
    return {"message": "Successfully logged out"}