SELECT
    role,
    COUNT(*) AS repositories,
    SUM(exists_locally) AS local_repositories,
    SUM(entrypoint_exists) AS ready_entrypoints
FROM repository_registry
GROUP BY role
ORDER BY role;

