from pydantic_settings import SettingsConfigDict 
from pydantic import BaseModel, Field 
from datetime import datetime 
from app.schemas.quota import QuotaShort

class UserUpdateQuota(BaseModel): 
    limit_bytes:int = Field(..., gt=0)
class AdminUserResponse(BaseModel): 
    id:int
    username:str 
    email:str 
    is_admin:bool 
    created_at:datetime
    quota:QuotaShort|None = None 

    model_config = SettingsConfigDict(
        from_attributes=True
    )

class MessageResponse(BaseModel): 
    message:str 