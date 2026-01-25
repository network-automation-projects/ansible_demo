#!/usr/bin/env python3
"""
Dice Roller MCP Server
A simple MCP server for dice rolling operations including coin flips,
D&D dice mechanics, and general dice rolling.
"""

import re
import random
import asyncio
from typing import Any, Sequence
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


# Initialize the MCP server
server = Server("dice-roller")


def parse_dice_notation(notation: str) -> tuple[int, int, int]:
    """
    Parse dice notation like "2d6", "1d20+5", "3d8-2"
    Returns: (num_dice, sides, modifier)
    """
    # Pattern: optional number of dice, 'd', number of sides, optional +/- modifier
    pattern = r'(\d+)d(\d+)([+-]\d+)?'
    match = re.match(pattern, notation.lower().strip())
    
    if not match:
        raise ValueError(f"Invalid dice notation: {notation}. Use format like '2d6' or '1d20+5'")
    
    num_dice = int(match.group(1))
    sides = int(match.group(2))
    modifier = int(match.group(3)) if match.group(3) else 0
    
    if num_dice < 1 or num_dice > 100:
        raise ValueError(f"Number of dice must be between 1 and 100, got {num_dice}")
    if sides < 2 or sides > 1000:
        raise ValueError(f"Number of sides must be between 2 and 1000, got {sides}")
    
    return num_dice, sides, modifier


def roll_dice_notation(notation: str) -> dict[str, Any]:
    """Roll dice based on notation and return detailed results."""
    num_dice, sides, modifier = parse_dice_notation(notation)
    
    rolls = [random.randint(1, sides) for _ in range(num_dice)]
    total = sum(rolls) + modifier
    
    return {
        "notation": notation,
        "rolls": rolls,
        "modifier": modifier,
        "total": total,
        "formatted": f"{notation}: {rolls} {'+' if modifier >= 0 else ''}{modifier if modifier != 0 else ''} = {total}"
    }


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools."""
    return [
        Tool(
            name="roll_dice",
            description="Roll dice using standard notation (e.g., '2d6', '1d20+5', '3d8-2'). Supports any number of dice and sides.",
            inputSchema={
                "type": "object",
                "properties": {
                    "notation": {
                        "type": "string",
                        "description": "Dice notation in format XdY+Z (e.g., '2d6', '1d20+5', '3d8-2')"
                    }
                },
                "required": ["notation"]
            }
        ),
        Tool(
            name="flip_coin",
            description="Flip a coin one or more times. Returns Heads or Tails for each flip.",
            inputSchema={
                "type": "object",
                "properties": {
                    "count": {
                        "type": "integer",
                        "description": "Number of coin flips (default: 1)",
                        "default": 1,
                        "minimum": 1,
                        "maximum": 100
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="roll_dnd_stats",
            description="Generate D&D character ability scores using the standard 4d6 drop lowest method. Returns all six ability scores.",
            inputSchema={
                "type": "object",
                "properties": {
                    "method": {
                        "type": "string",
                        "description": "Method for generating stats: '4d6' (default, roll 4d6 drop lowest) or 'point_buy' (not implemented, uses 4d6)",
                        "enum": ["4d6", "point_buy"],
                        "default": "4d6"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="roll_dnd_ability",
            description="Roll a D&D ability check, saving throw, or attack roll using a d20 with optional modifier.",
            inputSchema={
                "type": "object",
                "properties": {
                    "ability": {
                        "type": "string",
                        "description": "Ability name (str, dex, con, int, wis, cha) or 'attack'",
                        "enum": ["str", "dex", "con", "int", "wis", "cha", "attack"]
                    },
                    "modifier": {
                        "type": "integer",
                        "description": "Modifier to add to the roll (default: 0)",
                        "default": 0
                    }
                },
                "required": ["ability"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> Sequence[TextContent]:
    """Handle tool calls."""
    
    if name == "roll_dice":
        notation = arguments.get("notation", "")
        try:
            result = roll_dice_notation(notation)
            return [TextContent(
                type="text",
                text=f"🎲 {result['formatted']}\n\nRolls: {result['rolls']}\nTotal: {result['total']}"
            )]
        except ValueError as e:
            return [TextContent(type="text", text=f"❌ Error: {str(e)}")]
    
    elif name == "flip_coin":
        count = arguments.get("count", 1)
        if count < 1 or count > 100:
            return [TextContent(type="text", text="❌ Error: Count must be between 1 and 100")]
        
        results = [random.choice(["Heads", "Tails"]) for _ in range(count)]
        if count == 1:
            return [TextContent(type="text", text=f"🪙 {results[0]}")]
        else:
            heads_count = results.count("Heads")
            tails_count = results.count("Tails")
            return [TextContent(
                type="text",
                text=f"🪙 Flipped {count} coin(s):\n{', '.join(results)}\n\nHeads: {heads_count}, Tails: {tails_count}"
            )]
    
    elif name == "roll_dnd_stats":
        method = arguments.get("method", "4d6")
        
        def roll_4d6_drop_lowest():
            """Roll 4d6 and drop the lowest die."""
            rolls = [random.randint(1, 6) for _ in range(4)]
            rolls.sort()
            return sum(rolls[1:])  # Drop the lowest (first after sorting)
        
        abilities = {
            "STR": roll_4d6_drop_lowest(),
            "DEX": roll_4d6_drop_lowest(),
            "CON": roll_4d6_drop_lowest(),
            "INT": roll_4d6_drop_lowest(),
            "WIS": roll_4d6_drop_lowest(),
            "CHA": roll_4d6_drop_lowest()
        }
        
        stats_text = "\n".join([f"{ability}: {score}" for ability, score in abilities.items()])
        total_points = sum(abilities.values())
        
        return [TextContent(
            type="text",
            text=f"🎲 D&D Character Stats (4d6 drop lowest):\n\n{stats_text}\n\nTotal Points: {total_points}"
        )]
    
    elif name == "roll_dnd_ability":
        ability = arguments.get("ability", "").lower()
        modifier = arguments.get("modifier", 0)
        
        roll = random.randint(1, 20)
        total = roll + modifier
        
        ability_names = {
            "str": "Strength",
            "dex": "Dexterity",
            "con": "Constitution",
            "int": "Intelligence",
            "wis": "Wisdom",
            "cha": "Charisma",
            "attack": "Attack"
        }
        
        ability_display = ability_names.get(ability, ability.upper())
        modifier_str = f"{'+' if modifier >= 0 else ''}{modifier}" if modifier != 0 else ""
        
        # Check for natural 20 or 1
        result_note = ""
        if roll == 20:
            result_note = " (Natural 20! 🎉)"
        elif roll == 1:
            result_note = " (Natural 1! 💀)"
        
        return [TextContent(
            type="text",
            text=f"🎲 {ability_display} {'Check' if ability != 'attack' else 'Roll'}: d20{modifier_str}\n\nRoll: {roll}{modifier_str} = {total}{result_note}"
        )]
    
    else:
        return [TextContent(type="text", text=f"❌ Unknown tool: {name}")]


async def main():
    """Run the MCP server using stdio transport."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())

