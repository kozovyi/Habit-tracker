from datetime import date
import pytest

from rest_framework import status
from rest_framework.test import APIClient

from activity_log.exceprions import InvalidDateRange, InvalidPeriodToDate
from activity_log.serivices import ActivityStatisticsService
    
case = [
    {"period_from": date(2026, 1, 1), "period_to": date(2026, 1, 21), "err": None},
    {"period_from": date(2026, 1, 1), "period_to": date(2025, 1, 1), "err": InvalidDateRange},
    {"period_from": date(2026, 1, 1), "period_to": date(2040, 1, 1), "err": InvalidPeriodToDate},
    {"period_from": date(2040, 1, 1), "period_to": date(2041, 1, 1), "err": InvalidPeriodToDate},
]

@pytest.mark.parametrize("case", case)
def test_validate_date_range(case):
    data = {
        "period_from": case["period_from"],
        "period_to": case["period_to"]
    }
    err = case["err"]

    if err:
        with pytest.raises(err):
            ActivityStatisticsService.validate_date_range(None, data) == data # type: ignore

    else:
        assert ActivityStatisticsService.validate_date_range(None, data) == data