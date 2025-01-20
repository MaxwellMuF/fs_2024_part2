import json
import unittest
import tempfile
import pandas as pd
import streamlit as st

# Test the following methods from user_data_process
from domain.src.customer_data.user_data_process import (
                                                        DataValidator
                                                        )

# # Run test from main directory (as streamlit does with scripts) 
# python -m unittest domain\src\tests\test_user_data_process.py

#  --------------------------------------- Tests ------------------------------------------------------

import unittest

class TestDataValidation(unittest.TestCase):
    def setUp(self):
        """Set up sample DataFrame for testing"""
        # Creating user_data of one user
        user_data_example    = {"PLZ"               : {"1492": 12489}, 
                                "Stra\u00dfe"       : {"1492": "Stromstra\u00dfe"}, 
                                "Hausnummer"        : {"1492": "40"}, 
                                "Anzahl Ladepunkte" : {"1492": 2.0}, 
                                "KW"                : {"1492": 22.0}, 
                                "Rating"            : {"1492": "\u2b50\u2b50"}, 
                                "Comment"           : {"1492": "slow!"}, 
                                "Date"              : {"1492": "2025-01-20 18:55:19"}}
        self.user_data_example = user_data_example
        return
    
    def test_check_required_columns_exist(self):
        """Test of method: check_required_columns_exist."""
        columns_expected_example_1 = ["PLZ", "Straße", "Hausnummer"]
        columns_expected_example_2 = ["PLZ", "Straße", "Hausnummer", "Price"]

        # Case 1: True
        validator_1 = DataValidator(data_of_one_user=self.user_data_example)
        self.assertTrue(validator_1.check_required_columns_exist(columns_expected_example_1))

        # Case 1: False
        self.assertFalse(validator_1.check_required_columns_exist(columns_expected_example_2))
        return

    def test_check_columns_types(self):
        """Test of method: check_columns_types."""
        assert_data_types    = {"PLZ"               : int, 
                                "Straße"            : str, 
                                "Hausnummer"        : str, 
                                "Anzahl Ladepunkte" : float, 
                                "KW"                : float, 
                                "Rating"            : str, 
                                "Comment"           : str, 
                                "Date"              : str}

        # Case 1: True: Match all types
        validator_2 = DataValidator(data_of_one_user=self.user_data_example)
        self.assertTrue(validator_2.check_columns_types(assert_data_types))

        # Case 2: False: Mismatched type
        user_data_example_2 = self.user_data_example
        user_data_example_2["Date"] = {"1492": 1687}
        validator_2 = DataValidator(data_of_one_user=user_data_example_2)
        self.assertFalse(validator_2.check_columns_types(assert_data_types))
        return

    def test_check_required_column_values_not_empty(self):
        """Test of method: check_required_column_values_not_empty."""
        required_columns_example_1 = ["PLZ", "Straße"]
        required_columns_example_2 = ["PLZ", "Straße", "Hausnummer"]
        required_columns_example_3 = ["PLZ", "Straße", "Hausnummer", "Anzahl Ladepunkte"]

        user_data_example           = { "PLZ"                : {"1492": 12489,            "1493": 12489}, 
                                        "Straße"             : {"1492": "Stromstraße",    "1493": "Stromstraße"}, 
                                        "Hausnummer"         : {"1492": "40",             "1493": ""},
                                        "Anzahl Ladepunkte"  : {"1492": 2.0,              "1493": None}}

        validator = DataValidator(data_of_one_user=user_data_example)
        self.assertTrue(validator.check_required_column_values_not_empty(required_columns_example_1))
        self.assertFalse(validator.check_required_column_values_not_empty(required_columns_example_2))
        self.assertFalse(validator.check_required_column_values_not_empty(required_columns_example_3))
        return
