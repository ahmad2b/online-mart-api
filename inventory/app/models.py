from typing import Optional, List
from sqlmodel import Field, SQLModel

# Shared properties for Inventory Item
class InventoryBase(SQLModel):
    product_id: int = Field(index=True)  # Reference to the product
    quantity: int
    location: Optional[str] = None

# Properties to receive via API on inventory item creation
class InventoryCreate(InventoryBase):
    pass

# Properties to receive via API on inventory item update
class InventoryUpdate(SQLModel):
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    location: Optional[str] = None

# Database model, database table inferred from class name
class Inventory(InventoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

# Properties to return via API, id is always required
class InventoryPublic(InventoryBase):
    id: int

class InventoriesPublic(SQLModel):
    data: List[InventoryPublic]
    count: int

# Reservation Models

# Shared properties for Reservation
class ReservationBase(SQLModel):
    reserved_quantity: int
    reservation_date: str  # This should ideally be a date type

# Properties to receive via API on reservation creation
class ReservationCreate(ReservationBase):
    inventory_id: int
    
class ReservationUpdate(SQLModel):
    reserved_quantity: Optional[int] = None
    reservation_date: Optional[str] = None

class Reservation(ReservationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    inventory_id: int = Field(foreign_key="inventory.id")

class ReservationPublic(ReservationBase):
    id: int

class ReservationsPublic(SQLModel):
    data: List[ReservationPublic]
    count: int

# Adjustment Models

# Shared properties for Adjustment
class AdjustmentBase(SQLModel):
    adjustment_quantity: int
    adjustment_date: str  # This should ideally be a date type
    reason: Optional[str] = None

class AdjustmentCreate(AdjustmentBase):
    inventory_id: int

class AdjustmentUpdate(SQLModel):
    adjustment_quantity: Optional[int] = None
    adjustment_date: Optional[str] = None
    reason: Optional[str] = None

class Adjustment(AdjustmentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    inventory_id: int = Field(foreign_key="inventory.id")

class AdjustmentPublic(AdjustmentBase):
    id: int

class AdjustmentsPublic(SQLModel):
    data: List[AdjustmentPublic]
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

    
class AuthUserPublic(UserBase):
    id: int