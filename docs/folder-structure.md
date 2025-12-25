# Spec Kit Folder Structure Guide

This document clarifies the purpose of each folder in a Spec Kit project and where different types of files belong.

## Critical Distinction

**Spec Kit maintains TWO separate hierarchies:**

1. **Design Documents** (`specs/` folder) - Specifications for what to build
2. **Application Code** (repository root) - Implementation of the application

**NEVER implement application features in the specs folder or other special-purpose folders.**

## Folder Hierarchy

### Design Documents (Read-Only During Implementation)

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
