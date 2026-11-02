from pydantic_settings import SettingsConfigDict 
from pydantic import BaseModel
from datetime import datetime

class FileResponse(BaseModel): 
    id:int 
    filename:str 
    size_bytes:int
    mime_type:str|None = None
    uploaded_at:datetime

    model_config = SettingsConfigDict(
        from_attributes=True
    )

class FileUploadResponse(BaseModel): 
    id:int 
    filename:str 
    size_bytes:int
    message:str = "File uploaded seccessfuly!"
