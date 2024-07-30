from services.payments.payment_params.paypal.base.amount import AmountParamBase
from services.payments.payment_responses.paypal.refund_payment_response import RefundPayPalPaymentResponse
from services.payments.payment_params.paypal.refund_breakdown import RefundBreakdown


class PaymentRefundResponseParser:
    def __init__(self, response: dict):
        self.response = response

    def get_seller_payable_breakdown_item(self, key: str) -> AmountParamBase:
        seller_payable_breakdown_item = self.response["seller_payable_breakdown"][key]
        return AmountParamBase(
            currency_code=seller_payable_breakdown_item["currency_code"],
            value=seller_payable_breakdown_item["value"],
        )

    def parse(self) -> RefundPayPalPaymentResponse:
        refund_id = self.response["id"]
        status = self.response["status"]
        refund_reason = self.response["note_to_payer"]

        gross_amount = self.get_seller_payable_breakdown_item("gross_amount")
        provider_fee = self.get_seller_payable_breakdown_item("paypal_fee")
        net_amount = self.get_seller_payable_breakdown_item("net_amount")

        refund_breakdown_object = RefundBreakdown(
            gross_amount=gross_amount,
            provider_fee=provider_fee,
            net_amount=net_amount,
        )

        return RefundPayPalPaymentResponse(
            refund_id=refund_id,
            status=status,
            refund_reason=refund_reason,
            refund_breakdown=refund_breakdown_object,
        )


