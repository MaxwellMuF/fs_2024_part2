import time
import json

import numpy        as np
import pandas       as pd
import streamlit    as st

# Own python files
from application.src.utilities   import methods
from application.src.utilities   import helper_page_2_charging_stations as helper



# ----------------------------- streamlit widgets ------------------------------

def init_user_db_if_needed(df_user_selected_subset_show: pd.DataFrame) -> pd.DataFrame:
    """User DB three cases: use as data 1. use session_state or
                                        2. load json or 
                                        3. initialize a user DB)"""
    # 1. use session_state as user DB
    if "df_stations_user_edit" in st.session_state:
        return st.session_state.df_stations_user_edit
    else:
        with open("application\data\data_user\DataBase_user_changes.json", "r") as file:
            loaded_database = json.load(file)
    # 2. use loaded json as user DB
    if st.session_state.username in loaded_database.keys():
        return pd.DataFrame(loaded_database[st.session_state.username])
    # 3. initialize a new user DB
    else:

        return pd.DataFrame(columns=df_user_selected_subset_show.columns.to_list()+["Rating", "Comment"])

def config_edit_df_user_posts() -> dict:
    config = {
        'PLZ' : st.column_config.NumberColumn('PLZ', min_value=10115, max_value=14200, required=True), #width='large',
        'Straße' : st.column_config.TextColumn('Straße', required=True), #width='medium',
        'Hausnummer' : st.column_config.TextColumn('Hausnummer', required=True, width='small'),
        'KW' : st.column_config.NumberColumn('KW', min_value=1, max_value=1000, width='small'),
        'Available' : st.column_config.SelectboxColumn('Available', options=["✔️", "❌"], width='small'),
        'Rating' : st.column_config.SelectboxColumn('Rating', options=["⭐"*i for i in range(1,6)], width=105),
        'Comment' : st.column_config.TextColumn('Comment')}
    
    return config

def spawn_interactiv_df_for_user_comment(df_user_changes: pd.DataFrame) -> None:
    """Spawn interactiv df for user posts: 
            1. Create config
            2. Spawn interactiv dataframe
            3. Show post bevor submit it
            4. Submit post, i.e. save it in user DB
            """
        # 1. Define config for interactiv df with st.column_config
    config = config_edit_df_user_posts()

            # Create container user post
    with st.container(border=True):
        st.header("Do you want to add a Charging Station or leave a comment?")
        st.write("Tank you for helping the project and other users! Here you can add \
                a new Charging Station? You can also leave a recommendation or a comment for an existing recommendation:")
        
        # 2. Spawn interactiv df
        df_stations_user_edit = st.data_editor(df_user_changes, column_config=config,
                                               use_container_width=True, hide_index=True, num_rows='dynamic')

            	# Reload page iusse solution: save it in a session state
        st.session_state.df_stations_user_edit = df_stations_user_edit

        # 3. Spawn button to check post bevor submit
        if st.button('Get results'):
            st.write("Here is your post. You can change it at any time.")
            st.dataframe(df_stations_user_edit)

        # 4. Spawn button to submit
            if st.button("Submit post", key="submited_post"):
                st.write("We have saved your post. Thank you for your support!")

            # Save post if submitted: add post to DB and save DB
        elif st.session_state.submited_post == True:
            helper.load_db_add_dict_save_db(path_to_db="application\data\data_user\DataBase_user_changes.json", 
                                            df_to_add=df_stations_user_edit)
            st.write("We have saved your post. Thank you for your support!")
            time.sleep(3)
            st.rerun()

    return
# ----------------------------- streamlit page ------------------------------

def make_streamlit_page_elements(df_user_selected_subset_show: pd.DataFrame) -> None:
    # Load or init user DB
    df_user_changes = init_user_db_if_needed(df_user_selected_subset_show)

    # Spawn interactiv df for user comments
    spawn_interactiv_df_for_user_comment(df_user_changes)

def main() -> None:
    """Main of the Charging Stations page: 
            Load and process data and save it as streamlit state.
            Makes heatmap of electric Charging Stations in berlin.
            And show selected data and submit and save user posts."""
    
    st.title(body="Rate and comment Charging Station",
             help="On this page you will find the charging station search. \
                  You can also write comments and add new charging stations. \
                  Look out for the question marks to find out more about each box.")
    
    make_streamlit_page_elements(st.session_state.df_charging_berlin)
    return

# call main directly because of st.navigation
main()