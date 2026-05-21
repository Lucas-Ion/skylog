from src.database import Base
from sqlalchemy import String, Float, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column


class Airport(Base):
    __tablename__ = "airports"
    id: Mapped[int] = mapped_column(primary_key=True)
    icao_code: Mapped[str] = mapped_column(String(4), unique=True)
    iata_code: Mapped[str | None] = mapped_column(String(3), unique=True)
    name: Mapped[str] = mapped_column(String(45))
    city: Mapped[str] = mapped_column(String(45))
    country: Mapped[str] = mapped_column(String(2))
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    elevation_ft: Mapped[int] = mapped_column(Integer)
    timezone: Mapped[str | None ] = mapped_column(String(45))
