# Spec Kit MCP Server

The Spec Kit MCP (Model Context Protocol) Server provides a standardized interface to Spec Kit's core capabilities, allowing any MCP-compatible client to leverage template rendering, validation, and artifact generation features.

## Overview

The MCP server exposes Spec Kit functionality as **discoverable tools** that can be called by any MCP-compatible AI client (e.g., Claude Desktop, VS Code extensions, custom integrations). This provides:

- **Agent-agnostic integration**: One standard interface works with all MCP-compatible clients
- **Discoverability**: Clients can automatically discover available Spec Kit capabilities
- **Centralized upgrades**: Update the server once, all clients benefit
- **Side-effect free operations**: Server returns content; clients apply changes locally

## Architecture: Hybrid Approach

Spec Kit MCP Server follows a **hybrid architecture**:

- **Layer 1 - Repo-Native Kit**: The existing CLI, templates, `.specify/` structure, and scripts remain unchanged
- **Layer 2 - MCP Adapter**: The MCP server exposes reusable, tool-like pieces to MCP clients

This preserves the "repo as source of truth" model while enabling standardized tool-based access.

## Installation

### Install with MCP support

```bash
# Install with MCP dependencies
pip install 'specify-cli[mcp]'

# Or with uv
uv pip install 'specify-cli[mcp]'
```

### Verify installation

```bash
specify-mcp --help
```

## Available MCP Tools

The MCP server exposes the following tools:

### 1. `speckit_list_templates`

List all available Spec Kit templates with their IDs and descriptions.

**Parameters:** None

**Returns:** JSON object containing:
- `templates`: Array of available artifact templates
- `command_templates`: Array of slash command templates
- `version`: Spec Kit version

**Example:**
```json
{
  "templates": [
    {
      "id": "spec",
      "path": "templates/spec-template.md",
      "description": "Spec Kit Spec template"
    },
    ...
  ],
  "command_templates": [...],
  "version": "0.0.22"
}
```

### 2. `speckit_render_template`

Render a Spec Kit template with provided variables.

**Parameters:**
- `template_id` (required): Template ID - one of: `spec`, `plan`, `tasks`, `checklist`, `constitution`
- `variables` (optional): Object with variable substitutions (e.g., `{"PROJECT_NAME": "MyApp"}`)

**Returns:** Rendered template content as text

**Example:**
```json
{
  "template_id": "spec",
  "variables": {
    "PROJECT_NAME": "TaskManager",
    "FEATURE_NAME": "user-authentication"
  }
}
```

### 3. `speckit_validate_artifacts`

Validate consistency between Spec Kit artifacts (spec, plan, tasks).

**Parameters:**
- `spec_content` (required): Content of spec.md file
- `plan_content` (optional): Content of plan.md file
- `tasks_content` (optional): Content of tasks.md file

**Returns:** JSON object with:
- `status`: "valid" or "issues_found"
- `findings`: Array of validation findings
- `timestamp`: ISO 8601 timestamp

**Example:**
```json
{
  "status": "issues_found",
  "findings": [
    "Spec missing section: ## User Stories",
    "Plan missing section: ## Technical Approach"
  ],
  "timestamp": "2024-12-25T12:00:00.000000"
}
```

### 4. `speckit_generate_checklist`

Generate a quality checklist tailored to project context.

**Parameters:**
- `project_name` (required): Name of the project
- `tech_stack` (optional): Technology stack (e.g., "React + Node.js")
- `focus_areas` (optional): Array of focus areas (e.g., `["security", "performance"]`)

**Returns:** Formatted checklist as markdown text

**Example:**
```json
{
  "project_name": "TaskManager",
  "tech_stack": "React + Node.js",
  "focus_areas": ["security", "accessibility"]
}
```

### 5. `speckit_get_command_template`

Get a Spec Kit slash command template.

**Parameters:**
- `command_name` (required): Command name - one of: `specify`, `plan`, `tasks`, `implement`, `clarify`, `analyze`, `checklist`, `constitution`, `taskstoissues`

**Returns:** Command template content as text

**Example:**
```json
{
  "command_name": "specify"
}
```

## Usage with MCP Clients

### Claude Desktop

Add to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "specify-mcp": {
      "command": "specify-mcp"
    }
  }
}
```

Restart Claude Desktop. You can now use Spec Kit tools in your conversations:

```
Use the speckit_list_templates tool to show me available templates
```

### VS Code with MCP Extension

Install an MCP extension for VS Code, then configure:

```json
{
  "mcp.servers": {
    "specify-mcp": {
      "command": "specify-mcp"
    }
  }
}
```

### Custom Integration

The MCP server uses stdio for communication. Example Python client:

```python
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="specify-mcp",
        args=[],
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            print(f"Available tools: {[t.name for t in tools.tools]}")
            
            # Call a tool
            result = await session.call_tool(
                "speckit_list_templates",
                arguments={}
            )
            print(json.dumps(json.loads(result.content[0].text), indent=2))

if __name__ == "__main__":
    asyncio.run(main())
```

## Development

### Running the server directly

```bash
# From the repository root
python -m specify_mcp
```

### Testing tools

You can test individual tools using the MCP Inspector or a simple client script.

### Adding new tools

To add new MCP tools:

1. Define the tool in `handle_list_tools()` with proper schema
2. Implement the tool handler in `handle_call_tool()`
3. Update this documentation
4. Test with an MCP client

## Security Considerations

The MCP server follows these security principles:

- **Read-only by default**: Tools return content; they don't modify files
- **No file system writes**: Clients are responsible for applying changes
- **Input validation**: All tool inputs are validated before processing
- **Error handling**: Exceptions are caught and returned as error messages

For production deployments, consider:

- Running the server with restricted permissions
- Adding authentication/authorization layers
- Implementing rate limiting
- Adding audit logging
- Running in a sandboxed environment

## Comparison: CLI vs MCP Server

| Feature | CLI (`specify`) | MCP Server (`specify-mcp`) |
|---------|-----------------|----------------------------|
| **Installation** | Standalone | Requires MCP-compatible client |
| **Workflow** | Interactive commands | Tool-based API calls |
| **File operations** | Creates/modifies files | Returns content (client applies) |
| **Integration** | Direct command line | Any MCP client |
| **Use case** | Bootstrap projects | AI-assisted development |
| **State management** | Local file system | Stateless (client manages) |

## Best Practices

### When to use the MCP server

Use the MCP server when:
- Integrating Spec Kit into AI-assisted workflows
- Building custom tools that leverage Spec Kit templates
- Need standardized, discoverable access to Spec Kit capabilities
- Working with MCP-compatible AI clients

### When to use the CLI

Use the CLI when:
- Bootstrapping new projects
- Managing `.specify/` structure
- Running standalone commands
- Working without MCP clients

### Hybrid workflow

The recommended approach is **hybrid**:

1. Use `specify init` to bootstrap projects (CLI)
2. Use MCP tools for AI-assisted spec/plan/task generation
3. Use slash commands for guided workflows
4. Use validation tools to ensure consistency

## Troubleshooting

### Server not starting

```bash
# Check if MCP dependencies are installed
pip show mcp

# Install if missing
pip install 'specify-cli[mcp]'
```

### Tools not discovered

Ensure your MCP client is configured correctly and has restarted after configuration changes.

### Template not found errors

The server looks for templates in these locations (in order):
1. Current working directory (`./templates/`)
2. Package installation directory
3. Falls back to current directory

Make sure the server is run from a directory with access to templates, or templates are installed with the package.

## Roadmap

Future enhancements planned for the MCP server:

- **Advanced validation**: Deeper cross-artifact consistency checks
- **Upgrade assistance**: Tools to diff and upgrade `.specify/` structures
- **Repository analysis**: Tools to analyze existing codebases
- **Template customization**: Dynamic template generation based on project context
- **Metrics & reporting**: Generate reports on spec quality and completeness

## Contributing

Contributions to the MCP server are welcome! See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## License

The Spec Kit MCP Server is part of Spec Kit and is licensed under the MIT License. See [LICENSE](../LICENSE) for details.
