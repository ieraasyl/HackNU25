from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routers import chat
from app.routers import vacancies, applications
from app.tasks.jobs import broker
from app.db.session import init_db, engine
from taskiq import TaskiqScheduler
from sqlmodel import SQLModel
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize database
    await init_db()
    yield
    # Shutdown: cleanup if needed

app = FastAPI(title="HackNU API", lifespan=lifespan)

origins = ["*"]  # later restrict to widget/dashboard domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(chat.router)
app.include_router(vacancies.router)
app.include_router(applications.router)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/debug/reset-db")
async def reset_database():
    """
    Debug endpoint to reset the database by dropping and recreating all tables.
    WARNING: This will delete all data!
    """
    try:
        # Drop all tables
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)
        
        # Recreate all tables
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        
        return {
            "status": "success",
            "message": "Database has been reset successfully. All tables dropped and recreated."
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to reset database: {str(e)}"
        }
