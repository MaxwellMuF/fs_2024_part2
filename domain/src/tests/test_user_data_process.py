import json
import unittest
import tempfile
import pandas as pd
import streamlit as st

# Test the following methods from user_data_process
from domain.src.customer_data.user_data_process import DataValidator

# # Run test from main directory (as streamlit does with scripts) 
# python -m unittest domain\src\tests\test_user_data_process.py

#  --------------------------------------- Tests ------------------------------------------------------

import unittest

class TestDataValidation(unittest.TestCase):
    def setUp(self):
        """Set up all required test data"""
        # Data test 1
        self.user_data_test_1           =  {"PLZ"               : {"1492": 12489}, 
                                            "Stra\u00dfe"       : {"1492": "Stromstra\u00dfe"}, 
                                            "Hausnummer"        : {"1492": "40"}, 
                                            "Anzahl Ladepunkte" : {"1492": 2.0}, 
                                            "KW"                : {"1492": 22.0}, 
                                            "Rating"            : {"1492": "\u2b50\u2b50"}, 
                                            "Comment"           : {"1492": "slow!"}, 
                                            "Date"              : {"1492": "2025-01-20 18:55:19"}}
        
        self.columns_expected_1         =  ["PLZ", "Straße", "Hausnummer"]
        self.columns_expected_2         =  ["PLZ", "Straße", "Hausnummer", "Price"]

        # Data test 2
        self.columns_types              =  {"PLZ"               : int, 
                                            "Straße"            : str, 
                                            "Hausnummer"        : str, 
                                            "Anzahl Ladepunkte" : float, 
                                            "KW"                : float, 
                                            "Rating"            : str, 
                                            "Comment"           : str, 
                                            "Date"              : str}
        
        user_data_test_2                =   self.user_data_test_1.copy()
        user_data_test_2["Date"]        =  {"1492": 1687}
        self.user_data_test_2           =   user_data_test_2

        # Data test 3
        self.user_data_test_3           =  {"PLZ"                : {"1492": 12489,            "1493": 12489}, 
                                            "Straße"             : {"1492": "Stromstraße",    "1493": "Stromstraße"}, 
                                            "Hausnummer"         : {"1492": "40",             "1493": ""},
                                            "Anzahl Ladepunkte"  : {"1492": 2.0,              "1493": None}}
        
        self.columns_required_1         =  ["PLZ", "Straße"]
        self.columns_required_2         =  ["PLZ", "Straße", "Hausnummer"]
        self.columns_required_3         =  ["PLZ", "Straße", "Hausnummer", "Anzahl Ladepunkte"]
    

    def test_check_required_columns_exist(self):
        """Test of method: check_required_columns_exist."""
        # Case 1: exist
        validator_1_1 = DataValidator(data_of_one_user  =self.user_data_test_1,
                                      columns_expected  =self.columns_expected_1,
                                      columns_types     =self.columns_types,
                                      columns_required  =self.columns_required_1)
        self.assertTrue(validator_1_1.check_required_columns_exist())

        # Case 2: one not exist
        validator_1_2 = DataValidator(data_of_one_user  =self.user_data_test_1,
                                      columns_expected  =self.columns_expected_2,
                                      columns_types     =self.columns_types,
                                      columns_required  =self.columns_required_1)
        self.assertFalse(validator_1_2.check_required_columns_exist())


    def test_check_columns_types(self):
        """Test of method: check_columns_types."""
        # Case 1: True: Match all types
        validator_2_1 = DataValidator(data_of_one_user  =self.user_data_test_1,
                                      columns_expected  =self.columns_expected_1,
                                      columns_types     =self.columns_types,
                                      columns_required  =self.columns_required_1)
        self.assertTrue(validator_2_1.check_columns_types())

        # Case 2: False: Mismatched type
        validator_2_2 = DataValidator(data_of_one_user  =self.user_data_test_2,
                                      columns_expected  =self.columns_expected_1,
                                      columns_types     =self.columns_types,
                                      columns_required  =self.columns_required_1)
        self.assertFalse(validator_2_2.check_columns_types())


    def test_check_required_column_values_not_empty(self):
        """Test of method: check_required_column_values_not_empty."""
        # Case 1: all values are not empty
        validator_3_1 = DataValidator(data_of_one_user  =self.user_data_test_3,
                                      columns_expected  =self.columns_expected_1,
                                      columns_types     =self.columns_types,
                                      columns_required  =self.columns_required_1)
        self.assertTrue(validator_3_1.check_required_column_values_not_empty())

        # Case 2: one string is empty
        validator_3_2 = DataValidator(data_of_one_user  =self.user_data_test_3,
                                      columns_expected  =self.columns_expected_1,
                                      columns_types     =self.columns_types,
                                      columns_required  =self.columns_required_2)
        self.assertFalse(validator_3_2.check_required_column_values_not_empty())

        # Case 3: float int is None
        validator_3_3 = DataValidator(data_of_one_user  =self.user_data_test_3,
                                      columns_expected  =self.columns_expected_1,
                                      columns_types     =self.columns_types,
                                      columns_required  =self.columns_required_3)
        self.assertFalse(validator_3_3.check_required_column_values_not_empty())

    
    def test_run_validations(self):
        # Case 1: pass all tests
        validator_4_1 = DataValidator(data_of_one_user  =self.user_data_test_1,
                                      columns_expected  =self.columns_expected_1,
                                      columns_types     =self.columns_types,
                                      columns_required  =self.columns_required_1)
        validator_4_1
        self.assertTrue(validator_4_1.run_validations())

        # Case 2: fail one test
        validator_4_2 = DataValidator(data_of_one_user  =self.user_data_test_1,
                                      columns_expected  =self.columns_expected_2,
                                      columns_types     =self.columns_types,
                                      columns_required  =self.columns_required_1)
        validator_4_2
        self.assertFalse(validator_4_2.run_validations())
