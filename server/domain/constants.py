"""
Constants used in astronomical calculations
"""

# Nakshatras (27 lunar mansions)
NAKSHATRAS = [
    'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
    'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
    'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha', 'Moola',
    'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha',
    'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
]

# Nadi groups
NADI_GROUPS = {
    'Aadi': [
        'Ashwini', 'Ardra', 'Punarvasu', 'Uttara Phalguni', 'Hasta', 'Jyeshtha',
        'Moola', 'Shatabhisha', 'Purva Bhadrapada'
    ],
    'Madhya': [
        'Bharani', 'Mrigashira', 'Pushya', 'Purva Phalguni', 'Chitra', 'Anuradha',
        'Purva Ashadha', 'Dhanishta', 'Uttara Bhadrapada'
    ],
    'Antya': [
        'Krittika', 'Rohini', 'Ashlesha', 'Magha', 'Swati', 'Vishakha',
        'Uttara Ashadha', 'Shravana', 'Revati'
    ]
}

# Astronomical constants
J2000_EPOCH = 2451545.0  # Julian date for J2000.0 (Jan 1, 2000, 12:00 TT)
DAYS_PER_CENTURY = 36525.0
NAKSHATRA_SPAN_DEGREES = 360.0 / 27.0  # 13.333... degrees
PADA_SPAN_DEGREES = NAKSHATRA_SPAN_DEGREES / 4.0  # 3.333... degrees

# Lahiri Ayanamsa reference
LAHIRI_REFERENCE_JD = 2433282.5  # March 21, 1956, 0h UT
LAHIRI_BASE_AYANAMSA = 23.85

