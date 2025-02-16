import csv
from FacilityRecord import FacilityRecord

class Persistence:
    @staticmethod
    def load_records(file_path, num_records=100):
        """Load records from a CSV file."""
        records = []
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                for i, row in enumerate(reader):
                    if i >= num_records:  # Limit to the first few records
                        break
                    record = FacilityRecord(
                        region=row[0],
                        district=row[1],
                        license_number=row[2],
                        facility_name=row[3],
                        facility_type=row[4],
                        facility_address_1=row[5],
                        facility_address_2=row[6],
                        facility_address_3=row[7],
                        max_children=int(row[8]) if row[8].isdigit() else 0,
                        max_infants=int(row[9]) if row[9].isdigit() else 0,
                        max_preschool=int(row[10]) if row[10].isdigit() else 0,
                        max_school_age=int(row[11]) if row[11].isdigit() else 0,
                        language_of_service=row[12],
                        operator_id=row[13],
                        designated_facility=row[14]
                    )
                    records.append(record)
        except FileNotFoundError:
            print("Error: The file was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        return records