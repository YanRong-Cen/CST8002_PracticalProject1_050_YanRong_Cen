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

# 添加项目根目录到模块搜索路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from business.business import FacilityManager
from persistence.Persistence import Persistence
from model.FacilityRecord import StandardFacilityRecord, CompactFacilityRecord, DetailedFacilityRecord
import os
import uuid
from business.business import FacilityManager
from model.FacilityRecord import StandardFacilityRecord, CompactFacilityRecord, DetailedFacilityRecord

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
    print("10. Change data sturcture")
    print("11. Exit")

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
        choice = input("Select an option (1-11): ")

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
                # 首先检查索引是否有效并获取当前记录
                current_record = None
                with manager.records_lock:
                    if 0 <= index < len(manager.records):
                        current_record = manager.records[index]
                    else:
                        print("\nInvalid record index!")
                        continue

                if current_record:
                    print(f"\nCurrent record:\n{current_record}")
                    print("\nEnter new details:")
                    updated_record = get_record_input(current_format)
                    if manager.edit_record(index, updated_record):
                        print("\nRecord updated successfully!")
                    else:
                        print("\nFailed to update record!")
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
            print("\nExiting program...")
            break

if __name__ == "__main__":
    main()