import uuid
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Cookie, Response, BackgroundTasks
from sqlalchemy.orm import Session
from db.database import get_db, SessionLocal

from models.story import Story, StoryNode
from models.job import StoryJob
from schemas.story import (
    CompleteStoryNodeResponse,
    CompleteStoryResponse,
    CreateStoryRequest,
)

from schemas.job import StoryJobResponse

router = APIRouter(
    prefix="/stories",
    tags=["stories"],
)


def get_session_id(session_id: Optional[str] = Cookie(None)) -> str:
    if session_id is None:
        session_id = str(uuid.uuid4())
    return session_id


@router.post("/recreate", response_model=StoryJobResponse)
def create_story_job(
    request: CreateStoryRequest,
    background_tasks: BackgroundTasks,
    response: Response,
    db: Session = Depends(get_db),
    session_id: str = Depends(get_session_id),
):
    response.set_cookie(key="session_id", value=session_id, httponly=True)

    job_id = str(uuid.uuid4())
    job = StoryJob(
        job_id=job_id, theme=request.theme, status="pending", session_id=session_id
    )
    db.add(job)
    db.commit()

    return job


def generate_story_task(job_id: str, theme: str, session_id: str):
    # Simulate story generation logic
    db = SessionLocal()
    try:
        job = db.query(StoryJob).filter(StoryJob.id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        try:
            job.status = "in_progress"
            db.commit()

            story = {}

            job.story_id = 1
            job.status = "completed"
            job.completed_at = datetime.now()
            db.commit()
        except Exception as e:
            job.status = "failed"
            job.completed_at = datetime.now()
            job.error_message = str(e)
            db.commit()
    finally:
        db.close()


@router.get("/{story_id}/complete", response_model=CompleteStoryResponse)
def get_complet_story(story_id: int, db: Session = Depends(get_db)):
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    return story

def build_complete_story_tree(db: Session, story: Story) -> CompleteStoryResponse:
    return CompleteStoryResponse.from_orm(story)
