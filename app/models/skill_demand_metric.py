from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import Date, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.mixins import CreatedAtMixin, UUIDPrimaryKeyMixin


class SkillDemandMetric(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "skill_demand_metrics"
    __table_args__ = (
        UniqueConstraint(
            "skill_id",
            "department_id",
            "snapshot_date",
            name="uq_skill_demand_metrics_skill_department_date",
        ),
    )

    skill_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True
    )
    department_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("departments.id", ondelete="CASCADE"), nullable=False, index=True
    )
    snapshot_date: Mapped[date] = mapped_column(Date, nullable=False)
    supply_percent: Mapped[int] = mapped_column(Integer, nullable=False)
    demand_percent: Mapped[int] = mapped_column(Integer, nullable=False)
    market_trend: Mapped[str | None] = mapped_column(String(100), nullable=True)

    skill = relationship("Skill", back_populates="skill_demand_metrics")
    department = relationship("Department", back_populates="skill_demand_metrics")
