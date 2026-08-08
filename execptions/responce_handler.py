# import os
import sys
import logging
from typing import Any, Optional

# os.makedirs("logs", exist_ok=True)

# log_path = os.path.join("logs", "app.log")

logging.basicConfig(
    filename=r'logs\app.log',
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ResponseHandler:
    def __init__(self, success: bool, data: Any = None, error_msg: Optional[str] = None, error_code: Optional[int] = None):
        self.success = success
        self.data = data
        self.error_msg = error_msg
        self.error_code = error_code

    @classmethod
    def ok(cls, data: Any = None):
        return cls(success=True, data=data)

    @classmethod
    def fail(cls, msg: str, technical_msg: Optional[str] = None, code: Optional[int] = None):
        logging.error(f"Operation failed: {technical_msg} [Code: {code}]")
        return cls(success=False, error_msg=msg, error_code=code)

    @classmethod
    def critical(cls, msg: str, technical_msg: Optional[str] = None, code: Optional[int] = None):
        logging.critical(f"{technical_msg} [Code: {code}]")
        print(f"❌ [CRITICAL ERROR]: {msg}")
        sys.exit(1)  # Exit the application on critical failure

    @classmethod
    def warning(cls, msg: str, technical_msg: Optional[str] = None, code: Optional[int] = None):
        logging.warning(f"{technical_msg} [Code: {code}]")
        print(f"⚠️ [WARNING]: {msg}")
        return cls(success=True, error_msg=msg, error_code=code)


