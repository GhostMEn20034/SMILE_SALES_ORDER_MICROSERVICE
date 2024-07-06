from result_classes.orders.create_order import CreateOrderResult


class InitializePaymentParams:
    """
    Params required to initialize the payment
    """
    def __init__(self, created_order: CreateOrderResult):
        self.created_order = created_order

