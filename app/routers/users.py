from fastapi import APIRouter, Depends

from app.schemas.quota import QuotaResponse 
from app.schemas.user import UserResponse
from app.database.engine import SessionDep 
from app.services.dependencies import CurrentUser

from app.repositories.quota import QuotaRepository

router = APIRouter(
    prefix="/users", 
    tags=["Users"]
)

@router.get("/me", response_model=UserResponse)
async def get_me(user:CurrentUser): 
    return user

@router.get("/me/quota", response_model=QuotaResponse)
async def get_my_quota(user:CurrentUser, db:SessionDep): 
    quota = await QuotaRepository(db).get_by_user(user.id)
    return QuotaResponse.from_quota(quota)

