"""
Course: CST8002 - Programming Language
Professor: Todd Keuleman
Due Date: 2025-02-16
Author: YanRong Cen

Description:
This module contains the FacilityManager class, which manages facility records.
It provides methods to load, save, display, add, and delete records.
"""
from persistence.Persistence import Persistence
from model.FacilityRecord import FacilityRecord 
from operator import attrgetter
import threading
import queue
import time
from model.containers import FacilityContainer
from business.sorting import SortingStrategy

class FacilityManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.container = FacilityContainer("list")  # 默认使用列表
        self.records = []
        self.records_lock = threading.Lock()  # 保护记录访问的线程锁
        self.load_complete = threading.Event()  # 标记数据加载完成的事件
        self.save_queue = queue.Queue()  # 保存操作队列
        self.display_queue = queue.Queue()  # 显示操作队列
        
        # 启动后台保存线程
        self.save_thread = threading.Thread(target=self._save_worker, name="SaveThread")
        self.save_thread.daemon = True
        self.save_thread.start()
        
        # 启动后台显示线程
        self.display_thread = threading.Thread(target=self._display_worker, name="DisplayThread")
        self.display_thread.daemon = True
        self.display_thread.start()
        
        Persistence.initialize_database(db_path)
        self.load_records_async()  # 异步加载记录

    def _save_worker(self):
        """后台保存工作线程"""
        while True:
            try:
                # 等待保存请求
                save_request = self.save_queue.get(timeout=1)
                if save_request == "STOP":
                    break
                
                # 执行保存操作
                with self.records_lock:
                    Persistence.save_records(self.db_path, self.records)
                print("\nRecords saved in background.")
                
                self.save_queue.task_done()
            except queue.Empty:
                continue  # 超时后继续等待
            except Exception as e:
                print(f"\nError saving records: {e}")

    def _display_worker(self):
        """后台显示工作线程"""
        while True:
            try:
                # 等待显示请求
                display_request = self.display_queue.get(timeout=1)
                if display_request == "STOP":
                    break
                
                # 获取记录副本
                with self.records_lock:
                    records_copy = list(enumerate(self.records))
                
                # 显示记录
                for i, record in records_copy:
                    print(f"\n[{i}] {record}")
                    if (i + 1) % 10 == 0:
                        user_input = input("\nPress Enter to continue (or 'q' to quit): ")
                        if user_input.lower() == 'q':
                            break
                
                self.display_queue.task_done()
            except queue.Empty:
                continue  # 超时后继续等待
            except Exception as e:
                print(f"\nError displaying records: {e}")

    def load_records_async(self):
        """异步从数据库加载记录"""
        def load_worker():
            try:
                loaded_records = Persistence.load_records(self.db_path)
                with self.records_lock:
                    self.records = loaded_records
                print("\nRecords loaded successfully!")
            finally:
                self.load_complete.set()  # 确保在任何情况下都标记加载完成

        # 创建并启动加载线程
        load_thread = threading.Thread(target=load_worker, name="LoadThread")
        load_thread.daemon = True
        load_thread.start()

    def wait_for_load(self, timeout=None):
        """等待数据加载完成
        
        Args:
            timeout (float, optional): 超时时间（秒）
        
        Returns:
            bool: 是否成功加载
        """
        if not self.load_complete.is_set():
            print("\nWaiting for records to load...")
            return self.load_complete.wait(timeout)
        return True

    def save_records(self):
        """异步保存记录到数据库"""
        if not self.wait_for_load(timeout=10):
            print("\nError: Unable to save - data loading timeout")
            return False
            
        # 将保存请求添加到队列
        self.save_queue.put("SAVE")
        return True

    def add_record(self, record):
        """添加记录"""
        if not self.wait_for_load(timeout=10):
            print("\nError: Unable to add record - data loading timeout")
            return False
            
        with self.records_lock:
            self.records.append(record)
            # 触发异步保存
            self.save_queue.put("SAVE")
        print("\nRecord added successfully!")
        return True

    def delete_record(self, index):
        """删除记录"""
        if not self.wait_for_load(timeout=10):
            print("\nError: Unable to delete record - data loading timeout")
            return False
            
        with self.records_lock:
            if 0 <= index < len(self.records):
                del self.records[index]
                # 触发异步保存
                self.save_queue.put("SAVE")
                print("\nRecord deleted successfully!")
                return True
            else:
                print("\nInvalid record index!")
                return False

    def edit_record(self, index, updated_record):
        """编辑记录"""
        if not self.wait_for_load(timeout=10):
            print("\nError: Unable to edit record - data loading timeout")
            return False
            
        with self.records_lock:
            if 0 <= index < len(self.records):
                self.records[index] = updated_record
                # 触发异步保存
                self.save_queue.put("SAVE")
                print("\nRecord updated successfully!")
                return True
            else:
                print("\nInvalid record index!")
                return False

    def display_records_with_name(self):
        """异步显示记录"""
        if not self.wait_for_load(timeout=10):
            print("\nError: Unable to display records - data loading timeout")
            return False

        # 创建显示完成事件
        display_complete = threading.Event()

        def display_worker():
            try:
                with self.records_lock:
                    records_copy = list(enumerate(self.records))
            
                for i, record in records_copy:
                    print(f"\n[{i}] {record}")
                    if (i + 1) % 10 == 0:
                        user_input = input("\nPress Enter to continue (or 'q' to quit): ")
                        if user_input.lower() == 'q':
                            break
            finally:
                display_complete.set()  # 标记显示完成

        # 创建并启动显示线程
        display_thread = threading.Thread(target=display_worker, name="DisplayThread")
        display_thread.daemon = True
        display_thread.start()
        
        # 等待显示完成
        display_complete.wait()
        return True

    def get_sortable_fields(self):
        """
        获取可排序的字段列表
        
        Returns:
            list: 可排序字段的列表
        """
        if not self.wait_for_load(timeout=10):
            print("\nError: Unable to get fields - data loading timeout")
            return []
            
        with self.records_lock:
            if not self.records:
                return []
            return [attr for attr in vars(self.records[0]).keys() 
                    if not attr.startswith('_')]

    def __del__(self):
        """清理资源"""
        # 停止后台线程
        self.save_queue.put("STOP")
        self.display_queue.put("STOP")

    def change_container_type(self, container_type: str):
        """切换数据结构类型"""
        with self.records_lock:
            records = self.container.get_all()
            self.container = FacilityContainer(container_type)
            for record in records:
                self.container.add(record)

    def sort_records(self, field: str, algorithm: str = "quick", callback=None):
        """
        异步对记录进行排序
        
        Args:
            field (str): 要排序的字段名称
            algorithm (str): 排序算法 ("quick", "merge", "builtin")
            callback: Optional callback to be called when sorting is complete
        """
        if not self.wait_for_load(timeout=10):
            print("\nError: Unable to sort records - data loading timeout")
            return False
        
        def sort_worker():
            try:
                with self.records_lock:
                    # Get all records from the container
                    records = self.records.copy()
                    
                    # Sort the records using the specified algorithm
                    if algorithm == "quick":
                        sorted_records = SortingStrategy.quick_sort(records, field)
                    elif algorithm == "merge":
                        sorted_records = SortingStrategy.merge_sort(records, field)
                    else:
                        sorted_records = sorted(records, key=attrgetter(field))
                    
                    # Update both the container and the records list
                    self.records = sorted_records
                    self.container = FacilityContainer(self.container.container_type)
                    for record in sorted_records:
                        self.container.add(record)
                    
                    # Trigger async save
                    self.save_queue.put("SAVE")
                    
                print(f"\nRecords sorted by {field} using {algorithm} sort")
                if callback:
                    callback()
            except AttributeError as e:
                print(f"\nError: Invalid field name '{field}' - {e}")
            except Exception as e:
                print(f"\nError during sorting: {e}")

        # Create and start sorting thread
        sort_thread = threading.Thread(target=sort_worker, name="SortThread")
        sort_thread.daemon = True
        sort_thread.start()
        return True