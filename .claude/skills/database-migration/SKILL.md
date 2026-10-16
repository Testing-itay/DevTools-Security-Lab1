


---
name: Database Migration
description: Generate and validate database migration scripts across multiple ORMs.
---

# Database Migration Skill

Create safe, reversible database migrations that preserve data integrity and support multiple ORM ecosystems.

## Migration Best Practices

- **One logical change per migration**: Add a column, create a table, or alter an index—not all at once. Simplifies rollback and review.
- **Idempotency where possible**: Use `IF NOT EXISTS`, `IF EXISTS` to make migrations safe to re-run.
- **Avoid data loss**: Prefer adding columns as nullable, backfilling, then adding constraints. Avoid dropping columns with data without explicit backup steps.
- **Naming**: Use descriptive names (e.g., `add_user_email_index`, `create_orders_table`) and timestamps for ordering.

## Rollback Strategies

- Every migration should have a corresponding down/rollback script that restores the previous schema.
- For destructive changes (DROP, DELETE), document data backup and restore procedures.
- Test rollbacks in a staging environment before production deployment.
- Use transactions where the database supports DDL in transactions (e.g., PostgreSQL); otherwise, design for partial failure recovery.

## Data Integrity

- Add foreign keys, check constraints, and NOT NULL only after data is validated and backfilled.
- Use batched updates for large tables to avoid long-running transactions and lock contention.
- Validate migration scripts against a copy of production data before applying to production.

## ORM Support

- **SQLAlchemy/Alembic**: Generate migrations with `alembic revision`, use `op.batch_alter_table` for SQLite.
- **TypeORM**: Use `synchronize: false` in production; rely on migration files.
- **Django**: Use `makemigrations` and `migrate`; avoid editing applied migrations.
- **Prisma**: Use `prisma migrate dev` for development; `prisma migrate deploy` for production.

Provide migration files with clear comments and a summary of schema changes.
