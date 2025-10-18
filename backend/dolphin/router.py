"""
Example integration of Dolphin ByteDance with the chat router
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
import logging
import os

# Import our Dolphin components
from dolphin.service import get_dolphin_service
from dolphin.config import dolphin_config

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/dolphin")

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[ChatMessage]] = []
    system_prompt: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    status: str = "success"

@router.post("/chat", response_model=ChatResponse)
async def chat_with_dolphin(request: ChatRequest):
    """
    Chat endpoint using Dolphin (local or cloud)
    """
    try:
        # For local mode, no API key required
        if dolphin_config.provider == "local":
            service = get_dolphin_service()
        else:
            # For cloud providers, API key is required
            api_key = os.getenv("DOLPHIN_API_KEY") or dolphin_config.api_key
            if not api_key:
                raise HTTPException(
                    status_code=500, 
                    detail="Dolphin API key not configured"
                )
            service = get_dolphin_service(api_key=api_key)
        
        # Convert conversation history to dict format
        history = [{"role": msg.role, "content": msg.content} for msg in request.conversation_history]
        
        # Get response from Dolphin
        response = await service.chat(
            user_message=request.message,
            conversation_history=history,
            system_prompt=request.system_prompt
        )
        
        return ChatResponse(response=response)
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat/stream")
async def stream_chat_with_dolphin(request: ChatRequest):
    """
    Streaming chat endpoint using Dolphin (local or cloud)
    """
    async def generate():
        try:
            # For local mode, no API key required
            if dolphin_config.provider == "local":
                service = get_dolphin_service()
            else:
                # For cloud providers, API key is required
                api_key = os.getenv("DOLPHIN_API_KEY") or dolphin_config.api_key
                if not api_key:
                    yield f"data: {json.dumps({'error': 'API key not configured'})}\n\n"
                    return
                service = get_dolphin_service(api_key=api_key)
            
            # Convert conversation history to dict format
            history = [{"role": msg.role, "content": msg.content} for msg in request.conversation_history]
            
            # Stream response from Dolphin
            async for chunk in service.stream_chat(
                user_message=request.message,
                conversation_history=history,
                system_prompt=request.system_prompt
            ):
                yield f"data: {json.dumps({'content': chunk})}\n\n"
                
            yield f"data: {json.dumps({'status': 'complete'})}\n\n"
            
        except Exception as e:
            logger.error(f"Error in streaming endpoint: {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )

@router.websocket("/ws")
async def dolphin_websocket(websocket: WebSocket):
    """
    WebSocket endpoint for real-time chat with Dolphin (local or cloud)
    """
    await websocket.accept()
    
    try:
        # For local mode, no API key required
        if dolphin_config.provider == "local":
            service = get_dolphin_service()
        else:
            # For cloud providers, API key is required
            api_key = os.getenv("DOLPHIN_API_KEY") or dolphin_config.api_key
            if not api_key:
                await websocket.send_text(json.dumps({
                    "error": "Dolphin API key not configured"
                }))
                await websocket.close()
                return
            service = get_dolphin_service(api_key=api_key)
        conversation_history = []
        
        await websocket.send_text(json.dumps({
            "status": "connected",
            "message": "Dolphin ByteDance chat ready!"
        }))
        
        while True:
            # Receive message from client
            message = await websocket.receive_text()
            
            try:
                data = json.loads(message)
                user_message = data.get("message", "")
                system_prompt = data.get("system_prompt")
                
                if not user_message:
                    await websocket.send_text(json.dumps({
                        "error": "No message provided"
                    }))
                    continue
                
                # Add user message to history
                conversation_history.append({
                    "role": "user", 
                    "content": user_message
                })
                
                # Get response from Dolphin
                response = await service.chat(
                    user_message=user_message,
                    conversation_history=conversation_history[:-1],  # Exclude current message
                    system_prompt=system_prompt
                )
                
                # Add assistant response to history
                conversation_history.append({
                    "role": "assistant",
                    "content": response
                })
                
                # Send response back to client
                await websocket.send_text(json.dumps({
                    "response": response,
                    "conversation_id": len(conversation_history) // 2
                }))
                
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({
                    "error": "Invalid JSON format"
                }))
            except Exception as e:
                logger.error(f"Error in WebSocket: {e}")
                await websocket.send_text(json.dumps({
                    "error": str(e)
                }))
                
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.close()

class PDFAnalysisRequest(BaseModel):
    analysis_prompt: Optional[str] = "Please analyze this document and provide a summary of its key points."
    extract_text: Optional[bool] = True

class PDFQuestionRequest(BaseModel):
    question: str
    include_context: Optional[bool] = True

class PDFAnalysisResponse(BaseModel):
    success: bool
    metadata: Optional[Dict[str, Any]] = None
    extracted_text: Optional[str] = None
    analysis: Optional[str] = None
    error: Optional[str] = None

class PDFQuestionResponse(BaseModel):
    success: bool
    question: str
    answer: Optional[str] = None
    used_context: Optional[bool] = None
    error: Optional[str] = None

@router.post("/analyze-pdf", response_model=PDFAnalysisResponse)
async def analyze_pdf_document(
    file: UploadFile = File(...),
    analysis_prompt: str = Form("Please analyze this document and provide a summary of its key points."),
    extract_text: bool = Form(True)
):
    """
    Analyze a PDF document using Dolphin ByteDance
    
    - **file**: PDF file to analyze
    - **analysis_prompt**: Prompt for document analysis
    - **extract_text**: Whether to extract and analyze text content
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Read file content
        pdf_content = await file.read()
        
        if len(pdf_content) == 0:
            raise HTTPException(status_code=400, detail="Empty file uploaded")
        
        # Get service and analyze
        service = get_dolphin_service()
        result = await service.analyze_pdf(
            pdf_content=pdf_content,
            analysis_prompt=analysis_prompt,
            extract_text=extract_text
        )
        
        return PDFAnalysisResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"PDF analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.post("/ask-pdf", response_model=PDFQuestionResponse)
async def ask_pdf_question(
    file: UploadFile = File(...),
    question: str = Form(...),
    include_context: bool = Form(True)
):
    """
    Ask a question about a PDF document
    
    - **file**: PDF file to analyze
    - **question**: Question to ask about the document
    - **include_context**: Whether to include document content in the analysis
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Read file content
        pdf_content = await file.read()
        
        if len(pdf_content) == 0:
            raise HTTPException(status_code=400, detail="Empty file uploaded")
        
        # Get service and ask question
        service = get_dolphin_service()
        result = await service.ask_about_pdf(
            pdf_content=pdf_content,
            question=question,
            include_context=include_context
        )
        
        return PDFQuestionResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"PDF question error: {e}")
        raise HTTPException(status_code=500, detail=f"Question failed: {str(e)}")

@router.post("/pdf-metadata")
async def get_pdf_metadata(file: UploadFile = File(...)):
    """
    Extract metadata from a PDF file without processing content
    
    - **file**: PDF file to analyze
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Read file content
        pdf_content = await file.read()
        
        if len(pdf_content) == 0:
            raise HTTPException(status_code=400, detail="Empty file uploaded")
        
        # Import here to avoid startup errors if library not installed
        from .pdf_processor import PDFProcessor
        
        # Get metadata and validation
        metadata = PDFProcessor.get_pdf_metadata(pdf_content)
        validation = PDFProcessor.validate_pdf(pdf_content)
        
        return {
            "filename": file.filename,
            "metadata": metadata,
            "validation": validation
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"PDF metadata error: {e}")
        raise HTTPException(status_code=500, detail=f"Metadata extraction failed: {str(e)}")

@router.get("/health")
async def dolphin_health():
    """
    Health check for Dolphin ByteDance integration
    """
    api_key = os.getenv("DOLPHIN_API_KEY") or dolphin_config.api_key
    
    return {
        "status": "ok" if api_key else "warning",
        "api_key_configured": bool(api_key),
        "base_url": dolphin_config.base_url,
        "model_endpoint": dolphin_config.model_endpoint,
        "pdf_support": True
    }