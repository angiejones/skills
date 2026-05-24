# SKILL.md Template

This file documents a repeatable workflow or expert pattern that AI should follow. Create one for complex, multi-step procedures in your codebase.

Example use cases:

- "How to add a new feature"
- "The migration workflow"
- "Code review checklist"
- "Deployment procedure"
- "How to add a new permission"

---

---

name: skill-name
description: One-line description of when to use this pattern. Include the most common user phrases that should trigger this skill.

---

# [Workflow Name]

## When to use

Describe when an AI (or developer) should follow this pattern. Be specific:

- Adding a new payment method
- Migrating the database schema
- Setting up a new environment

## Overview

Provide a high-level explanation of why this workflow exists and what it accomplishes.

## Step-by-step workflow

### Step 1: [Action]

What to do and why.

Example:

```bash
npm run lint
```

### Step 2: [Action]

More details.

### Step 3: [Action]

Final steps.

## Checklist

Use this to verify completion:

- [ ] All tests passing
- [ ] Code reviewed
- [ ] Documentation updated

## Common mistakes

- ❌ **Mistake**: Forgetting to update the schema migration
  - **Why it breaks**: Database and code get out of sync
  - **How to fix**: Always generate migrations before writing code that depends on them

- ❌ **Mistake**: Skipping the integration tests
  - **Why it breaks**: Features work in isolation but fail in production
  - **How to fix**: Run the full test suite before committing

## Examples

### Good Example

[Show a real example from the repo]

### What not to do

[Show a counterexample]

## Related

See also:

- [Related workflow](./other-workflow.md)
- [Reference docs](../AGENTS.md)

---

## Tips for using this skill

**When creating new SKILLs:**

- Document workflows that take 5+ steps
- Focus on things that vary significantly between developers
- Update yearly as the project evolves
- Keep them <500 lines (shorter is better)

**When following SKILLs:**

- Read the full workflow before starting
- Check the "Common mistakes" section
- Ask for clarification if steps are unclear
