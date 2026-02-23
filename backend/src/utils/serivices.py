from typing import Type
from rest_framework.serializers import Serializer


from rest_framework import status
from rest_framework.exceptions import APIException

class InvalidDataProvided(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid data provided."
    default_code = "invalid_data"

def validate_by_serializer(
    SerializerClass: Type[Serializer], context, data=None, many=False
):
    request = context.get("request")
    user = "anonymous" if not request else request.user
    data = (
        data
        if data is not None
        else getattr(request, "data", {}) if request else {}
    )

    serializer = SerializerClass(data=data, context=context, many = many)
    if serializer.is_valid():
        validated_data = serializer.validated_data
    else:
        # logger.info(f"User: <{user}>  provided invalid data: <{serializer.errors}>")
        raise InvalidDataProvided(
            detail=f"User: <{user}>  provided invalid data: <{serializer.errors}>"
        )
    return validated_data
