import json
import unittest
import tempfile
import pandas as pd


#  --------------------------------------- Functions ------------------------------------------------------

# GREEN: Minimal implementation
def check_required_columns_exist(data_of_one_user: dict, columns_expected: list) -> bool:
    """Check if all columns_expected are keys from data_of_one_user"""
    return set(columns_expected).issubset(data_of_one_user.keys())
