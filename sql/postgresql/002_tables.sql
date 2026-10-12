BEGIN;

CREATE TABLE IF NOT EXISTS permissions
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    permission_name character varying(120) NOT NULL,
    permission_code character varying(120) NOT NULL,
    description text,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT permissions_id_pk PRIMARY KEY (id),
    CONSTRAINT permissions_permission_code_uq UNIQUE (permission_code)
)
TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS roles
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    role_name character varying(100) NOT NULL,
    category character varying(100),
    description text,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT roles_id_pk PRIMARY KEY (id),
    CONSTRAINT roles_role_name_uq UNIQUE (role_name)
)
TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS designations
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    designation_code character varying(50) NOT NULL,
    designation_name character varying(120) NOT NULL,
    level_order integer NOT NULL DEFAULT 1,
    description text,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT designations_id_pk PRIMARY KEY (id),
    CONSTRAINT designations_designation_code_uq UNIQUE (designation_code)
)
TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS departments
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    department_code character varying(50) NOT NULL,
    department_name character varying(120) NOT NULL,
    manager_user_id uuid,
    is_active boolean NOT NULL DEFAULT true,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT departments_id_pk PRIMARY KEY (id),
    CONSTRAINT departments_department_code_uq UNIQUE (department_code)
)
TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS users
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    role_id uuid NOT NULL,
    designation_id uuid,
    department_id uuid,
    first_name character varying(80) NOT NULL,
    last_name character varying(80) NOT NULL,
    email character varying(255) NOT NULL,
    password_hash character varying(255) NOT NULL,
    employment_status character varying(50) NOT NULL DEFAULT 'active',
    is_active boolean NOT NULL DEFAULT true,
    last_login_at timestamp with time zone,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT users_id_pk PRIMARY KEY (id),
    CONSTRAINT users_email_uq UNIQUE (email),
    CONSTRAINT users_designation_id_fk
        FOREIGN KEY (designation_id)
        REFERENCES designations (id)
        ON DELETE SET NULL,
    CONSTRAINT users_department_id_fk
        FOREIGN KEY (department_id)
        REFERENCES departments (id)
        ON DELETE SET NULL,
    CONSTRAINT users_role_id_fk
        FOREIGN KEY (role_id)
        REFERENCES roles (id)
        ON DELETE RESTRICT
)
TABLESPACE pg_default;

ALTER TABLE departments
    DROP CONSTRAINT IF EXISTS departments_manager_user_id_fk;

ALTER TABLE departments
    ADD CONSTRAINT departments_manager_user_id_fk
        FOREIGN KEY (manager_user_id)
        REFERENCES users (id)
        ON DELETE SET NULL;

CREATE TABLE IF NOT EXISTS role_permissions
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    role_id uuid NOT NULL,
    permission_id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT role_permissions_id_pk PRIMARY KEY (id),
    CONSTRAINT role_permissions_role_permission_uq UNIQUE (role_id, permission_id),
    CONSTRAINT role_permissions_role_id_fk
        FOREIGN KEY (role_id)
        REFERENCES roles (id)
        ON DELETE CASCADE,
    CONSTRAINT role_permissions_permission_id_fk
        FOREIGN KEY (permission_id)
        REFERENCES permissions (id)
        ON DELETE CASCADE
)
TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS skills
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    name character varying(120) NOT NULL,
    category character varying(80),
    description text,
    is_active boolean NOT NULL DEFAULT true,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT skills_id_pk PRIMARY KEY (id),
    CONSTRAINT skills_name_uq UNIQUE (name)
)
TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS auth_sessions
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL,
    refresh_token_hash character varying(255) NOT NULL,
    ip_address character varying(64),
    user_agent character varying(512),
    expires_at timestamp with time zone NOT NULL,
    revoked_at timestamp with time zone,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT auth_sessions_id_pk PRIMARY KEY (id),
    CONSTRAINT auth_sessions_user_id_fk
        FOREIGN KEY (user_id)
        REFERENCES users (id)
        ON DELETE CASCADE
)
TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS employee_profiles
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL,
    current_role_title character varying(150) NOT NULL,
    experience_years integer NOT NULL DEFAULT 0,
    career_goal_summary character varying(255),
    bio text,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT employee_profiles_id_pk PRIMARY KEY (id),
    CONSTRAINT employee_profiles_user_id_uq UNIQUE (user_id),
    CONSTRAINT employee_profiles_experience_years_chk CHECK (experience_years >= 0),
    CONSTRAINT employee_profiles_user_id_fk
        FOREIGN KEY (user_id)
        REFERENCES users (id)
        ON DELETE CASCADE
)
TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS user_skills
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL,
    skill_id uuid NOT NULL,
    proficiency_level integer NOT NULL,
    proficiency_label character varying(50),
    evidence_source character varying(120),
    last_assessed_at timestamp with time zone,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT user_skills_id_pk PRIMARY KEY (id),
    CONSTRAINT user_skills_user_skill_uq UNIQUE (user_id, skill_id),
    CONSTRAINT user_skills_skill_id_fk
        FOREIGN KEY (skill_id)
        REFERENCES skills (id)
        ON DELETE CASCADE,
    CONSTRAINT user_skills_user_id_fk
        FOREIGN KEY (user_id)
        REFERENCES users (id)
        ON DELETE CASCADE
)
TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS career_goals
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL,
    target_designation_id uuid,
    target_role_title character varying(150) NOT NULL,
    target_track character varying(100),
    target_date date,
    status character varying(50) NOT NULL DEFAULT 'active',
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT career_goals_id_pk PRIMARY KEY (id),
    CONSTRAINT career_goals_user_id_fk
        FOREIGN KEY (user_id)
        REFERENCES users (id)
        ON DELETE CASCADE,
    CONSTRAINT career_goals_target_designation_id_fk
        FOREIGN KEY (target_designation_id)
        REFERENCES designations (id)
        ON DELETE SET NULL
)
TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS career_paths
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    title character varying(150) NOT NULL,
    target_designation_id uuid,
    track character varying(100),
    difficulty character varying(50),
    growth_outlook character varying(100),
    default_timeline_months integer,
    is_active boolean NOT NULL DEFAULT true,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT career_paths_id_pk PRIMARY KEY (id),
    CONSTRAINT career_paths_target_designation_id_fk
        FOREIGN KEY (target_designation_id)
        REFERENCES designations (id)
        ON DELETE SET NULL
)
TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS career_path_skills
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    career_path_id uuid NOT NULL,
    skill_id uuid NOT NULL,
    required_level integer NOT NULL,
    weight integer NOT NULL DEFAULT 1,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT career_path_skills_id_pk PRIMARY KEY (id),
    CONSTRAINT career_path_skills_path_skill_uq UNIQUE (career_path_id, skill_id),
    CONSTRAINT career_path_skills_career_path_id_fk
        FOREIGN KEY (career_path_id)
        REFERENCES career_paths (id)
        ON DELETE CASCADE,
    CONSTRAINT career_path_skills_skill_id_fk
        FOREIGN KEY (skill_id)
        REFERENCES skills (id)
        ON DELETE CASCADE
)
TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS readiness_assessments
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL,
    career_goal_id uuid NOT NULL,
    readiness_score integer NOT NULL,
    growth_score integer NOT NULL,
    skills_matched integer NOT NULL,
    skills_total integer NOT NULL,
    assessed_on date NOT NULL,
    assessment_source character varying(100),
    summary_data jsonb,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT readiness_assessments_id_pk PRIMARY KEY (id),
    CONSTRAINT readiness_assessments_user_goal_date_uq UNIQUE (user_id, career_goal_id, assessed_on),
    CONSTRAINT readiness_assessments_user_id_fk
        FOREIGN KEY (user_id)
        REFERENCES users (id)
        ON DELETE CASCADE,
    CONSTRAINT readiness_assessments_career_goal_id_fk
        FOREIGN KEY (career_goal_id)
        REFERENCES career_goals (id)
        ON DELETE CASCADE
)
TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS skill_gap_analyses
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL,
    career_goal_id uuid NOT NULL,
    skill_id uuid NOT NULL,
    current_level integer NOT NULL,
    required_level integer NOT NULL,
    priority character varying(30),
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT skill_gap_analyses_id_pk PRIMARY KEY (id),
    CONSTRAINT skill_gap_analyses_user_goal_skill_uq UNIQUE (user_id, career_goal_id, skill_id),
    CONSTRAINT skill_gap_analyses_user_id_fk
        FOREIGN KEY (user_id)
        REFERENCES users (id)
        ON DELETE CASCADE,
    CONSTRAINT skill_gap_analyses_career_goal_id_fk
        FOREIGN KEY (career_goal_id)
        REFERENCES career_goals (id)
        ON DELETE CASCADE,
    CONSTRAINT skill_gap_analyses_skill_id_fk
        FOREIGN KEY (skill_id)
        REFERENCES skills (id)
        ON DELETE CASCADE
)
TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS career_recommendations
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL,
    career_path_id uuid NOT NULL,
    match_score integer NOT NULL,
    rank_order integer NOT NULL,
    recommendation_type character varying(50),
    rationale jsonb,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT career_recommendations_id_pk PRIMARY KEY (id),
    CONSTRAINT career_recommendations_user_id_fk
        FOREIGN KEY (user_id)
        REFERENCES users (id)
        ON DELETE CASCADE,
    CONSTRAINT career_recommendations_career_path_id_fk
        FOREIGN KEY (career_path_id)
        REFERENCES career_paths (id)
        ON DELETE CASCADE
)
TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS whatif_simulations
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL,
    career_path_id uuid NOT NULL,
    cloud_skill_level integer,
    leadership_skill_level integer,
    projected_readiness integer,
    projected_timeline_months integer,
    key_recommendation text,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT whatif_simulations_id_pk PRIMARY KEY (id),
    CONSTRAINT whatif_simulations_user_id_fk
        FOREIGN KEY (user_id)
        REFERENCES users (id)
        ON DELETE CASCADE,
    CONSTRAINT whatif_simulations_career_path_id_fk
        FOREIGN KEY (career_path_id)
        REFERENCES career_paths (id)
        ON DELETE CASCADE
)
TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS development_plans
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL,
    career_goal_id uuid NOT NULL,
    title character varying(150) NOT NULL,
    status character varying(50) NOT NULL DEFAULT 'draft',
    start_date date,
    target_completion_date date,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT development_plans_id_pk PRIMARY KEY (id),
    CONSTRAINT development_plans_user_id_fk
        FOREIGN KEY (user_id)
        REFERENCES users (id)
        ON DELETE CASCADE,
    CONSTRAINT development_plans_career_goal_id_fk
        FOREIGN KEY (career_goal_id)
        REFERENCES career_goals (id)
        ON DELETE CASCADE
)
TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS development_plan_steps
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    plan_id uuid NOT NULL,
    title character varying(150) NOT NULL,
    description text,
    status character varying(50) NOT NULL DEFAULT 'pending',
    sort_order integer NOT NULL DEFAULT 1,
    duration_weeks integer,
    due_date date,
    completed_at timestamp with time zone,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT development_plan_steps_id_pk PRIMARY KEY (id),
    CONSTRAINT development_plan_steps_plan_id_fk
        FOREIGN KEY (plan_id)
        REFERENCES development_plans (id)
        ON DELETE CASCADE
)
TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS roadmaps
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL,
    roadmap_data jsonb NOT NULL,
    generated_by roadmap_generated_by NOT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT roadmaps_id_pk PRIMARY KEY (id),
    CONSTRAINT roadmaps_user_id_fk
        FOREIGN KEY (user_id)
        REFERENCES users (id)
        ON DELETE CASCADE
)
TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS learning_recommendations
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL,
    recommendations jsonb NOT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT learning_recommendations_id_pk PRIMARY KEY (id),
    CONSTRAINT learning_recommendations_user_id_fk
        FOREIGN KEY (user_id)
        REFERENCES users (id)
        ON DELETE CASCADE
)
TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS chat_history
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL,
    message text NOT NULL,
    response text NOT NULL,
    context jsonb,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT chat_history_id_pk PRIMARY KEY (id),
    CONSTRAINT chat_history_user_id_fk
        FOREIGN KEY (user_id)
        REFERENCES users (id)
        ON DELETE CASCADE
)
TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS teams
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    department_id uuid NOT NULL,
    manager_user_id uuid NOT NULL,
    team_name character varying(120) NOT NULL,
    team_code character varying(50) NOT NULL,
    is_active boolean NOT NULL DEFAULT true,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT teams_id_pk PRIMARY KEY (id),
    CONSTRAINT teams_team_code_uq UNIQUE (team_code),
    CONSTRAINT teams_department_id_fk
        FOREIGN KEY (department_id)
        REFERENCES departments (id)
        ON DELETE CASCADE,
    CONSTRAINT teams_manager_user_id_fk
        FOREIGN KEY (manager_user_id)
        REFERENCES users (id)
        ON DELETE CASCADE
)
TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS team_insights
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    team_id uuid NOT NULL,
    snapshot_date date NOT NULL,
    team_size integer NOT NULL,
    avg_readiness_score integer NOT NULL,
    critical_gap_count integer NOT NULL,
    summary_data jsonb,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT team_insights_id_pk PRIMARY KEY (id),
    CONSTRAINT team_insights_team_date_uq UNIQUE (team_id, snapshot_date),
    CONSTRAINT team_insights_team_id_fk
        FOREIGN KEY (team_id)
        REFERENCES teams (id)
        ON DELETE CASCADE
)
TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS team_members
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL,
    team_id uuid NOT NULL,
    member_role character varying(50),
    joined_at date,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT team_members_id_pk PRIMARY KEY (id),
    CONSTRAINT team_members_user_team_uq UNIQUE (user_id, team_id),
    CONSTRAINT team_members_user_id_fk
        FOREIGN KEY (user_id)
        REFERENCES users (id)
        ON DELETE CASCADE,
    CONSTRAINT team_members_team_id_fk
        FOREIGN KEY (team_id)
        REFERENCES teams (id)
        ON DELETE CASCADE
)
TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS team_skill_metrics
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    team_insight_id uuid NOT NULL,
    skill_id uuid NOT NULL,
    members_with_skill integer NOT NULL,
    member_count integer NOT NULL,
    coverage_percent integer NOT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT team_skill_metrics_id_pk PRIMARY KEY (id),
    CONSTRAINT team_skill_metrics_insight_skill_uq UNIQUE (team_insight_id, skill_id),
    CONSTRAINT team_skill_metrics_team_insight_id_fk
        FOREIGN KEY (team_insight_id)
        REFERENCES team_insights (id)
        ON DELETE CASCADE,
    CONSTRAINT team_skill_metrics_skill_id_fk
        FOREIGN KEY (skill_id)
        REFERENCES skills (id)
        ON DELETE CASCADE
)
TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS org_insights
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    snapshot_date date NOT NULL,
    total_employees integer NOT NULL,
    department_count integer NOT NULL,
    avg_readiness_score integer NOT NULL,
    open_positions integer NOT NULL,
    summary_data jsonb,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT org_insights_id_pk PRIMARY KEY (id),
    CONSTRAINT org_insights_snapshot_date_uq UNIQUE (snapshot_date)
)
TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS department_insights
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    department_id uuid NOT NULL,
    snapshot_date date NOT NULL,
    team_size integer NOT NULL,
    readiness_score integer NOT NULL,
    growth_percent numeric(5,2) NOT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT department_insights_id_pk PRIMARY KEY (id),
    CONSTRAINT department_insights_department_date_uq UNIQUE (department_id, snapshot_date),
    CONSTRAINT department_insights_department_id_fk
        FOREIGN KEY (department_id)
        REFERENCES departments (id)
        ON DELETE CASCADE
)
TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS skill_demand_metrics
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    skill_id uuid NOT NULL,
    department_id uuid NOT NULL,
    snapshot_date date NOT NULL,
    supply_percent integer NOT NULL,
    demand_percent integer NOT NULL,
    market_trend character varying(100),
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT skill_demand_metrics_id_pk PRIMARY KEY (id),
    CONSTRAINT skill_demand_metrics_skill_department_date_uq UNIQUE (skill_id, department_id, snapshot_date),
    CONSTRAINT skill_demand_metrics_skill_id_fk
        FOREIGN KEY (skill_id)
        REFERENCES skills (id)
        ON DELETE CASCADE,
    CONSTRAINT skill_demand_metrics_department_id_fk
        FOREIGN KEY (department_id)
        REFERENCES departments (id)
        ON DELETE CASCADE
)
TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS talent_insights
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL,
    snapshot_date date NOT NULL,
    potential_score integer NOT NULL,
    growth_percent integer NOT NULL,
    skill_growth_percent integer NOT NULL,
    talent_segment character varying(100),
    top_skill character varying(120),
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT talent_insights_id_pk PRIMARY KEY (id),
    CONSTRAINT talent_insights_user_date_uq UNIQUE (user_id, snapshot_date),
    CONSTRAINT talent_insights_user_id_fk
        FOREIGN KEY (user_id)
        REFERENCES users (id)
        ON DELETE CASCADE
)
TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS audit_logs
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    actor_user_id uuid,
    entity_type character varying(100) NOT NULL,
    entity_id uuid,
    action character varying(100) NOT NULL,
    change_summary jsonb,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT audit_logs_id_pk PRIMARY KEY (id),
    CONSTRAINT audit_logs_actor_user_id_fk
        FOREIGN KEY (actor_user_id)
        REFERENCES users (id)
        ON DELETE SET NULL
)
TABLESPACE pg_default;

COMMIT;
