from datetime import date, datetime
from uuid import uuid4

from fastapi import FastAPI
from pydantic import BaseModel

from app.database import supabase


app = FastAPI(title="Project Highlights API", version="0.2.0")


class EventCreate(BaseModel):
    name: str
    location: str | None = None
    start_date: date | None = None
    end_date: date | None = None


class GameCreate(BaseModel):
    title: str
    opponent: str | None = None
    game_date: date | None = None


class SegmentCreate(BaseModel):
    filename: str
    segment_order: int


@app.get("/")
async def root():
    return {"status": "online", "message": "Project Highlights API is running 🚀"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/events")
async def create_event(event: EventCreate):
    new_event = {
        "id": f"evt_{uuid4().hex[:8]}",
        "name": event.name,
        "location": event.location,
        "start_date": event.start_date.isoformat() if event.start_date else None,
        "end_date": event.end_date.isoformat() if event.end_date else None,
        "status": "created",
        "created_at": datetime.utcnow().isoformat(),
    }

    result = supabase.table("events").insert(new_event).execute()
    return result.data[0]


@app.get("/events")
async def list_events():
    result = supabase.table("events").select("*").execute()
    return result.data


@app.post("/events/{event_id}/games")
async def create_game(event_id: str, game: GameCreate):
    new_game = {
        "id": f"game_{uuid4().hex[:8]}",
        "event_id": event_id,
        "title": game.title,
        "opponent": game.opponent,
        "game_date": game.game_date.isoformat() if game.game_date else None,
        "status": "created",
        "created_at": datetime.utcnow().isoformat(),
    }

    result = supabase.table("games").insert(new_game).execute()
    return result.data[0]


@app.get("/events/{event_id}/games")
async def list_games(event_id: str):
    result = supabase.table("games").select("*").eq("event_id", event_id).execute()
    return result.data


@app.post("/games/{game_id}/segments")
async def create_segment(game_id: str, segment: SegmentCreate):
    new_segment = {
        "id": f"seg_{uuid4().hex[:8]}",
        "game_id": game_id,
        "filename": segment.filename,
        "segment_order": segment.segment_order,
        "status": "created",
        "created_at": datetime.utcnow().isoformat(),
    }

    result = supabase.table("game_segments").insert(new_segment).execute()
    return result.data[0]


@app.get("/games/{game_id}/segments")
async def list_segments(game_id: str):
    result = (
        supabase.table("game_segments")
        .select("*")
        .eq("game_id", game_id)
        .order("segment_order")
        .execute()
    )
    return result.data