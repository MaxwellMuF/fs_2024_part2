import json
import unittest
import tempfile
import pandas as pd
import streamlit as st

from unittest.mock import MagicMock, patch

# Test the following methods from helper_page_2
from application.src.ui.page_3_rate_and_comment import (
                                                        init_data
                                                        )

# test fails because of session states. Hard to reproduce with Mock
# python -m unittest application\src\tests\test_page_3_rate_and_comment.py

#  --------------------------------------- Tests ------------------------------------------------------
# class TestInitData(unittest.TestCase):

#     def setUp(self):
#         """Set up sample DataFrame for testing"""
#         # Creating a simple DataFrame for testing
#         data = {
#             "PLZ": [10115, 10117, 10119, 10243],
#             "KW": [3.7, 13.2, 150.0, 600.0]
#         }
#         self.df = pd.DataFrame(data)
#         return
    
#     def test_helper_subset_with_criteria_all(self):
#         """Test the `helper_subset_with_criteria` function with criteria = 'All'."""
#         # Call the function with "All"
#         result = subset_with_criteria(self.df, "PLZ", "All")

#         # Verify that the result is a copy of the original DataFrame
#         pd.testing.assert_frame_equal(result, self.df)
#         return
    
import unittest
import pandas as pd

class TestInitData(unittest.TestCase):
    def test_init_data_with_sample_data(self):
        # Sample input data
        geodata = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
        charging_data = pd.DataFrame({"colA": ["A", "B"], "colB": ["C", "D"]})
        expected_processed_data = pd.DataFrame({"processed_col": ["X", "Y"]})

        # Dummy function for reading CSV
        def dummy_read_csv(filepath, sep, low_memory):
            if "geodata" in filepath:
                return geodata
            elif "Ladesaeulenregister" in filepath:
                return charging_data
            else:
                raise ValueError("Unexpected file path")

        # Dummy function for processing data
        def dummy_process_data(df1, df2):
            self.assertTrue(df1.equals(geodata))  # Assert correct geodata passed
            self.assertTrue(df2.equals(charging_data))  # Assert correct charging data passed
            return expected_processed_data

        # Call the function
        # from your_module import init_data  # Replace with actual module name
        result = init_data(
            geodata_path="infrastructure\data\datasets\geodata_berlin_plz.csv",
            charging_data_path="infrastructure\data\datasets\Ladesaeulenregister.csv")

        # Assert the processed data is as expected
        print(result)
        self.assertTrue(result.equals(expected_processed_data))

if __name__ == "__main__":
    unittest.main()

