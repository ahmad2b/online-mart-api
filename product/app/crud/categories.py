from typing import Any, List, Optional
from sqlmodel import Session, select
from app.models import Category, CategoryCreate, CategoryUpdate

def create_category(*, session: Session, category_create: CategoryCreate) -> Category:
    db_obj = Category.model_validate(category_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def update_category(*, session: Session, db_category: Category, category_update: CategoryUpdate) -> Category:
    category_data = category_update.model_dump(exclude_unset=True)
    db_category.sqlmodel_update(category_data)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category

def get_category_by_id(*, session: Session, category_id: int) -> Optional[Category]:
    statement = select(Category).where(Category.id == category_id)
    return session.exec(statement).first()

def get_categories(*, session: Session, skip: int = 0, limit: int = 10) -> List[Category]:
    statement = select(Category).offset(skip).limit(limit)
    return session.exec(statement).all()

def delete_category(*, session: Session, category_id: int) -> None:
    category = get_category_by_id(session=session, category_id=category_id)
    if category:
        session.delete(category)
        session.commit()
