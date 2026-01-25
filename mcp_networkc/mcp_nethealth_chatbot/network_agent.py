#!/usr/bin/env python3
"""
Network Health AI Agent
An AI-powered network monitoring assistant that uses OpenAI API and MCP context
to provide intelligent, context-aware network diagnostics and recommendations.
"""

import os
import json
import asyncio
import logging
from typing import Optional, Dict, Any
from datetime import datetime

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False

import requests

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
MCP_SERVER_COMMAND = ["python", "network_monitor_server.py"]
PROMETHEUS_URL = os.getenv("PROMETHEUS_URL", "http://localhost:9090")


class NetworkAgent:
    """AI agent for network monitoring with MCP context integration."""
    
    def __init__(self, openai_api_key: Optional[str] = None, model: str = "gpt-4"):
        """Initialize the network agent."""
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI library not available. Install with: pip install openai")
        
        self.client = OpenAI(api_key=openai_api_key or OPENAI_API_KEY)
        self.model = model
        self.mcp_session: Optional[ClientSession] = None
        
    async def connect_mcp(self):
        """Connect to the MCP server."""
        if not MCP_AVAILABLE:
            logger.warning("MCP client not available, using direct API calls")
            print("⚠ MCP client library not available. Install with: pip install mcp")
            return
        
        try:
            # Get the directory where network_monitor_server.py is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            server_script = os.path.join(script_dir, "network_monitor_server.py")
            
            if not os.path.exists(server_script):
                logger.warning(f"MCP server script not found at {server_script}")
                print(f"⚠ MCP server script not found at {server_script}")
                print("⚠ Continuing without MCP connection - some features may be limited")
                return
            
            print("Connecting to MCP server...")
            server_params = StdioServerParameters(
                command="python3",
                args=[server_script],
                env=None
            )
            
            stdio_transport = await stdio_client(server_params)
            read_stream, write_stream = stdio_transport
            
            self.mcp_session = ClientSession(read_stream, write_stream)
            await self.mcp_session.initialize()
            
            logger.info("Connected to MCP server")
            print("✓ Connected to MCP server")
            
            # Test the connection
            try:
                tools = await self.mcp_session.list_tools()
                print(f"✓ MCP connection verified ({len(tools.tools)} tools available)")
            except Exception as e:
                logger.warning(f"MCP connected but tool listing failed: {e}")
                
        except Exception as e:
            logger.error(f"Failed to connect to MCP server: {str(e)}")
            print(f"⚠ Failed to connect to MCP server: {str(e)}")
            print("⚠ Continuing without MCP connection - some features may be limited")
            print("  Make sure network_monitor_server.py is in the same directory")
    
    async def close_mcp(self):
        """Close MCP session cleanly."""
        if self.mcp_session:
            try:
                await self.mcp_session.close()
                logger.info("MCP session closed")
            except Exception as e:
                logger.error(f"Error closing MCP session: {str(e)}")
    
    async def call_mcp_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call an MCP tool."""
        if not self.mcp_session:
            # Fallback: make direct HTTP calls if MCP not available
            logger.warning(f"MCP not connected, cannot call tool: {tool_name}")
            return {"error": "MCP not connected"}
        
        try:
            result = await self.mcp_session.call_tool(tool_name, arguments)
            return {"success": True, "result": result}
        except Exception as e:
            logger.error(f"Error calling MCP tool {tool_name}: {str(e)}")
            return {"error": str(e)}
    
    def retrieve_context(self, device: str = "") -> str:
        """Retrieve network context from MCP storage."""
        try:
            # For now, use direct context storage access
            # In production, this would call the MCP tool
            context_file = f"context_{device}.json" if device else "context_all.json"
            
            # Try to read from file if exists
            if os.path.exists(context_file):
                with open(context_file, 'r') as f:
                    return json.dumps(json.load(f), indent=2)
            
            return "No historical context available"
        except Exception as e:
            logger.error(f"Error retrieving context: {str(e)}")
            return f"Error retrieving context: {str(e)}"
    
    def query_prometheus(self, query: str) -> Dict[str, Any]:
        """Query Prometheus metrics."""
        try:
            api_url = f"{PROMETHEUS_URL}/api/v1/query"
            params = {"query": query}
            
            response = requests.get(api_url, params=params, timeout=5)
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            logger.error(f"Error querying Prometheus: {str(e)}")
            return {"error": str(e), "message": "Prometheus may not be running"}
    
    async def get_network_state(self, router: str = "router1") -> Dict[str, Any]:
        """Get current network state using MCP tools."""
        state = {
            "router": router,
            "timestamp": datetime.now().isoformat()
        }
        
        # Get interface status
        iface_result = await self.call_mcp_tool("check_interface_status", {"router": router})
        state["interfaces"] = iface_result
        
        # Get device info
        device_result = await self.call_mcp_tool("get_device_info", {"router": router})
        state["device_info"] = device_result
        
        # Detect issues
        issues_result = await self.call_mcp_tool("detect_issues", {"router": router})
        state["issues"] = issues_result
        
        return state
    
    async def query(self, user_query: str, router: str = "router1") -> str:
        """Process a user query and return AI-powered response."""
        logger.info(f"Processing query: {user_query}")
        
        # Retrieve historical context
        context = self.retrieve_context(router)
        
        # Get current network state
        current_state = await self.get_network_state(router)
        
        # Query Prometheus if relevant
        prometheus_data = {}
        if "latency" in user_query.lower() or "metrics" in user_query.lower():
            prometheus_data = self.query_prometheus("up")
        
        # Construct prompt with context
        system_prompt = """You are an expert network operations AI assistant specializing in network monitoring, 
diagnostics, and troubleshooting. You have access to:
1. Current network device state (interfaces, device info, issues)
2. Historical context from previous checks
3. Prometheus metrics data

Provide clear, actionable insights. Reference historical context when relevant (e.g., "Similar to yesterday's issue...").
Be specific about which interfaces or devices have problems and suggest concrete remediation steps."""
        
        user_prompt = f"""User Query: {user_query}

Current Network State:
{json.dumps(current_state, indent=2, default=str)}

Historical Context:
{context}

Prometheus Metrics:
{json.dumps(prometheus_data, indent=2) if prometheus_data else "Not available"}

Please analyze the network state and provide:
1. Current status assessment
2. Any issues detected
3. Comparison with historical context (if available)
4. Recommended actions

Be concise but thorough."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            ai_response = response.choices[0].message.content
            
            # Store new context
            await self.store_context(router, current_state, ai_response)
            
            return ai_response
        
        except Exception as e:
            logger.error(f"Error querying OpenAI: {str(e)}")
            return f"Error: {str(e)}. Make sure OPENAI_API_KEY is set correctly."
    
    async def store_context(self, device: str, state: Dict[str, Any], ai_insight: str):
        """Store network context for future reference."""
        try:
            context_entry = {
                "timestamp": datetime.now().isoformat(),
                "device": device,
                "state": state,
                "ai_insight": ai_insight
            }
            
            # Store via MCP tool
            await self.call_mcp_tool("store_network_context", {
                "device": device,
                "interfaces": state.get("interfaces", {}).get("result", []),
                "alerts": state.get("issues", {}).get("result", {}).get("issues", []),
                "metrics": {}
            })
            
            logger.info(f"Stored context for {device}")
        except Exception as e:
            logger.error(f"Error storing context: {str(e)}")


async def main():
    """Main entry point for the network agent."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Network Health AI Agent")
    parser.add_argument("--query", type=str, help="Query to ask the AI agent")
    parser.add_argument("--router", type=str, default="router1", help="Router to query")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    args = parser.parse_args()
    
    if not OPENAI_API_KEY:
        print("ERROR: OPENAI_API_KEY environment variable not set")
        print("Set it with: export OPENAI_API_KEY='your-api-key'")
        return
    
    agent = NetworkAgent()
    
    # Connect to MCP server
    await agent.connect_mcp()
    
    try:
        if args.interactive:
            print("Network Health AI Agent - Interactive Mode")
            print("Type 'exit', 'quit', or 'q' to quit\n")
            
            while True:
                try:
                    query = input("Query: ").strip()
                    if query.lower() in ['exit', 'quit', 'q']:
                        print("\nExiting...")
                        break
                    
                    if query:
                        response = await agent.query(query, args.router)
                        print(f"\nAI Response:\n{response}\n")
                except KeyboardInterrupt:
                    print("\n\nExiting...")
                    break
                except EOFError:
                    print("\n\nExiting...")
                    break
                except Exception as e:
                    print(f"Error: {str(e)}\n")
        elif args.query:
            response = await agent.query(args.query, args.router)
            print(response)
        else:
            # Demo query
            demo_query = "Check for latency issues on router1"
            print(f"Demo Query: {demo_query}\n")
            response = await agent.query(demo_query, args.router)
            print(f"AI Response:\n{response}")
    finally:
        # Clean up MCP session
        await agent.close_mcp()


if __name__ == "__main__":
    asyncio.run(main())

