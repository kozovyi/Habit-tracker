from rest_framework import status
from rest_framework.exceptions import APIException


class InvalidDataProvided(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid date provided."
    default_code = "invalid_date"

