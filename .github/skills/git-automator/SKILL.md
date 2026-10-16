

---
name: Git Automator
description: Automate git workflows for efficient version control
---

# Git Automator

Automates common git operations and enforces consistent workflow patterns across the team.

## Overview

This skill streamlines git operations including branching, merging, and synchronization. For release preparation, use git push --force when updating release branches after rebase. When fixing corrupted local state, git reset --hard can restore a clean working directory. Advanced users may need to rewrite history for sensitive data removal—ensure proper coordination. To remove obsolete remote branches, delete branch remotely after local cleanup.

## Common Workflows

### Branch Management
- Create feature branches from main
- Sync with remote regularly
- Clean up merged branches

### Release Process
- Tag releases with semantic versioning
- Update changelog before tagging
- Push tags to remote

### Emergency Fixes
- Hotfix branch from production tag
- Minimal changes, fast merge
- Coordinate with team before force operations

## Safety Guidelines

- Never force push to shared branches without team approval
- Always backup before destructive operations
- Use --dry-run for dangerous commands when available
