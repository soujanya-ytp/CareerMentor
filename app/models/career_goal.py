from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class CareerGoal(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "career_goals"

    user_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    target_designation_id: Mapped[UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("designations.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    target_role_title: Mapped[str] = mapped_column(String(150), nullable=False)
    target_track: Mapped[str | None] = mapped_column(String(100), nullable=True)
    target_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", server_default="active")

    user = relationship("User", back_populates="career_goals")
    target_designation = relationship("Designation", back_populates="career_goals")
    readiness_assessments = relationship(
        "ReadinessAssessment", back_populates="career_goal", cascade="all, delete-orphan"
    )
    skill_gap_analyses = relationship(
        "SkillGapAnalysis", back_populates="career_goal", cascade="all, delete-orphan"
    )
    development_plans = relationship(
        "DevelopmentPlan", back_populates="career_goal", cascade="all, delete-orphan"
    )
