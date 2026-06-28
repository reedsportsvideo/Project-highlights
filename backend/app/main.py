from fastapi import FastAPI

app = FastAPI(
    title="Project Highlights API",
    version="0.1.0"
)

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Project Highlights API is running 🚀"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }