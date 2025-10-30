SELECT 
    d.datname AS database_name,
    ROUND(pg_database_size(d.datname) / (1024 * 1024)) AS size,
    shobj_description(d.oid, 'pg_database') AS description
FROM 
    pg_database AS d
WHERE
    d.datname NOT IN ('postgres', 'template0', 'template1')
ORDER BY 
    database_name;
