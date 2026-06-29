from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter
from pydantic import BaseModel

from app.database import supabase


router = APIRouter(prefix="/events", tags=["events"])


class EventCreate(BaseModel):
    name: str
    location: str | None = None
    start_date: str | None = None
    end_date: str | None = None


@router.post("")
async def create_event(event: EventCreate):
    new_event = {
        "id": f"evt_{uuid4().hex[:8]}",
        "name": event.name,
        "location": event.location,
        "start_date": event.start_date,
        "end_date": event.end_date,
        "status": "created",
        "created_at": datetime.utcnow().isoformat(),
    }

    result = supabase.table("events").insert(new_event).execute()
    return result.data[0]


@router.get("")
async def list_events():
    result = supabase.table("events").select("*").execute()
    return result.data