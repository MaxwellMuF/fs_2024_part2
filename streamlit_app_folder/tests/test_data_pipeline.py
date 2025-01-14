import unittest
import pandas as pd
from io import StringIO
# Own python files: will be tested
from streamlit_app_folder.data_pipeline import data_process

class TestDataProcess(unittest.TestCase):

    def setUp(self):
        """Create csv sample data for testing purpose with StringIO and expected output with pd"""
        # Sample data for geodata
        self.geodata_csv    = StringIO( """PLZ;geometry
                                            10179;"POINT(13.408056 52.518611)"
                                            10243;"POINT(13.454281 52.514233)"
                                        """)
        
        # Sample data for charging data
        self.charging_csv   = \
        StringIO("""Postleitzahl;Breitengrad;Längengrad;Bundesland;Straße;Hausnummer;Ort;Nennleistung Ladeeinrichtung [kW];Steckertypen1
                    10179;52,518611;13,408056;Berlin;Some Street;1;Berlin;22,0;Type2
                    10243;52,514233;13,454281;Berlin;Another Street;2;Berlin;11,0;Type1
                """)

        # Expected output
        self.df_expected_output    = pd.DataFrame({
            "PLZ": [10179, 10243],
            "Breitengrad": ["52.518611", "52.514233"],
            "Längengrad": ["13.408056", "13.454281"],
            "Bundesland": ["Berlin", "Berlin"],
            "Straße": ["Some Street", "Another Street"],
            "Hausnummer": [1, 2],
            "Ort": ["Berlin", "Berlin"],
            "KW": [22.0, 11.0],
            "Plug Types": ["Type2", "Type1"],
            "geometry": ["POINT (13.408056 52.518611)", "POINT (13.454281 52.514233)"]
        })

    def test_data_process(self):
        """Test data_process func: read sample data. Apply data_process on test data. Assert expected output"""
        # Convert the StringIO CSV data into DataFrames
        df_geodata = pd.read_csv(self.geodata_csv, sep=";")
        df_charging = pd.read_csv(self.charging_csv, sep=";")

        # Run the data_process function
        result = data_process(df_geodata, df_charging)

        # Convert the geometry column to strings for comparison
        result["geometry"] = result["geometry"].apply(str)

        # Compare the resulting DataFrame to the expected DataFrame
        pd.testing.assert_frame_equal(result, self.df_expected_output, check_dtype=False)

if __name__ == "__main__":
    unittest.main()

