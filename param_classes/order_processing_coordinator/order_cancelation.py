import uuid


class OrderCancellationParams:
    def __init__(self, order_uuid: uuid.UUID):
        self.order_uuid = order_uuid

