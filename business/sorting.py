"""
Course: CST8002 - Programming Language
Professor: Todd Keuleman
Due Date: 2025-02-16
Author: YanRong Cen

Description:
This module provides different sorting algorithms for facility records.
"""
from typing import List

class SortingStrategy:
    @staticmethod
    def quick_sort(records: List, field: str) -> List:
        if len(records) <= 1:
            return records
        pivot = records[len(records)//2]
        pivot_val = getattr(pivot, field)
        left = [x for x in records if getattr(x, field) < pivot_val]
        middle = [x for x in records if getattr(x, field) == pivot_val]
        right = [x for x in records if getattr(x, field) > pivot_val]
        return SortingStrategy.quick_sort(left, field) + middle + SortingStrategy.quick_sort(right, field)
    
    @staticmethod
    def merge_sort(records: List, field: str) -> List:
        if len(records) <= 1:
            return records
            
        mid = len(records) // 2
        left = SortingStrategy.merge_sort(records[:mid], field)
        right = SortingStrategy.merge_sort(records[mid:], field)
        
        return SortingStrategy.merge(left, right, field)
    
    @staticmethod
    def merge(left: List, right: List, field: str) -> List:
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if getattr(left[i], field) <= getattr(right[j], field):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result