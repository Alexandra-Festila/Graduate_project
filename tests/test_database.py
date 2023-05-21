import sqlite3 

from unittest import TestCase
from unittest.mock import patch
from textwrap import dedent

from src.database import DatabaseManager

class CreateTableTest(TestCase):
    def setUp(self):
        self.db = DatabaseManager(":memory:")

    def test_create_table(self):
        with patch("src.database.DatabaseManager._execute") as mock_execute:
            self.db.create_table(
                table_name="test_table",
                columns={
                    "id": "integer primary key autoincrement",
                    "test_column_one": "text not null",
                    "test_column_two": "text not null"
                }
            )

            mock_execute.assert_called_with(
                dedent(
                    """
                        CREATE TABLE IF NOT EXISTS test_table (
                            id INTEGER PRIMARY KEY AUTOINCREMENT, test_column_one TEXT NOT NULL, test_column_two TEXT NOT NULL
                        );
                    """
                )
            )

    def test_missing_table_name(self):
        with self.assertRaises(sqlite3.OperationalError):
            self.db.create_table(
                table_name="",
                columns={
                    "id": "integer primary key autoincrement",
                    "test_column_one": "text not null",
                    "test_column_two": "text not null"
                }
            )

    def tearDown(self):
        del self.db

class DropTableTest(TestCase):
    def setUp(self):
        self.db = DatabaseManager(":memory:")

    def test_drop_table(self):
        with patch("src.database.DatabaseManager._execute") as mock_execute:
            self.db.drop_table(table_name="test_table")
            mock_execute.assert_called_with("DROP TABLE test_table;")

    def tearDown(self):
        del self.db

class AddRecordTest(TestCase):
    def setUp(self):
        self.db = DatabaseManager(":memory:")

    def test_add_record(self):
        with patch("src.database.DatabaseManager._execute") as mock_execute:
            self.db.add_record(
                table_name="test_table",
                data={
                    "key_one": "value_one",
                    "key_two": 42,
                    "key_three": 3.14
                }
            )

        mock_execute.assert_called_once_with(
                        dedent(
                            """
                            INSERT INTO
                                test_table (
                                    key_one, key_two, key_three
                                ) VALUES (
                                    ?, ?, ?
                                );
                            """
                        ), 
                        ("value_one", 42, 3.14)
                    )

    def tearDown(self):
        del self.db

class SelectRecordTest(TestCase):
    def setUp(self):
        self.db = DatabaseManager(":memory:")

    def test_select_record(self):
        with patch("src.database.DatabaseManager._execute") as mock_execute:
            self.db.select_record(
                table_name="test_table",
            )
            mock_execute.assert_called_once_with(
                "SELECT * FROM test_table;", ()
            )

    def test_select_record_by_criteria(self):
        with patch("src.database.DatabaseManager._execute") as mock_execute:
            self.db.select_record(
                table_name="test_table",
                criteria={
                    "key_one": "value_one",
                    "key_two": 42,
                    "key_three": 3.14
                },
            )
            mock_execute.assert_called_once_with(
                "SELECT * FROM test_table WHERE key_one = ? AND key_two = ? AND key_three = ?;",
                ("value_one", 42, 3.14)
            )

    def test_select_record_by_criteria_ord(self):
        with patch("src.database.DatabaseManager._execute") as mock_execute:
            self.db.select_record(
                table_name="test_table",
                criteria={
                    "key_one": "value_one",
                    "key_two": 42,
                    "key_three": 3.14
                },
                order_by="key_one"
            )
            mock_execute.assert_called_once_with(
                "SELECT * FROM test_table WHERE key_one = ? AND key_two = ? AND key_three = ? ORDER BY key_one;",
                ("value_one", 42, 3.14)
            )

    def tearDown(self):
        del self.db

    class DeleteRecordTest(TestCase):
        def setUp(self) -> None:
            self.db = DatabaseManager(":memory:")

        def test_delete_entry(self):
            with patch("src.database.DatabaseManager._execute") as mock_execute:
                self.db.delete_record(
                    table_name="test_table",
                    criteria={
                        "key_one": "value_one",
                        "key_two": 42,
                        "key_three": 3.14
                    },
                )
                mock_execute.assert_called_once_with(
                    dedent(
                        """
                        DELETE FROM
                            test_table
                        WHERE
                            key_one = ? AND key_two = ? AND key_three =?;
                        """
                    ),
                    ("value_one", "value_two", "value_three")
                )

        def test_delete_entry_missing_criteria(self):
            with patch("src.database.DatabaseManager._execute"):
                with self.assertRaises(TypeError):
                    self.db.delete_record(
                        table_name="test_table",
                    )

        def tearDown(self) -> None:
            del self.db

