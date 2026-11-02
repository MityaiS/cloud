import uuid
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File as FastAPIFile
from app.database.engine import SessionDep
from app.services.dependencies import get_current_user
from app.repositories.file import FileRepository
from app.repositories.quota import QuotaRepository
from app.services.quota import QuotaService
from app.services.storage import MinIOService
from app.schemas.file import FileResponse, FileUploadResponse

router = APIRouter(prefix="/files", tags=["Files"])
storage = MinIOService()

@router.post("/upload", response_model=FileUploadResponse)
async def upload(db:SessionDep, file: UploadFile = FastAPIFile(...), user=Depends(get_current_user)):
    quota_service = QuotaService(QuotaRepository(db))
    if not await quota_service.check(user.id, file.size):
        raise HTTPException(413, "Quota exceeded")

    key = f"user_{user.id}/{uuid.uuid4()}_{file.filename}"
    await storage.upload_file(await file.read(), key, file.content_type)

    file_repo = FileRepository(db)
    new_file = await file_repo.create(
        user_id=user.id, filename=file.filename, object_key=key,
        size_bytes=file.size, mime_type=file.content_type
    )
    await quota_service.add_usage(user.id, file.size)
    await db.commit()
    return FileUploadResponse(id=new_file.id, filename=file.filename, size_bytes=file.size)

@router.get("/", response_model=list[FileResponse])
async def list_files(db:SessionDep, user=Depends(get_current_user)):
    return await FileRepository(db).list_by_user(user.id)

@router.delete("/{file_id}")
async def delete_file(file_id: int, db:SessionDep, user=Depends(get_current_user)):
    file_repo = FileRepository(db)
    file = await file_repo.get_by_id_and_user(file_id, user.id)
    if not file:
        raise HTTPException(404, "File not found")

    await storage.delete_file(file.object_key)
    await file_repo.delete(file)
    await QuotaService(QuotaRepository(db)).add_usage(user.id, -file.size_bytes)
    await db.commit()
    return {"message": "File deleted"}