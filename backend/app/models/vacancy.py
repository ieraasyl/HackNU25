from sqlmodel import SQLModel, Field, Column, TIMESTAMP
from sqlalchemy import JSON
from typing import Optional, Dict, Any
from datetime import datetime, timezone
import uuid

def utc_now():
    """Return current UTC time as timezone-aware datetime"""
    return datetime.now(timezone.utc)

class Vacancy(SQLModel, table=True):
    """Job vacancy/position model"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    title: str = Field(index=True)
    description: str
    company: str
    location: str
    salary_min: int
    salary_max: int
    employment_type: str = Field(default="Full-time")  # Full-time, Part-time, Contract, Internship
    requirements: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))  # JSON field for requirements
    requirements_parsed: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))  # Parsed requirements
    created_at: datetime = Field(default_factory=utc_now, sa_column=Column(TIMESTAMP(timezone=True)))
    updated_at: datetime = Field(default_factory=utc_now, sa_column=Column(TIMESTAMP(timezone=True)))

class VacancyCreate(SQLModel):
    """Schema for creating a new vacancy"""
    title: str
    description: str
    company: str
    location: str
    salary_min: int
    salary_max: int
    employment_type: str = "Full-time"
    requirements: Dict[str, Any] = {}
    requirements_parsed: Optional[Dict[str, Any]] = None

class VacancyRead(SQLModel):
    """Schema for reading vacancy data"""
    id: str
    title: str
    description: str
    company: str
    location: str
    salary_min: int
    salary_max: int
    employment_type: str
    requirements: Dict[str, Any]
    requirements_parsed: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime
