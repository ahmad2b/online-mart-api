from app.models import Product, Category, Brand
from app.utils import CRUDBase

class CRUDProduct(CRUDBase[Product]):
    pass

class CRUDCategory(CRUDBase[Category]):
    pass

class CRUDBrand(CRUDBase[Brand]):
    pass

product_crud = CRUDProduct(Product)
category_crud = CRUDCategory(Category)
brand_crud = CRUDBrand(Brand)
