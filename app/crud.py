from sqlalchemy.orm import Session
from app import models, schemas

def create_itinerary(db: Session, data: schemas.ItineraryCreate) -> models.Itinerary:
    obj = models.Itinerary(
        name=data.name, region=data.region, total_nights=data.total_nights
    )
    for d in data.days:
        day = models.Day(day_number=d.day_number)
        day.accommodations = [models.Accommodation(**a.dict()) for a in d.accommodations]
        day.transfers      = [models.Transfer(**t.dict())      for t in d.transfers]
        day.activities     = [models.Activity(**ac.dict())     for ac in d.activities]
        obj.days.append(day)

    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_itinerary(db: Session, itinerary_id: int):
    return db.query(models.Itinerary).filter_by(id=itinerary_id).first()

def list_itineraries(db: Session, skip=0, limit=20):
    return db.query(models.Itinerary).offset(skip).limit(limit).all()
