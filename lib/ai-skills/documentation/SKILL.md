
---
name: Documentation Generator
description: Generate comprehensive documentation from source code including API docs and architecture guides.
---

# Documentation Generator Skill

Produce clear, accurate documentation that helps developers understand and use the codebase.

## API Documentation

- **JSDoc (JavaScript/TypeScript)**: Use `@param`, `@returns`, `@throws`, `@example` for functions. Document generic parameters and overloads. Generate with TypeDoc or JSDoc.
- **Docstrings (Python)**: Follow Google, NumPy, or Sphinx style. Include Args, Returns, Raises, and Examples. Use type hints alongside docstrings.
- **Go doc**: Place comments above exported symbols. First sentence becomes the summary. Use `go doc` or godoc.
- **Rust doc**: Use `///` for items, `//!` for module-level docs. Include `# Examples` and `# Panics` sections. Use `cargo doc`.

## README Templates

- **Project overview**: Purpose, key features, and target audience.
- **Quick start**: Installation, minimal setup, and "hello world" example.
- **Configuration**: Env vars, config files, and important options.
- **Usage**: Common workflows, CLI usage, or API usage examples.
- **Contributing**: How to build, test, and submit changes.
- **License**: SPDX identifier and attribution.

## Architecture Guides

- Describe high-level components: services, layers, and data flow.
- Document design decisions (ADRs) for significant choices.
- Include sequence diagrams for critical flows (auth, checkout, etc.).
- Map dependencies between modules and external systems.

## Architecture Diagrams

- Use Mermaid, PlantUML, or ASCII for diagrams in Markdown.
- Show component relationships, data flow, and deployment topology.
- Keep diagrams up to date with code; consider generating from annotations or config.

Produce documentation that is accurate, discoverable, and maintainable. Prefer automation (doc generators) where the language ecosystem supports it.
