from pydantic_settings import SettingsConfigDict
from pydantic import BaseModel 

class QuotaResponse(BaseModel): 
    limit_bytes:int 
    used_bytes:int
    available_bytes:int 
    percent_used:float 

    @classmethod
    def from_quota(cls, q): 
        return cls(limit_bytes = q.limit_bytes, 
                   used_bytes = q.used_bytes,
                   available_bytes = q.limit_bytes-q.used_bytes, 
                   percent_used = round((q.used_bytes/q.limit_bytes)*100, 2) if q.limit_bytes else 0
        )

class QuotaShort(BaseModel): 
    limit_bytes:int 
    used_bytes:int 

    model_config = SettingsConfigDict(
        from_attributes=True
    )

