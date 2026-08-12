import mysql.connector
from db_errors import DB_ERROR_MAP
from exceptions.error_codes import ErrorCodes
from exceptions.response_handler import ResponseHandler

def check_params(params):
    if not params:
        return ()
    if isinstance(params, (tuple, list, dict)):
        return params
    return (params,)

def catch_db_errors(func):
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

