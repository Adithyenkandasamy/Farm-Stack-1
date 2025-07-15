import uuid
from typing import Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from models.job import StoryJob
from schemas.job import StoryJobResponse
from core.story_generator import StoryGenerator

router = APIRouter(
    prefix = "/jobs",
    tags = ["jobs"] 
)

@router.get("/{job_id}", response_model = StoryJobResponse)
def get_job_status(job_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a job by ID. If the job is still in the **pending** state,
    trigger story generation synchronously so the client does not need to
    poll another endpoint.
    """
    job = db.query(StoryJob).filter(StoryJob.job_id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # If the story has not yet been generated, do it now
    if job.status == "pending":
        try:
            job.status = "in_progress"
            db.commit()

            story = StoryGenerator.generate_story(db, job.session_id, job.theme)

            job.story_id = story.id
            job.completed_at = datetime.now()
            job.status = "completed"
            db.commit()
        except Exception as e:
            job.status = "failed"
            job.error = str(e)
            job.completed_at = datetime.now()
            db.commit()

    return job