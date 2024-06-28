from app.models import Inventory, Reservation, Adjustment
from app.utils import CRUDBase

class CRUDInventory(CRUDBase[Inventory]):
    pass

class CRUDReservation(CRUDBase[Reservation]):
    pass

class CRUDAdjustment(CRUDBase[Adjustment]):
    pass

inventory_crud = CRUDInventory(Inventory)
reservation_crud = CRUDReservation(Reservation)
adjustment_crud = CRUDAdjustment(Adjustment)
