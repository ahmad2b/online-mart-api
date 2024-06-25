from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, func
from app.crud.index import brand_crud as crud
from app.api.deps import SessionDep, get_current_active_superuser, BrandProducerDep
from app.models import (
    Message, Brand, BrandCreate, BrandPublic, BrandUpdate, BrandsPublic
)

router = APIRouter()

@router.get("/", response_model=BrandsPublic)
def get_all_brands(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all brands
    """
    count_statement = select(func.count()).select_from(Brand)
    count = session.exec(count_statement).one()

    statement = select(Brand).offset(skip).limit(limit)
    brands = session.exec(statement).all()

    return BrandsPublic(data=brands, count=count)

@router.post("/", dependencies=[Depends(get_current_active_superuser)], response_model=BrandPublic)
async def create_brand(*, session: SessionDep, brand_in: BrandCreate, producer: BrandProducerDep) -> Any:
    """
    Create a new brand
    """
    brand = crud.brand_crud.create(session=session, obj_in=brand_in)
    await producer.brand_created(brand.dict())
    return brand

@router.patch("/{brand_id}", dependencies=[Depends(get_current_active_superuser)], response_model=BrandPublic)
async def update_brand(*, session: SessionDep, brand_id: int, brand_in: BrandUpdate, producer: BrandProducerDep) -> Any:
    """
    Update a brand
    """
    db_brand = crud.brand_crud.get_by_id(session=session, id=brand_id)
    if not db_brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    db_brand = crud.brand_crud.update(session=session, db_obj=db_brand, obj_in=brand_in)
    await producer.brand_updated(db_brand.dict())
    return db_brand

@router.get("/{brand_id}", response_model=BrandPublic)
def get_brand_by_id(brand_id: int, session: SessionDep) -> Any:
    """
    Get a specific brand by id."""
    brand = crud.brand_crud.get_by_id(session=session, id=brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return brand

@router.delete("/{brand_id}", dependencies=[Depends(get_current_active_superuser)], response_model=Message)
async def delete_brand(session: SessionDep, brand_id: int, producer: BrandProducerDep) -> Message:
    """
    Delete a brand
    """
    brand = crud.brand_crud.get_by_id(session=session, id=brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    crud.brand_crud.remove(session=session, id=brand_id)
    await producer.brand_deleted(brand.dict())
    return Message(message="Brand deleted successfully")
