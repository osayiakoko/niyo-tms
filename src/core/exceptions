from rest_framework.exceptions import APIException as DrfAPIException
from rest_framework import status


class APIException(DrfAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "api_exception"
    default_detail = "An exception occured"

    def __init__(self, status_code: int = None, detail: str = None, code: str = None):
        if status_code:
            self.status_code = status_code
        super().__init__(detail, code)
