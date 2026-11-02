from pydantic_settings import SettingsConfigDict
from pydantic import BaseModel
from datetime import datetime

class UserResponse(BaseModel): 
    id:int 
    username:str 
    email:str 
    is_admin:bool 
    created_at:datetime 

    model_config = SettingsConfigDict(
        from_attributes=True
    )
