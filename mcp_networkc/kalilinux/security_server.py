#!/usr/bin/env python3
"""
Kali Security Tools MCP Server
An MCP server for security testing tools including nmap, nikto, sqlmap,
wpscan, dirb, and searchsploit. Designed for educational web penetration
testing on your own environment.
"""

import os
import re
import asyncio
import subprocess
from typing import Any, Sequence, Optional
from urllib.parse import urlparse
from ipaddress import ip_address, AddressValueError
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Initialize the MCP server
server = Server("kali-security-tools")

# Configuration from environment variables
SCAN_TIMEOUT = int(os.getenv("SCAN_TIMEOUT", "300"))
MAX_OUTPUT_SIZE = int(os.getenv("MAX_OUTPUT_SIZE", "1048576"))  # 1MB default
ALLOWED_NETWORKS = os.getenv("ALLOWED_NETWORKS", "").split(",") if os.getenv("ALLOWED_NETWORKS") else []


def validate_url(url: str) -> bool:
    """Validate URL format and scheme."""
    try:
        result = urlparse(url)
        if not result.scheme or result.scheme not in ["http", "https"]:
            return False
        if not result.netloc:
            return False
        # Basic validation - allow http/https URLs
        return True
    except Exception:
        return False


def validate_ip(ip: str) -> bool:
    """Validate IP address format (IPv4 or IPv6)."""
    try:
        ip_address(ip)
        return True
    except (ValueError, AddressValueError):
        return False


def validate_host(host: str) -> bool:
    """Validate host (IP address or hostname)."""
    # Allow IP addresses
    if validate_ip(host):
        return True
    # Allow hostnames (basic validation)
    if re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$', host):
        return True
    return False


def sanitize_string(value: str, max_length: int = 1000) -> str:
    """Sanitize string input to prevent injection."""
    # Remove any shell metacharacters
    value = re.sub(r'[;&|`$(){}[\]<>"\']', '', value)
    # Limit length
    if len(value) > max_length:
        value = value[:max_length]
    return value.strip()


def check_network_allowed(target: str) -> bool:
    """Check if target is in allowed networks (if configured)."""
    if not ALLOWED_NETWORKS or not any(ALLOWED_NETWORKS):
        return True  # No restrictions
    
    # Extract IP from target if it's a URL
    if "://" in target:
        parsed = urlparse(target)
        target = parsed.hostname or target
    
    # If it's an IP, check against allowed networks
    if validate_ip(target):
        from ipaddress import ip_network, ip_address
        target_ip = ip_address(target)
        for network_str in ALLOWED_NETWORKS:
            if network_str.strip():
                try:
                    network = ip_network(network_str.strip(), strict=False)
                    if target_ip in network:
                        return True
                except Exception:
                    continue
        return False
    
    return True  # Allow hostnames if no IP restrictions


async def run_command(cmd: list[str], timeout: int = SCAN_TIMEOUT) -> tuple[str, str, int]:
    """
    Run a command safely using subprocess.
    Returns: (stdout, stderr, returncode)
    """
    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            limit=MAX_OUTPUT_SIZE
        )
        
        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            process.kill()
            await process.wait()
            return "", f"Command timed out after {timeout} seconds", -1
        
        stdout_text = stdout.decode('utf-8', errors='replace')[:MAX_OUTPUT_SIZE]
        stderr_text = stderr.decode('utf-8', errors='replace')[:MAX_OUTPUT_SIZE]
        
        return stdout_text, stderr_text, process.returncode
    except Exception as e:
        return "", f"Error executing command: {str(e)}", -1


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools."""
    return [
        Tool(
            name="nmap_scan",
            description="Perform network port scanning using nmap. Scans specified host/port for open ports and services.",
            inputSchema={
                "type": "object",
                "properties": {
                    "target": {
                        "type": "string",
                        "description": "Target host (IP address or hostname) to scan"
                    },
                    "ports": {
                        "type": "string",
                        "description": "Port specification (e.g., '80,443', '1-1000', '80'). Default: common ports",
                        "default": ""
                    },
                    "scan_type": {
                        "type": "string",
                        "description": "Scan type: 'syn' (default), 'connect', 'udp', or 'all'",
                        "enum": ["syn", "connect", "udp", "all"],
                        "default": "syn"
                    }
                },
                "required": ["target"]
            }
        ),
        Tool(
            name="nikto_scan",
            description="Perform web server vulnerability scanning using nikto. Scans web servers for known vulnerabilities.",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Target URL (e.g., http://example.com or https://example.com)"
                    },
                    "port": {
                        "type": "integer",
                        "description": "Port number (default: 80 for http, 443 for https)",
                        "default": 0
                    }
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="sqlmap_scan",
            description="Perform SQL injection testing using sqlmap. Tests web applications for SQL injection vulnerabilities.",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Target URL with parameter (e.g., http://example.com/page?id=1)"
                    },
                    "method": {
                        "type": "string",
                        "description": "HTTP method: 'GET' (default) or 'POST'",
                        "enum": ["GET", "POST"],
                        "default": "GET"
                    }
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="wpscan_scan",
            description="Perform WordPress vulnerability scanning using wpscan. Scans WordPress installations for vulnerabilities.",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "WordPress site URL (e.g., http://example.com or https://example.com)"
                    },
                    "scan_type": {
                        "type": "string",
                        "description": "Scan type: 'basic' (default), 'plugins', 'themes', or 'full'",
                        "enum": ["basic", "plugins", "themes", "full"],
                        "default": "basic"
                    }
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="dirb_scan",
            description="Perform directory/file brute-forcing using dirb. Discovers hidden directories and files on web servers.",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Target URL (e.g., http://example.com or https://example.com)"
                    },
                    "wordlist": {
                        "type": "string",
                        "description": "Wordlist to use: 'common' (default), 'small', 'medium', or 'big'",
                        "enum": ["common", "small", "medium", "big"],
                        "default": "common"
                    }
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="searchsploit_search",
            description="Search the Exploit Database using searchsploit. Searches for exploits by keyword, CVE, or platform.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (keyword, CVE number, platform, etc.)"
                    },
                    "type": {
                        "type": "string",
                        "description": "Search type: 'all' (default), 'exploits', or 'shellcode'",
                        "enum": ["all", "exploits", "shellcode"],
                        "default": "all"
                    }
                },
                "required": ["query"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> Sequence[TextContent]:
    """Handle tool calls."""
    
    try:
        if name == "nmap_scan":
            target = arguments.get("target", "").strip()
            if not target:
                return [TextContent(type="text", text="❌ Error: target is required")]
            
            if not validate_host(target):
                return [TextContent(type="text", text="❌ Error: Invalid target host format")]
            
            if not check_network_allowed(target):
                return [TextContent(type="text", text="❌ Error: Target not in allowed networks")]
            
            ports = sanitize_string(arguments.get("ports", ""), max_length=100)
            scan_type = arguments.get("scan_type", "syn")
            
            # Build nmap command
            cmd = ["nmap"]
            
            # Add scan type flags
            if scan_type == "syn":
                cmd.extend(["-sS"])
            elif scan_type == "connect":
                cmd.extend(["-sT"])
            elif scan_type == "udp":
                cmd.extend(["-sU"])
            elif scan_type == "all":
                cmd.extend(["-sS", "-sT", "-sU"])
            
            # Add port specification
            if ports:
                cmd.extend(["-p", ports])
            else:
                cmd.extend(["-F"])  # Fast scan of common ports
            
            # Add target
            cmd.append(target)
            
            stdout, stderr, returncode = await run_command(cmd)
            
            result_text = f"🔍 Nmap Scan Results\n\n"
            result_text += f"Target: {target}\n"
            result_text += f"Ports: {ports if ports else 'Common ports (fast scan)'}\n"
            result_text += f"Scan Type: {scan_type}\n"
            result_text += f"Command: {' '.join(cmd)}\n\n"
            result_text += f"{'='*60}\n\n"
            
            if stdout:
                result_text += f"Output:\n{stdout}\n"
            if stderr:
                result_text += f"\nErrors/Warnings:\n{stderr}\n"
            if returncode != 0:
                result_text += f"\nExit Code: {returncode}\n"
            
            return [TextContent(type="text", text=result_text)]
        
        elif name == "nikto_scan":
            url = arguments.get("url", "").strip()
            if not url:
                return [TextContent(type="text", text="❌ Error: url is required")]
            
            if not validate_url(url):
                return [TextContent(type="text", text="❌ Error: Invalid URL format. Must be http:// or https://")]
            
            if not check_network_allowed(url):
                return [TextContent(type="text", text="❌ Error: Target not in allowed networks")]
            
            port = arguments.get("port", 0)
            
            # Build nikto command
            cmd = ["nikto", "-h", url]
            if port > 0 and port <= 65535:
                cmd.extend(["-p", str(port)])
            
            stdout, stderr, returncode = await run_command(cmd, timeout=600)
            
            result_text = f"🔍 Nikto Scan Results\n\n"
            result_text += f"Target: {url}\n"
            if port > 0:
                result_text += f"Port: {port}\n"
            result_text += f"Command: {' '.join(cmd)}\n\n"
            result_text += f"{'='*60}\n\n"
            
            if stdout:
                result_text += f"Output:\n{stdout}\n"
            if stderr:
                result_text += f"\nErrors/Warnings:\n{stderr}\n"
            if returncode != 0:
                result_text += f"\nExit Code: {returncode}\n"
            
            return [TextContent(type="text", text=result_text)]
        
        elif name == "sqlmap_scan":
            url = arguments.get("url", "").strip()
            if not url:
                return [TextContent(type="text", text="❌ Error: url is required")]
            
            if not validate_url(url):
                return [TextContent(type="text", text="❌ Error: Invalid URL format. Must be http:// or https://")]
            
            if not check_network_allowed(url):
                return [TextContent(type="text", text="❌ Error: Target not in allowed networks")]
            
            method = arguments.get("method", "GET").upper()
            
            # Build sqlmap command (basic scan)
            cmd = ["sqlmap", "-u", url, "--batch", "--crawl=2"]
            if method == "POST":
                cmd.extend(["--data", ""])  # User should provide data if needed
            
            stdout, stderr, returncode = await run_command(cmd, timeout=600)
            
            result_text = f"🔍 SQLMap Scan Results\n\n"
            result_text += f"Target: {url}\n"
            result_text += f"Method: {method}\n"
            result_text += f"Command: {' '.join(cmd)}\n\n"
            result_text += f"{'='*60}\n\n"
            
            if stdout:
                result_text += f"Output:\n{stdout}\n"
            if stderr:
                result_text += f"\nErrors/Warnings:\n{stderr}\n"
            if returncode != 0:
                result_text += f"\nExit Code: {returncode}\n"
            
            return [TextContent(type="text", text=result_text)]
        
        elif name == "wpscan_scan":
            url = arguments.get("url", "").strip()
            if not url:
                return [TextContent(type="text", text="❌ Error: url is required")]
            
            if not validate_url(url):
                return [TextContent(type="text", text="❌ Error: Invalid URL format. Must be http:// or https://")]
            
            if not check_network_allowed(url):
                return [TextContent(type="text", text="❌ Error: Target not in allowed networks")]
            
            scan_type = arguments.get("scan_type", "basic")
            
            # Build wpscan command
            cmd = ["wpscan", "--url", url, "--no-update", "--disable-tls-checks"]
            
            if scan_type == "plugins":
                cmd.extend(["--enumerate", "p"])
            elif scan_type == "themes":
                cmd.extend(["--enumerate", "t"])
            elif scan_type == "full":
                cmd.extend(["--enumerate", "vp,vt,u"])
            # basic scan uses default options
            
            stdout, stderr, returncode = await run_command(cmd, timeout=600)
            
            result_text = f"🔍 WPScan Results\n\n"
            result_text += f"Target: {url}\n"
            result_text += f"Scan Type: {scan_type}\n"
            result_text += f"Command: {' '.join(cmd)}\n\n"
            result_text += f"{'='*60}\n\n"
            
            if stdout:
                result_text += f"Output:\n{stdout}\n"
            if stderr:
                result_text += f"\nErrors/Warnings:\n{stderr}\n"
            if returncode != 0:
                result_text += f"\nExit Code: {returncode}\n"
            
            return [TextContent(type="text", text=result_text)]
        
        elif name == "dirb_scan":
            url = arguments.get("url", "").strip()
            if not url:
                return [TextContent(type="text", text="❌ Error: url is required")]
            
            if not validate_url(url):
                return [TextContent(type="text", text="❌ Error: Invalid URL format. Must be http:// or https://")]
            
            if not check_network_allowed(url):
                return [TextContent(type="text", text="❌ Error: Target not in allowed networks")]
            
            wordlist = arguments.get("wordlist", "common")
            
            # Map wordlist names to common dirb wordlists
            wordlist_map = {
                "common": "/usr/share/dirb/wordlists/common.txt",
                "small": "/usr/share/dirb/wordlists/small.txt",
                "medium": "/usr/share/dirb/wordlists/big.txt",
                "big": "/usr/share/dirb/wordlists/big.txt"
            }
            
            wordlist_path = wordlist_map.get(wordlist, wordlist_map["common"])
            
            # Build dirb command
            cmd = ["dirb", url, wordlist_path, "-S", "-w"]
            
            stdout, stderr, returncode = await run_command(cmd, timeout=600)
            
            result_text = f"🔍 Dirb Scan Results\n\n"
            result_text += f"Target: {url}\n"
            result_text += f"Wordlist: {wordlist}\n"
            result_text += f"Command: {' '.join(cmd)}\n\n"
            result_text += f"{'='*60}\n\n"
            
            if stdout:
                result_text += f"Output:\n{stdout}\n"
            if stderr:
                result_text += f"\nErrors/Warnings:\n{stderr}\n"
            if returncode != 0:
                result_text += f"\nExit Code: {returncode}\n"
            
            return [TextContent(type="text", text=result_text)]
        
        elif name == "searchsploit_search":
            query = arguments.get("query", "").strip()
            if not query:
                return [TextContent(type="text", text="❌ Error: query is required")]
            
            query = sanitize_string(query, max_length=200)
            search_type = arguments.get("type", "all")
            
            # Build searchsploit command
            cmd = ["searchsploit"]
            
            if search_type == "exploits":
                cmd.append("--exclude", "shellcodes")
            elif search_type == "shellcode":
                cmd.append("--exclude", "exploits")
            # all includes both
            
            cmd.extend(["--json", query])
            
            stdout, stderr, returncode = await run_command(cmd)
            
            result_text = f"🔍 SearchSploit Results\n\n"
            result_text += f"Query: {query}\n"
            result_text += f"Type: {search_type}\n"
            result_text += f"Command: {' '.join(cmd)}\n\n"
            result_text += f"{'='*60}\n\n"
            
            if stdout:
                result_text += f"Output:\n{stdout}\n"
            if stderr:
                result_text += f"\nErrors/Warnings:\n{stderr}\n"
            if returncode != 0:
                result_text += f"\nExit Code: {returncode}\n"
            
            return [TextContent(type="text", text=result_text)]
        
        else:
            return [TextContent(type="text", text=f"❌ Unknown tool: {name}")]
    
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]


async def main():
    """Run the MCP server using stdio transport."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())

