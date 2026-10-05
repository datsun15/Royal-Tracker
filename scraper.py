import json
import time
import requests

# Royal Caribbean Fleet with MMSI numbers (Unique transponder ID for each ship)
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
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.vesselfinder.com/"
}

print("Fetching live AIS ship coordinates...")

for ship in SHIPS:
    try:
        # Query public AIS transponder endpoint by MMSI
        url = f"https://www.vesselfinder.com/api/pub/click/{ship['mmsi']}"
        res = requests.get(url, headers=headers, timeout=10)
        
        if res.status_code == 200:
            data = res.json()
            # Extract coordinates from response
            lat = data.get("lat") or data.get("latitude")
            lon = data.get("lon") or data.get("longitude")
            
            if lat and lon and (lat != 0 and lon != 0):
                fleet_data.append({
                    "name": ship["name"],
                    "mmsi": ship["mmsi"],
                    "lat": float(lat),
                    "lon": float(lon)
                })
                print(f"[✓] {ship['name']}: ({lat}, {lon})")
            else:
                print(f"[!] {ship['name']}: No valid coordinates returned.")
        else:
            print(f"[!] {ship['name']}: HTTP Status {res.status_code}")

    except Exception as err:
        print(f"[X] {ship['name']} failed: {err}")

    # Delay to remain within rate limits
    time.sleep(2)

# Write valid positions to ships.json
with open("ships.json", "w") as f:
    json.dump(fleet_data, f, indent=2)

print(f"\nSaved {len(fleet_data)} active ship positions to ships.json.")
