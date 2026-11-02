from sqlalchemy import String, BigInteger, DateTime, ForeignKey, func 
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.database.engine import Base

class User(Base): 
    __tablename__ = "users"
    id:Mapped[int] = mapped_column(primary_key=True, index=True)
    username:Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email:Mapped[str] = mapped_column(String(100), unique=True, index=True)
    hashed_password:Mapped[str] = mapped_column(String(255))
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_admin:Mapped[bool] = mapped_column(default=0)

class Quota(Base): 
    __tablename__ = "quotas"
    id:Mapped[int] = mapped_column(primary_key=True)
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    limit_bytes:Mapped[int] = mapped_column(BigInteger, default=15*1024**3)
    used_bytes:Mapped[int] = mapped_column(BigInteger, default=0)

class File(Base): 
    __tablename__ = "files"
    id:Mapped[int] = mapped_column(primary_key=True)
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id"))
    filename:Mapped[str] = mapped_column(String(255))
    object_key:Mapped[str] = mapped_column(String(512), unique=True)
    size_bytes:Mapped[int] = mapped_column(BigInteger)
    uploaded_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    mime_type:Mapped[str|None] = mapped_column(String(100), default=None)
