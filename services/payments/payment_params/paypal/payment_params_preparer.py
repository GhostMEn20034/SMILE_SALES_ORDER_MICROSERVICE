from decimal import Decimal
from typing import List, Union
from django.db.models import QuerySet
from django.conf import settings

from apps.orders.models import OrderItem
from .purchase_unit_params import PurchaseItem, PurchaseUnit, AmountParam
from .amount_params import UnitAmount, AmountBreakdown, ItemTotalBreakdown, TaxAmount, TaxTotalBreakdown
from param_classes.payments.build_purchase_unit_params import BuildPurchaseUnitParams
from result_classes.payments.purchase_unit_build import PurchaseUnitBuildResult


class PayPalPaymentParamsPreparer:
    @staticmethod
    def build_purchase_unit_items(order_items: Union[List[OrderItem], QuerySet[OrderItem]],
                                  currency_code: str) -> PurchaseUnitBuildResult:
        purchase_unit_items = []
        total_amount = Decimal("0.00")
        total_tax = Decimal("0.00")

        for order_item in order_items:
            price_per_unit = round(order_item.price_per_unit, 2)
            tax = round(order_item.tax_per_unit, 2)

            unit_amount = UnitAmount(
                value=str(price_per_unit),
                currency_code=currency_code
            )

            tax_amount = TaxAmount(
                value=str(tax),
                currency_code=currency_code
            )

            purchase_unit_item = PurchaseItem(
                name=f"Product #{order_item.product.object_id}",
                quantity=order_item.quantity,
                url=f"{settings.FRONTEND_BASE_URL}/item/{order_item.product.object_id}",
                sku=order_item.product.sku,
                image_url=order_item.product.image,
                unit_amount=unit_amount,
                tax=tax_amount,
            )

            purchase_unit_items.append(purchase_unit_item)
            total_amount += price_per_unit * purchase_unit_item.quantity
            total_tax += tax * purchase_unit_item.quantity

        return PurchaseUnitBuildResult(
            purchase_unit_items=purchase_unit_items,
            total_items_amount=total_amount,
            total_items_tax=total_tax,
        )

    @staticmethod
    def build_purchase_unit(params: BuildPurchaseUnitParams) -> PurchaseUnit:
        purchase_unit_build_result = PayPalPaymentParamsPreparer.build_purchase_unit_items(
            params.order_items, params.currency_code
        )
        total_amount = round(purchase_unit_build_result.total_items_amount, 2)
        total_tax = round(purchase_unit_build_result.total_items_tax, 2)


        overall_total = round(total_amount + total_tax, 2
                              )

        item_total = ItemTotalBreakdown(
            value=str(total_amount),
            currency_code=params.currency_code,
        )

        tax_total = TaxTotalBreakdown(
            value=str(total_tax),
            currency_code=params.currency_code,
        )

        amount_breakdown = AmountBreakdown(
            item_total=item_total,
            tax_total=tax_total
        )

        purchase_unit = PurchaseUnit(
            reference_id=params.reference_id, description=params.description,
            amount=AmountParam(
                value=str(overall_total),
                currency_code=params.currency_code,
                amount_breakdown=amount_breakdown,
            ),
            items=purchase_unit_build_result.purchase_unit_items,
        )

        return purchase_unit
