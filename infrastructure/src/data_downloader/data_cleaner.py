import re
import pandas as pd

def process_excel_to_csv():
    """Load the excel file and drop 'Public Key' columns and save as csv"""
    df_charging_stations = pd.read_excel("infrastructure\data\datasets\Ladesaeulenregister.xlsx", header=10)
    df_charging_stations.drop([f"Public Key{i}" for i in range(1,7)], axis=1, inplace=True)
    df_charging_stations.to_csv("infrastructure\data\datasets\Ladesaeulenregister.csv")
    return 

# # apply some rex filter if needed
# rex_pattern = r'\W'
# def string_alpha_only(strings):
#     return re.sub(rex_pattern, '', strings)

# df_charging_stations["Betreiber"] = df_charging_stations["Betreiber"].astype(str).apply(string_alpha_only)
