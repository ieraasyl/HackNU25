from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class Application(SQLModel, table=True):
    """Job application model"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    vacancy_id: str = Field(foreign_key="vacancy.id", index=True)
    name: str
    email: str = Field(index=True)
    phone: Optional[str] = None
    cover_letter: Optional[str] = None
    resume_url: Optional[str] = None  # URL/path to uploaded resume
    resume_text: Optional[str] = None  # Extracted text from resume
    status: str = Field(default="pending")  # pending, reviewing, accepted, rejected
    ai_match_score: Optional[float] = None  # AI-calculated fit score (0-100)
    ai_matching_sections: Optional[str] = None  # AI-extracted relevant sections
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ApplicationCreate(SQLModel):
    """Schema for creating a new application"""
    vacancy_id: str
    name: str
    email: str
    phone: Optional[str] = None
    cover_letter: Optional[str] = None

class ApplicationRead(SQLModel):
    """Schema for reading application data"""
    id: str
    vacancy_id: str
    name: str
    email: str
    phone: Optional[str]
    cover_letter: Optional[str]
    resume_url: Optional[str]
    status: str
    ai_match_score: Optional[float]
    created_at: datetime
    updated_at: datetime

class ApplicationStatusUpdate(SQLModel):
    """Schema for updating application status"""
    status: str  # pending, reviewing, accepted, rejected
