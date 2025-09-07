from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, EmailStr
import os
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Database connection
client = MongoClient(os.environ.get('MONGO_URL'))
db = client[os.environ.get('DB_NAME', 'europa_db')]

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema
        return core_schema.no_info_wrap_validator_function(
            cls.validate,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        if isinstance(v, str):
            if ObjectId.is_valid(v):
                return v
            raise ValueError("Invalid ObjectId")
        raise ValueError("Invalid type for ObjectId")

# User Models
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    country: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserProfile(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    email: EmailStr
    country: str
    level: int = 1
    experience: int = 0
    gold: int = 100
    strength: int = 10
    rank: str = "Recruit"
    political_party: Optional[PyObjectId] = None
    companies: List[PyObjectId] = []
    achievements: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_admin: bool = False
    is_banned: bool = False

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    country: Optional[str] = None

# Country Models
class Country(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    code: str
    name: str
    flag: str
    regions: List[str]
    capital: str
    total_power: int = 0
    total_players: int = 0
    current_president: Optional[PyObjectId] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# Battle Models
class BattleParticipant(BaseModel):
    user: PyObjectId
    damage: int
    side: str  # attacker/defender

class Battle(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    region: str
    attacker: str
    defender: str
    status: str = "ongoing"  # ongoing/victory/defeat
    start_time: datetime = Field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = None
    attacker_damage: int = 0
    defender_damage: int = 0
    participants: List[BattleParticipant] = []
    winner: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class BattleFight(BaseModel):
    damage: int
    side: str

# Company Models
class Company(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    type: str
    owner: PyObjectId
    country: str
    employees: List[PyObjectId] = []
    quality: int = Field(ge=1, le=5)
    daily_profit: int = 0
    productivity: int = 100
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class CompanyCreate(BaseModel):
    name: str
    type: str
    country: str
    quality: int = Field(ge=1, le=5, default=1)

# Political Models
class PoliticalParty(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    country: str
    leader: PyObjectId
    members: List[PyObjectId] = []
    ideology: str
    description: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class PartyCreate(BaseModel):
    name: str
    country: str
    ideology: str
    description: str

# News Models
class News(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    content: str
    type: str  # military/politics/economy
    author: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    is_global: bool = False
    countries: List[str] = []

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class NewsCreate(BaseModel):
    title: str
    content: str
    type: str
    author: str = "System"
    is_global: bool = False
    countries: List[str] = []

# Message Models (New Feature)
class Message(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    from_user: PyObjectId
    to_user: PyObjectId
    subject: str
    content: str
    is_read: bool = False
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class MessageCreate(BaseModel):
    to_user: PyObjectId
    subject: str
    content: str

# Market Models (New Feature)
class Market(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    seller: PyObjectId
    item: str
    quantity: int
    price: int
    country: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class MarketCreate(BaseModel):
    item: str
    quantity: int
    price: int
    country: str

# League Models (New Feature)
class League(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: str
    countries: List[str]
    type: str  # military/economic/political
    leader: str  # country code
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class LeagueCreate(BaseModel):
    name: str
    description: str
    type: str
    leader: str

# Database Helper Functions
class DatabaseHelper:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
        return db.users.find_one({"email": email})
    
    @staticmethod
    def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
        return db.users.find_one({"username": username})
    
    @staticmethod
    def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
        return db.users.find_one({"_id": ObjectId(user_id)})
    
    @staticmethod
    def create_user(user_data: Dict[str, Any]) -> str:
        user_data["password"] = DatabaseHelper.hash_password(user_data["password"])
        user_data["created_at"] = datetime.utcnow()
        user_data["updated_at"] = datetime.utcnow()
        result = db.users.insert_one(user_data)
        return str(result.inserted_id)
    
    @staticmethod
    def update_user(user_id: str, update_data: Dict[str, Any]) -> bool:
        update_data["updated_at"] = datetime.utcnow()
        result = db.users.update_one(
            {"_id": ObjectId(user_id)}, 
            {"$set": update_data}
        )
        return result.modified_count > 0