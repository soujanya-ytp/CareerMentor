from __future__ import annotations

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class Designation(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "designations"

    designation_code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    designation_name: Mapped[str] = mapped_column(String(120), nullable=False)
    level_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    users = relationship("User", back_populates="designation")
    career_goals = relationship("CareerGoal", back_populates="target_designation")
    career_paths = relationship("CareerPath", back_populates="target_designation")
