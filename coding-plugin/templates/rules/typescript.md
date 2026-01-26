# TypeScript Rules

_Loaded when working on .ts/.tsx files_

## Type Conventions

- Prefer `interface` over `type` for object shapes
- Use `type` for unions, intersections, and utility types
- Avoid `any` - use `unknown` with type guards instead
- Export types from dedicated `types.ts` files

## Import Patterns

- Group imports: external → internal → relative
- Use path aliases (`@/`) for deep imports
- Prefer named exports over default exports

## Naming

- Interfaces: PascalCase, no `I` prefix
- Types: PascalCase
- Constants: UPPER_SNAKE_CASE
- Functions: camelCase, verb prefix (get, set, handle, etc.)

## Async/Await

- Always handle errors with try/catch
- Prefer `Promise.all` for parallel operations
- Use `Promise.allSettled` when partial failures are acceptable
