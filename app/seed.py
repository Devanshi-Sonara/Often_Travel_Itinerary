from datetime import date, time
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app import models

def seed():
    db: Session = SessionLocal()
    db.query(models.Itinerary).delete()
    db.commit()

    packages = [
        ("Phuket Highlights 3N", "Phuket", 3),
        ("Krabi Escape 4N",     "Krabi",  4),
        ("Phuket-Krabi Combo 6N","Phuket", 6),
        ("Southern Thailand 8N","Krabi",  8),
    ]

    for title, region, nights in packages:
        iti = models.Itinerary(name=title, region=region, total_nights=nights)
        for d in range(1, nights + 1):
            day = models.Day(day_number=d)
            day.accommodations.append(models.Accommodation(
                hotel="Sample Resort",
                city=region,
                check_in=date(2025, 6, d),
                check_out=date(2025, 6, d+1)
            ))
            day.activities.append(models.Activity(
                name="Island Tour",
                description="Boat excursion",
                start=time(8,0),
                end=time(16,0),
                price=99.0
            ))
            iti.days.append(day)
        db.add(iti)
    db.commit()
    db.close()
    print("Seeded ✔")

if __name__ == "__main__":
    seed()
