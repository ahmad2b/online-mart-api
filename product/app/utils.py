from typing import TypeVar, Generic, Type, Optional, List, Any
from sqlmodel import SQLModel, Session, select

T = TypeVar("T", bound=SQLModel)

class CRUDBase(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    def create(self, *, session: Session, obj_in: T) -> T:
        db_obj = self.model.model_validate(obj_in)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def update(self, *, session: Session, db_obj: T, obj_in: Any) -> T:
        obj_data = obj_in.model_dump(exclude_unset=True)
        db_obj.sqlmodel_update(obj_data)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def get_by_id(self, *, session: Session, id: int) -> Optional[T]:
        statement = select(self.model).where(self.model.id == id)
        return session.exec(statement).first()

    def get_multi(self, *, session: Session, skip: int = 0, limit: int = 10) -> List[T]:
        statement = select(self.model).offset(skip).limit(limit)
        return session.exec(statement).all()

    def remove(self, *, session: Session, id: int) -> None:
        obj = self.get_by_id(session=session, id=id)
        if obj:
            session.delete(obj)
            session.commit()
