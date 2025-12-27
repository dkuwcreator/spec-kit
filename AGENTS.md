# AGENTS.md

## About Spec Kit and Specify

**GitHub Spec Kit** is a comprehensive toolkit for implementing Spec-Driven Development (SDD) - a methodology that emphasizes creating clear specifications before implementation. The toolkit includes templates, scripts, and workflows that guide development teams through a structured approach to building software.

**Specify CLI** is the command-line interface that bootstraps projects with the Spec Kit framework. It sets up the necessary directory structures, templates, and AI agent integrations to support the Spec-Driven Development workflow.

The toolkit supports multiple AI coding assistants, allowing teams to use their preferred tools while maintaining consistent project structure and development practices.

---

## General practices

- Any changes to `__init__.py` for the Specify CLI require a version rev in `pyproject.toml` and addition of entries to `CHANGELOG.md`.

## Adding New Agent Support

This section explains how to add support for new AI agents/assistants to the Specify CLI. Use this guide as a reference when integrating new AI tools into the Spec-Driven Development workflow.

### Overview

Specify supports multiple AI agents by generating agent-specific command files and directory structures when initializing projects. Each agent has its own conventions for:

- **Command file formats** (Markdown, TOML, etc.)
- **Directory structures** (`.claude/commands/`, `.windsurf/workflows/`, etc.)
- **Command invocation patterns** (slash commands, CLI tools, etc.)
- **Argument passing conventions** (`$ARGUMENTS`, `{{args}}`, etc.)

### Current Supported Agents

| Agent                      | Directory              | Format   | CLI Tool        | Description                 |
| -------------------------- | ---------------------- | -------- | --------------- | --------------------------- |
| **Claude Code**            | `.claude/commands/`    | Markdown | `claude`        | Anthropic's Claude Code CLI |
| **Gemini CLI**             | `.gemini/commands/`    | TOML     | `gemini`        | Google's Gemini CLI         |
| **GitHub Copilot**         | `.github/agents/`      | Markdown | N/A (IDE-based) | GitHub Copilot in VS Code   |
| **Cursor**                 | `.cursor/commands/`    | Markdown | `cursor-agent`  | Cursor CLI                  |
| **Qwen Code**              | `.qwen/commands/`      | TOML     | `qwen`          | Alibaba's Qwen Code CLI     |
| **opencode**               | `.opencode/command/`   | Markdown | `opencode`      | opencode CLI                |
| **Codex CLI**              | `.codex/commands/`     | Markdown | `codex`         | Codex CLI                   |
| **Windsurf**               | `.windsurf/workflows/` | Markdown | N/A (IDE-based) | Windsurf IDE workflows      |
| **Kilo Code**              | `.kilocode/rules/`     | Markdown | N/A (IDE-based) | Kilo Code IDE               |
| **Auggie CLI**             | `.augment/rules/`      | Markdown | `auggie`        | Auggie CLI                  |
| **Roo Code**               | `.roo/rules/`          | Markdown | N/A (IDE-based) | Roo Code IDE                |
| **CodeBuddy CLI**          | `.codebuddy/commands/` | Markdown | `codebuddy`     | CodeBuddy CLI               |
| **Qoder CLI**              | `.qoder/commands/`     | Markdown | `qoder`         | Qoder CLI                   |
| **Amazon Q Developer CLI** | `.amazonq/prompts/`    | Markdown | `q`             | Amazon Q Developer CLI      |
| **Amp**                    | `.agents/commands/`    | Markdown | `amp`           | Amp CLI                     |
| **SHAI**                   | `.shai/commands/`      | Markdown | `shai`          | SHAI CLI                    |
| **IBM Bob**                | `.bob/commands/`       | Markdown | N/A (IDE-based) | IBM Bob IDE                 |

### Step-by-Step Integration Guide

Follow these steps to add a new agent (using a hypothetical new agent as an example):

#### 1. Add to AGENT_CONFIG

**IMPORTANT**: Use the actual CLI tool name as the key, not a shortened version.

Add the new agent to the `AGENT_CONFIG` dictionary in `src/specify_cli/__init__.py`. This is the **single source of truth** for all agent metadata:

```python
AGENT_CONFIG = {
    # ... existing agents ...
    "new-agent-cli": {  # Use the ACTUAL CLI tool name (what users type in terminal)
        "name": "New Agent Display Name",
        "folder": ".newagent/",  # Directory for agent files
        "install_url": "https://example.com/install",  # URL for installation docs (or None if IDE-based)
        "requires_cli": True,  # True if CLI tool required, False for IDE-based agents
    },
}
```

**Key Design Principle**: The dictionary key should match the actual executable name that users install. For example:

- ✅ Use `"cursor-agent"` because the CLI tool is literally called `cursor-agent`
- ❌ Don't use `"cursor"` as a shortcut if the tool is `cursor-agent`

This eliminates the need for special-case mappings throughout the codebase.

**Field Explanations**:

- `name`: Human-readable display name shown to users
- `folder`: Directory where agent-specific files are stored (relative to project root)
- `install_url`: Installation documentation URL (set to `None` for IDE-based agents)
- `requires_cli`: Whether the agent requires a CLI tool check during initialization

#### 2. Update CLI Help Text

Update the `--ai` parameter help text in the `init()` command to include the new agent:

```python
ai_assistant: str = typer.Option(None, "--ai", help="AI assistant to use: claude, gemini, copilot, cursor-agent, qwen, opencode, codex, windsurf, kilocode, auggie, codebuddy, new-agent-cli, or q"),
```

Also update any function docstrings, examples, and error messages that list available agents.

#### 3. Update README Documentation

Update the **Supported AI Agents** section in `README.md` to include the new agent:

- Add the new agent to the table with appropriate support level (Full/Partial)
- Include the agent's official website link
- Add any relevant notes about the agent's implementation
- Ensure the table formatting remains aligned and consistent

#### 4. Update Release Package Script

Modify `.github/workflows/scripts/create-release-packages.sh`:

##### Add to ALL_AGENTS array

```bash
ALL_AGENTS=(claude gemini copilot cursor-agent qwen opencode windsurf q)
```

##### Add case statement for directory structure

```bash
case $agent in
  # ... existing cases ...
  windsurf)
    mkdir -p "$base_dir/.windsurf/workflows"
    generate_commands windsurf md "\$ARGUMENTS" "$base_dir/.windsurf/workflows" "$script" ;;
esac
```

#### 4. Update GitHub Release Script

Modify `.github/workflows/scripts/create-github-release.sh` to include the new agent's packages:

```bash
gh release create "$VERSION" \
  # ... existing packages ...
  .genreleases/spec-kit-template-windsurf-sh-"$VERSION".zip \
  .genreleases/spec-kit-template-windsurf-ps-"$VERSION".zip \
  # Add new agent packages here
```

#### 5. Update Agent Context Scripts

##### Bash script (`scripts/bash/update-agent-context.sh`)

Add file variable:

```bash
WINDSURF_FILE="$REPO_ROOT/.windsurf/rules/specify-rules.md"
```

Add to case statement:

```bash
case "$AGENT_TYPE" in
  # ... existing cases ...
  windsurf) update_agent_file "$WINDSURF_FILE" "Windsurf" ;;
  "")
    # ... existing checks ...
    [ -f "$WINDSURF_FILE" ] && update_agent_file "$WINDSURF_FILE" "Windsurf";
    # Update default creation condition
    ;;
esac
```

##### PowerShell script (`scripts/powershell/update-agent-context.ps1`)

Add file variable:

```powershell
$windsurfFile = Join-Path $repoRoot '.windsurf/rules/specify-rules.md'
```

Add to switch statement:

```powershell
switch ($AgentType) {
    # ... existing cases ...
    'windsurf' { Update-AgentFile $windsurfFile 'Windsurf' }
    '' {
        foreach ($pair in @(
            # ... existing pairs ...
            @{file=$windsurfFile; name='Windsurf'}
        )) {
            if (Test-Path $pair.file) { Update-AgentFile $pair.file $pair.name }
        }
        # Update default creation condition
    }
}
```

#### 6. Update CLI Tool Checks (Optional)

For agents that require CLI tools, add checks in the `check()` command and agent validation:

```python
# In check() command
tracker.add("windsurf", "Windsurf IDE (optional)")
windsurf_ok = check_tool_for_tracker("windsurf", "https://windsurf.com/", tracker)

# In init validation (only if CLI tool required)
elif selected_ai == "windsurf":
    if not check_tool("windsurf", "Install from: https://windsurf.com/"):
        console.print("[red]Error:[/red] Windsurf CLI is required for Windsurf projects")
        agent_tool_missing = True
```

**Note**: CLI tool checks are now handled automatically based on the `requires_cli` field in AGENT_CONFIG. No additional code changes needed in the `check()` or `init()` commands - they automatically loop through AGENT_CONFIG and check tools as needed.

## Important Design Decisions

### Using Actual CLI Tool Names as Keys

**CRITICAL**: When adding a new agent to AGENT_CONFIG, always use the **actual executable name** as the dictionary key, not a shortened or convenient version.

**Why this matters:**

- The `check_tool()` function uses `shutil.which(tool)` to find executables in the system PATH
- If the key doesn't match the actual CLI tool name, you'll need special-case mappings throughout the codebase
- This creates unnecessary complexity and maintenance burden

**Example - The Cursor Lesson:**

❌ **Wrong approach** (requires special-case mapping):

```python
AGENT_CONFIG = {
    "cursor": {  # Shorthand that doesn't match the actual tool
        "name": "Cursor",
        # ...
    }
}

# Then you need special cases everywhere:
cli_tool = agent_key
if agent_key == "cursor":
    cli_tool = "cursor-agent"  # Map to the real tool name
```

✅ **Correct approach** (no mapping needed):

```python
AGENT_CONFIG = {
    "cursor-agent": {  # Matches the actual executable name
        "name": "Cursor",
        # ...
    }
}

# No special cases needed - just use agent_key directly!
```

**Benefits of this approach:**

- Eliminates special-case logic scattered throughout the codebase
- Makes the code more maintainable and easier to understand
- Reduces the chance of bugs when adding new agents
- Tool checking "just works" without additional mappings

#### 7. Update Devcontainer files (Optional)

For agents that have VS Code extensions or require CLI installation, update the devcontainer configuration files:

##### VS Code Extension-based Agents

For agents available as VS Code extensions, add them to `.devcontainer/devcontainer.json`:

```json
{
  "customizations": {
    "vscode": {
      "extensions": [
        // ... existing extensions ...
        // [New Agent Name]
        "[New Agent Extension ID]"
      ]
    }
  }
}
```

##### CLI-based Agents

For agents that require CLI tools, add installation commands to `.devcontainer/post-create.sh`:

```bash
#!/bin/bash

# Existing installations...

echo -e "\n🤖 Installing [New Agent Name] CLI..."
# run_command "npm install -g [agent-cli-package]@latest" # Example for node-based CLI
# or other installation instructions (must be non-interactive and compatible with Linux Debian "Trixie" or later)...
echo "✅ Done"

```

**Quick Tips:**

- **Extension-based agents**: Add to the `extensions` array in `devcontainer.json`
- **CLI-based agents**: Add installation scripts to `post-create.sh`
- **Hybrid agents**: May require both extension and CLI installation
- **Test thoroughly**: Ensure installations work in the devcontainer environment

## Agent Categories

### CLI-Based Agents

Require a command-line tool to be installed:

- **Claude Code**: `claude` CLI
- **Gemini CLI**: `gemini` CLI
- **Cursor**: `cursor-agent` CLI
- **Qwen Code**: `qwen` CLI
- **opencode**: `opencode` CLI
- **Amazon Q Developer CLI**: `q` CLI
- **CodeBuddy CLI**: `codebuddy` CLI
- **Qoder CLI**: `qoder` CLI
- **Amp**: `amp` CLI
- **SHAI**: `shai` CLI

### IDE-Based Agents

Work within integrated development environments:

- **GitHub Copilot**: Built into VS Code/compatible editors
- **Windsurf**: Built into Windsurf IDE
- **IBM Bob**: Built into IBM Bob IDE

## Command File Formats

### Markdown Format

Used by: Claude, Cursor, opencode, Windsurf, Amazon Q Developer, Amp, SHAI, IBM Bob

**Standard format:**

```markdown
---
description: "Command description"
---

Command content with {SCRIPT} and $ARGUMENTS placeholders.
```

**GitHub Copilot Chat Mode format:**

```markdown
---
description: "Command description"
mode: speckit.command-name
---

Command content with {SCRIPT} and $ARGUMENTS placeholders.
```

### TOML Format

Used by: Gemini, Qwen

```toml
description = "Command description"

prompt = """
Command content with {SCRIPT} and {{args}} placeholders.
"""
```

## Directory Conventions

- **CLI agents**: Usually `.<agent-name>/commands/`
- **IDE agents**: Follow IDE-specific patterns:
  - Copilot: `.github/agents/`
  - Cursor: `.cursor/commands/`
  - Windsurf: `.windsurf/workflows/`

## Argument Patterns

Different agents use different argument placeholders:

- **Markdown/prompt-based**: `$ARGUMENTS`
- **TOML-based**: `{{args}}`
- **Script placeholders**: `{SCRIPT}` (replaced with actual script path)
- **Agent placeholders**: `__AGENT__` (replaced with agent name)

## Testing New Agent Integration

1. **Build test**: Run package creation script locally
2. **CLI test**: Test `specify init --ai <agent>` command
3. **File generation**: Verify correct directory structure and files
4. **Command validation**: Ensure generated commands work with the agent
5. **Context update**: Test agent context update scripts

## Common Pitfalls

1. **Using shorthand keys instead of actual CLI tool names**: Always use the actual executable name as the AGENT_CONFIG key (e.g., `"cursor-agent"` not `"cursor"`). This prevents the need for special-case mappings throughout the codebase.
2. **Forgetting update scripts**: Both bash and PowerShell scripts must be updated when adding new agents.
3. **Incorrect `requires_cli` value**: Set to `True` only for agents that actually have CLI tools to check; set to `False` for IDE-based agents.
4. **Wrong argument format**: Use correct placeholder format for each agent type (`$ARGUMENTS` for Markdown, `{{args}}` for TOML).
5. **Directory naming**: Follow agent-specific conventions exactly (check existing agents for patterns).
6. **Help text inconsistency**: Update all user-facing text consistently (help strings, docstrings, README, error messages).

## Future Considerations

When adding new agents:

- Consider the agent's native command/workflow patterns
- Ensure compatibility with the Spec-Driven Development process
- Document any special requirements or limitations
- Update this guide with lessons learned
- Verify the actual CLI tool name before adding to AGENT_CONFIG

## Semantic Architecture Agent Usage

Spec Kit includes specialized commands for analyzing and enforcing [Semantic Architecture](https://github.com/dkuwcreator/Semantic-Architecture) principles. These commands help maintain codebases optimized for human-AI collaboration.

### Available Commands

- **`/speckit.semantic-audit`**: Comprehensive codebase compliance analysis
- **`/speckit.semantic-validate`**: Deep validation of specific semantic modules
- **`/speckit.semantic-restructure`**: Interactive restructuring and documentation generation

### When to Use Semantic Architecture Commands

#### During Project Bootstrap

When starting a new project or adopting Semantic Architecture:

1. **Run initial audit**:
   ```bash
   /speckit.semantic-audit
   ```
   - Understand current compliance state
   - Identify which directories could be semantic modules
   - Get prioritized action plan

2. **Generate module documentation** (for each identified module):
   ```bash
   /speckit.semantic-restructure src/[module-name]/
   ```
   - Creates README.md template based on code analysis
   - Creates AGENT_INSTRUCTION.md template with inferred boundaries
   - Provides customization guidance

3. **Validate generated docs**:
   ```bash
   /speckit.semantic-validate src/[module-name]/
   ```
   - Checks documentation completeness
   - Verifies meaning parity
   - Identifies remaining gaps

#### During Feature Development

Integrate with standard Spec-Driven Development workflow:

**Before Planning** (`/speckit.plan`):
- Use `/speckit.semantic-validate [affected-modules]` to ensure clean baseline
- Check existing module documentation for guidance

**During Specification** (`/speckit.specify`):
- Declare semantic scope (modules in/out of scope)
- Document cross-module impacts
- Use audit findings to inform scope boundaries

**During Planning** (`/speckit.plan`):
- Map planned changes to semantic modules
- Identify meaning parity update requirements
- Plan documentation updates alongside code changes

**After Implementation**:
- Update module README.md and AGENT_INSTRUCTION.md (meaning parity)
- Re-validate affected modules: `/speckit.semantic-validate [modules]`
- Run `/speckit.semantic-audit` if multiple modules changed

#### Regular Maintenance

**Quarterly Audits**:
```bash
/speckit.semantic-audit
```
- Detect semantic drift that accumulated over time
- Identify new documentation gaps
- Monitor compliance trends
- Prioritize documentation debt

**Before Major Releases**:
```bash
# Validate critical modules
/speckit.semantic-validate src/auth/ src/api/ src/core/

# Full audit
/speckit.semantic-audit
```
- Ensure documentation is current
- Fix semantic drift before release
- Verify module boundaries are respected

#### Refactoring and Restructuring

When improving codebase architecture:

1. **Identify coupling issues**:
   ```bash
   /speckit.semantic-audit
   ```
   - Boundary violations report
   - Tight coupling detection
   - Suggested module clusters

2. **Plan refactoring**:
   ```bash
   /speckit.semantic-restructure --refactor-boundaries src/module-a/ src/module-b/
   ```
   - Boundary improvement suggestions
   - Interface refactoring proposals
   - Migration checklist

3. **Extract new modules**:
   ```bash
   /speckit.semantic-restructure --extract [functionality] from src/[old-module]/
   ```
   - Module extraction plan
   - Documentation templates for new module
   - Migration guidance

### Best Practices

#### For AI Agents Working with Semantic Modules

1. **Always check module documentation first**:
   - Read README.md for purpose, responsibilities, invariants
   - Read AGENT_INSTRUCTION.md for boundaries and constraints
   - Respect documented limitations

2. **Validate before making changes**:
   ```bash
   /speckit.semantic-validate [target-module]
   ```
   - Understand current state
   - Identify existing issues
   - Plan changes that improve compliance

3. **Maintain meaning parity**:
   - Update README.md when behavior changes
   - Update AGENT_INSTRUCTION.md when boundaries change
   - Document new APIs, dependencies, invariants
   - Same commit/PR for code + docs

4. **Respect bounded contexts**:
   - Changes should stay within declared module boundaries
   - Cross-module changes require explicit justification
   - Use public APIs only (no internal imports)
   - Document new cross-module dependencies

5. **Escalate when uncertain**:
   - If change affects multiple modules → ask for approval
   - If boundary becomes unclear → request restructuring
   - If invariant might be violated → verify with human

#### For Human Developers

1. **Use audit for prioritization**:
   - Start with CRITICAL severity items
   - Address HIGH severity semantic drift
   - Plan MEDIUM/LOW items for later

2. **Generate templates, don't start from scratch**:
   - Use `/speckit.semantic-restructure` to generate docs
   - Customize based on actual code behavior
   - Don't hallucinate - base on real code

3. **Validate regularly, not just at the end**:
   - Validate modules after significant changes
   - Run audits after merging multiple features
   - Include validation in CI/CD pipeline (future)

4. **Document restructuring decisions**:
   - Use `/speckit.semantic-restructure` to plan before executing
   - Generate migration checklists
   - Update all affected module documentation

### Integration with Constitution

If your project has a constitution (`/memory/constitution.md`) with Semantic Architecture principles:

1. **Audit respects constitution rules**:
   - Uses constitution's Semantic Architecture section as authority
   - Reports violations of constitution-defined rules
   - Flags missing required sections

2. **Commands reference constitution**:
   - Validation checks against constitution requirements
   - Restructuring suggestions align with constitution principles
   - Generated documentation follows constitution patterns

3. **Update constitution when needed**:
   - If project-specific rules emerge, add to constitution
   - Use constitution to define organization-wide module standards
   - Constitution changes should trigger re-audit

### Common Pitfalls to Avoid

1. **Don't generate docs without analyzing code**:
   - ❌ Wrong: Generic templates not based on actual code
   - ✅ Right: Use `/speckit.semantic-restructure` to infer from code

2. **Don't skip validation after changes**:
   - ❌ Wrong: Assume docs are still accurate after code changes
   - ✅ Right: Re-validate modules after implementation

3. **Don't ignore semantic drift warnings**:
   - ❌ Wrong: Defer fixing drift indefinitely
   - ✅ Right: Fix CRITICAL/HIGH drift before merging

4. **Don't bypass module boundaries**:
   - ❌ Wrong: Import from `module/internal/` for convenience
   - ✅ Right: Use public API, or request boundary expansion

5. **Don't create modules for everything**:
   - ❌ Wrong: Single-file "modules" with no clear bounded context
   - ✅ Right: Modules have cohesive responsibilities and clear boundaries

### Example Workflows

#### Workflow 1: Documenting Existing Codebase

```bash
# Step 1: Understand current state
/speckit.semantic-audit

# Step 2: Generate docs for priority module
/speckit.semantic-restructure src/auth/

# Step 3: Review and customize generated templates
# (human edits README.md and AGENT_INSTRUCTION.md)

# Step 4: Validate documentation
/speckit.semantic-validate src/auth/

# Step 5: Fix any issues identified
# (update docs or code to achieve meaning parity)

# Step 6: Repeat for other modules
```

#### Workflow 2: Feature Development with Semantic Scope

```bash
# Step 1: Validate baseline
/speckit.semantic-validate src/auth/

# Step 2: Create spec with semantic scope
/speckit.specify Add OAuth2 support to authentication module

# Step 3: Plan with module awareness
/speckit.plan Use passport.js for OAuth2, maintain backward compatibility

# Step 4: Generate tasks (includes doc updates)
/speckit.tasks

# Step 5: Implement (code + docs in same commit)
/speckit.implement

# Step 6: Validate after changes
/speckit.semantic-validate src/auth/
```

#### Workflow 3: Quarterly Maintenance Audit

```bash
# Step 1: Full audit
/speckit.semantic-audit

# Step 2: Review findings, prioritize
# Focus on CRITICAL and HIGH severity items

# Step 3: Fix semantic drift
# For each drifted module:
/speckit.semantic-validate src/[module]/
# Then fix identified issues

# Step 4: Generate missing docs
# For undocumented modules:
/speckit.semantic-restructure src/[module]/

# Step 5: Re-audit to verify
/speckit.semantic-audit
```

---

*This documentation should be updated whenever new agents are added to maintain accuracy and completeness.*
