#!/usr/bin/env python3
"""
HackNU25 Backend Server
FastAPI server with OpenAI GPT for PDF document analysis
Two endpoints: analyze-pdf (with AI) and parse-pdf (text extraction only)
"""

import os
import logging
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn

# Import our modules
from config.settings import settings
from models.response import PDFAnalysisResponse
from services.pdf_request import PDFRequestService

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    version=settings.app_version
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize request service
pdf_request_service = PDFRequestService()


# API Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": settings.app_title, 
        "version": settings.app_version,
        "description": settings.app_description,
        "endpoints": {
            "health": "/health",
            "analyze_pdf": "/api/v1/analyze-pdf (PDF → AI analysis)",
            "parse_pdf": "/api/v1/parse-pdf (PDF → text extraction only)",
            "docs": "/docs",
            "test_interface": "/test"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    openai_status = "connected" if settings.openai_api_key and settings.openai_client else "no_api_key"
    return {
        "status": "healthy",
        "openai_status": openai_status,
        "model": settings.openai_model
    }


@app.post("/api/v1/analyze-pdf", response_model=PDFAnalysisResponse)
async def analyze_pdf(
    file: UploadFile = File(...),
    include_raw_text: bool = Form(False, description="Include extracted text in response")
):
    """Analyze PDF resume with comprehensive AI analysis using OpenAI GPT"""
    return await pdf_request_service.process_analyze_request(file, include_raw_text)


@app.post("/api/v1/parse-pdf", response_model=PDFAnalysisResponse)
async def parse_pdf(
    file: UploadFile = File(...),
    include_raw_text: bool = Form(True, description="Include extracted text in response")
):
    """Extract text from PDF using PyPDF only (no AI analysis)"""
    return await pdf_request_service.process_parse_request(file, include_raw_text)


@app.get("/test")
async def serve_test_interface():
    """Serve the HTML test interface"""
    html_file_path = os.path.join(os.path.dirname(__file__), "pdf_test_interface.html")
    if os.path.exists(html_file_path):
        return FileResponse(html_file_path)
    else:
        raise HTTPException(status_code=404, detail="Test interface not found")


if __name__ == "__main__":
    logger.info("🚀 Starting HackNU25 Backend Server...")
    logger.info("📄 PDF processing with OpenAI GPT and text extraction")
    logger.info("🎯 Two specialized endpoints")
    
    print("🚀 Starting HackNU25 Backend Server...")
    print("📄 PDF processing with OpenAI GPT and text extraction")
    print("🎯 Two specialized endpoints")
    print("")
    
    if settings.openai_api_key and settings.openai_client:
        logger.info("✅ OpenAI API key configured")
        print("✅ OpenAI API key configured")
    else:
        logger.warning("⚠️ No OpenAI API key - AI analysis will not work")
        print("⚠️  No OpenAI API key - AI analysis will not work")
        print("   Set OPENAI_API_KEY environment variable for AI analysis")
    
    print("")
    print(f"🌐 API Documentation: http://{settings.host}:{settings.port}/docs")
    print("🤖 AI Analysis: POST /api/v1/analyze-pdf")
    print("📄 Text Extraction: POST /api/v1/parse-pdf")
    print(f"🧪 Test interface: http://{settings.host}:{settings.port}/test")
    print("🏥 Health check: GET /health")
    print("📝 Logs: hacknu25_server.log")
    
    logger.info(f"🌐 Server starting on http://{settings.host}:{settings.port}")
    
    uvicorn.run(
        app, 
        host=settings.host, 
        port=settings.port,
        reload=settings.reload,
        log_level="info"
    )