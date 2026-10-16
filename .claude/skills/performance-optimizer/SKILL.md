

---
name: Performance Optimizer
description: Identify and fix performance bottlenecks in application code.
---

# Performance Optimizer Skill

Systematically identify and resolve performance issues to improve latency, throughput, and resource usage.

## Profiling Approach

- Identify hot paths: database queries, external API calls, CPU-intensive computations, and I/O operations.
- Use language-specific profilers (cProfile, Node.js --inspect, Go pprof) to gather baseline metrics.
- Focus on the 80/20 rule: optimize the small fraction of code causing most of the delay.

## Caching Strategies

- **Application cache**: In-memory (Redis, Memcached) for frequently accessed, rarely changing data.
- **HTTP cache**: ETag, Cache-Control headers for static and semi-static responses.
- **Query cache**: Cache expensive DB queries with appropriate TTL and invalidation.
- **Computation cache**: Memoize pure functions with deterministic inputs.
- Document cache invalidation rules to avoid stale data.

## Query Optimization

- Eliminate N+1 queries: use batch loading, JOINs, or eager loading.
- Add indexes for filter, sort, and join columns. Avoid over-indexing write-heavy tables.
- Use EXPLAIN/EXPLAIN ANALYZE to verify query plans. Optimize slow queries before adding indexes.
- Consider read replicas or connection pooling for high concurrency.

## Lazy Loading and Deferral

- Defer non-critical work: background jobs, async processing, and queue-based architectures.
- Lazy-load large resources (images, modules) when needed. Use code splitting in frontend bundles.
- Stream large responses instead of buffering in memory.

## Output

Provide concrete code changes with before/after metrics where possible. Prioritize high-impact, low-risk optimizations.
