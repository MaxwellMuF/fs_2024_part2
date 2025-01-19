import json
import numpy        as np
import pandas       as pd
import streamlit    as st

def subset_with_criteria(df: pd.DataFrame, column: str, criteria: str):
    """Make subset with respect to user selected criteria"""
    df_result = df.copy()
    if criteria != "All":
        return df_result[df_result[column] == criteria].copy()
    else:
        return df_result

def unique_values_of_column(df: pd.DataFrame, column_name: str):
    """Get unique values of col 'column_name' of given pd.df as a list. Add str 'All' on top of list"""
    return ["All"] + sorted(df[column_name].unique())

def list_for_tooltip(df: pd.DataFrame, column_name: str, criteria: str):
    """Make list of 'KW' for given PLZ (criteria) and round them. Sort list and return in reverse order"""
    df = df[df[column_name]==criteria].copy()
    df = df.round({'KW':0}).astype({'KW':int}).loc[:,"KW"]
    kW_list = df.to_list()
    return sorted(kW_list)[::-1]

def drop_column_and_sort_by_column(df: pd.DataFrame, list_drop_column_names: list[str], sort_column_name: str):
    """Drop one or multible columns and sort the remaining df by column_name in descending order. 
    Return pd.DataFrame if a geopanda_df is given as input"""
    df = df.drop(columns=list_drop_column_names, axis=1).sort_values(sort_column_name, ascending=False).copy()
    return pd.DataFrame(df)

def load_json(path="DataBase_user_changes.json"):
    """Load json to python dict. Use encoding='utf-8' to handle german letters like 'ä' or 'ß' """
    with open(path, "r", encoding='utf-8') as file:
        dict_loaded = json.load(file)
    return dict_loaded

def save_json(dict_for_saving, path="DataBase_user_changes.json"):
    with open(path, "w", encoding='utf-8') as file:
        json.dump(dict_for_saving, file)
    return

def load_db_add_dict_save_db(path_to_db, df_to_add: pd.DataFrame):
    # Load data
    user_name = st.session_state.username
    user_database = load_json(path=path_to_db)
    if user_name in user_database.keys():
        df_user_database = pd.DataFrame(user_database[user_name])
    else:
        df_user_database = pd.DataFrame(columns=df_to_add.columns)

    df_user_database = pd.concat([df_user_database, df_to_add], axis=0)
    # user_database[user_name] = df_to_add.to_dict()
    user_database[user_name] = df_user_database.to_dict()
    save_json(user_database, path=path_to_db)
    return

def add_col_available(df: pd.DataFrame, chance: list[float, float]):
    """Add Available col by randomly pick one of two options with frequency chance (e.g. [0.4,0.6]) """
    df_result = df.copy()
    df_result["Available"] = np.random.choice(["✔️", "❌"], df_result.shape[0], p=chance) # .tolist()
    return df_result