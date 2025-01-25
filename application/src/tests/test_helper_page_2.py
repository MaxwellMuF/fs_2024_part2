import unittest
import tempfile
import pandas as pd

from unittest.mock import MagicMock, patch

# Test the following methods from helper_page_2
from application.src.utilities.helper_page_2 import (
                                                        subset_with_criteria,           # 1
                                                        unique_values_of_column,        # 2
                                                        list_for_tooltip,               # 3
                                                        drop_column_and_sort_by_column, # 4
                                                        load_json,                      # 5
                                                        add_col_available               # 6
                                                        )


# # Run test from main directory (as streamlit does with scripts) 
# python -m unittest application\src\tests\test_helper_page_2.py

#  --------------------------------------- Tests ------------------------------------------------------

# 1
class TestSubsetWithCriteria(unittest.TestCase):

    def setUp(self):
        """Set up sample DataFrame for testing"""
        # Creating a simple DataFrame for testing
        data = {
            "PLZ": [10115, 10117, 10119, 10243],
            "KW": [3.7, 13.2, 150.0, 600.0]
        }
        self.df = pd.DataFrame(data)
        return

    def test_helper_subset_with_criteria_all(self):
        """Test the `helper_subset_with_criteria` function with criteria = 'All'."""
        # Call the function with "All"
        result = subset_with_criteria(self.df, "PLZ", "All")

        # Verify that the result is a copy of the original DataFrame
        pd.testing.assert_frame_equal(result, self.df)
        return

    def test_helper_subset_with_criteria_filtered(self):
        """Test the `helper_subset_with_criteria` function with specific criteria"""
        # Call the function with a specific criteria
        result = subset_with_criteria(self.df, "PLZ", 10115)

        # Verify that the result contains only the row where "PLZ" is 10115
        expected_data = {
            "PLZ": [10115],
            "KW": [3.7]
        }
        expected_df = pd.DataFrame(expected_data)

        # Verify that the result matches the expected filtered DataFrame
        pd.testing.assert_frame_equal(result, expected_df)
        return

# 2
class TestUniqueValuesOfColumn(unittest.TestCase):

    def test_helper_unique_values_of_column(self):
        """Test the helper_unique_values_of_column function"""

        # Create a sample dataframe
        data = {
            "PLZ": [10115, 10117, 10119, 10117, 10119, 10121],
            "KW": [3.7, 13.2, 3.7, 600.0, 150.0, 13.2]
        }
        df = pd.DataFrame(data)

        # Test with "PLZ" column
        expected_output_plz = ["All", 10115, 10117, 10119, 10121]
        result_plz = unique_values_of_column(df, "PLZ")

        self.assertEqual(result_plz, expected_output_plz)

        # Test with "KW" column
        expected_output_kW = ["All", 3.7, 13.2, 150.0, 600.0]
        result_city = unique_values_of_column(df, "KW")

        self.assertEqual(result_city, expected_output_kW)
        return

# 3
class TestListForTooltip(unittest.TestCase):
    def test_list_for_tooltip(self):
        """Test list_for_tooltip function"""
        data = {
            "PLZ": [10115, 10115, 10119, 10119],
            "KW": [22.5, 50.3, 11.0, 100.9],
        }
        df = pd.DataFrame(data)

        result = list_for_tooltip(df, "PLZ", 10115)
        expected = [50, 22]

        self.assertEqual(result, expected)
        return

# 4
class TestDropColumnAndSortByColumn(unittest.TestCase):
    def test_drop_column_and_sort_by_column(self):
        """Test drop_column_and_sort_by_column function"""
        data = {
            "Straße":  [i for i in "abcdef"],
            "KW":   [11, 13.2, 3.7, 600, 150, 22],
            "geo":  ["POINT(13.408056 52.518611)"]*6
        }
        df = pd.DataFrame(data)

        result = drop_column_and_sort_by_column(df, ["geo"], "KW")
        expected = pd.DataFrame({"Straße":  [i for i in "defbac"], 
                                 "KW":   [600, 150, 22, 13.2, 11, 3.7,],})

        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)

# 5
class TestLoadJson(unittest.TestCase):
    def test_load_json(self):
        """Test load_json function"""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        temp_file.write(b'{"key": "value"}')
        temp_file.close()

        result = load_json(temp_file.name)
        expected = {"key": "value"}

        self.assertEqual(result, expected)

# 6
class TestAddColAvailable(unittest.TestCase):
    @patch("numpy.random.choice", return_value=["✔️", "❌", "✔️"])
    def test_add_col_available(self, mock_random_choice):
        """Test add_col_available function"""
        data = {"A": [1, 2, 3]}
        df = pd.DataFrame(data)

        result = add_col_available(df, [0.5, 0.5])

        expected = pd.DataFrame({"A": [1, 2, 3], "Available": ["✔️", "❌", "✔️"]})
        pd.testing.assert_frame_equal(result, expected)


if __name__ == "__main__":
    unittest.main()
