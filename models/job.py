from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from db.database import Base


class StoryJob(Base):
    __tablename__ = "story_jobs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    job_id: Mapped[str] = mapped_column(String, index=True, unique=True)
    session_id: Mapped[str] = mapped_column(String, index=True)
    theme: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)
    story_id: Mapped[Optional[int]] = mapped_column(ForeignKey("stories.id"), nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    story = relationship("Story", back_populates="jobs")
