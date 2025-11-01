"""
Julian Date Calculator
Single Responsibility: Convert calendar dates to Julian dates
"""
from datetime import datetime
from typing import Optional
import math


class JulianDateCalculator:
    """
    Calculates Julian dates from Gregorian calendar dates.
    Follows SRP: Only responsible for Julian date conversion.
    """
    
    @staticmethod
    def from_ut_datetime(ut_datetime: datetime) -> float:
        """
        Calculate Julian date from UTC datetime.
        
        Formula based on: https://aa.usno.navy.mil/faq/julian-date
        
        Args:
            ut_datetime: UTC datetime object
            
        Returns:
            Julian date as float
        """
        year = ut_datetime.year
        month = ut_datetime.month
        day = ut_datetime.day
        
        # Convert time to decimal hours
        hours = ut_datetime.hour
        minutes = ut_datetime.minute
        seconds = ut_datetime.second
        ut_decimal = hours + minutes / 60.0 + seconds / 3600.0
        
        # Adjust for months <= 2 (treat as previous year)
        if month <= 2:
            year -= 1
            month += 12
        
        # Calculate Gregorian calendar adjustment
        a = math.floor(year / 100)
        b = 2 - a + math.floor(a / 4)
        
        # Julian Day Number at 0h UT
        jd0 = (
            math.floor(365.25 * (year + 4716)) +
            math.floor(30.6001 * (month + 1)) +
            day + b - 1524.5
        )
        
        # Add fractional day
        return jd0 + ut_decimal / 24.0
    
    @staticmethod
    def from_date_time_strings(
        date_str: str,
        time_str: str,
        timezone_offset: float
    ) -> Optional[float]:
        """
        Calculate Julian date from date/time strings and timezone offset.
        
        Args:
            date_str: Date in YYYY-MM-DD format
            time_str: Time in HH:MM format
            timezone_offset: Timezone offset in hours (UTC offset)
            
        Returns:
            Julian date or None if parsing fails
        """
        try:
            # Parse date
            date_parts = date_str.split('-')
            if len(date_parts) != 3:
                return None
            
            year = int(date_parts[0])
            month = int(date_parts[1])
            day = int(date_parts[2])
            
            # Parse time
            time_parts = time_str.split(':')
            if len(time_parts) != 2:
                return None
            
            hour = int(time_parts[0])
            minute = int(time_parts[1])
            
            # Convert to UTC (subtract timezone offset)
            utc_hour = hour - timezone_offset
            utc_minute = minute
            
            # Handle overflow/underflow
            while utc_hour >= 24:
                utc_hour -= 24
                day += 1
            while utc_hour < 0:
                utc_hour += 24
                day -= 1
            
            # Create UTC datetime
            ut_datetime = datetime(
                year, month, day,
                int(utc_hour), utc_minute, 0
            )
            
            return JulianDateCalculator.from_ut_datetime(ut_datetime)
            
        except (ValueError, IndexError, AttributeError):
            return None
    
    @staticmethod
    def to_julian_centuries(julian_date: float) -> float:
        """
        Convert Julian date to Julian centuries from J2000.0 epoch.
        
        Args:
            julian_date: Julian date
            
        Returns:
            Julian centuries (T) from J2000.0
        """
        from server.domain.constants import J2000_EPOCH, DAYS_PER_CENTURY
        return (julian_date - J2000_EPOCH) / DAYS_PER_CENTURY

