from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import MappedAsDataclass, DeclarativeBase
from config import settings 
from fastapi import Depends
from typing import Annotated 

engine = create_async_engine(settings.DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(MappedAsDataclass, DeclarativeBase): 
    pass

async def get_db(): 
    async with AsyncSessionLocal() as session: 
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_db)]