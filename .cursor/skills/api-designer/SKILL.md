

---
name: API Designer
description: Design and document RESTful API endpoints following OpenAPI standards.
---

# API Designer Skill

Design and document RESTful APIs that are consistent, predictable, and well-documented.

## REST Conventions

- Use nouns for resources (e.g., `/users`, `/orders`), verbs for actions only when necessary (e.g., `/orders/{id}/cancel`).
- Prefer plural resource names. Use kebab-case or camelCase consistently per project convention.
- Apply HTTP methods correctly: GET (read), POST (create), PUT (replace), PATCH (partial update), DELETE (remove).

## Status Codes

- 200 OK: Successful GET, PUT, PATCH.
- 201 Created: Successful POST with Location header for new resource.
- 204 No Content: Successful DELETE or update with no body.
- 400 Bad Request: Validation errors, malformed input.
- 401 Unauthorized: Missing or invalid authentication.
- 403 Forbidden: Authenticated but not authorized.
- 404 Not Found: Resource does not exist.
- 409 Conflict: State conflict (e.g., duplicate, version mismatch).
- 422 Unprocessable Entity: Semantic validation failures.
- 500 Internal Server Error: Unexpected server errors.

## Pagination Patterns

- Use `limit` and `offset` or `page` and `page_size` for list endpoints.
- Return metadata: `total`, `has_next`, `next_cursor` where applicable.
- Prefer cursor-based pagination for large, frequently changing datasets.
- Document default and max page sizes in OpenAPI.

## OpenAPI Output

Produce valid OpenAPI 3.x specs with schemas, examples, error responses, and security schemes. Include request/response examples for each endpoint.
