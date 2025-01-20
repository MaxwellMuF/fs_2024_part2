import json
import unittest
import tempfile
import pandas as pd
import streamlit as st

# Test the following methods from user_data_process
from domain.src.customer_data.user_data_process import (
                                                        check_required_columns_exist,
                                                        check_columns_types,
                                                        check_required_column_values_not_empty
                                                        )

# # Run test from main directory (as streamlit does with scripts) 
# python -m unittest application\src\tests\test_helper_page_2_charging_stations.py

#  --------------------------------------- Tests ------------------------------------------------------

# RED: Test for Check_data_class
def test_check_required_columns_exist():
    """Test of function: check_required_columns_exist. Testcase True and False."""

    columns_expected_example_1  = ["PLZ", "Straße", "Hausnummer"]
    columns_expected_example_2  = ["PLZ", "Straße", "Hausnummer", "Date", "KW"]
    
    user_data_example_1         = {"PLZ"        : {"1492": 12489}, 
                                   "Straße"     : {"1492": "Stromstraße"}, 
                                   "Hausnummer" : {"1492": "40"}}
    
    assert check_required_columns_exist(user_data_example_1, columns_expected_example_1) == True
    assert check_required_columns_exist(user_data_example_1, columns_expected_example_2) == False
    
    return 

def test_check_columns_types():
    """Test of function: check_columns_types. Testcase True and False."""
    user_data_example    = {"PLZ"               : {"1492": 12489}, 
                            "Stra\u00dfe"       : {"1492": "Stromstra\u00dfe"}, 
                            "Hausnummer"        : {"1492": "40"}, 
                            "Anzahl Ladepunkte" : {"1492": 2.0}, 
                            "KW"                : {"1492": 22.0}, 
                            "Rating"            : {"1492": "\u2b50\u2b50"}, 
                            "Comment"           : {"1492": "slow!"}, 
                            "Date"              : {"1492": "2025-01-20 18:55:19"}}
    
    assert_data_types    = {"PLZ"               : int, 
                            "Straße"            : str, 
                            "Hausnummer"        : str, 
                            "Anzahl Ladepunkte" : float, 
                            "KW"                : float, 
                            "Rating"            : str, 
                            "Comment"           : str, 
                            "Date"              : str}
    
    # Case 1: True: Match all types
    assert check_columns_types(user_data_example, assert_data_types) == True
    
    # Case 2: Mismatched type
    user_data_example["Date"] = {"1492": 1687}
    assert check_columns_types(user_data_example, assert_data_types) == False

    return 

def test_check_required_column_values_not_empty():
    """Test of function: check_columns_types. Three test cases."""
    columns_expected_example_1  = ["PLZ", "Straße"]
    columns_expected_example_2  = ["PLZ", "Straße", "Hausnummer"]
    columns_expected_example_3  = ["PLZ", "Straße", "Hausnummer", "Anzahl Ladepunkte"]
    
    user_data_example           = {"PLZ"                : {"1492": 12489,            "1493": 12489}, 
                                   "Straße"             : {"1492": "Stromstraße",    "1493": "Stromstraße"}, 
                                   "Hausnummer"         : {"1492": "40",             "1493": ""},
                                   "Anzahl Ladepunkte"  : {"1492": 2.0,              "1493": None}}

    # Case 1: True: All required columns have non-empty values
    assert check_required_column_values_not_empty(user_data_example, columns_expected_example_1) == True
    
    # Case 2: False: str value is empty 
    assert check_required_column_values_not_empty(user_data_example, columns_expected_example_2) == False
    
    # Case 2: False: float value is None
    assert check_required_column_values_not_empty(user_data_example, columns_expected_example_3) == False

if __name__ == "__main__":
    test_check_required_columns_exist()
    test_check_columns_types()
    test_check_required_column_values_not_empty()
    print("test passed")
