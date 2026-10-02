"""
database.py

Handles all PostgreSQL database communication for the
Student Grade Management System.

Only this class directly interacts with PostgreSQL.
"""

import os

import psycopg2
from psycopg2 import Error
from psycopg2.extras import RealDictCursor


class DatabaseManager:
    """
    DatabaseManager is responsible only for database communication.

    Responsibilities:
    - Open database connection
    - Execute INSERT/UPDATE/DELETE
    - Execute SELECT
    - Return query results
    - Commit transactions
    - Close connection
    """

    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")

        if not self.database_url:
            raise Exception("DATABASE_URL environment variable is not set.")

        self.connection = None
        self.cursor = None
        self.connect()

    # ----------------------------------------------------------
    # Connection Methods
    # ----------------------------------------------------------
    def connect(self):
        """
        Establish connection with PostgreSQL database.
        """
        try:
            self.connection = psycopg2.connect(
                self.database_url
            )

            self.cursor = self.connection.cursor(
                cursor_factory=RealDictCursor
            )

        except Error as error:
            raise Exception(f"Database Connection Error : {error}")

    def disconnect(self):
        """
        Close cursor and database connection.
        """
        if self.cursor is not None:
            self.cursor.close()
            self.cursor = None

        if self.connection is not None and not self.connection.closed:
            self.connection.close()
            self.connection = None

    # ----------------------------------------------------------
    # Query Execution
    # ----------------------------------------------------------
    def execute_query(self, query, values=None):
        """
        Execute INSERT / UPDATE / DELETE query.

        If the query returns a row, for example:

            INSERT ... RETURNING student_id

        the first returned value is returned.

        Otherwise, None is returned.
        """
        try:
            if values is None:
                self.cursor.execute(query)
            else:
                self.cursor.execute(query, values)

            result = None

            if self.cursor.description is not None:
                result = self.cursor.fetchone()

            self.connection.commit()

            if result is not None:
                return next(iter(result.values()))

            return None

        except Error as error:
            self.connection.rollback()
            raise Exception(f"Query Execution Error : {error}")

    def begin_transaction(self):
        """
        Starts a database transaction.
        """
        self.connection.autocommit = False

    def fetch_one(self, query, values=None):
        """
        Execute SELECT query and return one row.
        """
        try:
            if values is None:
                self.cursor.execute(query)
            else:
                self.cursor.execute(query, values)

            return self.cursor.fetchone()

        except Error as error:
            raise Exception(f"Fetch Error : {error}")

    def fetch_all(self, query, values=None):
        """
        Execute SELECT query and return all rows.
        """
        try:
            if values is None:
                self.cursor.execute(query)
            else:
                self.cursor.execute(query, values)

            return self.cursor.fetchall()

        except Error as error:
            raise Exception(f"Fetch Error : {error}")

    # ----------------------------------------------------------
    # Utility Methods
    # ----------------------------------------------------------
    def record_exists(self, query, values=None):
        """
        Returns True if at least one record exists.
        """
        result = self.fetch_one(query, values)
        return result is not None

    def get_row_count(self):
        """
        Returns number of rows affected by previous query.
        """
        return self.cursor.rowcount

    def commit(self):
        """
        Commit current transaction.
        """
        try:
            self.connection.commit()
        except Error as error:
            raise Exception(f"Commit Error : {error}")

    def rollback(self):
        """
        Rollback current transaction.
        """
        try:
            self.connection.rollback()
        except Error as error:
            raise Exception(f"Rollback Error : {error}")

    def reconnect(self):
        """
        Reconnect to database.
        """
        self.disconnect()
        self.connect()

    def is_connected(self):
        """
        Returns True if database connection is active.
        """
        return (
            self.connection is not None
            and not self.connection.closed
        )

    # ----------------------------------------------------------
    # Context Manager Support
    # ----------------------------------------------------------
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

    # ----------------------------------------------------------
    # Destructor
    # ----------------------------------------------------------
    def __del__(self):
        try:
            self.disconnect()
        except Exception:
            pass

