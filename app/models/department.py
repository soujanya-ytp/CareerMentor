from __future__ import annotations

from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class Department(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "departments"

    department_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    department_name: Mapped[str] = mapped_column(String(120), nullable=False)
    manager_user_id: Mapped[UUID | None] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")

    manager = relationship(
        "User", foreign_keys=[manager_user_id], back_populates="managed_departments"
    )
    users = relationship("User", back_populates="department", foreign_keys="User.department_id")
    teams = relationship("Team", back_populates="department", cascade="all, delete-orphan")
    department_insights = relationship(
        "DepartmentInsight", back_populates="department", cascade="all, delete-orphan"
    )
    skill_demand_metrics = relationship(
        "SkillDemandMetric", back_populates="department", cascade="all, delete-orphan"
    )
