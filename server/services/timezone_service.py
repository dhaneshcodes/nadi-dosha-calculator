"""
Timezone Service
Handles timezone detection from coordinates or geocoding data
"""
from typing import Optional, Dict
import urllib.request
import urllib.parse
import json
from server.utils.logger import setup_logger

logger = setup_logger("timezone")


class TimezoneService:
    """
    Timezone detection service.
    Follows SRP: Only responsible for timezone detection.
    """
    
    @staticmethod
    async def get_timezone(lat: float, lon: float, geocode_data: Optional[Dict] = None) -> float:
        """
        Get timezone offset in hours from coordinates.
        
        Args:
            lat: Latitude
            lon: Longitude
            geocode_data: Optional geocoding data (may contain timezone)
            
        Returns:
            Timezone offset in hours (e.g., 5.5 for IST)
        """
        # If geocoding provided exact timezone, use it
        if geocode_data and geocode_data.get('timezone_exact') and geocode_data.get('timezone'):
            tz_name = geocode_data['timezone']
            try:
                return TimezoneService._parse_timezone_offset(tz_name)
            except:
                pass
        
        # Try TimeAPI
        try:
            timeapi_url = f'https://timeapi.io/api/TimeZone/coordinate?latitude={lat}&longitude={lon}'
            req = urllib.request.Request(timeapi_url)
            
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                
                if 'utcOffset' in data:
                    # Convert "05:30:00" to 5.5
                    offset_str = data['utcOffset']
                    return TimezoneService._parse_timezone_offset(offset_str)
        except Exception as e:
            logger.warning(f"TimeAPI failed: {e}")
        
        # Fallback: Estimate from longitude
        # Approximate: 1 hour = 15 degrees longitude
        estimated_offset = lon / 15.0
        logger.debug(f"Using estimated timezone offset from longitude: {estimated_offset}")
        return estimated_offset
    
    @staticmethod
    def _parse_timezone_offset(offset_str: str) -> float:
        """
        Parse timezone offset string to float hours.
        Handles formats like "+05:30", "5.5", "05:30:00"
        """
        offset_str = str(offset_str).strip()
        
        # Handle +/- signs
        sign = 1
        if offset_str.startswith('-'):
            sign = -1
            offset_str = offset_str[1:]
        elif offset_str.startswith('+'):
            offset_str = offset_str[1:]
        
        # Try parsing as decimal (e.g., "5.5")
        try:
            return sign * float(offset_str)
        except ValueError:
            pass
        
        # Try parsing as HH:MM or HH:MM:SS
        if ':' in offset_str:
            parts = offset_str.split(':')
            hours = float(parts[0])
            minutes = float(parts[1]) / 60.0 if len(parts) > 1 else 0.0
            return sign * (hours + minutes)
        
        # Default
        return 0.0


timezone_service = TimezoneService()

