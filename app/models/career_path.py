from __future__ import annotations

from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class CareerPath(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "career_paths"

    title: Mapped[str] = mapped_column(String(150), nullable=False)
    target_designation_id: Mapped[UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("designations.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    track: Mapped[str | None] = mapped_column(String(100), nullable=True)
    difficulty: Mapped[str | None] = mapped_column(String(50), nullable=True)
    growth_outlook: Mapped[str | None] = mapped_column(String(100), nullable=True)
    default_timeline_months: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")

    target_designation = relationship("Designation", back_populates="career_paths")
    career_path_skills = relationship(
        "CareerPathSkill", back_populates="career_path", cascade="all, delete-orphan"
    )
    career_recommendations = relationship(
        "CareerRecommendation", back_populates="career_path", cascade="all, delete-orphan"
    )
    whatif_simulations = relationship(
        "WhatIfSimulation", back_populates="career_path", cascade="all, delete-orphan"
    )
