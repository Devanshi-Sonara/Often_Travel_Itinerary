# app/models.py
from datetime import datetime, date, time
from sqlalchemy import (
    String,
    Integer,
    Float,
    Date,
    Time,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


# ─────────────────────────────────────────────
#  ITINERARY  →  DAY  →  {Accommodation,Transfer,Activity}
# ─────────────────────────────────────────────
class Itinerary(Base):
    __tablename__ = "itineraries"

    id:            Mapped[int]       = mapped_column(Integer, primary_key=True)
    name:          Mapped[str]       = mapped_column(String(120))
    region:        Mapped[str]       = mapped_column(String(30))  # Phuket / Krabi
    total_nights:  Mapped[int]       = mapped_column(Integer)
    created_at:    Mapped[datetime]  = mapped_column(
        DateTime, default=datetime.utcnow
    )

    days: Mapped[list["Day"]] = relationship(
        back_populates="itinerary", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("idx_itinerary_region_nights", "region", "total_nights"),
    )


class Day(Base):
    __tablename__ = "days"

    id:           Mapped[int] = mapped_column(Integer, primary_key=True)
    itinerary_id: Mapped[int] = mapped_column(
        ForeignKey("itineraries.id", ondelete="CASCADE")
    )
    day_number:   Mapped[int] = mapped_column(Integer)       # 1-based sequence

    itinerary:      Mapped["Itinerary"] = relationship(back_populates="days")
    accommodations: Mapped[list["Accommodation"]] = relationship(
        cascade="all, delete-orphan"
    )
    transfers: Mapped[list["Transfer"]] = relationship(
        cascade="all, delete-orphan"
    )
    activities: Mapped[list["Activity"]] = relationship(
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("itinerary_id", "day_number", name="uix_day_per_itinerary"),
        Index("idx_day_itinerary", "itinerary_id"),
    )


class Accommodation(Base):
    __tablename__ = "accommodations"

    id:        Mapped[int]  = mapped_column(Integer, primary_key=True)
    day_id:    Mapped[int]  = mapped_column(ForeignKey("days.id", ondelete="CASCADE"))
    hotel:     Mapped[str]  = mapped_column(String(120))
    city:      Mapped[str]  = mapped_column(String(40))
    check_in:  Mapped[date] = mapped_column(Date)
    check_out: Mapped[date] = mapped_column(Date)


class Transfer(Base):
    __tablename__ = "transfers"

    id:        Mapped[int]  = mapped_column(Integer, primary_key=True)
    day_id:    Mapped[int]  = mapped_column(ForeignKey("days.id", ondelete="CASCADE"))
    from_loc:  Mapped[str]  = mapped_column(String(40))
    to_loc:    Mapped[str]  = mapped_column(String(40))
    mode:      Mapped[str]  = mapped_column(String(20))       # flight / ferry / taxi
    depart:    Mapped[time] = mapped_column(Time)
    arrive:    Mapped[time] = mapped_column(Time)


class Activity(Base):
    __tablename__ = "activities"

    id:          Mapped[int]    = mapped_column(Integer, primary_key=True)
    day_id:      Mapped[int]    = mapped_column(ForeignKey("days.id", ondelete="CASCADE"))
    name:        Mapped[str]    = mapped_column(String(120))
    description: Mapped[str]    = mapped_column(String(300))
    start:       Mapped[time]   = mapped_column(Time)
    end:         Mapped[time]   = mapped_column(Time)
    price:       Mapped[float]  = mapped_column(Float, default=0.0)
