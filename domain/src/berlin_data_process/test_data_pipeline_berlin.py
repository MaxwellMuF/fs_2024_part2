import unittest

# Test the following methods from user_data_process
from domain.src.berlin_data_process import data_pipeline_berlin


# # Run test from main directory (as streamlit does with scripts) 
# python -m unittest domain\src\berlin_data_process\test_data_pipeline_berlin.py

#  --------------------------------------- Tests ------------------------------------------------------

class TestFilterColumns(unittest.TestCase):
    def setUp(self):
        """Set up all required test data"""
        self.testdata = [{key:value for key,value in zip(range(10),range(10))}]*2
        self.testdata_incorrect = [{key:value for key,value in zip(range(1,10),range(1,10))}]
        self.required_columns = [i for i in range(5)]

    def test_process(self):
        """Process test: """
        # 1. Case: pass test
        expected = [{key:value for key,value in zip(range(5),range(5))}]*2
        filter_columns = data_pipeline_berlin.FilterColumns(self.required_columns)
        self.assertEqual(filter_columns.process(self.testdata), expected)

        # 2. Case: incomplete data
        expected = []
        filter_columns2 = data_pipeline_berlin.FilterColumns(self.required_columns)

        with self.assertRaises(KeyError) as context:
            filter_columns2.process(self.testdata_incorrect)
        
        self.assertIn("Missing required column: 0 in row: {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9}", 
                      str(context.exception))

 

class TestCleaner(unittest.TestCase):
    def setUp(self):
        """Set up all required test data"""
        self.residents_reject_data = ["", "None", "NaN", "0"]
        self.test_data = [{i:values} for i,values in zip(range(len(self.residents_reject_data)),
                                                             self.residents_reject_data)]
        self.test_data += [{"key":"some_value"}]
        
    def test_process(self):
        """Process test: 1 of 5 rows pass"""
        expected = [{"key":"some_value"}]
        cleaner1 = data_pipeline_berlin.Cleaner()
        self.assertEqual(cleaner1.process(self.test_data, self.residents_reject_data), 
                         expected)

