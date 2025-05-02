from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app import crud, schemas

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/itineraries", tags=["itineraries"])

@router.post("/", response_model=schemas.ItineraryOut, status_code=status.HTTP_201_CREATED)
def create(data: schemas.ItineraryCreate, db: Session = Depends(get_db)):
    return crud.create_itinerary(db, data)

@router.get("/", response_model=list[schemas.ItineraryOut])
def list_itineraries(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return crud.list_itineraries(db, skip, limit)

@router.get("/{itinerary_id}", response_model=schemas.ItineraryOut)
def read(itinerary_id: int, db: Session = Depends(get_db)):
    obj = crud.get_itinerary(db, itinerary_id)
    if not obj:
        raise HTTPException(404, detail="Itinerary not found")
    return obj
