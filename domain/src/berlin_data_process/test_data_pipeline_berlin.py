import unittest

# Test the following methods from user_data_process
from domain.src.berlin_data_process import data_pipeline_berlin


# # Run test from main directory (as streamlit does with scripts) 
# python -m unittest domain\src\berlin_data_process\test_data_pipeline_berlin.py

#  --------------------------------------- Tests ------------------------------------------------------

class TestCleaner(unittest.TestCase):
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
                                     'einwohner': '', 
                                     'qkm': '3.216483', 
                                     'lat': '51.07897', 
                                     'lon': '13.72638'},
                                    {'plz': '01127', 
                                     'note': '01127 Dresden', 
                                     'einwohner': '15079', 
                                     'qkm': '3.216483', 
                                     'lat': '51.07897', 
                                     'lon': 'None'},
                                    {'plz': '01127', 
                                     'note': '01127 Dresden', 
                                     'einwohner': '15079', 
                                     'qkm': 'NaN', 
                                     'lat': '51.07897', 
                                     'lon': '13.72638'},
                                    {'plz': '0', 
                                     'note': '01127 Dresden', 
                                     'einwohner': '15079', 
                                     'qkm': '3.216483', 
                                     'lat': '51.07897', 
                                     'lon': '13.72638'}]
        self.residents_reject_data = ["", "None", "NaN", "0"]
        
    def test_process(self):
        # 1. Case: 1 of 5 rows pass
        cleaner1 = data_pipeline_berlin.Cleaner()
        self.assertEqual(cleaner1.process(data=self.residents_testdata1, reject_data=self.residents_reject_data), 
                                            [self.residents_testdata1[0]])

