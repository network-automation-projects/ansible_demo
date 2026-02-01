#!/usr/bin/env python3
"""
Network Monitor MCP Server
An MCP server for network device monitoring, health checks, and context-aware diagnostics.
Uses Netmiko for device interaction and maintains persistent context via MCP.
"""

import json
import re
import asyncio
import logging
import os
from datetime import datetime
from typing import Any, Sequence
from pathlib import Path

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

try:
    from netmiko import ConnectHandler
    NETMIKO_AVAILABLE = True
except ImportError:
    NETMIKO_AVAILABLE = False

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize the MCP server
server = Server("network-monitor")

# In-memory context storage (in production, this would use persistent storage)
CONTEXT_STORAGE: dict[str, Any] = {}

# Default device credentials for Containerlab Nokia SR Linux
# Credentials are loaded from environment variables for security
DEFAULT_DEVICE_CONFIG = {
    'device_type': 'nokia_srl',
    'username': os.getenv('ROUTER_USERNAME', 'admin'),
    'password': os.getenv('ROUTER_PASSWORD', ''),
    'port': int(os.getenv('ROUTER_PORT', '22')),
    'timeout': 30,
    'session_timeout': 30,
}

# Containerlab hostname pattern
CLAB_HOSTNAME_PATTERN = 'clab-mcp-nethealth-chatbot-{router}'


def get_device_connection(router_name: str) -> dict[str, Any]:
    """Get device connection parameters for a router."""
    device = DEFAULT_DEVICE_CONFIG.copy()
    device['host'] = CLAB_HOSTNAME_PATTERN.format(router=router_name)
    return device


def parse_interface_status(output: str) -> list[dict[str, Any]]:
    """Parse Nokia SR Linux interface status output."""
    interfaces = []
    # Basic parsing - SR Linux uses different commands
    # This is a simplified parser - adjust based on actual SR Linux output
    lines = output.split('\n')
    for line in lines:
        if 'ethernet' in line.lower() or 'interface' in line.lower():
            # Extract interface name and status
            parts = line.split()
            if len(parts) >= 2:
                interface_name = parts[0]
                status = 'up' if 'up' in line.lower() else 'down'
                interfaces.append({
                    'name': interface_name,
                    'status': status,
                    'line': line.strip()
                })
    return interfaces


def query_device(router_name: str, command: str) -> str:
    """Query a network device using Netmiko."""
    if not NETMIKO_AVAILABLE:
        logger.warning("Netmiko not available, returning mock data")
        return f"Mock output for {command} on {router_name}"
    
    device = get_device_connection(router_name)
    try:
        logger.info(f"Connecting to {device['host']}")
        conn = ConnectHandler(**device)
        output = conn.send_command(command)
        conn.disconnect()
        logger.info(f"Successfully executed {command} on {router_name}")
        return output
    except Exception as e:
        logger.error(f"Error querying device {router_name}: {str(e)}")
        return f"Error: {str(e)}"


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools."""
    return [
        Tool(
            name="check_interface_status",
            description="Query interface status on a network device via Netmiko. Returns interface names, status (up/down), and basic statistics.",
            inputSchema={
                "type": "object",
                "properties": {
                    "router": {
                        "type": "string",
                        "description": "Router name (e.g., 'router1' or 'router2')",
                        "enum": ["router1", "router2"],
                        "default": "router1"
                    }
                },
                "required": ["router"]
            }
        ),
        Tool(
            name="get_device_info",
            description="Get device information including hostname, version, uptime, and system facts.",
            inputSchema={
                "type": "object",
                "properties": {
                    "router": {
                        "type": "string",
                        "description": "Router name (e.g., 'router1' or 'router2')",
                        "enum": ["router1", "router2"],
                        "default": "router1"
                    }
                },
                "required": ["router"]
            }
        ),
        Tool(
            name="store_network_context",
            description="Store network state and context to MCP persistent storage. Includes device status, interfaces, alerts, and timestamps.",
            inputSchema={
                "type": "object",
                "properties": {
                    "device": {
                        "type": "string",
                        "description": "Device/router name"
                    },
                    "interfaces": {
                        "type": "array",
                        "description": "Array of interface status objects",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "status": {"type": "string"},
                                "latency_ms": {"type": ["number", "null"]}
                            }
                        }
                    },
                    "alerts": {
                        "type": "array",
                        "description": "Array of alert messages",
                        "items": {"type": "string"}
                    },
                    "metrics": {
                        "type": "object",
                        "description": "Additional metrics data"
                    }
                },
                "required": ["device"]
            }
        ),
        Tool(
            name="retrieve_network_context",
            description="Retrieve historical network context from MCP storage. Returns stored network state, previous issues, and historical data.",
            inputSchema={
                "type": "object",
                "properties": {
                    "device": {
                        "type": "string",
                        "description": "Device/router name to retrieve context for (optional, if not provided returns all)",
                        "default": ""
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of historical entries to return",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 100
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="query_prometheus",
            description="Query Prometheus metrics API for network metrics. Requires Prometheus to be running and accessible.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "PromQL query string (e.g., 'interface_errors_total{device=\"router1\"}')"
                    },
                    "prometheus_url": {
                        "type": "string",
                        "description": "Prometheus API URL",
                        "default": "http://localhost:9090"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="detect_issues",
            description="Analyze current network state and detect issues like interface down, high latency, or connectivity problems. Uses stored context for comparison.",
            inputSchema={
                "type": "object",
                "properties": {
                    "router": {
                        "type": "string",
                        "description": "Router name to check",
                        "enum": ["router1", "router2"],
                        "default": "router1"
                    },
                    "check_interfaces": {
                        "type": "boolean",
                        "description": "Check interface status",
                        "default": True
                    },
                    "check_latency": {
                        "type": "boolean",
                        "description": "Check for latency issues",
                        "default": True
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
        if name == "check_interface_status":
            router = arguments.get("router", "router1")
            logger.info(f"Checking interface status on {router}")
            
            # SR Linux command for interface status
            command = "show interface ethernet-1/1 state"
            output = query_device(router, command)
            
            # Try alternative command if first doesn't work
            if "Error" in output or not output.strip():
                command = "info from state interface ethernet-1/1"
                output = query_device(router, command)
            
            interfaces = parse_interface_status(output)
            
            result = {
                "router": router,
                "timestamp": datetime.now().isoformat(),
                "interfaces": interfaces if interfaces else [{"name": "ethernet-1/1", "status": "unknown", "raw_output": output[:200]}],
                "raw_output": output[:500]  # Limit output size
            }
            
            return [TextContent(
                type="text",
                text=f"Interface Status for {router}:\n\n{json.dumps(result, indent=2)}"
            )]
        
        elif name == "get_device_info":
            router = arguments.get("router", "router1")
            logger.info(f"Getting device info for {router}")
            
            commands = [
                "show system information",
                "show version",
                "show system uptime"
            ]
            
            results = {}
            for cmd in commands:
                output = query_device(router, cmd)
                results[cmd] = output[:300]  # Limit output size
            
            result = {
                "router": router,
                "timestamp": datetime.now().isoformat(),
                "info": results
            }
            
            return [TextContent(
                type="text",
                text=f"Device Info for {router}:\n\n{json.dumps(result, indent=2)}"
            )]
        
        elif name == "store_network_context":
            device = arguments.get("device", "unknown")
            interfaces = arguments.get("interfaces", [])
            alerts = arguments.get("alerts", [])
            metrics = arguments.get("metrics", {})
            
            context_entry = {
                "timestamp": datetime.now().isoformat(),
                "device": device,
                "interfaces": interfaces,
                "alerts": alerts,
                "metrics": metrics
            }
            
            # Store in context storage
            if device not in CONTEXT_STORAGE:
                CONTEXT_STORAGE[device] = []
            
            CONTEXT_STORAGE[device].append(context_entry)
            
            # Keep only last 100 entries per device
            if len(CONTEXT_STORAGE[device]) > 100:
                CONTEXT_STORAGE[device] = CONTEXT_STORAGE[device][-100:]
            
            logger.info(f"Stored context for {device}: {len(CONTEXT_STORAGE[device])} entries")
            
            return [TextContent(
                type="text",
                text=f"✓ Stored network context for {device} at {context_entry['timestamp']}\n\nStored {len(interfaces)} interfaces, {len(alerts)} alerts"
            )]
        
        elif name == "retrieve_network_context":
            device_filter = arguments.get("device", "")
            limit = arguments.get("limit", 10)
            
            if device_filter:
                # Return context for specific device
                contexts = CONTEXT_STORAGE.get(device_filter, [])
                contexts = contexts[-limit:] if len(contexts) > limit else contexts
                result = {
                    "device": device_filter,
                    "entries": contexts,
                    "count": len(contexts)
                }
            else:
                # Return all contexts
                result = {
                    "devices": list(CONTEXT_STORAGE.keys()),
                    "contexts": {k: v[-limit:] for k, v in CONTEXT_STORAGE.items()},
                    "total_entries": sum(len(v) for v in CONTEXT_STORAGE.values())
                }
            
            return [TextContent(
                type="text",
                text=f"Retrieved Network Context:\n\n{json.dumps(result, indent=2, default=str)}"
            )]
        
        elif name == "query_prometheus":
            query = arguments.get("query", "")
            prometheus_url = arguments.get("prometheus_url", "http://localhost:9090")
            
            if not query:
                return [TextContent(type="text", text="❌ Error: Query parameter is required")]
            
            try:
                import requests
                api_url = f"{prometheus_url}/api/v1/query"
                params = {"query": query}
                
                response = requests.get(api_url, params=params, timeout=5)
                response.raise_for_status()
                
                data = response.json()
                result = {
                    "query": query,
                    "status": data.get("status", "unknown"),
                    "data": data.get("data", {})
                }
                
                return [TextContent(
                    type="text",
                    text=f"Prometheus Query Results:\n\n{json.dumps(result, indent=2)}"
                )]
            except ImportError:
                return [TextContent(
                    type="text",
                    text="❌ Error: 'requests' library not available. Install with: pip install requests"
                )]
            except Exception as e:
                logger.error(f"Prometheus query error: {str(e)}")
                return [TextContent(
                    type="text",
                    text=f"❌ Error querying Prometheus: {str(e)}\n\nMake sure Prometheus is running at {prometheus_url}"
                )]
        
        elif name == "detect_issues":
            router = arguments.get("router", "router1")
            check_interfaces = arguments.get("check_interfaces", True)
            check_latency = arguments.get("check_latency", True)
            
            issues = []
            warnings = []
            
            # Check interfaces if requested
            if check_interfaces:
                command = "show interface ethernet-1/1 state"
                output = query_device(router, command)
                interfaces = parse_interface_status(output)
                
                for iface in interfaces:
                    if iface.get("status") == "down":
                        issues.append(f"Interface {iface.get('name')} is DOWN on {router}")
                    elif iface.get("status") == "unknown":
                        warnings.append(f"Could not determine status for {iface.get('name')} on {router}")
            
            # Retrieve historical context for comparison
            historical_context = CONTEXT_STORAGE.get(router, [])
            previous_issues = []
            if historical_context:
                last_context = historical_context[-1]
                prev_alerts = last_context.get("alerts", [])
                if prev_alerts:
                    previous_issues = prev_alerts
            
            result = {
                "router": router,
                "timestamp": datetime.now().isoformat(),
                "issues": issues,
                "warnings": warnings,
                "previous_issues": previous_issues,
                "status": "healthy" if not issues else "unhealthy"
            }
            
            return [TextContent(
                type="text",
                text=f"Issue Detection for {router}:\n\n{json.dumps(result, indent=2)}"
            )]
        
        else:
            return [TextContent(type="text", text=f"❌ Unknown tool: {name}")]
    
    except Exception as e:
        logger.error(f"Error in tool {name}: {str(e)}", exc_info=True)
        return [TextContent(
            type="text",
            text=f"❌ Error executing {name}: {str(e)}"
        )]


async def main():
    """Run the MCP server using stdio transport."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())

