from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
import mysql.connector

class DatabaseHandler:
    def __init__(self):
        self.conn = self._get_connection()

    def _get_connection(self):
        return mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

    def cursor(self):
        return self.conn.cursor(dictionary=True)

    def execute_query(self, query, params=()):
        """Used for INSERT, UPDATE, DELETE queries."""
        formatted_params = self.check_params(params)
        with self.cursor() as cursor:
            cursor.execute(query, formatted_params)
            self.commit()
            return cursor.rowcount

    def fetch_all(self, query, params=()):
        """Used to get all matching rows."""
        formatted_params = self.check_params(params)
        with self.cursor() as cursor:
            cursor.execute(query, formatted_params)
            return cursor.fetchall()

    def fetch_one(self, query, params=()):
        """Used to get a single matching row."""
        formatted_params = self.check_params(params)
        with self.cursor() as cursor:
            cursor.execute(query, formatted_params)
            return cursor.fetchone()

    def fetch_many(self, query, size, params=()):
        """Used to get a specific limit of rows."""
        formatted_params = self.check_params(params)
        with self.cursor() as cursor:
            cursor.execute(query, formatted_params)
            return cursor.fetchmany(size=size)

    def commit(self):
        self.conn.commit()

    @staticmethod
    def check_params(params):
        # Catches None, (), [], {}, and forces a safe empty tuple
        if not params:
            return ()
        # Passes pre-formed valid containers directly through
        if isinstance(params, (tuple, list, dict)):
            return params
        # Safely wraps isolated strings/integers into a 1-item tuple
        return (params,)
