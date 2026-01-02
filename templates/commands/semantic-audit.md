---
description: Analyze a codebase for Semantic Architecture compliance, identifying modules, documentation gaps, and semantic drift.
scripts:
  sh: scripts/bash/check-prerequisites.sh --json
  ps: scripts/powershell/check-prerequisites.ps1 -Json
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Goal

Perform a comprehensive Semantic Architecture compliance audit of the codebase. Identify:
- Existing semantic modules and their documentation status
- Missing README.md or AGENT_INSTRUCTION.md files
- Semantic drift between documentation and implementation
- Module boundary violations and dependency issues
- Opportunities for module extraction and improved bounded contexts

## Background: Semantic Architecture

**Semantic Architecture** is a development methodology that treats codebases as systems optimized for understanding, not just execution. It introduces **Semantic Modules** as the atomic bounded context for safe AI-assisted development.

**Learn more**: https://github.com/dkuwcreator/Semantic-Architecture

### Key Concepts

1. **Semantic Modules**: Bounded contexts that serve as the fundamental unit for human-AI collaboration. Each module encapsulates:
   - Clear responsibilities and invariants (README.md)
   - AI guidance and safety constraints (AGENT_INSTRUCTION.md)
   - Code implementing the module's purpose

2. **Meaning Parity**: Documentation and agent instructions must stay synchronized with code behavior to prevent semantic drift.

3. **Bounded Context Enforcement**: Changes should respect module boundaries, with explicit escalation for cross-module impacts.

## Operating Constraints

**STRICTLY READ-ONLY**: This command does **not** modify any files. It only analyzes and reports findings.

**Constitution Authority**: If a project constitution exists (`/memory/constitution.md`), its Semantic Architecture section defines the project-specific rules. Use these as the authoritative guidelines for the audit.

## Execution Steps

### 1. Initialize Audit Context

Run `{SCRIPT}` once from repo root and parse JSON for repository information.

**For single quotes in args**: Use escape syntax: `'I'\''m Groot'` or double-quote: `"I'm Groot"`.

### 2. Discover Project Structure

Scan the repository to identify:

**Build Space (Application Code)**:
- Primary source directories (e.g., `src/`, `lib/`, `backend/`, `frontend/`, `packages/`)
- Test directories (e.g., `tests/`, `test/`, `__tests__/`, `spec/`)
- Configuration files and project metadata

**Design Space (Specifications)**:
- Feature specifications directory (typically `specs/` or `FEATURE_DIR`)
- Architecture documentation
- Project constitution (`/memory/constitution.md`)

**Module Candidates**:
- Directories containing code with cohesive responsibilities
- Existing folders with README.md files
- Directories with clear semantic boundaries (e.g., `auth/`, `api/`, `storage/`)

### 3. Identify Semantic Modules

For each directory in the codebase, determine if it represents a semantic module:

**Module Indicators** (positive signals):
- Contains code files implementing a cohesive function
- Has a clear, single responsibility
- Contains related functionality grouped together
- Has existing documentation (README.md)
- Name suggests bounded context (e.g., `auth/`, `payment/`, `notifications/`)

**Not a Module** (exclude):
- Pure utility/helper directories without clear bounded context
- Build artifacts or generated code directories
- Third-party dependencies (`node_modules/`, `vendor/`, etc.)
- Configuration-only directories
- Test fixtures or mock data directories

**Module Classification**:
- **Compliant**: Has both README.md and AGENT_INSTRUCTION.md
- **Partial**: Has README.md but missing AGENT_INSTRUCTION.md
- **Undocumented**: Missing both documentation files
- **Potential**: Directory structure suggests module but needs documentation

### 4. Analyze Module Documentation

For each identified module, check documentation status:

#### README.md Analysis

If present, verify it contains:
- **Purpose**: Clear statement of module responsibility
- **Invariants**: Non-negotiable behavioral guarantees (if applicable)
- **Examples**: Usage patterns and integration examples
- **Dependencies**: What the module requires from other modules
- **API/Interface**: How to interact with the module

**Quality Assessment**:
- ✅ Complete: All key sections present with sufficient detail
- ⚠️ Incomplete: Missing critical sections or lacks detail
- ❌ Stub: Placeholder or minimal documentation
- ❓ Outdated: Documentation mentions code/features not present (semantic drift)

#### AGENT_INSTRUCTION.md Analysis

If present, verify it contains:
- **Boundaries**: What the module does and doesn't do
- **Allowed Edits**: Operations that are safe to perform
- **Safety Constraints**: Rules that must never be violated
- **Testing Requirements**: How to verify changes are correct

**Quality Assessment**:
- ✅ Complete: All key sections present with actionable guidance
- ⚠️ Incomplete: Missing critical sections
- ❌ Stub: Placeholder only
- ❓ Outdated: Instructions don't match current code structure

### 5. Detect Semantic Drift

**Semantic drift** occurs when documentation describes behavior that differs from implementation.

**Detection strategies**:

1. **File/Function References**: Check if documented APIs/functions exist in code
2. **Dependency Alignment**: Verify documented dependencies match actual imports
3. **Example Validation**: Check if code examples would actually work
4. **Invariant Verification**: Look for code that might violate documented invariants
5. **Interface Matching**: Compare documented interfaces with actual exports/public APIs

**Drift Indicators**:
- Documentation mentions files/functions that don't exist
- Code imports modules not listed in dependencies
- Examples reference deprecated or removed APIs
- Documented invariants contradicted by implementation
- Interface definitions don't match actual code

**Output**: For each drift instance, report:
- Module name
- Drift type (missing code, extra code, mismatched behavior)
- Location in docs and code
- Severity (CRITICAL, HIGH, MEDIUM, LOW)

### 6. Analyze Module Boundaries

Evaluate how well modules maintain bounded contexts:

**Boundary Violations**:
- **Tight Coupling**: Module directly modifies another module's internal state
- **Hidden Dependencies**: Module uses another module without documenting it
- **Leaky Abstraction**: Module exposes internal implementation details
- **Circular Dependencies**: Module A depends on B, B depends on A

**Cross-Module Analysis**:
- Map actual dependencies between modules (via imports/requires)
- Compare with documented dependencies
- Identify clusters of tightly coupled modules
- Flag opportunities for better boundaries

### 7. Generate Compliance Report

Output a comprehensive Markdown report with the following structure:

```markdown
# Semantic Architecture Audit Report

**Generated**: [timestamp]
**Repository**: [repo name]
**Audit Scope**: [description of what was analyzed]

## Executive Summary

- **Total Modules Identified**: [count]
  - Compliant: [count] (has both README.md and AGENT_INSTRUCTION.md)
  - Partial: [count] (has README.md only)
  - Undocumented: [count] (missing both)
  - Potential: [count] (candidates for modularization)

- **Semantic Drift Instances**: [count]
  - Critical: [count]
  - High: [count]
  - Medium: [count]
  - Low: [count]

- **Boundary Issues**: [count violations]

## Module Inventory

| Module Path | Status | README.md | AGENT_INSTRUCTION.md | Issues |
|-------------|--------|-----------|----------------------|--------|
| src/auth/ | Compliant | ✅ Complete | ✅ Complete | 0 |
| src/api/ | Partial | ✅ Complete | ❌ Missing | 1 |
| src/storage/ | Undocumented | ❌ Missing | ❌ Missing | 2 |

## Semantic Drift Analysis

### Critical Drift

| Module | Type | Location | Description | Recommendation |
|--------|------|----------|-------------|----------------|
| [module] | Missing Code | README.md:L42 | Documents `authenticate()` function not found in code | Remove from docs or implement |

### High Drift

[Similar table for HIGH severity items]

## Boundary Analysis

### Violations Detected

| Module A | Module B | Issue Type | Description |
|----------|----------|------------|-------------|
| src/auth/ | src/user/ | Tight Coupling | auth directly modifies user.status field |

### Dependency Map

[Visual or textual representation of module dependencies]

### Suggested Module Clusters

[Groups of related modules that could benefit from clearer boundaries]

## Recommendations

### Priority 1: Critical Issues (Fix Immediately)

1. **Fix semantic drift in [module]**: [specific action]
2. **Address boundary violation in [modules]**: [specific action]

### Priority 2: Documentation Gaps (Fix Before Next Feature)

1. **Add AGENT_INSTRUCTION.md to [module]**: [guidance]
2. **Complete README.md for [module]**: [missing sections]

### Priority 3: Improvements (Plan for Refactoring)

1. **Extract [potential module] into semantic module**: [rationale]
2. **Refactor [modules] cluster for clearer boundaries**: [strategy]

## Module Documentation Templates

### For Undocumented Modules

[Provide templates for each undocumented module based on analysis]

**Module: src/auth/**

Suggested README.md structure:
- Purpose: [inferred from code analysis]
- Key Responsibilities: [list of main functions/features]
- Invariants: [based on code patterns]
- Dependencies: [from import analysis]

## Constitution Compliance

[If /memory/constitution.md exists]

**Constitution Status**: [Present/Absent]

**Semantic Architecture Section**: [Present/Absent]

**Compliance Issues**:
- [List any violations of constitution-defined Semantic Architecture rules]

## Next Steps

1. **Immediate Actions**:
   - Address CRITICAL semantic drift issues
   - Fix boundary violations blocking safe AI collaboration

2. **Short-term (This Sprint)**:
   - Add missing AGENT_INSTRUCTION.md files to partial modules
   - Complete stub documentation
   - Resolve HIGH drift issues

3. **Long-term (Roadmap)**:
   - Extract potential modules with clear boundaries
   - Refactor tightly coupled module clusters
   - Establish semantic drift prevention practices

## Commands for Remediation

```bash
# To validate individual modules after fixes:
/speckit.semantic-validate src/auth/

# To restructure specific modules:
/speckit.semantic-restructure src/api/

# To re-run full audit:
/speckit.semantic-audit
```

---

**Note**: This audit is a point-in-time assessment. Regular audits recommended after major features or quarterly.
```

### 8. Provide Actionable Guidance

After presenting the report, offer to:

1. **Generate documentation templates** for undocumented modules
2. **Create remediation tasks** that can be added to tasks.md
3. **Suggest module extraction** strategies for better boundaries
4. **Draft AGENT_INSTRUCTION.md** files based on code analysis

Ask: "Would you like me to generate documentation templates for any specific modules? Specify module path(s)."

## Analysis Heuristics

### Module Detection Heuristics

**Strong Module Indicators** (high confidence):
- Directory contains 5+ related code files
- Directory name matches common bounded context pattern (auth, api, core, data, etc.)
- Existing README.md suggests intentional modularization
- Clear single responsibility (e.g., all files relate to authentication)

**Weak Module Indicators** (potential, needs verification):
- Directory with 2-4 code files
- Generic name (utils, helpers, common) but cohesive functionality
- Nested deeply but has clear purpose

**Not a Module**:
- Single file in directory
- Mixed unrelated concerns
- Pure configuration without logic
- Generated or build artifact

### Semantic Drift Detection Heuristics

**File-based**:
- Parse documentation for code references (function names, class names, file paths)
- Check if referenced items exist in codebase
- Flag missing or renamed items

**Import-based**:
- Extract documented dependencies from README.md
- Parse actual imports from code files
- Flag undocumented dependencies or documented but unused

**Example-based**:
- Extract code examples from markdown code blocks
- Check if example APIs exist in current codebase
- Flag broken examples

**Invariant-based** (advanced, optional):
- Identify invariant statements in README.md
- Look for code patterns that might violate them
- Flag potential contradictions (e.g., "never returns null" but code has `return null`)

### Boundary Violation Detection

**Import Graph Analysis**:
- Build dependency graph from imports
- Identify cycles (A → B → A)
- Flag direct access to internal files across module boundaries

**Convention Violations**:
- Module A imports from `module_b/internal/` or `module_b/src/`
- Module A imports from `module_b.py` when `module_b/__init__.py` should be interface

## Token Efficiency Guidelines

**Progressive Disclosure**:
- Load module documentation incrementally (don't dump all READMEs at once)
- Analyze and report in batches (top 10 modules first, then offer to continue)
- Summarize large findings (if >20 drift instances, show top 10 + count)

**Focus on High-Signal Output**:
- Prioritize CRITICAL and HIGH severity findings
- Aggregate LOW severity items into summary counts
- Provide actionable next steps, not exhaustive listings

**Avoid Redundancy**:
- Don't duplicate information across report sections
- Use tables and compact formats
- Reference sections by link rather than repeating content

## Context

{ARGS}
