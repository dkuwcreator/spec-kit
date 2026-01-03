#!/usr/bin/env python3
"""
Example MCP Client for Spec Kit

This script demonstrates how to interact with the Spec Kit MCP server
using the MCP Python SDK. It shows basic operations like listing templates,
rendering templates, and validating artifacts.

Requirements:
    pip install mcp

Usage:
    python examples/mcp_client_example.py
"""

import asyncio
import json
import sys
from pathlib import Path

try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
except ImportError:
    print("Error: MCP package not found. Install with: pip install mcp", file=sys.stderr)
    sys.exit(1)


async def list_templates(session: ClientSession):
    """List all available templates."""
    print("\n=== Listing Templates ===")
    result = await session.call_tool(
        "speckit_list_templates",
        arguments={}
    )
    
    data = json.loads(result.content[0].text)
    print(f"Spec Kit Version: {data['version']}")
    print(f"\nAvailable Templates ({len(data['templates'])}):")
    for template in data['templates']:
        print(f"  - {template['id']}: {template['description']}")
    
    print(f"\nCommand Templates ({len(data['command_templates'])}):")
    for cmd in data['command_templates']:
        print(f"  - {cmd['id']}")
    
    return data


async def render_spec_template(session: ClientSession):
    """Render a spec template with example variables."""
    print("\n=== Rendering Spec Template ===")
    result = await session.call_tool(
        "speckit_render_template",
        arguments={
            "template_id": "spec",
            "variables": {
                "PROJECT_NAME": "TaskManager",
                "FEATURE_NAME": "user-authentication"
            }
        }
    )
    
    rendered = result.content[0].text
    # Show first 500 characters
    print("Rendered template (first 500 chars):")
    print(rendered[:500] + "...")
    return rendered


async def validate_artifacts(session: ClientSession):
    """Validate artifact consistency."""
    print("\n=== Validating Artifacts ===")
    
    # Example spec content (minimal)
    spec_content = """
# Feature Specification: User Authentication

## User Stories

1. As a user, I want to log in with email and password
2. As a user, I want to reset my password if forgotten

## Functional Requirements

- FR1: System must validate email format
- FR2: System must hash passwords before storage

## Non-Functional Requirements

- NFR1: Login must complete within 2 seconds
"""
    
    # Example plan content (minimal)
    plan_content = """
# Implementation Plan: User Authentication

## Technical Approach

Using JWT tokens for session management with bcrypt for password hashing.

## Implementation Details

- Authentication service with token generation
- Password reset email service
"""
    
    result = await session.call_tool(
        "speckit_validate_artifacts",
        arguments={
            "spec_content": spec_content,
            "plan_content": plan_content,
        }
    )
    
    validation = json.loads(result.content[0].text)
    print(f"Validation Status: {validation['status']}")
    if validation['findings']:
        print("\nFindings:")
        for finding in validation['findings']:
            print(f"  - {finding}")
    else:
        print("No issues found!")
    
    return validation


async def generate_checklist(session: ClientSession):
    """Generate a quality checklist."""
    print("\n=== Generating Checklist ===")
    result = await session.call_tool(
        "speckit_generate_checklist",
        arguments={
            "project_name": "TaskManager",
            "tech_stack": "React + Node.js + PostgreSQL",
            "focus_areas": ["security", "performance", "accessibility"]
        }
    )
    
    checklist = result.content[0].text
    print(checklist)
    return checklist


async def get_command_template(session: ClientSession):
    """Get a command template."""
    print("\n=== Getting Command Template ===")
    result = await session.call_tool(
        "speckit_get_command_template",
        arguments={
            "command_name": "specify"
        }
    )
    
    template = result.content[0].text
    # Show first 300 characters
    print("Command template (first 300 chars):")
    print(template[:300] + "...")
    return template


async def main():
    """Main function to demonstrate MCP client usage."""
    print("=== Spec Kit MCP Client Example ===")
    print("Connecting to specify-mcp server...")
    
    # Configure server parameters
    server_params = StdioServerParameters(
        command="specify-mcp",
        args=[],
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the session
                await session.initialize()
                
                # List available tools
                tools = await session.list_tools()
                print(f"\nConnected! Available tools: {len(tools.tools)}")
                for tool in tools.tools:
                    print(f"  - {tool.name}: {tool.description[:80]}...")
                
                # Demonstrate each capability
                await list_templates(session)
                await render_spec_template(session)
                await validate_artifacts(session)
                await generate_checklist(session)
                await get_command_template(session)
                
                print("\n=== Example Complete ===")
                print("All MCP tools executed successfully!")
    
    except FileNotFoundError:
        print("\nError: specify-mcp command not found.", file=sys.stderr)
        print("Make sure you have installed specify-cli with MCP support:", file=sys.stderr)
        print("  pip install 'specify-cli[mcp]'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
