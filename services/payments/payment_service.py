import uuid
from decimal import Decimal

from django.conf import settings

from param_classes.payments.build_purchase_unit_params import BuildPurchaseUnitParams
from .payment_clients.paypal import PayPalClient
from .payment_params.paypal.create_paypal_payment_params import CreatePaypalPaymentParams
from .payment_params.paypal.payment_source import PayPalPaymentSource
from .payment_params.paypal.experience_context import PayPalExperienceContext
from .payment_params.paypal.payment_params_preparer import PayPalPaymentParamsPreparer
from apps.products.models import Product



class PaymentService:
    def __init__(self):
        self.paypal_client = PayPalClient(
            settings.PAYPAL_CLIENT_ID,
            settings.PAYPAL_SECRET,
        )

    def create_paypal_payment(self):
        products = Product.objects.filter(price__lte=Decimal("1000.00"))[:5]
        build_purchase_unit_params = BuildPurchaseUnitParams(
            reference_id=str(uuid.uuid4()),
            description="Order in Smile Sales",
            products=products,
            currency_code="USD",
        )
        purchase_unit = PayPalPaymentParamsPreparer.build_purchase_unit(build_purchase_unit_params)
        experience_context = PayPalExperienceContext(
            brand_name="Smile Sales",
            shipping_preference="NO_SHIPPING",
            landing_page="LOGIN",
            user_action="PAY_NOW",
            return_url=f"{settings.FRONTEND_BASE_URL}/payments/success?order_id={purchase_unit.reference_id}",
            cancel_url=f"{settings.FRONTEND_BASE_URL}/payments/cancelled",
        )
        payment_source = PayPalPaymentSource(experience_context)

        create_payment_params = CreatePaypalPaymentParams(
            intent="CAPTURE",
            purchase_units=[purchase_unit, ],
            paypal_payment_source=payment_source,
        )

        created_payment_data = self.paypal_client.create_payment(create_payment_params)
        return created_payment_data
