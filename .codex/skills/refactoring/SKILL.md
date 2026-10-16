

---
name: Refactoring Assistant
description: Suggest and apply code refactoring patterns to improve code quality.
---

# Refactoring Assistant Skill

Guide and execute refactoring to improve readability, maintainability, and adherence to design principles.

## Code Smells to Address

- **Long methods**: Extract into smaller, well-named functions. Aim for single responsibility per function.
- **Large classes**: Split by responsibility. Consider composition over inheritance.
- **Duplicate code**: Extract common logic into shared functions or base classes. Apply DRY.
- **Long parameter lists**: Introduce parameter objects or builder patterns.
- **Feature envy**: Move behavior to the class that owns the data.
- **Primitive obsession**: Replace primitives with value objects for domain concepts.
- **Speculative generality**: Remove unused abstractions; YAGNI.

## Design Patterns

- **Strategy**: Extract varying algorithms into interchangeable strategies.
- **Factory/Builder**: Simplify object creation with complex setup.
- **Observer/Event**: Decouple producers from consumers for event-driven flows.
- **Repository**: Abstract data access for testability and flexibility.
- **Decorator**: Add behavior without subclassing. Use for cross-cutting concerns.

## SOLID Principles

- **S**ingle Responsibility: One reason to change per class/module.
- **O**pen/Closed: Extend via new code, not modification of existing code.
- **L**iskov Substitution: Subtypes must be substitutable for their base types.
- **I**nterface Segregation: Prefer many specific interfaces over one general one.
- **D**ependency Inversion: Depend on abstractions, not concretions. Inject dependencies.

## Workflow

Propose refactorings in small, incremental steps. Ensure tests pass after each step. Prefer automated refactorings (rename, extract method) where the IDE supports them. Document the rationale for each change.
