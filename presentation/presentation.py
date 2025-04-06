"""
Course: CST8002 - Programming Language
Professor: Todd Keuleman
Due Date: 2025-02-16
Author: YanRong Cen

Description:

This module handles the user interface for the facility management system.
It provides functions to display menus, get user input, and manage facility records.
"""
import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from business.business import FacilityManager
from persistence.Persistence import Persistence
from model.FacilityRecord import StandardFacilityRecord, CompactFacilityRecord, DetailedFacilityRecord
import os
import uuid
from business.business import FacilityManager
from model.FacilityRecord import StandardFacilityRecord, CompactFacilityRecord, DetailedFacilityRecord
from presentation.visualization import FacilityVisualizer

def convert_record_format(record, target_format):
    """
    Convert a record from one format to another.
    
    Args:
        record: The source record to convert
        target_format: The target record class (Standard, Compact, or Detailed)
    
    Returns:
        A new record of the target format type
    """
    # 如果记录已经是目标格式，直接返回
    if isinstance(record, target_format):
        return record
        
    # 创建新的目标格式记录
    return target_format(
        region=record.region,
        district=record.district,
        license_number=record.license_number,
        facility_name=record.facility_name,
        facility_type=record.facility_type,
        facility_address_1=record.facility_address_1,
        facility_address_2=record.facility_address_2,
        facility_address_3=record.facility_address_3,
        max_children=record.max_children,
        max_infants=record.max_infants,
        max_preschool=record.max_preschool,
        max_school_age=record.max_school_age,
        language_of_service=record.language_of_service,
        operator_id=record.operator_id,
        designated_facility=record.designated_facility
    )

def display_menu():
    print("\nMenu:")
    print("1. Display all records")
    print("2. Select a record to display")
    print("3. Add a new record")
    print("4. Edit a record")
    print("5. Delete a record")
    print("6. Reload records from database")
    print("7. Save records to database")
    print("8. Change record format")
    print("9. Sort records")
    print("10. Change data structure")
    print("11. Create visualization")
    print("12. Exit")

def get_record_input(record_class=StandardFacilityRecord):
    """获取用户输入并创建记录"""
    data = {
        'region': input("Enter region: "),
        'district': input("Enter district: "),
        'license_number': input("Enter license number: "),
        'facility_name': input("Enter facility name: "),
        'facility_type': input("Enter facility type: "),
        'facility_address_1': input("Enter address line 1: "),
        'facility_address_2': input("Enter address line 2: "),
        'facility_address_3': input("Enter address line 3: "),
        'max_children': int(input("Enter max children: ")),
        'max_infants': int(input("Enter max infants: ")),
        'max_preschool': int(input("Enter max preschool: ")),
        'max_school_age': int(input("Enter max school age: ")),
        'language_of_service': input("Enter language of service: "),
        'operator_id': input("Enter operator ID: "),
        'designated_facility': input("Enter designated facility: ")
    }
    return record_class(**data)

def display_columns_for_edit(record):
    """Display all columns of a record and allow selection for editing."""
    print("\nAvailable columns for editing:")
    columns = [
        "region", "district", "license_number", "facility_name", "facility_type",
        "facility_address_1", "facility_address_2", "facility_address_3",
        "max_children", "max_infants", "max_preschool", "max_school_age",
        "language_of_service", "operator_id", "designated_facility"
    ]
    
    for i, column in enumerate(columns, 1):
        current_value = getattr(record, column)
        print(f"{i}. {column}: {current_value}")
    
    return columns

def get_column_input(column_name, current_value):
    """Get input for a specific column."""
    if column_name.startswith("max_"):
        while True:
            try:
                value = int(input(f"Enter new value for {column_name} (current: {current_value}): "))
                if value >= 0:
                    return value
                print("Please enter a non-negative number.")
            except ValueError:
                print("Please enter a valid number.")
    else:
        return input(f"Enter new value for {column_name} (current: {current_value}): ")

def edit_record_interactive(manager, index, current_format):
    """Interactive record editing with column selection."""
    try:
        # First check if index is valid and get current record
        current_record = None
        with manager.records_lock:
            if 0 <= index < len(manager.records):
                current_record = manager.records[index]
            else:
                print("\nInvalid record index!")
                return

        if current_record:
            print(f"\nCurrent record:\n{current_record}")
            
            while True:
                # Display columns and get selection
                columns = display_columns_for_edit(current_record)
                print("\nOptions:")
                print("1. Edit a column")
                print("2. Save changes")
                print("3. Cancel editing")
                
                choice = input("\nSelect an option (1-3): ")
                
                if choice == "1":
                    try:
                        col_index = int(input("Enter column number to edit: ")) - 1
                        if 0 <= col_index < len(columns):
                            column_name = columns[col_index]
                            current_value = getattr(current_record, column_name)
                            new_value = get_column_input(column_name, current_value)
                            setattr(current_record, column_name, new_value)
                            print(f"\n{column_name} updated successfully!")
                        else:
                            print("\nInvalid column number!")
                    except ValueError:
                        print("\nPlease enter a valid number!")
                
                elif choice == "2":
                    if manager.edit_record(index, current_record):
                        print("\nRecord updated successfully!")
                    else:
                        print("\nFailed to update record!")
                    break
                
                elif choice == "3":
                    print("\nEditing cancelled.")
                    break
                
                else:
                    print("\nInvalid option!")
    
    except ValueError:
        print("\nPlease enter a valid number!")

def create_visualization(manager):
    """Handle visualization creation."""
    if not manager.wait_for_load(timeout=10):
        print("\nError: Unable to create visualization - data loading timeout")
        return

    with manager.records_lock:
        available_fields = FacilityVisualizer.get_available_fields(manager.records)
        if not available_fields:
            print("\nNo fields available for visualization!")
            return

        print("\nAvailable fields for visualization:")
        print("-----------------------------------")
        field_descriptions = {
            "region": "Geographic region of the facility",
            "district": "School district where the facility is located",
            "license_number": "Unique license identifier",
            "facility_name": "Name of the facility",
            "facility_type": "Type of childcare facility",
            "facility_address_1": "Primary address line",
            "facility_address_2": "Secondary address line",
            "facility_address_3": "Additional address information",
            "max_children": "Maximum total children capacity",
            "max_infants": "Maximum infant capacity",
            "max_preschool": "Maximum preschool capacity",
            "max_school_age": "Maximum school-age capacity",
            "language_of_service": "Primary language of service",
            "operator_id": "Unique operator identifier",
            "designated_facility": "Designated facility information"
        }
        
        for i, field in enumerate(available_fields, 1):
            description = field_descriptions.get(field, "No description available")
            print(f"{i}. {field.replace('_', ' ').title()}")
            print(f"   Description: {description}")
            print("-----------------------------------")

        print("\nChart types:")
        print("1. Horizontal Bar Chart - Best for comparing many categories")
        print("2. Vertical Bar Chart - Good for showing trends over time")
        print("3. Pie Chart - Ideal for showing proportions of a whole")

        try:
            field_choice = int(input("\nSelect field number to visualize: ")) - 1
            chart_choice = input("Select chart type (1-3): ")

            if 0 <= field_choice < len(available_fields):
                field = available_fields[field_choice]
                title = f"Distribution of {field.replace('_', ' ').title()}"


                if chart_choice == "1":
                    FacilityVisualizer.create_horizontal_bar_chart(manager.records, field, title)
                elif chart_choice == "2":
                    FacilityVisualizer.create_vertical_bar_chart(manager.records, field, title)
                elif chart_choice == "3":
                    FacilityVisualizer.create_pie_chart(manager.records, field, title)
                else:
                    print("\nInvalid chart type!")
            else:
                print("\nInvalid field number!")
        except ValueError:
            print("\nInvalid input. Please enter a number!")

def main():
    DB_PATH = "facility_records.db"
    CSV_PATH = r"E:\level_4\Programming Language\Licensed_Early_Learning_and_Childcare_Facilities.csv"
    
    # 首次运行迁移数据
    if not os.path.exists(DB_PATH):
        Persistence.migrate_csv_to_db(CSV_PATH, DB_PATH)
    
    manager = FacilityManager(DB_PATH)
    current_format = StandardFacilityRecord
    
    print("\nProgram by: YanRong Cen\n")
    
    while True:
        display_menu()
        choice = input("Select an option (1-12): ")

        if choice == '1':
             # 清屏（可选）
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\nDisplaying records...")
            manager.display_records_with_name()
            input("\nPress Enter to return to menu...")
        elif choice == '2':
            try:
                index = int(input("Enter record index to display: "))
                # 获取记录的副本以避免长时间持有锁
                with manager.records_lock:
                    if 0 <= index < len(manager.records):
                        record = manager.records[index]
                        print(f"\nRecord details:\n{record}")
                    else:
                        print("\nInvalid record index!")
            except ValueError:
                print("\nPlease enter a valid number!")
        elif choice == '3':
            new_record = get_record_input(current_format)
            manager.add_record(new_record)
        elif choice == '4':
            try:
                index = int(input("Enter record index to edit: "))
                edit_record_interactive(manager, index, current_format)
            except ValueError:
                print("\nPlease enter a valid number!")
        elif choice == '5':
            try:
                index = int(input("Enter record index to delete: "))
                if manager.delete_record(index):
                    print("\nRecord deleted successfully!")
                else:
                    print("\nFailed to delete record!")
            except ValueError:
                print("\nPlease enter a valid number!")
        elif choice == '8':
            print("\n1. Standard\n2. Compact\n3. Detailed")
            fmt_choice = input("Select format: ")
            if fmt_choice == '1':
                current_format = StandardFacilityRecord
            elif fmt_choice == '2':
                current_format = CompactFacilityRecord
            elif fmt_choice == '3':
                current_format = DetailedFacilityRecord
            else:
                print("\nInvalid format choice!")
                continue

            # 转换现有记录格式
            with manager.records_lock:
                records = [convert_record_format(r, current_format) for r in manager.records]
                manager.records = records
                if manager.save_records():
                    print("\nRecord format changed successfully!")
                else:
                    print("\nFailed to change record format!")
        elif choice == '9':
            # 显示可排序的字段
            sortable_fields = manager.get_sortable_fields()
            if not sortable_fields:
                print("\nNo fields available for sorting!")
                continue

            print("\nAvailable fields for sorting:")
            for i, field in enumerate(sortable_fields, 1):
                print(f"{i}. {field}")
            

            print("\nSort algorithms:")
            print("1. Quick sort")
            print("2. Merge sort")
            print("3. Built-in sort")
            try:
                field_choice = int(input("\nSelect field number to sort by: ")) - 1
                algo_choice = input("Select sorting algorithm (1-3): ")

                if 0 <= field_choice < len(sortable_fields):
                    algorithm ={
                        "1": "quick",
                        "2": "merge",
                        "3": "builtin"

                    }.get(algo_choice, "quick")
                    manager.sort_records(sortable_fields[field_choice],algorithm)
                    print("\nSort operation started in background...")
                else:
                        print("\nInvalid field number!")
               
            except ValueError:
                print("\nInvalid input. Please enter a number!")
        elif choice == '10':
            print("\nAvailable data structures:")
            print("1. List")
            print("2. OrderedDict")
            print("3. Set")
            struct_choice = input("Select data structure: ")
            
            structure_type = {
                "1": "list",
                "2": "ordered_dict",
                "3": "set"
            }.get(struct_choice)
            
            if structure_type:
                manager.change_container_type(structure_type)
                print(f"\nData structure changed to {structure_type}")
            else:
                print("\nInvalid choice!")
        elif choice == '11':
            create_visualization(manager)
        elif choice == '12':
            print("\nExiting program...")
            break

if __name__ == "__main__":
    main()