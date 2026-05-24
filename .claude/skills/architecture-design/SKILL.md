---
name: architecture-design
description: Designs system architecture based on requirements. Use when creating technical architecture, selecting tech stack, or defining system components and their interactions.
---

# Architecture Design

## When to Use

- Designing new system architecture
- Evaluating tech stack choices
- Documenting system components and data flow

## Prerequisites

- Completed requirements analysis (README.md or PRD)

## Workflow
```
Task Progress:
- [ ] Step 1: Review requirements document
- [ ] Step 2: Identify key architectural drivers
- [ ] Step 3: Evaluate and select tech stack
- [ ] Step 4: Define system components
- [ ] Step 5: Design data models
- [ ] Step 6: Map component interactions
- [ ] Step 7: Document decisions (ADR format)
- [ ] Step 8: Identify risks and mitigations
```

## Key Considerations

1. **Drivers**: What requirements most impact architecture?
2. **Trade-offs**: What are we optimizing for? (speed, cost, scalability)
3. **Constraints**: What technical limitations exist?
4. **Integration**: What external systems must we connect to?

## Output Format
```markdown
# Architecture Design

## Overview
[High-level system description]

## Tech Stack
| Layer | Choice | Rationale |
|-------|--------|-----------|
| Frontend | ... | ... |
| Backend | ... | ... |
| Database | ... | ... |
| Deployment | ... | ... |

## System Components
[Component diagram or description]

## Data Models
[Core entities and relationships]

## Architecture Decision Records

### ADR-001: [Decision Title]
- **Status**: Accepted
- **Context**: [Why this decision was needed]
- **Decision**: [What was decided]
- **Consequences**: [Trade-offs and implications]

## Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| ... | ... | ... |
```

## Validation

Before finalizing:
- [ ] All architectural drivers addressed
- [ ] Tech choices justified with rationale
- [ ] Component boundaries clear
- [ ] Data flow documented
- [ ] Key decisions recorded as ADRs
