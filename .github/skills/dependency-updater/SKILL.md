


---
name: Dependency Updater
description: Check and update outdated dependencies across all package managers.
---

# Dependency Updater Skill

Safely identify, evaluate, and update outdated dependencies while minimizing breakage.

## Package Manager Support

- **npm/yarn/pnpm**: `npm outdated`, `yarn outdated`, `pnpm outdated`. Use `npm update`, `yarn upgrade`, or `pnpm update` with care.
- **pip**: `pip list --outdated`, `pip install --upgrade`. Prefer `pip-tools` or `poetry` for reproducible environments.
- **cargo**: `cargo outdated` (external crate). Use `cargo update` for lockfile updates.
- **Maven/Gradle**: Check for plugin and dependency updates via `versions:display-dependency-updates`.
- **NuGet**: `dotnet list package --outdated`.

## Semver and Breaking Changes

- **Major (x.0.0)**: Expect breaking changes. Read changelogs and migration guides before upgrading.
- **Minor (0.x.0)**: New features, ideally backward compatible. Lower risk but still test.
- **Patch (0.0.x)**: Bug fixes and security patches. Generally safe; prioritize for security.

## Security Updates

- Prioritize dependencies with known CVEs. Use `npm audit`, `pip-audit`, `cargo audit`, Dependabot, or Snyk.
- Apply security patches even across major versions when feasible; document any breaking changes introduced.

## Workflow

1. List outdated packages and their current vs. latest versions.
2. Check changelogs, release notes, and migration guides for breaking changes.
3. Propose updates in batches: security first, then patch, then minor. Handle major upgrades separately with explicit approval.
4. Run the full test suite after updates. Fix any failures or incompatibilities.
5. Update lockfiles and document the changes in commit messages or PR descriptions.
