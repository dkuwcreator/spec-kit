# GitHub Copilot Instructions for Spec Kit

## About This Repository

This is a fork of GitHub Spec Kit that integrates **Semantic Architecture** principles to optimize codebases for understanding and safe Human–AI collaboration.

## Semantic Architecture Overview

**Semantic Architecture** is a development methodology that treats codebases as systems optimized for understanding, not just execution. It introduces **Semantic Modules** as the atomic bounded context for safe AI-assisted development.

**Learn more**: [Semantic Architecture Repository](https://github.com/dkuwcreator/Semantic-Architecture)

### Key Concepts

1. **Semantic Modules**: Bounded contexts that serve as the fundamental unit for human-AI collaboration. Each module encapsulates:
   - Clear responsibilities and invariants
   - Explicit boundaries and interfaces
   - Human intent (README.md)
   - AI guidance (AGENT_INSTRUCTION.md)

2. **Meaning Parity**: Documentation and agent instructions must stay synchronized with code behavior to prevent semantic drift.

3. **Bounded Context Enforcement**: Changes should respect module boundaries, with explicit escalation for cross-module impacts.

## Copilot Guidelines for This Fork

### When Working on Spec Kit Features

1. **Respect Semantic Boundaries**
   - Treat each Semantic Module as a bounded context
   - Understand module responsibilities before making changes
   - Explicitly declare when changes cross module boundaries

2. **Enforce Scope Declaration**
   - Feature specifications MUST declare semantic scope (modules in/out of scope)
   - Plans MUST list impacted modules with invariants to preserve
   - Tasks MUST include documentation updates (README.md + AGENT_INSTRUCTION.md)

3. **Maintain Meaning Parity**
   - When changing behavior or invariants, update both:
     - README.md (human intent: what/why, responsibilities, invariants)
     - AGENT_INSTRUCTION.md (AI guidance: boundaries, allowed edits, safety constraints)
   - Verify that documentation matches implemented behavior
   - Flag semantic drift in reviews

4. **Cross-Module Changes Require Escalation**
   - If a change affects multiple modules:
     - Document dependencies and compatibility impacts
     - Justify the cross-module scope
     - Update affected module documentation
     - Consider migration notes if interfaces change

### When Modifying Spec Kit Templates

**CRITICAL**: This repository is template-driven. Changes must be:

- **Additive**: Never remove existing features or break placeholders
- **Backward-compatible**: Existing workflows must continue to function
- **Consistent**: Follow existing tone and formatting conventions
- **REQUIRED sections**: Clearly mark new mandatory sections

Templates live in:

- `templates/commands/*.md` - Command behavior templates
- `templates/*.md` - Artifact templates (spec, plan, tasks, etc.)
- `memory/constitution.md` - Constitution template

### Template Modification Rules

1. **Do NOT remove placeholders** like `[PROJECT_NAME]`, `[PRINCIPLE_1_NAME]`, etc.
2. **Do NOT delete existing sections** unless explicitly required
3. **Add new sections** clearly marked as "(Required)" or "(Optional)"
4. **Preserve comment guidance** that helps users understand templates
5. **Keep formatting consistent** with existing style

### Semantic Architecture Integration Points

The following Spec Kit templates now include Semantic Architecture requirements:

1. **Specification (`templates/spec-template.md`)**
   - Semantic Scope (Required): Declares modules in/out of scope and cross-module impacts

2. **Planning (`templates/plan-template.md`)**
   - Semantic Architecture Plan (Required): Lists impacted modules, invariants, and required documentation updates

3. **Tasks (`templates/tasks-template.md`)**
   - Semantic parity tasks for each impacted module (README.md + AGENT_INSTRUCTION.md updates)

4. **Checklist (`templates/commands/checklist.md`)**
   - Semantic Architecture Compliance Checks: Verifies scope, doc parity, and no semantic drift

5. **Constitution (`memory/constitution.md`)**
   - Semantic Architecture section: Defines principles for meaning-first development

### Code Review Checklist

Before finalizing any changes:

- [ ] No existing placeholders removed from templates
- [ ] New sections clearly marked REQUIRED or Optional
- [ ] Semantic scope declared for feature changes
- [ ] Module boundaries respected
- [ ] Documentation updated alongside code (meaning parity)
- [ ] Cross-module impacts documented and justified
- [ ] Backward compatibility verified
- [ ] Links to Semantic Architecture repo included where relevant

## Development Workflow

Spec Kit follows this template-driven workflow:

1. **Constitution** → Define project principles and constraints
2. **Specify** → Create feature specifications (what/why, no how)
3. **Plan** → Generate technical plans with semantic scope
4. **Tasks** → Break down into implementable tasks with doc parity requirements
5. **Implement** → Execute tasks while maintaining meaning parity
6. **Checklist** → Verify semantic architecture compliance

## Resources

- **Spec Kit README**: [/README.md](/README.md)
- **Semantic Architecture**: <https://github.com/dkuwcreator/Semantic-Architecture>
- **Semantic Architecture Docs**: [/docs/semantic-architecture.md](/docs/semantic-architecture.md)
- **Contributing Guide**: [/CONTRIBUTING.md](/CONTRIBUTING.md)

## Questions?

If you encounter ambiguity or need clarification:

1. Check the constitution at `/memory/constitution.md`
2. Review Semantic Architecture docs at `/docs/semantic-architecture.md`
3. Examine existing templates for patterns
4. Ask the user for guidance rather than making assumptions that could break compatibility
