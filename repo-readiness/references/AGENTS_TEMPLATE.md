# AGENTS.md Template

This file provides essential context for AI agents working with your codebase. Copy this template and customize it for your project.

---

# [Your Project Name]

**One-line description**: A brief summary of what this project does.

## Project Overview

Provide a clear explanation of:

- What problem this project solves
- Key use cases and stakeholders
- High-level architecture or structure

## Structure

Describe the main directories and their purposes:

```
src/
  └── component/  - React components and UI logic
lib/
  └── utils/      - Shared utility functions
tests/            - Test suite
docs/             - Documentation
```

## Key Technologies & Patterns

- **Framework**: [e.g., React 18, Express.js]
- **Language**: [e.g., TypeScript, Python]
- **Key Libraries**: [e.g., Redux, Prisma, Django ORM]
- **Testing**: [e.g., Jest, Pytest]

## Domain Knowledge

### Business Context

[Explain the domain: Is this a payments system? A content platform? An analytics tool?]

### Critical Constraints

[What must be true? What must never happen? Performance requirements? Security considerations?]

### Common Workflows

[How do developers typically work with this code?]

## Development Conventions

### Code Style

- Naming conventions: [camelCase for variables, PascalCase for components, UPPER_SNAKE_CASE for constants]
- File organization: [One component per file, tests colocated]
- Error handling: [Exceptions vs. Result types; how to handle errors]

### Architectural Decisions

[Important patterns and why they were chosen. This helps AI understand the codebase intent.]

Example:

- We use composition over inheritance for flexibility
- All state is managed in Redux (not local component state)
- Async operations use async/await with Promises

### Forbidden Patterns

[What should AI avoid suggesting?]

Example:

- Don't import styles directly; use CSS modules
- Don't modify global state outside Redux
- Don't use `eval()` or `new Function()`

## How to Run Locally

```bash
npm install
npm run dev
npm test
```

## Important Files & Their Purposes

- `package.json` — Dependencies and scripts
- `tsconfig.json` — TypeScript configuration
- `.eslintrc` — Code quality rules
- `README.md` — User-facing documentation

## Getting Help

[Where should AI agents look for answers? Docs folder? Comments? Specific files?]

---

## When to Update This File

- When project structure significantly changes
- When adding major new domains or services
- Quarterly review to keep knowledge current
