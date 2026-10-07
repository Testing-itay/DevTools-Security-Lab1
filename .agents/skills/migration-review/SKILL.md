---
name: migration-review
description: Review a database migration before it merges. Use when a diff adds or changes a migration file.
---

# Migration review

1. Check that the migration can run on a large table without a long lock.
   Adding a column with a default, or a new index without `CONCURRENTLY`,
   needs a second look.
2. Check that a down migration exists, or that the PR says why it cannot.
3. Check that the code in the same PR still works before the migration runs.
