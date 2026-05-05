"""
Nakshatra Mapper
Single Responsibility: Map sidereal longitude to Nakshatra and Pada
"""
from server.domain.constants import (
    NAKSHATRAS,
    NAKSHATRA_SPAN_DEGREES,
    PADA_SPAN_DEGREES
)


class NakshatraMapper:
    """
    Maps sidereal longitude to Nakshatra and Pada.
    Follows SRP: Only responsible for Nakshatra mapping.
    """
    
    @staticmethod
    def longitude_to_nakshatra(sidereal_longitude: float) -> tuple[str, int, int]:
        """
        Convert sidereal longitude to Nakshatra name, index, and Pada.
        
        Args:
            sidereal_longitude: Sidereal longitude in degrees [0, 360)
            
        Returns:
            Tuple of (nakshatra_name, nakshatra_index, pada_number)
        """
        # Normalize to [0, 360)
        longitude = sidereal_longitude % 360.0
        
        # Calculate Nakshatra index (0-26)
        nakshatra_index = int(longitude / NAKSHATRA_SPAN_DEGREES)
        
        # Ensure index is within valid range
        if nakshatra_index >= len(NAKSHATRAS):
            nakshatra_index = len(NAKSHATRAS) - 1
        elif nakshatra_index < 0:
            nakshatra_index = 0
        
        nakshatra_name = NAKSHATRAS[nakshatra_index]
        
        # Calculate position within Nakshatra
        position_in_nakshatra = longitude - (nakshatra_index * NAKSHATRA_SPAN_DEGREES)
        
        # Calculate Pada (1-4)
        pada_number = int(position_in_nakshatra / PADA_SPAN_DEGREES) + 1
        
        # Ensure Pada is in valid range (1-4)
        if pada_number > 4:
            pada_number = 4
        elif pada_number < 1:
            pada_number = 1
        
        return nakshatra_name, nakshatra_index, pada_number

