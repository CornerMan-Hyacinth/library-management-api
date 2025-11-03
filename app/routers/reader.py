from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import Reader, ReaderCreate, ReaderUpdate, ResponseModel
from ..crud import reader as reader_crud
from ..database import get_db
from ..utils.response import success_response, error_response

router = APIRouter(prefix="/readers", tags=["Readers"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_reader(reader: ReaderCreate, db: AsyncSession = Depends(get_db)):
    existing = await reader_crud.get_reader_by_email(db=db, email=reader.email)
    if existing:
        return error_response(
            message="Reader already exists", status_code=status.HTTP_409_CONFLICT
        )
        
    new_reader = await reader_crud.create_reader(db=db, reader=reader)
    return success_response("Reader added successfully", data=new_reader)

@router.get("/")
async def get_readers(db: AsyncSession = Depends(get_db)):
    readers = await reader_crud.get_readers(db=db)
    return success_response(message="Readers retrieved", data=readers)

@router.get("/{reader_id}")
async def get_reader(reader_id: str, db: AsyncSession = Depends(get_db)):
    reader = await reader_crud.get_reader_by_id(db=db, id=reader_id)
    if not reader:
        return error_response(
            message="Reader not found", status_code=status.HTTP_404_NOT_FOUND
        )
        
    return success_response(data=reader, message="Reader found")

@router.put("/{reader_id}")
async def update_reader(
    reader_id: str, reader: ReaderUpdate, db: AsyncSession = Depends(get_db)
):
    updated_reader = await reader_crud.update_reader(db=db, id=reader_id, data=reader)
    if not updated_reader:
        return error_response(
            message="Reader not found", status_code=status.HTTP_404_NOT_FOUND
        )
        
    return success_response(message="Reader found", data=updated_reader)

@router.delete("/{reader_id}")
async def delete_reader(reader_id: str, db: AsyncSession = Depends(get_db)):
    is_deleted = await reader_crud.delete_reader(db=db, id=reader_id)
    if not is_deleted:
        return error_response(
            message="Reader not found", status_code=status.HTTP_404_NOT_FOUND
        )
        
    return success_response(message="Reader deleted successfully")