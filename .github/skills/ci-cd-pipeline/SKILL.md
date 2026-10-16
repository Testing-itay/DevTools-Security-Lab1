


---
name: CI/CD Pipeline
description: Generate and optimize GitHub Actions CI/CD workflows.
allowed-tools: Read, Write
---

# CI/CD Pipeline Skill

Create and improve GitHub Actions workflows for reliable, fast, and maintainable CI/CD.

## Workflow Syntax

- Use `on` for triggers: `push`, `pull_request`, `workflow_dispatch`, `schedule`. Specify branches/tags to avoid unnecessary runs.
- Define jobs with `runs-on` (ubuntu-latest, windows-latest, macos-latest). Use matrix strategy for multi-version testing.
- Use `needs` for job dependencies. Parallelize independent jobs to reduce total time.
- Set `timeout-minutes` to prevent hung jobs from consuming resources.

## Caching

- Cache package manager caches: `actions/cache` for npm, pip, cargo, Maven, etc.
- Use `cache-dependency-path` for monorepos. Invalidate cache keys when lockfiles change.
- Cache build artifacts between jobs when build and test are split.

## Parallel Jobs

- Run lint, unit tests, integration tests, and build in parallel where possible.
- Use job matrices for testing across Node 18/20, Python 3.10/3.11, etc.
- Fail fast with `fail-fast: true` in matrix when one combination fails and others are unlikely to succeed.

## Deployment Strategies

- Use environments (e.g., `staging`, `production`) with protection rules and secrets.
- Implement blue-green or canary via separate workflows or manual approval gates.
- Tag releases with `actions/create-release` and `actions/upload-artifact` for binaries.
- Use `workflow_run` or `repository_dispatch` for deployment pipelines triggered by successful builds.

## Output

Produce valid `.yml` workflow files under `.github/workflows/`. Include comments for key decisions and document required secrets and environment variables.
