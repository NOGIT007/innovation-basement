# Git Rules

_Loaded when working with version control_

## Commit Format

- Use conventional commits: `type(scope): description`
- Types: feat, fix, docs, refactor, test, chore
- Keep subject line under 72 characters
- Body explains "why", not "what"

## Branch Naming

- Feature: `feat/issue-number-short-description`
- Fix: `fix/issue-number-short-description`
- Keep branch names under 50 characters

## Workflow

- One feature per branch
- Squash commits before merge (unless history matters)
- Delete branches after merge

## Code Review

- Small PRs (< 400 lines changed)
- Include test coverage
- Link to related issues
