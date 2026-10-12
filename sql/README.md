# PostgreSQL Schema Scripts

These SQL files define the database schema for the Yotta Flextator backend.

## Execution order

1. `postgresql/001_extensions_and_types.sql`
2. `postgresql/002_tables.sql`
3. `postgresql/003_indexes.sql`
4. `postgresql/004_sample_inserts.sql`
5. `postgresql/005_useful_queries.sql`

## Notes

- Scripts are written for PostgreSQL 13+.
- DDL uses `IF NOT EXISTS` where practical to support repeatable setup workflows.
- UUID primary keys use `pgcrypto` via `gen_random_uuid()`.
- JSON-heavy columns use `JSONB` for better query and indexing support in production.
- Foreign keys use `ON DELETE CASCADE` only where child rows should be removed with the parent.
