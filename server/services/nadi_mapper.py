"""
Nadi Mapper
Single Responsibility: Map Nakshatra to Nadi type
"""
from typing import Literal
from server.domain.constants import NADI_GROUPS


class NadiMapper:
    """
    Maps Nakshatra to Nadi type.
    Follows SRP: Only responsible for Nadi mapping.
    """
    
    @staticmethod
    def nakshatra_to_nadi(nakshatra_name: str) -> Literal["Aadi", "Madhya", "Antya"]:
        """
        Get Nadi type for a given Nakshatra.
        
        Args:
            nakshatra_name: Name of the Nakshatra
            
        Returns:
            Nadi type ("Aadi", "Madhya", or "Antya")
        """
        for nadi_type, nakshatras in NADI_GROUPS.items():
            if nakshatra_name in nakshatras:
                return nadi_type  # type: ignore
        
        # Default fallback (should not happen with valid input)
        return "Aadi"

