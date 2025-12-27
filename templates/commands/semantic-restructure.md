---
description: Guide restructuring of a codebase or module to align with Semantic Architecture principles, generating module documentation and suggesting boundary improvements.
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

Help restructure a codebase or specific module to align with Semantic Architecture principles by:
- Generating module documentation templates (README.md + AGENT_INSTRUCTION.md)
- Suggesting module boundary improvements
- Creating migration plans for existing codebases
- Identifying opportunities to extract semantic modules
- Providing actionable restructuring guidance

This command is **interactive and generative** - it creates documentation templates and suggests code organization changes (but does not modify code directly without approval).

## Background: Semantic Architecture

**Semantic Architecture** organizes code into **Semantic Modules** - bounded contexts with explicit human and AI documentation.

**Learn more**: https://github.com/dkuwcreator/Semantic-Architecture

### Key Principles

1. **Bounded Contexts**: Each module has clear responsibilities and boundaries
2. **Co-located Documentation**: README.md + AGENT_INSTRUCTION.md live with code
3. **Meaning Parity**: Documentation stays synchronized with implementation
4. **Agent Scope Discipline**: Changes respect module boundaries

## Operating Modes

This command operates in different modes based on user intent:

### Mode 1: Generate Module Documentation

**Trigger**: User specifies module path to document
**Example**: `/speckit.semantic-restructure src/auth/`

**Actions**:
- Analyze module code structure
- Generate README.md template
- Generate AGENT_INSTRUCTION.md template
- Create templates based on actual code analysis

### Mode 2: Extract New Module

**Trigger**: User wants to extract functionality into new module
**Example**: `/speckit.semantic-restructure --extract user-validation from src/user/`

**Actions**:
- Identify files to extract
- Suggest new module structure
- Generate documentation for new module
- Provide migration checklist

### Mode 3: Refactor Module Boundaries

**Trigger**: User wants to improve existing module boundaries
**Example**: `/speckit.semantic-restructure --refactor-boundaries src/auth/ src/user/`

**Actions**:
- Analyze coupling between modules
- Suggest interface improvements
- Propose boundary clarifications
- Generate updated documentation

### Mode 4: Full Codebase Restructuring

**Trigger**: User wants comprehensive restructuring guidance
**Example**: `/speckit.semantic-restructure --full-audit`

**Actions**:
- Analyze entire codebase
- Suggest module extraction opportunities
- Propose high-level architecture
- Generate migration roadmap

## Execution Steps

### 1. Initialize Context

Run `{SCRIPT}` once from repo root and parse JSON for repository information.

**Parse User Intent**:
- Determine which mode to operate in
- Extract target paths or restructuring scope
- Identify any specific requirements or constraints

**For single quotes in args**: Use escape syntax: `'I'\''m Groot'` or double-quote: `"I'm Groot"`.

### 2. Clarify Intent (Interactive)

Based on `$ARGUMENTS`, ask targeted questions:

**If path specified but mode unclear**:
- "Would you like me to:"
  - A) Generate documentation for existing module at [path]
  - B) Extract new module from [path]
  - C) Refactor boundaries for [path] and related modules
  - D) Full analysis with restructuring suggestions

**If extracting module**:
- "What functionality should the new module contain?"
- "What should the new module be named?"
- "Should existing code be moved or copied?"

**If refactoring boundaries**:
- "What issues are you experiencing?" (tight coupling, unclear responsibilities, etc.)
- "Are there specific modules that should interact less?"

**If full audit**:
- "What are your main concerns?" (monolith, unclear structure, AI collaboration safety, etc.)
- "Are there areas you want to preserve as-is?"

### 3. Analyze Target Code

For the target path(s):

**Code Structure Analysis**:
- Identify code files and their purposes
- Detect programming language(s)
- Map public vs private/internal code
- Identify entry points and main interfaces
- Detect dependencies (imports/requires)

**Semantic Analysis**:
- Infer module responsibility from code
- Identify cohesive functionality groups
- Detect potential sub-modules
- Map cross-module dependencies
- Identify tightly coupled areas

**Existing Documentation**:
- Check for existing README.md
- Check for existing AGENT_INSTRUCTION.md
- Assess documentation quality if present

### 4. Mode-Specific Actions

#### Mode 1: Generate Module Documentation

**Step 1: Generate README.md Template**

Based on code analysis, create a comprehensive README.md template:

```markdown
# [Module Name] Module

## Purpose

[Inferred from code analysis: Primary responsibility of this module]

**Suggested text**: This module is responsible for [inferred purpose based on code]. It provides [key capabilities] and ensures [main guarantees].

## Responsibilities

Based on code analysis, this module handles:

1. **[Responsibility 1]**: [Inferred from main code section]
2. **[Responsibility 2]**: [Inferred from secondary code section]
3. **[Responsibility 3]**: [Add more as needed]

**TODO**: Review and refine these responsibilities to match actual intent.

## Invariants

[Section to be completed - identify non-negotiable behavioral guarantees]

**Suggestions based on code**:
- [Detected pattern: e.g., "All inputs are validated before processing"]
- [Detected pattern: e.g., "Never returns null, uses Option/Result pattern"]
- [Add more based on code patterns]

**TODO**: Verify these invariants match intended behavior.

## API / Public Interface

### Main Functions

[List of detected public functions/classes]

#### `functionName(param1, param2)`

**Purpose**: [Inferred from function name and usage]
**Parameters**:
- `param1` ([type]): [description - TODO]
- `param2` ([type]): [description - TODO]
**Returns**: [type] - [description - TODO]
**Example**:
```[language]
// TODO: Add usage example
```

[Repeat for each public function]

## Dependencies

### Internal Dependencies
[List of internal module dependencies detected from imports]

- `[module path]`: [Purpose - TODO: describe why this dependency exists]

### External Dependencies
[List of external package dependencies]

- `[package name]` ([version]): [Purpose - TODO: describe usage]

## Usage Examples

[Provide 2-3 usage examples based on code analysis]

### Example 1: [Basic Usage]
```[language]
// TODO: Add basic usage example based on main API
```

### Example 2: [Common Pattern]
```[language]
// TODO: Add common integration pattern
```

## Architecture Notes

[Optional section for design decisions]

**TODO**: Document key architectural decisions:
- Why this module exists as separate bounded context
- Design patterns used (if any)
- Performance considerations (if any)

---

**Last Updated**: [Date]
**Authors**: [Team/Individual]
```

**Step 2: Generate AGENT_INSTRUCTION.md Template**

```markdown
# Agent Instructions: [Module Name]

## Module Boundaries

### What This Module Does

This module is responsible for:
- [Responsibility 1 from README]
- [Responsibility 2 from README]
- [Responsibility 3 from README]

### What This Module Does NOT Do

[Based on analysis of what's NOT in the code]

This module does not handle:
- [Out of scope item 1]
- [Out of scope item 2]
- [Any cross-cutting concerns handled elsewhere]

**Boundary Rule**: This module focuses solely on [core responsibility]. Related but separate concerns (like [example]) belong in [other module].

### Module Interface

**Public API** (can be called from outside):
[List of public functions detected]

**Internal API** (module-private):
[List of internal/private functions detected]

**Rule**: External code should ONLY use the Public API. Internal functions are subject to change.

## Allowed Edits

When modifying this module, you MAY:

### ✅ Safe Operations

1. **Add new functions** to the public API:
   - New functionality extending module's core responsibility
   - Must update README.md API section
   - Must add tests for new functions

2. **Modify internal implementation**:
   - Refactor internal functions
   - Optimize algorithms
   - As long as public API behavior remains unchanged

3. **Fix bugs**:
   - Correct incorrect behavior
   - Update documentation if behavior was misunderstood

4. **Improve documentation**:
   - Clarify existing documentation
   - Add examples
   - Fix outdated information (and update code if needed)

### Specific Allowed Patterns

[Based on code patterns detected]

- **[Pattern 1]**: [Description of safe change pattern]
- **[Pattern 2]**: [Description of safe change pattern]

## Safety Constraints

### ❌ FORBIDDEN Operations

**NEVER do the following without explicit escalation**:

1. **Break Public API Contracts**:
   - Changing function signatures for public APIs
   - Removing public functions
   - Changing return types in non-backward-compatible ways

2. **Violate Invariants**:
   [List invariants from README.md]
   - [Invariant 1 - must be preserved]
   - [Invariant 2 - must be preserved]

3. **Cross Module Boundaries**:
   - Directly modifying other modules' internal state
   - Importing from other modules' internal/private sections
   - Tight coupling with other modules

4. **Bypass Validation/Security**:
   [Based on validation patterns detected in code]
   - [Specific validation that must never be skipped]

### Specific Forbidden Patterns

[Based on code analysis]

- **[Anti-pattern 1]**: [Why it's forbidden]
- **[Anti-pattern 2]**: [Why it's forbidden]

## Testing Requirements

### Required Test Coverage

When making changes, ensure tests cover:

1. **Public API Functions**:
   [List each public function]
   - `functionName()`: Test [key scenarios]

2. **Invariants Verification**:
   [For each invariant from README]
   - Verify [invariant 1] holds under [scenarios]

3. **Edge Cases**:
   [Based on code analysis]
   - [Edge case 1 detected in code]
   - [Edge case 2 detected in code]

### Test Execution

**Run tests**: [TODO: Add command to run tests]
```bash
# Example: npm test [module-name]
# Example: pytest tests/[module-name]/
```

**Minimum Coverage**: [TODO: Define coverage threshold, e.g., 80%]

### Integration Testing

When changes affect module interface:
- Test integration with dependent modules: [list modules]
- Verify backward compatibility

## Dependencies & Integration

### Modules This Module Depends On

[From dependency analysis]

| Module | Purpose | Interface Used |
|--------|---------|----------------|
| [module path] | [why dependency exists] | [which functions/APIs] |

### Modules That Depend On This Module

[Requires broader codebase analysis - TODO]

**TODO**: Document known dependents and ensure changes don't break them.

### External Integration Points

[From external dependency analysis]

- **[External service/library]**: [How it's used]

## Common Modification Scenarios

### Scenario 1: Adding New Feature to Existing API

**Steps**:
1. Design function signature
2. Write tests first (TDD)
3. Implement function
4. Update README.md API section
5. Add usage example

**Safety Check**: Does new feature fit within module's core responsibility? If not, escalate.

### Scenario 2: Fixing a Bug

**Steps**:
1. Add test case reproducing bug
2. Fix implementation
3. Verify test passes
4. Check if README.md claims incorrect behavior (semantic drift)
5. Update docs if needed

### Scenario 3: Refactoring Internal Code

**Steps**:
1. Ensure existing tests pass
2. Refactor internal functions
3. Verify tests still pass
4. No README.md changes needed (internal change)

**Safety Check**: Did public API behavior change? If yes, update docs.

## Escalation Triggers

**ESCALATE to human review if**:

1. Change affects multiple modules
2. Change breaks public API contract
3. Unsure if change violates invariant
4. Change requires new external dependency
5. Module boundaries become unclear

**Escalation Process**: [TODO: Define - create GitHub issue, ping team lead, etc.]

---

**Last Updated**: [Date]
**Maintained by**: [Team/Individual]
```

**Step 3: Present Templates**

Show user the generated templates and ask:
- "Review the generated templates above. Would you like me to:"
  - A) Save these templates to the module directory
  - B) Refine specific sections before saving
  - C) Generate templates for additional modules

#### Mode 2: Extract New Module

**Step 1: Analyze Extraction Target**

Identify files and functions to extract:
- Parse user's specification of what to extract
- Find related code across current module
- Identify dependencies of target functionality
- Determine what would remain in original module

**Step 2: Suggest Module Structure**

```markdown
## Proposed Module Extraction

### New Module: [suggested-name]

**Location**: `[parent-path]/[suggested-name]/`

**Files to Move**:
- `[file1.ext]` - [purpose]
- `[file2.ext]` - [purpose]

**Files to Create**:
- `README.md` - Module documentation
- `AGENT_INSTRUCTION.md` - AI guidance
- `[index/init file]` - Module entry point

### Impact Analysis

**Original Module** (`[original-path]`):
- Will have reduced responsibility
- New dependencies: Will depend on extracted module
- Files remaining: [count] files

**New Module** (`[new-path]`):
- Clear, focused responsibility: [extracted purpose]
- Dependencies: [list dependencies]
- Interface: [proposed public API]

### Migration Checklist

- [ ] Create new module directory structure
- [ ] Move identified files to new module
- [ ] Create README.md for new module
- [ ] Create AGENT_INSTRUCTION.md for new module
- [ ] Update imports in original module
- [ ] Update README.md of original module (reduced scope)
- [ ] Update AGENT_INSTRUCTION.md of original module
- [ ] Create tests for new module
- [ ] Run integration tests
- [ ] Update any dependent modules
```

**Step 3: Generate Documentation for New Module**

Use Mode 1 templates, but tailored to extracted functionality.

**Step 4: Provide Migration Guidance**

Offer to:
- Generate tasks.md for the extraction
- Create stub files for new module
- Draft updated documentation for original module

#### Mode 3: Refactor Module Boundaries

**Step 1: Analyze Boundary Issues**

For specified modules:
- Build dependency graph
- Identify tight coupling
- Find boundary violations (internal imports)
- Detect overlapping responsibilities

**Step 2: Suggest Boundary Improvements**

```markdown
## Boundary Refactoring Suggestions

### Current Issues

1. **Tight Coupling**: [Module A] and [Module B]
   - [Module A] directly accesses [Module B]'s internal state
   - Suggested fix: Create explicit interface in [Module B]

2. **Overlapping Responsibilities**: [Module C] and [Module D]
   - Both handle [functionality X]
   - Suggested fix: Consolidate in [Module C], remove from [Module D]

3. **Unclear Interface**: [Module E]
   - Public API not well-defined
   - Internal functions exposed
   - Suggested fix: Define explicit public API, move internal to private

### Proposed Refactoring

#### Module A → Module B Interface

**Current** (problematic):
```[language]
// Module A accessing Module B internals
import { internalHelper } from 'module-b/internal/helper';
```

**Proposed** (clean boundary):
```[language]
// Module B exposes public API
import { processData } from 'module-b';
```

**Changes Required**:
1. Module B: Add `processData()` to public API
2. Module B: Update AGENT_INSTRUCTION.md to forbid external access to `internal/`
3. Module A: Change import to use public API
4. Module A: Update dependencies in README.md

### Refactoring Checklist

- [ ] Define clear public APIs for each module
- [ ] Update AGENT_INSTRUCTION.md with new boundaries
- [ ] Refactor code to respect boundaries
- [ ] Update README.md dependencies
- [ ] Add integration tests for new interfaces
- [ ] Remove direct access to internal code
```

**Step 3: Generate Updated Documentation**

For each affected module:
- Suggest updates to README.md (refined responsibilities)
- Suggest updates to AGENT_INSTRUCTION.md (clearer boundaries)

#### Mode 4: Full Codebase Restructuring

**Step 1: Comprehensive Analysis**

Scan entire codebase:
- Identify all potential semantic modules
- Build full dependency graph
- Detect architectural patterns (layering, etc.)
- Find areas of high coupling
- Identify code without clear module home

**Step 2: Propose High-Level Architecture**

```markdown
## Proposed Semantic Architecture

### Module Organization

Based on codebase analysis, suggested module structure:

```
[repo-root]/
├── src/
│   ├── core/                      # Core domain logic
│   │   ├── README.md
│   │   ├── AGENT_INSTRUCTION.md
│   │   └── [core modules]
│   ├── auth/                      # Authentication & authorization
│   │   ├── README.md
│   │   ├── AGENT_INSTRUCTION.md
│   │   └── [auth code]
│   ├── api/                       # External API interface
│   │   ├── README.md
│   │   ├── AGENT_INSTRUCTION.md
│   │   └── [api code]
│   └── data/                      # Data access layer
│       ├── README.md
│       ├── AGENT_INSTRUCTION.md
│       └── [data access code]
└── tests/
    └── [mirror structure]
```

### Module Descriptions

#### Core Module (`src/core/`)
- **Responsibility**: [Core business logic]
- **Current Location**: [scattered across files]
- **Extraction Complexity**: Medium
- **Priority**: High (foundational)

[Repeat for each proposed module]

### Migration Roadmap

**Phase 1: Foundation** (Week 1-2)
- [ ] Create core modules with documentation
- [ ] Extract core functionality
- [ ] Establish module boundaries

**Phase 2: Boundaries** (Week 3-4)
- [ ] Refactor cross-module dependencies
- [ ] Define clear interfaces
- [ ] Update all module documentation

**Phase 3: Completion** (Week 5-6)
- [ ] Generate remaining module documentation
- [ ] Validate semantic architecture compliance
- [ ] Training and documentation for team
```

**Step 3: Generate Migration Tasks**

Offer to generate detailed tasks.md for the migration.

### 5. Generate Documentation Templates

For any mode that requires new documentation:

**Template Generation Strategy**:
1. **Analyze code first**: Don't hallucinate, base templates on actual code
2. **Mark TODOs clearly**: Sections needing human input
3. **Provide suggestions**: Based on code analysis, offer starting points
4. **Include examples**: Show what good documentation looks like
5. **Reference actual code**: Link to specific files/functions

**Quality Indicators**:
- ✅ Template contains inferred content from code analysis
- ✅ TODOs are specific (not generic "fill this in")
- ✅ Examples match actual code patterns
- ✅ Suggestions are actionable

### 6. Offer Next Steps

After presenting restructuring plan:

```markdown
## Next Steps

**Immediate Actions**:
1. Review proposed structure/documentation
2. Provide feedback on suggestions
3. Approve or request refinements

**Once Approved**:
- I can generate tasks.md for the restructuring
- I can create stub files/directories
- I can help with specific documentation sections

**Commands**:
```bash
# To validate after restructuring:
/speckit.semantic-validate [module-path]

# To audit entire codebase:
/speckit.semantic-audit

# To generate missing docs:
/speckit.semantic-restructure --generate-docs [module-path]
```

**Questions?**
- Would you like me to refine any section?
- Should I generate tasks for this restructuring?
- Do you want to see more detail on any module?
```

## Code Analysis Strategies

### Module Responsibility Inference

**For Python**:
- Analyze main class/function names
- Parse module docstrings
- Identify common patterns (e.g., `*_handler`, `*_service`, `*_repository`)

**For JavaScript/TypeScript**:
- Analyze exported names
- Parse JSDoc comments
- Identify design patterns (controller, service, etc.)

**Generic**:
- File naming conventions
- Directory structure
- Common prefixes/suffixes in function names

### Invariant Detection

Look for code patterns that suggest invariants:
- Validation at function entry points → "All inputs are validated"
- Never returning null, using Optional → "Never returns null"
- Always using try/catch → "Never throws unhandled exceptions"
- Consistent use of types → "Type-safe API"

### Dependency Analysis

**Internal Dependencies**:
- Parse import/require statements
- Filter for relative or same-project imports
- Build dependency graph

**External Dependencies**:
- Parse package manifests (package.json, requirements.txt, go.mod)
- Identify third-party libraries

## Token Efficiency

**Progressive Disclosure**:
- Show overview first, details on request
- Generate one module's docs at a time (not all at once)
- Offer to continue vs dumping everything

**Compact Templates**:
- Use placeholders and TODOs effectively
- Don't repeat information
- Link to external resources vs explaining everything

**Focused Analysis**:
- Analyze only what's needed for current mode
- Don't do full codebase scan for single module documentation

## Context

{ARGS}
