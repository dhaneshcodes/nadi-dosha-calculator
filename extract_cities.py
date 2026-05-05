#!/usr/bin/env python3
"""
Extract Indian Cities Database from script.js to JSON file
"""
import re
import json
from pathlib import Path

def extract_database():
    """Extract INDIAN_CITIES_DATABASE from script.js"""
    script_path = Path("script.js")
    output_path = Path("server/data/indian_cities.json")
    
    if not script_path.exists():
        print("Error: script.js not found")
        return
    
    print("Reading script.js...")
    content = script_path.read_text(encoding='utf-8')
    
    # Find the database array
    pattern = r'const INDIAN_CITIES_DATABASE = \[(.*?)\];'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        print("Error: Could not find INDIAN_CITIES_DATABASE in script.js")
        return
    
    array_content = match.group(1)
    cities = []
    
    # Extract each city entry
    # Pattern: { place: '...', lat: ..., lon: ... }
    entry_pattern = r'\{[^}]+\}'
    for entry_match in re.finditer(entry_pattern, array_content):
        entry = entry_match.group(0)
        
        # Extract place
        place_match = re.search(r"place:\s*['\"]([^'\"]+)['\"]", entry)
        # Extract lat
        lat_match = re.search(r'lat:\s*([\d.]+)', entry)
        # Extract lon
        lon_match = re.search(r'lon:\s*([\d.]+)', entry)
        
        if place_match and lat_match and lon_match:
            cities.append({
                'place': place_match.group(1),
                'lat': float(lat_match.group(1)),
                'lon': float(lon_match.group(1))
            })
    
    # Remove duplicates
    seen = set()
    unique_cities = []
    for city in cities:
        key = city['place'].lower().strip()
        if key not in seen:
            seen.add(key)
            unique_cities.append(city)
    
    # Write to JSON
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(unique_cities, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Extracted {len(unique_cities)} unique cities")
    print(f"✅ Saved to {output_path}")

if __name__ == '__main__':
    extract_database()
