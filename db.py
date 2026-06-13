from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
import mysql.connector

class DataBaseHandlers:
    def __init__(self):
        self.conn = self._get_connection()

    def _get_connection(self):
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn

    def cursor(self):
        cursor = self.conn.cursor(dictionary=True)
        return cursor

    def execute_query(self, query, params=None):
        cursor = self.cursor()
        cursor.execute(query, params if params else ())
        
        self.commit()
        cursor.close()

        return cursor

    def fetch_all(self, query, params=None):
        cursor = self.cursor()
        cursor.execute(query, params if params else ())
        cursor.fetchall()

        self.commit()
        cursor.close()
        
        return cursor

    def fetch_one(self, query, params=None):
        cursor = self.cursor()
        cursor.execute(query, params if params else ())
        cursor.fetchone()

        self.commit()
        cursor.close()
        
        return cursor

    def fetch_many(self, query, size, params=None):
        cursor = self.cursor()
        cursor.execute(query, params if params else ())
        cursor.fetchmany(size=size)
        
        self.commit()
        cursor.close()
        
        return cursor

    def commit(self):
        self.conn.commit()

    