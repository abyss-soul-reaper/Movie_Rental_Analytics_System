import mysql.connector
from db_errors import DB_ERROR_MAP
from exceptions.error_codes import ErrorCodes
from db_helpers import catch_db_errors, check_params
from exceptions.response_handler import ResponseHandler
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT

class DatabaseHandler:
    def __init__(self):
        self.conn = self._get_connection()

    def _get_connection(self):
        try:
            conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                port=int(DB_PORT)  # Ensure the port is an integer
            )

            ResponseHandler.info("Database connection established successfully.")
            return conn
        except mysql.connector.Error as e:
            error_info = DB_ERROR_MAP.get(e.errno, {
                "msg": "An unexpected database error occurred.",
                "technical_msg": str(e),
                "code": ErrorCodes.DB_CONNECTION_FAILED.value
            })
            ResponseHandler.critical(**error_info)

    def cursor(self):
        if not self.conn.is_connected():
            self.conn = self._get_connection()
        return self.conn.cursor(dictionary=True)

    @catch_db_errors
    def execute_query(self, query, params=()):
        """Used for INSERT, UPDATE, DELETE queries."""
        formatted_params = check_params(params)
        with self.cursor() as cursor:
            cursor.execute(query, formatted_params)
            self.commit()
            return cursor.rowcount

    @catch_db_errors
    def fetch_all(self, query, params=()):
        """Used to get all matching rows."""
        formatted_params = check_params(params)
        with self.cursor() as cursor:
            cursor.execute(query, formatted_params)
            return cursor.fetchall()

    @catch_db_errors
    def fetch_one(self, query, params=()):
        """Used to get a single matching row."""
        formatted_params = check_params(params)
        with self.cursor() as cursor:
            cursor.execute(query, formatted_params)
            return cursor.fetchone()

    @catch_db_errors
    def fetch_many(self, query, size, params=()):
        """Used to get a specific limit of rows."""
        formatted_params = check_params(params)
        with self.cursor() as cursor:
            cursor.execute(query, formatted_params)
            return cursor.fetchmany(size=size)

    def commit(self):
        self.conn.commit()



