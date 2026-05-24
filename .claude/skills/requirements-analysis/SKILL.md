---
name: requirements-analysis
description: Analyzes project requirements and generates structured documentation. Use when starting a new project, clarifying scope, or creating README and PRD documents.
---

# Requirements Analysis

## When to Use

- Starting a new project
- Clarifying ambiguous requirements
- Generating README.md or PRD

## Workflow
```
Task Progress:
- [ ] Step 1: Gather context (user input, existing docs)
- [ ] Step 2: Identify core problem and goals
- [ ] Step 3: Define scope (in/out)
- [ ] Step 4: List functional requirements
- [ ] Step 5: List non-functional requirements
- [ ] Step 6: Identify constraints and assumptions
- [ ] Step 7: Generate output document
```

## Key Questions to Answer

1. **Problem**: What problem does this solve? For whom?
2. **Goals**: What does success look like?
3. **Scope**: What is explicitly included/excluded?
4. **Users**: Who are the primary users?
5. **Constraints**: Timeline, budget, technical limitations?

## Output Format

Generate a structured document with:
```markdown
# Project Name

## Problem Statement
[One paragraph describing the core problem]

## Goals
- Goal 1
- Goal 2

## Scope
### In Scope
- ...

### Out of Scope
- ...

## Functional Requirements
- FR1: ...
- FR2: ...

## Non-Functional Requirements
- NFR1: ...
- NFR2: ...

## Constraints & Assumptions
- ...
```

## Validation

Before finalizing, verify:
- [ ] Problem statement is clear and specific
- [ ] Goals are measurable
- [ ] Scope boundaries are explicit
- [ ] Requirements are testable
- [ ] No ambiguous terms without definition
