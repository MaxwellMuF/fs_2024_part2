import json
import unittest
import tempfile
import pandas as pd


#  --------------------------------------- Functions ------------------------------------------------------

# GREEN: Minimal implementation
def check_required_columns_exist(data_of_one_user: dict, columns_expected: list) -> bool:
    """Check if all columns_expected are keys from data_of_one_user"""
    return set(columns_expected).issubset(data_of_one_user.keys())

def check_columns_types(data_of_one_user: dict, assert_data_types:dict) -> bool:
    """Check if all values have the right type for that column"""
    for column,assert_type in assert_data_types.items():
        if not all(isinstance(value, assert_type) for value in data_of_one_user[column].values()):
            return False
    return True