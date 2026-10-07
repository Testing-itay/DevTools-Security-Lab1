---
name: dependency-bump
description: Bump one dependency to a newer version safely. Use when asked to upgrade a package or to fix a dependency advisory.
---

# Dependency bump

1. Read the changelog between the current and target version.
2. Change only that dependency and its lockfile entry.
3. Run the unit and integration tests for every service that imports it.
4. In the PR, list breaking changes from the changelog and how each was handled.
