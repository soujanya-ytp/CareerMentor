from __future__ import annotations

from uuid import UUID

from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.mixins import CreatedAtMixin, UUIDPrimaryKeyMixin


class WhatIfSimulation(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "whatif_simulations"

    user_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    career_path_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("career_paths.id", ondelete="CASCADE"), nullable=False, index=True
    )
    cloud_skill_level: Mapped[int | None] = mapped_column(Integer, nullable=True)
    leadership_skill_level: Mapped[int | None] = mapped_column(Integer, nullable=True)
    projected_readiness: Mapped[int | None] = mapped_column(Integer, nullable=True)
    projected_timeline_months: Mapped[int | None] = mapped_column(Integer, nullable=True)
    key_recommendation: Mapped[str | None] = mapped_column(Text, nullable=True)

    user = relationship("User", back_populates="whatif_simulations")
    career_path = relationship("CareerPath", back_populates="whatif_simulations")
