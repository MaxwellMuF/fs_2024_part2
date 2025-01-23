import re
import pandas as pd

df_charging_stations = pd.read_excel("infrastructure\data\datasets\Ladesaeulenregister.xlsx", header=10)

# df_charging_stations = pd.read_csv("infrastructure\data\datasets\Ladesaeulenregister.csv")

# rex_pattern = r'\W'
# def string_alpha_only(strings):
#     return re.sub(rex_pattern, '', strings)

# df_charging_stations["Betreiber"] = df_charging_stations["Betreiber"].astype(str).apply(string_alpha_only)
# print(df_charging_stations.head(5))

df_charging_stations.to_csv("infrastructure\data\datasets\Ladesaeulenregister.csv")