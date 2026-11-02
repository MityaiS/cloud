from contextlib import asynccontextmanager 
from fastapi import FastAPI 

from app.routers import admin, auth, files, users
from app.services.storage import MinIOService
from app.logger import logger 
from app.database.engine import engine, Base

@asynccontextmanager
async def lifespan(app:FastAPI): 
    logger.info("Starting Cloud Storage API...")
    # await MinIOService().ensure_bucket() 
    async with engine.begin() as conn: 
        await conn.run_sync(Base.metadata.create_all)
    logger.info("MinIO bucket ensured")
    yield 
    logger.info("Shutting down Cloud Storage API...")

app = FastAPI(
    title="Cloud Storage API", 
    version="1.0.0", 
    lifespan=lifespan
)

app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(files.router)
app.include_router(users.router)