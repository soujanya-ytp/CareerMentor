from __future__ import annotations

from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class Skill(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "skills"

    name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True, index=True)
    category: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true"
    )

    user_skills = relationship("UserSkill", back_populates="skill", cascade="all, delete-orphan")
    career_path_skills = relationship(
        "CareerPathSkill", back_populates="skill", cascade="all, delete-orphan"
    )
    skill_gap_analyses = relationship(
        "SkillGapAnalysis", back_populates="skill", cascade="all, delete-orphan"
    )
    team_skill_metrics = relationship(
        "TeamSkillMetric", back_populates="skill", cascade="all, delete-orphan"
    )
    skill_demand_metrics = relationship(
        "SkillDemandMetric", back_populates="skill", cascade="all, delete-orphan"
    )
