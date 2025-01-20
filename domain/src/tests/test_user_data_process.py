import json
import unittest
import tempfile
import pandas as pd
import streamlit as st

# Test the following methods from user_data_process
from domain.src.customer_data.user_data_process import (
                                                        check_one_user_data
)

# # Run test from main directory (as streamlit does with scripts) 
# python -m unittest application\src\tests\test_helper_page_2_charging_stations.py

#  --------------------------------------- Tests ------------------------------------------------------

# RED: Test for Check_data_class
def test_check_one_user_data():
    """Test of function: check_one_user_data"""

    columns_expected_example_1 = ["PLZ", "Straße", "Hausnummer"]
    columns_expected_example_2 = ["PLZ", "Straße", "Hausnummer", "Date", "KW"]
    
    user_data_example_1 = {"PLZ"              : {"1492": 12489}, 
                           "Straße"            : {"1492": "Stromstraße"}, 
                           "Hausnummer"        : {"1492": "40"}}
    
    assert check_one_user_data(user_data_example_1, columns_expected_example_1) == True
    assert check_one_user_data(user_data_example_1, columns_expected_example_2) == False
    
    return 


if __name__ == "__main__":
    test_check_one_user_data()
    print("test passed")
