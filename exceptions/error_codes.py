from enum import Enum

class ErrorCodes(Enum):
    # 1. (System Configuration)
    MISSING_ENV_FILE = 1001
    INCOMPLETE_CONFIG = 1002
    ROOT_USER_WARNING = 1003
    
    # 2. (Database Layer)
    DB_CONNECTION_FAILED = 2001
    SQL_QUERY_ERROR = 2002
    
    # 3. (Business Logic)
    INVALID_DATE_RANGE = 3001
    ZERO_DIVISION_IN_ANALYTICS = 3002
    
    # 4. (Exports)
    EXPORT_PERMISSION_DENIED = 4001
    FILE_WRITE_FAILED = 4002
