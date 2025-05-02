from datetime import date, time, datetime
from typing import List
from pydantic import BaseModel, Field

# Activity
class ActivityBase(BaseModel):
    name: str
    description: str = ""
    start: time
    end: time
    price: float = 0

class ActivityCreate(ActivityBase): ...
class ActivityOut(ActivityBase):
    id: int
    class Config: orm_mode = True

# Transfer
class TransferBase(BaseModel):
    from_loc: str
    to_loc: str
    mode: str
    depart: time
    arrive: time

class TransferCreate(TransferBase): ...
class TransferOut(TransferBase):
    id: int
    class Config: orm_mode = True

# Accommodation
class AccommodationBase(BaseModel):
    hotel: str
    city: str
    check_in: date
    check_out: date

class AccommodationCreate(AccommodationBase): ...
class AccommodationOut(AccommodationBase):
    id: int
    class Config: orm_mode = True

# Day
class DayCreate(BaseModel):
    day_number: int = Field(gt=0)
    accommodations: List[AccommodationCreate] = []
    transfers: List[TransferCreate] = []
    activities: List[ActivityCreate] = []

class DayOut(DayCreate):
    id: int
    accommodations: List[AccommodationOut]
    transfers: List[TransferOut]
    activities: List[ActivityOut]
    class Config: orm_mode = True

# Itinerary
class ItineraryCreate(BaseModel):
    name: str
    region: str
    total_nights: int = Field(gt=0)
    days: List[DayCreate]

class ItineraryOut(BaseModel):
    id: int
    name: str
    region: str
    total_nights: int
    created_at: datetime
    days: List[DayOut]
    class Config: orm_mode = True
