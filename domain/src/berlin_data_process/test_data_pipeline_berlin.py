import unittest

# Test the following methods from user_data_process
from domain.src.berlin_data_process import data_pipeline_berlin


# # Run test from main directory (as streamlit does with scripts) 
# python -m unittest domain\src\berlin_data_process\test_data_pipeline_berlin.py

#  --------------------------------------- Tests ------------------------------------------------------

class TestCleaner(unittest.TestCase):
    def setUp(self):
        """Set up all required test data"""

        self.residents_reject_data = ["", "None", "NaN", "0"]
        self.test_data = [{i:values} for i,values in zip(range(len(self.residents_reject_data)),
                                                             self.residents_reject_data)]
        self.test_data += [{"key":"some_value"}]
        
    def test_process(self):
        # 1. Case: 1 of 5 rows pass
        expected = [{"key":"some_value"}]
        cleaner1 = data_pipeline_berlin.Cleaner()
        self.assertEqual(cleaner1.process(self.test_data, self.residents_reject_data), 
                         expected)

