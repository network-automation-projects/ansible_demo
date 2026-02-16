"""
Python Network Automation - API Integration Exercises
"""

from typing import Dict, Any, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In production: import requests


def get_device_from_api(api_url: str, device_id: int, token: str) -> Dict[str, Any]:
    """Get device from API using GET request."""
    # TODO: Use requests.get() with headers for authentication
    headers = None  # Create headers dict with 'Authorization' key
    # response = requests.get(f"{api_url}/devices/{device_id}", headers=headers)
    # return response.json()
    pass


def create_device_via_api(api_url: str, device_data: Dict[str, Any], token: str) -> Dict[str, Any]:
    """Create device via API using POST request."""
    # TODO: Use requests.post() with JSON payload
    headers = None  # Include Authorization and Content-Type headers
    # response = requests.post(f"{api_url}/devices", json=device_data, headers=headers)
    # return response.json()
    pass


def update_device_via_api(api_url: str, device_id: int, updates: Dict[str, Any], token: str) -> Dict[str, Any]:
    """Update device via API using PUT request."""
    # TODO: Use requests.put() with JSON payload
    pass


def delete_device_via_api(api_url: str, device_id: int, token: str) -> bool:
    """Delete device via API using DELETE request."""
    # TODO: Use requests.delete() and check response.status_code
    pass


def create_api_session(base_url: str, token: str):
    """Create persistent API session."""
    # TODO: Use requests.Session() and set default headers
    # session = requests.Session()
    # session.headers.update({'Authorization': f'Token {token}'})
    # return session
    pass


if __name__ == "__main__":
    print("API Integration Exercises")
    print("Uncomment test cases to verify solutions")
