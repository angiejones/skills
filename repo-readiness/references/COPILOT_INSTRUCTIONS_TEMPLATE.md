# copilot-instructions.md Template

This file provides rules and constraints for AI when working with your repository. It's like `.gitignore` for AI behavior. Copy this template and customize it for your project.

---

# AI Instructions for [Your Project Name]

These instructions guide AI assistants (GitHub Copilot, Claude, etc.) on how to work effectively with this codebase.

## Code Quality Standards

### Must Follow

- Run tests before suggesting changes: `npm test`
- All new code must have TypeScript types (no `any`)
- All public functions must have JSDoc comments
- Follow the project's ESLint configuration
- Use async/await, not callbacks

### Should Consider

- Performance implications for large datasets
- Accessibility (WCAG) for UI components
- Security implications for user data handling

### Avoid Suggesting

- Disabling linter rules without explanation
- Hardcoded values (use environment variables instead)
- `setTimeout` for synchronization (use Promises)
- Inline styles (use CSS modules)

## Architecture & Patterns

### Naming Conventions

- Component files: `PascalCase.tsx`
- Utilities: `camelCase.ts`
- Constants: `UPPER_SNAKE_CASE`
- Private methods: prefix with `_`

### State Management

- Global state: Redux with slices
- Component state: React hooks only
- API data: Managed in Redux slices, not local state
- UI state (modals, dropdowns): Local state is OK

### File Organization

```
src/features/
  └── auth/
      ├── components/     - React components
      ├── hooks/          - Custom hooks
      ├── services/       - API calls and business logic
      ├── store/          - Redux slice
      └── types.ts        - TypeScript types
```

### Error Handling

- All API calls should have error boundaries
- Throw `Error` with descriptive message (not strings)
- Log errors to monitoring service (Sentry, etc.)
- Show user-friendly error messages, not stack traces

## Common Tasks & How to Approach Them

### Adding a New API Endpoint

1. Create a new Redux slice in `store/`
2. Add action creators and reducers
3. Create a service file in `services/`
4. Create component that uses the hook
5. Add tests for the slice, service, and component

### Adding a New Component

1. Create component file in `components/`
2. Add TypeScript types
3. Add JSDoc comment
4. Create `.test.tsx` file with 3+ test cases
5. Export from `index.ts`

### Refactoring Existing Code

1. Run tests first to establish baseline
2. Refactor with tests passing
3. Update types if structure changes
4. Update AGENTS.md if patterns change

## What NOT to Do

❌ Don't modify `redux/store.ts` directly — add new slices instead  
❌ Don't add new dependencies without checking with the team  
❌ Don't disable TypeScript strict mode  
❌ Don't commit node_modules or build artifacts  
❌ Don't hardcode API URLs (use environment variables)  
❌ Don't modify other developers' commented code

## Testing Requirements

- Minimum 80% code coverage
- All public functions must have unit tests
- All user interactions must have integration tests
- API errors must be tested
- Run `npm test -- --coverage` before submitting

## Performance Guidelines

- Bundle size: Keep under 100KB (gzipped)
- Render time: Components should render in <16ms
- API response time: Aim for <200ms
- Lazy load large components
- Memoize expensive computations

## Security Considerations

- Never log user PII or passwords
- Always escape user input for HTML
- Use HTTPS for all API calls
- Validate input on both client and server
- Use environment variables for secrets (never commit `.env`)
- Check OWASP guidelines for auth features

## Documentation Requirements

- README.md explains how to run the project
- Complex functions have comments explaining _why_, not just _what_
- Architecture decisions are documented in AGENTS.md
- Breaking changes require CHANGELOG entry

## Questions?

Refer to:

- **AGENTS.md** for project context and patterns
- **docs/** folder for detailed guides
- **README.md** for getting started
- GitHub issues for project decisions

---

Last updated: [DATE]
