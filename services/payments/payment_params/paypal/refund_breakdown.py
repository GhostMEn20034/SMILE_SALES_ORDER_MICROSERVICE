from services.payments.payment_params.paypal.base.amount import AmountParamBase


class RefundBreakdown:
    def __init__(self, gross_amount: AmountParamBase, provider_fee: AmountParamBase, net_amount: AmountParamBase):
        self.provider_fee = provider_fee
        self.gross_amount = gross_amount
        self.net_amount = net_amount
