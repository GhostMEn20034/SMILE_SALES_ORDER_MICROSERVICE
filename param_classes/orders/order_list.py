from typing import Optional, Literal


class OrderListParams:
    def __init__(self, user_id: int,
                 order_status: Optional[Literal["allOrders", "notShipped", "canceledOrders"]] = None,
                 time_filter: Optional[str] = None):
        self.user_id = user_id
        self.order_status = order_status
        self.time_filter = time_filter
