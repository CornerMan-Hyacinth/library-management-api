from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.crud import borrow as borrow_crud, book as book_crud, profile as profile_crud
from app.database import get_db
from app.schemas import Borrow, BorrowCreate, BorrowUpdate, BookUpdate, ResponseModel
from app.utils.response import success_response, error_response
from app.utils.core.auth import get_current_staff

router = APIRouter(
    prefix="/borrows", tags=["Borrows"], dependencies=[Depends(get_current_staff)]
)

@router.post("/", response_model=ResponseModel[Borrow])
async def create_borrowed_book(borrow: BorrowCreate, db: AsyncSession = Depends(get_db)):
    # 1. Validate book exists
    book = await book_crud.get_book_by_id(db=db, id=borrow.book_id)
    if not book:
        return error_response(
            message="Book does not exist", status_code=status.HTTP_404_NOT_FOUND
        )
       
    # 2. Validate user exists
    user = await profile_crud.get_profile_by_email(db=db, email=borrow.user_email) 
    if not user:
        return error_response(
            message="User does not exist", status_code=status.HTTP_404_NOT_FOUND
        )
           
    # 3. Check availability
    if not book.available_copies:
        return error_response(
            message=f"All copies of {book.title} have been borrowed",
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )
        
    # 4. Create borrow
    new_borrow = await borrow_crud.create_borrow(db=db, borrow=borrow)
    
    # 5. Update book
    await book_crud.update_book(
        db=db, id=book.id, data=BookUpdate(available_copies=book.available_copies - 1)
    )
    
    return success_response(
        message="Book successfully borrowed",
        data=new_borrow,
        status_code=status.HTTP_201_CREATED
    )

@router.get("/", response_model=ResponseModel[List[Borrow]])
async def get_borrowed_books(db: AsyncSession = Depends(get_db)):
    borrows = await borrow_crud.get_borrows(db=db)
    return success_response(
        message="Retrieved borrowed books successfully", data=borrows
    )
    
@router.get("/user/{user_email}", response_model=ResponseModel[List[Borrow]])
async def get_borrowed_books_by_user_email(
    user_email: str, db: AsyncSession = Depends(get_db)
):
    borrows = await borrow_crud.get_borrows_by_user(db=db, user_email=user_email)
    return success_response(
        message="Retrieved borrowed books by user id successfully", data=borrows
    )
    
@router.get("/book/{book_id}", response_model=ResponseModel[List[Borrow]])
async def get_borrowed_books_by_book_id(book_id: str, db: AsyncSession = Depends(get_db)):
    borrows = await borrow_crud.get_borrows_by_book(db=db, book_id=book_id)
    return success_response(
        message="Retrieved borrowed books by book id successfully", data=borrows
    )
    
@router.get("/{borrow_id}", response_model=ResponseModel[Borrow])
async def get_borrowed_book_by_id(borrow_id: str, db: AsyncSession = Depends(get_db)):
    borrow = await borrow_crud.get_borrow_by_id(db=db, borrow_id=borrow_id)
    if not borrow:
        return error_response(
            message="Borrowed item not found", status_code=status.HTTP_404_NOT_FOUND
        )
        
    return success_response(message="Retrieved borrowed item successfully", data=borrow)
    
@router.put("/{borrow_id}", response_model=ResponseModel[Borrow])
async def update_borrowed_book(
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

@router.delete("/{borrow_id}", response_model=ResponseModel[None])
async def return_borrowed_book(borrow_id: str, db: AsyncSession = Depends(get_db)):
    # Get borrow data
    borrow = await borrow_crud.get_borrow_by_id(db=db, borrow_id=borrow_id)
    
    # Validate
    if not borrow:
        return error_response(
            message="Borrowed data not found", status_code=status.HTTP_404_NOT_FOUND
        )
    
    # Delete borrow
    await borrow_crud.delete_borrow(db=db, borrow_id=borrow_id)
       
    # Get book
    book = await book_crud.get_book_by_id(db=db, id=borrow.book_id)
    
    # Update book
    await book_crud.update_book(
        db=db, id=book.id, data=BookUpdate(available_copies=book.available_copies + 1)
    )
    
    return success_response(message="Deleted borrowed data successfully")
    
    