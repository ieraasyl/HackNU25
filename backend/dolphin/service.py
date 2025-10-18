from typing import List, Dict, Any, Optional, AsyncGenerator
import logging
from .local_client import LocalDolphinClient
from .config import dolphin_config
from .pdf_processor import PDFProcessor

logger = logging.getLogger(__name__)

class DolphinService:
    """
    Service layer for Local Dolphin operations - NO API KEY NEEDED!
    """
    
    def __init__(self, api_key: Optional[str] = None):
        # API key is optional now - we run locally!
        self.api_key = api_key or dolphin_config.api_key
        
        # Only require API key for cloud providers
        if dolphin_config.requires_api_key and not self.api_key:
            logger.warning("No API key provided, but running in local mode - that's OK!")
        
        logger.info(f"🦌 Dolphin service initialized in '{dolphin_config.provider}' mode")
    
    async def chat(self, 
                   user_message: str, 
                   conversation_history: Optional[List[Dict[str, str]]] = None,
                   system_prompt: Optional[str] = None) -> str:
        """
        Simple chat interface
        
        Args:
            user_message: The user's message
            conversation_history: Previous conversation messages
            system_prompt: System prompt to set context
            
        Returns:
            Model response
        """
        
        messages = []
        
        # Add system prompt if provided
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # Add conversation history
        if conversation_history:
            messages.extend(conversation_history)
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        async with LocalDolphinClient() as client:
            try:
                response = await client.generate_response(
                    messages=messages,
                    max_tokens=dolphin_config.max_tokens,
                    temperature=dolphin_config.temperature
                )
                
                return response["response"]
                
            except Exception as e:
                logger.error(f"Error in chat: {e}")
                raise
    
    async def stream_chat(self, 
                         user_message: str, 
                         conversation_history: Optional[List[Dict[str, str]]] = None,
                         system_prompt: Optional[str] = None) -> AsyncGenerator[str, None]:
        """
        Streaming chat interface
        
        Args:
            user_message: The user's message
            conversation_history: Previous conversation messages
            system_prompt: System prompt to set context
            
        Yields:
            Streaming response chunks
        """
        
        messages = []
        
        # Add system prompt if provided
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # Add conversation history
        if conversation_history:
            messages.extend(conversation_history)
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        async with LocalDolphinClient() as client:
            try:
                async for chunk in client.stream_response(
                    messages=messages,
                    max_tokens=dolphin_config.max_tokens,
                    temperature=dolphin_config.temperature
                ):
                    if "choices" in chunk and len(chunk["choices"]) > 0:
                        delta = chunk["choices"][0].get("delta", {})
                        if "content" in delta:
                            yield delta["content"]
                            
            except Exception as e:
                logger.error(f"Error in stream_chat: {e}")
                raise

    async def analyze_pdf(self, 
                         pdf_content: bytes, 
                         analysis_prompt: str = "Please analyze this document and provide a summary of its key points.",
                         extract_text: bool = True) -> Dict[str, Any]:
        """
        Analyze a PDF document using Dolphin ByteDance
        
        Args:
            pdf_content: PDF file content as bytes
            analysis_prompt: Prompt for analysis
            extract_text: Whether to extract and include text content
            
        Returns:
            Analysis results including summary, metadata, and optionally extracted text
        """
        try:
            # Validate PDF
            validation = PDFProcessor.validate_pdf(pdf_content)
            if not validation["valid"]:
                return {
                    "success": False,
                    "error": "PDF validation failed",
                    "details": validation["errors"]
                }
            
            # Get metadata
            metadata = PDFProcessor.get_pdf_metadata(pdf_content)
            
            result = {
                "success": True,
                "metadata": metadata,
                "validation": validation
            }
            
            if extract_text:
                # Extract text content
                try:
                    text_content = await PDFProcessor.extract_text_from_pdf(pdf_content)
                    result["extracted_text"] = text_content
                    
                    # Analyze with Dolphin
                    analysis_message = f"{analysis_prompt}\n\nDocument content:\n{text_content}"
                    
                    # Truncate if too long (adjust based on model limits)
                    max_content_length = 8000
                    if len(analysis_message) > max_content_length:
                        truncated_text = text_content[:max_content_length - len(analysis_prompt) - 100]
                        analysis_message = f"{analysis_prompt}\n\nDocument content (truncated):\n{truncated_text}\n\n... (content truncated)"
                    
                    response = await self.chat(analysis_message)
                    result["analysis"] = response
                    
                except Exception as e:
                    logger.warning(f"Text extraction failed: {e}")
                    result["text_extraction_error"] = str(e)
                    
                    # Try analysis with just metadata
                    metadata_prompt = f"{analysis_prompt}\n\nI cannot extract text from this PDF, but here's what I know about it:\n"
                    metadata_prompt += f"- Pages: {metadata.get('num_pages', 'Unknown')}\n"
                    metadata_prompt += f"- Size: {metadata.get('size_kb', 'Unknown')} KB\n"
                    if metadata.get('title'):
                        metadata_prompt += f"- Title: {metadata['title']}\n"
                    if metadata.get('author'):
                        metadata_prompt += f"- Author: {metadata['author']}\n"
                    
                    response = await self.chat(metadata_prompt)
                    result["analysis"] = response
            
            return result
            
        except Exception as e:
            logger.error(f"PDF analysis failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def ask_about_pdf(self, 
                           pdf_content: bytes, 
                           question: str,
                           include_context: bool = True) -> Dict[str, Any]:
        """
        Ask specific questions about a PDF document
        
        Args:
            pdf_content: PDF file content as bytes
            question: Question to ask about the document
            include_context: Whether to include document text in the prompt
            
        Returns:
            Response to the question
        """
        try:
            # Validate PDF
            validation = PDFProcessor.validate_pdf(pdf_content)
            if not validation["valid"]:
                return {
                    "success": False,
                    "error": "PDF validation failed",
                    "details": validation["errors"]
                }
            
            if include_context:
                # Extract text content
                try:
                    text_content = await PDFProcessor.extract_text_from_pdf(pdf_content)
                    
                    # Create question with context
                    context_message = f"Based on the following document, please answer this question: {question}\n\n"
                    context_message += f"Document content:\n{text_content}"
                    
                    # Truncate if too long
                    max_length = 8000
                    if len(context_message) > max_length:
                        truncated_text = text_content[:max_length - len(question) - 200]
                        context_message = f"Based on the following document (truncated), please answer this question: {question}\n\n"
                        context_message += f"Document content:\n{truncated_text}\n\n... (content truncated)"
                    
                    response = await self.chat(context_message)
                    
                    return {
                        "success": True,
                        "question": question,
                        "answer": response,
                        "used_context": True
                    }
                    
                except Exception as e:
                    logger.warning(f"Could not extract text, asking without context: {e}")
            
            # Ask without context or if text extraction failed
            metadata = PDFProcessor.get_pdf_metadata(pdf_content)
            no_context_message = f"I have a PDF document with the following properties:\n"
            no_context_message += f"- Pages: {metadata.get('num_pages', 'Unknown')}\n"
            no_context_message += f"- Size: {metadata.get('size_kb', 'Unknown')} KB\n"
            if metadata.get('title'):
                no_context_message += f"- Title: {metadata['title']}\n"
            no_context_message += f"\nQuestion: {question}\n\n"
            no_context_message += "Note: I cannot read the document content, so please provide a general answer based on the document properties."
            
            response = await self.chat(no_context_message)
            
            return {
                "success": True,
                "question": question,
                "answer": response,
                "used_context": False,
                "note": "Response based on metadata only, document text could not be extracted"
            }
            
        except Exception as e:
            logger.error(f"PDF question failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

# Global service instance
dolphin_service = None

def get_dolphin_service(api_key: Optional[str] = None) -> DolphinService:
    """Get or create a Dolphin service instance"""
    global dolphin_service
    if dolphin_service is None or api_key:
        dolphin_service = DolphinService(api_key=api_key)
    return dolphin_service