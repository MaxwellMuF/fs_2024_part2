import json
import numpy        as np
import pandas       as pd
import geopandas    as gpd

# 1 
def subset_with_criteria(df: pd.DataFrame, column: str, criteria: str):
    """Make subset with respect to user selected criteria"""
    df_result = df.copy()
    if criteria != "All":
        return df_result[df_result[column] == criteria]#.copy()
    else:
        return df_result

# 2
def unique_values_of_column(df: pd.DataFrame, column_name: str):
    """Get unique values of col 'column_name' of given pd.df as a list. Add str 'All' on top of list"""
    return ["All"] + sorted(df[column_name].unique())

# 3
def list_for_tooltip(df: pd.DataFrame, column_name: str, criteria: str):
    """Make list of 'KW' for given PLZ (criteria) and round them. Sort list and return in reverse order"""
    df = df[df[column_name]==criteria].copy()
    df = df.round({'KW':0}).astype({'KW':int}).loc[:,"KW"]
    kW_list = df.to_list()
    return sorted(kW_list)[::-1]

# 4
def drop_column_and_sort_by_column(df: pd.DataFrame, list_drop_column_names: list[str], sort_column_name: str):
    """Drop one or multible columns and sort the remaining df by column_name in descending order. 
    Return pd.DataFrame if a geopanda_df is given as input"""
    df.dropna(subset    =[sort_column_name], inplace=True)
    df = df.drop(columns=list_drop_column_names, axis=1).sort_values(sort_column_name, ascending=False).copy()
    return pd.DataFrame(df)

# 5
def load_json(path="DataBase_user_changes.json"):
    """Load json to python dict. Use encoding='utf-8' to handle german letters like 'ä' or 'ß' """
    with open(path, "r", encoding='utf-8') as file:
        dict_loaded = json.load(file)
    return dict_loaded

# 6
def add_col_available(df: pd.DataFrame, chance: list[float, float]):
    """Add Available col by randomly pick one of two options with frequency chance (e.g. [0.4,0.6]) """
    df_result = df.copy()
    df_result["Available"] = np.random.choice(["✔️", "❌"], df_result.shape[0], p=chance) # .tolist()
    return df_result

#7
def merge_with_geometry(df: pd.DataFrame, df_geo: pd.DataFrame) -> pd.DataFrame:
    """Merge df_charging_berlin and df_geodat_plt to get geo data for berlins zip codes"""
    df_merged                  = df.merge(df_geo, on='PLZ', how ='right') #pdict["geocode"]
    df_merged.dropna(subset    =['geometry'], inplace=True)

    # Make geopanda df for creationg heatmap later on
    df_merged.loc[:,'geometry']= gpd.GeoSeries.from_wkt(df_merged['geometry'])
    df_merged                  = gpd.GeoDataFrame(df_merged, geometry='geometry')

    return df_merged