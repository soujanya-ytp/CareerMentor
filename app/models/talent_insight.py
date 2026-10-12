from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import Date, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.mixins import CreatedAtMixin, UUIDPrimaryKeyMixin


class TalentInsight(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "talent_insights"
    __table_args__ = (UniqueConstraint("user_id", "snapshot_date", name="uq_talent_insights_user_date"),)

    user_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    snapshot_date: Mapped[date] = mapped_column(Date, nullable=False)
    potential_score: Mapped[int] = mapped_column(Integer, nullable=False)
    growth_percent: Mapped[int] = mapped_column(Integer, nullable=False)
    skill_growth_percent: Mapped[int] = mapped_column(Integer, nullable=False)
    talent_segment: Mapped[str | None] = mapped_column(String(100), nullable=True)
    top_skill: Mapped[str | None] = mapped_column(String(120), nullable=True)

    user = relationship("User", back_populates="talent_insights")
