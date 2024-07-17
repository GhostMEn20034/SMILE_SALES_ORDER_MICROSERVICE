import uuid


class ChangeArchivedStatusParams:
    def __init__(self, user_id: int, order_uuid: uuid.UUID, purpose: str):
        self.user_id = user_id
        self.order_uuid = order_uuid
        self.purpose = purpose
    