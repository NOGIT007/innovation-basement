# Testing Rules

_Loaded when working on test files_

## Test Structure

- One test file per source file: `foo.ts` → `foo.test.ts`
- Use `describe` blocks for grouping related tests
- Test names should describe behavior: "should [action] when [condition]"

## Mocking

- Mock at module boundaries, not internal functions
- Reset mocks in `beforeEach` or `afterEach`
- Prefer dependency injection over module mocking

## Assertions

- One logical assertion per test
- Use specific matchers (`toHaveBeenCalledWith` over `toHaveBeenCalled`)
- Test error cases explicitly

## Coverage

- Focus on critical paths, not percentages
- Integration tests for API endpoints
- Unit tests for business logic
