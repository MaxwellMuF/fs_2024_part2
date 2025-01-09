import pandas as pd
from core import methods as m1
from core import HelperTools as ht
from core.config import pdict

@ht.timer
def data_process():
    """Data process: Load and process data"""
    # Load data
    df_geodat_plz = pd.read_csv('data/datasets/geodata_berlin_plz.csv', sep=';')  # For geospatial data
    df_lstat = pd.read_excel('data/datasets/Ladesaeulenregister_SEP.xlsx', header=10)
    df_residents = pd.read_csv('data/datasets/plz_einwohner.csv')  # Adjust the path accordingly


    # Inspect data (optional debugging statements)
    print("Initial columns in df_lstat:", df_lstat.columns)
    print("Sample data from df_lstat:", df_lstat.head(3))

    #df_residents = pd.read_csv('data/datasets/plz_einwohner.csv')  # Adjust the path accordingly

    # Data Quality Checks
    required_columns_charging = ['Postleitzahl', 'Bundesland', 'Breitengrad', 'Längengrad', 'Nennleistung Ladeeinrichtung [kW]']
    column_formats_charging = {
        'Postleitzahl': int,
        'Bundesland': str,
        'Breitengrad': (float, str),  # Allow strings due to conversion step
        'Längengrad': (float, str),
        'Nennleistung Ladeeinrichtung [kW]': float
    }
    value_ranges_charging = {
        'Postleitzahl': (10000, 14200),
        'Nennleistung Ladeeinrichtung [kW]': (0, 1000)
    }
    quality_issues_lstat = ht.check_data_quality(df_lstat, required_columns_charging, column_formats_charging, value_ranges_charging)
    if quality_issues_lstat:
        print()
        # print("Data Quality Issues for Charging Stations:", quality_issues_lstat)

    required_columns_residents = ['plz', 'einwohner', 'lat', 'lon']
    column_formats_residents = {
        'plz': int,
        'einwohner': int,
        'lat': float,
        'lon': float
    }
    value_ranges_residents = {
        'plz': (10000, 14200),
        'einwohner': (0, 50000)
    }
    quality_issues_residents = ht.check_data_quality(df_residents, required_columns_residents, column_formats_residents, value_ranges_residents)
    if quality_issues_residents:
        print()
        # print("Data Quality Issues for Residents Data:", quality_issues_residents)

    # Preprocess data
    gdf_lstat = m1.preprop_lstat(df_lstat, df_geodat_plz, pdict)
    gdf_lstat3 = m1.count_plz_occurrences(gdf_lstat)
    gdf_residents2 = m1.preprop_resid(df_residents, df_geodat_plz, pdict)

    gdf_lstat3.to_csv("gdf_lstat3.csv")
    gdf_residents2.to_csv("gdf_residents2.csv")

    return gdf_lstat3, gdf_residents2

def load_or_process_data():
    try:
        gdf_lstat3 = pd.read_csv("gdf_lstat3.csv")
        gdf_residents2 = pd.read_csv("gdf_residents2.csv")
        print("Loaded Date")
        return gdf_lstat3, gdf_residents2 

    except:
        print("Make Data process")
        return data_process()
