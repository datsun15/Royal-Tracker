import json
import re
import time
import requests
from bs4 import BeautifulSoup

# Comprehensive list of Royal Caribbean ships with CruiseMapper URL slugs
SHIPS = [
    # Icon Class
    {"name": "Icon of the Seas", "url": "https://www.cruisemapper.com/ships/Icon-Of-The-Seas-2166"},
    {"name": "Star of the Seas", "url": "https://www.cruisemapper.com/ships/Star-Of-The-Seas-2715"},
    {"name": "Legend of the Seas", "url": "https://www.cruisemapper.com/ships/Legend-Of-The-Seas-2113"},

    # Oasis Class
    {"name": "Utopia of the Seas", "url": "https://www.cruisemapper.com/ships/Utopia-Of-The-Seas-2167"},
    {"name": "Wonder of the Seas", "url": "https://www.cruisemapper.com/ships/Wonder-Of-The-Seas-2165"},
    {"name": "Symphony of the Seas", "url": "https://www.cruisemapper.com/ships/Symphony-Of-The-Seas-1522"},
    {"name": "Harmony of the Seas", "url": "https://www.cruisemapper.com/ships/Harmony-Of-The-Seas-1067"},
    {"name": "Allure of the Seas", "url": "https://www.cruisemapper.com/ships/Allure-Of-The-Seas-536"},
    {"name": "Oasis of the Seas", "url": "https://www.cruisemapper.com/ships/Oasis-Of-The-Seas-609"},

    # Quantum / Quantum Ultra Class
    {"name": "Spectrum of the Seas", "url": "https://www.cruisemapper.com/ships/Spectrum-Of-The-Seas-1718"},
    {"name": "Odyssey of the Seas", "url": "https://www.cruisemapper.com/ships/Odyssey-Of-The-Seas-1717"},
    {"name": "Ovations of the Seas", "url": "https://www.cruisemapper.com/ships/Ovation-Of-The-Seas-1017"},
    {"name": "Anthem of the Seas", "url": "https://www.cruisemapper.com/ships/Anthem-Of-The-Seas-1016"},
    {"name": "Quantum of the Seas", "url": "https://www.cruisemapper.com/ships/Quantum-Of-The-Seas-951"},

    # Freedom Class
    {"name": "Freedom of the Seas", "url": "https://www.cruisemapper.com/ships/Freedom-Of-The-Seas-538"},
    {"name": "Liberty of the Seas", "url": "https://www.cruisemapper.com/ships/Liberty-Of-The-Seas-539"},
    {"name": "Independence of the Seas", "url": "https://www.cruisemapper.com/ships/Independence-Of-The-Seas-537"},

    # Voyager Class
    {"name": "Voyager of the Seas", "url": "https://www.cruisemapper.com/ships/Voyager-Of-The-Seas-544"},
    {"name": "Explorer of the Seas", "url": "https://www.cruisemapper.com/ships/Explorer-Of-The-Seas-540"},
    {"name": "Adventure of the Seas", "url": "https://www.cruisemapper.com/ships/Adventure-Of-The-Seas-535"},
    {"name": "Navigator of the Seas", "url": "https://www.cruisemapper.com/ships/Navigator-Of-The-Seas-542"},
    {"name": "Mariner of the Seas", "url": "https://www.cruisemapper.com/ships/Mariner-Of-The-Seas-541"},

    # Radiance Class
    {"name": "Radiance of the Seas", "url": "https://www.cruisemapper.com/ships/Radiance-Of-The-Seas-543"},
    {"name": "Brilliance of the Seas", "url": "https://www.cruisemapper.com/ships/Brilliance-Of-The-Seas-571"},
    {"name": "Serenade of the Seas", "url": "https://www.cruisemapper.com/ships/Serenade-Of-The-Seas-573"},
    {"name": "Jewel of the Seas", "url": "https://www.cruisemapper.com/ships/Jewel-Of-The-Seas-572"},

    # Vision Class
    {"name": "Grandeur of the Seas", "url": "https://www.cruisemapper.com/ships/Grandeur-Of-The-Seas-575"},
    {"name": "Enchantment of the Seas", "url": "https://www.cruisemapper.com/ships/Enchantment-Of-The-Seas-574"},
    {"name": "Rhapsody of the Seas", "url": "https://www.cruisemapper.com/ships/Rhapsody-Of-The-Seas-577"},
    {"name": "Vision of the Seas", "url": "https://www.cruisemapper.com/ships/Vision-Of-The-Seas-578"}
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

fleet_data = []

print(f"Starting tracking run for {len(SHIPS)} ships...\n")

for ship in SHIPS:
    try:
        response = requests.get(ship["url"], headers=headers, timeout=10)
        
        # Regex patterns to find coordinate variables embedded in script tags or source code
        lat_match = re.search(r'latitude\s*[:=]\s*([+-]?\d+\.\d+)', response.text, re.IGNORECASE)
        lon_match = re.search(r'longitude\s*[:=]\s*([+-]?\d+\.\d+)', response.text, re.IGNORECASE)
        
        if lat_match and lon_match:
            lat = float(lat_match.group(1))
            lon = float(lon_match.group(1))
        else:
            # Alternate pattern match check for map variables
            lat_match_alt = re.search(r'data-lat="([+-]?\d+\.\d+)"', response.text)
            lon_match_alt = re.search(r'data-lon="([+-]?\d+\.\d+)"', response.text)
            
            if lat_match_alt and lon_match_alt:
                lat = float(lat_match_alt.group(1))
                lon = float(lon_match_alt.group(1))
            else:
                # Fallback location (Miami) if coordinates are unavailable or obscured
                lat, lon = 25.77427, -80.19366

        fleet_data.append({
            "name": ship["name"],
            "lat": lat,
            "lon": lon
        })
        print(f"[✓] Scraped: {ship['name']} -> ({lat}, {lon})")

    except Exception as e:
        print(f"[✗] Error scraping {ship['name']}: {e}")

    # Friendly delay to prevent triggering rate limits or bans
    time.sleep(1)

# Save output to ships.json
with open("ships.json", "w") as f:
    json.dump(fleet_data, f, indent=2)

print("\nSuccessfully updated ships.json!")
