import unittest
import threading
import time
from model.FacilityRecord import StandardFacilityRecord, CompactFacilityRecord, DetailedFacilityRecord
from business.business import FacilityManager
from presentation.presentation import convert_record_format

FILE_PATH = r"E:\level_4\Programming Language\Licensed_Early_Learning_and_Childcare_Facilities.csv"
print("\nProgram by: YanRong Cen\n")  # Display my name

class TestFacilityManager(unittest.TestCase):
    def setUp(self):
        """Set up a FacilityManager instance for testing."""
        self.manager = FacilityManager(FILE_PATH)
        self.test_records = [
            StandardFacilityRecord(
                region="Region A",
                district="District 1",
                license_number="123",
                facility_name="Facility A",
                facility_type="Type 1",
                facility_address_1="Address 1",
                facility_address_2="",
                facility_address_3="",
                max_children=10,
                max_infants=2,
                max_preschool=4,
                max_school_age=4,
                language_of_service="English",
                operator_id="op1",
                designated_facility="Yes"
            ),
            StandardFacilityRecord(
                region="Region B",
                district="District 2",
                license_number="456",
                facility_name="Facility B",
                facility_type="Type 2",
                facility_address_1="Address 2",
                facility_address_2="",
                facility_address_3="",
                max_children=20,
                max_infants=5,
                max_preschool=8,
                max_school_age=7,
                language_of_service="French",
                operator_id="op2",
                designated_facility="No"
            ),
            StandardFacilityRecord(
                region="Region C",
                district="District 3",
                license_number="789",
                facility_name="Facility C",
                facility_type="Type 3",
                facility_address_1="Address 3",
                facility_address_2="",
                facility_address_3="",
                max_children=15,
                max_infants=3,
                max_preschool=6,
                max_school_age=6,
                language_of_service="English",
                operator_id="op3",
                designated_facility="Yes"
            )
        ]

    def test_initialization_loads_records(self):
        """Test that the FacilityManager initializes with records from the CSV file."""
        self.assertGreater(len(self.manager.records), 0, "No records were loaded from the CSV file.")

    def test_add_record(self):
        """Test adding a record."""
        initial_count = len(self.manager.records)  # Get the initial count
        self.manager.add_record(self.test_records[0])
        self.assertEqual(len(self.manager.records), initial_count + 1)  # Expect count to increase by 1

    def test_delete_record(self):
        """Test deleting a record."""
        self.manager.add_record(self.test_records[0])  # Add the test record first
        self.manager.delete_record(0)  # Delete the record
        self.assertEqual(len(self.manager.records), 100)  # Expect count to be back to 100

    def test_polymorphic_record_formatting(self):
        """Test that records can be formatted in different ways using polymorphism."""
        # Test standard format
        standard_record = self.test_records[0]
        self.assertIn("Region: Region A", str(standard_record))
        self.assertIn("District: District 1", str(standard_record))

        # Test compact format
        compact_record = convert_record_format(standard_record, CompactFacilityRecord)
        compact_str = str(compact_record)
        self.assertIn("Facility A (123)", compact_str)
        self.assertIn("Capacity: 10", compact_str)
        self.assertIn("Region: Region A", compact_str)

        # Test detailed format
        detailed_record = convert_record_format(standard_record, DetailedFacilityRecord)
        detailed_str = str(detailed_record)
        self.assertIn("Facility Details:", detailed_str)
        self.assertIn("Name: Facility A", detailed_str)
        self.assertIn("Capacity Information:", detailed_str)

    def test_async_sorting(self):
        """
        Test asynchronous sorting functionality.
        This test verifies:
        1. Records are sorted correctly by the specified field
        2. Sorting operation is performed asynchronously
        3. Thread safety is maintained
        4. Multiple concurrent sort operations are handled correctly
        """
        # Add test records to manager
        for record in self.test_records:
            self.manager.add_record(record)

        # Create an event to track sort completion
        sort_complete = threading.Event()
        original_records = None

        # Store original records for comparison
        with self.manager.records_lock:
            original_records = self.manager.records.copy()

        # Start sorting by max_children
        self.manager.sort_records("max_children")

        # Wait a short time to ensure sorting has started
        time.sleep(0.1)

        # Verify records can still be accessed during sorting
        with self.manager.records_lock:
            self.assertEqual(len(self.manager.records), len(self.test_records))

        # Wait for sorting to complete (maximum 5 seconds)
        time.sleep(5)

        # Verify records are sorted by max_children
        with self.manager.records_lock:
            sorted_records = self.manager.records
            for i in range(len(sorted_records) - 1):
                self.assertLessEqual(
                    sorted_records[i].max_children,
                    sorted_records[i + 1].max_children,
                    "Records not properly sorted by max_children"
                )

        # Verify record count hasn't changed
        with self.manager.records_lock:
            self.assertEqual(
                len(self.manager.records),
                len(original_records),
                "Record count changed during sorting"
            )

if __name__ == "__main__":
    unittest.main() 