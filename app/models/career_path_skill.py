from __future__ import annotations

from uuid import UUID

from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.mixins import CreatedAtMixin, UUIDPrimaryKeyMixin


class CareerPathSkill(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "career_path_skills"
    __table_args__ = (
        UniqueConstraint("career_path_id", "skill_id", name="uq_career_path_skills_path_skill"),
    )

    career_path_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("career_paths.id", ondelete="CASCADE"), nullable=False, index=True
    )
    skill_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True
    )
    required_level: Mapped[int] = mapped_column(Integer, nullable=False)
    weight: Mapped[int] = mapped_column(Integer, nullable=False, default=1, server_default="1")

    career_path = relationship("CareerPath", back_populates="career_path_skills")
    skill = relationship("Skill", back_populates="career_path_skills")
