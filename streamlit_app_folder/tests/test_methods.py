import unittest
import pandas as pd
from io import StringIO
from streamlit_app_folder.methods import count_plz_occurrences  # Replace with the actual module name

class TestCountPLZOccurrences(unittest.TestCase):

    def setUp(self):
        """Create sample data df_test_input for testing purpose with pd and expected output with pd"""

        self.df_test_input = pd.DataFrame({
            "PLZ": [10179, 10179, 10243, 10243, 10243],
            "KW": [22.0, 11.0, 50.0, 22.0, 11.0],
            "geometry": [
                "POINT(13.408056 52.518611)",
                "POINT(13.408056 52.518611)",
                "POINT(13.454281 52.514233)",
                "POINT(13.454281 52.514233)",
                "POINT(13.454281 52.514233)"
            ]
        })

        self.df_expected_output = pd.DataFrame({
            "PLZ": [10179, 10243],
            "Number": [2, 3],
            "geometry": ["POINT(13.408056 52.518611)", "POINT(13.454281 52.514233)"]
        })

    def test_count_plz_occurrences(self):
        # Run the function
        result = count_plz_occurrences(self.df_test_input)

        # Compare the resulting DataFrame to the expected DataFrame
        pd.testing.assert_frame_equal(result, self.df_expected_output)

if __name__ == "__main__":
    unittest.main()
