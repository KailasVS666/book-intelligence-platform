from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """
    Standardizes error responses across the entire API and ensures
    all server exceptions are logged with context.
    """
    # Call base exception handler first
    response = exception_handler(exc, context)

    if response is None:
        # This is an unhandled server error
        logger.error(f"Unhandled Exception: {str(exc)}", exc_info=True)
        return Response(
            {"error": "A serious server error occurred. Please contact systems administration."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Standardize the error format for handled exceptions
    custom_data = {
        "error": response.data.get('detail', 'Validation failed'),
        "errors": response.data if isinstance(response.data, dict) and 'detail' not in response.data else None
    }
    response.data = custom_data

    return response
