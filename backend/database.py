from motor.motor_asyncio import AsyncIOMotorClient
import os
from typing import List, Dict, Any, Optional
from bson import ObjectId
from datetime import datetime

class Database:
    client: AsyncIOMotorClient = None
    db = None

database = Database()

async def get_database() -> AsyncIOMotorClient:
    return database.db

async def connect_to_mongo():
    """Create database connection"""
    database.client = AsyncIOMotorClient(os.environ.get("MONGO_URL"))
    database.db = database.client[os.environ.get("DB_NAME", "europa_db")]
    print("Connected to MongoDB")

async def close_mongo_connection():
    """Close database connection"""
    database.client.close()
    print("Disconnected from MongoDB")

# Collection helpers
class Collections:
    @staticmethod
    async def get_users():
        return database.db.users
    
    @staticmethod
    async def get_countries():
        return database.db.countries
    
    @staticmethod
    async def get_battles():
        return database.db.battles
    
    @staticmethod
    async def get_companies():
        return database.db.companies
    
    @staticmethod
    async def get_political_parties():
        return database.db.political_parties
    
    @staticmethod
    async def get_news():
        return database.db.news
    
    @staticmethod
    async def get_messages():
        return database.db.messages
    
    @staticmethod
    async def get_market():
        return database.db.market
    
    @staticmethod
    async def get_leagues():
        return database.db.leagues

# Database operations
class DatabaseOperations:
    
    # User operations
    @staticmethod
    async def create_user(user_data: Dict[str, Any]) -> str:
        collection = await Collections.get_users()
        user_data["created_at"] = datetime.utcnow()
        user_data["updated_at"] = datetime.utcnow()
        result = await collection.insert_one(user_data)
        return str(result.inserted_id)
    
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
        collection = await Collections.get_users()
        return await collection.find_one({"email": email})
    
    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
        collection = await Collections.get_users()
        return await collection.find_one({"_id": ObjectId(user_id)})
    
    @staticmethod
    async def update_user(user_id: str, update_data: Dict[str, Any]) -> bool:
        collection = await Collections.get_users()
        update_data["updated_at"] = datetime.utcnow()
        result = await collection.update_one(
            {"_id": ObjectId(user_id)}, 
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    @staticmethod
    async def get_users_by_country(country: str, limit: int = 50) -> List[Dict[str, Any]]:
        collection = await Collections.get_users()
        cursor = collection.find({"country": country}).limit(limit)
        return await cursor.to_list(length=limit)
    
    @staticmethod
    async def get_user_rankings(limit: int = 100) -> List[Dict[str, Any]]:
        collection = await Collections.get_users()
        cursor = collection.find({}).sort("experience", -1).limit(limit)
        return await cursor.to_list(length=limit)
    
    # Country operations
    @staticmethod
    async def create_country(country_data: Dict[str, Any]) -> str:
        collection = await Collections.get_countries()
        country_data["created_at"] = datetime.utcnow()
        result = await collection.insert_one(country_data)
        return str(result.inserted_id)
    
    @staticmethod
    async def get_all_countries() -> List[Dict[str, Any]]:
        collection = await Collections.get_countries()
        cursor = collection.find({}).sort("total_players", -1)
        return await cursor.to_list(length=None)
    
    @staticmethod
    async def get_country_by_code(code: str) -> Optional[Dict[str, Any]]:
        collection = await Collections.get_countries()
        return await collection.find_one({"code": code.upper()})
    
    @staticmethod
    async def update_country_stats(code: str) -> bool:
        """Update country player count and power"""
        users_collection = await Collections.get_users()
        countries_collection = await Collections.get_countries()
        
        # Count players and calculate total power
        player_count = await users_collection.count_documents({"country": code.lower()})
        
        # Calculate total power (sum of all users' strength)
        pipeline = [
            {"$match": {"country": code.lower()}},
            {"$group": {"_id": None, "total_power": {"$sum": "$strength"}}}
        ]
        result = await users_collection.aggregate(pipeline).to_list(1)
        total_power = result[0]["total_power"] if result else 0
        
        # Update country
        update_result = await countries_collection.update_one(
            {"code": code.upper()},
            {"$set": {"total_players": player_count, "total_power": total_power}}
        )
        return update_result.modified_count > 0
    
    # Battle operations
    @staticmethod
    async def create_battle(battle_data: Dict[str, Any]) -> str:
        collection = await Collections.get_battles()
        battle_data["start_time"] = datetime.utcnow()
        result = await collection.insert_one(battle_data)
        return str(result.inserted_id)
    
    @staticmethod
    async def get_active_battles() -> List[Dict[str, Any]]:
        collection = await Collections.get_battles()
        cursor = collection.find({"status": "ongoing"}).sort("start_time", -1)
        return await cursor.to_list(length=None)
    
    @staticmethod
    async def get_battle_by_id(battle_id: str) -> Optional[Dict[str, Any]]:
        collection = await Collections.get_battles()
        return await collection.find_one({"_id": ObjectId(battle_id)})
    
    @staticmethod
    async def join_battle(battle_id: str, user_id: str, damage: int, side: str) -> bool:
        collection = await Collections.get_battles()
        
        # Add participant
        participant = {
            "user": ObjectId(user_id),
            "damage": damage,
            "side": side
        }
        
        # Update battle with new participant and damage
        update_data = {
            "$push": {"participants": participant}
        }
        
        if side == "attacker":
            update_data["$inc"] = {"attacker_damage": damage}
        else:
            update_data["$inc"] = {"defender_damage": damage}
        
        result = await collection.update_one(
            {"_id": ObjectId(battle_id)},
            update_data
        )
        return result.modified_count > 0
    
    # Company operations
    @staticmethod
    async def create_company(company_data: Dict[str, Any]) -> str:
        collection = await Collections.get_companies()
        company_data["created_at"] = datetime.utcnow()
        result = await collection.insert_one(company_data)
        return str(result.inserted_id)
    
    @staticmethod
    async def get_companies_by_owner(owner_id: str) -> List[Dict[str, Any]]:
        collection = await Collections.get_companies()
        cursor = collection.find({"owner": ObjectId(owner_id)})
        return await cursor.to_list(length=None)
    
    @staticmethod
    async def get_companies_by_country(country: str, limit: int = 50) -> List[Dict[str, Any]]:
        collection = await Collections.get_companies()
        cursor = collection.find({"country": country}).limit(limit)
        return await cursor.to_list(length=limit)
    
    # News operations
    @staticmethod
    async def create_news(news_data: Dict[str, Any]) -> str:
        collection = await Collections.get_news()
        news_data["timestamp"] = datetime.utcnow()
        result = await collection.insert_one(news_data)
        return str(result.inserted_id)
    
    @staticmethod
    async def get_recent_news(country: str = None, limit: int = 20) -> List[Dict[str, Any]]:
        collection = await Collections.get_news()
        
        query = {}
        if country:
            query = {
                "$or": [
                    {"is_global": True},
                    {"countries": country}
                ]
            }
        else:
            query = {"is_global": True}
        
        cursor = collection.find(query).sort("timestamp", -1).limit(limit)
        return await cursor.to_list(length=limit)
    
    # Message operations
    @staticmethod
    async def send_message(message_data: Dict[str, Any]) -> str:
        collection = await Collections.get_messages()
        message_data["timestamp"] = datetime.utcnow()
        result = await collection.insert_one(message_data)
        return str(result.inserted_id)
    
    @staticmethod
    async def get_user_messages(user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        collection = await Collections.get_messages()
        cursor = collection.find({"to_user": ObjectId(user_id)}).sort("timestamp", -1).limit(limit)
        return await cursor.to_list(length=limit)
    
    @staticmethod
    async def mark_message_read(message_id: str, user_id: str) -> bool:
        collection = await Collections.get_messages()
        result = await collection.update_one(
            {"_id": ObjectId(message_id), "to_user": ObjectId(user_id)},
            {"$set": {"is_read": True}}
        )
        return result.modified_count > 0