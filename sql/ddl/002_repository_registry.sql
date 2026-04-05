CREATE TABLE IF NOT EXISTS repository_registry (
    id TEXT NOT NULL,
    title TEXT NOT NULL,
    role TEXT NOT NULL,
    resolved_path TEXT NOT NULL,
    exists_locally INTEGER NOT NULL,
    entrypoint_exists INTEGER NOT NULL,
    readme_title TEXT
);

