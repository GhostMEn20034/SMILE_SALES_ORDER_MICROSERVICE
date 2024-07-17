from datetime import datetime
from typing import Dict, Optional

from .consts import time_filters_all_orders, time_filters_canceled_orders, generate_last_n_years


class OrderListFiltersGenerator:
    def __init__(self, order_status: str):
        self.order_status = order_status

    @staticmethod
    def __get_year_filters() -> Dict[str, str]:
        current_year = datetime.now().year
        years = {}
        for year in range(current_year, current_year - generate_last_n_years, -1):
            years[f"year-{year}"] = str(year)

        return years

    def _get_time_filters_for_all_orders(self):
        time_filters = {**time_filters_all_orders}

        year_filters: Dict[str, str] = self.__get_year_filters()
        time_filters.update(year_filters)

        return time_filters

    def _get_time_filters_for_canceled_orders(self):
        time_filters = {**time_filters_canceled_orders}

        year_filters: Dict[str, str] = self.__get_year_filters()
        time_filters.update(year_filters)

        return time_filters

    def get_filters(self) -> Optional[Dict[str, str]]:
        filters = None

        if self.order_status == "allOrders":
            filters = self._get_time_filters_for_all_orders()
        elif self.order_status == "canceledOrders":
            filters = self._get_time_filters_for_canceled_orders()
                   
        if filters is not None:
            filters["archived"] = "Archived Orders"


        return filters

