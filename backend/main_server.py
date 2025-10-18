#!/usr/bin/env python3
"""
HackNU25 Backend Server
FastAPI server with Google Gemini AI for PDF document analysis
Simplified, production-ready architecture
"""

import os
import io
from typing import Optional, List
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import pypdf
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("⚠️  GEMINI_API_KEY not found in environment. Set it or the server will use mock responses.")
    GEMINI_API_KEY = None

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    
# Initialize FastAPI
app = FastAPI(
    title="HackNU25 Backend API",
    description="PDF document analysis powered by Google Gemini AI - Clean, Simple, Production Ready",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChatRequest(BaseModel):
    message: str
    system_prompt: Optional[str] = None
    
class ChatResponse(BaseModel):
    response: str
    status: str

class PDFAnalysisResponse(BaseModel):
    success: bool
    extracted_text: Optional[str] = None
    analysis: Optional[str] = None
    metadata: Optional[dict] = None
    error: Optional[str] = None

# Gemini model instance
def get_gemini_model():
    """Get configured Gemini model instance"""
    if GEMINI_API_KEY:
        return genai.GenerativeModel('gemini-2.5-flash')  # Stable and available
    return None

def extract_text_from_pdf(pdf_content: bytes) -> tuple[str, dict]:
    """Extract text and metadata from PDF"""
    try:
        pdf_stream = io.BytesIO(pdf_content)
        reader = pypdf.PdfReader(pdf_stream)
        
        # Extract text from all pages
        text = ""
        for page_num, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text.strip():
                text += f"Page {page_num + 1}:\n{page_text}\n\n"
        
        # Get metadata
        metadata = {
            "pages": len(reader.pages),
            "size_kb": len(pdf_content) / 1024,
            "has_text": bool(text.strip())
        }
        
        # Try to get PDF info
        if reader.metadata:
            pdf_info = reader.metadata
            metadata.update({
                "title": pdf_info.get("/Title", "Unknown"),
                "author": pdf_info.get("/Author", "Unknown"),
                "subject": pdf_info.get("/Subject", "Unknown"),
                "creator": pdf_info.get("/Creator", "Unknown")
            })
        
        return text.strip(), metadata
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing PDF: {str(e)}")

async def analyze_with_gemini(text: str, prompt: str) -> str:
    """Analyze text using Gemini AI"""
    if not GEMINI_API_KEY:
        return f"Mock analysis (no API key): Based on the document content, this appears to be a professional document containing: {text[:200]}..."
    
    try:
        model = get_gemini_model()
        
        # Create comprehensive resume analysis prompt
        resume_analysis_prompt = f"""
You are an expert ATS (Applicant Tracking System) analyzer. Extract and structure the following information from this resume/CV document:

### 1. PERSONAL INFORMATION
- Full Name
- Email Address
- Phone Number
- Location (City, Country/State)
- LinkedIn Profile
- GitHub/Portfolio Links
- Professional Title/Current Position
- Professional Summary/Objective

### 2. WORK EXPERIENCE
For each job position, extract:
- Job Title
- Company Name
- Employment Duration (Start Date - End Date)
- Company Location
- Key Responsibilities (bullet points)
- Achievements with quantifiable results
- Technologies/Tools used
- Industry sector

### 3. EDUCATION
For each educational qualification:
- Degree Type and Name
- Institution/University Name
- Graduation Year
- Major/Field of Study
- GPA (if mentioned)
- Relevant Coursework
- Academic Honors/Awards

### 4. TECHNICAL SKILLS
Categorize into:
- Programming Languages
- Frameworks/Libraries
- Databases
- Cloud Platforms
- Development Tools
- Software/Applications

### 5. SOFT SKILLS
- Leadership abilities
- Communication skills
- Problem-solving capabilities
- Teamwork experience
- Other interpersonal skills

### 6. LANGUAGES
- Language name
- Proficiency level (Native, Fluent, Intermediate, Beginner)

### 7. PROJECTS (if applicable)
For each project:
- Project Name
- Duration
- Technologies Used
- Project Description
- Your Role
- Outcome/Impact

### 8. CERTIFICATIONS & ACHIEVEMENTS
- Certification Name
- Issuing Organization
- Issue Date/Expiration
- Professional Awards
- Publications/Research

### 9. ADDITIONAL INFORMATION
- Volunteer Work
- Professional Memberships
- Conferences/Workshops
- Relevant Hobbies/Interests

Document Content:
{text}

Please provide a comprehensive, structured analysis in JSON-like format with clear sections and bullet points. If any section is not present in the document, mention "Not specified" or "Not mentioned".

Focus on extracting factual information and quantifiable achievements. Highlight any standout qualifications or unique aspects of the candidate's profile.
"""
        
        response = model.generate_content(resume_analysis_prompt)
        return response.text
        
    except Exception as e:
        return f"Gemini analysis failed: {str(e)}. Please check your API key and try again."

# API Endpoints

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "HackNU25 Backend API", 
        "version": "1.0.0",
        "description": "PDF processing with keyword analysis and text extraction",
        "endpoints": {
            "health": "/health",
            "analyze_pdf": "/api/v1/analyze-pdf (PDF + keywords → AI analysis)",
            "parse_resume": "/api/v1/parse-resume (PDF → PyPDF text extraction)",
            "docs": "/docs",
            "test_interface": "/test"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    gemini_status = "connected" if GEMINI_API_KEY else "no_api_key"
    return {
        "status": "healthy",
        "gemini_status": gemini_status,
        "model": "gemini-pro"
    }

@app.post("/api/v1/analyze-pdf", response_model=PDFAnalysisResponse)
async def analyze_pdf(
    file: UploadFile = File(...),
    keywords: str = Form(..., description="Keywords to analyze in the PDF"),
    extract_text: bool = Form(False, description="Include extracted text in response")
):
    """Analyze PDF based on provided keywords using Gemini AI"""
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Read and process PDF
        pdf_content = await file.read()
        
        if not pdf_content:
            raise HTTPException(status_code=400, detail="Empty PDF file")
        
        # Extract text and metadata
        extracted_text, metadata = extract_text_from_pdf(pdf_content)
        
        if not extracted_text:
            return PDFAnalysisResponse(
                success=False,
                error="No text could be extracted from the PDF. The file might be image-based or corrupted.",
                metadata=metadata
            )
        
        # Create keyword-based analysis prompt
        keyword_prompt = f"""
Analyze this document based on the following keywords: {keywords}

Please provide a comprehensive analysis focusing on:
1. How the document relates to these keywords
2. Specific mentions or references to these keywords
3. Context and relevance of these keywords in the document
4. Any related concepts or themes

Keywords to focus on: {keywords}

Document Content:
{extracted_text}

Provide a structured analysis with clear sections and bullet points.
"""
        
        # Analyze with Gemini using keyword-based prompt
        analysis = await analyze_with_gemini(extracted_text, keyword_prompt)
        
        return PDFAnalysisResponse(
            success=True,
            extracted_text=extracted_text if extract_text else None,
            analysis=analysis,
            metadata=metadata
        )
        
    except HTTPException:
        raise
    except Exception as e:
        return PDFAnalysisResponse(
            success=False,
            error=f"Analysis failed: {str(e)}"
        )

@app.post("/api/v1/parse-resume", response_model=PDFAnalysisResponse)
async def parse_resume(
    file: UploadFile = File(...),
    include_raw_text: bool = Form(True, description="Include extracted text in response")
):
    """Extract text from PDF resume using PyPDF (no AI analysis)"""
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Read and process PDF
        pdf_content = await file.read()
        
        if not pdf_content:
            raise HTTPException(status_code=400, detail="Empty PDF file")
        
        # Extract text and metadata using PyPDF only
        extracted_text, metadata = extract_text_from_pdf(pdf_content)
        
        if not extracted_text:
            return PDFAnalysisResponse(
                success=False,
                error="No text could be extracted from the PDF. The file might be image-based or corrupted.",
                metadata=metadata
            )
        
        # Return extracted text without AI analysis
        return PDFAnalysisResponse(
            success=True,
            extracted_text=extracted_text if include_raw_text else None,
            analysis="Text extraction completed successfully using PyPDF. No AI analysis performed.",
            metadata=metadata
        )
        
    except HTTPException:
        raise
    except Exception as e:
        return PDFAnalysisResponse(
            success=False,
            error=f"Text extraction failed: {str(e)}"
        )

@app.get("/test")
async def serve_test_interface():
    """Serve the HTML test interface"""
    from fastapi.responses import FileResponse
    import os
    
    html_file_path = os.path.join(os.path.dirname(__file__), "pdf_test_interface.html")
    if os.path.exists(html_file_path):
        return FileResponse(html_file_path)
    else:
        raise HTTPException(status_code=404, detail="Test interface not found")

if __name__ == "__main__":
    print("🚀 Starting HackNU25 Backend Server...")
    print("📄 PDF processing with keyword analysis and text extraction")
    print("🎯 Two specialized endpoints")
    print("")
    
    if GEMINI_API_KEY:
        print("✅ Gemini API key configured")
    else:
        print("⚠️  No Gemini API key - keyword analysis will not work")
        print("   Set GEMINI_API_KEY environment variable for AI analysis")
        print("   Get free key: https://makersuite.google.com/app/apikey")
    
    print("")
    print("🌐 API Documentation: http://127.0.0.1:8001/docs")
    print("� Keyword analysis: POST /api/v1/analyze-pdf")
    print("� Text extraction: POST /api/v1/parse-resume")
    print("🧪 Test interface: http://127.0.0.1:8001/test")
    print("🏥 Health check: GET /health")
    
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=8001,
        log_level="info"
    )