import os
import uuid
from business import FacilityManager
from FacilityRecord import FacilityRecord

def display_menu():
    """Display the main menu options."""
    print("\nMenu:")
    print("1. Display all records")
    print("2. Select a record to display")
    print("3. Add a new record")
    print("4. Edit a record")
    print("5. Delete a record")
    print("6. Reload records from CSV")
    print("7. Save records to CSV")
    print("8. Exit")
    
def main():
    FILE_PATH = r"E:\level_4\Programming Language\Licensed_Early_Learning_and_Childcare_Facilities.csv"  
    facility_manager = FacilityManager(FILE_PATH)
    
    if not os.path.exists(FILE_PATH):
        print(f"Error: The file '{FILE_PATH}' does not exist.")
        return

    print("\nProgram by: YanRong Cen\n")  # Display my name
    facility_manager.load_records(FILE_PATH)
    
    while True:
        display_menu()
        choice = input("Select an option (1-8): ")

        if choice == '1':
            facility_manager.display_records_with_name(facility_manager.records)
        elif choice == '2':
            index = int(input("Enter the index of the record to display: "))
            facility_manager.select_record(index)
        elif choice == '3':
            new_record = get_record_input()
            facility_manager.add_record(new_record)
            print("Record added successfully.")
        elif choice == '4':
            index = int(input("Enter the index of the record to edit: "))
            if 0 <= index < len(facility_manager.records):
                print("Editing record at index:", index)
                updated_record = get_record_input()
                facility_manager.records[index] = updated_record
                print("Record updated successfully.")
            else:
                print("Error: Index out of range.")
        elif choice == '5':
            index = int(input("Enter the index of the record to delete: "))
            facility_manager.delete_record(index)
            print("Record deleted successfully.")
            
        elif choice == '6':
            facility_manager.load_records(FILE_PATH)
            print("Records reloaded successfully.")
        elif choice == '7':
            output_file_path = f"output_{uuid.uuid4()}.csv"
            facility_manager.g(output_file_path)
            print(f"Records saved to {output_file_path}")
        elif choice == '8':
            print("Exiting the program.")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main() 
def get_record_input():
    """Get facility record details from user input with validation."""
    while True:
        try:
            region = input("Enter region: ")
            district = input("Enter district: ")
            license_number = input("Enter license number: ")
            facility_name = input("Enter facility name: ")
            facility_type = input("Enter facility type: ")
            facility_address_1 = input("Enter address line 1: ")
            facility_address_2 = input("Enter address line 2: ")
            facility_address_3 = input("Enter address line 3: ")
            max_children = int(input("Enter max children: "))
            max_infants = int(input("Enter max infants: "))
            max_preschool = int(input("Enter max preschool: "))
            max_school_age = int(input("Enter max school age: "))
            language_of_service = input("Enter language of service: ")
            operator_id = input("Enter operator ID: ")
            designated_facility = input("Enter designated facility: ")

            return FacilityRecord(region, district, license_number, facility_name, facility_type,
                                  facility_address_1, facility_address_2, facility_address_3,
                                  max_children, max_infants, max_preschool, max_school_age,
                                  language_of_service, operator_id, designated_facility)
        except ValueError:
            print("Invalid input. Please enter numeric values for max children, infants, preschool, and school age.")