from app.models import Cart, CartItem
from app.utils import CRUDBase

class CRUDCart(CRUDBase[Cart]):
    pass

class CRUDCartItem(CRUDBase[CartItem]):
    pass

cart_crud = CRUDCart(Cart)
cart_item_crud = CRUDCartItem(CartItem)