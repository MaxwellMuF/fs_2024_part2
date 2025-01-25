import json
import pandas                       as pd
import streamlit                    as st

from datetime                       import datetime
from application.src.utilities      import helper_page_2 as helper2

# 1
def user_selected_row_to_df(df_user_selected_subset: pd.DataFrame, dict_user_selected_row: dict) -> pd.DataFrame:
    """Use index of selected rows (dict_user) to make subset of data (df_user) and
       return the selected subset (df_seleced)"""
    row_idx = dict_user_selected_row.selection.rows
    df_selected_to_rate = df_user_selected_subset.iloc[row_idx,:]

    return df_selected_to_rate

# 2
def load_or_init_user_db(df_user_selected_subset_show: pd.DataFrame) -> pd.DataFrame:
    """User DB two cases: use as data 1. loadet data if user in DB
                                      2. initialize a user DB"""

    loaded_data_dict = helper2.load_json("application/data/data_user/DataBase_user_changes.json")

    # 1. user in DB
    if st.session_state.username in loaded_data_dict.keys():
        return pd.DataFrame(loaded_data_dict[st.session_state.username])
    # 2. new user DB
    else:
        return pd.DataFrame(columns=df_user_selected_subset_show.columns)

# 3
def load_all_users_db() -> pd.DataFrame:
    users_db_dict = helper2.load_json(path="application/data/data_user/DataBase_user_changes.json")
    df_all_users_posts = pd.DataFrame()
    for user in users_db_dict.keys():
        df_user = pd.DataFrame(users_db_dict[user])
        df_user["User"] = user
        df_all_users_posts = pd.concat(objs=[df_all_users_posts, df_user], axis=0, ignore_index=True)
    
    return df_all_users_posts

# 4
def add_date_or_date_column(df: pd.DataFrame):
    if "Date" in df.columns:
        for idx in df.index:
            # do not overwrite existing date (in page_3: interactiv_df_users_previous_submissions_widget())
            if not df.loc[idx,"Date"]:
                df.loc[idx,"Date"] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    else:
        df["Date"] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    
    return df

# 5
def save_json(dict_for_saving, path="DataBase_user_changes.json"):
    with open(path, "w", encoding='utf-8') as file:
        json.dump(dict_for_saving, file)
    return

# 6
def load_db_add_dict_save_db(path_to_db, df_to_add: pd.DataFrame, overwrite: str=False):
    # Load data
    user_name = st.session_state.username
    user_database = helper2.load_json(path=path_to_db)
    # if user exist use db else init db
    if user_name in user_database.keys():
        df_user_database = pd.DataFrame(user_database[user_name])
    else:
        df_user_database = pd.DataFrame(columns=df_to_add.columns)
    
    # add date
    df_to_add_with_date = add_date_or_date_column(df_to_add)

    # if new post: concat, else overwrite, i.e. edit old posts
    if overwrite:
        df_user_database_all = df_to_add_with_date
    else:
        # concat(new,old) avoids dublicates. old will always win. Actually because of pd.Dataframe(df.to_dict), 
        # i.e. later rows overwrite earlier rows with same index (see testing_tests.py, search "Orig concat")
        df_user_database_all = pd.concat([df_to_add_with_date, df_user_database], axis=0)

    # df_user_database_all.drop_duplicates(inplace=True)
    # user_database[user_name] = df_to_add.to_dict()
    user_database[user_name] = df_user_database_all.to_dict()
    save_json(user_database, path=path_to_db)
    return