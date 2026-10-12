from __future__ import annotations

from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class LearningRecommendation(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "learning_recommendations"

    user_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    recommendations: Mapped[dict] = mapped_column(JSONB, nullable=False)

    user = relationship("User", back_populates="learning_recommendations")
