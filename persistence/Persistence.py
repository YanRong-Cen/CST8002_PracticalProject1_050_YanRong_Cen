"""
Course: CST8002 - Programming Language
Professor: Todd Keuleman
Due Date: 2025-02-16
Author: YanRong Cen

Description:
This module handles the loading and saving of facility records to and from a CSV file.
"""
import csv
from model.FacilityRecord import FacilityRecord
import sqlite3
from model.FacilityRecord import  (  # 使用绝对导入
    StandardFacilityRecord,
    CompactFacilityRecord,
    DetailedFacilityRecord
)
from contextlib import contextmanager
from queue import Queue
from collections import OrderedDict
from typing import Dict, List, Set
import bisect
import threading
from operator import attrgetter

class DatabasePool:
    def __init__(self, db_path, pool_size=5):
        self.db_path = db_path
        self.pool = Queue(maxsize=pool_size)
        for _ in range(pool_size):
            self.pool.put(sqlite3.connect(db_path))

    @contextmanager
    def get_connection(self):
        conn = self.pool.get()
        try:
            yield conn
        finally:
            self.pool.put(conn)

class Persistence:
    @staticmethod
    def initialize_database(db_path):
        """Create the database table if it doesn't exist."""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS FacilityRecords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                region TEXT,
                district TEXT,
                license_number TEXT,
                facility_name TEXT,
                facility_type TEXT,
                facility_address_1 TEXT,
                facility_address_2 TEXT,
                facility_address_3 TEXT,
                max_children INTEGER,
                max_infants INTEGER,
                max_preschool INTEGER,
                max_school_age INTEGER,
                language_of_service TEXT,
                operator_id TEXT,
                designated_facility TEXT,
                record_type TEXT  -- 标识记录格式类型
            )
        ''')
        conn.commit()
        conn.close()

    @staticmethod
    def load_records(db_path):
        """Load records from the database."""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM FacilityRecords")
        rows = cursor.fetchall()
        records = []
        for row in rows:
            record_data = {
                'region': row[1],
                'district': row[2],
                'license_number': row[3],
                'facility_name': row[4],
                'facility_type': row[5],
                'facility_address_1': row[6],
                'facility_address_2': row[7],
                'facility_address_3': row[8],
                'max_children': row[9],
                'max_infants': row[10],
                'max_preschool': row[11],
                'max_school_age': row[12],
                'language_of_service': row[13],
                'operator_id': row[14],
                'designated_facility': row[15],
                'record_type': row[16]
            }
            # 根据record_type创建对应子类实例
            if record_data['record_type'] == 'CompactFacilityRecord':
                record = CompactFacilityRecord(**record_data)
            elif record_data['record_type'] == 'DetailedFacilityRecord':
                record = DetailedFacilityRecord(**record_data)
            else:
                record = StandardFacilityRecord(**record_data)
            records.append(record)
        conn.close()
        return records

    @staticmethod
    def save_records(db_path, records):
        """Save records to the database."""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM FacilityRecords")  # 清空旧数据
        for record in records:
            record_type = record.__class__.__name__
            cursor.execute('''
                INSERT INTO FacilityRecords (
                    region, district, license_number, facility_name, facility_type,
                    facility_address_1, facility_address_2, facility_address_3,
                    max_children, max_infants, max_preschool, max_school_age,
                    language_of_service, operator_id, designated_facility, record_type
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                record.region, record.district, record.license_number, record.facility_name,
                record.facility_type, record.facility_address_1, record.facility_address_2,
                record.facility_address_3, record.max_children, record.max_infants,
                record.max_preschool, record.max_school_age, record.language_of_service,
                record.operator_id, record.designated_facility, record_type
            ))
        conn.commit()
        conn.close()

    @staticmethod
    def migrate_csv_to_db(csv_path, db_path):
        """迁移CSV数据到数据库（一次性操作）"""
        Persistence.initialize_database(db_path)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                cursor.execute('''
                    INSERT INTO FacilityRecords (
                        region, district, license_number, facility_name, facility_type,
                        facility_address_1, facility_address_2, facility_address_3,
                        max_children, max_infants, max_preschool, max_school_age,
                        language_of_service, operator_id, designated_facility, record_type
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'StandardFacilityRecord')
                ''', row)
        conn.commit()
        conn.close()

    @staticmethod
    def create_record(db_path, record):
        """创建单条记录"""
        conn = sqlite3.connect(db_path)
        try:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO FacilityRecords ... ''')
            conn.commit()
            return True
        except Exception as e:
            print(f"Error creating record: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def update_record(db_path, record_id, record):
        """更新单条记录"""
        conn = sqlite3.connect(db_path)
        try:
            cursor = conn.cursor()
            cursor.execute('''UPDATE FacilityRecords SET ... WHERE id = ?''')
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating record: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def delete_record(db_path, record_id):
        """删除单条记录"""
        conn = sqlite3.connect(db_path)
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM FacilityRecords WHERE id = ?', (record_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting record: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def batch_update(db_path, records):
        """批量更新记录，使用事务"""
        conn = sqlite3.connect(db_path)
        try:
            cursor = conn.cursor()
            cursor.execute("BEGIN TRANSACTION")
            for record in records:
                cursor.execute('''UPDATE ... ''')
            cursor.execute("COMMIT")
            return True
        except Exception as e:
            cursor.execute("ROLLBACK")
            print(f"Error in batch update: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def create_indexes(db_path):
        """创建索引以提高查询性能"""
        conn = sqlite3.connect(db_path)
        try:
            cursor = conn.cursor()
            cursor.execute('''CREATE INDEX IF NOT EXISTS idx_license_number 
                             ON FacilityRecords(license_number)''')
            cursor.execute('''CREATE INDEX IF NOT EXISTS idx_facility_name 
                             ON FacilityRecords(facility_name)''')
            conn.commit()
        finally:
            conn.close()

