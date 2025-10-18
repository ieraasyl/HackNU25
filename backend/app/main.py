#!/usr/bin/env python3
"""
HackNU25 Main Application Entry Point
Runs the PDF analysis server from the app folder
"""

import sys
import os
import uvicorn
import logging

# Add the backend directory to the Python path so we can import from parent directory
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

# Import the server from the parent directory
from server import app
from config.settings import settings

logger = logging.getLogger(__name__)


def main():
    """Main entry point for the HackNU25 application"""
    logger.info("🚀 Starting HackNU25 Application from app/main.py")
    logger.info("📄 PDF Analysis Server with FastAPI")
    
    print("🚀 Starting HackNU25 Application from app/main.py")
    print("📄 PDF Analysis Server with FastAPI")
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


if __name__ == "__main__":
    main()
