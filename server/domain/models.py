"""
Domain models for Nadi calculation results
"""
from dataclasses import dataclass
from typing import Literal


@dataclass
class NadiResult:
    """Result of Nadi calculation"""
    nakshatra: str
    nakshatra_index: int
    pada: int
    nadi: Literal["Aadi", "Madhya", "Antya"]
    sidereal_longitude: float
    tropical_longitude: float
    accuracy: str
    
    def to_dict(self) -> dict:
        """Convert to dictionary for API response"""
        return {
            "nakshatra": self.nakshatra,
            "nakshatraIndex": self.nakshatra_index,
            "pada": self.pada,
            "nadi": self.nadi,
            "siderealLongitude": round(self.sidereal_longitude, 6),
            "tropicalLongitude": round(self.tropical_longitude, 6),
            "accuracy": self.accuracy
        }


@dataclass
class BirthDetails:
    """Birth details for calculation"""
    birth_date: str  # YYYY-MM-DD
    birth_time: str  # HH:MM
    timezone: str
    latitude: float
    longitude: float

