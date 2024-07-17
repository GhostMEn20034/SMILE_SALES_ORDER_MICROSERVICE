from typing import Optional, Dict, Any
from django.utils import timezone
from datetime import datetime
from copy import deepcopy

from .consts import generate_last_n_years


class OrderListFiltersResolver:
    def __init__(self, order_status: Optional[str] = None, time_filter: Optional[str] = None):
        self.order_status = order_status if order_status else "allOrders"
        self.time_filter = time_filter

    def resolve_order_status(self) -> Dict[str, Any]:
        status_to_filters_mapping = {
            "allOrders": {},
            "notShipped": {
                "status__in": ['pending','processed', ]
            },
            "canceledOrders": {
                "status": "cancelled",
            },
        }

        return status_to_filters_mapping.get(self.order_status, {})

    @staticmethod
    def _get_year_to_filter_mapping() -> Dict[str, Dict[str, int]]:
        current_year = datetime.now().year
        year_to_filter_mapping = {}
        for year in range(current_year, current_year - generate_last_n_years, -1):
            year_to_filter_mapping[f"year-{year}"] = {"created_at__year": year}

        return year_to_filter_mapping

    @staticmethod
    def _get_other_filters_mapping() -> Dict[str, Any]:
        filters = {
            "archived": {"archived": True}
        }

        return filters

    def _get_default_time_filter(self) -> Optional[str]:

        if self.order_status == 'allOrders':
            default_time_filter = 'last30'
        elif self.order_status == 'canceledOrders':
            default_time_filter = 'last30'
        else:
            default_time_filter = None

        return default_time_filter

    def _get_custom_timeframe_to_filter_mapping(self):
        # Calculate the date 30 days ago from now
        thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
        # Calculate the date 3 months ago from now
        three_months_ago = timezone.now() - timezone.timedelta(days=90)
        # Calculate the date 3 months ago from now
        six_months_ago = timezone.now() - timezone.timedelta(days=180)


        time_filters_all_orders = {
            'last30': {
                'created_at__gte': thirty_days_ago,
            },
            'months-3': {
                'created_at__gte': three_months_ago,
            }
        }

        time_filters_canceled_orders = {
            'last30': {
                'created_at__gte': thirty_days_ago,
            },
            'months-6': {
                'created_at__gte': six_months_ago,
            },
        }

        order_status_to_time_filters_mapping = {
            "allOrders": time_filters_all_orders,
            "canceledOrders": time_filters_canceled_orders,
            "notShipped": {},
        }

        return order_status_to_time_filters_mapping.get(self.order_status, {})

    def resolve_time_filter(self) -> Dict[str, Any]:
        time_filters = deepcopy(self._get_custom_timeframe_to_filter_mapping())
        time_filters.update(self._get_year_to_filter_mapping())
        time_filters.update(self._get_other_filters_mapping())

        time_filter = self.time_filter if self.time_filter else self._get_default_time_filter()
        return time_filters.get(time_filter, {})
