

---
name: Test Generator
description: Generate comprehensive unit tests for functions and classes.
allowed-tools: Read, Write, Shell
---

# Test Generator Skill

Generate high-quality unit tests that maximize coverage and confidence in the codebase.

## Test Generation Strategies

1. **Input Partitioning**: Identify equivalence classes and boundary values. Test empty inputs, single items, max-size collections, and invalid types.

2. **State Coverage**: For stateful objects, test initialization, transitions, and terminal states. Cover happy path and all error branches.

3. **Mocking Patterns**: Mock external dependencies (HTTP, DB, file system) at boundaries. Use dependency injection to enable test doubles. Avoid over-mocking; prefer real objects for pure logic.

4. **Assertions**: Use descriptive assertion messages. Prefer specific matchers (e.g., `toThrowWithMessage`) over generic ones. Assert on observable behavior, not implementation details.

## Coverage Targets

- Aim for 80%+ line coverage on business logic; 100% on critical paths (auth, payments, data integrity).
- Prioritize branch coverage over line coverage for complex conditionals.
- Use **Read** to understand the function/class under test, **Write** to create test files, and **Shell** to run the test suite and verify results.

## Output Format

- Place tests in the project's standard test directory (e.g., `tests/`, `__tests__/`, `*.test.ts`).
- Follow existing test naming and structure conventions.
- Include setup/teardown where needed and ensure tests are isolated and repeatable.
