from mysql.connector import errorcode
from execptions.error_codes import ErrorCodes


CR_CONN_HOST_ERROR = 2003  # Can't connect to MySQL server

DB_ERROR_MAP = {
    # --- أخطاء مرحلة الاتصال (Connection Layer) ---
    errorcode.ER_ACCESS_DENIED_ERROR: {
        "msg": "Something went wrong. Please try again later.",
        "technical_msg": "Check your DB_USER and DB_PASSWORD in the .env file.",
        "code": ErrorCodes.DB_CONNECTION_FAILED.value
    },
    errorcode.ER_BAD_DB_ERROR: {
        "msg": "The system is currently undergoing maintenance. Please wait.",
        "technical_msg": "Check your DB_NAME in the .env file.",
        "code": ErrorCodes.DB_CONNECTION_FAILED.value
    },
    CR_CONN_HOST_ERROR: {
        "msg": "Unable to establish connection. Please check your internet or try again.",
        "technical_msg": "Check your DB_HOST and DB_PORT. Verify if the database server is running.",
        "code": ErrorCodes.DB_CONNECTION_FAILED.value
    },

    # --- أخطاء مرحلة العمليات والاستعلامات (Query & CRUD Layer) ---
    errorcode.ER_PARSE_ERROR: {
        "msg": "An unexpected error occurred while processing your request.",
        "technical_msg": "Syntax error in the SQL statement. Review the query string format.",
        "code": ErrorCodes.SQL_QUERY_ERROR.value
    },
    errorcode.ER_NO_SUCH_TABLE: {
        "msg": "An internal service error occurred. Our team has been notified.",
        "technical_msg": "The table specified in the query does not exist in the schema.",
        "code": ErrorCodes.SQL_QUERY_ERROR.value
    },
    errorcode.ER_DUP_ENTRY: {
        "msg": "The data you entered could not be saved. Please verify your inputs.",
        "technical_msg": "The value provided already exists in a unique key column (Duplicate Entry).",
        "code": ErrorCodes.SQL_QUERY_ERROR.value
    },
    errorcode.ER_NO_REFERENCED_ROW_2: {
        "msg": "Action denied. The requested operation is invalid.",
        "technical_msg": "The referenced relation key does not exist in the parent table (Foreign Key violation).",
        "code": ErrorCodes.SQL_QUERY_ERROR.value
    },
    errorcode.ER_ROW_IS_REFERENCED_2: {
        "msg": "This item cannot be modified or deleted at this moment.",
        "technical_msg": "The row is locked by foreign key constraints from dependent tables.",
        "code": ErrorCodes.SQL_QUERY_ERROR.value
    }
}
