# Dice Roller MCP Server

A simple, clean MCP (Model Context Protocol) server for dice rolling operations. Perfect for coin flips, D&D gameplay, and general dice rolling mechanics.

## Features

- **General Dice Rolling**: Roll any combination of dice using standard notation (e.g., `2d6`, `1d20+5`, `3d8-2`)
- **Coin Flips**: Flip one or multiple coins
- **D&D Character Stats**: Generate ability scores using the standard 4d6 drop lowest method
- **D&D Ability Checks**: Roll d20 ability checks, saving throws, or attack rolls with modifiers

## Tools

### `roll_dice`
Roll dice using standard notation.

**Parameters:**
- `notation` (string, required): Dice notation in format `XdY+Z`
  - Examples: `"2d6"`, `"1d20+5"`, `"3d8-2"`, `"4d10"`

**Example:**
```
roll_dice(notation="2d6+3")
```

### `flip_coin`
Flip a coin one or more times.

**Parameters:**
- `count` (integer, optional): Number of coin flips (default: 1, max: 100)

**Example:**
```
flip_coin(count=5)
```

### `roll_dnd_stats`
Generate D&D character ability scores.

**Parameters:**
- `method` (string, optional): Generation method - `"4d6"` (default) or `"point_buy"` (currently uses 4d6)

**Example:**
```
roll_dnd_stats(method="4d6")
```

### `roll_dnd_ability`
Roll a D&D ability check, saving throw, or attack roll.

**Parameters:**
- `ability` (string, required): Ability name - `"str"`, `"dex"`, `"con"`, `"int"`, `"wis"`, `"cha"`, or `"attack"`
- `modifier` (integer, optional): Modifier to add to the roll (default: 0)

**Example:**
```
roll_dnd_ability(ability="dex", modifier=3)
```

## Building and Running

### Prerequisites
- Docker Desktop installed
- Docker MCP Toolkit enabled in Docker Desktop beta features

### Build the Docker Image

```bash
cd DiceRoller
docker build -t dice-mcp-server .
```

### Verify the Image

```bash
docker images | grep dice-mcp-server
```

## Integration with Docker MCP Gateway

### 1. Create Custom Catalog (Optional)

Create a catalog file at `~/.docker/mcp/catalogs/my-custom-catalog.yaml`:

```yaml
servers:
  dice:
    ref: dice-mcp-server:latest
    description: Simple dice roller for coin flips, D&D dice, and general rolling
    tools:
      - name: roll_dice
        description: Roll dice using standard notation (e.g., '2d6', '1d20+5')
      - name: flip_coin
        description: Flip a coin one or more times
      - name: roll_dnd_stats
        description: Generate D&D character ability scores using 4d6 drop lowest
      - name: roll_dnd_ability
        description: Roll a D&D ability check, saving throw, or attack roll
```

### 2. Update Registry

Edit `~/.docker/mcp/registry.yaml` and add:

```yaml
  dice:
    ref: dice-mcp-server:latest
```

### 3. Configure MCP Client

Update your MCP client configuration (e.g., Claude Desktop, Cursor) to use the Docker MCP Gateway with your custom catalog.

For Claude Desktop, edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

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
        "/home/.docker/mcp/registry.yaml"
      ]
    }
  }
}
```

Replace `YOUR_USERNAME` with your actual username.

## Usage Examples

Once connected to an MCP client, you can use natural language:

- "Roll 2d6 for me"
- "Flip a coin"
- "Generate D&D character stats"
- "Roll a dexterity check with +3 modifier"
- "Roll 1d20+5 for an attack"

## Technical Details

- **Language**: Python 3.11+
- **MCP SDK**: Official Anthropic MCP SDK
- **Transport**: stdio (standard input/output)
- **Dependencies**: Minimal - just the MCP SDK

## License

This is a simple example project. Use freely for learning and development.

