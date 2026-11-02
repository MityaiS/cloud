from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.database.models import Quota

class QuotaRepository:
    def __init__(self, db:AsyncSession):
        self.db = db

    async def get_by_user(self, user_id:int)->Quota|None:
        result = await self.db.execute(select(Quota).where(Quota.user_id == user_id))
        return result.scalar_one_or_none()

    async def create(self, user_id:int)->Quota:
        quota = Quota(user_id = user_id)
        self.db.add(quota)
        await self.db.flush()
        return quota

    async def update_usage(self, user_id:int, delta:int)->None:
        await self.db.execute(update(Quota).where(Quota.user_id == user_id).values(used_bytes=Quota.used_bytes + delta))

    async def set_limit(self, user_id:int, limit_bytes:int)->None:
        await self.db.execute(update(Quota).where(Quota.user_id == user_id).values(limit_bytes=limit_bytes))