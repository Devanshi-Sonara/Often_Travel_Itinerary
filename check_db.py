from app.core.database import SessionLocal
from app.models import Itinerary

db = SessionLocal()

itineraries = db.query(Itinerary).all()
for i in itineraries:
    print(f"[{i.id}] {i.name} ({i.total_nights} nights) in {i.region}")
