BEGIN;

CREATE INDEX IF NOT EXISTS ix_permissions_permission_name
    ON permissions (permission_name);

CREATE INDEX IF NOT EXISTS ix_roles_category
    ON roles (category);

CREATE INDEX IF NOT EXISTS ix_designations_level_order
    ON designations (level_order);

CREATE INDEX IF NOT EXISTS ix_departments_manager_user_id
    ON departments (manager_user_id);

CREATE INDEX IF NOT EXISTS ix_departments_is_active
    ON departments (is_active);

CREATE INDEX IF NOT EXISTS ix_users_designation_id
    ON users (designation_id);

CREATE INDEX IF NOT EXISTS ix_users_role_id
    ON users (role_id);

CREATE INDEX IF NOT EXISTS ix_users_department_id
    ON users (department_id);

CREATE INDEX IF NOT EXISTS ix_users_is_active
    ON users (is_active);

CREATE INDEX IF NOT EXISTS ix_users_employment_status
    ON users (employment_status);

CREATE INDEX IF NOT EXISTS ix_role_permissions_role_id
    ON role_permissions (role_id);

CREATE INDEX IF NOT EXISTS ix_role_permissions_permission_id
    ON role_permissions (permission_id);

CREATE INDEX IF NOT EXISTS ix_skills_category
    ON skills (category);

CREATE INDEX IF NOT EXISTS ix_skills_is_active
    ON skills (is_active);

CREATE INDEX IF NOT EXISTS ix_auth_sessions_user_id
    ON auth_sessions (user_id);

CREATE INDEX IF NOT EXISTS ix_auth_sessions_expires_at
    ON auth_sessions (expires_at);

CREATE INDEX IF NOT EXISTS ix_employee_profiles_user_id
    ON employee_profiles (user_id);

CREATE INDEX IF NOT EXISTS ix_user_skills_user_id
    ON user_skills (user_id);

CREATE INDEX IF NOT EXISTS ix_user_skills_skill_id
    ON user_skills (skill_id);

CREATE INDEX IF NOT EXISTS ix_user_skills_proficiency_level
    ON user_skills (proficiency_level);

CREATE INDEX IF NOT EXISTS ix_career_goals_user_id
    ON career_goals (user_id);

CREATE INDEX IF NOT EXISTS ix_career_goals_target_designation_id
    ON career_goals (target_designation_id);

CREATE INDEX IF NOT EXISTS ix_career_goals_status
    ON career_goals (status);

CREATE INDEX IF NOT EXISTS ix_career_paths_target_designation_id
    ON career_paths (target_designation_id);

CREATE INDEX IF NOT EXISTS ix_career_paths_track
    ON career_paths (track);

CREATE INDEX IF NOT EXISTS ix_career_paths_is_active
    ON career_paths (is_active);

CREATE INDEX IF NOT EXISTS ix_career_path_skills_career_path_id
    ON career_path_skills (career_path_id);

CREATE INDEX IF NOT EXISTS ix_career_path_skills_skill_id
    ON career_path_skills (skill_id);

CREATE INDEX IF NOT EXISTS ix_readiness_assessments_user_id
    ON readiness_assessments (user_id);

CREATE INDEX IF NOT EXISTS ix_readiness_assessments_career_goal_id
    ON readiness_assessments (career_goal_id);

CREATE INDEX IF NOT EXISTS ix_readiness_assessments_assessed_on
    ON readiness_assessments (assessed_on);

CREATE INDEX IF NOT EXISTS ix_readiness_assessments_summary_data_gin
    ON readiness_assessments USING GIN (summary_data);

CREATE INDEX IF NOT EXISTS ix_roadmaps_user_id
    ON roadmaps (user_id);

CREATE INDEX IF NOT EXISTS ix_roadmaps_generated_by
    ON roadmaps (generated_by);

CREATE INDEX IF NOT EXISTS ix_roadmaps_roadmap_data_gin
    ON roadmaps USING GIN (roadmap_data);

CREATE INDEX IF NOT EXISTS ix_skill_gap_analyses_user_id
    ON skill_gap_analyses (user_id);

CREATE INDEX IF NOT EXISTS ix_skill_gap_analyses_career_goal_id
    ON skill_gap_analyses (career_goal_id);

CREATE INDEX IF NOT EXISTS ix_skill_gap_analyses_skill_id
    ON skill_gap_analyses (skill_id);

CREATE INDEX IF NOT EXISTS ix_skill_gap_analyses_priority
    ON skill_gap_analyses (priority);

CREATE INDEX IF NOT EXISTS ix_career_recommendations_user_id
    ON career_recommendations (user_id);

CREATE INDEX IF NOT EXISTS ix_career_recommendations_career_path_id
    ON career_recommendations (career_path_id);

CREATE INDEX IF NOT EXISTS ix_career_recommendations_rank_order
    ON career_recommendations (rank_order);

CREATE INDEX IF NOT EXISTS ix_career_recommendations_rationale_gin
    ON career_recommendations USING GIN (rationale);

CREATE INDEX IF NOT EXISTS ix_whatif_simulations_user_id
    ON whatif_simulations (user_id);

CREATE INDEX IF NOT EXISTS ix_whatif_simulations_career_path_id
    ON whatif_simulations (career_path_id);

CREATE INDEX IF NOT EXISTS ix_development_plans_user_id
    ON development_plans (user_id);

CREATE INDEX IF NOT EXISTS ix_development_plans_career_goal_id
    ON development_plans (career_goal_id);

CREATE INDEX IF NOT EXISTS ix_development_plans_status
    ON development_plans (status);

CREATE INDEX IF NOT EXISTS ix_development_plan_steps_plan_id
    ON development_plan_steps (plan_id);

CREATE INDEX IF NOT EXISTS ix_development_plan_steps_status
    ON development_plan_steps (status);

CREATE INDEX IF NOT EXISTS ix_learning_recommendations_user_id
    ON learning_recommendations (user_id);

CREATE INDEX IF NOT EXISTS ix_learning_recommendations_recommendations_gin
    ON learning_recommendations USING GIN (recommendations);

CREATE INDEX IF NOT EXISTS ix_chat_history_user_id
    ON chat_history (user_id);

CREATE INDEX IF NOT EXISTS ix_chat_history_context_gin
    ON chat_history USING GIN (context);

CREATE INDEX IF NOT EXISTS ix_teams_department_id
    ON teams (department_id);

CREATE INDEX IF NOT EXISTS ix_teams_manager_user_id
    ON teams (manager_user_id);

CREATE INDEX IF NOT EXISTS ix_teams_is_active
    ON teams (is_active);

CREATE INDEX IF NOT EXISTS ix_team_members_user_id
    ON team_members (user_id);

CREATE INDEX IF NOT EXISTS ix_team_members_team_id
    ON team_members (team_id);

CREATE INDEX IF NOT EXISTS ix_team_insights_team_id
    ON team_insights (team_id);

CREATE INDEX IF NOT EXISTS ix_team_insights_snapshot_date
    ON team_insights (snapshot_date);

CREATE INDEX IF NOT EXISTS ix_team_insights_summary_data_gin
    ON team_insights USING GIN (summary_data);

CREATE INDEX IF NOT EXISTS ix_team_skill_metrics_team_insight_id
    ON team_skill_metrics (team_insight_id);

CREATE INDEX IF NOT EXISTS ix_team_skill_metrics_skill_id
    ON team_skill_metrics (skill_id);

CREATE INDEX IF NOT EXISTS ix_org_insights_snapshot_date
    ON org_insights (snapshot_date);

CREATE INDEX IF NOT EXISTS ix_org_insights_summary_data_gin
    ON org_insights USING GIN (summary_data);

CREATE INDEX IF NOT EXISTS ix_department_insights_department_id
    ON department_insights (department_id);

CREATE INDEX IF NOT EXISTS ix_department_insights_snapshot_date
    ON department_insights (snapshot_date);

CREATE INDEX IF NOT EXISTS ix_skill_demand_metrics_skill_id
    ON skill_demand_metrics (skill_id);

CREATE INDEX IF NOT EXISTS ix_skill_demand_metrics_department_id
    ON skill_demand_metrics (department_id);

CREATE INDEX IF NOT EXISTS ix_skill_demand_metrics_snapshot_date
    ON skill_demand_metrics (snapshot_date);

CREATE INDEX IF NOT EXISTS ix_talent_insights_user_id
    ON talent_insights (user_id);

CREATE INDEX IF NOT EXISTS ix_talent_insights_snapshot_date
    ON talent_insights (snapshot_date);

CREATE INDEX IF NOT EXISTS ix_audit_logs_actor_user_id
    ON audit_logs (actor_user_id);

CREATE INDEX IF NOT EXISTS ix_audit_logs_entity_type
    ON audit_logs (entity_type);

CREATE INDEX IF NOT EXISTS ix_audit_logs_entity_id
    ON audit_logs (entity_id);

COMMIT;
