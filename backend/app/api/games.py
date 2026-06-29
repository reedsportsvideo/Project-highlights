from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter
from pydantic import BaseModel

from app.database import supabase


router = APIRouter(tags=["games"])


class GameCreate(BaseModel):
    title: str
    opponent: str | None = None
    game_date: str | None = None


@router.post("/events/{event_id}/games")
async def create_game(event_id: str, game: GameCreate):
    new_game = {
        "id": f"game_{uuid4().hex[:8]}",
        "event_id": event_id,
        "title": game.title,
        "opponent": game.opponent,
        "game_date": game.game_date,
        "status": "created",
        "created_at": datetime.utcnow().isoformat(),
    }

    result = supabase.table("games").insert(new_game).execute()
    return result.data[0]


@router.get("/events/{event_id}/games")
async def list_games(event_id: str):
    result = supabase.table("games").select("*").eq("event_id", event_id).execute()
    return result.data