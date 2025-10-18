"""
PDF analysis service using OpenAI GPT for resume analysis
"""

from pdf_utils import analyze_with_openai


class PDFAnalyzerService:
    """Service for AI-powered PDF analysis using OpenAI GPT"""
    
    @staticmethod
    async def analyze_with_openai(text: str) -> str:
        """Analyze resume text using OpenAI GPT with predefined comprehensive analysis"""
        return await analyze_with_openai(text)