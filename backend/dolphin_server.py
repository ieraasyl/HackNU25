#!/usr/bin/env python3
"""
Standalone Dolphin FastAPI Server

This is a minimal FastAPI server that only includes the Dolphin ByteDance integration.
Use this to test the Dolphin integration independently.
"""

from fastapi import FastAPI
from dolphin.router import router as dolphin_router

# Create FastAPI app
app = FastAPI(
    title="Dolphin ByteDance API",
    description="Standalone API for Dolphin ByteDance integration",
    version="1.0.0"
)

# Include Dolphin router
app.include_router(dolphin_router, prefix="/api/v1", tags=["dolphin"])

@app.get("/")
async def root():
    return {
        "message": "Dolphin ByteDance API", 
        "status": "running",
        "endpoints": {
            "health": "/health",
            "dolphin_chat": "/api/v1/chat",
            "dolphin_health": "/api/v1/health"
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "dolphin-api"}

if __name__ == "__main__":
    import uvicorn
    print("🐬 Starting Dolphin ByteDance API server...")
    print("📖 API documentation will be available at: http://localhost:8001/docs")
    print("🔧 Health check: http://localhost:8001/health")
    print("💬 Chat endpoint: http://localhost:8001/api/v1/chat")
    uvicorn.run(app, host="0.0.0.0", port=8001)