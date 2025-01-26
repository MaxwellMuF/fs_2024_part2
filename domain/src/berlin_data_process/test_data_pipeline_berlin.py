import unittest

# Test the following methods from user_data_process
from domain.src.berlin_data_process import data_pipeline_berlin


# # Run test from main directory (as streamlit does with scripts) 
# python -m unittest domain\src\berlin_data_process\test_data_pipeline_berlin.py

#  --------------------------------------- Tests ------------------------------------------------------

class TestFilterColumns(unittest.TestCase):
    def setUp(self):
        """Set up all required test data"""
        self.testdata               = [{key:value for key,value in zip(range(10),range(10))}]*2
        self.testdata_incorrect     = [{key:value for key,value in zip(range(1,10),range(1,10))}]
        self.required_columns       = [i for i in range(5)]

    def test_process(self):
        """Process test: 1. filter correct, 2. missing column"""
        # 1. Case: pass test
        expected            = [{key:value for key,value in zip(range(5),range(5))}]*2
        filter_columns      = data_pipeline_berlin.FilterColumns(self.required_columns)

        self.assertEqual(filter_columns.process(self.testdata), expected)

        # 2. Case: incomplete data
        expected            = []
        filter_columns2     = data_pipeline_berlin.FilterColumns(self.required_columns)

        with self.assertRaises(KeyError) as context:
            filter_columns2.process(self.testdata_incorrect)
        self.assertIn("FilterColumns: Missing required column: 0 in row: {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9}", 
                      str(context.exception))
 

class TestCleaner(unittest.TestCase):
    def setUp(self):
        """Set up all required test data"""
        self.residents_reject_data = ["", "None", "NaN", "0"]
        self.test_data = [{i:values} for i,values in zip(range(len(self.residents_reject_data)),
                                                             self.residents_reject_data)]
        self.test_data += [{"key":"some_value"}, {"key2":"some_value2"}]
        
    def test_process(self):
        """Process test: 2 of 6 rows pass"""
        expected = [{"key":"some_value"}, {"key2":"some_value2"}]
        cleaner1 = data_pipeline_berlin.Cleaner()
        self.assertEqual(cleaner1.process(self.test_data, self.residents_reject_data), 
                         expected)
        
class TestFilterBerlin(unittest.TestCase):
    def setUp(self):
        """Set up all required test data"""
        self.testdata               = [{"PLZ":value} for value in range(901, 1501, 100)]
        self.filter_plz_min         = 1000
        self.filter_plz_max         = 1400
        
    def test_process(self):
        """Process test: filter rows correctly"""
        expected                    = [{"PLZ":value} for value in range(1001, 1401, 100)]
        filter_berlin1              = data_pipeline_berlin.FilterBerlin(self.filter_plz_min, self.filter_plz_max)

        self.assertEqual(filter_berlin1.process(self.testdata), expected)


class TestValidator(unittest.TestCase):
    def setUp(self):
        """Set up all required test data"""
        self.testdata               = [{"PLZ":10, "Straße":"some_street", "KW":3.7}] * 100_000
        self.testdata_incorrect     = [{"PLZ":10, "Straße":"some_street", "KW":3.7},
                                       {"PLZ":10.1, "Straße":"some_street", "KW":3.7},
                                       {"PLZ":10, "Straße":"some_street", "KW":"some_str"}]
        
        self.required_types         = {"PLZ":int, "Straße":str, "KW":float}
        
    def test_process(self):
        """Process test: filter rows correctly"""
        # 1. Case: pass test
        expected                    = self.testdata
        validator1                  = data_pipeline_berlin.Validator(self.required_types)

        self.assertEqual(validator1.process(self.testdata), expected)

        # 2. Case:
        validator2                  = data_pipeline_berlin.Validator(self.required_types)

        with self.assertRaises(ValueError) as context:
            validator2.process(self.testdata_incorrect)
        self.assertIn("Skipped invalid row: {'PLZ': 10, 'Straße': 'some_street', 'KW': 'some_str'}. Error: could not convert string to float: 'some_str'", 
                      str(context.exception))
        self.assertEqual(validator2.process(self.testdata), expected)

