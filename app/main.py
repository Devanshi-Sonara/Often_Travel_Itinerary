from fastapi import FastAPI
from app.models import Base
from app.core.database import engine
from app.routers import itineraries, mcp
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # create tables automatically on first run (dev only)
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Travel Itinerary API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(itineraries.router)
app.include_router(mcp.router)
