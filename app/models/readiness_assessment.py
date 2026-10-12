from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import Date, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.mixins import CreatedAtMixin, UUIDPrimaryKeyMixin


class ReadinessAssessment(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "readiness_assessments"
    __table_args__ = (
        UniqueConstraint("user_id", "career_goal_id", "assessed_on", name="uq_readiness_user_goal_date"),
    )

    user_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    career_goal_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("career_goals.id", ondelete="CASCADE"), nullable=False, index=True
    )
    readiness_score: Mapped[int] = mapped_column(Integer, nullable=False)
    growth_score: Mapped[int] = mapped_column(Integer, nullable=False)
    skills_matched: Mapped[int] = mapped_column(Integer, nullable=False)
    skills_total: Mapped[int] = mapped_column(Integer, nullable=False)
    assessed_on: Mapped[date] = mapped_column(Date, nullable=False)
    assessment_source: Mapped[str | None] = mapped_column(String(100), nullable=True)
    summary_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    user = relationship("User", back_populates="readiness_assessments")
    career_goal = relationship("CareerGoal", back_populates="readiness_assessments")
