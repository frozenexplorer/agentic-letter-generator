import csv
from typing import List, Dict

def load_employee_data(filepath: str) -> List[Dict]:
    """Load employee metadata from CSV into a list of dicts"""
    employees = []
    with open(filepath, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Clean up keys and values
            employee = {k.strip(): v.strip() for k, v in row.items()}
            employees.append(employee)
    return employees
