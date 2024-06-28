from typing import Any
from fastapi import APIRouter, HTTPException
from sqlmodel import select, func

from app.api.deps import SessionDep, ProductProducerDep, CurrentUser
from app.models import ProductPublic, Product, ProductsPublic, ProductCreate, ProductUpdate, Message
from app.crud import product_crud, category_crud, brand_crud

router = APIRouter()

@router.get("/", response_model=ProductsPublic)
async def get_all_products(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all products
    """
    count_statement = select(func.count()).select_from(Product)
    count = session.exec(count_statement).one()

    statement = select(Product).offset(skip).limit(limit)
    products = session.exec(statement).all()

    return ProductsPublic(data=products, count=count)
    

@router.post("/", response_model=ProductPublic)
async def create_product(*, session: SessionDep, product_in: ProductCreate, producer: ProductProducerDep, current_user: CurrentUser):
    """
    Create a new product
    """
    # Check if category exists
    category = category_crud.get_by_id(session=session, id=product_in.category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Check if brand exists
    brand = brand_crud.get_by_id(session=session, id=product_in.brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    product = product_crud.create(session=session, obj_in=product_in)
    await producer.product_created(product.dict())
    return product

@router.patch("/{product_id}", response_model=ProductPublic)
async def update_product(*, session: SessionDep, product_id: int, product_in: ProductUpdate, producer: ProductProducerDep, current_user: CurrentUser ) -> Any:
    """
    Update a product
    """
    db_product = product_crud.get_by_id(session=session, id=product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")    
    db_product = product_crud.update(session=session, db_obj=db_product, obj_in=product_in)
    await producer.product_updated(db_product.dict())
    return db_product

@router.get("/{product_id}", response_model=ProductPublic)
def get_product_by_id(product_id: int, session: SessionDep)-> Any:
    """
    Get a specific product by id.
    """
    product = product_crud.get_by_id(session=session, id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.delete("/{product_id}", response_model=Message)
async def delete_product(session: SessionDep, product_id: int, producer: ProductProducerDep, current_user: CurrentUser) -> Message:
    """
    Delete a product
    """
    product = product_crud.get_by_id(session=session, id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product_crud.remove(session=session, id=product_id)
    await producer.product_deleted(product.dict())
    return Message(message="Product deleted successfully")
