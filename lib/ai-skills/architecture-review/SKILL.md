


---
name: Architecture Review
description: Analyze system architecture and suggest improvements for scalability and maintainability.
---

# Architecture Review Skill

Evaluate system design and recommend changes to improve scalability, maintainability, and resilience.

## Microservices Patterns

- **Bounded contexts**: Ensure each service owns a clear domain. Avoid shared databases; prefer APIs or events for cross-service communication.
- **API gateway**: Centralize auth, rate limiting, and routing. Keep services behind the gateway.
- **Event-driven**: Use message queues or event buses for async, decoupled communication. Design for eventual consistency where appropriate.
- **Service discovery**: Support dynamic registration and discovery for deployment flexibility.
- **Circuit breaker**: Isolate failing dependencies to prevent cascading failures.

## Coupling Analysis

- **Afferent coupling**: Count incoming dependencies. High afferent = stable core; changes have wide impact.
- **Efferent coupling**: Count outgoing dependencies. High efferent = fragile; depends on many external modules.
- **Instability**: I = Ce / (Ca + Ce). Prefer stable cores (low I) and flexible peripheries (high I).
- Identify cyclic dependencies and recommend breaking cycles via interfaces or new modules.

## Dependency Graphs

- Build a dependency graph of modules, packages, or services. Use tools (e.g., madge, jdeps, cargo-deps) or static analysis.
- Identify critical paths, bottlenecks, and single points of failure.
- Recommend layering (e.g., presentation → application → domain → infrastructure) and enforce dependency direction.

## Scalability Considerations

- **Horizontal scaling**: Stateless services, shared-nothing design, idempotent operations.
- **Data partitioning**: Sharding, partitioning by tenant or region. Avoid hot spots.
- **Caching**: Edge, application, and data-layer caching. Define invalidation strategies.
- **Async processing**: Offload heavy work to queues. Use backpressure and rate limiting.

## Output

Provide a structured review: current state summary, identified issues with severity, recommended changes with rationale, and a prioritized action plan. Include diagrams where they clarify the analysis.
