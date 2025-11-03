from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..crud import borrow as borrow_crud, book as book_crud
from ..database import get_db
from ..schemas import Borrow, BorrowCreate, BorrowUpdate
from ..utils.response import success_response, error_response

router = APIRouter(prefix="/borrows", tags=["Borrows"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_borrow(borrow: BorrowCreate, db: AsyncSession = Depends(get_db)):
    book = await book_crud.get_book_by_id(db=db, id=borrow.book_id)
    borrows = await borrow_crud.get_borrows_by_book(db=db, book_id=borrow.book_id)
    
    if borrows >= book.quantity:
        return error_response(
            message=f"All copies of {book.title} has been borrowed",
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )
        
    new_borrow = await borrow_crud.create_borrow(db=db, borrow=borrow)
    return success_response(message="Book successfully borrowed", data=new_borrow)

@router.get("/")
async def get_borrows(db: AsyncSession = Depends(get_db)):
    borrows = await borrow_crud.get_borrows(db=db)
    return success_response(
        message="Retrieved borrowed books successfully", data=borrows
    )
    
@router.get("/reader/{reader_id}")
async def get_borrows_by_reader_id(reader_id: str, db: AsyncSession = Depends(get_db)):
    borrows = await borrow_crud.get_borrows_by_reader(db=db, reader_id=reader_id)
    return success_response(
        message="Retrieved borrowed books by reader id successfully", data=borrows
    )
    
@router.get("/book/{book_id}")
async def get_borrows_by_book_id(book_id: str, db: AsyncSession = Depends(get_db)):
    borrows = await borrow_crud.get_borrows_by_book(db=db, book_id=book_id)
    return success_response(
        message="Retrieved borrowed books by book id successfully", data=borrows
    )
    
@router.put("/{borrow_id}")
async def update_borrow(
    borrow_id: str, borrow: BorrowUpdate, db: AsyncSession = Depends(get_db)
):
    updated_borrow = await borrow_crud.update_borrow(
        db=db, borrow_id=borrow_id, data=borrow
    )
    if not updated_borrow:
        return error_response(
            message="Borrowed data not found", status_code=status.HTTP_404_NOT_FOUND
        )
        
    return success_response(
        message="Updated borrowed data successfully", data=updated_borrow
    )

@router.delete("/")
async def delete_borrow(borrow_id: str, db: AsyncSession = Depends(get_db)):
    is_deleted = await borrow_crud.delete_borrow(db=db, borrow_id=borrow_id)
    if not is_deleted:
        return error_response(
            message="Borrowed data not found", status_code=status.HTTP_404_NOT_FOUND
        )
        
    return success_response(message="Deleted borrowed data successfully")
    
    