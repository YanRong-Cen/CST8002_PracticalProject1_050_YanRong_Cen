"""
Course: CST8002 - Programming Language
Professor: Todd Keuleman
Due Date: 2025-02-16
Author: YanRong Cen

Description:
This module provides visualization capabilities for the facility management system.
"""
import matplotlib.pyplot as plt
from collections import Counter
from typing import List
from model.FacilityRecord import FacilityRecord

class FacilityVisualizer:
    @staticmethod
    def create_horizontal_bar_chart(records: List[FacilityRecord], field: str, title: str):
        """Create a horizontal bar chart showing the distribution of values for a given field."""
        # Count occurrences of each value
        values = [getattr(record, field) for record in records]
        value_counts = Counter(values)
        
        # Sort by count in descending order
        sorted_counts = dict(sorted(value_counts.items(), key=lambda x: x[1], reverse=True))
        
        # Create the chart
        plt.figure(figsize=(12, 6))
        plt.barh(list(sorted_counts.keys()), list(sorted_counts.values()))
        plt.title(title)
        plt.xlabel('Count')
        plt.ylabel(field.replace('_', ' ').title())
        plt.tight_layout()
        
        # Save the chart
        plt.savefig('facility_chart.png')
        plt.close()
        print("\nChart saved as 'facility_chart.png'")

    @staticmethod
    def create_vertical_bar_chart(records: List[FacilityRecord], field: str, title: str):
        """Create a vertical bar chart showing the distribution of values for a given field."""
        # Count occurrences of each value
        values = [getattr(record, field) for record in records]
        value_counts = Counter(values)
        
        # Sort by count in descending order
        sorted_counts = dict(sorted(value_counts.items(), key=lambda x: x[1], reverse=True))
        
        # Create the chart
        plt.figure(figsize=(12, 6))
        plt.bar(list(sorted_counts.keys()), list(sorted_counts.values()))
        plt.title(title)
        plt.xlabel(field.replace('_', ' ').title())
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save the chart
        plt.savefig('facility_chart.png')
        plt.close()
        print("\nChart saved as 'facility_chart.png'")

    @staticmethod
    def create_pie_chart(records: List[FacilityRecord], field: str, title: str):
        """Create a pie chart showing the distribution of values for a given field."""
        # Count occurrences of each value
        values = [getattr(record, field) for record in records]
        value_counts = Counter(values)
        
        # Sort by count in descending order
        sorted_counts = dict(sorted(value_counts.items(), key=lambda x: x[1], reverse=True))
        
        # Create the chart
        plt.figure(figsize=(10, 10))
        plt.pie(list(sorted_counts.values()), labels=list(sorted_counts.keys()), autopct='%1.1f%%')
        plt.title(title)
        plt.axis('equal')
        
        # Save the chart
        plt.savefig('facility_chart.png')
        plt.close()
        print("\nChart saved as 'facility_chart.png'")

    @staticmethod
    def get_available_fields(records: List[FacilityRecord]) -> List[str]:
        """Get list of available fields for visualization."""
        if not records:
            return []
        return [attr for attr in vars(records[0]).keys() 
                if not attr.startswith('_')] 