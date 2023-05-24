from unittest import TestCase
from unittest.mock import patch

from src.commands import CreateVitalSignsTableCommand, AddRecordCommand


class CreateTableCommandTest(TestCase):
    def setUp(self):
        self.command = CreateVitalSignsTableCommand()

    def test_execute(self):
        with patch("src.commands.DatabaseManager.create_table") as mocked_create_table:
            self.command.execute()
            mocked_create_table.assert_called_with(
                table_name="vitals",
                columns={
                    'record_id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
                    'patient_id': 'INTEGER NOT NULL',
                    'date': 'TEXT NOT NULL',
                    'heart_rate': 'INTEGER',
                    'blood_pressure': 'TEXT',
                    'respiratory_rate': 'INTEGER',
                    'oxygen_saturation': 'REAL',
                    'temperature': 'REAL'
                }
            )


class AddRecordCommandTest(TestCase):
    def setUp(self):
        self.command = AddRecordCommand()

    def test_execute(self):
        with patch("src.commands.DatabaseManager.add_record") as mocked_add_record:
            data = {
                "patient_id": "mock_patient_id",
                "heart_rate": "mock_heart_rate",
                "blood_pressure": "mock_blood_pressure",
                "respiratory_rate": "mock_respiratory_rate",
                "oxygen_saturation": "mock_oxygen_saturation",
                "temperature": "mock_temperature",
            }
            result = self.command.execute(data)
            mocked_add_record.assert_called_with(
                table_name="vitals",
                data=data
            )
            expected_result = f"Vital signs successfully recorded for patient {data['patient_id']}."
            self.assertEqual(result, expected_result)
