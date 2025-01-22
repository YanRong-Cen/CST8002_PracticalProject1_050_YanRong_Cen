"""
Course: CST8002 - Programming Language
Professor: Todd Keuleman
Due Date: 2025-01-26
Author: YanRong Cen

Description:
This program processes a dataset of facilities, parses the records into objects,
stores them in a list, and outputs the details in a readable format. The program
includes exception handling, file input/output, and demonstrates the use of loops,
methods, and classes.
"""


class FacilityRecord:
    """
    Represents a record for a facility, containing details such as region, license number,
    type of facility, and maximum capacities for children of various age groups.
    """
    def __init__(self, region, district, license_number, facility_name, facility_type,
         facility_address_1, facility_address_2, facility_address_3,
         max_children, max_infants, max_preschool, max_school_age,
         language_of_service, operator_id, designated_facility):
        
        self.region = region
        self.district = district
        self.license_number = license_number
        self.facility_name = facility_name
        self.facility_type = facility_type
        self.facility_address_1 = facility_address_1
        self.facility_address_2 = facility_address_2
        self.facility_address_3 = facility_address_3
        self.max_children = max_children
        self.max_infants = max_infants
        self.max_preschool = max_preschool
        self.max_school_age = max_school_age
        self.language_of_service = language_of_service
        self.operator_id = operator_id
        self.designated_facility = designated_facility

def __str__(self):
    """
    Returns a string representation of the facility record.

    Returns:
        str: A formatted string containing all details of the facility record.
    """
    return (f"Region: {self.region}, District: {self.district}, License #: {self.license_number}, "
            f"Facility Name: {self.facility_name}, Type: {self.facility_type}, "
            f"Address: {self.facility_address_1}, {self.facility_address_2}, {self.facility_address_3}, "
            f"Max Children: {self.max_children}, Infants: {self.max_infants}, Preschool: {self.max_preschool}, "
            f"School Age: {self.max_school_age}, Language: {self.language_of_service}, "
            f"Operator ID: {self.operator_id}, Designated Facility: {self.designated_facility}")
