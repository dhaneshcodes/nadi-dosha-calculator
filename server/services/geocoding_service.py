"""
Geocoding Service
Handles location geocoding with database-first approach
"""
import json
from typing import Optional, Dict, List, Tuple
from pathlib import Path
from server.utils.logger import setup_logger

logger = setup_logger("geocoding")

# Load Indian cities database
INDIAN_CITIES_DATABASE = []

def load_database():
    """Load Indian cities database from JSON file"""
    global INDIAN_CITIES_DATABASE
    if INDIAN_CITIES_DATABASE:
        return  # Already loaded
    
    try:
        # Try loading from JSON file
        json_path = Path(__file__).parent.parent / "data" / "indian_cities.json"
        if json_path.exists():
            with open(json_path, 'r', encoding='utf-8') as f:
                INDIAN_CITIES_DATABASE = json.load(f)
                logger.info(f"Loaded {len(INDIAN_CITIES_DATABASE)} cities from database")
                return
    except Exception as e:
        logger.warning(f"Could not load database from JSON: {e}")
    
    # Fallback: Try extracting from script.js
    try:
        script_path = Path(__file__).parent.parent.parent / "script.js"
        if script_path.exists():
            content = script_path.read_text(encoding='utf-8')
            # Extract database array using regex
            import re
            # Find the array definition
            pattern = r'const INDIAN_CITIES_DATABASE = \[(.*?)\];'
            match = re.search(pattern, content, re.DOTALL)
            if match:
                array_content = match.group(1)
                # Parse individual entries
                entries = re.findall(r'\{[^}]+\}', array_content)
                for entry in entries:
                    place_match = re.search(r"place:\s*['\"]([^'\"]+)['\"]", entry)
                    lat_match = re.search(r"lat:\s*([\d.]+)", entry)
                    lon_match = re.search(r"lon:\s*([\d.]+)", entry)
                    if place_match and lat_match and lon_match:
                        INDIAN_CITIES_DATABASE.append({
                            'place': place_match.group(1),
                            'lat': float(lat_match.group(1)),
                            'lon': float(lon_match.group(1))
                        })
                logger.info(f"Extracted {len(INDIAN_CITIES_DATABASE)} cities from script.js")
                return
    except Exception as e:
        logger.warning(f"Could not extract database from script.js: {e}")
    
    # Initialize with minimal cities if database not loaded
    if not INDIAN_CITIES_DATABASE:
        logger.warning("Using minimal city database - some cities may not be found")
        INDIAN_CITIES_DATABASE = [
            {'place': 'Mumbai, Maharashtra, India', 'lat': 19.0760, 'lon': 72.8777},
            {'place': 'Delhi, India', 'lat': 28.7041, 'lon': 77.1025},
            {'place': 'Bangalore, Karnataka, India', 'lat': 12.9716, 'lon': 77.5946},
            {'place': 'Hyderabad, Telangana, India', 'lat': 17.3850, 'lon': 78.4867},
            {'place': 'Chennai, Tamil Nadu, India', 'lat': 13.0827, 'lon': 80.2707},
            {'place': 'Adoni, Andhra Pradesh, India', 'lat': 15.6281, 'lon': 77.2750},
        ]

# Load on module import
load_database()


class GeocodingService:
    """
    Geocoding service with database-first approach.
    Follows SRP: Only responsible for geocoding.
    """
    
    def __init__(self):
        self.cache: Dict[str, Dict] = {}
        load_database()
    
    def lookup_in_database(self, place: str) -> Optional[Dict[str, float]]:
        """
        Search local database first (fastest, no network).
        
        Args:
            place: Place name to search
            
        Returns:
            Dict with lat/lon or None if not found
        """
        normalized = place.lower().strip()
        place_parts = normalized.split(',')
        city_name = place_parts[0].strip().lower()
        
        # Try exact match
        for city in INDIAN_CITIES_DATABASE:
            if city['place'].lower() == normalized:
                logger.debug(f"Database exact match: {place}")
                return {'lat': city['lat'], 'lon': city['lon']}
        
        # Try fuzzy match (city name only)
        for city in INDIAN_CITIES_DATABASE:
            db_city_name = city['place'].split(',')[0].strip().lower()
            if db_city_name == city_name:
                logger.debug(f"Database fuzzy match: {place} → {city['place']}")
                return {'lat': city['lat'], 'lon': city['lon']}
        
        # Try partial match
        for city in INDIAN_CITIES_DATABASE:
            db_place = city['place'].lower()
            if city_name in db_place or db_place.split(',')[0] in city_name:
                logger.debug(f"Database partial match: {place} → {city['place']}")
                return {'lat': city['lat'], 'lon': city['lon']}
        
        return None
    
    async def geocode(self, place: str) -> Dict[str, float]:
        """
        Geocode a place name to coordinates.
        Uses database-first, then APIs.
        
        Args:
            place: Place name to geocode
            
        Returns:
            Dict with lat, lon, and source
        """
        # Step 1: Check database
        db_result = self.lookup_in_database(place)
        if db_result:
            return {**db_result, 'source': 'Indian Cities Database'}
        
        # Step 2: Check cache (in-memory for session)
        if place in self.cache:
            cached = self.cache[place]
            return {**cached, 'source': f"{cached.get('source', 'Cached')} (cached)"}
        
        # Step 3: Use geocoding API
        try:
            import urllib.request
            import urllib.parse
            
            # Try geocode.prateekanand.com first
            city_name = place.split(',')[0].strip()
            geocode_url = f'https://geocode.prateekanand.com/geocode?city={urllib.parse.quote(city_name)}&limit=5'
            
            req = urllib.request.Request(
                geocode_url,
                headers={'Accept': 'application/json', 'User-Agent': 'NadiDoshaCalculator/1.0'}
            )
            
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                
                if data and isinstance(data, list) and len(data) > 0:
                    # Sort by population
                    sorted_data = sorted(data, key=lambda x: x.get('population', 0), reverse=True)
                    best = sorted_data[0]
                    
                    result = {
                        'lat': float(best['latitude']),
                        'lon': float(best['longitude']),
                        'source': 'Geocode API',
                        'timezone': best.get('timezone'),
                        'timezone_exact': True
                    }
                    
                    # Cache result
                    self.cache[place] = result
                    return result
        except Exception as e:
            logger.warning(f"Geocode API failed for {place}: {e}")
        
        # Fallback to Photon API
        try:
            import urllib.request
            import urllib.parse
            
            photon_url = f'https://photon.komoot.io/api/?q={urllib.parse.quote(place)}&limit=1'
            req = urllib.request.Request(photon_url)
            
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                
                if data and 'features' in data and len(data['features']) > 0:
                    coords = data['features'][0]['geometry']['coordinates']
                    result = {
                        'lat': float(coords[1]),
                        'lon': float(coords[0]),
                        'source': 'Photon API'
                    }
                    
                    self.cache[place] = result
                    return result
        except Exception as e:
            logger.warning(f"Photon API failed for {place}: {e}")
        
        raise ValueError(f"Could not geocode place: {place}")


geocoding_service = GeocodingService()

