


---
name: Code Review
description: Review code for bugs, security issues, and best practices.
allowed-tools: Read, Grep, Glob
---

# Code Review Skill

When invoked, systematically analyze the target codebase for quality, correctness, and maintainability.

## Analysis Checklist

1. **Bug Detection**: Look for off-by-one errors, null/undefined dereferences, race conditions, and improper error handling. Trace control flow for edge cases and boundary conditions.

2. **Security Issues**: Identify SQL injection, XSS, CSRF, insecure deserialization, hardcoded secrets, and improper authentication/authorization. Check input validation and output encoding.

3. **Best Practices**: Verify naming conventions, DRY violations, appropriate use of design patterns, and adherence to language/framework idioms. Flag magic numbers and unclear abstractions.

4. **Performance**: Spot N+1 queries, unnecessary allocations, blocking I/O in async paths, and inefficient algorithms. Suggest caching or batching where appropriate.

5. **Maintainability**: Assess testability, coupling, cohesion, and documentation. Recommend extracting complex logic into well-named functions or modules.

## Workflow

- Use **Read** to load the files under review.
- Use **Grep** to search for patterns (e.g., `eval`, `exec`, `dangerouslySetInnerHTML`, `password`, `secret`).
- Use **Glob** to discover related files (tests, configs, dependencies) for context.
- Provide actionable, prioritized feedback with file:line references and concrete suggestions.
