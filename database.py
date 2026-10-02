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
        self._row_count = 0
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
            self.connection = None
            self.cursor = None
            raise Exception(f"Database Connection Error : {error}")

    def _ensure_connection(self):
        """
        Make sure the PostgreSQL connection and cursor are usable.
        Reconnect if either one has become unusable.
        """

        if self.connection is None or self.connection.closed != 0:
            self.connect()
            return

        if self.cursor is None or self.cursor.closed:
            self.cursor = self.connection.cursor(
                cursor_factory=RealDictCursor
            )

    def disconnect(self):
        """
        Safely close cursor and database connection.
        """

        try:
            if self.cursor is not None and not self.cursor.closed:
                self.cursor.close()
        except Exception:
            pass
        finally:
            self.cursor = None

        try:
            if self.connection is not None and self.connection.closed == 0:
                self.connection.close()
        except Exception:
            pass
        finally:
            self.connection = None

    # ----------------------------------------------------------
    # Query Execution
    # ----------------------------------------------------------
    def execute_query(self, query, values=None):
        """
        Execute INSERT / UPDATE / DELETE query.

        Returns:
            First returned value when the query uses RETURNING.
            Otherwise None.
        """

        try:
            self._ensure_connection()
            if values is None:
                self.cursor.execute(query)
            else:
                self.cursor.execute(query, values)

            self._row_count = self.cursor.rowcount
            result = None

            # PostgreSQL returns inserted IDs through RETURNING
            if "RETURNING" in query.strip().upper():
                result = self.cursor.fetchone()

            self.connection.commit()
            if result is not None:
                return list(result.values())[0]

            return None

        except Error as error:
            try:
                self.connection.rollback()
            except Exception:
                pass
            raise Exception(f"Query Execution Error : {error}")

    def begin_transaction(self):
        """
        Start a database transaction.
        """
        self._ensure_connection()
        self.connection.autocommit = False

    def fetch_one(self, query, values=None):
        """
        Execute SELECT query and return one row.
        """

        for attempt in range(2):

            try:
                self._ensure_connection()

                if values is None:
                    self.cursor.execute(query)
                else:
                    self.cursor.execute(query, values)

                result = self.cursor.fetchone()

                # End the transaction created by SELECT
                self.connection.commit()

                return result

            except Error as error:

                try:
                    self.connection.rollback()
                except Exception:
                    pass

                if attempt == 0:
                    self.reconnect()
                    continue

                raise Exception(f"Fetch Error : {error}")

    def fetch_all(self, query, values=None):
        """
        Execute SELECT query and return all rows.
        """

        for attempt in range(2):
            try:
                self._ensure_connection()

                if values is None:
                    self.cursor.execute(query)
                else:
                    self.cursor.execute(query, values)

                result = self.cursor.fetchall()

                # End the transaction created by SELECT
                self.connection.commit()
                return result

            except Error as error:

                try:
                    self.connection.rollback()
                except Exception:
                    pass

                if attempt == 0:
                    self.reconnect()
                    continue

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
        return self._row_count

    def commit(self):
        try:
            self._ensure_connection()
            self.connection.commit()
        except Error as error:
            raise Exception(f"Commit Error : {error}")

    def rollback(self):
        try:
            self._ensure_connection()
            self.connection.rollback()
        except Error as error:
            raise Exception(f"Rollback Error : {error}")

    def reconnect(self):
        """
        Safely reconnect to PostgreSQL.
        """
        try:
            if self.cursor is not None and not self.cursor.closed:
                self.cursor.close()
        except Exception:
            pass

        try:
            if self.connection is not None and self.connection.closed == 0:
                self.connection.close()
        except Exception:
            pass

        self.cursor = None
        self.connection = None
        self.connect()

    def is_connected(self):
        return (
            self.connection is not None
            and self.connection.closed == 0
            and self.cursor is not None
            and not self.cursor.closed
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

