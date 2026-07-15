"""
database.py

Handles all MySQL database communication for the
Student Grade Management System.

Only this class directly interacts with MySQL.
"""

import mysql.connector
from mysql.connector import Error


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

    def __init__(self, host="localhost", user="root", password="your_password", database="student_grade_manager"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
        self.connect()


    # ----------------------------------------------------------
    # Connection Methods
    # ----------------------------------------------------------
    def connect(self):
        """
        Establish connection with MySQL database.
        """
        try:
            self.connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)

        except Error as error:
            raise Exception(f"Database Connection Error : {error}")


    def disconnect(self):
        """
        Close cursor and database connection.
        """
        if self.cursor is not None:
            self.cursor.close()

        if self.connection is not None and self.connection.is_connected():
            self.connection.close()


    # ----------------------------------------------------------
    # Query Execution
    # ----------------------------------------------------------
    def execute_query(self, query, values=None):
        """
        Execute INSERT / UPDATE / DELETE query.
        Returns:
            last inserted id (if available)
        """
        try:
            if values is None:
                self.cursor.execute(query)
            else:
                self.cursor.execute(query, values)

            self.connection.commit()
            return self.cursor.lastrowid

        except Error as error:
            self.connection.rollback()
            raise Exception(f"Query Execution Error : {error}")
        

    def begin_transaction(self):
        """
        Starts a database transaction.
        """
        self.connection.start_transaction()


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
            and self.connection.is_connected()
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




