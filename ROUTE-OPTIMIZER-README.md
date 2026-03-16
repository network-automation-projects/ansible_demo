# Route Optimizer

Finds the fastest driving order for a round trip (start → all stops → start) and opens the route in Google Maps.

## Web app (for your boss)

1. Create a venv (optional but recommended): `python3 -m venv .venv && source .venv/bin/activate`
2. Install: `pip install -r route-optimizer-requirements.txt`
3. Run: `python app.py`
4. Open in browser: **http://127.0.0.1:5000**
5. Enter **Start & end** (e.g. Sebring, FL) and **Stops** (one per line), then click **Optimize route**.
6. Use **Open in Google Maps** or **Copy link** to share or navigate.

To let others on your network use it, they open `http://<your-computer-ip>:5000` while the app is running.

## CLI

```bash
python route_optimizer.py
```

Uses the built-in Sebring + 5 stops and prints the optimal order and map link.

## Files

- `app.py` – Flask server and embedded frontend
- `route_logic.py` – Geocoding, OSRM, TSP, map URL
- `route_optimizer.py` – CLI entry point
- `route-optimizer-requirements.txt` – Flask dependency
