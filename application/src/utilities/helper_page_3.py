import json
import numpy        as np
import pandas       as pd
import streamlit    as st

from application.src.utilities          import helper_page_2 as helper2

def user_selected_row_to_df(df_user_selected_subset: pd.DataFrame, dict_user_selected_row: dict) -> pd.DataFrame:
    """Use index of selected rows (dict_user) to make subset of data (df_user) and
       return the selected subset (df_seleced)"""
    row_idx = dict_user_selected_row.selection.rows
    df_selected_to_rate = df_user_selected_subset.iloc[row_idx,:]

    return df_selected_to_rate

def load_or_init_user_db(df_user_selected_subset_show: pd.DataFrame) -> pd.DataFrame:
    """User DB two cases: use as data 1. loadet data if user in DB
                                      2. initialize a user DB"""

    with open("application/data/data_user/DataBase_user_changes.json", "r") as file:
        loaded_database = json.load(file)
    # 1. user in DB
    if st.session_state.username in loaded_database.keys():
        return pd.DataFrame(loaded_database[st.session_state.username])
    # 2. new user DB
    else:
        return pd.DataFrame(columns=df_user_selected_subset_show)
    
def load_all_users_db() -> pd.DataFrame:
    users_db_dict = helper2.load_json(path="application/data/data_user/DataBase_user_changes.json")
    df_all_users_posts = pd.DataFrame()
    for user in users_db_dict.keys():
        df_user = pd.DataFrame(users_db_dict[user])
        df_user["User"] = user
        df_all_users_posts = pd.concat(objs=[df_all_users_posts, df_user], axis=0, ignore_index=True)
    
    return df_all_users_posts