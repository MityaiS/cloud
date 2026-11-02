from fastapi import APIRouter, HTTPException
from app.database.engine import SessionDep
from app.repositories.user import UserRepository 
from app.repositories.quota import QuotaRepository 
from app.schemas.auth import UserRegister, UserLogin, Token
from app.services.security import hash_password, verify_password, create_access_token

router = APIRouter(
    prefix='/auth', 
    tags=['Auth']
)

@router.post('/register', status_code=201)
async def register(data:UserRegister, db:SessionDep): 
    user_repo=UserRepository(db)
    if await user_repo.get_by_username(data.username): 
        raise HTTPException(400, "Username exists")

    user = await user_repo.create(data.username, data.email, hash_password(data.password))
    await QuotaRepository(db).create(user.id)
    await db.commit() 

    return {"message":"User registered successfuly", "user_id":user.id}

@router.post("/login", response_model=Token)
async def login(data:UserLogin, db:SessionDep):
    user_repo = UserRepository(db)
    user = await user_repo.get_by_username(data.username)
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")

    token = create_access_token({"sub": str(user.id)})
    
    return {"access_token": token, "token_type": "bearer"}