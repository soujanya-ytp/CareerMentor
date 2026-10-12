from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import inspect, select
from sqlalchemy.orm import Session

from app.db.session import SessionLocal, get_database_url_for_logging
from app.models.designation import Designation
from app.models.role import Role
from app.models.skill import Skill
from app.models.user import User

# Keep role identifiers aligned with the application's enum/authorization checks.
DEFAULT_ROLE_SEEDS = (
    {
        "role_name": "organization_admin",
        "category": "Admin",
        "description": "Administrative role with platform-wide access.",
    },
    {
        "role_name": "hr",
        "category": "HR",
        "description": "Human resources role for workforce planning and analytics.",
    },
    {
        "role_name": "employee",
        "category": "Employee",
        "description": "Standard employee role for career development features.",
    },
)

DEFAULT_DESIGNATION_SEEDS = (
    {
        "designation_code": "ASSOC_L1",
        "designation_name": "Associate L1",
        "level_order": 1,
        "description": "Entry-level individual contributor.",
    },
    {
        "designation_code": "ASSOC_L2",
        "designation_name": "Associate L2",
        "level_order": 2,
        "description": "Developing individual contributor with growing ownership.",
    },
    {
        "designation_code": "SR_ASSOC",
        "designation_name": "Senior Associate",
        "level_order": 3,
        "description": "Experienced contributor with consistent delivery.",
    },
    {
        "designation_code": "LEAD",
        "designation_name": "Lead",
        "level_order": 4,
        "description": "Team lead guiding delivery and mentoring peers.",
    },
    {
        "designation_code": "SR_LEAD",
        "designation_name": "Senior Lead",
        "level_order": 5,
        "description": "Senior lead driving larger workstreams and cross-team execution.",
    },
    {
        "designation_code": "ASST_MGR",
        "designation_name": "Assistant Manager",
        "level_order": 6,
        "description": "People manager supporting execution and team growth.",
    },
    {
        "designation_code": "MGR",
        "designation_name": "Manager",
        "level_order": 7,
        "description": "Manager accountable for team outcomes and people development.",
    },
    {
        "designation_code": "SR_MGR",
        "designation_name": "Senior Manager",
        "level_order": 8,
        "description": "Senior manager coordinating multiple teams or functions.",
    },
    {
        "designation_code": "ASSOC_DIR",
        "designation_name": "Associate Director",
        "level_order": 9,
        "description": "Associate director leading strategic execution across teams.",
    },
    {
        "designation_code": "DIR",
        "designation_name": "Director",
        "level_order": 10,
        "description": "Director owning departmental direction and delivery.",
    },
    {
        "designation_code": "SR_DIR",
        "designation_name": "Senior Director",
        "level_order": 11,
        "description": "Senior director steering multi-team strategy and operations.",
    },
    {
        "designation_code": "VP",
        "designation_name": "Vice President",
        "level_order": 12,
        "description": "Executive leadership role for organizational planning.",
    },
)

DEFAULT_SKILL_SEEDS = (
    {"name": "React", "category": "Frontend", "description": "JavaScript library for building UI"},
    {"name": "HTML", "category": "Frontend", "description": "Markup language for web pages"},
    {"name": "CSS", "category": "Frontend", "description": "Styling language for web design"},
    {"name": "Tailwind CSS", "category": "Frontend", "description": "Utility-first CSS framework"},
    {"name": "Next.js", "category": "Frontend", "description": "React framework for SSR and fullstack apps"},
    {"name": "Node.js", "category": "Backend", "description": "JavaScript runtime for server-side apps"},
    {"name": "Java", "category": "Backend", "description": "Object-oriented programming language"},
    {"name": "Spring Boot", "category": "Backend", "description": "Java-based backend framework"},
    {"name": "Python", "category": "Backend", "description": "General-purpose programming language"},
    {"name": "SQL", "category": "Database", "description": "Language for managing relational databases"},
    {"name": "PostgreSQL", "category": "Database", "description": "Advanced open-source relational DB"},
    {"name": "MongoDB", "category": "Database", "description": "NoSQL document database"},
    {"name": "AWS", "category": "Cloud", "description": "Amazon Web Services cloud platform"},
    {"name": "Docker", "category": "DevOps", "description": "Containerization platform"},
    {"name": "Kubernetes", "category": "DevOps", "description": "Container orchestration tool"},
    {"name": "Git", "category": "DevOps", "description": "Version control system"},
    {"name": "System Design", "category": "Architecture", "description": "Designing scalable systems"},
)

DEFAULT_SEED_USER = {
    "first_name": "Default",
    "last_name": "HR",
    "email": "syed.osman@yottatechports.com",
    "password": "ChangeMe123!",
    "role_name": "hr",
    "designation_code": "MGR",
}

REQUIRED_TABLES = ("roles", "designations", "users", "skills")


@dataclass(frozen=True)
class SeedSummary:
    created_roles: int
    existing_roles: int
    created_designations: int
    existing_designations: int
    created_skills: int
    existing_skills: int
    default_user_created: bool
    default_user_updated: bool


def _ensure_required_tables(session: Session) -> None:
    inspector = inspect(session.get_bind())
    missing_tables = [table_name for table_name in REQUIRED_TABLES if not inspector.has_table(table_name)]
    if missing_tables:
        missing = ", ".join(sorted(missing_tables))
        raise RuntimeError(
            f"Missing required tables: {missing}. Run `alembic upgrade head` before seeding."
        )


def _seed_roles(session: Session) -> tuple[dict[str, Role], int, int]:
    role_names = [role_seed["role_name"] for role_seed in DEFAULT_ROLE_SEEDS]
    existing_roles = {
        role.role_name: role
        for role in session.execute(select(Role).where(Role.role_name.in_(role_names))).scalars().all()
    }

    created_count = 0
    existing_count = 0
    resolved_roles: dict[str, Role] = {}

    for role_seed in DEFAULT_ROLE_SEEDS:
        role = existing_roles.get(role_seed["role_name"])
        if role is None:
            role = Role(**role_seed)
            session.add(role)
            created_count += 1
        else:
            existing_count += 1

        resolved_roles[role_seed["role_name"]] = role

    session.flush()
    return resolved_roles, created_count, existing_count


def _seed_designations(session: Session) -> tuple[dict[str, Designation], int, int]:
    designation_codes = [
        designation_seed["designation_code"] for designation_seed in DEFAULT_DESIGNATION_SEEDS
    ]
    existing_designations = {
        designation.designation_code: designation
        for designation in session.execute(
            select(Designation).where(Designation.designation_code.in_(designation_codes))
        )
        .scalars()
        .all()
    }

    created_count = 0
    existing_count = 0
    resolved_designations: dict[str, Designation] = {}

    for designation_seed in DEFAULT_DESIGNATION_SEEDS:
        designation = existing_designations.get(designation_seed["designation_code"])
        if designation is None:
            designation = Designation(**designation_seed)
            session.add(designation)
            created_count += 1
        else:
            existing_count += 1

        resolved_designations[designation_seed["designation_code"]] = designation

    session.flush()
    return resolved_designations, created_count, existing_count


def _seed_skills(session: Session) -> tuple[int, int]:
    skill_names = [s["name"] for s in DEFAULT_SKILL_SEEDS]
    existing_skills = {
        skill.name: skill
        for skill in session.execute(select(Skill).where(Skill.name.in_(skill_names))).scalars().all()
    }

    created_count = 0
    existing_count = 0

    for skill_seed in DEFAULT_SKILL_SEEDS:
        if skill_seed["name"] in existing_skills:
            existing_count += 1
        else:
            session.add(Skill(**skill_seed))
            created_count += 1

    session.flush()
    return created_count, existing_count


def _seed_default_user(
    session: Session,
    roles_by_name: dict[str, Role],
    designations_by_code: dict[str, Designation],
) -> tuple[bool, bool]:
    default_user = session.execute(
        select(User).where(User.email == DEFAULT_SEED_USER["email"])
    ).scalar_one_or_none()

    role = roles_by_name[DEFAULT_SEED_USER["role_name"]]
    designation = designations_by_code[DEFAULT_SEED_USER["designation_code"]]

    if default_user is None:
        default_user = User(
            first_name=DEFAULT_SEED_USER["first_name"],
            last_name=DEFAULT_SEED_USER["last_name"],
            email=DEFAULT_SEED_USER["email"],
            password_hash=DEFAULT_SEED_USER["password"],
            role=role,
            designation=designation,
            employment_status="active",
            is_active=True,
        )
        session.add(default_user)
        session.flush()
        return True, False

    updated = False

    if default_user.first_name != DEFAULT_SEED_USER["first_name"]:
        default_user.first_name = DEFAULT_SEED_USER["first_name"]
        updated = True
    if default_user.last_name != DEFAULT_SEED_USER["last_name"]:
        default_user.last_name = DEFAULT_SEED_USER["last_name"]
        updated = True
    if default_user.role_id != role.id:
        default_user.role = role
        updated = True
    if default_user.designation_id != designation.id:
        default_user.designation = designation
        updated = True
    if default_user.employment_status != "active":
        default_user.employment_status = "active"
        updated = True
    if not default_user.is_active:
        default_user.is_active = True
        updated = True

    session.flush()
    return False, updated


def seed_defaults(session: Session) -> SeedSummary:
    _ensure_required_tables(session)

    roles_by_name, created_roles, existing_roles = _seed_roles(session)
    designations_by_code, created_designations, existing_designations = _seed_designations(session)
    created_skills, existing_skills = _seed_skills(session)
    default_user_created, default_user_updated = _seed_default_user(
        session,
        roles_by_name=roles_by_name,
        designations_by_code=designations_by_code,
    )
    session.commit()

    return SeedSummary(
        created_roles=created_roles,
        existing_roles=existing_roles,
        created_designations=created_designations,
        existing_designations=existing_designations,
        created_skills=created_skills,
        existing_skills=existing_skills,
        default_user_created=default_user_created,
        default_user_updated=default_user_updated,
    )


def main() -> None:
    print(f"Seeding database defaults into {get_database_url_for_logging()}")

    with SessionLocal() as session:
        try:
            summary = seed_defaults(session)
        except Exception:
            session.rollback()
            raise

    print(
        "Seed complete: "
        f"{summary.created_roles} roles created, {summary.existing_roles} roles already present, "
        f"{summary.created_designations} designations created, {summary.existing_designations} designations already present, "
        f"{summary.created_skills} skills created, {summary.existing_skills} skills already present."
    )

    if summary.default_user_created:
        print(
            "Default HR user created: "
            f"{DEFAULT_SEED_USER['email']} / {DEFAULT_SEED_USER['password']} "
            "(change this password immediately if you use the account beyond local setup)."
        )
    elif summary.default_user_updated:
        print(
            "Default HR user already existed and was reconciled to the expected HR/Manager profile. "
            "Existing password was preserved."
        )
    else:
        print("Default HR user already existed. Existing password was preserved.")


if __name__ == "__main__":
    main()
