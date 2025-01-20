import json
import unittest
import tempfile
import pandas as pd


#  --------------------------------------- Functions ------------------------------------------------------

# GREEN: Minimal implementation
def check_one_user_data(data_of_one_user, columns_expected):
    """ Check data quality of one user"""

    catch_mission_columns = []
    for column in columns_expected:
        if column not in data_of_one_user.keys():
            catch_mission_columns.append(column)
    
    return catch_mission_columns
