from sqlmodel import create_engine, SQLModel, Session
from app.core.config import settings


connection_string = str(settings.DATABASE_URL)

engine = create_engine(
    connection_string, connect_args={}, pool_recycle=300
)

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
