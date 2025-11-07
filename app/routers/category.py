from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..schemas import Category, CategoryCreate, CategoryUpdate, ResponseModel
from ..crud import category as cat_crud
from ..database import get_db
from ..utils.response import success_response, error_response

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=ResponseModel[Category])
async def create_category(category: CategoryCreate, db: AsyncSession = Depends(get_db)):
    exists = await cat_crud.get_category_by_name(db=db, category=category.name)
    if exists:
        return error_response(
            message="Category already exists", status_code=status.HTTP_409_CONFLICT
        )
        
    new_cat = await cat_crud.create_category(db=db, category=category)
    return success_response(
        message="Category created successfully",
        data=new_cat,
        status_code=status.HTTP_201_CREATED
    )

@router.get("/", response_model=ResponseModel[List[Category]])
async def get_categories(db: AsyncSession = Depends(get_db)):
    categories = await cat_crud.get_categories(db=db)
    return success_response(message="Categories retrieved successfully", data=categories)

@router.get("/{category_id}", response_model=ResponseModel[Category])
async def get_category_by_id(category_id: str, db: AsyncSession = Depends(get_db)):
    category = await cat_crud.get_category_by_id(db=db, category_id=category_id)
    if not category:
        return error_response(
            message="Category not found", status_code=status.HTTP_404_NOT_FOUND
        )
        
    return success_response(message="Category found", data=category)
    
@router.get("/name/{category_name}", response_model=ResponseModel[Category])
async def get_category_by_name(category_name: str, db: AsyncSession = Depends(get_db)):
    category = await cat_crud.get_category_by_name(db=db, category=category_name)
    if not category:
        return error_response(
            message="Category not found", status_code=status.HTTP_404_NOT_FOUND
        )
        
    return success_response(message="Category found", data=category)

@router.put("/{category_id}", response_model=ResponseModel[Category])
async def update_category(
    category_id: str, category: CategoryUpdate, db: AsyncSession = Depends(get_db)
):
    updated_cat = await cat_crud.update_category(
        db=db, category_id=category_id, data=category
    )
    if not updated_cat:
        return error_response(
            message="Category not found", status_code=status.HTTP_404_NOT_FOUND
        )
        
    return success_response(message="Category updated successfully", data=category)


@router.delete("/{category_id}", response_model=ResponseModel[None])
async def delete_category(category_id: str, db: AsyncSession = Depends(get_db)):
    is_deleted = await cat_crud.delete_category(db=db, category_id=category_id)
    if not is_deleted:
        return error_response(
            message="Category not found", status_code=status.HTTP_404_NOT_FOUND
        )
        
    return success_response(message="Category deleted successfully")