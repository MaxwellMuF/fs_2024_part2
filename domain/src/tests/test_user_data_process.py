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

# RED: First Test
def test_check_one_user_data():
    """Test of function: check_one_user_data"""

    columns_expected_example = ['PLZ', 'Straße', 'Hausnummer', 'Anzahl Ladepunkte', 'KW', 'Rating', 'Comment', 'Date']

    # Date column is mission
    user_data_example = {"PLZ"              : {"1492": 12489}, 
                        "Straße"            : {"1492": "Stromstraße"}, 
                        "Hausnummer"        : {"1492": "40"}, 
                        "Anzahl Ladepunkte" : {"1492": 2.0}, 
                        "KW"                : {"1492": 22.0}, 
                        "Rating"            : {"1492": "\u2b50\u2b50"}, 
                        "Comment"           : {"1492": "slow!"}}
    
    expected_result_user_data_example = ["Date"]
    
    # all columns are existing
    user_data_example_2 = {"PLZ"              : {"1492": 12489}, 
                        "Straße"            : {"1492": "Stromstraße"}, 
                        "Hausnummer"        : {"1492": "40"}, 
                        "Anzahl Ladepunkte" : {"1492": 2.0}, 
                        "KW"                : {"1492": 22.0}, 
                        "Rating"            : {"1492": "\u2b50\u2b50"}, 
                        "Comment"           : {"1492": "slow!"}, 
                        "Date"              : {"1492": "2025-01-20 18:55:19"}}
    
    expected_result_user_data_example_2 = []
    
    result_1 = check_one_user_data(user_data_example, columns_expected_example)
    result_2 = check_one_user_data(user_data_example_2, columns_expected_example)

    assert result_1 == expected_result_user_data_example
    assert result_2 == expected_result_user_data_example_2
    
    return 


if __name__ == "__main__":
    test_check_one_user_data()
    print("test passed")
