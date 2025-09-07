from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from datetime import datetime
from ..database import DatabaseOperations
from ..auth import get_current_user, get_current_admin_user
from ..models import Battle, BattleFight
from bson import ObjectId
import random

router = APIRouter(prefix="/battles", tags=["battles"])

@router.get("/", response_model=dict)
async def get_active_battles():
    """Get all active battles"""
    
    battles = await DatabaseOperations.get_active_battles()
    
    # Convert ObjectIds to strings
    for battle in battles:
        battle["_id"] = str(battle["_id"])
        for participant in battle.get("participants", []):
            participant["user"] = str(participant["user"])
    
    return {"battles": battles}

@router.get("/{battle_id}", response_model=dict)
async def get_battle_details(battle_id: str):
    """Get detailed battle information"""
    
    battle = await DatabaseOperations.get_battle_by_id(battle_id)
    if not battle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Battle not found"
        )
    
    # Convert ObjectIds to strings
    battle["_id"] = str(battle["_id"])
    
    # Get participant details
    participants_with_details = []
    for participant in battle.get("participants", []):
        user = await DatabaseOperations.get_user_by_id(str(participant["user"]))
        if user:
            participant_detail = {
                "user": {
                    "_id": str(user["_id"]),
                    "username": user["username"],
                    "country": user["country"],
                    "rank": user["rank"]
                },
                "damage": participant["damage"],
                "side": participant["side"]
            }
            participants_with_details.append(participant_detail)
    
    battle["participants_details"] = participants_with_details
    
    return {"battle": battle}

@router.post("/{battle_id}/fight", response_model=dict)
async def join_battle(
    battle_id: str,
    fight_data: BattleFight,
    current_user: dict = Depends(get_current_user)
):
    """Join a battle and deal damage"""
    
    battle = await DatabaseOperations.get_battle_by_id(battle_id)
    if not battle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Battle not found"
        )
    
    if battle["status"] != "ongoing":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Battle is not active"
        )
    
    # Check if user is already participating
    user_id = ObjectId(current_user["_id"])
    for participant in battle.get("participants", []):
        if participant["user"] == user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Already participating in this battle"
            )
    
    # Validate damage based on user strength
    max_damage = current_user["strength"] * random.randint(8, 12) // 10
    actual_damage = min(fight_data.damage, max_damage)
    
    # Add user to battle
    success = await DatabaseOperations.join_battle(
        battle_id, 
        current_user["_id"], 
        actual_damage, 
        fight_data.side
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to join battle"
        )
    
    # Update user experience and gold
    exp_gain = actual_damage // 10
    gold_gain = actual_damage // 50
    
    await DatabaseOperations.update_user(current_user["_id"], {
        "experience": current_user["experience"] + exp_gain,
        "gold": current_user["gold"] + gold_gain
    })
    
    # Check if battle should end (for demo purposes)
    updated_battle = await DatabaseOperations.get_battle_by_id(battle_id)
    total_damage = updated_battle["attacker_damage"] + updated_battle["defender_damage"]
    
    if total_damage > 100000:  # End battle at 100k total damage
        winner = "attacker" if updated_battle["attacker_damage"] > updated_battle["defender_damage"] else "defender"
        winner_country = updated_battle["attacker"] if winner == "attacker" else updated_battle["defender"]
        
        battles_collection = await DatabaseOperations.Collections.get_battles()
        await battles_collection.update_one(
            {"_id": ObjectId(battle_id)},
            {
                "$set": {
                    "status": "victory" if winner == "attacker" else "defeat",
                    "winner": winner_country,
                    "end_time": datetime.utcnow()
                }
            }
        )
        
        # Create news about battle result
        news_data = {
            "title": f"Beteja për {updated_battle['region']} përfundoi",
            "content": f"{winner_country} fitoi betejën për kontrollin e {updated_battle['region']}",
            "type": "military",
            "author": "Sistema e Lajmeve",
            "is_global": True,
            "countries": [updated_battle["attacker"], updated_battle["defender"]]
        }
        await DatabaseOperations.create_news(news_data)
    
    return {
        "message": "Successfully joined battle",
        "damage_dealt": actual_damage,
        "experience_gained": exp_gain,
        "gold_gained": gold_gain
    }

@router.post("/", response_model=dict)
async def create_battle(
    battle_data: dict,
    current_user: dict = Depends(get_current_admin_user)
):
    """Create a new battle (admin only)"""
    
    # Validate required fields
    required_fields = ["region", "attacker", "defender"]
    for field in required_fields:
        if field not in battle_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Missing required field: {field}"
            )
    
    # Check if countries exist
    attacker_country = await DatabaseOperations.get_country_by_code(battle_data["attacker"])
    defender_country = await DatabaseOperations.get_country_by_code(battle_data["defender"])
    
    if not attacker_country or not defender_country:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or both countries not found"
        )
    
    # Create battle
    new_battle = {
        "region": battle_data["region"],
        "attacker": battle_data["attacker"].lower(),
        "defender": battle_data["defender"].lower(),
        "status": "ongoing",
        "attacker_damage": 0,
        "defender_damage": 0,
        "participants": []
    }
    
    battle_id = await DatabaseOperations.create_battle(new_battle)
    
    # Create news about new battle
    news_data = {
        "title": f"Betejë e re në {battle_data['region']}",
        "content": f"{attacker_country['name']} ka nisur një sulm ndaj {defender_country['name']} për kontrollin e {battle_data['region']}",
        "type": "military",
        "author": "Sistema e Lajmeve",
        "is_global": True,
        "countries": [battle_data["attacker"].lower(), battle_data["defender"].lower()]
    }
    await DatabaseOperations.create_news(news_data)
    
    return {"message": "Battle created successfully", "battle_id": battle_id}

@router.put("/{battle_id}/end", response_model=dict)
async def end_battle(
    battle_id: str,
    winner_data: dict,
    current_user: dict = Depends(get_current_admin_user)
):
    """End a battle manually (admin only)"""
    
    battle = await DatabaseOperations.get_battle_by_id(battle_id)
    if not battle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Battle not found"
        )
    
    if battle["status"] != "ongoing":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Battle is not active"
        )
    
    winner = winner_data.get("winner")  # "attacker" or "defender"
    if winner not in ["attacker", "defender"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Winner must be 'attacker' or 'defender'"
        )
    
    winner_country = battle["attacker"] if winner == "attacker" else battle["defender"]
    
    # Update battle
    battles_collection = await DatabaseOperations.Collections.get_battles()
    await battles_collection.update_one(
        {"_id": ObjectId(battle_id)},
        {
            "$set": {
                "status": "victory" if winner == "attacker" else "defeat",
                "winner": winner_country,
                "end_time": datetime.utcnow()
            }
        }
    )
    
    # Create news
    loser_country = battle["defender"] if winner == "attacker" else battle["attacker"]
    news_data = {
        "title": f"Beteja për {battle['region']} përfundoi",
        "content": f"{winner_country} fitoi betejën kundër {loser_country} për kontrollin e {battle['region']}",
        "type": "military",
        "author": "Sistema e Lajmeve",
        "is_global": True,
        "countries": [battle["attacker"], battle["defender"]]
    }
    await DatabaseOperations.create_news(news_data)
    
    return {"message": f"Battle ended. Winner: {winner_country}"}