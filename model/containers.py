"""
Course: CST8002 - Programming Language
Professor: Todd Keuleman
Due Date: 2025-02-17
Author: YanRong Cen

Description:
This module provides different data structure implementations for storing facility records.
"""
from collections import OrderedDict
from typing import Dict, List, Set

class FacilityContainer:
    """可切换的数据结构容器"""
    def __init__(self, container_type="list"):
        self.container_type = container_type
        self.reset_container()
        
    def reset_container(self):
        if self.container_type == "list":
            self._container = []
        elif self.container_type == "ordered_dict":
            self._container = OrderedDict()
        elif self.container_type == "set":
            self._container = set()
        else:
            raise ValueError(f"Unsupported container type: {self.container_type}")
            
    def add(self, record):
        if self.container_type == "list":
            self._container.append(record)
        elif self.container_type == "ordered_dict":
            self._container[record.license_number] = record
        elif self.container_type == "set":
            self._container.add(record)
            
    def remove(self, record):
        if self.container_type == "list":
            self._container.remove(record)
        elif self.container_type == "ordered_dict":
            del self._container[record.license_number]
        elif self.container_type == "set":
            self._container.remove(record)
            
    def get_all(self) -> List:
        if self.container_type == "list":
            return self._container
        elif self.container_type == "ordered_dict":
            return list(self._container.values())
        elif self.container_type == "set":
            return list(self._container)