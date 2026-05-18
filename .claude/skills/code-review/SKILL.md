---
name: code-review
description: Structured code review methodology. Use when reviewing code changes, pull requests, or auditing existing code for quality and issues.
---

# Code Review

## When to Use

- Reviewing code changes or PRs
- Auditing existing code quality
- Pre-commit self-review

## Workflow
```
Task Progress:
- [ ] Step 1: Understand context (what and why)
- [ ] Step 2: Check correctness (does it work?)
- [ ] Step 3: Check maintainability (is it clear?)
- [ ] Step 4: Check edge cases and errors
- [ ] Step 5: Check security implications
- [ ] Step 6: Provide actionable feedback
```

## Review Priorities

| Priority | Focus |
|----------|-------|
| P0 | Bugs, security issues, data loss risks |
| P1 | Logic errors, missing edge cases |
| P2 | Maintainability, clarity |
| P3 | Style, naming, minor improvements |

## Output Format
```markdown
## Review Summary

**Context**: [What this change does]
**Verdict**: Approve / Request Changes / Needs Discussion

## Issues Found

### P0 (Blocking)
- [ ] [File:Line] Description of issue

### P1 (Important)
- [ ] [File:Line] Description of issue

### P2/P3 (Suggestions)
- [ ] [File:Line] Description of suggestion

## What's Good
- [Positive observations]
```

## Pre-Push Checklist

Before pushing code to remote (especially for CI/CD deployment):
- [ ] Run `npm run build` locally to verify all dependencies are committed
- [ ] Check for missing imports from new files/directories
- [ ] Verify all modified files are staged (`git status`)
- [ ] Ensure shared hooks, utilities, and components are tracked

**Common CI Build Failures:**
| Issue | Root Cause | Prevention |
|-------|------------|------------|
| Module not found | File exists locally but not committed | `git status` before push |
| Export errors | Named vs default export mismatch | Verify export syntax matches imports |
| TypeScript errors | Files with `@ts-nocheck` removed or new type errors | Run `npm run type-check` |

## Validation

Before submitting review:
- [ ] Understood the intent before critiquing
- [ ] Issues prioritized by severity
- [ ] Feedback is specific and actionable
- [ ] Tone is constructive
