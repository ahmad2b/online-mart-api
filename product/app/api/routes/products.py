from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, func

from app import crud
from app.api.deps import SessionDep, get_current_active_superuser, ProductProducer, get_product_producer ,ProductProducerDep
from app.models import ProductPublic, Product, ProductsPublic, ProductCreate, ProductUpdate, Message
from app.crud.index import product_crud as crud

router = APIRouter()

@router.get("/", response_model=ProductsPublic)
async def read_products(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all products
    """
    count_statement = select(func.count()).select_from(Product)
    count = session.exec(count_statement).one()

    statement = select(Product).offset(skip).limit(limit)
    products = session.exec(statement).all()

    return ProductsPublic(data=products, count=count)
    

@router.post("/", dependencies=[Depends(get_current_active_superuser)], response_model=ProductPublic)
async def create_product(*, session: SessionDep, product_in: ProductCreate, producer: ProductProducerDep):
    """
    Create a new product
    """
    product = crud.create(session=session, obj_in=product_in)
    await producer.product_created(product.dict())
    return product

@router.patch("/{product_id}", dependencies=[Depends(get_current_active_superuser)], response_model=ProductPublic)
async def update_product(*, session: SessionDep, product_id: int, product_in: ProductUpdate, producer: ProductProducerDep ) -> Any:
    """
    Update a product
    """
    db_product = crud.get_by_id(session=session, id=product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")    
    db_product = crud.update(session=session, db_obj=db_product, obj_in=product_in)
    await producer.product_updated(db_product.dict())
    return db_product

@router.get("/{product_id}", response_model=ProductPublic)
def get_product_by_id(product_id: int, session: SessionDep)-> Any:
    """
    Get a specific product by id.
    """
    product = crud.get_by_id(session=session, id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.delete("/{product_id}", dependencies=[Depends(get_current_active_superuser)], response_model=Message)
async def delete_product(session: SessionDep, product_id: int, producer: ProductProducerDep) -> Message:
    """
    Delete a product
    """
    product = crud.get_by_id(session=session, id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    crud.remove(session=session, id=product_id)
    await producer.product_deleted(product.dict())
    return Message(message="Product deleted successfully")
