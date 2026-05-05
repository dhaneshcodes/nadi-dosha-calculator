"""
Ayanamsa Calculator
Single Responsibility: Calculate Lahiri Ayanamsa for sidereal conversion
"""
import math
from server.domain.constants import (
    LAHIRI_REFERENCE_JD,
    LAHIRI_BASE_AYANAMSA,
    J2000_EPOCH
)


class AyanamsaCalculator:
    """
    Calculates Lahiri (Chitrapaksha) Ayanamsa.
    Follows SRP: Only responsible for Ayanamsa calculation.
    """
    
    @staticmethod
    def calculate_lahiri_ayanamsa(julian_date: float) -> float:
        """
        Calculate enhanced Lahiri Ayanamsa with nutation correction.
        
        Reference point: 285° on March 21, 1956 (Lahiri's definition)
        Includes nutation correction for improved accuracy.
        
        Args:
            julian_date: Julian date
            
        Returns:
            Ayanamsa in degrees
        """
        # Base Ayanamsa calculation
        days_from_reference = julian_date - LAHIRI_REFERENCE_JD
        years_from_reference = days_from_reference / 365.25
        base_ayanamsa = LAHIRI_BASE_AYANAMSA + 0.013888889 * years_from_reference
        
        # Julian centuries from J2000.0 for nutation
        t = (julian_date - J2000_EPOCH) / 36525.0
        
        # Calculate longitude of ascending node of Moon's orbit
        omega = (
            125.04452 -
            1934.136261 * t +
            0.0020708 * t * t +
            t * t * t / 450000.0
        )
        
        # Nutation correction (simplified)
        nutation_correction = -0.00569 - 0.00478 * math.sin(math.radians(omega))
        
        return base_ayanamsa + nutation_correction
    
    @staticmethod
    def tropical_to_sidereal(tropical_longitude: float, ayanamsa: float) -> float:
        """
        Convert tropical longitude to sidereal longitude.
        
        Args:
            tropical_longitude: Tropical longitude in degrees
            ayanamsa: Ayanamsa in degrees
            
        Returns:
            Sidereal longitude in degrees [0, 360)
        """
        sidereal = tropical_longitude - ayanamsa
        return ((sidereal % 360.0) + 360.0) % 360.0

