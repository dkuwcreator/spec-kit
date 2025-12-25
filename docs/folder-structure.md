# Semantic Architecture: Artifact Spaces in Spec Kit

This guide explains how Semantic Architecture principles map to folder structure in Spec Kit projects.

## Critical Distinction: Principles vs. Implementation

**Semantic Architecture defines principles, not folder structures.**

- ✅ **Principles**: Artifact spaces, bounded contexts, co-located meaning, agent scope discipline
- ❌ **NOT prescribed**: Folder names like `src/`, `tests/`, `backend/`, etc.

**Important**: Structures like `src/` and `tests/` are **examples** that commonly emerge when organizing code according to Semantic Architecture principles. They are **outcomes**, not requirements. Your project defines its own structure in plan.md based on its specific needs.

## The Core Mental Model: Three Artifact Spaces

Semantic Architecture organizes development around **three artifact spaces**, regardless of tooling:

1. **Design Space** - Requirements and specifications (immutable during implementation)
2. **Build Space** - Application code and tests (where implementation happens)
3. **Module Space** - Code co-located with documentation (prevents semantic drift)

This is a **tool-agnostic** mental model. Spec Kit is one concrete implementation that maps these spaces to specific folders.

**Reference**: [Semantic Architecture Repository](https://github.com/dkuwcreator/Semantic-Architecture)

## How Spec Kit Maps the Spaces

### Design Space → `FEATURE_DIR` (typically `specs/###-feature-name/`)

**What it contains**: Requirements, specifications, contracts, research

```text
specs/###-feature-name/          # Design Space in Spec Kit
├── spec.md                      # What to build (functional requirements)
├── plan.md                      # How to build (architecture, tech stack)
├── tasks.md                     # Step-by-step breakdown
├── research.md                  # Technical decisions and alternatives
├── data-model.md                # Entity definitions
├── semantic-map.md              # Module topology (NEW - see plan template)
├── contracts/                   # API specifications (OpenAPI, GraphQL)
└── checklists/                  # Quality verification
```

**Purpose**: Describes WHAT to build and WHY

**Rule**: **Read-Only during implementation** (except tasks.md to mark complete)

**Created by**: `/speckit.specify`, `/speckit.plan`, `/speckit.tasks`, `/speckit.checklist`

**Used by**: Implementation agents read these to understand requirements

### Build Space → Repository/Application Root

**What it contains**: The actual product being built

**Example organization** (NOT prescribed - your plan.md defines the actual structure):

```text
Repository Root/                 # Build Space in Spec Kit
├── [your code organization]    # Examples below show common patterns
│   ├── [modules/]              # Your semantic modules
│   ├── [components/]           # Your application structure
│   └── ...
├── [your test organization]    # Where you organize tests
│   └── ...
├── docs/                       # User documentation
└── config/                     # Configuration files
```

**Common patterns that emerge** (examples only):
- Code folders: `src/`, `lib/`, `app/`, `backend/`, `frontend/`, `api/`
- Test folders: `tests/`, `test/`, `spec/`, `__tests__/`
- Platform-specific: `ios/`, `android/`, `web/`, `mobile/`

**Purpose**: Implementation target - where ALL code changes happen

**Rule**: **Mutable** - this is where implementation tasks create/modify files

**Structure**: Defined in plan.md based on your project's specific needs and technology choices

### Module Space → Co-located within Build Space

**What it contains**: Module code + documentation together

**Example** (folder names will match your project's structure from plan.md):

```text
<your-module-location>/          # Module Space (within Build Space)
├── README.md                    # Human intent: what/why, responsibilities, invariants
├── AGENT_INSTRUCTION.md         # AI guidance: boundaries, allowed edits, testing
├── <module_code>.*              # Module implementation
└── ...
```

**Purpose**: Prevents semantic drift by keeping code and meaning together

**Rule**: **Documentation MUST be updated when module behavior changes** (same commit)

**Examples** (showing different project structures - yours will match plan.md):
- Module in flat structure: `auth/` with README.md + AGENT_INSTRUCTION.md + code
- Module in layered structure: `backend/api/` with README.md + AGENT_INSTRUCTION.md + code
- Module in platform structure: `ios/UserProfile/` with README.md + AGENT_INSTRUCTION.md + code

**Note**: The folder names (`src/`, `backend/`, `ios/`, etc.) are project-specific choices, not Semantic Architecture requirements.

## Tool-Agnostic Principles (Not Spec Kit Specific)

These principles apply regardless of what tool you use:

1. **Design Space is immutable during implementation**
   - Prevents scope creep
   - Maintains requirement stability
   - Spec Kit: `specs/` folder

2. **Build Space is where implementation happens**
   - All code changes target Build Space
   - Never implement in Design Space
   - Spec Kit: Repository root

3. **Module Space co-locates code and meaning**
   - README.md explains human intent
   - AGENT_INSTRUCTION.md guides AI agents
   - Both live WITH the code they describe
   - Spec Kit: Modules in Build Space (structure from plan.md)
   - **Note**: Semantic Architecture prescribes co-location, not specific folder names

4. **Agents operate within bounded context**
   - Local Module Agent: single module only
   - Cluster Agent: multiple related modules
   - System Agent: cross-cutting changes
   - Escalation required when expanding scope

## Spec Kit-Specific Implementation Details

```text
specs/
└── ###-feature-name/          # Each feature gets its own folder
    ├── spec.md                # Feature specification (what/why)
    ├── plan.md                # Implementation plan (how)
    ├── tasks.md               # Task breakdown (step-by-step)
    ├── research.md            # Technical research and decisions
    ├── data-model.md          # Entity and relationship definitions
    ├── quickstart.md          # Usage scenarios and testing guide
    ├── contracts/             # API specifications (OpenAPI, GraphQL, etc.)
    └── checklists/            # Quality verification checklists
```

**Purpose**: Design artifacts that describe WHAT to build and HOW to build it.

**Usage**:
- Created by `/speckit.specify`, `/speckit.plan`, `/speckit.tasks`, `/speckit.checklist` commands
- READ by implementation agents to understand what to build
- NOT modified during implementation (except tasks.md to mark tasks complete with `[x]`)
- Lives alongside the application code but is NOT part of the application itself

### Application Code (Implementation Target)

```text
Repository Root/
├── src/                       # Application source code
│   ├── models/               # Data models
│   ├── services/             # Business logic
│   ├── api/                  # API endpoints
│   ├── cli/                  # Command-line interface
│   └── lib/                  # Shared utilities
├── tests/                    # Test suites
│   ├── unit/                # Unit tests
│   ├── integration/         # Integration tests
│   └── contract/            # Contract tests
├── docs/                     # User documentation
├── config/                   # Configuration files
└── [other app folders]      # Project-specific structure
```

**Purpose**: The actual application being built.

**Usage**:
- This is where ALL implementation tasks create/modify files
- Structure is defined in `plan.md` based on project type (single/web/mobile)
- Paths in `tasks.md` reference these locations (e.g., `src/models/user.py`)
- This is the deliverable product, not the design documents

### Alternative Application Structures

Depending on project type (from `plan.md`):

#### Web Application

```text
Repository Root/
├── backend/
│   ├── src/
│   │   ├── models/
│   │   ├── services/
│   │   └── api/
│   └── tests/
└── frontend/
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   └── services/
    └── tests/
```

#### Mobile + API

```text
Repository Root/
├── api/
│   └── [backend structure]
├── ios/
│   └── [iOS project structure]
└── android/
    └── [Android project structure]
```

### Spec Kit Infrastructure (Do Not Modify)

```text
Repository Root/
├── .github/                  # GitHub workflows and actions
│   ├── workflows/           # CI/CD pipelines
│   └── copilot-instructions.md  # GitHub Copilot configuration
├── templates/               # Spec Kit templates
│   ├── spec-template.md
│   ├── plan-template.md
│   ├── tasks-template.md
│   └── commands/           # Command definitions
├── memory/                  # Project memory and constitution
│   └── constitution.md     # Project principles and rules
├── scripts/                 # Spec Kit utility scripts
│   ├── bash/
│   └── powershell/
└── docs/                    # Spec Kit documentation
```

**Purpose**: Spec Kit framework files and configuration.

**Usage**:
- Generally READ-ONLY during feature development
- `.github/` can be modified for project-specific CI/CD needs
- `templates/` and `scripts/` should NOT be modified unless contributing to Spec Kit itself
- `memory/constitution.md` is created once and rarely modified

### Special Purpose Folders

```text
Repository Root/
├── .vscode/                 # Editor settings (VS Code)
├── .idea/                   # Editor settings (IntelliJ)
├── node_modules/            # Dependencies (Node.js)
├── venv/                    # Virtual environment (Python)
├── target/                  # Build output (Java, Rust)
├── dist/                    # Distribution build output
└── build/                   # Build artifacts
```

**Purpose**: Editor configuration, dependencies, and build artifacts.

**Usage**:
- Created automatically by tools (package managers, build systems)
- Should be in `.gitignore`
- NOT part of application source code
- NOT where application features are implemented

## Common Mistakes to Avoid

### ❌ WRONG: Implementing in specs folder

```text
# BAD - Don't do this!
specs/001-user-auth/
├── spec.md
├── plan.md
├── src/                     # ❌ WRONG LOCATION
│   └── auth.py             # ❌ Application code in specs folder
└── tests/                   # ❌ WRONG LOCATION
    └── test_auth.py        # ❌ Tests in specs folder
```

**Problem**: Application code belongs at repository root, not in specs folder.

### ✅ CORRECT: Implementing at repository root

```text
# GOOD - Correct structure
specs/001-user-auth/
├── spec.md                  # ✅ Design document
├── plan.md                  # ✅ Design document
└── tasks.md                 # ✅ Design document

src/                         # ✅ At repository root
└── auth.py                 # ✅ Application code at correct location

tests/                       # ✅ At repository root
└── test_auth.py            # ✅ Tests at correct location
```

**Solution**: Design documents in specs/, application code at repository root.

### ❌ WRONG: Implementing in special folders

```text
# BAD - Don't do this!
templates/
└── my-feature-code.py      # ❌ Application code in templates folder

scripts/
└── my-app-logic.sh         # ❌ Application code in scripts folder

.github/
└── my-api.py               # ❌ Application code in .github folder
```

**Problem**: Special folders have specific purposes and are not for application features.

### ✅ CORRECT: Understanding folder purposes

```text
templates/                   # ✅ Spec Kit templates only
scripts/                     # ✅ Spec Kit utility scripts only
.github/                     # ✅ GitHub workflows and CI/CD only
memory/                      # ✅ Constitution and project memory only

src/                         # ✅ Application code here
└── my-feature-code.py      # ✅ Correct location
```

**Solution**: Use each folder for its intended purpose.

## Task Path Guidelines

When generating tasks in `tasks.md`, file paths should:

1. **Reference repository root**, not specs folder:
   - ✅ `src/models/user.py`
   - ❌ `specs/001-feature/src/models/user.py`

2. **Match structure from plan.md**:
   - If plan.md defines `backend/src/`, use `backend/src/models/user.py`
   - If plan.md defines `src/`, use `src/models/user.py`

3. **Be absolute or relative to repository root**:
   - ✅ `/home/project/src/models/user.py` (absolute)
   - ✅ `src/models/user.py` (relative to repo root)
   - ❌ `../../../src/models/user.py` (confusing relative path)

4. **Not reference special folders for app code**:
   - ❌ `specs/001-feature/src/models/user.py`
   - ❌ `templates/my-feature.py`
   - ❌ `scripts/my-app-logic.py`
   - ❌ `.github/my-api.py`

## Implementation Workflow

When implementing features with `/speckit.implement`:

1. **Read design documents** from `FEATURE_DIR` (specs/###-feature-name/)
   - Load spec.md, plan.md, tasks.md, etc.
   - Understand what to build and how to build it

2. **Change directory** to repository root (if not already there)
   - All implementation happens from repository root context
   - Paths in tasks are relative to repository root

3. **Create/modify application files** at repository root
   - Follow structure defined in plan.md
   - Create files in src/, tests/, etc.
   - NOT in specs/ folder

4. **Update tasks.md** to mark tasks complete
   - Change `- [ ]` to `- [x]` for completed tasks
   - This is the ONLY file in specs/ modified during implementation

## Semantic Architecture Integration

When using Semantic Architecture principles:

1. **Module documentation** (README.md, AGENT_INSTRUCTION.md) lives WITH the module:
   - ✅ `src/auth/README.md` (next to auth module code)
   - ✅ `backend/src/api/README.md` (next to api module code)
   - ❌ `specs/001-feature/auth/README.md` (wrong location)

2. **Design documents** describe modules but don't contain them:
   - ✅ `specs/001-feature/plan.md` references `src/auth/` module
   - ✅ `specs/001-feature/spec.md` declares semantic scope for `src/auth/`
   - ❌ Module implementation does NOT live in specs/

3. **Meaning parity** updates happen at module location:
   - Task: "Update src/auth/README.md to reflect OAuth2 support"
   - ✅ Modifies `src/auth/README.md` at repository root
   - ❌ Does NOT create `specs/001-feature/src/auth/README.md`

## Quick Reference

| Type | Location | Purpose | Modified During Implementation? |
|------|----------|---------|--------------------------------|
| Design docs | `specs/###-feature/` | What/how to build | Only tasks.md (mark complete) |
| Application code | `src/`, `tests/` at repo root | The actual product | ✅ Yes - this is where you implement |
| Spec Kit templates | `templates/` | Framework templates | ❌ No - read-only |
| Spec Kit scripts | `scripts/` | Utility scripts | ❌ No - read-only |
| Constitution | `memory/` | Project principles | ❌ No - rarely modified |
| GitHub config | `.github/` | CI/CD workflows | Sometimes (for project needs) |
| Editor config | `.vscode/`, `.idea/` | Editor settings | Sometimes (for project needs) |

## Summary

**Golden Rule**: Design documents describe what to build (specs/), application code IS what you build (repository root).

**Remember**:
- specs/ = Design documents (read to understand, not implementation target)
- Repository root (src/, tests/, etc.) = Implementation target (where code goes)
- Special folders (.github/, templates/, scripts/, memory/) = Infrastructure (not for app features)

When in doubt, ask:
1. "Is this a design document or application code?"
2. "Where does plan.md say the application structure lives?"
3. "Am I implementing an app feature or modifying Spec Kit itself?"

If you're implementing an app feature, it goes at repository root, NOT in specs/ or other special folders.
