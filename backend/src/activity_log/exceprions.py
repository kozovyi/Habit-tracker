from rest_framework import status
from rest_framework.exceptions import APIException

class InvalidDataProvided(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid date provided."
    default_code = "invalid_date"

class InvalidPeriodToDate(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "The period-to date cannot be future."
    default_code = "invalid_period_to_date"


class InvalidDateRange(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Period-from date must be before period-to date."
    default_code = "invalid_date_range"