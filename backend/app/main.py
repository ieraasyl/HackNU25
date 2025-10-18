from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat
from app.tasks.jobs import broker
from taskiq import TaskiqScheduler
import asyncio

# Import Dolphin router
try:
    from dolphin.router import router as dolphin_router
    DOLPHIN_AVAILABLE = True
except ImportError:
    DOLPHIN_AVAILABLE = False
    print("Warning: Dolphin ByteDance module not available")

app = FastAPI(title="SmartBot API")

origins = ["*"]  # later restrict to widget/dashboard domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)

# Include Dolphin router if available
if DOLPHIN_AVAILABLE:
    app.include_router(dolphin_router)

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "features": {
            "dolphin_bytedance": DOLPHIN_AVAILABLE
        }
    }
