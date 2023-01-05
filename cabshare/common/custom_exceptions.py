from rest_framework.exceptions import APIException
from rest_framework import status

class SuspiciousOperationException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'duplicate record'
    default_code = 'duplicate_record'

class ValidationException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'failed validation'
    default_code = 'failed_validation'