from __future__ import annotations

from datetime import date

from sqlalchemy import Date, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class OrgInsight(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "org_insights"
    __table_args__ = (UniqueConstraint("snapshot_date", name="uq_org_insights_snapshot_date"),)

    snapshot_date: Mapped[date] = mapped_column(Date, nullable=False)
    total_employees: Mapped[int] = mapped_column(Integer, nullable=False)
    department_count: Mapped[int] = mapped_column(Integer, nullable=False)
    avg_readiness_score: Mapped[int] = mapped_column(Integer, nullable=False)
    open_positions: Mapped[int] = mapped_column(Integer, nullable=False)
    summary_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
