import sys

import typing as t

from datetime import datetime

print("Before import statement")  # Add this line before the import statement

from src.database import DatabaseManager

print("After import statement")  # Add this line after the import statement

db = DatabaseManager("patient_monitoring.db")

class Command(t.Protocol):
    def execute(self):
        pass

class CreateVitalSignsTableCommand:
    def execute(self, db: DatabaseManager):
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

class AddVitalsCommand:
    """ A command class the adds a vitals record for a specific patient"""

    def execute(self, patient: int, data: t.Dict[str, t.Union[str, int, float]]) -> str:
        "The actual execution of the command."

        date = datetime.utcnow().isoformat()
        data.setdefault("date", date)
        patient_id = data["patient_id"]

        db.add_record(table_name="vitals", data=data)

        return f"Vital signs successfully recorded for patient {patient_id}."


class ListRecordsCommand:
    """A command class that lists vitals records based on specific criteria."""

    def __init__(self, order_by: str = "date_added"):
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

    def execute (self, data: int):
        result = db.select_record(table_name="vitals", criteria={"patient_id": data}).fetchone()
        return result


class DeleteRecordCommand:
        """A command class that deletes a record from the SQL table"""
        
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
