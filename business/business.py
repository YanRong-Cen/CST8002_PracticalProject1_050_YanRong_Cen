"""
Course: CST8002 - Programming Language
Professor: Todd Keuleman
Due Date: 2025-02-16
Author: YanRong Cen

Description:
This module contains the FacilityManager class, which manages facility records.
It provides methods to load, save, display, add, and delete records.
"""
from persistence.Persistence import Persistence
from model.FacilityRecord import FacilityRecord 
class FacilityManager:
    """
    A class to manage facility records.

    Attributes:
        records (list): A list of FacilityRecord objects.
    """
    def __init__(self, file_path):
        """
        Initializes the FacilityManager and loads records from the specified CSV file.

        Args:
            file_path (str): The path to the CSV file containing facility records.
        """
        self.records = []
        self.load_records(file_path)

    def load_records(self, file_path, num_records=100):
        """
        Load records from a CSV file using the Persistence layer.

        Args:
            file_path (str): The path to the CSV file.
            num_records (int): The maximum number of records to load (default is 100).
        """
        """Load records from a CSV file using the Persistence layer."""
        self.records = Persistence.load_records(file_path, num_records)
    def save_records(self, file_path):
        """
        Save records to a CSV file using the Persistence layer.

        Args:
            file_path (str): The path to the CSV file where records will be saved.
        """
        """Save records to a CSV file using the Persistence layer."""
        Persistence.save_records(file_path, self.records)
    def display_records_with_name(self,records):
        """
        Display all facility records with your name every 10 records.

        Args:
            records (list): A list of FacilityRecord objects to display.
        """
        """Display all facility records with your name every 10 records."""
        for i, record in enumerate(records):
            print(record)
            if (i + 1) % 10 == 0:  # Print name every 10 records
                print("Program by YanRong Cen")

    def display_records(self):
        """
        Display all facility records.
        """
        """Display all facility records."""
        for record in self.records:
            print(record)
    def select_record(self, index):
        """
        Select and display a specific record by index.

        Args:
            index (int): The index of the record to display.
        """
        """Select and display a specific record by index."""
        if 0 <= index < len(self.records):
            print(self.records[index])
        else:
            print("Error: Index out of range.")
    def add_record(self, record):
        """
        Add a new record to the list.

        Args:
            record (FacilityRecord): The record to be added.
        """
        """Add a new record to the list."""
        self.records.append(record)
    def delete_record(self, index):
        """
        Delete a record by index.

        Args:
            index (int): The index of the record to delete.
        """
        """Delete a record by index."""
        if 0 <= index < len(self.records):
            del self.records[index]
        else:
            print("Error: Index out of range.") 

