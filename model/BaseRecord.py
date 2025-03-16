"""
Course: CST8002 - Programming Language
Professor: Todd Keuleman
Due Date: 2025-02-16
Author: YanRong Cen

Description:
Base class for facility records that defines the common interface and functionality.
"""

class BaseRecord:
    def __init__(self, region, district, license_number, facility_name, facility_type,
                 facility_address_1, facility_address_2, facility_address_3,
                 max_children, max_infants, max_preschool, max_school_age,
                 language_of_service, operator_id, designated_facility, record_type=None):
        self.region = region
        self.district = district
        self.license_number = license_number
        self.facility_name = facility_name
        self.facility_type = facility_type
        self.facility_address_1 = facility_address_1
        self.facility_address_2 = facility_address_2
        self.facility_address_3 = facility_address_3
        self.max_children = int(max_children) if max_children else 0
        self.max_infants = int(max_infants) if max_infants else 0
        self.max_preschool = int(max_preschool) if max_preschool else 0
        self.max_school_age = int(max_school_age) if max_school_age else 0
        self.language_of_service = language_of_service
        self.operator_id = operator_id
        self.designated_facility = designated_facility
        self.record_type = record_type or self.__class__.__name__

    def format_record(self):
        """
        Abstract method that should be implemented by subclasses to format the record
        according to their specific requirements.
        """
        raise NotImplementedError("Subclasses must implement format_record()")

    def __str__(self):
        """
        Returns a string representation of the record using the format_record method.
        """
        return self.format_record() 