import uuid
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Cookie, Responce, BackgroundTasks
from sqlalchemy.orm import Session

from db.database import get_db, SessionLocal
from models.story import Story, StoryNode
from models.job import StoryJob
from schemas.story import (
    CreateStoryRequest, CompleteStoryResponce, CompleteStoryNodeResponce)
from schemas.job import StoryJobResponce

router = APIRouter(
    prefix="/stories",
    tags=["Stories"]
)

def get_session_id(session_id: Optional[str] = Cookie(None)):
    if session_id is None:
        raise HTTPException(status_code=401, detail="Session ID is not found")
    return session_id    
        