import re
import os
import pandas       as pd
import geopandas    as gpd

def process_excel_to_csv():
    """Load the excel file and drop 'Public Key' columns and save as csv""" 
    df_charging_stations = pd.read_excel("infrastructure/data/raw_data/Ladesaeulenregister.xlsx", header=10)
    # A provider has entered his api key and triggered github secret-security-policy
    df_charging_stations.drop([f"Public Key{i}" for i in range(1,7)], axis=1, inplace=True)
    df_charging_stations.to_csv("infrastructure/data/raw_data/Ladesaeulenregister.csv")
    os.remove("infrastructure/data/raw_data/Ladesaeulenregister.xlsx")
    return

def process_geojson_to_csv():
    """Make geopandas from geojson and save as csv"""
    gdf_berlin = gpd.read_file("infrastructure/data/raw_data/plz.geojson")
    gdf_berlin.rename(columns={"plz":"PLZ"}, inplace=True)
    gdf_berlin.set_index("PLZ", drop=True, inplace=True)
    gdf_berlin.to_csv("infrastructure/data/raw_data/geodata_berlin_plz.csv")
    os.remove("infrastructure/data/raw_data/plz.geojson")
    return

# # apply some rex filter if needed
# rex_pattern = r'\W'
# def string_alpha_only(strings):
#     return re.sub(rex_pattern, '', strings)

# df_charging_stations["Betreiber"] = df_charging_stations["Betreiber"].astype(str).apply(string_alpha_only)
