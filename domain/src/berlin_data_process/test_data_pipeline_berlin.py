import unittest

# Test the following methods from user_data_process
from domain.src.berlin_data_process import data_pipeline_berlin


# # Run test from main directory (as streamlit does with scripts) 
# python -m unittest domain\src\tests\test_data_pipeline_berlin.py

#  --------------------------------------- Tests ------------------------------------------------------

class TestDataCleaner(unittest.TestCase):
    def setUp(self):
        """Set up all required test data"""

        self.residents_testdata1 = [{'plz': '01109', 
                                    'note': '01109 Dresden', 
                                    'einwohner': '20010', 
                                    'qkm': '24.736193', 
                                    'lat': '51.12232', 
                                    'lon': '13.75621'}, 
                                    {'plz': '01127', 
                                     'note': '01127 Dresden', 
                                     'einwohner': '15079', 
                                     'qkm': '3.216483', 
                                     'lat': '51.07897', 
                                     'lon': '13.72638'}]
        self.residents_testdata2 = [{'plz': '01109', 
                                    'note': '01109 Dresden', 
                                    'einwohner': '20010', 
                                    'qkm': '24.736193', 
                                    'lat': '51.12232', 
                                    'lon': 'None'}, 
                                    {'plz': '01127', 
                                     'note': '01127 Dresden', 
                                     'einwohner': '', 
                                     'qkm': '3.216483', 
                                     'lat': '51.07897', 
                                     'lon': '13.72638'}]
        
    def test_process(self):
        # 1. Case all data passed
        cleaned_data = data_pipeline_berlin.DataCleaner(self.residents_testdata1)
        self.assertEqual(cleaned_data, self.residents_testdata1)
        # 2. Case: filtered all rows
        cleaned_data = data_pipeline_berlin.DataCleaner(self.residents_testdata2)
        self.assertEqual(cleaned_data, [])
