import json
import unittest
import tempfile
import pandas as pd


#  --------------------------------------- Functions ------------------------------------------------------

class DataValidator:
    def __init__(self, 
                 data_of_one_user   : dict,
                 columns_types      : dict, 
                 columns_expected   : list, 
                 columns_required   : list):
        self.data                                      = data_of_one_user
        self.columns_expected                          = columns_expected
        self.columns_types                             = columns_types
        self.columns_required                          = columns_required
        self.pass_all_validations                      = False


    def check_required_columns_exist(self) -> bool:
        """Check if all required columns exist in the data."""
        return set(self.columns_expected).issubset(self.data.keys())


    def check_columns_types(self) -> bool:
        """Check if the columns in the data have the expected types."""
        for column, expected_type in self.columns_types.items():
            if not all(isinstance(value, expected_type) for value in self.data[column].values()):
                return False
        return True


    def check_required_column_values_not_empty(self) -> bool:
        """Check if all values in the required columns are not empty."""
        for column in self.columns_required:
            if not all(bool(value) for value in self.data[column].values()):
                return False
        return True
    
    def run_validations(self):
        return self.check_required_columns_exist() \
                and self.check_columns_types() \
                and self.check_required_column_values_not_empty()




# def check_required_columns_exist(data_of_one_user: dict, columns_expected: list) -> bool:
#     """Check if all columns_expected are keys from data_of_one_user"""
#     return set(columns_expected).issubset(data_of_one_user.keys())

# def check_columns_types(data_of_one_user: dict, assert_data_types:dict) -> bool:
#     """Check if all values have the right type for that column"""
#     for column,assert_type in assert_data_types.items():
#         if not all(isinstance(value, assert_type) for value in data_of_one_user[column].values()):
#             return False
#     return True

# def check_required_column_values_not_empty(data_of_one_user: dict, columns_expected: list) -> bool:
#     """Check wether all values of expected columns are not empty"""
#     for column in columns_expected:
#         if not all(bool(value) for value in data_of_one_user[column].values()):
#             return False
#     return True
