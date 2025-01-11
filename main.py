from datetime import timezone
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from routes.user_route import router as auth_router
from scheduled_tasks.tasks import clean_up_session
from utils.settings import settings


jobstores = {"default": MemoryJobStore()}

scheduler = AsyncIOScheduler(jobstores=jobstores, timezone=timezone.utc)


@scheduler.scheduled_job("interval", minutes=60)
async def scheduled_job():
    await clean_up_session()


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield


app = FastAPI(
    title="Authentication Using Sessions",
    description="Authentication Using Sessions",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=(lifespan),
)


@app.get("/")
async def root():
    return RedirectResponse("/docs")


app.include_router(auth_router, prefix=f"{settings.API_VERSION}")
