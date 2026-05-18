---
name: task-planning
description: Breaks down architecture into actionable development tasks. Use when creating implementation plans, sprint backlogs, or task sequences with dependencies.
---

# Task Planning

## When to Use

- Breaking architecture into development tasks
- Creating implementation roadmap
- Prioritizing and sequencing work

## Prerequisites

- Completed architecture design document

## Workflow
```
Task Progress:
- [ ] Step 1: Review architecture document
- [ ] Step 2: Identify major milestones
- [ ] Step 3: Break milestones into tasks
- [ ] Step 4: Estimate complexity (S/M/L)
- [ ] Step 5: Identify dependencies
- [ ] Step 6: Sequence tasks
- [ ] Step 7: Define acceptance criteria per task
```

## Task Breakdown Principles

1. **Single responsibility**: One task = one deliverable
2. **Testable**: Each task has clear acceptance criteria
3. **Right-sized**: Completable in 1-4 hours ideally
4. **Independent**: Minimize dependencies where possible

## Output Format
```markdown
# Implementation Plan

## Milestones Overview

| # | Milestone | Description | Tasks |
|---|-----------|-------------|-------|
| M1 | ... | ... | T1-T3 |
| M2 | ... | ... | T4-T7 |

## Task Details

### T1: [Task Title]
- **Milestone**: M1
- **Complexity**: S/M/L
- **Dependencies**: None | T#
- **Description**: [What to implement]
- **Acceptance Criteria**:
  - [ ] Criterion 1
  - [ ] Criterion 2
- **Files to Create/Modify**:
  - `path/to/file.ts`

### T2: [Task Title]
...

## Dependency Graph
```
T1 → T2 → T4
↓
T3 → T5
```

## Suggested Sequence

1. T1 (no dependencies)
2. T2, T3 (parallel, depend on T1)
3. ...
```

## Validation

Before finalizing:
- [ ] All architecture components covered
- [ ] No circular dependencies
- [ ] Each task has acceptance criteria
- [ ] Complexity estimates provided
- [ ] Critical path identified
