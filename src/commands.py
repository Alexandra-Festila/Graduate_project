import sys

import typing as t

from datetime import datetime

from src.database import DatabaseManager

db = DatabaseManager("patient_monitoring.db")

class Command(t.Protocol):
    def execute(self):
        pass

class CreateVitalSignsTableCommand:
    def execute(self):
        db.create_table(
            table_name="vitals",
            columns={
                'record_id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
                'patient_id': 'INTEGER NOT NULL',
                'date': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
                'heart_rate': 'INTEGER',
                'blood_pressure': 'TEXT',
                'respiratory_rate': 'INTEGER',
                'oxygen_saturation': 'REAL',
                'temperature': 'REAL'
            }
        )

class AddRecordCommand:
    """ A command class the adds a vitals record for a patient"""

    def execute(self, data: t.Dict[str, t.Union[str, int, float]], timestamp: t.Optional[str]) -> str:
        "The actual execution of the command."

        date = timestamp or datetime.utcnow().isoformat()
        data.setdefault("date", date)
        patient_id = data["patient_id"]

        db.add_record(table_name="vitals", data=data)

        return f"Vital signs successfully recorded for patient {patient_id}."


class ListRecordsCommand:
    """A command class that lists vitals records based on specific criteria."""

    def __init__(self, order_by: str = "date"):
        self.order_by = order_by

    def execute(self) -> t.List[str]:
        "The actual execution of the command."

        cursor = db.select_record(
            table_name="vitals",
            order_by=self.order_by
        )
        results = cursor.fetchall()
        return results

class GetPatientRecordsCommand:
    """A command class that will return all the records of a specific patient."""

    def execute (self, data: int) -> t.Optional[tuple]:
        result = db.select_record(table_name="vitals", criteria={"patient_id": data}).fetchone()
        return result


class DeleteRecordCommand:
        """A command class that deletes a single record from the SQL table"""
        
        def execute(self, data: int) -> str:
            db.delete_record(table_name="vitals", criteria={"id": data})
            return f"Record {data} deleted."


class DeletePatientRecordsCommand:
        """A command class that deletes a record from the SQL table"""
        
        def execute(self, data: int) -> str:
            db.delete_record(table_name="vitals", criteria={"patient_id": data})
            return f"All records deleted for patient {data}."


class QuitCommand:
    """A command class that will exit the application."""

    def execute(self):
        sys.exit()
