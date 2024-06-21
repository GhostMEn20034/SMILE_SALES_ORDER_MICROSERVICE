class AmountParamBase:
    def __init__(self, value: str, currency_code: str):
        self.value = value
        self.currency_code = currency_code


    def to_dict(self):
        return {
            'value': self.value,
            'currency_code': self.currency_code,
        }


class AmountBreakdown:
    """
    The subtotal for all items.
    Required if the request includes purchase_units[].items[].unit_amount.
    Must equal the sum of (items[].unit_amount * items[].quantity) for all items.
    item_total.value can not be a negative number.
    """
    def __init__(self, item_total: AmountParamBase):
        self.item_total = item_total

    def to_dict(self):
        return {
            'item_total': self.item_total.to_dict()
        }


class AmountParam(AmountParamBase):
    """
    The total order amount.
    PROPERTIES:
        value: The value, which might be:
            - An integer for currencies like JPY that are not typically fractional.
            - A decimal fraction for currencies like TND that are subdivided into thousandths.
        currency_code: The three-character ISO-4217 currency code that identifies the currency.
    """

    def __init__(self, value: str, currency_code: str, amount_breakdown: AmountBreakdown):
        super().__init__(value, currency_code, )
        self.breakdown = amount_breakdown

    def to_dict(self):
        return {
            'value': self.value,
            'currency_code': self.currency_code,
            'breakdown': self.breakdown.to_dict(),
        }


class UnitAmount(AmountParamBase):
    """
    The item price or rate per unit
    """
    pass
