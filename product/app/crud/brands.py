from typing import Any, List, Optional
from sqlmodel import Session, select
from app.models import Brand, BrandCreate, BrandUpdate

def create_brand(*, session: Session, brand_create: BrandCreate) -> Brand:
    db_obj = Brand.model_validate(brand_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def update_brand(*, session: Session, db_brand: Brand, brand_update: BrandUpdate) -> Brand:
    brand_data = brand_update.model_dump(exclude_unset=True)
    db_brand.sqlmodel_update(brand_data)
    session.add(db_brand)
    session.commit()
    session.refresh(db_brand)
    return db_brand

def get_brand_by_id(*, session: Session, brand_id: int) -> Optional[Brand]:
    statement = select(Brand).where(Brand.id == brand_id)
    return session.exec(statement).first()

def get_brands(*, session: Session, skip: int = 0, limit: int = 10) -> List[Brand]:
    statement = select(Brand).offset(skip).limit(limit)
    return session.exec(statement).all()

def delete_brand(*, session: Session, brand_id: int) -> None:
    brand = get_brand_by_id(session=session, brand_id=brand_id)
    if brand:
        session.delete(brand)
        session.commit()
