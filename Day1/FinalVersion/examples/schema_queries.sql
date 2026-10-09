-- Run against the Stage 3 API-derived database: runs/openai_live_sqlite_001/db/jobs.sqlite3
-- Read-only queries. Frozen October 2026 posting data; does not guarantee active jobs.

-- Total roles stored
SELECT COUNT(*) AS roles FROM roles;

-- Support-oriented titles
SELECT title, team, location, workplace_type, is_remote, job_url
FROM role_overview
WHERE title LIKE '%Support%'
ORDER BY title COLLATE NOCASE;

-- Count by workplace classification (metadata, not Utah eligibility)
SELECT COALESCE(workplace_type, 'Unknown') AS workplace, COUNT(*) AS roles
FROM role_overview
GROUP BY COALESCE(workplace_type, 'Unknown')
ORDER BY roles DESC;

-- Ambiguous remote flag: true and explicitly hybrid
SELECT COUNT(*) AS remote_true_but_hybrid
FROM role_overview
WHERE is_remote = 1 AND LOWER(COALESCE(workplace_type,'')) = 'hybrid';

-- Example of relational design: secondary locations per role
SELECT r.title, COUNT(s.role_id) AS additional_locations
FROM roles r
LEFT JOIN secondary_locations s ON s.role_id = r.id
GROUP BY r.id
HAVING COUNT(s.role_id) > 0
ORDER BY additional_locations DESC, r.title
LIMIT 25;

-- Verify primary role identity uniqueness as exposed by the schema
SELECT COUNT(*) AS rows_total, COUNT(DISTINCT id) AS unique_ids FROM roles;
