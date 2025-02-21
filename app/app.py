# app/app.py
from fastapi import FastAPI
from api.routers import health
from core.logging import configure_logging

app = FastAPI(title="PyPerfect API", version="0.1.0")

# Configure logging
configure_logging()

# Include routes
app.include_router(health.router)

@app.get("/")
async def root():
    return {"message": "Welcome to PyPerfect"}
