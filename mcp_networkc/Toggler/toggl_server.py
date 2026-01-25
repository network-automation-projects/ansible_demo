#!/usr/bin/env python3
"""
Toggl MCP Server
An MCP server for Toggl time tracking operations including starting timers,
stopping timers, and viewing time entries.
"""

import os
import base64
import asyncio
from datetime import datetime, timezone
from typing import Any, Sequence, Optional
import aiohttp
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Initialize the MCP server
server = Server("toggl-tracker")

# Toggl API base URL
TOGGL_API_BASE = "https://api.track.toggl.com/api/v9"


def get_auth_headers() -> dict[str, str]:
    """
    Get authentication headers for Toggl API.
    Uses HTTP Basic Auth with API token.
    Reads from Docker secret file first, then falls back to environment variable.
    """
    api_token = None
    
    # Try to read from Docker secret first (for Docker Swarm)
    secret_path = "/run/secrets/toggl_api_token"
    if os.path.exists(secret_path):
        try:
            with open(secret_path, 'r') as f:
                api_token = f.read().strip()
        except Exception as e:
            # If we can't read the secret file, fall through to env var
            pass
    
    # Fall back to environment variable
    if not api_token:
        api_token = os.getenv("TOGGL_API_TOKEN")
    
    if not api_token:
        raise ValueError(
            "TOGGL_API_TOKEN not found. Please set it via Docker secret "
            "(/run/secrets/toggl_api_token) or environment variable TOGGL_API_TOKEN."
        )
    
    # Toggl API uses format: api_token:api_token for Basic Auth
    credentials = f"{api_token}:api_token"
    encoded = base64.b64encode(credentials.encode()).decode()
    
    return {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/json"
    }


async def get_current_time_entry() -> Optional[dict[str, Any]]:
    """
    Get the currently running time entry.
    Returns None if no timer is running.
    """
    headers = get_auth_headers()
    url = f"{TOGGL_API_BASE}/me/time_entries/current"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 404:
                return None  # No current timer
            response.raise_for_status()
            return await response.json()


async def start_time_entry(
    workspace_id: int,
    description: Optional[str] = None,
    project_id: Optional[int] = None,
    tag_ids: Optional[list[int]] = None,
    billable: Optional[bool] = None
) -> dict[str, Any]:
    """
    Start a new time entry.
    
    Args:
        workspace_id: Toggl workspace ID (required)
        description: Task description (optional)
        project_id: Project ID to associate with (optional)
        tag_ids: List of tag IDs (optional)
        billable: Whether entry is billable (optional)
    
    Returns:
        Created time entry object
    """
    headers = get_auth_headers()
    url = f"{TOGGL_API_BASE}/workspaces/{workspace_id}/time_entries"
    
    # Build payload
    payload: dict[str, Any] = {
        "duration": -1,  # -1 indicates a running timer
        "workspace_id": workspace_id,
        "start": datetime.now(timezone.utc).isoformat()
    }
    
    if description:
        payload["description"] = description
    if project_id:
        payload["project_id"] = project_id
    if tag_ids:
        payload["tag_ids"] = tag_ids
    if billable is not None:
        payload["billable"] = billable
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status == 429:
                retry_after = response.headers.get("Retry-After", "60")
                raise Exception(
                    f"Rate limit exceeded. Please wait {retry_after} seconds before retrying."
                )
            response.raise_for_status()
            return await response.json()


async def stop_time_entry(workspace_id: int, time_entry_id: int) -> dict[str, Any]:
    """
    Stop a running time entry.
    
    Args:
        workspace_id: Toggl workspace ID
        time_entry_id: Time entry ID to stop
    
    Returns:
        Updated time entry object
    """
    headers = get_auth_headers()
    url = f"{TOGGL_API_BASE}/workspaces/{workspace_id}/time_entries/{time_entry_id}"
    
    # Stop the timer by setting the stop time to now
    payload = {
        "stop": datetime.now(timezone.utc).isoformat()
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.patch(url, headers=headers, json=payload) as response:
            if response.status == 429:
                retry_after = response.headers.get("Retry-After", "60")
                raise Exception(
                    f"Rate limit exceeded. Please wait {retry_after} seconds before retrying."
                )
            response.raise_for_status()
            return await response.json()


async def get_time_entries(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 10
) -> list[dict[str, Any]]:
    """
    Get time entries with optional filtering.
    
    Args:
        start_date: Filter entries from this date (YYYY-MM-DD or RFC3339)
        end_date: Filter entries until this date (YYYY-MM-DD or RFC3339)
        limit: Maximum number of entries to return (default: 10)
    
    Returns:
        List of time entry objects
    """
    headers = get_auth_headers()
    url = f"{TOGGL_API_BASE}/me/time_entries"
    
    params: dict[str, Any] = {}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 429:
                retry_after = response.headers.get("Retry-After", "60")
                raise Exception(
                    f"Rate limit exceeded. Please wait {retry_after} seconds before retrying."
                )
            response.raise_for_status()
            entries = await response.json()
            
            # Limit results
            if isinstance(entries, list):
                return entries[:limit]
            return entries.get("items", [])[:limit] if isinstance(entries, dict) else []


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools."""
    return [
        Tool(
            name="start_timer",
            description="Start a new time tracking entry in Toggl. Requires a workspace ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "workspace_id": {
                        "type": "integer",
                        "description": "Toggl workspace ID (required)"
                    },
                    "description": {
                        "type": "string",
                        "description": "Description of the task being tracked"
                    },
                    "project_id": {
                        "type": "integer",
                        "description": "Project ID to associate this time entry with"
                    },
                    "tag_ids": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "List of tag IDs to apply to this time entry"
                    },
                    "billable": {
                        "type": "boolean",
                        "description": "Whether this time entry is billable"
                    }
                },
                "required": ["workspace_id"]
            }
        ),
        Tool(
            name="stop_timer",
            description="Stop the currently running time entry in Toggl. Automatically finds and stops the active timer.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="view_timers",
            description="View existing time entries from Toggl with optional date filtering.",
            inputSchema={
                "type": "object",
                "properties": {
                    "start_date": {
                        "type": "string",
                        "description": "Filter entries from this date (YYYY-MM-DD or RFC3339 format)"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "Filter entries until this date (YYYY-MM-DD or RFC3339 format)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of entries to return (default: 10)",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 100
                    }
                },
                "required": []
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> Sequence[TextContent]:
    """Handle tool calls."""
    
    try:
        if name == "start_timer":
            workspace_id = arguments.get("workspace_id")
            if not workspace_id:
                return [TextContent(
                    type="text",
                    text="❌ Error: workspace_id is required to start a timer"
                )]
            
            description = arguments.get("description")
            project_id = arguments.get("project_id")
            tag_ids = arguments.get("tag_ids")
            billable = arguments.get("billable")
            
            result = await start_time_entry(
                workspace_id=workspace_id,
                description=description,
                project_id=project_id,
                tag_ids=tag_ids,
                billable=billable
            )
            
            desc = result.get("description", "No description")
            entry_id = result.get("id", "Unknown")
            start_time = result.get("start", "Unknown")
            
            return [TextContent(
                type="text",
                text=f"✅ Timer started!\n\n"
                     f"Entry ID: {entry_id}\n"
                     f"Description: {desc}\n"
                     f"Start time: {start_time}\n"
                     f"Status: Running"
            )]
        
        elif name == "stop_timer":
            # First, get the current running timer
            current_entry = await get_current_time_entry()
            
            if not current_entry:
                return [TextContent(
                    type="text",
                    text="ℹ️ No timer is currently running."
                )]
            
            workspace_id = current_entry.get("workspace_id")
            time_entry_id = current_entry.get("id")
            
            if not workspace_id or not time_entry_id:
                return [TextContent(
                    type="text",
                    text="❌ Error: Could not determine workspace_id or time_entry_id from current timer"
                )]
            
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
            
            return [TextContent(
                type="text",
                text=f"✅ Timer stopped!\n\n"
                     f"Entry ID: {entry_id}\n"
                     f"Description: {desc}\n"
                     f"Start time: {start_time}\n"
                     f"Stop time: {stop_time}\n"
                     f"Duration: {duration_str}"
            )]
        
        elif name == "view_timers":
            start_date = arguments.get("start_date")
            end_date = arguments.get("end_date")
            limit = arguments.get("limit", 10)
            
            entries = await get_time_entries(
                start_date=start_date,
                end_date=end_date,
                limit=limit
            )
            
            if not entries:
                return [TextContent(
                    type="text",
                    text="ℹ️ No time entries found."
                )]
            
            # Format entries for display
            entries_text = []
            for i, entry in enumerate(entries, 1):
                desc = entry.get("description", "No description")
                entry_id = entry.get("id", "Unknown")
                start_time = entry.get("start", "Unknown")
                stop_time = entry.get("stop", "Still running" if entry.get("duration", 0) < 0 else entry.get("stop", "Unknown"))
                duration = entry.get("duration", 0)
                project_name = entry.get("project_name", "No project")
                
                # Format duration
                if duration < 0:
                    duration_str = "Running..."
                elif duration > 0:
                    hours = duration // 3600
                    minutes = (duration % 3600) // 60
                    seconds = duration % 60
                    duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                else:
                    duration_str = "0:00:00"
                
                entries_text.append(
                    f"{i}. Entry #{entry_id}\n"
                    f"   Description: {desc}\n"
                    f"   Project: {project_name}\n"
                    f"   Start: {start_time}\n"
                    f"   Stop: {stop_time}\n"
                    f"   Duration: {duration_str}\n"
                )
            
            return [TextContent(
                type="text",
                text=f"📊 Found {len(entries)} time entry/entries:\n\n" + "\n".join(entries_text)
            )]
        
        else:
            return [TextContent(type="text", text=f"❌ Unknown tool: {name}")]
    
    except ValueError as e:
        return [TextContent(type="text", text=f"❌ Configuration Error: {str(e)}")]
    except aiohttp.ClientResponseError as e:
        if e.status == 401:
            return [TextContent(
                type="text",
                text="❌ Authentication Error: Invalid API token. Please check your TOGGL_API_TOKEN."
            )]
        elif e.status == 403:
            return [TextContent(
                type="text",
                text="❌ Authorization Error: You don't have permission to access this resource."
            )]
        elif e.status == 404:
            return [TextContent(
                type="text",
                text="❌ Not Found: The requested resource was not found."
            )]
        else:
            return [TextContent(
                type="text",
                text=f"❌ API Error ({e.status}): {e.message}"
            )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"❌ Error: {str(e)}"
        )]


async def main():
    """Run the MCP server using stdio transport."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())

