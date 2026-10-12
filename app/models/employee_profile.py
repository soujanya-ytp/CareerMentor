from __future__ import annotations

from uuid import UUID

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class EmployeeProfile(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "employee_profiles"

    user_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True, index=True
    )
    current_role_title: Mapped[str] = mapped_column(String(150), nullable=False)
    experience_years: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    career_goal_summary: Mapped[str | None] = mapped_column(String(255), nullable=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)

    user = relationship("User", back_populates="employee_profile")
