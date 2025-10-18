from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

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
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

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
    created_at: datetime
    updated_at: datetime
