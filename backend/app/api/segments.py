from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter
from pydantic import BaseModel

from app.database import supabase


router = APIRouter(tags=["segments"])


class SegmentCreate(BaseModel):
    filename: str
    segment_order: int


@router.post("/games/{game_id}/segments")
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


@router.get("/games/{game_id}/segments")
async def list_segments(game_id: str):
    result = (
        supabase.table("game_segments")
        .select("*")
        .eq("game_id", game_id)
        .order("segment_order")
        .execute()
    )
    return result.data