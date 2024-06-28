from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

# Shared properties
class OrderBase(SQLModel):
    status: str
    total_amount: float
    
# Properties to receive via API on order creation
class OrderCreate(OrderBase):
    user_id: int
    items: List["OrderItemCreate"] = []
    shipping_details: Optional["ShippingDetailsCreate"] = None
    
# Database model, database table inferred from class name
class Order(OrderBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    items: List["OrderItem"] = Relationship(back_populates="order")
    shipping_details: Optional["ShippingDetails"] = Relationship(back_populates="order")
    order_history: List["OrderHistory"] = Relationship(back_populates="order")

# Properties to return via API, id is always required
class OrderPublic(OrderBase):
    id: int
    items: List["OrderItemPublic"]
    shipping_details: Optional["ShippingDetailsPublic"]
    order_history: List["OrderHistoryPublic"]

class OrdersPublic(SQLModel):
    data: List[OrderPublic]
    count: int
    
# Properties to receive via API on order update
class OrderUpdate(SQLModel):
    status: Optional[str] = None
    total_amount: Optional[float] = None
    
# OrderItem Models

# Shared properties
class OrderItemBase(SQLModel):
    product_id: int
    quantity: int
    price: float

# Properties to receive via API on order item creation
class OrderItemCreate(OrderItemBase):
    pass

# Properties to receive via API on order item update
class OrderItemUpdate(SQLModel):
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    price: Optional[float] = None

# Database model, database table inferred from class name
class OrderItem(OrderItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.id")
    order: "Order" = Relationship(back_populates="items")

# Properties to return via API, id is always required
class OrderItemPublic(OrderItemBase):
    id: int
    
class OrderItemsPublic(SQLModel):
    data: List[OrderItemPublic]
    count: int

# ShippingDetails Models

# Shared properties
class ShippingDetailsBase(SQLModel):
    address: str
    city: str
    postal_code: str
    country: str

# Properties to receive via API on shipping details creation
class ShippingDetailsCreate(ShippingDetailsBase):
    pass

# Properties to receive via API on shipping details update
class ShippingDetailsUpdate(SQLModel):
    address: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None

# Database model, database table inferred from class name
class ShippingDetails(ShippingDetailsBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.id")
    order: "Order" = Relationship(back_populates="shipping_details")

# Properties to return via API, id is always required
class ShippingDetailsPublic(ShippingDetailsBase):
    id: int

# OrderHistory Models

# Shared properties
class OrderHistoryBase(SQLModel):
    status: str
    timestamp: str

# Properties to receive via API on order history creation
class OrderHistoryCreate(OrderHistoryBase):
    pass

# Properties to receive via API on order history update
class OrderHistoryUpdate(SQLModel):
    status: Optional[str] = None
    timestamp: Optional[str] = None

# Database model, database table inferred from class name
class OrderHistory(OrderHistoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.id")
    order: "Order" = Relationship(back_populates="order_history")

# Properties to return via API, id is always required
class OrderHistoryPublic(OrderHistoryBase):
    id: int
   
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