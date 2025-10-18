from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat
from app.tasks.jobs import broker
from taskiq import TaskiqScheduler
import asyncio

app = FastAPI(title="HackNU25 API")

origins = ["*"]  # later restrict to widget/dashboard domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "message": "HackNU25 Backend API is running"
    }
