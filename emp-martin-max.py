"""
    name : martin stordeur && maxime kapczuk 
    date : 2023-10-05
    description : Application de lecture d'empreintes digitales utilisant PyQt5 et pyfingerprint.
"""


import unittest
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication
from emp_martin_max import FingerprintScannerApp

# filepath: test_emp-martin-max.py

class TestFingerprintScannerApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])  # Required for PyQt5 tests

    def setUp(self):
        self.window = FingerprintScannerApp()

    @patch("emp_martin_max.PyFingerprint")
    def test_start_scan(self, mock_pyfingerprint):
        # Mock PyFingerprint behavior
        mock_instance = mock_pyfingerprint.return_value
        mock_instance.verifyPassword.return_value = True
        mock_instance.readImage.return_value = True
        mock_instance.searchTemplate.return_value = (-1, 0)

        # Simulate button click to start scan
        self.window.start_scan()

        # Verify UI updates
        self.assertEqual(self.window.status_label.text(), "Scan en cours")
        self.assertFalse(self.window.scan_button.isEnabled())

    @patch("emp_martin_max.PyFingerprint")
    def test_scan_fingerprint_no_match(self, mock_pyfingerprint):
        # Mock PyFingerprint behavior for no match
        mock_instance = mock_pyfingerprint.return_value
        mock_instance.verifyPassword.return_value = True
        mock_instance.readImage.return_value = True
        mock_instance.searchTemplate.return_value = (-1, 0)

        # Call scan_fingerprint directly
        self.window.scan_fingerprint()

        # Verify UI updates for no match
        self.assertEqual(self.window.status_label.text(), "Aucune correspondance trouvée.")
        self.assertEqual(self.window.status_label.styleSheet(), "font-size: 16px; color: red;")

    @patch("emp_martin_max.PyFingerprint")
    def test_scan_fingerprint_match_found(self, mock_pyfingerprint):
        # Mock PyFingerprint behavior for a match
        mock_instance = mock_pyfingerprint.return_value
        mock_instance.verifyPassword.return_value = True
        mock_instance.readImage.return_value = True
        mock_instance.searchTemplate.return_value = (5, 80)
        mock_instance.downloadTemplate.return_value = b"mock_fingerprint_data"

        # Call scan_fingerprint directly
        self.window.scan_fingerprint()

        # Verify UI updates for a match
        self.assertEqual(self.window.status_label.text(), "Empreinte trouvée (Position #5)")
        self.assertEqual(self.window.status_label.styleSheet(), "font-size: 16px; color: green;")

    @patch("emp_martin_max.PyFingerprint")
    def test_scan_fingerprint_error(self, mock_pyfingerprint):
        # Mock PyFingerprint to raise an exception
        mock_instance = mock_pyfingerprint.return_value
        mock_instance.verifyPassword.side_effect = Exception("Mocked error")

        # Call scan_fingerprint directly
        self.window.scan_fingerprint()

        # Verify UI updates for an error
        self.assertTrue("Erreur: Mocked error" in self.window.status_label.text())
        self.assertEqual(self.window.status_label.styleSheet(), "font-size: 16px; color: red;")

if __name__ == "__main__":
    unittest.main()