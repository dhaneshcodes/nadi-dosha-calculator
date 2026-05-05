"""
Pydantic schemas for API request/response validation
"""
from pydantic import BaseModel, validator, Field
from typing import Optional, List


class PersonBirthDetails(BaseModel):
    """Birth details for a single person"""
    name: Optional[str] = Field(None, description="Person name")
    birth_date: str = Field(..., description="Date in YYYY-MM-DD format")
    birth_time: str = Field(..., description="Time in HH:MM format (24-hour)")
    place_of_birth: str = Field(..., description="Place of birth (city, state, country)")
    
    @validator('birth_date')
    def validate_date_format(cls, v):
        """Validate date format YYYY-MM-DD"""
        parts = v.split('-')
        if len(parts) != 3:
            raise ValueError('Date must be in YYYY-MM-DD format')
        try:
            year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
            if not (1900 <= year <= 2100):
                raise ValueError('Year must be between 1900 and 2100')
            if not (1 <= month <= 12):
                raise ValueError('Month must be between 1 and 12')
            if not (1 <= day <= 31):
                raise ValueError('Day must be between 1 and 31')
        except ValueError as e:
            if 'invalid literal' in str(e).lower():
                raise ValueError('Date must contain valid numbers')
            raise
        return v
    
    @validator('birth_time')
    def validate_time_format(cls, v):
        """Validate time format HH:MM"""
        parts = v.split(':')
        if len(parts) != 2:
            raise ValueError('Time must be in HH:MM format (24-hour)')
        try:
            hour, minute = int(parts[0]), int(parts[1])
            if not (0 <= hour <= 23):
                raise ValueError('Hour must be between 0 and 23')
            if not (0 <= minute <= 59):
                raise ValueError('Minute must be between 0 and 59')
        except ValueError as e:
            if 'invalid literal' in str(e).lower():
                raise ValueError('Time must contain valid numbers')
            raise
        return v
    
    @validator('place_of_birth')
    def validate_place(cls, v):
        """Validate place of birth is not empty"""
        if not v or not v.strip():
            raise ValueError('Place of birth is required')
        if len(v.strip()) < 2:
            raise ValueError('Place of birth must be at least 2 characters')
        return v.strip()


class NadiCalculationRequest(BaseModel):
    """Request schema for Nadi calculation - complete workflow"""
    person1: PersonBirthDetails = Field(..., description="First person details")
    person2: Optional[PersonBirthDetails] = Field(None, description="Second person details (for comparison mode)")


class CalculationRequest(BaseModel):
    """Legacy request schema for Nadi calculation (deprecated - use NadiCalculationRequest)"""
    birth_date: str = Field(..., description="Date in YYYY-MM-DD format")
    birth_time: str = Field(..., description="Time in HH:MM format (24-hour)")
    timezone: str = Field(..., description="Timezone offset (e.g., '5.5', '+05:30')")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude in degrees")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude in degrees")
    
    @validator('birth_date')
    def validate_date_format(cls, v):
        """Validate date format YYYY-MM-DD"""
        parts = v.split('-')
        if len(parts) != 3:
            raise ValueError('Date must be in YYYY-MM-DD format')
        try:
            year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
            if not (1900 <= year <= 2100):
                raise ValueError('Year must be between 1900 and 2100')
            if not (1 <= month <= 12):
                raise ValueError('Month must be between 1 and 12')
            if not (1 <= day <= 31):
                raise ValueError('Day must be between 1 and 31')
        except ValueError as e:
            if 'invalid literal' in str(e).lower():
                raise ValueError('Date must contain valid numbers')
            raise
        return v
    
    @validator('birth_time')
    def validate_time_format(cls, v):
        """Validate time format HH:MM"""
        parts = v.split(':')
        if len(parts) != 2:
            raise ValueError('Time must be in HH:MM format')
        try:
            hour, minute = int(parts[0]), int(parts[1])
            if not (0 <= hour <= 23):
                raise ValueError('Hour must be between 0 and 23')
            if not (0 <= minute <= 59):
                raise ValueError('Minute must be between 0 and 59')
        except ValueError as e:
            if 'invalid literal' in str(e).lower():
                raise ValueError('Time must contain valid numbers')
            raise
        return v


class PersonNadiResult(BaseModel):
    """Nadi calculation result for a single person"""
    name: Optional[str] = None
    nakshatra: str
    nakshatraIndex: int
    pada: int
    nadi: str
    siderealLongitude: float
    tropicalLongitude: float
    accuracy: str


class NadiComparisonResult(BaseModel):
    """Complete Nadi Dosha comparison result"""
    person1: PersonNadiResult
    person2: Optional[PersonNadiResult] = None
    hasDosha: bool = Field(..., description="Whether Nadi Dosha exists")
    doshaType: Optional[str] = Field(None, description="Type of dosha (if any)")
    compatible: bool = Field(..., description="Whether the match is compatible")
    message: str = Field(..., description="Compatibility message")


class CalculationResponse(BaseModel):
    """Legacy response schema for Nadi calculation"""
    nakshatra: str
    nakshatraIndex: int
    pada: int
    nadi: str
    siderealLongitude: float
    tropicalLongitude: float
    accuracy: str


class ErrorResponse(BaseModel):
    """Error response schema"""
    error: str
    detail: Optional[str] = None

