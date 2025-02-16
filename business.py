from Persistence import Persistence
class FacilityManager:
    def __init__(self, file_path):
        self.records = []
        self.load_records(file_path)

    def load_records(self, file_path, num_records=100):
        """Load records from a CSV file using the Persistence layer."""
        self.records = Persistence.load_records(file_path, num_records)
