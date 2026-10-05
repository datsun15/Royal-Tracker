import json
import re
import time
import requests

# Royal Caribbean Fleet with MMSI numbers
SHIPS = [
    {"name": "Icon of the Seas", "mmsi": "311001128"},
    {"name": "Symphony of the Seas", "mmsi": "311000646"},
    {"name": "Wonder of the Seas", "mmsi": "311001033"},
    {"name": "Utopia of the Seas", "mmsi": "311001174"},
    {"name": "Oasis of the Seas", "mmsi": "311020600"},
    {"name": "Allure of the Seas", "mmsi": "311036300"},
    {"name": "Harmony of the Seas", "mmsi": "311000399"},
    {"name": "Spectrum of the Seas", "mmsi": "311000758"},
    {"name": "Odyssey of the Seas", "mmsi": "311000912"},
    {"name": "Ovation of the Seas", "mmsi": "311000397"},
    {"name": "Anthem of the Seas", "mmsi": "311000274"},
    {"name": "Quantum of the Seas", "mmsi": "311000267"},
    {"name": "Freedom of the Seas", "mmsi": "311000122"},
    {"name": "Liberty of the Seas", "mmsi": "311000223"},
    {"name": "Independence of the Seas", "mmsi": "311000244"},
    {"name": "Voyager of the Seas", "mmsi": "311312000"},
    {"name": "Explorer of the Seas", "mmsi": "311313000"},
    {"name": "Adventure of the Seas", "mmsi": "311315000"},
    {"name": "Navigator of the Seas", "mmsi": "311492000"},
    {"name": "Mariner of the Seas", "mmsi": "311493000"},
    {"name": "Radiance of the Seas", "mmsi": "311019000"},
    {"name": "Brilliance of the Seas", "mmsi": "311361000"},
    {"name": "Serenade of the Seas", "mmsi": "311494000"},
    {"name": "Jewel of the Seas", "mmsi": "311582000"},
    {"name": "Grandeur of the Seas", "mmsi": "311781000"},
    {"name": "Enchantment of the Seas", "mmsi": "311782000"},
    {"name": "Rhapsody of the Seas", "mmsi": "311783000"},
    {"name": "Vision of the Seas", "mmsi": "311784000"}
]

fleet_data = []

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

print("Fetching live AIS positions...")

for ship in SHIPS:
    try:
        # OpenSeaMap / Public AIS Data API
        url = f"https://map.openseamap.org/api/get_vessel_pos.php?mmsi={ship['mmsi']}"
        res = requests.get(url, headers=headers, timeout=10)

        if res.status_code == 200 and res.text.strip():
            # Parse response
            try:
                data = res.json()
                lat = float(data.get("lat", 0))
                lon = float(data.get("lon", 0))
            except Exception:
                # Regular expression parsing fallback if format is JSONP/text
                lat_match = re.search(r'["\']?lat["\']?\s*[:=]\s*([+-]?\d+\.\d+)', res.text, re.IGNORECASE)
                lon_match = re.search(r'["\']?lon["\']?\s*[:=]\s*([+-]?\d+\.\d+)', res.text, re.IGNORECASE)
                lat = float(lat_match.group(1)) if lat_match else 0
                lon = float(lon_match.group(1)) if lon_match else 0

            if lat != 0 and lon != 0:
                fleet_data.append({
                    "name": ship["name"],
                    "mmsi": ship["mmsi"],
                    "lat": lat,
                    "lon": lon
                })
                print(f"[✓] Found {ship['name']}: Lat {lat}, Lon {lon}")
            else:
                print(f"[!] {ship['name']}: No current position broadcast.")
        else:
            print(f"[!] {ship['name']}: Endpoint returned status {res.status_code}")

    except Exception as e:
        print(f"[X] {ship['name']} failed: {e}")

    time.sleep(1)

# Write valid positions
with open("ships.json", "w") as f:
    json.dump(fleet_data, f, indent=2)

print(f"\nCompleted! Written {len(fleet_data)} ships to ships.json")
