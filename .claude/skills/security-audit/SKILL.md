
---
name: Security Audit
description: Perform comprehensive security audits on application code.
allowed-tools: Read, Grep, Glob, Shell
---

# Security Audit Skill

Conduct thorough security reviews to identify vulnerabilities and recommend mitigations.

## OWASP Top 10 Focus

1. **Injection**: SQL, NoSQL, OS command, LDAP. Check parameterized queries, input sanitization, and least-privilege execution.
2. **Broken Authentication**: Weak passwords, session fixation, credential stuffing. Verify token handling, MFA, and session invalidation.
3. **Sensitive Data Exposure**: Unencrypted storage, logging of PII, weak TLS. Audit logging, error messages, and data at rest.
4. **XML External Entities (XXE)**: Disable external entities in XML parsers.
5. **Broken Access Control**: IDOR, privilege escalation, missing authorization checks. Enforce RBAC/ABAC at every endpoint.
6. **Security Misconfiguration**: Default credentials, verbose errors, unnecessary features enabled.
7. **XSS**: Reflected, stored, DOM-based. Ensure output encoding and CSP.
8. **Insecure Deserialization**: Validate and sanitize serialized data; avoid deserializing untrusted input.
9. **Using Components with Known Vulnerabilities**: Dependency scanning.
10. **Insufficient Logging & Monitoring**: Audit trails, alerting on anomalies.

## Dependency Scanning

- Use **Shell** to run `npm audit`, `pip-audit`, `cargo audit`, or equivalent for the project's package manager.
- Flag outdated packages with known CVEs. Prioritize direct dependencies and high-severity issues.

## Secret Detection

- Use **Grep** for patterns: API keys, passwords, private keys, tokens (e.g., `password\s*=\s*`, `api_key`, `secret`, `.pem`, `Bearer`).
- Check config files, env examples, and committed history. Recommend moving secrets to vaults or env vars.

## Workflow

Use **Read** and **Grep** to trace data flow from input to output. Use **Glob** to find config and deployment files. Produce a prioritized findings report with remediation steps.
