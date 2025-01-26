import pandas as pd
import geopandas as gpd



# Process data for berlin, i.e. filter for berlin data
# ----------------------------- Functions ------------------------------

def data_process_stations(df: pd.DataFrame, required_columns: tuple, column_mapper: dict) -> pd.DataFrame:
    """Data process: Load and process data"""
    
    # Filter required columns and Berlin zip code
    df_subset_berlin                        = df[(df[required_columns[0]] > 10000) & # (df["Bundesland"] == "Berlin") &
                                                 (df[required_columns[0]] < 14200)].copy() # .astype({required_columns[0] : int})
    df_subset_berlin_cols                   = df_subset_berlin.loc[:, required_columns].copy()
    # Rename some columns of df_charging
    df_subset_berlin_cols.rename(columns    = column_mapper, inplace = True)

    return df_subset_berlin_cols

# ----------------------------- Pipeline ------------------------------

raw_data_path = "infrastructure/data/raw_data"
processed_data = "domain/data/processed_data_for_ui"

# Filter columns
stations_required_columns   = ("Postleitzahl", "Straße", "Hausnummer", "Art der Ladeeinrichung", "Anzahl Ladepunkte",
                               "Nennleistung Ladeeinrichtung [kW]")
residents_required_columns  = ("plz", "einwohner")
# Rename columns
stations_columns_mapper     = {"Nennleistung Ladeeinrichtung [kW]"   : "KW", 
                               "Postleitzahl"                        : "PLZ"}
residents_columns_mapper    = {"plz"                                 : "PLZ", 
                               "einwohner"                           : "Residents"}


df_charging_raw = pd.read_csv(f"{raw_data_path}/Ladesaeulenregister.csv", sep=",")
df_residents_raw = pd.read_csv(f"{raw_data_path}/plz_einwohner.csv", sep=",")
df_geodata_raw = pd.read_csv(f"{raw_data_path}/geodata_berlin_plz.csv", sep=",")

df_charging_berlin  = data_process_stations(df_charging_raw, stations_required_columns, stations_columns_mapper)
df_residents_berlin = data_process_stations(df_residents_raw, residents_required_columns, residents_columns_mapper)

df_charging_berlin.to_csv(f"{processed_data}/Ladesaeulenregister.csv", index=False)
df_residents_berlin.to_csv(f"{processed_data}/plz_einwohner.csv", index=False)
df_geodata_raw.to_csv(f"{processed_data}/geodata_berlin_plz.csv", index=False)