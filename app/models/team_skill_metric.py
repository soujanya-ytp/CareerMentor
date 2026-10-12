from __future__ import annotations

from uuid import UUID

from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.mixins import CreatedAtMixin, UUIDPrimaryKeyMixin


class TeamSkillMetric(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "team_skill_metrics"
    __table_args__ = (
        UniqueConstraint("team_insight_id", "skill_id", name="uq_team_skill_metrics_insight_skill"),
    )

    team_insight_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("team_insights.id", ondelete="CASCADE"), nullable=False, index=True
    )
    skill_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True
    )
    members_with_skill: Mapped[int] = mapped_column(Integer, nullable=False)
    member_count: Mapped[int] = mapped_column(Integer, nullable=False)
    coverage_percent: Mapped[int] = mapped_column(Integer, nullable=False)

    team_insight = relationship("TeamInsight", back_populates="skill_metrics")
    skill = relationship("Skill", back_populates="team_skill_metrics")
