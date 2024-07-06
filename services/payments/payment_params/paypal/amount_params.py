from services.payments.payment_params.paypal.base.amount import AmountParamBase


class ItemTotalBreakdown(AmountParamBase):
    pass

class TaxTotalBreakdown(AmountParamBase):
    pass


class AmountBreakdown:
    """
    The subtotal for all items.
    Required if the request includes purchase_units[].items[].unit_amount.
    Must equal the sum of (items[].unit_amount * items[].quantity) for all items.
    item_total.value can not be a negative number.
    """
    def __init__(self, item_total: ItemTotalBreakdown, tax_total: TaxTotalBreakdown):
        self.item_total = item_total
        self.tax_total = tax_total

    def to_dict(self):
        return {
            'item_total': self.item_total.to_dict(),
            'tax_total': self.tax_total.to_dict(),
        }


class UnitAmount(AmountParamBase):
    """
    The item price or rate per unit
    """
    pass


class TaxAmount(AmountParamBase):
    """
    The item tax per unit
    """
    pass
