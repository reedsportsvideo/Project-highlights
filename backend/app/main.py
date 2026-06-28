from datetime import datetime
from uuid import uuid4

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(
    title="Project Highlights API",
    version="0.1.0"
)


class ProjectCreate(BaseModel):
    player_name: str
    team: str
    jersey_number: int
    position: str


class Project(ProjectCreate):
    id: str
    status: str
    created_at: str


projects: list[Project] = []


@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Project Highlights API is running 🚀"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/projects", response_model=Project)
async def create_project(project: ProjectCreate):
    new_project = Project(
        id=f"proj_{uuid4().hex[:8]}",
        status="created",
        created_at=datetime.utcnow().isoformat(),
        **project.model_dump()
    )

    projects.append(new_project)
    return new_project


@app.get("/projects", response_model=list[Project])
async def list_projects():
    return projects