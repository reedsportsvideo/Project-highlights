from fastapi import FastAPI

from app.api.events import router as events_router
from app.api.games import router as games_router
from app.api.segments import router as segments_router


app = FastAPI(title="Project Highlights API", version="0.2.0")

app.include_router(events_router)
app.include_router(games_router)
app.include_router(segments_router)


@app.get("/")
async def root():
    return {"status": "online", "message": "Project Highlights API is running 🚀"}


@app.get("/health")
async def health():
    return {"status": "healthy"}