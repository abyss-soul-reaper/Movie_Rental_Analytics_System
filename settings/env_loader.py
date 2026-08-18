import os
from dotenv import load_dotenv
from pkg_exceptions.status_code import ErrorCodes
from pkg_exceptions.output_handler import ResponseHandler

env_loaded = load_dotenv()

if not env_loaded:
    ResponseHandler.critical(
        msg="System startup failed: Environment and configuration settings are incomplete.",
        technical_msg=".env file is missing from the project root.",
        code=ErrorCodes.MISSING_ENV_FILE.value
    )

DB_HOST     =           os.getenv("DB_HOST")
DB_USER     =           os.getenv("DB_USER")
DB_PASSWORD =       os.getenv("DB_PASSWORD")
DB_NAME     =           os.getenv("DB_NAME")
DB_PORT     =     os.getenv("DB_PORT", 3306)  # Default to 3306 if not set

missing_critical_vars = []
if not DB_HOST:
    missing_critical_vars.append("DB_HOST")
if not DB_USER:
    missing_critical_vars.append("DB_USER")
if not DB_PASSWORD:
    missing_critical_vars.append("DB_PASSWORD")
if not DB_NAME:
    missing_critical_vars.append("DB_NAME")

if missing_critical_vars:
    ResponseHandler.critical(
        msg="System startup failed: Environment and configuration settings are incomplete.",
        technical_msg=f"Missing required keys in .env: {', '.join(missing_critical_vars)}",
        code=ErrorCodes.INCOMPLETE_CONFIG.value
    )

if DB_USER.lower() == "root": # type: ignore #
    ResponseHandler.warning(
        msg="Using 'root' as the database user is not recommended for production environments.",
        technical_msg="The 'root' user has full privileges and should only be used for administrative tasks.",
        code=ErrorCodes.ROOT_USER_WARNING.value
    )

ResponseHandler.info("Environment variables and system configurations loaded successfully.")




