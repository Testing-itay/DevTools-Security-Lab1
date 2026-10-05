# DevTools Engine — Codex Project Instructions

You are working on **devtools-engine**, a multi-service AI development platform for code analysis, agent orchestration, and developer tool management.

## Project Overview

- **Python API** (FastAPI): REST/GraphQL APIs, ML model serving
- **Node.js Services** (Express): Real-time orchestration, WebSocket handlers
- **Go Scanner** (Gin): Security and code analysis
- **Java Analytics** (Spring Boot): Metrics, reporting, aggregation
- **C# Core** (ASP.NET Core): Business logic, plugin framework
- **Rust CLI**: Fast developer tooling

## Coding Standards

1. **Style**: Follow language-specific style guides (PEP 8 for Python, standard Go formatting, etc.).
2. **Naming**: Use descriptive names. Prefer `snake_case` in Python, `camelCase` in TypeScript/Java/C#, `PascalCase` for public types.
3. **Documentation**: Add docstrings/comments for public APIs and non-obvious logic.
4. **Error handling**: Use appropriate error types; avoid silent failures.

## Preferred Patterns

- **Async/await** where supported (Python, TypeScript, Rust).
- **Dependency injection** for testability (Spring, ASP.NET Core).
- **Structured logging** with correlation IDs for tracing.
- **Configuration via environment** — no hardcoded secrets.

## Testing Requirements

- Unit tests for business logic.
- Integration tests for API endpoints and service boundaries.
- Aim for meaningful coverage; avoid tests that only assert implementation details.

## Project Conventions

- Keep services loosely coupled; communicate via well-defined APIs.
- Prefer small, focused modules over large monoliths.
- Use existing patterns in the codebase when extending functionality.
