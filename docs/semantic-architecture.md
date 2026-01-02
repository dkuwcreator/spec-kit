# Semantic Architecture Integration in Spec Kit

## Overview

This fork of GitHub Spec Kit integrates **Semantic Architecture** principles to optimize codebases for understanding and safe Human–AI collaboration. Semantic Architecture treats documentation and code as equal citizens, enforcing **meaning parity** to prevent semantic drift.

**Reference**: [Semantic Architecture Repository](https://github.com/dkuwcreator/Semantic-Architecture)

**Related**: [Folder Structure Guide](./folder-structure.md) - Understanding where design documents and application code belong in Spec Kit

## What is Semantic Architecture?

Semantic Architecture is a development methodology based on these key principles:

1. **Codebases should be optimized for understanding, not just execution**
   - Code is read far more often than it's written
   - AI agents and humans must share a common understanding
   - Documentation is not optional—it's a critical artifact

2. **Semantic Modules are the atomic bounded context**
   - Each module has clear responsibilities and invariants
   - Modules encapsulate both human intent (README.md) and AI guidance (AGENT_INSTRUCTION.md)
   - Changes should respect module boundaries

3. **Meaning parity prevents semantic drift**
   - Documentation must match implemented behavior
   - When code changes, docs change (same commit/PR)
   - Stale documentation is a high-severity defect

## Semantic Modules

A **Semantic Module** is the fundamental unit for safe Human–AI collaboration. Each module consists of:

**IMPORTANT**: Module documentation lives WITH the module code at the repository root (e.g., `src/auth/README.md`), NOT in the specs folder. See [Folder Structure Guide](./folder-structure.md) for details.

### Required Artifacts

#### README.md (Human Intent)

**Location**: Next to module code (e.g., `src/auth/README.md`, `backend/src/api/README.md`)

Documents what the module does and why it exists:

- **Purpose**: Clear statement of the module's responsibility
- **Invariants**: Non-negotiable behavioral guarantees
- **Examples**: Usage patterns and integration examples
- **Dependencies**: What the module requires from other modules

#### AGENT_INSTRUCTION.md (AI Guidance)

**Location**: Next to module code (e.g., `src/auth/AGENT_INSTRUCTION.md`, `backend/src/api/AGENT_INSTRUCTION.md`)

Guides AI agents on how to safely work with the module:

- **Boundaries**: What the module does and doesn't do
- **Allowed Edits**: Operations that are safe to perform
- **Safety Constraints**: Rules that must never be violated
- **Testing Requirements**: How to verify changes are correct

### Bounded Context Rules

1. **Isolation**: Modules should minimize dependencies
2. **Explicit Interfaces**: Module interactions must be documented
3. **Stable Contracts**: Interfaces should maintain backward compatibility
4. **Clear Ownership**: Each module has defined responsibilities

## Mapping to Spec Kit Workflow

Semantic Architecture integrates into each phase of Spec Kit's template-driven workflow:

### 1. Constitution Phase (`/speckit.constitution`)

**Added**: Semantic Architecture principles section in `memory/constitution.md`

Defines organization-wide rules for:

- Module boundaries and bounded contexts
- Escalation requirements for cross-module changes
- Meaning parity enforcement
- Semantic drift prevention

### 2. Specification Phase (`/speckit.specify`)

**Added**: Semantic Scope (Required) section in `templates/spec-template.md`

Every feature specification must declare:

#### Modules In Scope

List all modules that will be modified:

```markdown
- **auth/login**: Authentication module
  - **Responsibility**: User login and session management
  - **Impact**: Add OAuth2 provider support
```

#### Modules Out Of Scope

Prevent scope creep by explicitly excluding modules:

```markdown
- **auth/signup**: User registration not affected by this feature
- **payment**: Separate feature, not in this scope
```

#### Cross-Module Impacts

Document dependencies and compatibility requirements:

```markdown
**Dependencies**: 
- auth/login depends on auth/tokens for JWT generation
- Maintains backward compatibility with existing session-based auth

**Migration Notes**:
- Existing users can upgrade OAuth2 support without re-authentication
```

### 3. Planning Phase (`/speckit.plan`)

**Added**: Semantic Architecture Plan (Required) section in `templates/plan-template.md`

The implementation plan must map features to modules:

#### Modules Impacted

```markdown
- **auth/login**:
  - Current Responsibility: Email/password authentication
  - Planned Changes: Add OAuth2 provider integration (Google, GitHub)
  - Files Affected: src/auth/login.py, src/auth/providers.py
```

#### Invariants to Preserve

```markdown
- User session tokens remain valid after OAuth2 integration
- Existing password-based login continues to work
- Session expiry behavior unchanged
```

#### Meaning Parity Updates Required

```markdown
**README.md Updates**:
- auth/login: Document OAuth2 provider configuration
- auth/tokens: Update JWT claim structure examples

**AGENT_INSTRUCTION.md Updates**:
- auth/login: Add OAuth2 provider validation rules
- auth/providers: Define new module boundaries and testing requirements
```

### 4. Tasks Phase (`/speckit.tasks`)

**Added**: Semantic Architecture Compliance phase in `templates/tasks-template.md`

Tasks must include documentation updates for each impacted module:

```markdown
## Phase N: Semantic Architecture Compliance

### Module Documentation Updates

- [ ] T042 [P] Update auth/login/README.md:
  - Add OAuth2 provider configuration examples
  - Document new login flow options
  - Update invariants (session compatibility)

- [ ] T043 [P] Update auth/login/AGENT_INSTRUCTION.md:
  - Add allowed edits for OAuth2 configuration
  - Define testing requirements for provider integration
  - Update boundary rules (no direct token generation)

### Semantic Drift Verification

- [ ] T044 Verify spec ↔ plan ↔ tasks ↔ code alignment
- [ ] T045 Meaning parity check: docs match implementation
```

### 5. Checklist Phase (`/speckit.checklist`)

**Added**: Semantic Architecture Compliance category in checklist generation

The checklist command now generates items to verify:

```markdown
## Semantic Architecture Compliance

- [ ] CHK001 - Are all impacted modules listed in Semantic Scope? [Completeness]
- [ ] CHK002 - Are modules out of scope documented? [Coverage]
- [ ] CHK003 - Do tasks include README.md updates for each module? [Completeness]
- [ ] CHK004 - Do tasks include AGENT_INSTRUCTION.md updates? [Completeness]
- [ ] CHK005 - Is there spec → plan → tasks alignment? [Traceability]
- [ ] CHK006 - Are cross-module changes justified? [Justification]
```

## Using Semantic Scope in Practice

### Example: Adding OAuth2 Support

#### Step 1: Specify with Semantic Scope

```markdown
## Semantic Scope (Required)

### Modules In Scope

- **auth/login** (src/auth/login.py):
  - Responsibility: User authentication
  - Impact: Add OAuth2 provider support alongside existing password auth

- **auth/providers** (NEW MODULE):
  - Responsibility: OAuth2 provider integration (Google, GitHub)
  - Impact: New module for provider-specific logic

### Modules Out Of Scope

- **auth/signup**: User registration not affected
- **auth/password-reset**: Separate feature
- **user-profile**: No profile changes needed

### Cross-Module Impacts

**Dependencies**:
- auth/login → auth/providers (new dependency)
- auth/login → auth/tokens (existing, unchanged)

**Compatibility**:
- Backward compatible: existing password auth continues to work
- New users can choose OAuth2 or password
```

#### Step 2: Plan Module Implementation

```markdown
## Semantic Architecture Plan (Required)

### Modules Impacted

- **auth/login**:
  - Current: Email/password only
  - Planned: Add OAuth2 option
  - Files: src/auth/login.py, src/auth/routes.py

- **auth/providers** (NEW):
  - Planned: OAuth2 provider abstraction
  - Files: src/auth/providers.py, src/auth/oauth_handlers.py

### Invariants to Preserve

- Session token format unchanged
- Password auth flow unmodified
- Existing API endpoints maintain compatibility

### Meaning Parity Updates

**Note**: Module documentation lives at repository root with the module code. See [Folder Structure Guide](./folder-structure.md).

**src/auth/login/README.md** (at repository root):
- Document OAuth2 configuration
- Show example login flows
- Update integration patterns

**src/auth/login/AGENT_INSTRUCTION.md** (at repository root):
- Add OAuth2 validation rules
- Define testing requirements
- Update allowed edits

**src/auth/providers/README.md** (NEW - at repository root):
- Define module purpose
- Document provider interface
- Show usage examples

**src/auth/providers/AGENT_INSTRUCTION.md** (NEW - at repository root):
- Define module boundaries
- Specify safety constraints
- List testing requirements
```

#### Step 3: Generate Tasks with Doc Updates

**Note**: All paths below are relative to repository root, NOT the specs folder. See [Folder Structure Guide](./folder-structure.md).

```markdown
## Phase 4: Semantic Architecture Compliance

- [ ] T032 [P] Update src/auth/login/README.md (at repository root)
- [ ] T033 [P] Update src/auth/login/AGENT_INSTRUCTION.md (at repository root)
- [ ] T034 [P] Create src/auth/providers/README.md (at repository root)
- [ ] T035 [P] Create src/auth/providers/AGENT_INSTRUCTION.md (at repository root)
- [ ] T036 Verify spec ↔ plan ↔ tasks ↔ code alignment
- [ ] T037 Meaning parity check
```

## Preventing Semantic Drift

**Semantic drift** occurs when documentation describes behavior that differs from actual implementation.

### Detection Mechanisms

1. **Specification Phase**: Declare upfront what modules are in/out of scope
2. **Planning Phase**: Map modules to specific implementation changes
3. **Task Phase**: Include documentation update tasks
4. **Checklist Phase**: Verify meaning parity

### Prevention Best Practices

1. **Same Commit Rule**: Code and docs change together
2. **Required Review**: Documentation review is part of code review
3. **Automated Checks**: CI can flag missing doc updates
4. **Regular Audits**: Use `/speckit.checklist` for semantic drift detection

### Fixing Semantic Drift

If drift is detected:

1. **Identify the divergence**: What differs between docs and code?
2. **Determine source of truth**: Is the code correct or the docs?
3. **Update both if needed**: Code may need fixes, docs definitely do
4. **Document the fix**: Commit message should mention "Fix semantic drift in [module]"

## Semantic Drift Checklist

Use this checklist to verify meaning parity:

- [ ] README.md describes actual behavior (not planned/old)
- [ ] AGENT_INSTRUCTION.md reflects actual boundaries
- [ ] Examples in docs work with current code
- [ ] Invariants listed in docs are enforced in code
- [ ] Dependencies listed in docs match actual imports
- [ ] Interface contracts match implementation
- [ ] Error scenarios documented match error handling code

## Benefits of Semantic Architecture in Spec Kit

1. **Safer AI Collaboration**: Clear boundaries prevent unintended changes
2. **Better Onboarding**: New developers understand modules through docs
3. **Reduced Bugs**: Invariants are explicit and verifiable
4. **Scope Control**: Features stay bounded to declared modules
5. **Maintainability**: Documentation stays synchronized with code
6. **Knowledge Preservation**: Module intent survives team changes

## Cross-Module Changes

Sometimes features genuinely need to modify multiple modules. Semantic Architecture doesn't prevent this—it requires **explicit justification and escalation**.

### When Cross-Module is Acceptable

- **Well-justified**: Clear reason why single-module won't work
- **Documented**: All impacts and dependencies mapped
- **Reviewed**: Additional scrutiny for scope expansion
- **Migrated**: Upgrade path for dependent modules

### Escalation Process

1. **Justify in spec**: Explain why cross-module is necessary
2. **Map dependencies**: List all affected modules and relationships
3. **Assess compatibility**: Breaking changes require migration notes
4. **Plan updates**: All affected modules get doc updates
5. **Review carefully**: Cross-module changes need extra review

## FAQ

### Q: Does this create more work?

A: Upfront, yes—you document module scope. Long-term, it saves time by preventing:

- Scope creep and unintended changes
- Debugging due to unclear boundaries
- Onboarding slowdowns from outdated docs
- Semantic drift repair work

### Q: What if I'm building a new project with no modules yet?

A: Start with coarse-grained modules (e.g., "auth", "api", "storage") and refine as the project grows. The Semantic Scope section helps you think about module boundaries from day one.

### Q: Do I need both README.md and AGENT_INSTRUCTION.md?

A: For Semantic Modules, yes. README.md is for humans (what/why), AGENT_INSTRUCTION.md is for AI agents (boundaries/constraints). They serve different audiences.

### Q: What if my docs get out of sync anyway?

A: Use `/speckit.checklist` to generate a semantic drift audit. The checklist will identify where docs and code diverge, then fix both.

### Q: Can I skip Semantic Architecture for small features?

A: No. Even small features should declare semantic scope. It takes 2 minutes and prevents scope creep. The smaller the feature, the easier it is to get this right.

### Q: How does this work with existing projects?

A: Start by adding Semantic Scope to new features. Over time, backfill module documentation (README.md + AGENT_INSTRUCTION.md) for critical modules. Prioritize by risk/change frequency.

## Dedicated Semantic Architecture Commands

Spec Kit includes specialized commands for analyzing, validating, and restructuring codebases according to Semantic Architecture principles:

### `/speckit.semantic-audit` - Comprehensive Compliance Analysis

**Purpose**: Analyze entire codebase for Semantic Architecture compliance.

**Use Cases**:
- Initial assessment of existing projects
- Regular compliance audits (quarterly or after major features)
- Identifying documentation gaps across all modules
- Detecting semantic drift at scale

**What it does**:
- Scans repository to identify all semantic modules
- Checks for missing README.md or AGENT_INSTRUCTION.md files
- Detects semantic drift (docs ↔ code misalignment)
- Validates module boundaries and dependencies
- Generates comprehensive compliance report with prioritized action items

**Example Usage**:
```bash
# Audit entire codebase
/speckit.semantic-audit

# Audit with specific focus
/speckit.semantic-audit Focus on authentication and API modules
```

**Output**: Detailed report including:
- Module inventory (compliant, partial, undocumented)
- Semantic drift instances by severity
- Boundary violations and coupling issues
- Prioritized recommendations
- Documentation templates for undocumented modules

### `/speckit.semantic-validate` - Deep Module Validation

**Purpose**: Perform detailed validation of specific semantic modules.

**Use Cases**:
- Before merging module changes
- After refactoring module boundaries
- Verifying meaning parity for critical modules
- Validating new module documentation

**What it does**:
- Validates README.md and AGENT_INSTRUCTION.md completeness
- Checks meaning parity (documentation matches code)
- Verifies bounded context rules
- Analyzes cross-module dependencies
- Validates testing requirements

**Example Usage**:
```bash
# Validate single module
/speckit.semantic-validate src/auth/

# Validate multiple modules
/speckit.semantic-validate src/auth/ src/api/ src/storage/
```

**Output**: Detailed validation report including:
- Overall grade (A-F)
- Documentation completeness scores
- API/dependency alignment analysis
- Boundary compliance status
- Prioritized action items for fixes

### `/speckit.semantic-restructure` - Interactive Restructuring Guidance

**Purpose**: Guide restructuring of projects to align with Semantic Architecture principles.

**Use Cases**:
- Generating documentation for undocumented modules
- Extracting new semantic modules from existing code
- Refactoring module boundaries to reduce coupling
- Planning comprehensive codebase restructuring

**What it does**:
- Generates README.md and AGENT_INSTRUCTION.md templates based on code analysis
- Suggests module extraction opportunities
- Proposes boundary improvements for coupled modules
- Creates migration plans for restructuring
- Provides step-by-step restructuring checklists

**Example Usage**:
```bash
# Generate docs for existing module
/speckit.semantic-restructure src/auth/

# Extract new module
/speckit.semantic-restructure --extract user-validation from src/user/

# Refactor module boundaries
/speckit.semantic-restructure --refactor-boundaries src/auth/ src/user/

# Full codebase restructuring plan
/speckit.semantic-restructure --full-audit
```

**Output**: Context-aware guidance including:
- Generated documentation templates (inferred from code)
- Module extraction/refactoring plans
- Boundary improvement suggestions
- Migration checklists and roadmaps
- Actionable next steps

### Workflow Integration

**Recommended Usage Pattern**:

1. **Initial Assessment** (New or Existing Project):
   ```bash
   /speckit.semantic-audit
   ```
   - Understand current compliance state
   - Identify priority modules to document

2. **Module Documentation** (Per Module):
   ```bash
   /speckit.semantic-restructure src/[module-path]/
   ```
   - Generate README.md and AGENT_INSTRUCTION.md templates
   - Customize based on actual module behavior

3. **Validation** (Before Merge/After Changes):
   ```bash
   /speckit.semantic-validate src/[module-path]/
   ```
   - Verify documentation completeness
   - Check meaning parity
   - Ensure boundary compliance

4. **Regular Audits** (Quarterly/After Major Features):
   ```bash
   /speckit.semantic-audit
   ```
   - Detect semantic drift
   - Identify new documentation gaps
   - Monitor compliance trends

### Integration with Feature Development

**During Feature Spec** (`/speckit.specify`):
- Declare semantic scope (modules in/out of scope)
- Document cross-module impacts

**During Planning** (`/speckit.plan`):
- Map modules to implementation changes
- Identify meaning parity update requirements

**During Task Generation** (`/speckit.tasks`):
- Include documentation update tasks for affected modules

**Before Implementation** (`/speckit.implement`):
- Validate affected modules: `/speckit.semantic-validate [modules]`
- Ensure clean baseline before changes

**After Implementation**:
- Re-validate modules: `/speckit.semantic-validate [modules]`
- Update docs alongside code (meaning parity)
- Run `/speckit.semantic-audit` if multiple modules changed

**Quality Gate** (`/speckit.checklist`):
- Semantic Architecture compliance checks included automatically
- Verifies scope, doc parity, bounded contexts

## Resources

- **Semantic Architecture Repo**: <https://github.com/dkuwcreator/Semantic-Architecture>
- **Spec Kit Repository**: <https://github.com/dkuwcreator/spec-kit>
- **Constitution Template**: [/memory/constitution.md](/memory/constitution.md)
- **Spec Template**: [/templates/spec-template.md](/templates/spec-template.md)
- **Plan Template**: [/templates/plan-template.md](/templates/plan-template.md)
- **Tasks Template**: [/templates/tasks-template.md](/templates/tasks-template.md)

## Next Steps

1. **Read the Constitution**: Review `/memory/constitution.md` for Semantic Architecture principles
2. **Try a Spec**: Use `/speckit.specify` and fill in the Semantic Scope section
3. **Generate a Checklist**: Run `/speckit.checklist` to see Semantic Architecture compliance checks
4. **Review Templates**: Examine updated templates to see integration points

## Contributing

When contributing to this fork:

1. Respect Semantic Architecture principles
2. Never remove the Semantic Scope/Plan/Compliance sections from templates
3. Update documentation alongside code changes
4. Include Semantic Architecture compliance checks in reviews
5. Document any new integration points

For questions or improvements, open an issue in the [spec-kit repository](https://github.com/dkuwcreator/spec-kit).
