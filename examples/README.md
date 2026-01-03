# Spec Kit Examples

This directory contains example scripts and usage demonstrations for Spec Kit.

## MCP Client Example

The `mcp_client_example.py` script demonstrates how to interact with the Spec Kit MCP server using the MCP Python SDK.

### Prerequisites

```bash
# Install Spec Kit with MCP support
pip install 'specify-cli[mcp]'

# Or install just the MCP SDK to run the client
pip install mcp
```

### Running the Example

```bash
# From the repository root
python examples/mcp_client_example.py
```

### What the Example Does

The script demonstrates all five MCP tools:

1. **List Templates**: Shows all available Spec Kit templates
2. **Render Template**: Renders a spec template with example variables
3. **Validate Artifacts**: Validates consistency between spec and plan documents
4. **Generate Checklist**: Creates a quality checklist for a project
5. **Get Command Template**: Retrieves a slash command template

### Expected Output

```text
=== Spec Kit MCP Client Example ===
Connecting to specify-mcp server...

Connected! Available tools: 5
  - speckit_list_templates: List all available Spec Kit templates with their IDs and...
  - speckit_render_template: Render a Spec Kit template with provided variables. Ret...
  - speckit_validate_artifacts: Validate consistency between Spec Kit artifacts (spe...
  - speckit_generate_checklist: Generate a quality checklist tailored to the project...
  - speckit_get_command_template: Get a Spec Kit slash command template for a specif...

=== Listing Templates ===
Spec Kit Version: 0.0.22

Available Templates (5):
  - spec: Spec Kit Spec template
  - plan: Spec Kit Plan template
  - tasks: Spec Kit Tasks template
  - checklist: Spec Kit Checklist template
  - constitution: Spec Kit Constitution template

...
```

## Creating Your Own MCP Client

You can use the example as a starting point for your own MCP integrations:

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def my_integration():
    server_params = StdioServerParameters(
        command="specify-mcp",
        args=[],
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Your custom logic here
            result = await session.call_tool(
                "speckit_list_templates",
                arguments={}
            )
            # Process result...

asyncio.run(my_integration())
```

## Additional Resources

- [MCP Server Documentation](../docs/mcp-server.md)
- [MCP Protocol Specification](https://modelcontextprotocol.io)
- [Spec Kit README](../README.md)
