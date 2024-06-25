from typing import List, Optional
from sqlmodel import Session, select
from app.models import Product, ProductCreate, ProductUpdate

def create_product(*, session: Session, product_create: ProductCreate) -> Product:
    db_obj = Product.model_validate(product_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def update_product(*, session: Session, db_product: Product, product_update: ProductUpdate) -> Product:
    product_data = product_update.model_dump(exclude_unset=True)
    db_product.sqlmodel_update(product_data)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

def get_product_by_id(*, session: Session, product_id: int) -> Optional[Product]:
    statement = select(Product).where(Product.id == product_id)
    return session.exec(statement).first()

def get_products(*, session: Session, skip: int = 0, limit: int = 10) -> List[Product]:
    statement = select(Product).offset(skip).limit(limit)
    return session.exec(statement).all()

def delete_product(*, session: Session, product_id: int) -> None:
    product = get_product_by_id(session=session, product_id=product_id)
    if product:
        session.delete(product)
        session.commit()
