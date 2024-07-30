from services.payments.payment_params.paypal.refund_breakdown import RefundBreakdown


class RefundPayPalPaymentResponse:
    def __init__(self, refund_id: str, status: str, refund_reason: str, refund_breakdown: RefundBreakdown):
        self.status = status
        self.refund_id = refund_id
        self.refund_breakdown = refund_breakdown
        self.refund_reason = refund_reason
