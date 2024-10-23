from rest_framework.response import Response
from rest_framework.views import exception_handler

def custom_response(status, message, data=None, errors=None, status_code=200):
    return Response({
        "status": status,
        "message": message,
        "data": data,
        "errors": errors
    }, status=status_code)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        custom_response_data = {
            "status": "error",
            "message": str(exc),
            "data": None,
            "errors": response.data
        }
        response.data = custom_response_data
    return response

