from sqlmodel import Field, SQLModel

# Shared properties
class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = None

# Properties to receive via API on user creation
class UserCreate(UserBase):
    pass

# Properties to receive via API on user update
class UserUpdate(UserBase):
    email: str | None = None  # type: ignore
    is_active: bool | None = None
    is_superuser: bool | None = None
    full_name: str | None = None

# Properties to receive via API on update, all are optional
class UserUpdateMe(SQLModel):
    full_name: str | None = None
    email: str | None = None

# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: int

class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int

# Generic message
class Message(SQLModel):
    message: str
