#!/usr/bin/env python3
"""
Diagnostic script to check MCP kalilinux server setup
"""
import json
import os
import subprocess
from pathlib import Path

LOG_PATH = "/Users/rebeccaclarke/Documents/Financial/Gigs/Devops - Software Engineering/.cursor/debug.log"

def log_entry(message, data=None, hypothesis_id="DIAG"):
    """Write diagnostic log entry"""
    try:
        with open(LOG_PATH, 'a') as f:
            entry = {
                "sessionId": "debug-session",
                "runId": "run1",
                "hypothesisId": hypothesis_id,
                "location": "diagnose_mcp.py",
                "message": message,
                "data": data or {},
                "timestamp": int(__import__('time').time() * 1000)
            }
            f.write(json.dumps(entry) + '\n')
    except Exception as e:
        print(f"Failed to write log: {e}")

def check_docker_image():
    """Check if Docker image exists"""
    log_entry("Checking Docker image", {"image": "kali-security-mcp-server:latest"}, "A")
    try:
        result = subprocess.run(
            ["docker", "images", "kali-security-mcp-server:latest", "--format", "{{.Repository}}:{{.Tag}}"],
            capture_output=True,
            text=True,
            timeout=5
        )
        exists = bool(result.stdout.strip())
        log_entry("Docker image check result", {"exists": exists, "output": result.stdout.strip()}, "A")
        return exists
    except Exception as e:
        log_entry("Docker image check error", {"error": str(e)}, "A")
        return False

def check_catalog_file():
    """Check if catalog file exists and is readable"""
    catalog_path = Path.home() / ".docker" / "mcp" / "catalogs" / "kalilinux-catalog.yaml"
    log_entry("Checking catalog file", {"path": str(catalog_path)}, "B")
    exists = catalog_path.exists()
    readable = catalog_path.is_file() and os.access(catalog_path, os.R_OK)
    log_entry("Catalog file check result", {"exists": exists, "readable": readable}, "B")
    
    if exists and readable:
        try:
            content = catalog_path.read_text()
            log_entry("Catalog file content", {"size": len(content), "has_kali_security": "kali-security" in content}, "B")
        except Exception as e:
            log_entry("Catalog file read error", {"error": str(e)}, "B")
    
    return exists and readable

def check_registry_entry():
    """Check if registry has kali-security entry"""
    registry_path = Path.home() / ".docker" / "mcp" / "registry.yaml"
    log_entry("Checking registry file", {"path": str(registry_path)}, "E")
    exists = registry_path.exists()
    log_entry("Registry file exists", {"exists": exists}, "E")
    
    if exists:
        try:
            content = registry_path.read_text()
            has_entry = "kali-security" in content
            log_entry("Registry entry check", {"has_kali_security": has_entry, "content_preview": content[:200]}, "E")
            return has_entry
        except Exception as e:
            log_entry("Registry read error", {"error": str(e)}, "E")
    
    return False

def check_mcp_logs():
    """Check recent MCP gateway logs for kali-security"""
    log_dir = Path.home() / "Library" / "Application Support" / "Cursor" / "logs"
    log_entry("Checking MCP logs directory", {"path": str(log_dir)}, "D")
    
    if not log_dir.exists():
        log_entry("MCP logs directory not found", {}, "D")
        return False
    
    # Find most recent log directory
    log_dirs = sorted([d for d in log_dir.iterdir() if d.is_dir()], reverse=True)
    if not log_dirs:
        log_entry("No log directories found", {}, "D")
        return False
    
    latest_log_dir = log_dirs[0]
    mcp_log_file = latest_log_dir / "window1" / "exthost" / "anysphere.cursor-mcp" / "MCP user-mcp-toolkit-gateway.log"
    
    log_entry("Checking MCP log file", {"path": str(mcp_log_file)}, "D")
    
    if mcp_log_file.exists():
        try:
            content = mcp_log_file.read_text()
            has_kali = "kali-security" in content or "kali" in content.lower()
            log_entry("MCP log analysis", {"has_kali_reference": has_kali, "log_size": len(content)}, "D")
            return has_kali
        except Exception as e:
            log_entry("MCP log read error", {"error": str(e)}, "D")
    
    return False

def main():
    """Run all diagnostic checks"""
    log_entry("Starting MCP diagnostics", {}, "DIAG")
    
    results = {
        "docker_image": check_docker_image(),
        "catalog_file": check_catalog_file(),
        "registry_entry": check_registry_entry(),
        "mcp_logs_mention_kali": check_mcp_logs()
    }
    
    log_entry("Diagnostic results summary", results, "DIAG")
    
    print("\n=== MCP Kali Security Diagnostic Results ===")
    print(f"Docker image exists: {results['docker_image']}")
    print(f"Catalog file exists: {results['catalog_file']}")
    print(f"Registry entry exists: {results['registry_entry']}")
    print(f"MCP logs mention kali: {results['mcp_logs_mention_kali']}")
    print("\nCheck the debug log for detailed information.")

if __name__ == "__main__":
    main()


