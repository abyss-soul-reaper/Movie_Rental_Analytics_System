from functools import wraps
from typing import Callable, TypeVar
from pkg_exceptions.status_code import ErrorCodes
from pkg_exceptions.output_handler import ResponseHandler

T = TypeVar('T')  # Generic type for return value of the wrapped function

def catch_application_errors(func: Callable[..., T]) -> Callable[..., ResponseHandler]:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:

            result = func(*args, **kwargs)

            if isinstance(result, ResponseHandler):
                return result

            return ResponseHandler.ok(result)
        
        except Exception as e:

            error_info = {
                "msg": "An internal processing error occurred in the analytics system.",
                "technical_msg": str(e),
                "code": ErrorCodes.SERVICE_UNAVAILABLE.value
            }
            return ResponseHandler.exception(**error_info)
        
    return wrapper


