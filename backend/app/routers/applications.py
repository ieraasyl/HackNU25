from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.models.application import Application, ApplicationCreate, ApplicationRead, ApplicationStatusUpdate
from app.models.vacancy import Vacancy
from app.db.session import async_session
from app.utils.file_upload import save_uploaded_file, get_file_url

router = APIRouter(prefix="/api/applications", tags=["Applications"])

async def get_session():
    """Dependency for database session"""
    async with async_session() as session:
        yield session

@router.post("", response_model=ApplicationRead, status_code=201)
async def submit_application(
    vacancy_id: str = Form(...),
    name: str = Form(...),
    email: str = Form(...),
    phone: Optional[str] = Form(None),
    cover_letter: Optional[str] = Form(None),
    resume: UploadFile = File(...),
    session: AsyncSession = Depends(get_session)
):
    """
    Submit a job application
    
    - **vacancy_id**: ID of the vacancy being applied to
    - **name**: Applicant's full name
    - **email**: Applicant's email
    - **phone**: Applicant's phone number (optional)
    - **cover_letter**: Cover letter text (optional)
    - **resume**: Resume file (PDF, DOC, DOCX)
    """
    # Verify vacancy exists
    result = await session.execute(
        select(Vacancy).where(Vacancy.id == vacancy_id)
    )
    vacancy = result.scalar_one_or_none()
    
    if not vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    
    if vacancy.status != "active":
        raise HTTPException(status_code=400, detail="This vacancy is no longer accepting applications")
    
    # Save resume file
    try:
        resume_path = await save_uploaded_file(resume)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")
    
    # Create application
    application = Application(
        vacancy_id=vacancy_id,
        name=name,
        email=email,
        phone=phone,
        cover_letter=cover_letter,
        resume_url=resume_path,
        status="pending"
    )
    
    session.add(application)
    await session.commit()
    await session.refresh(application)
    
    return application

@router.get("", response_model=List[ApplicationRead])
async def get_applications(
    vacancy_id: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session)
):
    """
    Get list of applications (admin/HR only - authentication to be added)
    
    - **vacancy_id**: Filter by vacancy ID
    - **status**: Filter by application status
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    """
    query = select(Application)
    
    if vacancy_id:
        query = query.where(Application.vacancy_id == vacancy_id)
    
    if status:
        query = query.where(Application.status == status)
    
    query = query.offset(skip).limit(limit).order_by(Application.created_at.desc())
    
    result = await session.execute(query)
    applications = result.scalars().all()
    
    return applications

@router.get("/{application_id}", response_model=ApplicationRead)
async def get_application(
    application_id: str,
    session: AsyncSession = Depends(get_session)
):
    """
    Get details of a specific application
    
    - **application_id**: ID of the application
    """
    result = await session.execute(
        select(Application).where(Application.id == application_id)
    )
    application = result.scalar_one_or_none()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    return application

@router.patch("/{application_id}/status", response_model=ApplicationRead)
async def update_application_status(
    application_id: str,
    status_update: ApplicationStatusUpdate,
    session: AsyncSession = Depends(get_session)
):
    """
    Update application status (admin/HR only - authentication to be added)
    
    - **application_id**: ID of the application
    - **status_update**: New status (pending, reviewing, accepted, rejected)
    """
    allowed_statuses = ["pending", "reviewing", "accepted", "rejected"]
    if status_update.status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Allowed values: {', '.join(allowed_statuses)}"
        )
    
    result = await session.execute(
        select(Application).where(Application.id == application_id)
    )
    application = result.scalar_one_or_none()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    application.status = status_update.status
    from datetime import datetime
    application.updated_at = datetime.utcnow()
    
    await session.commit()
    await session.refresh(application)
    
    return application
