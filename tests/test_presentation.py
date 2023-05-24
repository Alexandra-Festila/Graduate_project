from unittest import TestCase
from unittest.mock import patch

from src.presentation import get_new_records


class PresentationTest(TestCase):
    def test_get_new_records(self):
        with patch("builtins.input", side_effect=["mock_patient_id", "mock_heart_rate","mock_blood_pressure",
                "mock_respiratory_rate", "mock_oxygen_saturation", "mock_temperature"]):
            result = get_new_records()
            self.assertEqual(
                result,
                {
                    "patient_id": "mock_patient_id",
                    "heart_rate": "mock_heart_rate",
                    "blood_pressure": "mock_blood_pressure",
                    "respiratory_rate": "mock_respiratory_rate",
                    "oxygen_saturation": "mock_oxygen_saturation",
                    "temperature": "mock_temperature",
                }
            )