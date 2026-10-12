from __future__ import annotations

from uuid import UUID

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class Roadmap(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "roadmaps"

    user_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    roadmap_data: Mapped[dict] = mapped_column(JSONB, nullable=False)
    generated_by: Mapped[str] = mapped_column(
        Enum("ai", "manager", "hr", "organization", name="roadmap_generated_by"),
        nullable=False,
    )

    user = relationship("User", back_populates="roadmaps")


CareerRoadmap = Roadmap
