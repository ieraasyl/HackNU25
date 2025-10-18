"""
PDF analysis service using OpenAI GPT for resume analysis
"""

from pdf_utils import analyze_with_openai
from models.response import StructuredAnalysis


class PDFAnalyzerService:
    """Service for AI-powered PDF analysis using OpenAI GPT"""
    
    @staticmethod
    async def analyze_with_openai(text: str) -> StructuredAnalysis:
        """Analyze resume text using OpenAI GPT and return structured JSON data"""
        return await analyze_with_openai(text)