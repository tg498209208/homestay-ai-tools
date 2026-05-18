---
name: testing
description: Test strategy and planning methodology. Use when designing test plans, identifying test cases, or establishing testing approach for a project.
---

# Testing

## When to Use

- Designing test strategy for new features
- Identifying test cases from requirements
- Planning test coverage

## Workflow
```
Task Progress:
- [ ] Step 1: Review requirements and acceptance criteria
- [ ] Step 2: Identify test levels needed
- [ ] Step 3: Define test cases per requirement
- [ ] Step 4: Identify edge cases and error scenarios
- [ ] Step 5: Prioritize tests by risk
- [ ] Step 6: Document test plan
```

## Test Levels

| Level | Purpose | When to Use |
|-------|---------|-------------|
| Unit | Single function/component | Core logic |
| Integration | Component interactions | API, database |
| E2E | Full user flows | Critical paths |

## Test Case Design

For each requirement, identify:

1. **Happy path**: Expected normal behavior
2. **Edge cases**: Boundary conditions
3. **Error cases**: Invalid inputs, failures
4. **Security cases**: Auth, permissions (if applicable)

## Output Format
```markdown
# Test Plan

## Overview
- **Feature**: [What is being tested]
- **Risk Level**: High / Medium / Low

## Test Cases

### [Requirement ID]: [Requirement Description]

| ID | Scenario | Input | Expected | Priority |
|----|----------|-------|----------|----------|
| T1 | Happy path | ... | ... | P0 |
| T2 | Edge case | ... | ... | P1 |
| T3 | Error case | ... | ... | P1 |

## Coverage Summary

| Level | Planned | Notes |
|-------|---------|-------|
| Unit | Yes/No | ... |
| Integration | Yes/No | ... |
| E2E | Yes/No | ... |
```

## Validation

Before finalizing:
- [ ] All requirements have test cases
- [ ] Happy path + edge cases + error cases covered
- [ ] Priorities assigned by risk
- [ ] Test levels appropriate to project needs
