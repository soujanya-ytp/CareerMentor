from __future__ import annotations

from uuid import UUID

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class CareerRecommendation(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "career_recommendations"

    user_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    career_path_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("career_paths.id", ondelete="CASCADE"), nullable=False, index=True
    )
    match_score: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_order: Mapped[int] = mapped_column(Integer, nullable=False)
    recommendation_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    rationale: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    user = relationship("User", back_populates="career_recommendations")
    career_path = relationship("CareerPath", back_populates="career_recommendations")
