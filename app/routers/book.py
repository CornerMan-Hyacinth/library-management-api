from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas import Book, BookCreate, BookUpdate, ResponseModel
from app.crud import book as book_crud, category as cat_crud
from app.database import get_db
from app.utils.response import success_response, error_response
from app.utils.core.auth import get_current_staff

router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/", dependencies=[Depends(get_current_staff)], response_model=ResponseModel[Book])
async def create_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    existing = await book_crud.get_book_by_title(db=db, title=book.title)
    if existing != None:
        return error_response(
            message="Book with this title already exists",
            status_code=status.HTTP_409_CONFLICT
        )
    
    new_book = await book_crud.create_book(db=db, book=book)
    return success_response(
        message="Book added successfully",
        data=new_book,
        status_code=status.HTTP_201_CREATED
    )

@router.get("/", response_model=ResponseModel[List[Book]])
async def get_books(db: AsyncSession = Depends(get_db)):
    books = await book_crud.get_books(db=db)
    return success_response(data=books, message="Books retrieved")

@router.get("/{book_id}", response_model=ResponseModel[Book])
async def get_book(book_id: str, db: AsyncSession = Depends(get_db)):
    book = await book_crud.get_book_by_id(db=db, id=book_id)
    if not book:
        return error_response(
            message="Book not found", status_code=status.HTTP_404_NOT_FOUND
        )
    
    return success_response(data=book, message="Book found")

@router.get("/category/{category_name}", response_model=ResponseModel[Book])
async def get_books_by_category(category_name: str, db: AsyncSession = Depends(get_db)):
    cat = await cat_crud.get_category_by_name(db=db, category=category_name)
    if not cat:
        return error_response(
            message="Category not found", status_code=status.HTTP_404_NOT_FOUND
        )
        
    books = await book_crud.get_books_by_category(db=db, cat_id=cat.id)
    return success_response(data=books, message="Books retrieved by category")

@router.put("/{book_id}", dependencies=[Depends(get_current_staff)], response_model=ResponseModel[Book])
async def update_book(
    book_id: str, book: BookUpdate, db: AsyncSession = Depends(get_db)
):
    updated_book = await book_crud.update_book(db=db, id=book_id, data=book)
    if not updated_book:
        return error_response(
            message="Book not found", status_code=status.HTTP_404_NOT_FOUND
        )
        
    return success_response(data=updated_book, message="Book updated successfully")

@router.delete("/{book_id}", dependencies=[Depends(get_current_staff)], response_model=ResponseModel[None])
async def delete_book(book_id: str, db: AsyncSession = Depends(get_db)):
    deleted = await book_crud.delete_book(db=db, id=book_id)
    if not deleted:
        return error_response(
            message="Book not found", status_code=status.HTTP_404_NOT_FOUND
        )
        
    return success_response(message="Book deleted successfully")