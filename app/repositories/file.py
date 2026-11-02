from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import select, func
from app.database.models import File 

class FileRepository:
    def __init__(self, db:AsyncSession):
        self.db = db

    async def list_by_user(self, user_id:int)->list[File]:
        result = await self.db.execute(select(File).where(File.user_id == user_id).order_by(File.uploaded_at.desc()))
        return list(result.scalars().all())

    async def get_by_id_and_user(self, file_id:int, user_id:int)->File|None:
        result = await self.db.execute(select(File).where(File.id == file_id, File.user_id == user_id))
        return result.scalar_one_or_none()

    async def create(self, **kwargs)->File:
        file = File(**kwargs)
        self.db.add(file)
        await self.db.flush()
        return file

    async def count_by_user(self, user_id:int)->int:
        result = await self.db.execute(select(func.count()).select_from(File).where(File.user_id == user_id))
        return result.scalar_one()

    async def total_size_by_user(self, user_id:int)->int:
        result = await self.db.execute(select(func.coalesce(func.sum(File.size_bytes), 0)).where(File.user_id == user_id))
        return result.scalar_one()

    async def delete(self, file:File)->None:
        await self.db.delete(file)