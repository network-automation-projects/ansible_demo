#!/usr/bin/env python3
"""
Demo Queries for Network Health Chatbot
Example queries demonstrating context-aware network monitoring capabilities.
"""

import asyncio
import os
import sys

# Add parent directory to path to import network_agent
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from network_agent import NetworkAgent

# Demo queries showcasing different capabilities
DEMO_QUERIES = [
    {
        "query": "Check the network health status",
        "description": "Basic health check query",
        "router": "router1"
    },
    {
        "query": "Are there any interfaces down?",
        "description": "Interface status check",
        "router": "router1"
    },
    {
        "query": "Check for latency issues on router1",
        "description": "Latency monitoring query",
        "router": "router1"
    },
    {
        "query": "What's the current status of router2? Compare it with previous checks.",
        "description": "Context-aware comparison query",
        "router": "router2"
    },
    {
        "query": "Diagnose any network problems and suggest fixes",
        "description": "Diagnostic query with recommendations",
        "router": "router1"
    },
    {
        "query": "Show me device information and system uptime",
        "description": "Device information query",
        "router": "router1"
    }
]


async def run_demo():
    """Run demo queries."""
    print("=" * 70)
    print("Network Health Chatbot - Demo Queries")
    print("=" * 70)
    print()
    
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY environment variable not set")
        print("Set it with: export OPENAI_API_KEY='your-api-key'")
        return
    
    agent = NetworkAgent()
    
    # Connect to MCP server
    print("Connecting to MCP server...")
    await agent.connect_mcp()
    print("Connected!\n")
    
    for i, demo in enumerate(DEMO_QUERIES, 1):
        print(f"\n{'=' * 70}")
        print(f"Demo Query {i}/{len(DEMO_QUERIES)}")
        print(f"{'=' * 70}")
        print(f"Description: {demo['description']}")
        print(f"Query: {demo['query']}")
        print(f"Router: {demo['router']}")
        print("-" * 70)
        
        try:
            response = await agent.query(demo['query'], demo['router'])
            print(f"\nAI Response:\n{response}")
        except Exception as e:
            print(f"\nError: {str(e)}")
        
        print("\n" + "=" * 70)
        
        # Small delay between queries
        if i < len(DEMO_QUERIES):
            print("\nWaiting 2 seconds before next query...\n")
            await asyncio.sleep(2)
    
    print("\n" + "=" * 70)
    print("Demo Complete!")
    print("=" * 70)


async def run_single_demo(query: str, router: str = "router1"):
    """Run a single demo query."""
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY environment variable not set")
        return
    
    agent = NetworkAgent()
    await agent.connect_mcp()
    
    print(f"Query: {query}")
    print(f"Router: {router}")
    print("-" * 70)
    
    try:
        response = await agent.query(query, router)
        print(f"\nAI Response:\n{response}")
    except Exception as e:
        print(f"\nError: {str(e)}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run demo queries for Network Health Chatbot")
    parser.add_argument("--query", type=str, help="Run a single custom query")
    parser.add_argument("--router", type=str, default="router1", help="Router to query")
    args = parser.parse_args()
    
    if args.query:
        asyncio.run(run_single_demo(args.query, args.router))
    else:
        asyncio.run(run_demo())

