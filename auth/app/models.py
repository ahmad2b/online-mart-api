from sqlmodel import Field, SQLModel

class AuthUserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    full_name: str | None = None
    is_active: bool = True
    is_superuser: bool = False

class AuthUserCreate(AuthUserBase):
    password: str

class AuthUser(AuthUserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str

class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(SQLModel):
    sub: int | None = None

class NewPassword(SQLModel):
    token: str
    new_password: str
    
# Generic message
class Message(SQLModel):
    message: str
