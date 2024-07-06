class AmountParamBase:
    def __init__(self, value: str, currency_code: str):
        self.value = value
        self.currency_code = currency_code


    def to_dict(self):
        return {
            'value': self.value,
            'currency_code': self.currency_code,
        }
