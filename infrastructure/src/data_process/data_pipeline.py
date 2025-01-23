import pandas       as pd
import geopandas    as gpd

# from application.src.utilities import methods
from infrastructure.src.utilities.config import pdict


# @methods.timer
def data_process(df_geodat_plz: pd.DataFrame, df_charging: pd.DataFrame, required_columns: tuple): # geodata_path="data/datasets/geodata_berlin_plz.csv", 
                  # charging_data_path="data/datasets/Ladesaeulenregister.csv"):
    """Data process: Load and process data"""
    # Load data
    # df_geodat_plz = pd.read_csv(geodata_path, sep=';')  # For geospatial data
    # df_charging = pd.read_csv(charging_data_path, sep=';')  # For geospatial data

    ## Preprocessing dataframe from Ladesaeulenregister.csv
    
    # Select subset df_charging with fewer columns
    df_charging = df_charging.loc[:, required_columns].copy()
    
    # Rename some columns of df_charging
    df_charging.rename(columns = {"Nennleistung Ladeeinrichtung [kW]"   : "KW", 
                                  "Postleitzahl"                        : "PLZ",
                                  "Steckertypen1"                       : "Plug Types"}
                                  , inplace = True)

    # Now replace the commas with periods
    df_charging.loc[:,'Breitengrad']    = df_charging['Breitengrad'].str.replace(',', '.')
    df_charging.loc[:,'Längengrad']     = df_charging['Längengrad'].str.replace(',', '.')
    # df_charging.loc[:,'KW']             = df_charging['KW'].str.replace(',', '.')

    # Convert to string
    df_charging                         = df_charging.astype({"Breitengrad"   : str, 
                                                              "Längengrad"    : str,
                                                              "KW"            : float
                                                            })

    # Filter criteria "PLZ": only select "PLZ" in berlin
    df_charging_berlin                  = df_charging[(df_charging["PLZ"] > 10115) &   # (df_charging["Bundesland"] == 'Berlin') &
                                            (df_charging["PLZ"] < 14200)].copy().astype({"PLZ" : int})
    
    # Filter criteria "Bundesland": only select "Bundesland" containing Berlin
    df_charging_berlin                  = df_charging_berlin[df_charging_berlin["Bundesland"].str.contains("Berlin")]
    
    # Sort df by "PLZ" and reset index
    df_charging_berlin.sort_values(by   ="PLZ", inplace=True, ignore_index=True)
    
    # Merge df_charging_berlin and df_geodat_plt to get geo data for berlins zip codes
    df_charging_berlin                  = df_charging_berlin.merge(df_geodat_plz, on=pdict["geocode"], how ='left')
    df_charging_berlin.dropna(subset    =['geometry'], inplace=True)

    # Make geopanda df for creationg heatmap later on
    df_charging_berlin.loc[:,'geometry']= gpd.GeoSeries.from_wkt(df_charging_berlin['geometry'])
    df_charging_berlin                  = gpd.GeoDataFrame(df_charging_berlin, geometry='geometry')

    return df_charging_berlin
