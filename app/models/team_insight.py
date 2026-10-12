from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import Date, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.mixins import CreatedAtMixin, UUIDPrimaryKeyMixin


class TeamInsight(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "team_insights"
    __table_args__ = (UniqueConstraint("team_id", "snapshot_date", name="uq_team_insights_team_date"),)

    team_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("teams.id", ondelete="CASCADE"), nullable=False, index=True
    )
    snapshot_date: Mapped[date] = mapped_column(Date, nullable=False)
    team_size: Mapped[int] = mapped_column(Integer, nullable=False)
    avg_readiness_score: Mapped[int] = mapped_column(Integer, nullable=False)
    critical_gap_count: Mapped[int] = mapped_column(Integer, nullable=False)
    summary_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    team = relationship("Team", back_populates="insights")
    skill_metrics = relationship(
        "TeamSkillMetric", back_populates="team_insight", cascade="all, delete-orphan"
    )
