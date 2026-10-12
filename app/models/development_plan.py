from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class DevelopmentPlan(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "development_plans"

    user_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    career_goal_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("career_goals.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="draft", server_default="draft")
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    target_completion_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    user = relationship("User", back_populates="development_plans")
    career_goal = relationship("CareerGoal", back_populates="development_plans")
    steps = relationship(
        "DevelopmentPlanStep", back_populates="plan", cascade="all, delete-orphan"
    )
