from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class StoryJobBase(BaseModel):
    theme: str


class StoryJobResponse(BaseModel):
    job_id: str
    status: str
    created_at: datetime
    story_id: Optional[int] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None

    class Config:
        from_attributes = True


class CreateStoryJobCreate(StoryJobBase):
    pass
