

---
name: Code Translator
description: Translate code between programming languages while preserving logic and idioms.
---

# Code Translator Skill

Translate code accurately between languages while respecting idiomatic patterns and type systems.

## Language-Specific Patterns

- **Python ↔ TypeScript**: Generators vs. async iterators, list comprehensions vs. map/filter, decorators vs. higher-order functions.
- **Python ↔ Go**: Error handling (exceptions vs. explicit error returns), goroutines vs. asyncio, interfaces vs. duck typing.
- **Java ↔ C#**: Similar syntax but different ecosystems (Maven vs. NuGet, Spring vs. ASP.NET). Map annotations and attributes carefully.
- **Rust ↔ C/C++**: Ownership, borrowing, and lifetimes have no direct equivalent; translate to manual memory management or smart pointers where appropriate.

## Type Mapping

- Map primitive types: int ↔ number ↔ int32, string ↔ str ↔ String, bool ↔ boolean ↔ bool.
- Handle nullable types: Optional[T] ↔ T | null ↔ Option<T>. Preserve null-safety semantics.
- Translate collections: list ↔ Array ↔ Vec, dict ↔ Record/Map ↔ HashMap. Note ordering and mutability differences.
- Map custom types: classes, structs, interfaces, and enums. Preserve inheritance and composition relationships.

## Error Handling Translation

- **Exceptions → Result types**: Python/Java exceptions to Go `(value, error)` or Rust `Result<T, E>`.
- **Result types → Exceptions**: Rust/Go patterns to try/catch where exceptions are idiomatic.
- Preserve error propagation and context. Map custom error types to equivalent constructs.

## Output

Produce working, idiomatic code in the target language. Include comments for non-obvious translations. Preserve original logic, edge cases, and performance characteristics where possible. Note any platform or library differences that may affect behavior.
