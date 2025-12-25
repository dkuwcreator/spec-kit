# [PROJECT_NAME] Constitution
<!-- Example: Spec Constitution, TaskFlow Constitution, etc. -->

## Core Principles

### [PRINCIPLE_1_NAME]
<!-- Example: I. Library-First -->
[PRINCIPLE_1_DESCRIPTION]
<!-- Example: Every feature starts as a standalone library; Libraries must be self-contained, independently testable, documented; Clear purpose required - no organizational-only libraries -->

### [PRINCIPLE_2_NAME]
<!-- Example: II. CLI Interface -->
[PRINCIPLE_2_DESCRIPTION]
<!-- Example: Every library exposes functionality via CLI; Text in/out protocol: stdin/args → stdout, errors → stderr; Support JSON + human-readable formats -->

### [PRINCIPLE_3_NAME]
<!-- Example: III. Test-First (NON-NEGOTIABLE) -->
[PRINCIPLE_3_DESCRIPTION]
<!-- Example: TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced -->

### [PRINCIPLE_4_NAME]
<!-- Example: IV. Integration Testing -->
[PRINCIPLE_4_DESCRIPTION]
<!-- Example: Focus areas requiring integration tests: New library contract tests, Contract changes, Inter-service communication, Shared schemas -->

### [PRINCIPLE_5_NAME]
<!-- Example: V. Observability, VI. Versioning & Breaking Changes, VII. Simplicity -->
[PRINCIPLE_5_DESCRIPTION]
<!-- Example: Text I/O ensures debuggability; Structured logging required; Or: MAJOR.MINOR.BUILD format; Or: Start simple, YAGNI principles -->

## [SECTION_2_NAME]
<!-- Example: Additional Constraints, Security Requirements, Performance Standards, etc. -->

[SECTION_2_CONTENT]
<!-- Example: Technology stack requirements, compliance standards, deployment policies, etc. -->

## [SECTION_3_NAME]
<!-- Example: Development Workflow, Review Process, Quality Gates, etc. -->

[SECTION_3_CONTENT]
<!-- Example: Code review requirements, testing gates, deployment approval process, etc. -->

## Semantic Architecture (Meaning-First Development)

**Reference**: [Semantic Architecture](https://github.com/dkuwcreator/Semantic-Architecture)

### Core Principle: Operate Where You Have Full Context

Work is organized into **Semantic Modules** – bounded cognitive units that carry both code and meaning. Agents operate within a single module unless explicitly escalating to broader scope.

### Artifact Spaces (Tool-Agnostic)

Development artifacts live in three distinct spaces:

1. **Design Space (Read-Only)**:
   - Contains specifications, plans, contracts, research
   - Describes WHAT to build and WHY
   - **Immutable during implementation** (except progress tracking)
   - In Spec Kit: maps to `FEATURE_DIR` (typically `specs/<feature>/`)

2. **Build Space (Mutable)**:
   - Contains application code, tests, runtime configuration
   - The actual product being built
   - Where ALL implementation happens
   - In Spec Kit: maps to repository/application root

3. **Module Space (Co-located Meaning)**:
   - Module code + documentation live together
   - Each module includes README.md + AGENT_INSTRUCTION.md alongside its code
   - Prevents semantic drift through proximity
   - In Spec Kit: modules live in Build Space (e.g., `src/<module>/`)

**Rule**: Design Space is read-only. Implementation happens in Build Space. Module documentation is co-located in Build Space.

### Semantic Modules: The Atomic Bounded Context

**Semantic Modules** are the fundamental unit for safe Human–AI collaboration. Each module:

- **Has clear responsibilities**: Explicit purpose and scope
- **Declares invariants**: Non-negotiable behavioral guarantees
- **Defines boundaries**: What is inside vs. outside the module
- **Specifies interfaces**: How the module interacts with others

**Required artifacts per module** (co-located with code):

- **README.md**: Human intent documentation
  - What the module does and why it exists
  - Key responsibilities and invariants
  - Usage examples and integration patterns
  
- **AGENT_INSTRUCTION.md**: AI guidance documentation
  - Allowed edits and safety constraints
  - Module boundaries and forbidden changes
  - Testing requirements and verification steps

### Agent Scope Discipline

Agents must operate within their authorized scope:

1. **Local Module Agent** (Default):
   - Can only modify one semantic module
   - Must update module's README.md and AGENT_INSTRUCTION.md when changing behavior
   - Operates where full context is available

2. **Cluster Agent**:
   - May coordinate changes across modules in the same cluster
   - Requires explicit justification for multi-module scope
   - Must document inter-module dependencies

3. **System Agent**:
   - Allowed to refactor cross-cutting architecture
   - Requires escalation and additional review
   - Must provide migration paths for affected modules

**Escalation Rule**: When a change requires broader scope than authorized, agent MUST:
- Document why single-module approach is insufficient
- Map all affected modules and dependencies
- Request explicit approval before proceeding

### Bounded Context Rules

1. **Scope Declaration (REQUIRED)**:
   - Feature specifications MUST explicitly declare:
     - Modules in scope (with responsibilities)
     - Modules out of scope (with rationale)
     - Cross-module impacts and dependencies

2. **Module Isolation**:
   - Changes SHOULD remain within declared module boundaries
   - Single-module changes are preferred over cross-module changes
   - Module dependencies MUST be explicitly documented

3. **Interface Stability**:
   - Module interfaces MUST maintain backward compatibility
   - Breaking changes MUST be documented with migration notes
   - Interface changes MUST update all dependent modules

### Cross-Module Escalation

When changes affect multiple modules:

1. **Justification Required**: Document why cross-module scope is necessary
2. **Dependency Mapping**: List all affected modules and their relationships
3. **Compatibility Analysis**: Assess impact on module interfaces
4. **Migration Planning**: Provide upgrade path for dependent modules
5. **Review Escalation**: Cross-module changes require additional review

### Meaning Parity (NON-NEGOTIABLE)

**Principle**: Documentation MUST match implemented behavior. No semantic drift allowed.

**Required actions when changing module behavior**:

1. **Update README.md**:
   - Reflect changed responsibilities or invariants
   - Update examples if behavior changes
   - Document new integration patterns

2. **Update AGENT_INSTRUCTION.md**:
   - Adjust allowed edits if boundaries change
   - Update safety constraints for new behavior
   - Revise testing requirements

3. **Verification**:
   - Documentation review MUST accompany code review
   - Both artifacts MUST be updated in the same commit/PR
   - Stale documentation is a blocking defect

### Semantic Drift Prevention

**Drift Definition**: When documentation describes behavior that differs from actual implementation.

**Prevention measures**:

- Specification phase: Declare semantic scope upfront
- Planning phase: Map modules to implementation changes
- Task phase: Include documentation update tasks for each affected module
- Implementation phase: Update docs alongside code
- Review phase: Verify meaning parity (use checklist)

**Detection**:

- Regular semantic drift audits via `/speckit.checklist`
- Automated checks for documentation staleness
- Human review of README.md ↔ code alignment
- Agent instruction validation against actual constraints

**Resolution**:

- Semantic drift is a **HIGH severity** issue
- MUST be fixed before feature merge
- Both code and docs may need updates to restore parity
- Document resolution in commit messages

## Governance
<!-- Example: Constitution supersedes all other practices; Amendments require documentation, approval, migration plan -->

[GOVERNANCE_RULES]
<!-- Example: All PRs/reviews must verify compliance; Complexity must be justified; Use [GUIDANCE_FILE] for runtime development guidance -->

**Version**: [CONSTITUTION_VERSION] | **Ratified**: [RATIFICATION_DATE] | **Last Amended**: [LAST_AMENDED_DATE]
<!-- Example: Version: 2.1.1 | Ratified: 2025-06-13 | Last Amended: 2025-07-16 -->
