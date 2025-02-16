"""
Course: CST8002 - Programming Language
Professor: Todd Keuleman
Due Date: 2025-02-16
Author: YanRong Cen

Description:
This module handles the loading and saving of facility records to and from a CSV file.
"""
import csv
from FacilityRecord import FacilityRecord

class Persistence:
    """
    A class to handle the persistence of facility records.

    Methods:
        load_records(file_path, num_records): Load records from a CSV file.
        save_records(file_path, records): Save records to a CSV file.
    """
    @staticmethod
    def load_records(file_path, num_records=100):
        """
        Load records from a CSV file.

        Args:
            file_path (str): The path to the CSV file.
            num_records (int): The maximum number of records to load (default is 100).

        Returns:
            list: A list of FacilityRecord objects.
        """
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
    @staticmethod
    def save_records(file_path, records):
        """
        Save records to a CSV file.

        Args:
            file_path (str): The path to the CSV file where records will be saved.
            records (list): A list of FacilityRecord objects to save.
        """
        """Save records to a CSV file."""
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # Write header
                writer.writerow(['Region', 'District', 'License Number', 'Facility Name', 
                                 'Facility Type', 'Address 1', 'Address 2', 'Address 3', 
                                 'Max Children', 'Max Infants', 'Max Preschool', 
                                 'Max School Age', 'Language of Service', 'Operator ID', 
                                 'Designated Facility'])
                for record in records:
                    writer.writerow([record.region, record.district, record.license_number,
                                     record.facility_name, record.facility_type,
                                     record.facility_address_1, record.facility_address_2,
                                     record.facility_address_3, record.max_children,
                                     record.max_infants, record.max_preschool,
                                     record.max_school_age, record.language_of_service,
                                     record.operator_id, record.designated_facility])
        except Exception as e:
            print(f"An error occurred while saving records: {e}") 

            