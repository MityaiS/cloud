from fastapi import APIRouter, Depends, HTTPException

from app.database.engine import SessionDep

from app.repositories.user import UserRepository
from app.repositories.quota import QuotaRepository

from app.schemas.user import UserResponse
from app.schemas.admin import UserUpdateQuota

from app.services.dependencies import get_current_admin

router = APIRouter(
    prefix="/admin",
    tags=["Admin"], 
    dependencies=[Depends(get_current_admin)]
)

@router.get("/users", response_model=list[UserResponse])
async def list_users(db:SessionDep):
    return await UserRepository(db).list_all() 

@router.put("/users/{user_id}/quota")
async def update_quota(user_id:int, db:SessionDep, data:UserUpdateQuota): 
    quota_repo = QuotaRepository(db)
    quota = await quota_repo.get_by_user(user_id)

    if not quota: 
        raise HTTPException(404, "Quota not found")
    quota.limit_bytes = data.limit_bytes
    await db.commit()
    return {"message":"Quota updated"}