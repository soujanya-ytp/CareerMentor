from __future__ import annotations

from uuid import UUID

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class SkillGapAnalysis(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "skill_gap_analyses"
    __table_args__ = (
        UniqueConstraint("user_id", "career_goal_id", "skill_id", name="uq_skill_gap_user_goal_skill"),
    )

    user_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    career_goal_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("career_goals.id", ondelete="CASCADE"), nullable=False, index=True
    )
    skill_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True
    )
    current_level: Mapped[int] = mapped_column(Integer, nullable=False)
    required_level: Mapped[int] = mapped_column(Integer, nullable=False)
    priority: Mapped[str | None] = mapped_column(String(30), nullable=True)

    user = relationship("User", back_populates="skill_gap_analyses")
    career_goal = relationship("CareerGoal", back_populates="skill_gap_analyses")
    skill = relationship("Skill", back_populates="skill_gap_analyses")
