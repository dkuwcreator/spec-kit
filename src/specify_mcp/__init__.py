#!/usr/bin/env python3
"""
Specify MCP Server - MCP wrapper for Spec Kit functionality

This MCP server exposes core Spec Kit capabilities as standardized MCP tools,
allowing any MCP-compatible client to leverage Spec Kit's template rendering,
validation, and artifact generation capabilities.

Usage:
    specify-mcp

The server exposes the following tools:
- speckit_list_templates: List available template IDs and versions
- speckit_render_template: Render templates with variables
- speckit_validate_artifacts: Cross-artifact consistency validation
- speckit_generate_checklist: Generate tailored checklists
"""

import sys
import json
import asyncio
from pathlib import Path
from typing import Any, Optional
from datetime import datetime

try:
    from mcp.server import Server, NotificationOptions
    from mcp.server.models import InitializationOptions
    import mcp.server.stdio
    import mcp.types as types
except ImportError:
    print("Error: MCP package not found. Install with: pip install 'specify-cli[mcp]'", file=sys.stderr)
    sys.exit(1)

# Initialize the MCP server
server = Server("specify-mcp")

# Template registry mapping template IDs to their file paths
TEMPLATES = {
    "spec": "templates/spec-template.md",
    "plan": "templates/plan-template.md",
    "tasks": "templates/tasks-template.md",
    "checklist": "templates/checklist-template.md",
    "constitution": "memory/constitution.md",
}

# Command templates for slash commands
COMMAND_TEMPLATES = {
    "specify": "templates/commands/specify.md",
    "plan": "templates/commands/plan.md",
    "tasks": "templates/commands/tasks.md",
    "implement": "templates/commands/implement.md",
    "clarify": "templates/commands/clarify.md",
    "analyze": "templates/commands/analyze.md",
    "checklist": "templates/commands/checklist.md",
    "constitution": "templates/commands/constitution.md",
    "taskstoissues": "templates/commands/taskstoissues.md",
}

def get_template_root() -> Path:
    """Get the root directory of templates (tries multiple possible locations)."""
    # Try current working directory first (for development/debugging)
    cwd_templates = Path.cwd() / "templates"
    if cwd_templates.exists():
        return Path.cwd()
    
    # Try relative to this file (installed package)
    pkg_templates = Path(__file__).parent.parent.parent / "templates"
    if pkg_templates.exists():
        return Path(__file__).parent.parent.parent
    
    # Default to current directory
    return Path.cwd()

def read_template(template_path: str) -> str:
    """Read a template file from the templates directory."""
    root = get_template_root()
    full_path = root / template_path
    
    if not full_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")
    
    return full_path.read_text(encoding="utf-8")

def render_template(template_content: str, variables: dict[str, str]) -> str:
    """
    Render a template with the provided variables.
    
    Simple string replacement for placeholders like [VARIABLE_NAME].
    """
    result = template_content
    for key, value in variables.items():
        placeholder = f"[{key}]"
        result = result.replace(placeholder, value)
    return result

def validate_spec_plan_consistency(spec_content: str, plan_content: str) -> list[str]:
    """
    Validate consistency between spec and plan artifacts.
    
    Returns a list of findings (empty if consistent).
    """
    findings = []
    
    # Check if both documents exist and have content
    if not spec_content.strip():
        findings.append("Spec document is empty")
    if not plan_content.strip():
        findings.append("Plan document is empty")
    
    # Basic checks for required sections
    spec_sections = ["## User Stories", "## Functional Requirements", "## Non-Functional Requirements"]
    for section in spec_sections:
        if section not in spec_content:
            findings.append(f"Spec missing section: {section}")
    
    plan_sections = ["## Technical Approach", "## Implementation Details"]
    for section in plan_sections:
        if section not in plan_content:
            findings.append(f"Plan missing section: {section}")
    
    return findings

def validate_plan_tasks_consistency(plan_content: str, tasks_content: str) -> list[str]:
    """
    Validate consistency between plan and tasks artifacts.
    
    Returns a list of findings (empty if consistent).
    """
    findings = []
    
    if not plan_content.strip():
        findings.append("Plan document is empty")
    if not tasks_content.strip():
        findings.append("Tasks document is empty")
    
    # Check for task breakdown structure
    if "## Task Breakdown" not in tasks_content and "## Tasks" not in tasks_content:
        findings.append("Tasks document missing task breakdown section")
    
    return findings

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List all available MCP tools for Spec Kit."""
    return [
        types.Tool(
            name="speckit_list_templates",
            description="List all available Spec Kit templates with their IDs and descriptions",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="speckit_render_template",
            description="Render a Spec Kit template with provided variables. Returns the rendered template content.",
            inputSchema={
                "type": "object",
                "properties": {
                    "template_id": {
                        "type": "string",
                        "description": "Template ID (e.g., 'spec', 'plan', 'tasks', 'checklist', 'constitution')",
                        "enum": list(TEMPLATES.keys()),
                    },
                    "variables": {
                        "type": "object",
                        "description": "Variables to substitute in the template (e.g., {'PROJECT_NAME': 'MyApp', 'FEATURE_NAME': 'user-auth'})",
                        "additionalProperties": {"type": "string"},
                    },
                },
                "required": ["template_id"],
            },
        ),
        types.Tool(
            name="speckit_validate_artifacts",
            description="Validate consistency between Spec Kit artifacts (spec, plan, tasks). Returns structured findings about missing sections, contradictions, or inconsistencies.",
            inputSchema={
                "type": "object",
                "properties": {
                    "spec_content": {
                        "type": "string",
                        "description": "Content of the spec.md file",
                    },
                    "plan_content": {
                        "type": "string",
                        "description": "Content of the plan.md file (optional)",
                    },
                    "tasks_content": {
                        "type": "string",
                        "description": "Content of the tasks.md file (optional)",
                    },
                },
                "required": ["spec_content"],
            },
        ),
        types.Tool(
            name="speckit_generate_checklist",
            description="Generate a quality checklist tailored to the project context. Returns a checklist for validating requirements completeness, clarity, and consistency.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_name": {
                        "type": "string",
                        "description": "Name of the project",
                    },
                    "tech_stack": {
                        "type": "string",
                        "description": "Technology stack being used (e.g., 'React + Node.js', '.NET + Blazor')",
                    },
                    "focus_areas": {
                        "type": "array",
                        "description": "Areas to focus on in the checklist (e.g., ['security', 'performance', 'accessibility'])",
                        "items": {"type": "string"},
                    },
                },
                "required": ["project_name"],
            },
        ),
        types.Tool(
            name="speckit_get_command_template",
            description="Get a Spec Kit slash command template for a specific command. Returns the template content for slash commands like /speckit.specify, /speckit.plan, etc.",
            inputSchema={
                "type": "object",
                "properties": {
                    "command_name": {
                        "type": "string",
                        "description": "Command name (e.g., 'specify', 'plan', 'tasks', 'implement', 'clarify', 'analyze', 'checklist', 'constitution')",
                        "enum": list(COMMAND_TEMPLATES.keys()),
                    },
                },
                "required": ["command_name"],
            },
        ),
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution requests."""
    
    if arguments is None:
        arguments = {}
    
    try:
        if name == "speckit_list_templates":
            # List all available templates
            templates_info = []
            for template_id, template_path in TEMPLATES.items():
                templates_info.append({
                    "id": template_id,
                    "path": template_path,
                    "description": f"Spec Kit {template_id.capitalize()} template",
                })
            
            result = {
                "templates": templates_info,
                "command_templates": [
                    {"id": cmd_id, "path": cmd_path}
                    for cmd_id, cmd_path in COMMAND_TEMPLATES.items()
                ],
                "version": "0.0.22",
            }
            
            return [
                types.TextContent(
                    type="text",
                    text=json.dumps(result, indent=2),
                )
            ]
        
        elif name == "speckit_render_template":
            template_id = arguments.get("template_id")
            variables = arguments.get("variables", {})
            
            if not template_id:
                raise ValueError("template_id is required")
            
            if template_id not in TEMPLATES:
                raise ValueError(f"Unknown template_id: {template_id}. Available: {list(TEMPLATES.keys())}")
            
            # Read and render template
            template_path = TEMPLATES[template_id]
            template_content = read_template(template_path)
            rendered = render_template(template_content, variables)
            
            return [
                types.TextContent(
                    type="text",
                    text=rendered,
                )
            ]
        
        elif name == "speckit_validate_artifacts":
            spec_content = arguments.get("spec_content", "")
            plan_content = arguments.get("plan_content", "")
            tasks_content = arguments.get("tasks_content", "")
            
            findings = []
            
            # Validate spec-plan consistency
            if spec_content and plan_content:
                findings.extend(validate_spec_plan_consistency(spec_content, plan_content))
            
            # Validate plan-tasks consistency
            if plan_content and tasks_content:
                findings.extend(validate_plan_tasks_consistency(plan_content, tasks_content))
            
            result = {
                "status": "valid" if not findings else "issues_found",
                "findings": findings,
                "timestamp": datetime.now().isoformat(),
            }
            
            return [
                types.TextContent(
                    type="text",
                    text=json.dumps(result, indent=2),
                )
            ]
        
        elif name == "speckit_generate_checklist":
            project_name = arguments.get("project_name", "Project")
            tech_stack = arguments.get("tech_stack", "")
            focus_areas = arguments.get("focus_areas", [])
            
            # Generate a basic checklist structure
            checklist_items = [
                "## Requirements Completeness",
                "- [ ] All user stories clearly defined",
                "- [ ] Functional requirements specified",
                "- [ ] Non-functional requirements documented",
                "- [ ] Success criteria established",
                "",
                "## Clarity & Consistency",
                "- [ ] No ambiguous language in requirements",
                "- [ ] Consistent terminology throughout",
                "- [ ] Dependencies clearly identified",
                "",
                "## Technical Alignment",
            ]
            
            if tech_stack:
                checklist_items.append(f"- [ ] {tech_stack} capabilities aligned with requirements")
            else:
                checklist_items.append("- [ ] Tech stack capabilities aligned with requirements")
            
            checklist_items.append("- [ ] Architecture supports scalability needs")
            checklist_items.append("")
            
            if focus_areas:
                checklist_items.append("## Focus Areas")
                for area in focus_areas:
                    checklist_items.append(f"- [ ] {area.capitalize()} considerations addressed")
                checklist_items.append("")
            
            checklist_items.extend([
                "## Implementation Readiness",
                "- [ ] Tasks broken down into implementable units",
                "- [ ] Dependencies between tasks identified",
                "- [ ] Resource requirements estimated",
            ])
            
            checklist = "\n".join(checklist_items)
            
            return [
                types.TextContent(
                    type="text",
                    text=f"# Quality Checklist: {project_name}\n\n{checklist}",
                )
            ]
        
        elif name == "speckit_get_command_template":
            command_name = arguments.get("command_name")
            
            if not command_name:
                raise ValueError("command_name is required")
            
            if command_name not in COMMAND_TEMPLATES:
                raise ValueError(f"Unknown command: {command_name}. Available: {list(COMMAND_TEMPLATES.keys())}")
            
            # Read command template
            template_path = COMMAND_TEMPLATES[command_name]
            template_content = read_template(template_path)
            
            return [
                types.TextContent(
                    type="text",
                    text=template_content,
                )
            ]
        
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    except Exception as e:
        return [
            types.TextContent(
                type="text",
                text=f"Error executing {name}: {str(e)}",
            )
        ]



def main():
    """Entry point for the MCP server (used by console script)."""
    asyncio.run(_run_server())

def run():
    """Alternative entry point for the MCP server."""
    main()

async def _run_server():
    """Internal async server runner."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="specify-mcp",
                server_version="0.0.22",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    main()
