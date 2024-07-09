from typing import Dict, List
from services.payments.payment_params.paypal.base.amount import AmountParamBase
from services.payments.payment_responses.paypal.capture_payment_response import (
    CapturePayPalPaymentResponse
)
from services.payments.payment_params.base.capture import Capture


class PayPalCaptureResponseParser:
    def __init__(self, response: Dict):
        self.response = response

    @staticmethod
    def get_payment_info_from_purchase_units(purchase_units: List[Dict]):
        payment_information = []
        for purchase_unit in purchase_units:
            payments = purchase_unit['payments']
            payment_information.append(payments)

        return payment_information

    @staticmethod
    def get_seller_receivable_breakdown_item(capture: dict, key: str) -> AmountParamBase:
        seller_receivable_breakdown_item = capture["seller_receivable_breakdown"][key]
        return AmountParamBase(
            currency_code=seller_receivable_breakdown_item["currency_code"],
            value=seller_receivable_breakdown_item["value"],
        )

    @staticmethod
    def get_capture_info_from_payment(payment_information: Dict) -> List[Capture]:
        capture_info = []
        for capture in payment_information["captures"]:
            capture_id = capture["id"]
            gross_amount = PayPalCaptureResponseParser. \
                get_seller_receivable_breakdown_item(capture, "gross_amount")
            paypal_fee = PayPalCaptureResponseParser. \
                get_seller_receivable_breakdown_item(capture, "paypal_fee")
            net_amount = PayPalCaptureResponseParser. \
                get_seller_receivable_breakdown_item(capture, "net_amount")

            capture_item = Capture(
                capture_id=capture_id,
                gross_amount=gross_amount,
                provider_fee=paypal_fee,
                net_amount=net_amount
            )
            capture_info.append(capture_item)

        return capture_info

    def parse(self) -> CapturePayPalPaymentResponse:
        purchase_units = self.response["purchase_units"]
        payment_information = self.get_payment_info_from_purchase_units(purchase_units)
        captures = self.get_capture_info_from_payment(payment_information[0])

        return CapturePayPalPaymentResponse(
            payment_id=self.response["id"],
            captures=captures,
        )
