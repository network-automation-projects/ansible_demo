"""
Pixela Habit Tracker Practice Scaffold

Goal (for the challenge):
- Comment out graph creation code (once the graph exists)
- POST a pixel for a specific date
- Refresh Pixela and see the new pixel

Docs:
- https://docs.pixe.la/
"""

import os
import requests
from datetime import datetime

# ----------------------------
# 1) Configuration
# ----------------------------
PIXELA_BASE_URL = "https://pixe.la/v1/users"

# Prefer environment variables so you don't hardcode secrets.
# In your terminal (macOS/Linux), run:
#   export PIXELA_USERNAME="rclarke009"
#   export PIXELA_TOKEN="123987"
#
# Or temporarily set them inside your IDE's run configuration.
USERNAME = os.getenv("PIXELA_USERNAME", "rclarke009")
TOKEN = os.getenv("PIXELA_TOKEN", "my_token")

# Your graph settings (edit these)
GRAPH_ID = "coding1"              # must be lowercase letters/numbers only
GRAPH_NAME = "Coding Practice"
UNIT = "min"                      # e.g. "min", "pages", "km"
TYPE = "int"                      # "int" or "float"
COLOR = "ajisai"                  # e.g. shibafu, momiji, sora, ichou, ajisai, kuro

HEADERS = {
    "X-USER-TOKEN": TOKEN
}

# ----------------------------
# 2) Helper functions
# ----------------------------
def create_user():
    """Create a Pixela user (run once)."""
    endpoint = PIXELA_BASE_URL
    payload = {
        "token": TOKEN,
        "username": USERNAME,
        "agreeTermsOfService": "yes",
        "notMinor": "yes",
    }
    r = requests.post(url=endpoint, json=payload)
    print("create_user:", r.status_code, r.text)


def create_graph():
    """Create a graph (run once per graph)."""
    endpoint = f"{PIXELA_BASE_URL}/{USERNAME}/graphs"
    payload = {
        "id": GRAPH_ID,
        "name": GRAPH_NAME,
        "unit": UNIT,
        "type": TYPE,
        "color": COLOR,
    }
    r = requests.post(url=endpoint, json=payload, headers=HEADERS)
    print("create_graph:", r.status_code, r.text)


def post_pixel(date_yyyymmdd: str, quantity: str):
    endpoint = f'{PIXELA_BASE_URL}/{USERNAME}/graphs/{GRAPH_ID}'
    pixeldata = {
        "date": date_yyyymmdd,
        "quantity": quantity 
    }
    response = requests.post(url=endpoint, json=pixeldata, headers=HEADERS)
    print(response.text)

def update_pixel(date_yyyymmdd: str, quantity: str):
    endpoint = f'{PIXELA_BASE_URL}/{USERNAME}/graphs/{GRAPH_ID}/{date_yyyymmdd}'
    pixeldata = {
        "date": date_yyyymmdd,
        "quantity": quantity 
    }
    response = requests.put(url=endpoint, json=pixeldata, headers=HEADERS)
    print(response.text)

def delete_pixel(date_yyyymmdd: str):
    endpoint = f'{PIXELA_BASE_URL}/{USERNAME}/graphs/{GRAPH_ID}/{date_yyyymmdd}'
    pixeldata = {
        "date": date_yyyymmdd,
    }
    response = requests.delete(url=endpoint, json=pixeldata, headers=HEADERS)
    print(response.text)


def graph_url() -> str:
    """Convenience: open this in your browser to see your graph."""
    return f"https://pixe.la/v1/users/{USERNAME}/graphs/{GRAPH_ID}.html"


# ----------------------------
# 3) Practice driver
# ----------------------------
def main():
    # Quick sanity checks:
    if USERNAME.startswith("YOUR_") or TOKEN.startswith("YOUR_"):
        print("Set PIXELA_USERNAME and PIXELA_TOKEN (or replace placeholders in code).")
        return

    print("Your graph URL:")
    print(graph_url())
    print()

    # ---- Run these ONCE, then comment them out ----
    #create_user()
    #create_graph()

    # ---- Challenge focus: POST a pixel for a specific date ----
    # Option A: hardcode a date (recommended for the challenge)
    # date_str = "20260106"      # YYYYMMDD
    # qty = "30"                 # must be a string; int graph expects whole numbers
    # post_pixel(date_str, qty)

    # Option B: post for "today" using datetime (useful later)
    #post_pixel(datetime.now().strftime("%Y%m%d"), "30")

    #post_pixel("20260105", "20")

    # post_pixel("20260104", "10")
    # post_pixel("20260103", "5")
    # post_pixel("20260102", "2")
    delete_pixel("20260101")    


    #put method to change an existing pixel
     


    # Extra practice:
    # update_pixel(date_str, "45")
    # delete_pixel(date_str)


if __name__ == "__main__":
    main()
