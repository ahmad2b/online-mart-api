from app.utils import CRUDBase
from app.models import Order, OrderItem, ShippingDetails, OrderHistory

crud_order = CRUDBase(Order)
crud_order_item = CRUDBase(OrderItem)
crud_shipping_details = CRUDBase(ShippingDetails)
crud_order_history = CRUDBase(OrderHistory)