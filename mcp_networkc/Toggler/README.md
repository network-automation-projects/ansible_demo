# Toggl MCP Server

An MCP (Model Context Protocol) server for Toggl time tracking operations. This server integrates with the Toggl Track API to start timers, stop timers, and view time entries.

## Features

- **Start Timer**: Create and start a new time tracking entry
- **Stop Timer**: Stop the currently running time entry
- **View Timers**: Retrieve and display existing time entries with optional date filtering

## Prerequisites

- Docker Desktop installed
- Docker MCP Toolkit enabled in Docker Desktop beta features
- Toggl API token (found in your Toggl Track profile settings)

## Getting Your Toggl API Token

1. Log in to [Toggl Track](https://track.toggl.com)
2. Go to your profile settings
3. Scroll down to find your API token
4. Copy the token (it looks like: `1971800d4d82861d8f2c1651fea4d212`)

## Building and Running

### Build the Docker Image

```bash
cd Toggler
docker build -t toggl-mcp-server .
```

### Verify the Image

```bash
docker images | grep toggl-mcp-server
```

## Configuration

The server supports two methods for providing the API token:

### Method 1: Docker Secrets (Recommended for Docker Swarm)

The server will automatically read from `/run/secrets/toggl_api_token` if available. Create the secret:

```bash
echo "your_api_token_here" | docker secret create toggl_api_token -
```

Then use the secret when creating a service:

```bash
docker service create \
  --secret toggl_api_token \
  --name toggl-mcp \
  toggl-mcp-server:latest
```

### Method 2: Environment Variable

Alternatively, you can set the `TOGGL_API_TOKEN` environment variable:

```bash
docker run -e TOGGL_API_TOKEN=your_api_token_here toggl-mcp-server
```

**Note:** The server checks Docker secrets first, then falls back to the environment variable.

## Integration with Docker MCP Gateway

### 1. Create Custom Catalog (Optional)

Create a catalog file at `~/.docker/mcp/catalogs/my-custom-catalog.yaml`:

```yaml
servers:
  toggl:
    ref: toggl-mcp-server:latest
    description: Toggl time tracking integration for starting timers, stopping timers, and viewing time entries
    tools:
      - name: start_timer
        description: Start a new time tracking entry in Toggl. Requires a workspace ID.
      - name: stop_timer
        description: Stop the currently running time entry in Toggl. Automatically finds and stops the active timer.
      - name: view_timers
        description: View existing time entries from Toggl with optional date filtering.
```

### 2. Update Registry

Edit `~/.docker/mcp/registry.yaml` and add:

```yaml
  toggl:
    ref: toggl-mcp-server:latest
```

### 3. Configure MCP Client

Update your MCP client configuration (e.g., Claude Desktop, Cursor) to use the Docker MCP Gateway with your custom catalog.

For Claude Desktop, edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

**Option A: Using Docker Secrets (Recommended)**

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
        "--secret",
        "source=toggl_api_token,target=toggl_api_token",
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

**Option B: Using Environment Variable**

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
        "--catalog",
        "docker-mcp",
        "--catalog",
        "my-custom-catalog",
        "--registry",
        "/home/.docker/mcp/registry.yaml",
        "--env",
        "TOGGL_API_TOKEN=your_api_token_here"
      ]
    }
  }
}
```

Replace `YOUR_USERNAME` with your actual username. For Option A, ensure you've created the Docker secret first (see Configuration section above).

## Tools

### `start_timer`

Start a new time tracking entry.

**Parameters:**
- `workspace_id` (integer, **required**): Toggl workspace ID
- `description` (string, optional): Description of the task being tracked
- `project_id` (integer, optional): Project ID to associate this time entry with
- `tag_ids` (array of integers, optional): List of tag IDs to apply to this time entry
- `billable` (boolean, optional): Whether this time entry is billable

**Example:**
```
start_timer(workspace_id=1234567, description="Working on MCP server", project_id=987654)
```

### `stop_timer`

Stop the currently running time entry. Automatically finds and stops the active timer.

**Parameters:** None

**Example:**
```
stop_timer()
```

### `view_timers`

View existing time entries with optional date filtering.

**Parameters:**
- `start_date` (string, optional): Filter entries from this date (YYYY-MM-DD or RFC3339 format)
- `end_date` (string, optional): Filter entries until this date (YYYY-MM-DD or RFC3339 format)
- `limit` (integer, optional): Maximum number of entries to return (default: 10, max: 100)

**Example:**
```
view_timers(start_date="2025-01-01", end_date="2025-01-31", limit=20)
```

## Usage Examples

Once connected to an MCP client, you can use natural language:

- "Start a timer for workspace 1234567 with description 'Working on project'"
- "Stop the current timer"
- "Show me my time entries from this week"
- "View my last 5 time entries"

## Finding Your Workspace ID

To find your workspace ID:

1. Log in to Toggl Track web app
2. Look at the URL when viewing your workspace: `https://track.toggl.com/workspaces/{workspace_id}/...`
3. Or use the Toggl API: `curl -u your_api_token:api_token https://api.track.toggl.com/api/v9/me/workspaces`

## Error Handling

The server handles various error scenarios:

- **Missing API Token**: Clear error message if `TOGGL_API_TOKEN` is not set
- **Authentication Errors**: 401 errors indicate invalid API token
- **Authorization Errors**: 403 errors indicate insufficient permissions
- **Rate Limiting**: 429 errors with retry-after information
- **No Running Timer**: Informative message when trying to stop a timer that isn't running

## API Rate Limits

Toggl API has rate limits based on your subscription plan:

- **Free**: 30 requests per hour, per user, per organization
- **Starter**: 240 requests per hour, per user, per organization
- **Premium**: 600 requests per hour, per user, per organization

The server will display rate limit errors if exceeded.

## Technical Details

- **Language**: Python 3.11+
- **MCP SDK**: Official Anthropic MCP SDK (>=1.0.0)
- **HTTP Client**: aiohttp (>=3.9.0) for async API calls
- **Transport**: stdio (standard input/output)
- **API Version**: Toggl Track API v9
- **Authentication**: HTTP Basic Auth with API token

## License

This is a simple example project. Use freely for learning and development.

