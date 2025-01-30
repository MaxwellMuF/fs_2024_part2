import json
import unittest
import tempfile
import pandas           as pd
import streamlit        as st

from datetime           import datetime
from unittest.mock      import patch, mock_open, Mock

# Test the following methods from helper_page_3
from application.src.utilities.helper_page_3 import (
                                                     user_selected_row_to_df,
                                                     load_or_init_user_db,
                                                     load_all_users_db,
                                                     add_date_or_date_column,
                                                     save_json,
                                                     load_db_add_dict_save_db
                                                    )

# # Run test from main directory (as streamlit does with scripts) 
# python -m unittest application\src\tests\test_helper_page_3.py

#  --------------------------------------- Tests ------------------------------------------------------

# 1
class TestUserSelectedRowToDf(unittest.TestCase):
    def test_user_selected_row_to_df(self):
        """Test user_selected_row_to_df. Create test data and dict (criteria) and assert the right subset of data"""
        # Sample input DataFrame
        df_user_selected_subset = pd.DataFrame({
            "col1": [1, 2, 3, 4],
            "col2": ["a", "b", "c", "d"]
        })

        # Mock dict as criteria
        mock_dict_user_selected_row = Mock()
        mock_dict_user_selected_row.selection.rows = [1, 3]  # Selected rows by user

        # Call the function
        result_df = user_selected_row_to_df(df_user_selected_subset, mock_dict_user_selected_row)

        # Expected output
        expected_df = pd.DataFrame({
            "col1": [2, 4],
            "col2": ["b", "d"]
        }, index=[1, 3])  # ensure desiered index

        # Assertions
        pd.testing.assert_frame_equal(result_df, expected_df)

# 2
class TestLoadOrInitUserDb(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    def test_load_existing_user_db(self, mock_json_load, mock_open_file):
        """Test case when the user is already in the database."""
        # Mocked loaded database
        mock_user_data = {
            "test_user": {
                "col1": [1, 2],
                "col2": ["a", "b"]
            }
        }

        # Mocked data and set st.session_state
        mock_json_load.return_value = mock_user_data
        st.session_state.username = "test_user"

        # Call the function
        result_df = load_or_init_user_db(mock_user_data["test_user"])

        # Expected DataFrame
        expected_df = pd.DataFrame({
            "col1": [1, 2],
            "col2": ["a", "b"]
        })

        # Assert the result matches the expected DataFrame
        pd.testing.assert_frame_equal(result_df, expected_df)


    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    def test_initialize_new_user_db(self, mock_json_load, mock_open_file):
        """Test case when the user is not in the database."""
        # Mocked loaded database (user not present)
        mock_user_data = {
            "old_user": {
                "col1": [1, 2],
                "col2": ["a", "b"]
            }
        }
        mock_json_load.return_value = mock_user_data

        # Mocked input DataFrame columns and set st.session_state
        df_user_selected_subset_show = pd.DataFrame(columns=["col1", "col2"])
        st.session_state.username = "new_user"

        # Call the function
        result_df = load_or_init_user_db(df_user_selected_subset_show)

        # Expected DataFrame: empty DataFrame with the same columns
        expected_df = pd.DataFrame(columns=["col1", "col2"])
      
        # Assert the result matches the expected DataFrame
        pd.testing.assert_frame_equal(result_df, expected_df)

        # Test hat geholfen! helper hatte eine schwäche und test hat sie gefunden. helper konnte verbessert werden

# 3
class TestLoadAllUsersDb(unittest.TestCase):
    @patch("application.src.utilities.helper_page_2.load_json") # to mock helper2 (short name is not supported)
    @patch("builtins.open", new_callable=mock_open)
    def test_load_all_users_db(self, mock_open_file, mock_load_json):
        """Test loading all user data from the database."""
        # Mocked JSON data representing multiple users
        mock_users_db_dict = {
            "user1": {
                "col1": [1, 2],
                "col2": ["a", "b"]
            },
            "user2": {
                "col1": [3],
                "col2": ["c"]
            }
        }
        mock_load_json.return_value = mock_users_db_dict

        # Expected DataFrame
        expected_df = pd.DataFrame({
            "col1": [1, 2, 3],
            "col2": ["a", "b", "c"],
            "User": ["user1", "user1", "user2"]
        })

        # Call the function
        result_df = load_all_users_db()

        # Assert the result matches the expected DataFrame
        pd.testing.assert_frame_equal(result_df, expected_df)

# 4
class TestAddDateOrDateColumn(unittest.TestCase):
    @patch("application.src.utilities.helper_page_3.datetime")  # Mock datetime
    def test_add_date_column_to_df_without_date(self, mock_datetime):
        """Test adding a new 'Date' column when it does not exist."""
        # Mock the current datetime
        mock_datetime.today.return_value = datetime(2025, 1, 1, 12, 0, 0)
        mock_datetime.strftime = datetime.strftime

        # Input DataFrame without 'Date' column
        input_df = pd.DataFrame({
            "ID": [1, 2, 3],
            "Name": ["Station A", "Station B", "Station C"]
        })

        # Expected DataFrame with 'Date' column
        expected_df = pd.DataFrame({
            "ID": [1, 2, 3],
            "Name": ["Station A", "Station B", "Station C"],
            "Date": "2025-01-01 12:00:00"
        })

        # Call the function
        result_df = add_date_or_date_column(input_df)

        # Assert the result matches the expected DataFrame
        pd.testing.assert_frame_equal(result_df, expected_df)

    @patch("application.src.utilities.helper_page_3.datetime")  # Mock datetime
    def test_update_empty_date_values(self, mock_datetime):
        """Test filling empty 'Date' values in an existing 'Date' column."""
        # Mock the current datetime
        mock_datetime.today.return_value = datetime(2025, 1, 1, 12, 0, 0)
        mock_datetime.strftime = datetime.strftime

        # Input DataFrame with an existing 'Date' column and some empty values
        input_df = pd.DataFrame({
            "ID": [1, 2, 3],
            "Name": ["Station A", "Station B", "Station C"],
            "Date": ["", "2025-01-05 10:00:00", ""]
        })

        # Expected DataFrame with empty 'Date' values filled
        expected_df = pd.DataFrame({
            "ID": [1, 2, 3],
            "Name": ["Station A", "Station B", "Station C"],
            "Date": ["2025-01-01 12:00:00", "2025-01-05 10:00:00", "2025-01-01 12:00:00"]
        })

        # Call the function
        result_df = add_date_or_date_column(input_df)

        # Assert the result matches the expected DataFrame
        pd.testing.assert_frame_equal(result_df, expected_df)

# 5
class TestSaveJson(unittest.TestCase):
    def test_save_json(self):
        """Test save_json function"""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")

        dict_to_save = {"key": "value"}
        save_json(dict_to_save, temp_file.name)
        temp_file.close()
        
        with open(temp_file.name, "r") as file:
            result = json.load(file)

        self.assertEqual(result, dict_to_save)

# 6
## spending too much time on trying to implement streamlit methods like st.session_state in tests
# class TestLoadDbAddDictSaveDb(unittest.TestCase):

#     @patch("application.src.utilities.helper_page_3.helper2.load_json")
#     @patch("application.src.utilities.helper_page_3.save_json")
#     @patch("application.src.utilities.helper_page_3.add_date_or_date_column")
#     # @patch("application.src.utilities.helper_page_3.st.session_state")
#     def test_user_in_db_no_overwrite(self, mock_session_state, mock_add_date, mock_save_json, mock_load_json):
#         """Test case where user exists in the database, and overwrite is False."""
#         # Mock session state
#         st.session_state.username = "test_user"

#         # Mock the user database loaded from JSON
#         mock_load_json.return_value = {
#             "test_user": {
#                 "ID": [1],
#                 "Name": ["Station A"],
#                 "Date": ["2025-01-01 12:00:00"]
#             }
#         }

#         # Input DataFrame to add
#         df_to_add = pd.DataFrame({
#             "ID": [2],
#             "Name": ["Station B"]
#         })

#         # Mock the output of add_date_or_date_column
#         mock_add_date.return_value = pd.DataFrame({
#             "ID": [2],
#             "Name": ["Station B"],
#             "Date": ["2025-01-02 12:00:00"]
#         })

#         # Expected concatenated DataFrame
#         expected_user_database = {
#             "test_user": {
#                 "ID": [2, 1],
#                 "Name": ["Station B", "Station A"],
#                 "Date": ["2025-01-02 12:00:00", "2025-01-01 12:00:00"]
#             }
#         }

#         # Call the function
#         path_to_db = "mock_path.json"
#         load_db_add_dict_save_db(path_to_db, df_to_add, overwrite=False)

#         # Verify the save_json call
#         mock_save_json.assert_called_once_with(expected_user_database, path=path_to_db)

#     @patch("application.src.utilities.helper_page_3.helper2.load_json")
#     @patch("application.src.utilities.helper_page_3.save_json")
#     @patch("application.src.utilities.helper_page_3.add_date_or_date_column")
#     # @patch("application.src.utilities.helper_page_3.st.session_state")
#     def test_user_not_in_db(self, mock_session_state, mock_add_date, mock_save_json, mock_load_json):
#         """Test case where user does not exist in the database."""
#         # Mock session state
#         st.session_state.username = "new_user"

#         # Mock the user database loaded from JSON
#         mock_load_json.return_value = {}

#         # Input DataFrame to add
#         df_to_add = pd.DataFrame({
#             "ID": [1],
#             "Name": ["Station A"]
#         })

#         # Mock the output of add_date_or_date_column
#         mock_add_date.return_value = pd.DataFrame({
#             "ID": [1],
#             "Name": ["Station A"],
#             "Date": ["2025-01-01 12:00:00"]
#         })

#         # Expected user database
#         expected_user_database = {
#             "new_user": {
#                 "ID": [1],
#                 "Name": ["Station A"],
#                 "Date": ["2025-01-01 12:00:00"]
#             }
#         }

#         # Call the function
#         path_to_db = "mock_path.json"
#         load_db_add_dict_save_db(path_to_db, df_to_add, overwrite=False)

#         # Verify the save_json call
#         mock_save_json.assert_called_once_with(expected_user_database, path=path_to_db)

#     @patch("application.src.utilities.helper_page_3.helper2.load_json")
#     @patch("application.src.utilities.helper_page_3.save_json")
#     @patch("application.src.utilities.helper_page_3.add_date_or_date_column")
#     # @patch("application.src.utilities.helper_page_3.st.session_state")
#     def test_user_in_db_with_overwrite(self, mock_session_state, mock_add_date, mock_save_json, mock_load_json):
#         """Test case where user exists in the database, and overwrite is True."""
#         # Mock session state
#         st.session_state.username = "test_user"

#         # Mock the user database loaded from JSON
#         mock_load_json.return_value = {
#             "test_user": {
#                 "ID": [1],
#                 "Name": ["Station A"],
#                 "Date": ["2025-01-01 12:00:00"]
#             }
#         }

#         # Input DataFrame to add
#         df_to_add = pd.DataFrame({
#             "ID": [2],
#             "Name": ["Station B"]
#         })

#         # Mock the output of add_date_or_date_column
#         mock_add_date.return_value = pd.DataFrame({
#             "ID": [2],
#             "Name": ["Station B"],
#             "Date": ["2025-01-02 12:00:00"]
#         })

#         # Expected user database after overwrite
#         expected_user_database = {
#             "test_user": {
#                 "ID": [2],
#                 "Name": ["Station B"],
#                 "Date": ["2025-01-02 12:00:00"]
#             }
#         }

#         # Call the function
#         path_to_db = "mock_path.json"
#         load_db_add_dict_save_db(path_to_db, df_to_add, overwrite=True)

#         # Verify the save_json call
#         mock_save_json.assert_called_once_with(expected_user_database, path=path_to_db)

