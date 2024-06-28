from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

class CartBase(SQLModel):
    user_id: int
    total_price: float = 0.0

class CartCreate(CartBase):
    pass

class CartUpdate(SQLModel):
    user_id: Optional[int] = None
    total_price: Optional[float] = None

class Cart(CartBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    items: List["CartItem"] = Relationship(back_populates="cart")

class CartPublic(CartBase):
    id: int
    items: List["CartItemPublic"]

class CartItemBase(SQLModel):
    product_id: int
    quantity: int
    price: float

class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(SQLModel):
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    price: Optional[float] = None

class CartItem(CartItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cart_id: Optional[int] = Field(default=None, foreign_key="cart.id")
    cart: Optional["Cart"] = Relationship(back_populates="items")

class CartItemPublic(CartItemBase):
    id: int
    cart_id: int
    
class CartItemsPublic(SQLModel):
    data: List[CartItemPublic]
    count: int

class CartsPublic(SQLModel):
    data: List[CartPublic]
    count: int

# Generic message
class Message(SQLModel):
    message: str
    
# Shared properties
class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = None

# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    
class AuthUserPublic(UserBase):
    id: int