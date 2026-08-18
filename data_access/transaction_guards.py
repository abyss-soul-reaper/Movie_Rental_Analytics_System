import mysql.connector
from functools import wraps
from typing import Callable, TypeVar
from pkg_exceptions.status_code import ErrorCodes
from data_access.exception_mapper import DB_ERROR_MAP
from pkg_exceptions.output_handler import ResponseHandler

T = TypeVar('T')  # Generic type for return value of the wrapped function

def check_params(params):
    if not params:
        return ()
    if isinstance(params, (tuple, list, dict)):
        return params
    return (params,)

def catch_db_errors(func: Callable[..., T]) -> Callable[..., ResponseHandler]:
    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        try:
            return ResponseHandler.ok(func(*args, **kwargs))
        except mysql.connector.Error as e:
            self.conn.rollback()

            error_info = DB_ERROR_MAP.get(e.errno, {
                "msg": "An unexpected database error occurred.",
                "technical_msg": str(e),
                "code": ErrorCodes.SQL_QUERY_ERROR.value
            })
            return ResponseHandler.exception(**error_info)
    return wrapper

