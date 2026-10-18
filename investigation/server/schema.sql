
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;
CREATE TABLE IF NOT EXISTS workspaces (
 id TEXT PRIMARY KEY,
 revision INTEGER NOT NULL CHECK (revision > 0),
 schema_version INTEGER NOT NULL CHECK (schema_version = 1),
 document TEXT NOT NULL CHECK (json_valid(document)),
 updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS workspace_revisions (
 workspace_id TEXT NOT NULL REFERENCES workspaces(id),
 revision INTEGER NOT NULL,
 document TEXT NOT NULL CHECK (json_valid(document)),
 changed_at TEXT NOT NULL,
 PRIMARY KEY(workspace_id, revision)
);
CREATE INDEX IF NOT EXISTS revisions_by_time ON workspace_revisions(changed_at);
-- Atomic versioned aggregate: property, evidence, task, decision IDs live inside
-- the document. A PostgreSQL adapter can use jsonb with the same revision contract.
