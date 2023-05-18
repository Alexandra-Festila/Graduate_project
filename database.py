""" A module for the persistence layer """

import sqlite3
import typing as t
from textwrap import dedent

class DatabaseManager:
    """ A class that provides an interface for managing a SQLite database. 
    The class has methods for connecting to the database, creating tables, 
    inserting, updating, and deleting data from tables, as well as querying 
    the database and fetching results."""

    def __init__(self, db_name: str):
        """Initializes the connection with the the SQLite database."""

        self.conn = sqlite3.connect(db_name)

    def __del__(self):
        """Closes the connection when the database is no longer in use."""
        
        self.conn.close()

    def _execute(self, statement: str) -> sqlite3.Cursor:
        """Takes an SQL statement and executes it with SQL"""
        cursor = self.conn.cursor()
        cursor.execute(statement)
        return cursor
    
    def create_table(self, table_name: str, columns: t.Dict[str, str]) -> None:
        """
        Takes in a table name and the columns names as parameters (names as keys and types as values) 
        and return the CREATE TABLE statement for SQLite.
        """
        columns_attributes = []
        for column_name, data_type in columns.items():
            current_column = f"{column_name} {data_type.upper()}"
            columns_attributes.append(current_column)
        columns_in_statement = ", ".join(columns_attributes)

        statement = f"""
            CREATE TABLE IF NOT EXISTS {table_name}(
                {columns_in_statement}
            );
        """

        self._execute(statement)

    def drop_table(self, table_name: str) -> None:
        """
        Takes in a table name to delete using the DROP TABLE statement for SQLite
        """

        statement = f"DROP TABLE {table_name};"
        self._execute(statement)

columns = {
    'id': 'integer primary key autoincrement',
    'name': 'text not null',
    'age': 'integer not null',
    'gender': 'text not null',
    'medical_history': 'text not null'
}
