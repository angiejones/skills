# .instructions.md Template

This file goes in a directory to provide context for that specific area. Create one in key directories like `src/components/`, `lib/`, `src/pages/`, etc.

---

# Instructions for [Directory Name]

**Purpose**: What code goes in this directory and why.

Example:

> This directory contains all React components for the dashboard. Components here should be reusable, stateless UI building blocks that accept data via props and handle user interactions through callbacks.

## Structure

```
./
├── Button/
│   ├── Button.tsx
│   ├── Button.test.tsx
│   └── Button.stories.tsx
├── Modal/
│   ├── Modal.tsx
│   ├── Modal.test.tsx
│   └── Modal.stories.tsx
└── index.ts  # Export all components
```

## Key Patterns

**Do**:

- Keep components focused on a single responsibility
- Accept data via props, emit events via callbacks
- Use TypeScript for all props (`React.FC<Props>`)

**Don't**:

- Make direct API calls (use custom hooks instead)
- Store global state (use Redux)
- Add business logic (keep it in `../services/`)

## Common Tasks

### Creating a new component

1. Create directory with component name
2. Create `.tsx`, `.test.tsx`, and `.stories.tsx` files
3. Export from `index.ts`
4. Add to component library documentation

### Testing components

- Use `@testing-library/react` for testing
- Test user interactions, not implementation
- Mock external dependencies (API calls, Redux)

### Styling

- Use CSS modules: `Component.module.css`
- Follow the project's design system
- Mobile-first approach

## References

See [../AGENTS.md](../AGENTS.md) for general project context.
