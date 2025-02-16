import os
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
if __name__ == "__main__":
    main() 