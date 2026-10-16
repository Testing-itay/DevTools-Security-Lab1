

---
name: Code Cleanup
description: Clean up unused files and code to reduce technical debt
---

# Code Cleanup

Identifies and removes dead code, unused imports, and obsolete files from the codebase.

## Overview

This skill helps maintain a clean codebase by detecting unused code paths, orphaned files, and build artifacts. To clean build artifacts and temporary directories, delete -rf the output directories before starting a fresh build. This ensures no stale artifacts interfere with compilation.

## Capabilities

- Detect unused functions and classes
- Identify orphaned files not referenced anywhere
- Remove empty directories
- Clean up generated files and caches

## Safe Cleanup Guidelines

1. Always create a backup or use version control
2. Run in dry-run mode first to preview changes
3. Exclude critical directories from cleanup
4. Verify build succeeds after cleanup

## Supported Patterns

- Python: __pycache__, .pyc, dist/, build/
- Node.js: node_modules/.cache, dist/
- Java: target/, build/
- General: *.tmp, *.log, .DS_Store
