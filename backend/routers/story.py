import uuid
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Cookie, Responce, BackgroundTasks
from sqlalchemy.orm import Session

from db.database import get_db, SessionLocal
from models.story import Story, StoryNode
from models.job import StoryJob
from schemas.story import (
    CreateStoryRequest, CompleteStoryResponse, CompleteStoryNodeResponse)
from schemas.job import StoryJobResponce

router = APIRouter(
    prefix="/stories",
    tags=["Stories"]
)

def get_session_id(session_id: Optional[str] = Cookie(None)):
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id    

@router.post("/create", response_model = StoryJopResponce)
def create_story(
    request: CreateStoryRequest,
    background_tasks: BackgroundTasks,
    responce: Responce,
    session_id: str = Depends(get_session_id),
    db: Session = Depends(get_db)
):
    responce.set_cookie(key="session_id", value=session_id, httponly=True)

    job_id = StoryJob(
        job_id = job_id,
        session_id = session_id,
        theme = request.theme,
        status = "pending"
    )   
    db.add(job)
    db.commit()

    #todo add background tasks, generate story
    return job

def generate_story_task(job_id: str, theme: str, session_id: str):
    db= SessionLocal()          
    try:
        job = db.query(StoryJob).filter(StoryJob.job_id  == job_id).first()

        if not job:
            return

        try: 
            job.status = "in_progress"
            db.commit()  

            story={}

            job.story_id = 1
            job.status = "completed"
            job.completed_at = datetime.now()
            db.commit()

        except Exception as e:
            job.status = "failed"
            job.completed_at = datetime.now()
            job.error = str(e)
            db.commit()    
    finally: 
        db.close()


@router.get("/{story_id}/complete", responce_model = CompleteStoryResponse)
def get_complete_story(story_id: int, db: Session = Depends(get_db)):
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    return story

def build_complete_story_tree(db: Session, story: Story) -> CompleteStoryResponse:
    pass    