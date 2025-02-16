from Persistence import Persistence
class FacilityManager:
    def __init__(self, file_path):
        self.records = []
        self.load_records(file_path)

    def load_records(self, file_path, num_records=100):
        """Load records from a CSV file using the Persistence layer."""
        self.records = Persistence.load_records(file_path, num_records)
    def save_records(self, file_path):
        """Save records to a CSV file using the Persistence layer."""
        Persistence.save_records(file_path, self.records)
    def display_records_with_name(self,records):
        """Display all facility records with your name every 10 records."""
        for i, record in enumerate(records):
            print(record)
            if (i + 1) % 10 == 0:  # Print name every 10 records
                print("Program by YanRong Cen")

    def display_records(self):
        """Display all facility records."""
        for record in self.records:
            print(record)
    def select_record(self, index):
        """Select and display a specific record by index."""
        if 0 <= index < len(self.records):
            print(self.records[index])
        else:
            print("Error: Index out of range.")

