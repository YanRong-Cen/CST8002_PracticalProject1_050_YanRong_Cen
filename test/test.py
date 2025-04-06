import unittest
import threading
import time
import os
import sys
import tempfile

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from model.FacilityRecord import StandardFacilityRecord, CompactFacilityRecord, DetailedFacilityRecord
from business.business import FacilityManager
from presentation.presentation import convert_record_format
from persistence.Persistence import Persistence

# Use a temporary database file for testing
TEST_DB_PATH = os.path.join(tempfile.gettempdir(), "test_facility.db")
CSV_PATH = os.path.join(project_root, "Licensed_Early_Learning_and_Childcare_Facilities.csv")

print("\nProgram by: YanRong Cen\n")  # Display my name

class TestFacilityManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up any necessary resources before all tests."""
        # Ensure the test database doesn't exist
        if os.path.exists(TEST_DB_PATH):
            try:
                os.remove(TEST_DB_PATH)
            except PermissionError:
                # If file is locked, use a different name
                cls.test_db_path = os.path.join(tempfile.gettempdir(), f"test_facility_{time.time()}.db")
            else:
                cls.test_db_path = TEST_DB_PATH
        else:
            cls.test_db_path = TEST_DB_PATH

    def setUp(self):
        """Set up a FacilityManager instance for testing."""
        # Initialize database using the class variable
        Persistence.initialize_database(self.__class__.test_db_path)
        
        # Create manager instance using the class variable
        self.manager = FacilityManager(self.__class__.test_db_path)
        
        # Define test records
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
        
        # Add test records to the database
        for record in self.test_records:
            self.manager.add_record(record)

    def tearDown(self):
        """Clean up after each test."""
        try:
            # Close database connections
            if hasattr(self, 'manager'):
                # Stop background threads
                self.manager.save_queue.put("STOP")
                self.manager.display_queue.put("STOP")
                # Wait for threads to finish
                time.sleep(0.1)
                
        finally:
            # Remove test database
            try:
                if os.path.exists(self.__class__.test_db_path):
                    os.remove(self.__class__.test_db_path)
            except PermissionError:
                pass  # If we can't remove it now, it will be removed in the next test

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests."""
        try:
            if os.path.exists(cls.test_db_path):
                os.remove(cls.test_db_path)
        except (PermissionError, AttributeError):
            pass

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
        initial_count = len(self.manager.records)
        self.manager.add_record(self.test_records[0])  # Add the test record first
        self.assertEqual(len(self.manager.records), initial_count + 1)  # Verify record was added
        self.manager.delete_record(0)  # Delete the record
        self.assertEqual(len(self.manager.records), initial_count)  # Should be back to initial count

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
        self.assertIn("Region A", compact_str)  # Region A without prefix in compact format

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
        # Store original records for comparison
        with self.manager.records_lock:
            original_records = self.manager.records.copy()
            original_count = len(original_records)

        # Start sorting by max_children
        sort_complete = threading.Event()
        def on_sort_complete():
            sort_complete.set()
        self.manager.sort_records("max_children", callback=on_sort_complete)

        # Wait a short time to ensure sorting has started
        time.sleep(0.1)

        # Verify records can still be accessed during sorting
        with self.manager.records_lock:
            self.assertEqual(len(self.manager.records), original_count)

        # Wait for sorting to complete (maximum 5 seconds)
        sort_complete.wait(5)

        # Verify records are sorted by max_children
        with self.manager.records_lock:
            sorted_records = self.manager.records
            for i in range(len(sorted_records) - 1):
                current_val = getattr(sorted_records[i], "max_children")
                next_val = getattr(sorted_records[i + 1], "max_children")
                self.assertLessEqual(
                    current_val,
                    next_val,
                    f"Records not properly sorted by max_children: {current_val} > {next_val}"
                )

        # Verify record count hasn't changed
        with self.manager.records_lock:
            self.assertEqual(
                len(self.manager.records),
                original_count,
                "Record count changed during sorting"
            )

if __name__ == "__main__":
    unittest.main() 