BEGIN;

INSERT INTO roles (role_name, category, description)
VALUES
    ('employee', 'employee', 'Default employee role'),
    ('manager', 'manager', 'Manager role with team oversight'),
    ('hr', 'hr', 'Human resources role for workforce analytics and people operations'),
    ('organization_admin', 'organization', 'Organization administrator role')
ON CONFLICT (role_name) DO NOTHING;

INSERT INTO designations (designation_code, designation_name, level_order, description)
VALUES
    ('SE1', 'Software Engineer I', 1, 'Entry-level engineering designation'),
    ('SE2', 'Software Engineer II', 2, 'Mid-level engineering designation'),
    ('SSE', 'Senior Software Engineer', 3, 'Senior engineering designation'),
    ('EM', 'Engineering Manager', 4, 'Engineering leadership designation'),
    ('HRBP', 'HR Business Partner', 5, 'Human resources partner designation'),
    ('DIR', 'Director', 6, 'Senior leadership designation')
ON CONFLICT (designation_code) DO NOTHING;

INSERT INTO departments (department_code, department_name, is_active)
VALUES
    ('ENG', 'Engineering', true),
    ('HR', 'Human Resources', true),
    ('OPS', 'Operations', true)
ON CONFLICT (department_code) DO NOTHING;

INSERT INTO permissions (permission_name, permission_code, description)
VALUES
    ('View Employee Dashboard', 'employee.dashboard.view', 'Access employee dashboard and career insights'),
    ('Manage Team Insights', 'manager.team_insights.view', 'Access manager dashboard and team insights'),
    ('View HR Analytics', 'hr.analytics.view', 'Access HR dashboards and workforce reporting'),
    ('Manage Users', 'users.manage', 'Create, update, and deactivate users')
ON CONFLICT (permission_code) DO NOTHING;

COMMIT;
