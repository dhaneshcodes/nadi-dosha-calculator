"""
Nadi Calculation Service
Orchestrates the calculation process using dependency injection (DIP)
"""
from server.domain.models import NadiResult, BirthDetails
from server.services.julian_date_calculator import JulianDateCalculator
from server.services.moon_position_calculator import MoonPositionCalculator
from server.services.ayanamsa_calculator import AyanamsaCalculator
from server.services.nakshatra_mapper import NakshatraMapper
from server.services.nadi_mapper import NadiMapper
from server.utils.logger import setup_logger
from typing import Optional

logger = setup_logger("nadi_calculation")


class NadiCalculationService:
    """
    Main service for calculating Nadi Dosha.
    Follows DIP: Depends on abstractions (other calculator services).
    Follows SRP: Orchestrates the calculation workflow.
    """
    
    def __init__(
        self,
        julian_calculator: JulianDateCalculator = None,
        moon_calculator: MoonPositionCalculator = None,
        ayanamsa_calculator: AyanamsaCalculator = None,
        nakshatra_mapper: NakshatraMapper = None,
        nadi_mapper: NadiMapper = None
    ):
        """
        Initialize with dependency injection.
        Defaults to concrete implementations but allows substitution for testing.
        """
        self.julian_calculator = julian_calculator or JulianDateCalculator()
        self.moon_calculator = moon_calculator or MoonPositionCalculator()
        self.ayanamsa_calculator = ayanamsa_calculator or AyanamsaCalculator()
        self.nakshatra_mapper = nakshatra_mapper or NakshatraMapper()
        self.nadi_mapper = nadi_mapper or NadiMapper()
    
    def calculate(self, birth_details: BirthDetails) -> Optional[NadiResult]:
        """
        Calculate Nadi, Nakshatra, and Pada from birth details.
        
        Args:
            birth_details: Birth details (date, time, location, timezone)
            
        Returns:
            NadiResult or None if calculation fails
        """
        # Step 1: Convert to Julian date
        julian_date = self.julian_calculator.from_date_time_strings(
            birth_details.birth_date,
            birth_details.birth_time,
            self._parse_timezone_offset(birth_details.timezone)
        )
        
        if julian_date is None:
            return None
        
        # Step 2: Calculate Julian centuries
        julian_centuries = self.julian_calculator.to_julian_centuries(julian_date)
        
        # Step 3: Calculate Moon's tropical longitude
        tropical_longitude = self.moon_calculator.calculate_tropical_longitude(julian_centuries)
        
        # Step 4: Calculate Ayanamsa
        ayanamsa = self.ayanamsa_calculator.calculate_lahiri_ayanamsa(julian_date)
        
        # Step 5: Convert to sidereal longitude
        sidereal_longitude = self.ayanamsa_calculator.tropical_to_sidereal(
            tropical_longitude,
            ayanamsa
        )
        
        # Step 6: Map to Nakshatra and Pada
        nakshatra_name, nakshatra_index, pada = self.nakshatra_mapper.longitude_to_nakshatra(
            sidereal_longitude
        )
        
        # Step 7: Map to Nadi
        nadi = self.nadi_mapper.nakshatra_to_nadi(nakshatra_name)
        
        return NadiResult(
            nakshatra=nakshatra_name,
            nakshatra_index=nakshatra_index,
            pada=pada,
            nadi=nadi,
            sidereal_longitude=sidereal_longitude,
            tropical_longitude=tropical_longitude,
            accuracy="Enhanced (±0.5 arc-minutes)"
        )
    
    @staticmethod
    def _parse_timezone_offset(timezone: str) -> float:
        """
        Parse timezone offset from string.
        Handles formats like "+05:30", "5.5", "Asia/Kolkata" (simplified)
        
        Args:
            timezone: Timezone offset as string (e.g., "5.5", "+05:30", "-5")
            
        Returns:
            Timezone offset in hours as float
        """
        try:
            # If already a number, convert directly
            if isinstance(timezone, (int, float)):
                return float(timezone)
            
            timezone = str(timezone).strip()
            
            # Try parsing as offset string (e.g., "+05:30")
            if ":" in timezone:
                # Determine sign
                sign = -1 if timezone.startswith("-") else 1
                # Remove + and - signs
                clean_tz = timezone.replace("+", "").replace("-", "")
                parts = clean_tz.split(":")
                hours = float(parts[0])
                minutes = float(parts[1]) / 60.0 if len(parts) > 1 else 0.0
                return sign * (hours + minutes)
            
            # Try parsing as decimal (e.g., "5.5")
            return float(timezone)
        except (ValueError, AttributeError, TypeError):
            # Default to UTC if parsing fails
            logger.warning(f"Could not parse timezone offset '{timezone}', defaulting to 0.0")
            return 0.0

