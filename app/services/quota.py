from app.repositories.quota import QuotaRepository

class QuotaService:
    def __init__(self, repo:QuotaRepository):
        self.repo = repo

    async def check(self, user_id:int, additional:int)->bool:
        quota = await self.repo.get_by_user(user_id)
        if not quota:
            return False
        return quota.used_bytes + additional <= quota.limit_bytes

    async def add_usage(self, user_id:int, delta:int):
        await self.repo.update_usage(user_id, delta)