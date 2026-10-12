-- 1. Fetch user with designation name and role name
SELECT
    u.id,
    u.first_name,
    u.last_name,
    u.email,
    dep.department_name,
    d.designation_name,
    r.role_name
FROM users u
LEFT JOIN departments dep ON dep.id = u.department_id
LEFT JOIN designations d ON d.id = u.designation_id
LEFT JOIN roles r ON r.id = u.role_id;

-- 2. Fetch all permissions for a given user
SELECT
    u.id AS user_id,
    p.permission_name,
    p.permission_code
FROM users u
JOIN roles r ON r.id = u.role_id
JOIN role_permissions rp ON rp.role_id = r.id
JOIN permissions p ON p.id = rp.permission_id
WHERE u.id = '<user_uuid>'
ORDER BY p.permission_name;

-- 3. Assign permission to a role
INSERT INTO role_permissions (role_id, permission_id, created_at)
VALUES ('<role_uuid>', '<permission_uuid>', now())
ON CONFLICT (role_id, permission_id) DO NOTHING;

-- 4. Deactivate a user
UPDATE users
SET
    is_active = false,
    updated_at = now()
WHERE id = '<user_uuid>';

-- 5. Get all users grouped by designation
SELECT
    d.designation_name,
    COUNT(u.id) AS total_users
FROM designations d
LEFT JOIN users u ON u.designation_id = d.id
GROUP BY d.designation_name
ORDER BY d.designation_name;

-- 6. Fetch active team members for a manager with their readiness score
SELECT
    t.team_name,
    u.id AS user_id,
    u.first_name,
    u.last_name,
    ra.readiness_score,
    ra.assessed_on
FROM teams t
JOIN team_members tm ON tm.team_id = t.id
JOIN users u ON u.id = tm.user_id
LEFT JOIN readiness_assessments ra ON ra.user_id = u.id
WHERE t.manager_user_id = '<manager_user_uuid>'
ORDER BY t.team_name, u.first_name, ra.assessed_on DESC;

-- 7. Top in-demand skills by department snapshot
SELECT
    d.department_name,
    s.name AS skill_name,
    sdm.supply_percent,
    sdm.demand_percent,
    sdm.market_trend
FROM skill_demand_metrics sdm
JOIN departments d ON d.id = sdm.department_id
JOIN skills s ON s.id = sdm.skill_id
WHERE sdm.snapshot_date = CURRENT_DATE
ORDER BY d.department_name, sdm.demand_percent DESC;
