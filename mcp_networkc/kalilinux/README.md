# Kali Security Tools MCP Server

An MCP (Model Context Protocol) server that provides security testing tools from a Kali Linux Docker container. Designed for educational web penetration testing on your own environment.

## Features

- **Network Scanning**: Port scanning with nmap
- **Web Vulnerability Scanning**: Web server scanning with nikto
- **SQL Injection Testing**: SQL injection detection with sqlmap
- **WordPress Scanning**: WordPress vulnerability scanning with wpscan
- **Directory Brute-Forcing**: Hidden directory discovery with dirb
- **Exploit Database Search**: Search exploits with searchsploit

## Security Features

- Runs as non-root user with minimal required Linux capabilities
- Input sanitization to prevent command injection
- Network restrictions (optional via environment variables)
- Output size limits and timeout enforcement
- Safe subprocess execution (no shell=True)

## Tools

### `nmap_scan`
Perform network port scanning using nmap.

**Parameters:**
- `target` (string, required): Target host (IP address or hostname) to scan
- `ports` (string, optional): Port specification (e.g., '80,443', '1-1000', '80'). Default: common ports
- `scan_type` (string, optional): Scan type - 'syn' (default), 'connect', 'udp', or 'all'

**Example:**
```
nmap_scan(target="192.168.1.1", ports="80,443", scan_type="syn")
```

### `nikto_scan`
Perform web server vulnerability scanning using nikto.

**Parameters:**
- `url` (string, required): Target URL (e.g., http://example.com or https://example.com)
- `port` (integer, optional): Port number (default: 80 for http, 443 for https)

**Example:**
```
nikto_scan(url="http://example.com", port=80)
```

### `sqlmap_scan`
Perform SQL injection testing using sqlmap.

**Parameters:**
- `url` (string, required): Target URL with parameter (e.g., http://example.com/page?id=1)
- `method` (string, optional): HTTP method - 'GET' (default) or 'POST'

**Example:**
```
sqlmap_scan(url="http://example.com/page?id=1", method="GET")
```

### `wpscan_scan`
Perform WordPress vulnerability scanning using wpscan.

**Parameters:**
- `url` (string, required): WordPress site URL (e.g., http://example.com or https://example.com)
- `scan_type` (string, optional): Scan type - 'basic' (default), 'plugins', 'themes', or 'full'

**Example:**
```
wpscan_scan(url="http://example.com", scan_type="full")
```

### `dirb_scan`
Perform directory/file brute-forcing using dirb.

**Parameters:**
- `url` (string, required): Target URL (e.g., http://example.com or https://example.com)
- `wordlist` (string, optional): Wordlist to use - 'common' (default), 'small', 'medium', or 'big'

**Example:**
```
dirb_scan(url="http://example.com", wordlist="common")
```

### `searchsploit_search`
Search the Exploit Database using searchsploit.

**Parameters:**
- `query` (string, required): Search query (keyword, CVE number, platform, etc.)
- `type` (string, optional): Search type - 'all' (default), 'exploits', or 'shellcode'

**Example:**
```
searchsploit_search(query="WordPress 5.0", type="exploits")
```

## Building and Running

### Prerequisites
- Docker Desktop installed
- Docker MCP Toolkit enabled in Docker Desktop beta features

### Build the Docker Image

```bash
cd kalilinux
docker build -t kali-security-mcp-server .
```

### Verify the Image

```bash
docker images | grep kali-security-mcp-server
```

## Environment Variables

The server supports the following environment variables:

- `SCAN_TIMEOUT`: Default timeout for tool execution in seconds (default: 300)
- `MAX_OUTPUT_SIZE`: Maximum output size in bytes (default: 1048576 = 1MB)
- `ALLOWED_NETWORKS`: Comma-separated list of allowed network ranges (optional, e.g., "192.168.1.0/24,10.0.0.0/8")

### Example with Environment Variables

```bash
docker run -e SCAN_TIMEOUT=600 -e ALLOWED_NETWORKS="192.168.1.0/24" kali-security-mcp-server
```

## Integration with Docker MCP Gateway

### 1. Create Custom Catalog (Optional)

Create a catalog file at `~/.docker/mcp/catalogs/my-custom-catalog.yaml`:

```yaml
servers:
  kali-security:
    ref: kali-security-mcp-server:latest
    description: Security testing tools MCP server for educational web penetration testing
    tools:
      - name: nmap_scan
        description: Perform network port scanning using nmap
      - name: nikto_scan
        description: Perform web server vulnerability scanning using nikto
      - name: sqlmap_scan
        description: Perform SQL injection testing using sqlmap
      - name: wpscan_scan
        description: Perform WordPress vulnerability scanning using wpscan
      - name: dirb_scan
        description: Perform directory/file brute-forcing using dirb
      - name: searchsploit_search
        description: Search the Exploit Database using searchsploit
```

### 2. Update Registry

Edit `~/.docker/mcp/registry.yaml` and add:

```yaml
  kali-security:
    ref: kali-security-mcp-server:latest
```

### 3. Configure MCP Client

Update your MCP client configuration (e.g., Claude Desktop, Cursor) to use the Docker MCP Gateway with your custom catalog.

**Important:** The kali-security server requires `NET_RAW` and `NET_ADMIN` capabilities for nmap to function properly. You must add these capabilities to your Docker MCP Gateway configuration.

#### For Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "docker-mcp": {
      "command": "docker",
      "args": [
        "mcp",
        "gateway",
        "run",
        "--volume",
        "/Users/YOUR_USERNAME:/home",
        "--cap-add",
        "NET_RAW",
        "--cap-add",
        "NET_ADMIN",
        "--catalog",
        "docker-mcp",
        "--catalog",
        "my-custom-catalog",
        "--registry",
        "/home/.docker/mcp/registry.yaml"
      ]
    }
  }
}
```

#### For Cursor

The configuration location depends on your Cursor version. Common locations:
- Settings UI: Open Cursor Settings → Extensions → MCP Servers
- Config file: `~/Library/Application Support/Cursor/User/globalStorage/mcp.json` (if exists)

Add the following configuration:

```json
{
  "mcpServers": {
    "docker-mcp": {
      "command": "docker",
      "args": [
        "mcp",
        "gateway",
        "run",
        "--volume",
        "/Users/YOUR_USERNAME:/home",
        "--cap-add",
        "NET_RAW",
        "--cap-add",
        "NET_ADMIN",
        "--catalog",
        "docker-mcp",
        "--catalog",
        "my-custom-catalog",
        "--registry",
        "/home/.docker/mcp/registry.yaml"
      ]
    }
  }
}
```

**Key additions:** The `--cap-add NET_RAW` and `--cap-add NET_ADMIN` flags are required for nmap to work properly.

Replace `YOUR_USERNAME` with your actual username.

## Usage Examples

Once connected to an MCP client, you can use natural language:

- "Scan ports 80 and 443 on 192.168.1.1"
- "Run a nikto scan on http://example.com"
- "Test http://example.com/page?id=1 for SQL injection"
- "Scan http://example.com for WordPress vulnerabilities"
- "Brute force directories on http://example.com"
- "Search for WordPress exploits in the exploit database"

## Security Considerations

### Educational Use Only
This server is designed for educational purposes and testing on your own environment. Always ensure you have proper authorization before scanning any systems.

### Network Restrictions
Use the `ALLOWED_NETWORKS` environment variable to restrict which networks can be scanned:

```bash
docker run -e ALLOWED_NETWORKS="192.168.1.0/24,10.0.0.0/8" kali-security-mcp-server
```

### Input Validation
All inputs are validated and sanitized to prevent command injection:
- URLs are validated for proper format (http/https)
- IP addresses are validated
- Hostnames are validated
- Command parameters are whitelisted
- No shell execution (subprocess with list arguments only)

### Non-Root Execution
The server runs as a non-root user (UID 1000) with minimal required Linux capabilities:
- `CAP_NET_RAW`: Required for raw sockets (nmap)
- `CAP_NET_ADMIN`: Required for network administration

## Technical Details

- **Base Image**: Kali Linux Rolling
- **Language**: Python 3.11+
- **MCP SDK**: Official Anthropic MCP SDK
- **Transport**: stdio (standard input/output)
- **Security Tools**: nmap, nikto, sqlmap, wpscan, dirb, searchsploit (via exploitdb)

## Troubleshooting

### Permission Errors (Operation not permitted)

If you encounter errors like `/usr/lib/nmap/nmap: Operation not permitted` when running nmap scans, the Docker MCP Gateway container needs additional Linux capabilities.

**Solution:** Add `--cap-add NET_RAW` and `--cap-add NET_ADMIN` to your MCP client configuration (see "Configure MCP Client" section above).

**Verify the fix:**
1. Restart your MCP client (Cursor/Claude Desktop)
2. Try running an nmap scan again
3. If issues persist, verify your configuration file syntax is correct

**Alternative:** If you're running the container directly (not through MCP Gateway), use:
```bash
docker run --cap-add=NET_RAW --cap-add=NET_ADMIN kali-security-mcp-server
```

### Timeout Issues
If scans are timing out, increase the `SCAN_TIMEOUT` environment variable:

```bash
docker run -e SCAN_TIMEOUT=600 kali-security-mcp-server
```

### Output Size Limits
If output is truncated, increase the `MAX_OUTPUT_SIZE` environment variable (in bytes):

```bash
docker run -e MAX_OUTPUT_SIZE=2097152 kali-security-mcp-server
```

## License

This is an educational project. Use responsibly and only on systems you own or have explicit permission to test.

