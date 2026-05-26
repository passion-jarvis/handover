"""
Google Maps No-Website Business Scraper
Usage:
  Single city:  python3 scraper.py --type "hair salon" --city "Los Angeles" --limit 100
  State-wide:   python3 scraper.py --type "hair salon" --state california --limit 5000
"""

import googlemaps
import csv
import argparse
import time
import os
import json
from datetime import datetime

API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY", "AIzaSyC2PVJtZrZMe3z80CB55HaDgEjT4alMHNs")

CITY_COORDS = {
    "los angeles": (34.0522, -118.2437),
    "new york": (40.7128, -74.0060),
    "chicago": (41.8781, -87.6298),
    "houston": (29.7604, -95.3698),
    "miami": (25.7617, -80.1918),
    "san francisco": (37.7749, -122.4194),
    "dallas": (32.7767, -96.7970),
    "atlanta": (33.7490, -84.3880),
    "phoenix": (33.4484, -112.0740),
    "seattle": (47.6062, -122.3321),
}

# California grid: covers all major metros + surrounding areas
# Format: (lat, lng, label)
CALIFORNIA_GRID = [
    # Greater Los Angeles
    (34.0522, -118.2437, "Los Angeles"),
    (34.0522, -118.4437, "West LA"),
    (34.0522, -118.0437, "East LA"),
    (34.1522, -118.2437, "North LA"),
    (33.9522, -118.2437, "South LA"),
    (34.0195, -118.4912, "Santa Monica"),
    (34.0736, -118.4004, "Beverly Hills"),
    (34.1478, -118.1445, "Pasadena"),
    (34.0633, -117.9497, "West Covina"),
    (34.1083, -117.7898, "San Bernardino"),
    (33.9806, -117.3755, "Riverside"),
    (34.0633, -117.5853, "Ontario"),
    (33.8536, -118.1397, "Long Beach"),
    (33.8366, -118.3400, "Torrance"),
    (33.7701, -118.1937, "Carson"),
    (33.9425, -118.4081, "Inglewood"),
    (34.1425, -118.2551, "Glendale"),
    (34.1808, -118.3090, "Burbank"),
    (34.2090, -118.4912, "Woodland Hills"),
    (34.2277, -118.2437, "San Fernando"),
    (34.1975, -119.1771, "Ventura"),
    (34.4208, -119.6982, "Santa Barbara"),
    # Orange County
    (33.7455, -117.8677, "Anaheim"),
    (33.6839, -117.7947, "Santa Ana"),
    (33.7701, -117.8823, "Orange"),
    (33.6403, -117.9187, "Irvine"),
    (33.5931, -117.7090, "Mission Viejo"),
    (33.7243, -117.6011, "Riverside OC"),
    # San Diego
    (32.7157, -117.1611, "San Diego"),
    (32.7157, -117.0011, "East San Diego"),
    (32.8157, -117.1611, "North San Diego"),
    (32.6157, -117.1611, "South San Diego"),
    (33.1192, -117.0864, "Escondido"),
    (33.1581, -117.3506, "Oceanside"),
    (32.9595, -117.2653, "Del Mar"),
    # SF Bay Area
    (37.7749, -122.4194, "San Francisco"),
    (37.7749, -122.2194, "Oakland"),
    (37.3382, -121.8863, "San Jose"),
    (37.5485, -121.9886, "Fremont"),
    (37.6879, -122.4702, "Daly City"),
    (37.8044, -122.2712, "Berkeley"),
    (37.9716, -122.5827, "San Rafael"),
    (37.4419, -122.1430, "Palo Alto"),
    (37.5630, -122.0530, "Hayward"),
    (37.9577, -121.2908, "Stockton"),
    (37.8044, -121.9780, "Pleasanton"),
    (37.6879, -121.7053, "Tracy"),
    (38.2975, -122.2869, "Napa"),
    (38.2919, -122.4580, "Santa Rosa"),
    (37.6547, -122.4077, "San Mateo"),
    (37.4971, -122.2547, "Redwood City"),
    (37.3229, -122.0322, "Sunnyvale"),
    (37.4041, -121.9679, "Santa Clara"),
    (37.1305, -121.6369, "Gilroy"),
    # Sacramento
    (38.5816, -121.4944, "Sacramento"),
    (38.5816, -121.2944, "East Sacramento"),
    (38.6816, -121.4944, "North Sacramento"),
    (38.4816, -121.4944, "South Sacramento"),
    (38.6785, -121.7733, "Davis"),
    (38.7521, -121.2880, "Roseville"),
    (38.9135, -121.0560, "Auburn"),
    (38.4405, -121.3689, "Elk Grove"),
    # Central Valley
    (36.7378, -119.7871, "Fresno"),
    (36.7378, -119.5871, "East Fresno"),
    (36.8378, -119.7871, "North Fresno"),
    (35.3733, -119.0187, "Bakersfield"),
    (35.3733, -118.8187, "East Bakersfield"),
    (37.6391, -120.9969, "Modesto"),
    (37.9716, -121.2908, "Stockton North"),
    (36.3302, -119.2921, "Visalia"),
    (36.5853, -119.6549, "Hanford"),
    (37.3022, -120.4829, "Merced"),
    (36.1405, -120.3522, "Coalinga"),
    # Inland Empire
    (34.0555, -117.1825, "Fontana"),
    (34.1083, -117.2898, "Rancho Cucamonga"),
    (34.0633, -117.3853, "Rialto"),
    (33.8536, -117.5522, "Perris"),
    (33.7296, -116.3742, "Palm Springs"),
    (33.8902, -116.5453, "Palm Desert"),
    # Other cities
    (35.6869, -120.6669, "San Luis Obispo"),
    (34.9592, -120.4349, "Santa Maria"),
    (36.6002, -121.8947, "Monterey"),
    (36.9741, -122.0308, "Santa Cruz"),
    (38.1041, -122.2566, "Vallejo"),
    (38.2494, -122.0400, "Fairfield"),
    (39.1454, -121.5936, "Yuba City"),
    (40.5865, -122.3917, "Redding"),
    (40.7654, -124.1873, "Eureka"),
    (39.7285, -121.8374, "Chico"),
]


CHECKPOINT_DIR = "/Users/passionchu/claude/projects/website-hustle"


def load_checkpoint(filename):
    """Load seen place_ids from checkpoint to allow resume."""
    if os.path.exists(filename):
        with open(filename) as f:
            return set(json.load(f))
    return set()


def save_checkpoint(seen_ids, filename):
    with open(filename, "w") as f:
        json.dump(list(seen_ids), f)


def scrape_point(gmaps, lat, lng, business_type, radius, seen_ids):
    """Scrape one lat/lng point. Returns list of no-website businesses."""
    found = []
    next_page_token = None
    pages = 0

    while pages < 3:
        try:
            if next_page_token:
                time.sleep(2)
                response = gmaps.places_nearby(
                    location=(lat, lng),
                    radius=radius,
                    page_token=next_page_token
                )
            else:
                response = gmaps.places_nearby(
                    location=(lat, lng),
                    radius=radius,
                    keyword=business_type
                )
        except Exception as e:
            print(f"  [API error] {e}")
            break

        for place in response.get("results", []):
            place_id = place["place_id"]
            if place_id in seen_ids:
                continue
            seen_ids.add(place_id)

            try:
                details = gmaps.place(
                    place_id,
                    fields=["name", "formatted_phone_number", "formatted_address", "website", "rating", "user_ratings_total", "url"]
                )["result"]
            except Exception as e:
                print(f"  [Details error] {e}")
                continue

            if not details.get("website"):
                found.append({
                    "Business Name": details.get("name", ""),
                    "Phone": details.get("formatted_phone_number", ""),
                    "Address": details.get("formatted_address", ""),
                    "Rating": details.get("rating", ""),
                    "Reviews": details.get("user_ratings_total", ""),
                    "Google Maps URL": details.get("url", ""),
                    "Website": "NONE",
                })

        next_page_token = response.get("next_page_token")
        pages += 1
        if not next_page_token:
            break

    return found


def scrape_state(business_type, state, limit=5000, radius=8000):
    if state.lower() != "california":
        print("Only 'california' is supported for state-wide scraping right now.")
        return

    gmaps = googlemaps.Client(key=API_KEY)
    grid = CALIFORNIA_GRID

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_file = f"{CHECKPOINT_DIR}/leads_{business_type.replace(' ', '_')}_california_{timestamp}.csv"
    checkpoint_file = f"{CHECKPOINT_DIR}/checkpoint_california.json"

    seen_ids = load_checkpoint(checkpoint_file)
    results = []
    total_checked = len(seen_ids)

    print(f"\nCalifornia state-wide scrape: '{business_type}'")
    print(f"Target: {limit} no-website leads")
    print(f"Grid points: {len(grid)}")
    print(f"Est. API cost: $150-250 depending on hit rate")
    print(f"Resuming from {total_checked} previously seen businesses\n")

    # Write CSV header
    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Business Name", "Phone", "Address", "Rating", "Reviews", "Google Maps URL", "Website"])
        writer.writeheader()

    for i, (lat, lng, label) in enumerate(grid):
        if len(results) >= limit:
            break

        print(f"[{i+1}/{len(grid)}] {label} — {len(results)} leads so far")
        found = scrape_point(gmaps, lat, lng, business_type, radius, seen_ids)

        if found:
            results.extend(found)
            # Append to CSV immediately (don't lose progress)
            with open(output_file, "a", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["Business Name", "Phone", "Address", "Rating", "Reviews", "Google Maps URL", "Website"])
                for r in found:
                    writer.writerow(r)
                    print(f"  + {r['Business Name']} — {r['Phone']}")

        # Save checkpoint every 5 grid points
        if i % 5 == 0:
            save_checkpoint(seen_ids, checkpoint_file)

        time.sleep(0.5)

    save_checkpoint(seen_ids, checkpoint_file)
    print(f"\nDone. {len(results)} leads saved to:\n{output_file}")
    return output_file


def scrape_city(business_type, city, limit=100, radius=15000):
    gmaps = googlemaps.Client(key=API_KEY)
    city_key = city.lower()

    if city_key not in CITY_COORDS:
        print(f"City '{city}' not in presets.")
        return []

    lat, lng = CITY_COORDS[city_key]
    print(f"\nSearching for '{business_type}' in {city} with no website...\n")

    results = []
    seen_ids = set()
    next_page_token = None

    while len(results) < limit:
        if next_page_token:
            time.sleep(2)
            response = gmaps.places_nearby(
                location=(lat, lng),
                radius=radius,
                page_token=next_page_token
            )
        else:
            response = gmaps.places_nearby(
                location=(lat, lng),
                radius=radius,
                keyword=business_type
            )

        for place in response.get("results", []):
            if len(results) >= limit:
                break

            place_id = place["place_id"]
            if place_id in seen_ids:
                continue
            seen_ids.add(place_id)

            details = gmaps.place(
                place_id,
                fields=["name", "formatted_phone_number", "formatted_address", "website", "rating", "user_ratings_total", "url"]
            )["result"]

            if not details.get("website"):
                results.append({
                    "Business Name": details.get("name", ""),
                    "Phone": details.get("formatted_phone_number", ""),
                    "Address": details.get("formatted_address", ""),
                    "Rating": details.get("rating", ""),
                    "Reviews": details.get("user_ratings_total", ""),
                    "Google Maps URL": details.get("url", ""),
                    "Website": "NONE",
                })
                print(f"  [{len(results)}] {details.get('name')} — {details.get('formatted_phone_number', 'no phone')}")

        next_page_token = response.get("next_page_token")
        if not next_page_token:
            break

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"{CHECKPOINT_DIR}/leads_{business_type.replace(' ', '_')}_{city.replace(' ', '_')}_{timestamp}.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"\nDone. {len(results)} leads saved to:\n{filename}")
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", default="hair salon", help="Business type")
    parser.add_argument("--city", default="", help="Single city (e.g. 'Los Angeles')")
    parser.add_argument("--state", default="", help="State-wide scrape (e.g. 'california')")
    parser.add_argument("--limit", type=int, default=5000, help="Max no-website results")
    parser.add_argument("--radius", type=int, default=8000, help="Search radius in meters per grid point")
    args = parser.parse_args()

    if args.state:
        scrape_state(args.type, args.state, args.limit, args.radius)
    elif args.city:
        scrape_city(args.type, args.city, args.limit, args.radius)
    else:
        print("Provide --city or --state")
