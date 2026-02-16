"""
Answer key for exercises.py in this folder.
Use this file to verify your solutions. Same structure as exercises.py with blanks filled in.
"""

from typing import Dict, Any, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import requests


def get_device_from_api(api_url: str, device_id: int, token: str) -> Dict[str, Any]:
    """Get device from API using GET request."""
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(f"{api_url}/devices/{device_id}", headers=headers)
    response.raise_for_status()
    return response.json()


def create_device_via_api(
    api_url: str, device_data: Dict[str, Any], token: str
) -> Dict[str, Any]:
    """Create device via API using POST request."""
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json",
    }
    response = requests.post(f"{api_url}/devices", json=device_data, headers=headers)
    response.raise_for_status()
    return response.json()


def update_device_via_api(
    api_url: str, device_id: int, updates: Dict[str, Any], token: str
) -> Dict[str, Any]:
    """Update device via API using PUT request."""
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json",
    }
    response = requests.put(
        f"{api_url}/devices/{device_id}", json=updates, headers=headers
    )
    response.raise_for_status()
    return response.json()


def delete_device_via_api(api_url: str, device_id: int, token: str) -> bool:
    """Delete device via API using DELETE request."""
    headers = {"Authorization": f"Token {token}"}
    response = requests.delete(f"{api_url}/devices/{device_id}", headers=headers)
    return response.status_code == 204 or response.status_code == 200


def create_api_session(base_url: str, token: str) -> requests.Session:
    """Create persistent API session."""
    session = requests.Session()
    session.headers.update({"Authorization": f"Token {token}"})
    return session


if __name__ == "__main__":
    print("05_api_integration – answer key (run exercises.py to practice)")
