from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class UserRole(str, Enum):
    employee = "employee"
    manager = "manager"
    hr = "hr"
    organization_admin = "organization_admin"


class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "users"

    role_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("roles.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    designation_id: Mapped[UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("designations.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    department_id: Mapped[UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("departments.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    manager_id: Mapped[UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    first_name: Mapped[str] = mapped_column(String(80), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    employment_status: Mapped[str] = mapped_column(
        String(50), nullable=False, default="active", server_default="active"
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true", index=True
    )
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    role = relationship("Role", back_populates="users")
    designation = relationship("Designation", back_populates="users")
    department = relationship("Department", back_populates="users", foreign_keys=[department_id])
    manager = relationship(
        "User",
        remote_side="User.id",
        back_populates="direct_reports",
        foreign_keys=[manager_id],
    )
    direct_reports = relationship("User", back_populates="manager", foreign_keys=[manager_id])
    managed_departments = relationship(
        "Department", foreign_keys="Department.manager_user_id", back_populates="manager"
    )
    auth_sessions = relationship("AuthSession", back_populates="user", cascade="all, delete-orphan")
    employee_profile = relationship(
        "EmployeeProfile", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    user_skills = relationship("UserSkill", back_populates="user", cascade="all, delete-orphan")
    career_goals = relationship("CareerGoal", back_populates="user", cascade="all, delete-orphan")
    readiness_assessments = relationship(
        "ReadinessAssessment", back_populates="user", cascade="all, delete-orphan"
    )
    skill_gap_analyses = relationship(
        "SkillGapAnalysis", back_populates="user", cascade="all, delete-orphan"
    )
    career_recommendations = relationship(
        "CareerRecommendation", back_populates="user", cascade="all, delete-orphan"
    )
    whatif_simulations = relationship(
        "WhatIfSimulation", back_populates="user", cascade="all, delete-orphan"
    )
    development_plans = relationship(
        "DevelopmentPlan", back_populates="user", cascade="all, delete-orphan"
    )
    roadmaps = relationship("Roadmap", back_populates="user", cascade="all, delete-orphan")
    learning_recommendations = relationship(
        "LearningRecommendation", back_populates="user", cascade="all, delete-orphan"
    )
    chat_history = relationship("ChatHistory", back_populates="user", cascade="all, delete-orphan")
    managed_teams = relationship(
        "Team",
        back_populates="manager",
        cascade="all, delete-orphan",
        foreign_keys="Team.manager_user_id",
    )
    team_memberships = relationship(
        "TeamMember", back_populates="user", cascade="all, delete-orphan"
    )
    talent_insights = relationship(
        "TalentInsight", back_populates="user", cascade="all, delete-orphan"
    )
    audit_logs = relationship("AuditLog", back_populates="actor")

    @property
    def full_name(self) -> str:
        return " ".join(part for part in [self.first_name, self.last_name] if part).strip()

    @property
    def role_name(self) -> str | None:
        if self.role is None:
            return None
        return self.role.role_name
    
    @property
    def designation_name(self) -> str | None:
        if self.designation is None:
            return None
        print('-------', self.designation)
        return self.designation.designation_name
