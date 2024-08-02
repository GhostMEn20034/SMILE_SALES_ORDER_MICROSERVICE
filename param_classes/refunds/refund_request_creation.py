from uuid import UUID


class RefundRequestCreationParams:
    def __init__(self, user_id: int, order_id: UUID, reason_for_return: str):
        self.user_id = user_id
        self.order_id = order_id
        self.reason_for_return = reason_for_return