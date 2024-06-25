from typing import List, Any
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select, func

from app.crud.index import category_crud as crud
from app.api.deps import SessionDep, get_current_active_superuser, CategoryProducerDep
from app.models import (
    Message, Category, CategoryCreate, CategoryPublic, CategoryUpdate, CategoriesPublic
)

router = APIRouter()

@router.get("/", response_model=CategoriesPublic)
def get_all_categories(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all categories
    """
    count_statement = select(func.count()).select_from(Category)
    count = session.exec(count_statement).one()

    statement = select(Category).offset(skip).limit(limit)
    categories = session.exec(statement).all()
    
    return CategoriesPublic(data=categories, count=count)


@router.post("/", dependencies=[Depends(get_current_active_superuser)], response_model=CategoryPublic)
async def create_category(*, session: SessionDep,  category_in: CategoryCreate, producer: CategoryProducerDep) -> Any:
    """
    Create a new category
    """
    category = crud.create(session=session, obj_in=category_in)
    await producer.category_created(category.dict())
    return category


@router.patch("/{category_id}", dependencies=[Depends(get_current_active_superuser)], response_model=CategoryPublic)
async def update_category(*, session: SessionDep, category_id: int, category_in: CategoryUpdate, producer: CategoryProducerDep) -> Any:
    db_category = crud.category_crud.get_by_id(session=session, id=category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    db_category = crud.category_crud.update(session=session, db_obj=db_category, obj_in=category_in)
    await producer.category_updated(db_category.dict())
    return db_category

@router.get("/{category_id}", response_model=CategoryPublic)
def read_category_by_id(category_id: int, session: SessionDep) -> Any:
    category = crud.category_crud.get_by_id(session=session, id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.delete("/{category_id}", dependencies=[Depends(get_current_active_superuser)], response_model=Message)
async def delete_category(session: SessionDep, category_id: int, producer: CategoryProducerDep) -> Message:
    category = crud.category_crud.get_by_id(session=session, id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    crud.category_crud.remove(session=session, id=category_id)
    await producer.category_deleted(category.dict())
    return Message(message="Category deleted successfully")