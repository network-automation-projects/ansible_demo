#!/usr/bin/env python3
"""
Simple script to stop the currently running Toggl timer.
"""

import os
import base64
import asyncio
from datetime import datetime, timezone
import aiohttp

TOGGL_API_BASE = "https://api.track.toggl.com/api/v9"


def get_auth_headers() -> dict[str, str]:
    """Get authentication headers for Toggl API."""
    api_token = os.getenv("TOGGL_API_TOKEN")
    
    if not api_token:
        raise ValueError(
            "TOGGL_API_TOKEN not found. Please set it as an environment variable."
        )
    
    credentials = f"{api_token}:api_token"
    encoded = base64.b64encode(credentials.encode()).decode()
    
    return {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/json"
    }


async def get_current_time_entry():
    """Get the currently running time entry."""
    headers = get_auth_headers()
    url = f"{TOGGL_API_BASE}/me/time_entries/current"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 404:
                return None
            response.raise_for_status()
            return await response.json()


async def stop_time_entry(workspace_id: int, time_entry_id: int):
    """Stop a running time entry."""
    headers = get_auth_headers()
    url = f"{TOGGL_API_BASE}/workspaces/{workspace_id}/time_entries/{time_entry_id}"
    
    payload = {
        "stop": datetime.now(timezone.utc).isoformat()
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.patch(url, headers=headers, json=payload) as response:
            response.raise_for_status()
            return await response.json()


async def main():
    """Main function to stop the timer."""
    try:
        # Get current running timer
        print("Checking for running timer...")
        current_entry = await get_current_time_entry()
        
        if not current_entry:
            print("ℹ️  No timer is currently running.")
            return
        
        workspace_id = current_entry.get("workspace_id")
        time_entry_id = current_entry.get("id")
        
        if not workspace_id or not time_entry_id:
            print("❌ Error: Could not determine workspace_id or time_entry_id from current timer")
            return
        
        # Stop the timer
        print(f"Stopping timer (Entry ID: {time_entry_id})...")
        result = await stop_time_entry(workspace_id, time_entry_id)
        
        desc = result.get("description", "No description")
        entry_id = result.get("id", "Unknown")
        start_time = result.get("start", "Unknown")
        stop_time = result.get("stop", "Unknown")
        duration = result.get("duration", 0)
        
        # Convert duration from seconds to hours:minutes:seconds
        if duration > 0:
            hours = duration // 3600
            minutes = (duration % 3600) // 60
            seconds = duration % 60
            duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            duration_str = "0:00:00"
        
        print("\n✅ Timer stopped!\n")
        print(f"Entry ID: {entry_id}")
        print(f"Description: {desc}")
        print(f"Start time: {start_time}")
        print(f"Stop time: {stop_time}")
        print(f"Duration: {duration_str}")
        
    except ValueError as e:
        print(f"❌ Configuration Error: {str(e)}")
    except aiohttp.ClientResponseError as e:
        if e.status == 401:
            print("❌ Authentication Error: Invalid API token. Please check your TOGGL_API_TOKEN.")
        elif e.status == 403:
            print("❌ Authorization Error: You don't have permission to access this resource.")
        elif e.status == 404:
            print("❌ Not Found: The requested resource was not found.")
        else:
            print(f"❌ API Error ({e.status}): {e.message}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())







