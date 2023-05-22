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

    def _execute(self, statement: str, values: t.Optional[t.Tuple] = None) -> sqlite3.Cursor:
        """Takes an SQL statement and optionally values for placeholders and executes it with SQLite"""

        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute(statement, values or [])
                return cursor

        except (sqlite3.IntegrityError, sqlite3.OperationalError):
            print(
                f"Something went wrong with the following transaction:\n {statement}"
                )
            raise
    
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

        statement = dedent(
        f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                {columns_in_statement}
            );
        """
        )

        self._execute(statement)

    def drop_table(self, table_name: str) -> None:
        """
        Takes in a table name to delete using the DROP TABLE statement for SQLite
        """

        statement = f"DROP TABLE {table_name};"
        self._execute(statement)


    def add_record(self, table_name:str, data: t.Dict[str, t.Union[str, int, float]]) -> None:

        """Taken in a table name and creates an INSERT data INTO statement and a data dictionary 
        (the keys being columns and the values being data points)"""

        column_names = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data.keys()))
        column_values = tuple(data.values())

        statement = dedent(
            f"""
            INSERT INTO
                {table_name} (
                    {column_names}
                ) VALUES (
                    {placeholders}
                );
            """
        )

        self._execute(statement, column_values)

    def delete_record(self, table_name: str, criteria: t.Dict[str, t.Union[str, int, float]]) -> None:
        """Taken in a table name and creates a DELETE FROM statement and a criteria)"""

        placeholders = [f"{column} = ?" for column in criteria.keys()]
        delete_criteria = " AND ".join(placeholders)
        delete_criteria_values = tuple(criteria.values)

        statement = dedent(
            f"""
                DELETE FROM 
                    {table_name} 
                WHERE 
                    {delete_criteria};
            """
        )

        self._execute(statement, delete_criteria_values)

    def select_record(
        self, 
        table_name: str, 
        criteria: t.Dict[str, t.Union[str, int, float]] = {}, 
        order_by: t.Optional[str] = None,
        ordered_desc: bool = False
    ) -> sqlite3.Cursor:
        """
        Executes a SELECT statement on the specified table with optional criteria and ordering.
        Returns the result cursor.
        """

        select_criteria_values = tuple(criteria.values())

        statement = f"SELECT * FROM {table_name}"
        if criteria:
            placeholders = [f"{column} = ?" for column in criteria.keys()]
            select_criteria = " AND ".join(placeholders)
            statement = statement  + f" WHERE {select_criteria}"

        if order_by:
            statement = statement + f" ORDER BY {order_by}"
            if ordered_desc:
                statement = statement + f" DESC"

        statement = statement + ";"

        return self._execute(statement, select_criteria_values)








