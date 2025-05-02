from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app import models, schemas

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

@router.get("/", response_model=list[schemas.ItineraryOut])
def recommend(nights: int = Query(..., ge=1, le=30), db: Session = Depends(get_db)):
    exact = db.query(models.Itinerary).filter_by(total_nights=nights).all()
    if exact:
        return exact
    closest = db.query(models.Itinerary).all()
    return sorted(closest, key=lambda x: abs(x.total_nights - nights))[:3]
