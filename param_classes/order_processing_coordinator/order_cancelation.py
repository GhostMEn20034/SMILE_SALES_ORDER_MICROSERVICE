import uuid


class OrderCancellationParams:
    def __init__(self, order_uuid: uuid.UUID, user_id: int):
        self.order_uuid = order_uuid
        self.user_id = user_id
