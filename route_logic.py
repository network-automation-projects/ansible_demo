"""
Shared route optimization logic: geocode, OSRM duration matrix, TSP, map URL.
"""

import itertools
import json
import time
import urllib.parse
import urllib.request

# Known coordinates (optional cache to avoid geocoding)
DEFAULT_COORDS: dict[str, tuple[float, float]] = {
    "Sebring, FL": (27.4959, -81.4409),
    "2308 Oakdale St S, St. Petersburg, FL 33705": (27.7406, -82.6528),
    "4718 Belfast Dr, New Port Richey, FL 34652": (28.2442, -82.7193),
    "1502 Valrico Lake Rd, Valrico, FL 33594": (27.9378, -82.2403),
    "2420 Chestnut Woods Dr, Lakeland, FL 33815": (28.0394, -81.9498),
    "3006 E Dr MLK Jr Blvd, Tampa, FL 33610": (27.9817, -82.4165),
}


def geocode_address(address: str) -> tuple[float, float] | None:
    """Return (lat, lon) for address using Nominatim. Rate-limited."""
    url = (
        "https://nominatim.openstreetmap.org/search?"
        + urllib.parse.urlencode({"q": address, "format": "json", "limit": 1})
    )
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "RouteOptimizer/1.0 (contact@example.com)"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode())
        if data and len(data) > 0:
            lat = float(data[0]["lat"])
            lon = float(data[0]["lon"])
            return (lat, lon)
    except Exception:
        pass
    return None


def get_coords(
    labels: list[str], coords_cache: dict[str, tuple[float, float]] | None = None
) -> tuple[list[tuple[float, float]], str | None]:
    """
    Return (coords_list, error). Uses coords_cache first; geocodes missing (1s delay each).
    """
    cache = dict(coords_cache or DEFAULT_COORDS)
    out: list[tuple[float, float]] = []
    for addr in labels:
        if addr.strip() == "":
            return ([], "One or more addresses are empty.")
        if addr in cache:
            out.append(cache[addr])
            continue
        time.sleep(1)  # Nominatim rate limit
        c = geocode_address(addr)
        if c is None:
            return ([], f"Could not find location: {addr[:50]}...")
        cache[addr] = c
        out.append(c)
    return (out, None)


def get_duration_matrix(coords_list: list[tuple[float, float]]) -> list[list[float]]:
    """Driving duration matrix in seconds from OSRM."""
    points = ";".join(f"{lon},{lat}" for lat, lon in coords_list)
    url = (
        "https://router.project-osrm.org/table/v1/driving/"
        f"{points}?annotations=duration"
    )
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode())
    if data.get("code") != "Ok":
        raise RuntimeError(data.get("message", "OSRM error"))
    durations = data["durations"]
    return [
        [(x if x is not None else 0.0) for x in row]
        for row in durations
    ]


def optimize_order(
    labels: list[str], coords_list: list[tuple[float, float]]
) -> tuple[tuple[int, ...], float, list[list[float]]]:
    """labels[0] = origin = destination; labels[1:] = stops. Returns (best_perm, total_sec, matrix)."""
    n = len(labels)
    matrix = get_duration_matrix(coords_list)

    def seg(i: int, j: int) -> float:
        return matrix[i][j]

    best_order: tuple[int, ...] = ()
    best_total = float("inf")
    for perm in itertools.permutations(range(1, n)):
        total = seg(0, perm[0])
        for k in range(len(perm) - 1):
            total += seg(perm[k], perm[k + 1])
        total += seg(perm[-1], 0)
        if total < best_total:
            best_total = total
            best_order = perm
    return (best_order, best_total, matrix)


def build_map_url(ordered_addresses: list[str]) -> str:
    """Google Maps path-style URL for the given order."""
    path_parts = [
        urllib.parse.quote(addr.replace(" ", "+"), safe="/,+")
        for addr in ordered_addresses
    ]
    return "https://www.google.com/maps/dir/" + "/".join(path_parts)


def fmt_duration(seconds: float) -> str:
    m = int(seconds) // 60
    h = m // 60
    m = m % 60
    if h:
        return f"{h}h {m}m"
    return f"{m} min"


def optimize_route(
    origin: str,
    stops: list[str],
    coords_cache: dict[str, tuple[float, float]] | None = None,
) -> dict:
    """
    Run full optimization. Returns dict:
      ok: bool
      error: str | None
      total_duration: str
      legs: list[{address, leg_minutes}]
      map_url: str
      order: list[str] (addresses in optimal order)
    """
    labels = [origin] + [s.strip() for s in stops if s.strip()]
    if len(labels) < 2:
        return {
            "ok": False,
            "error": "Add at least one stop.",
            "total_duration": "",
            "legs": [],
            "map_url": "",
            "order": [],
        }
    coords_list, err = get_coords(labels, coords_cache)
    if err:
        return {
            "ok": False,
            "error": err,
            "total_duration": "",
            "legs": [],
            "map_url": "",
            "order": [],
        }
    try:
        best_order, total_sec, matrix = optimize_order(labels, coords_list)
    except Exception as e:
        return {
            "ok": False,
            "error": str(e),
            "total_duration": "",
            "legs": [],
            "map_url": "",
            "order": [],
        }
    # Build legs
    legs = []
    for idx, i in enumerate(best_order):
        from_idx = 0 if idx == 0 else best_order[idx - 1]
        leg_sec = matrix[from_idx][i]
        legs.append({"address": labels[i], "leg_minutes": round(leg_sec / 60, 1)})
    leg_home_sec = matrix[best_order[-1]][0]
    legs.append({"address": labels[0], "leg_minutes": round(leg_home_sec / 60, 1)})
    order = [labels[i] for i in best_order]
    ordered_addresses = [labels[0]] + order + [labels[0]]
    map_url = build_map_url(ordered_addresses)
    return {
        "ok": True,
        "error": None,
        "total_duration": fmt_duration(total_sec),
        "legs": legs,
        "map_url": map_url,
        "order": order,
    }
