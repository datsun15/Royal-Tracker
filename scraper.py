import json
import re
import time
import requests

# Royal Caribbean Fleet with IMO numbers (IMO numbers never change and provide direct lookups)
SHIPS = [
    {"name": "Icon of the Seas", "imo": "9829930", "url": "https://www.cruisemapper.com/ships/Icon-Of-The-Seas-2110"},
    {"name": "Symphony of the Seas", "imo": "9744001", "url": "https://www.cruisemapper.com/ships/Symphony-Of-The-Seas-1730"},
    {"name": "Wonder of the Seas", "imo": "9863345", "url": "https://www.cruisemapper.com/ships/Wonder-Of-The-Seas-2165"},
    {"name": "Utopia of the Seas", "imo": "9880001", "url": "https://www.cruisemapper.com/ships/Utopia-Of-The-Seas-2167"},
    {"name": "Oasis of the Seas", "imo": "9383936", "url": "https://www.cruisemapper.com/ships/Oasis-Of-The-Seas-609"},
    {"name": "Allure of the Seas", "imo": "9383948", "url": "https://www.cruisemapper.com/ships/Allure-Of-The-Seas-536"},
    {"name": "Harmony of the Seas", "imo": "9682875", "url": "https://www.cruisemapper.com/ships/Harmony-Of-The-Seas-1067"},
    {"name": "Spectrum of the Seas", "imo": "9778088", "url": "https://www.cruisemapper.com/ships/Spectrum-Of-The-Seas-1718"},
    {"name": "Odyssey of the Seas", "imo": "9795737", "url": "https://www.cruisemapper.com/ships/Odyssey-Of-The-Seas-1717"},
    {"name": "Ovation of the Seas", "imo": "9697753", "url": "https://www.cruisemapper.com/ships/Ovation-Of-The-Seas-1017"},
    {"name": "Anthem of the Seas", "imo": "9656101", "url": "https://www.cruisemapper.com/ships/Anthem-Of-The-Seas-1016"},
    {"name": "Quantum of the Seas", "imo": "9549463", "url": "https://www.cruisemapper.com/ships/Quantum-Of-The-Seas-951"},
    {"name": "Freedom of the Seas", "imo": "9304033", "url": "https://www.cruisemapper.com/ships/Freedom-Of-The-Seas-538"},
    {"name": "Liberty of the Seas", "imo": "9333151", "url": "https://www.cruisemapper.com/ships/Liberty-Of-The-Seas-539"},
    {"name": "Independence of the Seas", "imo": "9349687", "url": "https://www.cruisemapper.com/ships/Independence-Of-The-Seas-537"},
    {"name": "Voyager of the Seas", "imo": "9161716", "url": "https://www.cruisemapper.com/ships/Voyager-Of-The-Seas-544"},
    {"name": "Explorer of the Seas", "imo": "9161728", "url": "https://www.cruisemapper.com/ships/Explorer-Of-The-Seas-540"},
    {"name": "Adventure of the Seas", "imo": "9116871", "url": "https://www.cruisemapper.com/ships/Adventure-Of-The-Seas-535"},
    {"name": "Navigator of the Seas", "imo": "9227508", "url": "https://www.cruisemapper.com/ships/Navigator-Of-The-Seas-542"},
    {"name": "Mariner of the Seas", "imo": "9227510", "url": "https://www.cruisemapper.com/ships/Mariner-Of-The-Seas-541"},
    {"name": "Radiance of the Seas", "imo": "9195195", "url": "https://www.cruisemapper.com/ships/Radiance-Of-The-Seas-543"},
    {"name": "Brilliance of the Seas", "imo": "9195200", "url": "https://www.cruisemapper.com/ships/Brilliance-Of-The-Seas-571"},
    {"name": "Serenade of the Seas", "imo": "9228344", "url": "https://www.cruisemapper.com/ships/Serenade-Of-The-Seas-573"},
    {"name": "Jewel of the Seas", "imo": "9228356", "url": "https://www.cruisemapper.com/ships/Jewel-Of-The-Seas-572"},
    {"name": "Grandeur of the Seas", "imo": "9102978", "url": "https://www.cruisemapper.com/ships/Grandeur-Of-The-Seas-575"},
    {"name": "Enchantment of the Seas", "imo": "9111802", "url": "https://www.cruisemapper.com/ships/Enchantment-Of-The-Seas-574"},
    {"name": "Rhapsody of the Seas", "imo": "9116869", "url": "https://www.cruisemapper.com/ships/Rhapsody-Of-The-Seas-577"},
    {"name": "Vision of the Seas", "imo": "9116871", "url": "https://www.cruisemapper.com/ships/Vision-Of-The-Seas-578"}
]

# Standard realistic browser headers to bypass simple bot blocks
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

fleet_data = []

session = requests.Session()

for idx, ship in enumerate(SHIPS):
    lat, lon = None, None
    try:
        res = session.get(ship["url"], headers=headers, timeout=12)
        html = res.text

        # 1. Look for embedded JSON-LD or JS objects containing coordinates
        coord_matches = re.findall(r'["\']?lat["\']?\s*[:=]\s*([+-]?\d+\.\d+).*?["\']?lon["\']?\s*[:=]\s*([+-]?\d+\.\d+)', html, re.DOTALL | re.IGNORECASE)
        
        if coord_matches:
            lat = float(coord_matches[0][0])
            lon = float(coord_matches[0][1])
        else:
            # 2. Look for metadata tags containing coordinates
            lat_meta = re.search(r'property="og:latitude"\s+content="([+-]?\d+\.\d+)"', html)
            lon_meta = re.search(r'property="og:longitude"\s+content="([+-]?\d+\.\d+)"', html)
            if lat_meta and lon_meta:
                lat = float(lat_meta.group(1))
                lon = float(lon_meta.group(1))

        # Check if coordinates are valid non-zero values
        if lat is not None and lon is not None and (lat != 0.0 or lon != 0.0):
            fleet_data.append({
                "name": ship["name"],
                "lat": lat,
                "lon": lon,
                "status": "Live"
            })
            print(f"[✓] {ship['name']}: Lat {lat}, Lon {lon}")
        else:
            print(f"[!] {ship['name']}: Coordinates missing or blocked.")

    except Exception as err:
        print(f"[X] Error fetching {ship['name']}: {err}")

    # Small delay between requests to avoid trigger limits
    time.sleep(1.5)

# Save updated dataset
with open("ships.json", "w") as f:
    json.dump(fleet_data, f, indent=2)

print(f"\nSuccessfully wrote {len(fleet_data)} active positions to ships.json!")
