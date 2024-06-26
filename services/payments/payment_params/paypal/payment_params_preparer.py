from decimal import Decimal
from typing import List, Union, Tuple
from django.db.models import QuerySet
from django.conf import settings

from apps.products.models import Product
from .purchase_unit_params import PurchaseItem, PurchaseUnit
from .amount_params import AmountParam, UnitAmount, AmountBreakdown, ItemTotalBreakdown
from param_classes.payments.build_purchase_unit_params import BuildPurchaseUnitParams

class PayPalPaymentParamsPreparer:
    @staticmethod
    def build_purchase_unit_items(products: Union[List[Product], QuerySet[Product]],
                                currency_code: str) -> Tuple[List[PurchaseItem], Decimal]:
        purchase_unit_items = []
        total_amount = Decimal("0.00")

        for product in products:
            discounted_price = round(product.discounted_price, 2)
            unit_amount = UnitAmount(
                value=str(discounted_price),
                currency_code=currency_code
            )

            purchase_unit_item = PurchaseItem(
                name=f"Product #{product.object_id}",
                quantity=4,
                url=f"{settings.FRONTEND_BASE_URL}/item/{product.object_id}",
                sku=product.sku,
                image_url=product.image,
                unit_amount=unit_amount
            )

            purchase_unit_items.append(purchase_unit_item)
            total_amount += discounted_price * purchase_unit_item.quantity

        return purchase_unit_items, total_amount

    @staticmethod
    def build_purchase_unit(params: BuildPurchaseUnitParams) -> PurchaseUnit:
        purchase_unit_items, total_amount = PayPalPaymentParamsPreparer.build_purchase_unit_items(
            params.products, params.currency_code
        )

        amount_breakdown = AmountBreakdown(
            item_total=ItemTotalBreakdown(
                value=str(round(total_amount, 2)),
                currency_code=params.currency_code,
            )
        )

        purchase_unit = PurchaseUnit(
            reference_id=params.reference_id, description=params.description,
            amount=AmountParam(
                value=str(round(total_amount, 2)),
                currency_code=params.currency_code,
                amount_breakdown=amount_breakdown,
            ),
            items=purchase_unit_items,
        )

        return purchase_unit

