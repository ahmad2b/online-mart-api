from typing import Optional, List
from sqlmodel import Field, SQLModel

# Shared properties
class ProductBase(SQLModel):
    name: str = Field(index=True)
    price: float
    description: Optional[str] = None
    sku: str = Field(unique=True, index=True)
    available: bool = True
    weight: Optional[str] = None
    dimensions: Optional[str] = None

# Properties to receive via API on product creation
class ProductCreate(ProductBase):
    category_id: Optional[int] = None
    brand_id: Optional[int] = None

# Properties to receive via API on product update
class ProductUpdate(SQLModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    sku: Optional[str] = None  # type: ignore
    available: Optional[bool] = None
    weight: Optional[str] = None
    dimensions: Optional[str] = None
    category_id: Optional[int] = None
    brand_id: Optional[int] = None
    
# Database model, database table inferred from class name
class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    category_id: Optional[int] = Field(foreign_key="category.id")
    brand_id: Optional[int] = Field(foreign_key="brand.id")

# Properties to return via API, id is always required
class ProductPublic(ProductBase):
    id: int

class ProductsPublic(SQLModel):
    data: List[ProductPublic]
    count: int

# Category Models

# Shared properties
class CategoryBase(SQLModel):
    name: str = Field(index=True)
    description: Optional[str] = None

# Properties to receive via API on category creation
class CategoryCreate(CategoryBase):
    pass

# Properties to receive via API on category update
class CategoryUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None

# Database model, database table inferred from class name
class Category(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

# Properties to return via API, id is always required
class CategoryPublic(CategoryBase):
    id: int

class CategoriesPublic(SQLModel):
    data: List[CategoryPublic]
    count: int

# Brand Models

# Shared properties
class BrandBase(SQLModel):
    name: str = Field(index=True)
    description: Optional[str] = None

# Properties to receive via API on brand creation
class BrandCreate(BrandBase):
    pass

# Properties to receive via API on brand update
class BrandUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None

# Database model, database table inferred from class name
class Brand(BrandBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

# Properties to return via API, id is always required
class BrandPublic(BrandBase):
    id: int

class BrandsPublic(SQLModel):
    data: List[BrandPublic]
    count: int

# Generic message
class Message(SQLModel):
    message: str
    
    
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

    
class AuthUserPublic(UserBase):
    id: int