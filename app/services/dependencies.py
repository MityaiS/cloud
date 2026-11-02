from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from app.database.engine import SessionDep
from app.repositories.user import UserRepository
from app.services.security import decode_access_token
from typing import Annotated
from app.database.models import User

security = HTTPBearer()

async def get_current_user(db:SessionDep, credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = decode_access_token(credentials.credentials)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(401, "Invalid token")
    except JWTError:
        raise HTTPException(401, "Invalid token")

    repo = UserRepository(db)
    user = await repo.get_by_id(int(user_id))
    if not user:
        raise HTTPException(401, "User not found")
    return user

async def get_current_admin(user=Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(403, "Admin access required")
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]
