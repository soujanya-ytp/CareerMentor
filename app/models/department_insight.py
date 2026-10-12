from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID

from sqlalchemy import Date, ForeignKey, Integer, Numeric, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.mixins import CreatedAtMixin, UUIDPrimaryKeyMixin


class DepartmentInsight(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "department_insights"
    __table_args__ = (
        UniqueConstraint("department_id", "snapshot_date", name="uq_department_insights_department_date"),
    )

    department_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("departments.id", ondelete="CASCADE"), nullable=False, index=True
    )
    snapshot_date: Mapped[date] = mapped_column(Date, nullable=False)
    team_size: Mapped[int] = mapped_column(Integer, nullable=False)
    readiness_score: Mapped[int] = mapped_column(Integer, nullable=False)
    growth_percent: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)

    department = relationship("Department", back_populates="department_insights")
