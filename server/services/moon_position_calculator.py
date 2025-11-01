"""
Moon Position Calculator
Single Responsibility: Calculate Moon's ecliptic longitude
Uses IAU 2000B lunar elements and ELP2000-85 periodic terms
"""
import math
from typing import List, Tuple


class MoonPositionCalculator:
    """
    Calculates Moon's ecliptic longitude using enhanced lunar theory.
    Follows SRP: Only responsible for Moon position calculation.
    """
    
    # IAU 2000B Moon's mean elements coefficients
    MEAN_LONGITUDE_COEFFS = [218.3164477, 481267.88123421, -0.0015786, 1/538841.0, -1/65194000.0]
    ELONGATION_COEFFS = [297.8501921, 445267.1114034, -0.0018819, 1/545868.0, -1/113065000.0]
    SUN_ANOMALY_COEFFS = [357.5291092, 35999.0502909, -0.0001536, 1/24490000.0, 0]
    MOON_ANOMALY_COEFFS = [134.9633964, 477198.8675055, 0.0087414, 1/69699.0, -1/14712000.0]
    ARGUMENT_LATITUDE_COEFFS = [93.2720950, 483202.0175233, -0.0036539, -1/3526000.0, 1/863310000.0]
    
    # ELP2000-85 periodic terms (60 main terms)
    # Format: [coefficient (micro-degrees), D, M, M', F]
    LONGITUDE_TERMS: List[Tuple[int, int, int, int, int]] = [
        (6288774, 0, 0, 1, 0), (1274027, 2, 0, -1, 0), (658314, 2, 0, 0, 0),
        (213618, 0, 0, 2, 0), (-185116, 0, 1, 0, 0), (-114332, 0, 0, 0, 2),
        (58793, 2, 0, -2, 0), (57066, 2, -1, -1, 0), (53322, 2, 0, 1, 0),
        (45758, 2, -1, 0, 0), (-40923, 0, 1, -1, 0), (-34720, 1, 0, 0, 0),
        (-30383, 0, 1, 1, 0), (15327, 2, 0, 0, -2), (-12528, 0, 0, 1, 2),
        (10980, 0, 0, 1, -2), (10675, 4, 0, -1, 0), (10034, 0, 0, 3, 0),
        (8548, 4, 0, -2, 0), (-7888, 2, 1, -1, 0), (-6766, 2, 1, 0, 0),
        (-5163, 1, 0, -1, 0), (4987, 1, 1, 0, 0), (4036, 2, -1, 1, 0),
        (3994, 2, 0, 2, 0), (3861, 4, 0, 0, 0), (3665, 2, 0, -3, 0),
        (-2689, 0, 1, -2, 0), (-2602, 2, 0, -1, 2), (2390, 2, -1, -2, 0),
        (-2348, 1, 0, 1, 0), (2236, 2, -2, 0, 0), (-2120, 0, 1, 2, 0),
        (-2069, 0, 2, 0, 0), (2048, 2, -2, -1, 0), (-1773, 2, 0, 1, -2),
        (-1595, 2, 0, 0, 2), (1215, 4, -1, -1, 0), (-1110, 0, 0, 2, 2),
        (-892, 3, 0, -1, 0), (-810, 2, 1, 1, 0), (759, 4, -1, -2, 0),
        (-713, 0, 2, -1, 0), (-700, 2, 2, -1, 0), (691, 2, 1, -2, 0),
        (596, 2, -1, 0, -2), (549, 4, 0, 1, 0), (537, 0, 0, 4, 0),
        (520, 4, -1, 0, 0), (-487, 1, 0, -2, 0), (-399, 2, 1, 0, -2),
        (-381, 0, 0, 2, -2), (351, 1, 1, 1, 0), (-340, 3, 0, -2, 0),
        (330, 4, 0, -3, 0), (327, 2, -1, 2, 0), (-323, 0, 2, 1, 0),
        (299, 1, 1, -1, 0), (294, 2, 0, 3, 0)
    ]
    
    @staticmethod
    def _normalize_degrees(angle: float) -> float:
        """Normalize angle to [0, 360) degrees"""
        return ((angle % 360.0) + 360.0) % 360.0
    
    @staticmethod
    def _polynomial(coeffs: List[float], t: float) -> float:
        """Calculate polynomial: c0 + c1*T + c2*T^2 + c3*T^3 + c4*T^4"""
        result = coeffs[0]
        t_power = t
        for i in range(1, len(coeffs)):
            result += coeffs[i] * t_power
            t_power *= t
        return result
    
    @classmethod
    def calculate_tropical_longitude(cls, julian_centuries: float) -> float:
        """
        Calculate Moon's tropical ecliptic longitude.
        
        Uses IAU 2000B mean elements and ELP2000-85 periodic terms.
        Accuracy: ±0.5 arc-minutes
        
        Args:
            julian_centuries: Julian centuries from J2000.0 (T)
            
        Returns:
            Tropical longitude in degrees [0, 360)
        """
        t = julian_centuries
        
        # Calculate mean elements
        L_prime = cls._normalize_degrees(cls._polynomial(cls.MEAN_LONGITUDE_COEFFS, t))
        D = cls._normalize_degrees(cls._polynomial(cls.ELONGATION_COEFFS, t))
        M = cls._normalize_degrees(cls._polynomial(cls.SUN_ANOMALY_COEFFS, t))
        M_prime = cls._normalize_degrees(cls._polynomial(cls.MOON_ANOMALY_COEFFS, t))
        F = cls._normalize_degrees(cls._polynomial(cls.ARGUMENT_LATITUDE_COEFFS, t))
        
        # Start with mean longitude
        lambda_tropical = L_prime
        
        # Add periodic terms (coefficients in micro-degrees)
        for coeff_microdeg, d, m, mp, f in cls.LONGITUDE_TERMS:
            argument = math.radians(d * D + m * M + mp * M_prime + f * F)
            correction = (coeff_microdeg / 1000000.0) * math.sin(argument)
            lambda_tropical += correction
        
        return cls._normalize_degrees(lambda_tropical)

