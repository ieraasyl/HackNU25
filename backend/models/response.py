"""
Pydantic models for HackNU25 Backend API
"""

from typing import Optional
from pydantic import BaseModel


class PDFAnalysisResponse(BaseModel):
    """Response model for PDF analysis endpoints"""
    success: bool
    extracted_text: Optional[str] = None
    analysis: Optional[str] = None
    metadata: Optional[dict] = None
    error: Optional[str] = None