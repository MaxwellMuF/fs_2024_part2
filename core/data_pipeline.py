import pandas       as pd
import geopandas    as gpd

from core import methods        as m1
from core import HelperTools    as ht
from core.config import pdict


@ht.timer
def data_process_old():
    """Data process: Load and process data"""
    # Load data
    df_geodat_plz = pd.read_csv('data/datasets/geodata_berlin_plz.csv', sep=';')  # For geospatial data
    df_lstat = pd.read_excel('data/datasets/Ladesaeulenregister_SEP.xlsx', header=10)
    df_residents = pd.read_csv('data/datasets/plz_einwohner.csv')  # Adjust the path accordingly


    # Inspect data (optional debugging statements)
    # print("Initial columns in df_lstat:", df_lstat.columns)
    # print("Sample data from df_lstat:", df_lstat.head(3))

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

    # gdf_lstat3.to_csv("gdf_lstat3.csv")
    # gdf_residents2.to_csv("gdf_residents2.csv")

    return gdf_lstat3 #, gdf_residents2

@ht.timer
def data_process():
    """Data process: Load and process data"""
    # Load data
    df_geodat_plz = pd.read_csv('data/datasets/geodata_berlin_plz.csv', sep=';')  # For geospatial data
    df_charging = pd.read_excel('data/datasets/Ladesaeulenregister_SEP.xlsx', header=10)
    # df_residents = pd.read_csv('data/datasets/plz_einwohner.csv')  # Adjust the path accordingly

    # Preprocessing dataframe from Ladesaeulenregister.csv
    
    df_charging = df_charging.loc[:,('Postleitzahl', 'Breitengrad','Längengrad','Bundesland', 'Straße', 'Hausnummer',
                                     'Ort', 'Nennleistung Ladeeinrichtung [kW]')]
    
    df_charging.rename(columns = {"Nennleistung Ladeeinrichtung [kW]":"KW", "Postleitzahl": "PLZ"}, inplace = True)

    # Convert to string
    df_charging.astype({"Breitengrad"   : str, 
                        "Längengrad"    : str})

    # Now replace the commas with periods
    df_charging.loc[:,'Breitengrad']  = df_charging['Breitengrad'].str.replace(',', '.')
    df_charging.loc[:,'Längengrad']   = df_charging['Längengrad'].str.replace(',', '.')

    df_charging_berlin          = df_charging[(df_charging["PLZ"] > 10115) &   # (df_charging["Bundesland"] == 'Berlin') &
                                            (df_charging["PLZ"] < 14200)].copy()
    df_charging_berlin = df_charging_berlin[df_charging_berlin["Bundesland"].str.contains("Berlin")]
    
    df_charging_berlin.sort_values(by="PLZ", inplace=True, ignore_index=True)
    # sorted_df               = dframe\
    # .sort_values(by='PLZ')\
    # .reset_index(drop=True)\
    # .sort_index()
        
    df_charging_berlin           = df_charging_berlin.merge(df_geodat_plz, on=pdict["geocode"], how ='left')
    df_charging_berlin.dropna(subset=['geometry'], inplace=True)

    df_charging_berlin.loc[:,'geometry']= gpd.GeoSeries.from_wkt(df_charging_berlin['geometry'])
    df_charging_berlin           = gpd.GeoDataFrame(df_charging_berlin, geometry='geometry')

    # df_charging_berlin            = m1.count_plz_occurrences(df_charging_berlin)

    # Preprocess data
    # gdf_lstat = m1.preprop_lstat(df_charging_berlin, df_geodat_plz, pdict)
    # # gdf_lstat = m1.sort_by_plz_add_geometry(df_lstat, df_geodat_plz, pdict)
    # gdf_lstat3 = m1.count_plz_occurrences(gdf_lstat)
    # gdf_residents2 = m1.preprop_resid(df_residents, df_geodat_plz, pdict)

    # gdf_lstat3.to_csv("gdf_lstat3.csv")
    # gdf_residents2.to_csv("gdf_residents2.csv")

    return df_charging_berlin

def load_or_process_data():
    try:
        gdf_lstat3 = pd.read_csv("gdf_lstat3.csv")
        gdf_residents2 = pd.read_csv("gdf_residents2.csv")
        print("Loaded Date")
        return gdf_lstat3, gdf_residents2 

    except:
        print("Make Data process")
        return data_process()
