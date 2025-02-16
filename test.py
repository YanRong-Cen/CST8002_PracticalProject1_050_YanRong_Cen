import unittest
from business import FacilityManager
from FacilityRecord import FacilityRecord
from presentation import main
FILE_PATH = r"E:\level_4\Programming Language\Licensed_Early_Learning_and_Childcare_Facilities.csv"
class TestFacilityManager(unittest.TestCase):
    def setUp(self):
        """Set up a FacilityManager instance for testing."""
        self.manager = FacilityManager(FILE_PATH)
        self.test_record = FacilityRecord(
            region="Test Region",
            district="Test District",
            license_number="12345",
            facility_name="Test Facility",
            facility_type="Childcare",
            facility_address_1="123 Test St",
            facility_address_2="Suite 100",
            facility_address_3="Test City",
            max_children=10,
            max_infants=5,
            max_preschool=3,
            max_school_age=2,
            language_of_service="English",
            operator_id="op123",
            designated_facility="Yes"
        )

    def test_initialization_loads_records(self):
        """Test that the FacilityManager initializes with records from the CSV file."""
        self.assertGreater(len(self.manager.records), 0, "No records were loaded from the CSV file.")

    def test_add_record(self):
        """Test adding a record."""
        initial_count = len(self.manager.records)  # Get the initial count
        self.manager.add_record(self.test_record)
        self.assertEqual(len(self.manager.records), initial_count + 1)  # Expect count to increase by 1

    def test_delete_record(self):
        """Test deleting a record."""
        self.manager.add_record(self.test_record)  # Add the test record first
        self.manager.delete_record(0)  # Delete the record
        self.assertEqual(len(self.manager.records), 100)  # Expect count to be back to 100

    def test_load_records(self):
        """Test loading records from a CSV file."""
        # Note: This test assumes a valid CSV file is present at the specified path.
        # You may want to mock file reading in a real test environment.
        # For demonstration, we will not implement this test fully.
        pass

if __name__ == "__main__":
    unittest.main() 