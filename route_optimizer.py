#!/usr/bin/env python3
"""
CLI: Optimize drive-time route (origin → stops → origin). Uses route_logic.
"""

from route_logic import DEFAULT_COORDS, optimize_route

SEBRING = "Sebring, FL"
STOPS = [
    "2308 Oakdale St S, St. Petersburg, FL 33705",
    "4718 Belfast Dr, New Port Richey, FL 34652",
    "1502 Valrico Lake Rd, Valrico, FL 33594",
    "2420 Chestnut Woods Dr, Lakeland, FL 33815",
    "3006 E Dr MLK Jr Blvd, Tampa, FL 33610",
]


def main() -> None:
    result = optimize_route(SEBRING, STOPS, coords_cache=DEFAULT_COORDS)
    if not result["ok"]:
        print("Error:", result["error"])
        return
    print("Optimal route (by drive time):")
    print("  Start:", SEBRING)
    for leg in result["legs"]:
        print(f"  → {leg['address']}  ({leg['leg_minutes']} min)")
    print()
    print("Total estimated drive time:", result["total_duration"])
    print()
    print("Map (Google Maps directions):")
    print("  " + result["map_url"])


if __name__ == "__main__":
    main()
