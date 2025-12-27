---
description: Validate a specific semantic module for compliance with Semantic Architecture principles, checking meaning parity and bounded context rules.
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

Perform deep validation of one or more specific semantic modules to ensure:
- Documentation exists and is complete (README.md + AGENT_INSTRUCTION.md)
- Meaning parity: docs accurately reflect code behavior
- Bounded context rules are followed
- Module boundaries are well-defined and respected
- Testing requirements are specified and achievable

This is a **targeted, detailed validation** for specific modules, unlike `/speckit.semantic-audit` which provides a broad overview of the entire codebase.

## Background: Semantic Architecture

**Semantic Architecture** treats each module as a bounded context with explicit documentation for both humans (README.md) and AI agents (AGENT_INSTRUCTION.md).

**Learn more**: https://github.com/dkuwcreator/Semantic-Architecture

## Operating Constraints

**READ-ONLY**: This command does **not** modify any files. It analyzes and reports validation results.

**Target**: One or more module paths specified by user, or current directory if not specified.

## Execution Steps

### 1. Initialize Validation Context

Run `{SCRIPT}` once from repo root and parse JSON for repository information.

**Parse Module Target**:
- If `$ARGUMENTS` contains a path (e.g., `src/auth/`), validate that module
- If `$ARGUMENTS` contains multiple paths, validate each
- If no path specified, validate module in current working directory
- If path doesn't exist, report error and exit

**For single quotes in args**: Use escape syntax: `'I'\''m Groot'` or double-quote: `"I'm Groot"`.

### 2. Module Discovery

For each target path:

**Verify Module Existence**:
- Check if path exists and is a directory
- Confirm directory contains code files (not just docs/config)
- Identify primary programming language(s)

**Locate Documentation**:
- Look for README.md in module directory
- Look for AGENT_INSTRUCTION.md in module directory
- Check for legacy/alternative names (README.rst, INSTRUCTIONS.md, etc.)

**Identify Module Structure**:
- List code files and subdirectories
- Identify test files (if co-located)
- Map public interfaces (exported functions/classes)
- Build internal structure overview

### 3. Documentation Completeness Check

#### README.md Validation

**Required Sections** (per Semantic Architecture guidelines):

1. **Purpose / Overview**:
   - ✅ Clear statement of module responsibility
   - ✅ Why this module exists
   - ⚠️ Check: Is purpose specific or too vague? ("Handles auth" ✅ vs "Misc utilities" ❌)

2. **Responsibilities**:
   - ✅ List of key responsibilities
   - ✅ Clear scope definition
   - ⚠️ Check: Are responsibilities cohesive or mixed concerns?

3. **Invariants** (if applicable):
   - ✅ Non-negotiable behavioral guarantees
   - ✅ Constraints that must never be violated
   - ⚠️ Check: Are invariants testable/verifiable?

4. **API / Interface**:
   - ✅ How to use the module
   - ✅ Key functions/classes and their purpose
   - ✅ Integration patterns
   - ⚠️ Check: Do documented APIs exist in code?

5. **Dependencies**:
   - ✅ What this module requires from other modules
   - ✅ External dependencies
   - ⚠️ Check: Do documented dependencies match imports?

6. **Examples** (recommended):
   - Usage examples
   - Integration patterns
   - ⚠️ Check: Do examples work with current code?

**Quality Assessment**:
- **Complete**: All required sections present with sufficient detail
- **Incomplete**: Missing 1-2 required sections
- **Minimal**: Has purpose only, missing most sections
- **Missing**: No README.md file

**Output**: List missing or incomplete sections with recommendations.

#### AGENT_INSTRUCTION.md Validation

**Required Sections** (per Semantic Architecture guidelines):

1. **Module Boundaries**:
   - ✅ What the module does (scope)
   - ✅ What the module does NOT do (out of scope)
   - ✅ Module interface definition
   - ⚠️ Check: Are boundaries clear and enforceable?

2. **Allowed Edits**:
   - ✅ Types of changes that are safe to make
   - ✅ Files that can be modified
   - ✅ Patterns that are acceptable
   - ⚠️ Check: Are allowed edits specific enough?

3. **Safety Constraints**:
   - ✅ Rules that must NEVER be violated
   - ✅ Forbidden operations
   - ✅ Invariants to preserve
   - ⚠️ Check: Are constraints clear and verifiable?

4. **Testing Requirements**:
   - ✅ How to verify changes are correct
   - ✅ Required test coverage
   - ✅ Key scenarios to test
   - ⚠️ Check: Are testing requirements achievable?

5. **Dependencies & Integration**:
   - ✅ How this module interacts with others
   - ✅ Interface contracts
   - ⚠️ Check: Are integration points documented?

**Quality Assessment**:
- **Complete**: All required sections present with actionable guidance
- **Incomplete**: Missing 1-2 required sections
- **Minimal**: Generic guidance, not module-specific
- **Missing**: No AGENT_INSTRUCTION.md file

**Output**: List missing or incomplete sections with recommendations.

### 4. Meaning Parity Validation

**Definition**: Documentation MUST accurately reflect implemented behavior. No semantic drift.

#### API/Interface Parity Check

**For each documented API** (from README.md):
1. Extract function/class names, method signatures
2. Search for definitions in code
3. Compare documented vs actual signatures
4. Flag mismatches (wrong name, wrong parameters, missing function)

**Parity Statuses**:
- ✅ **Aligned**: Documented API exists and matches code
- ⚠️ **Partial Match**: API exists but signature differs
- ❌ **Missing in Code**: Documented but not implemented
- ❓ **Undocumented**: Exists in code but not in docs

#### Dependency Parity Check

**For each documented dependency** (from README.md or AGENT_INSTRUCTION.md):
1. Extract module dependencies
2. Parse actual imports from code files
3. Cross-reference documented vs actual
4. Flag undocumented dependencies
5. Flag documented but unused dependencies

**Output**: Dependency alignment report:
- Dependencies documented AND used ✅
- Used but not documented ⚠️
- Documented but not used ❓
- External dependencies not documented ⚠️

#### Example Validation

**For each code example** in README.md:
1. Extract code from markdown code blocks
2. Check if example APIs exist in current codebase
3. Verify import statements are correct
4. Flag outdated or broken examples

**Quality Levels**:
- ✅ All examples reference current APIs
- ⚠️ Some examples reference deprecated APIs
- ❌ Examples would not run (missing imports, wrong APIs)
- N/A No examples provided

#### Invariant Verification

**For each documented invariant**:
1. Identify the behavioral guarantee (e.g., "never returns null", "always validates input")
2. Search code for patterns that might violate it
3. Flag potential violations for human review

**Note**: This is heuristic-based detection, not formal verification. Flag potential issues for manual review.

**Output**: List of invariants with validation status:
- ✅ No obvious violations found
- ⚠️ Potential violation detected (requires human review)
- ❓ Cannot verify automatically (complex invariant)

### 5. Bounded Context Validation

#### Internal Boundary Check

**Verify module isolation**:
1. Identify "internal" or "private" subdirectories/files
2. Check if external modules import from internals
3. Flag boundary violations

**Violations**:
- External import from `module/internal/`
- External import from `module/_private.py`
- Direct access to non-public APIs

#### Cross-Module Dependency Analysis

**Build import graph**:
1. Parse imports for target module
2. Identify which external modules it depends on
3. Compare with documented dependencies
4. Flag undocumented cross-module dependencies

**Check for coupling issues**:
- **Tight Coupling**: Module directly modifies another module's state
- **Circular Dependencies**: Module A → B → A
- **Hidden Dependencies**: Imports not documented

**Output**: Dependency graph showing:
- Documented dependencies ✅
- Undocumented dependencies ⚠️
- Circular dependencies ❌
- Suggested decoupling opportunities

#### Interface Stability Check

**For public APIs** (exported functions/classes):
1. Identify public interface from code
2. Compare with documented interface
3. Flag undocumented public APIs
4. Check if interface is overly broad (exposes too much)

**Quality Indicators**:
- ✅ Small, focused public interface
- ⚠️ Large interface, may need refactoring
- ❌ Exposes internal implementation details

### 6. Testing Requirements Validation

**From AGENT_INSTRUCTION.md**:
1. Extract documented testing requirements
2. Check if test files exist
3. Verify test coverage aligns with requirements

**Validation Checks**:
- Are test files present? (e.g., `tests/`, `test_module.py`, `module.test.js`)
- Do tests cover key scenarios mentioned in AGENT_INSTRUCTION.md?
- Are testing requirements achievable with current test infrastructure?

**Output**: Testing compliance report:
- ✅ Tests exist and cover required scenarios
- ⚠️ Tests exist but incomplete coverage
- ❌ No tests found
- ❓ Cannot verify (testing requirements too vague)

### 7. Generate Validation Report

Output a detailed Markdown report:

```markdown
# Semantic Module Validation Report

**Module**: [module path]
**Validated**: [timestamp]

## Overall Status

- **Documentation**: [Complete/Incomplete/Missing]
- **Meaning Parity**: [Aligned/Drifted/Unknown]
- **Bounded Context**: [Compliant/Violations Found]
- **Testing**: [Adequate/Incomplete/Missing]

**Overall Grade**: [A/B/C/D/F]
- A: Fully compliant semantic module
- B: Minor issues, mostly compliant
- C: Significant issues, needs work
- D: Major problems, not functioning as semantic module
- F: Missing critical components

## Documentation Completeness

### README.md

**Status**: [Present/Missing]

| Section | Status | Notes |
|---------|--------|-------|
| Purpose | ✅ Complete | Clear and specific |
| Responsibilities | ⚠️ Incomplete | Missing scope boundaries |
| Invariants | ❌ Missing | Should document validation rules |
| API/Interface | ✅ Complete | Well documented |
| Dependencies | ⚠️ Partial | Missing external deps |
| Examples | ✅ Complete | Current and working |

**Recommendations**:
1. Add invariants section documenting validation rules
2. Complete dependencies section with external libraries

### AGENT_INSTRUCTION.md

**Status**: [Present/Missing]

| Section | Status | Notes |
|---------|--------|-------|
| Module Boundaries | ✅ Complete | Clear scope definition |
| Allowed Edits | ⚠️ Incomplete | Too vague, needs specific examples |
| Safety Constraints | ✅ Complete | Clear forbidden operations |
| Testing Requirements | ❌ Missing | No testing guidance provided |
| Dependencies & Integration | ✅ Complete | Well documented |

**Recommendations**:
1. Add specific examples to Allowed Edits section
2. Add Testing Requirements section with key scenarios

## Meaning Parity Analysis

### API Alignment

| Documented API | Code Status | Issue |
|----------------|-------------|-------|
| `authenticate(username, password)` | ✅ Match | None |
| `validateToken(token)` | ⚠️ Partial | Signature differs: `validateToken(token, options)` |
| `refreshToken(user)` | ❌ Missing | Not found in code |
| - | ❓ Undocumented | `revokeToken(token)` exists but not documented |

**Critical Drift**: 1 documented API not found in code
**Minor Drift**: 1 signature mismatch, 1 undocumented API

### Dependency Alignment

| Dependency | Documented | Used in Code | Status |
|------------|------------|--------------|--------|
| `crypto` (Node.js) | ✅ Yes | ✅ Yes | ✅ Aligned |
| `jsonwebtoken` | ❌ No | ✅ Yes | ⚠️ Undocumented |
| `bcrypt` | ✅ Yes | ❌ No | ❓ Documented but unused |

**Issues**:
- `jsonwebtoken` used but not documented in dependencies
- `bcrypt` documented but not found in imports (possibly removed?)

### Example Validation

- ✅ Example 1: Basic authentication - APIs current and correct
- ❌ Example 2: Token refresh - References removed `refreshToken()` function
- ✅ Example 3: Validation - Working correctly

**Broken Examples**: 1 (needs update to remove `refreshToken` reference)

## Bounded Context Analysis

### Boundary Compliance

**Internal Access Violations**: 0
**Undocumented Dependencies**: 1
- `src/auth/` imports `src/user/internal/validator.js` (should use public API)

### Dependency Graph

```
src/auth/
  ├─→ crypto (external, documented) ✅
  ├─→ jsonwebtoken (external, undocumented) ⚠️
  ├─→ src/config/ (internal, documented) ✅
  └─→ src/user/ (internal, documented) ✅
      └─→ src/user/internal/validator.js (boundary violation) ❌
```

**Circular Dependencies**: None detected ✅

**Coupling Issues**:
- Tight coupling with `src/user/` - accesses internal validator

**Recommendations**:
1. Use public API from `src/user/` instead of internal validator
2. Document `jsonwebtoken` dependency in README.md

## Testing Validation

**Test Files Found**: 
- ✅ `tests/auth/authenticate.test.js`
- ✅ `tests/auth/validate.test.js`

**AGENT_INSTRUCTION.md Testing Requirements**: 
- ❌ Not specified (missing section)

**Coverage Assessment**: 
- Cannot fully assess without documented testing requirements
- Existing tests appear to cover basic scenarios

**Recommendations**:
1. Add Testing Requirements section to AGENT_INSTRUCTION.md
2. Specify key scenarios that must be tested
3. Document edge cases requiring test coverage

## Action Items

### Priority 1: Fix Semantic Drift (CRITICAL)

1. **Remove or implement `refreshToken(user)` function**:
   - Either implement the documented function
   - Or remove from README.md Example 2

2. **Fix boundary violation**:
   - Change `src/user/internal/validator.js` import to use public API
   - Update AGENT_INSTRUCTION.md to forbid internal imports

### Priority 2: Complete Documentation (HIGH)

1. **README.md improvements**:
   - Add Invariants section documenting validation rules
   - Document `jsonwebtoken` dependency
   - Remove or clarify `bcrypt` dependency

2. **AGENT_INSTRUCTION.md improvements**:
   - Add Testing Requirements section
   - Add specific examples to Allowed Edits
   - Update signature for `validateToken()` function

### Priority 3: Improve Quality (MEDIUM)

1. **Document undocumented API**:
   - Add `revokeToken(token)` to README.md API section

2. **Update examples**:
   - Fix Example 2 to not reference removed function

## Validation Summary

**Strengths**:
- Clear module purpose and boundaries
- Good API documentation (mostly aligned with code)
- No circular dependencies
- Tests exist for core functionality

**Weaknesses**:
- Semantic drift: 1 missing function, 1 signature mismatch
- Boundary violation: accessing internal APIs
- Missing testing requirements in AGENT_INSTRUCTION.md
- Undocumented dependencies

**Overall Assessment**: Grade B - Mostly compliant semantic module with fixable issues

---

**Next Steps**:
1. Fix critical semantic drift issues (Priority 1)
2. Complete documentation gaps (Priority 2)
3. Re-run validation: `/speckit.semantic-validate src/auth/`
```

### 8. Offer Assistance

After presenting the report, offer to:

1. **Generate missing documentation sections**: Create templates for missing sections
2. **Create fix tasks**: Generate tasks.md entries for action items
3. **Draft updates**: Suggest specific wording for documentation fixes

Ask: "Would you like me to generate documentation templates for the missing sections? (yes/no)"

## Validation Heuristics

### API Detection Strategies

**For JavaScript/TypeScript**:
- Parse `export` statements
- Identify exported functions/classes
- Extract JSDoc/TSDoc signatures

**For Python**:
- Parse `__all__` if present
- Identify top-level functions/classes in `__init__.py`
- Look for public items (not starting with `_`)

**For Go**:
- Exported identifiers (start with capital letter)
- Parse function signatures from `.go` files

**For Java/C#**:
- Public classes and methods
- Parse package/namespace exports

### Dependency Detection

**Import Parsing**:
- JavaScript: `import`/`require` statements
- Python: `import`/`from` statements
- Go: `import` statements
- Java: `import` statements

**External vs Internal**:
- External: Third-party packages (from package.json, requirements.txt, go.mod, etc.)
- Internal: Relative imports or same-project modules

### Semantic Drift Scoring

**Severity Levels**:
- **CRITICAL**: Documented API doesn't exist (breaks usage)
- **HIGH**: Signature mismatch (could break usage)
- **MEDIUM**: Undocumented API exists (missing docs)
- **LOW**: Minor wording inconsistencies

**Drift Score**:
- 0 critical + 0 high = ✅ Aligned
- 1-2 high or 3-5 medium = ⚠️ Minor Drift
- 3+ high or 1+ critical = ❌ Significant Drift

## Token Efficiency

**Progressive Loading**:
- Load documentation files first (small)
- Parse code only for specific validation checks
- Don't dump entire file contents into context

**Focused Analysis**:
- Prioritize critical validations (drift, boundaries)
- Detailed analysis only when issues found
- Summarize passing checks briefly

**Compact Output**:
- Use tables for structured data
- Limit examples to top 5 issues per category
- Provide counts for large result sets

## Context

{ARGS}
