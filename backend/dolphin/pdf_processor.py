"""
PDF Processing utilities for Dolphin ByteDance integration
"""

import base64
import io
from typing import Optional, Dict, Any, List
try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class PDFProcessor:
    """
    Handle PDF file processing for ByteDance API
    """
    
    @staticmethod
    async def extract_text_from_pdf(pdf_content: bytes) -> str:
        """
        Extract text content from PDF bytes
        
        Args:
            pdf_content: PDF file content as bytes
            
        Returns:
            Extracted text content
        """
        try:
            if PdfReader is None:
                raise ValueError("pypdf library not installed. Install with: pip install pypdf")
                
            # Create a PDF reader from bytes
            pdf_stream = io.BytesIO(pdf_content)
            pdf_reader = PdfReader(pdf_stream)
            
            # Extract text from all pages
            text_content = ""
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text.strip():
                        text_content += f"\n--- Page {page_num + 1} ---\n"
                        text_content += page_text
                        text_content += "\n"
                except Exception as e:
                    logger.warning(f"Could not extract text from page {page_num + 1}: {e}")
                    continue
            
            if not text_content.strip():
                raise ValueError("No text content could be extracted from PDF")
                
            return text_content.strip()
            
        except Exception as e:
            logger.error(f"PDF text extraction failed: {e}")
            raise ValueError(f"Failed to process PDF: {str(e)}")
    
    @staticmethod
    def encode_pdf_to_base64(pdf_content: bytes) -> str:
        """
        Encode PDF content to base64 string
        
        Args:
            pdf_content: PDF file content as bytes
            
        Returns:
            Base64 encoded string
        """
        try:
            return base64.b64encode(pdf_content).decode('utf-8')
        except Exception as e:
            logger.error(f"PDF base64 encoding failed: {e}")
            raise ValueError(f"Failed to encode PDF: {str(e)}")
    
    @staticmethod
    def get_pdf_metadata(pdf_content: bytes) -> Dict[str, Any]:
        """
        Extract metadata from PDF
        
        Args:
            pdf_content: PDF file content as bytes
            
        Returns:
            Dictionary containing PDF metadata
        """
        try:
            if PdfReader is None:
                raise ValueError("pypdf library not installed")
                
            pdf_stream = io.BytesIO(pdf_content)
            pdf_reader = PdfReader(pdf_stream)
            
            metadata = {
                "num_pages": len(pdf_reader.pages),
                "size_bytes": len(pdf_content),
                "size_kb": round(len(pdf_content) / 1024, 2)
            }
            
            # Extract document info if available
            if pdf_reader.metadata:
                doc_info = pdf_reader.metadata
                metadata.update({
                    "title": str(doc_info.get("/Title", "")) if doc_info.get("/Title") else None,
                    "author": str(doc_info.get("/Author", "")) if doc_info.get("/Author") else None,
                    "subject": str(doc_info.get("/Subject", "")) if doc_info.get("/Subject") else None,
                    "creator": str(doc_info.get("/Creator", "")) if doc_info.get("/Creator") else None,
                    "producer": str(doc_info.get("/Producer", "")) if doc_info.get("/Producer") else None,
                    "creation_date": str(doc_info.get("/CreationDate", "")) if doc_info.get("/CreationDate") else None,
                    "modification_date": str(doc_info.get("/ModDate", "")) if doc_info.get("/ModDate") else None
                })
            
            return metadata
            
        except Exception as e:
            logger.error(f"PDF metadata extraction failed: {e}")
            return {
                "num_pages": 0,
                "size_bytes": len(pdf_content),
                "size_kb": round(len(pdf_content) / 1024, 2),
                "error": str(e)
            }
    
    @staticmethod
    def validate_pdf(pdf_content: bytes, max_size_mb: int = 10) -> Dict[str, Any]:
        """
        Validate PDF file
        
        Args:
            pdf_content: PDF file content as bytes
            max_size_mb: Maximum allowed file size in MB
            
        Returns:
            Validation result dictionary
        """
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "metadata": {}
        }
        
        try:
            # Check file size
            size_mb = len(pdf_content) / (1024 * 1024)
            if size_mb > max_size_mb:
                result["valid"] = False
                result["errors"].append(f"File size ({size_mb:.2f}MB) exceeds maximum ({max_size_mb}MB)")
            
            # Try to read PDF
            if PdfReader is None:
                result["valid"] = False
                result["errors"].append("pypdf library not installed")
                return result
                
            pdf_stream = io.BytesIO(pdf_content)
            pdf_reader = PdfReader(pdf_stream)
            
            # Check if PDF has pages
            if len(pdf_reader.pages) == 0:
                result["valid"] = False
                result["errors"].append("PDF contains no pages")
            
            # Check if we can extract text
            try:
                text_content = ""
                for page in pdf_reader.pages[:3]:  # Check first 3 pages
                    text_content += page.extract_text()
                
                if not text_content.strip():
                    result["warnings"].append("PDF appears to contain no extractable text (might be image-only)")
            except Exception:
                result["warnings"].append("Could not extract text from PDF")
            
            # Get metadata
            result["metadata"] = PDFProcessor.get_pdf_metadata(pdf_content)
            
        except Exception as e:
            result["valid"] = False
            result["errors"].append(f"Invalid PDF file: {str(e)}")
        
        return result