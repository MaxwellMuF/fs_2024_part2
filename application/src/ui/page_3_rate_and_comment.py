import time
import json

import numpy        as np
import pandas       as pd
import streamlit    as st

# Own python files
# from application.src.utilities          import methods
from application.src.utilities          import helper_page_2_charging_stations as helper
from infrastructure.src.data_process    import data_pipeline



# ----------------------------- streamlit widgets ------------------------------

def init_data(geodata_path: str="infrastructure/data/datasets/geodata_berlin_plz.csv", 
              charging_data_path: str="infrastructure/data/datasets/Ladesaeulenregister.csv") -> None:
    """Init and process data only ones at the start of the app (instead of every tick)"""
    if "df_charging_berlin" not in st.session_state:
        df_geodat_plz = pd.read_csv(geodata_path, sep=';', low_memory=False)
        df_charging = pd.read_csv(charging_data_path, sep=';', low_memory=False)
        st.session_state.df_charging_berlin = data_pipeline.data_process(df_geodat_plz, df_charging)
        
    return

def filter_zip_code_widget(df: pd.DataFrame) -> pd.DataFrame:
    """User select zip code widget: selectbox for zip code and returns selected subset"""
    with st.container(border=True):
        st.header(body="Charging Stations in my zip code",
                  help=st.session_state.text_for_page_help["filter_zip_code_widget_help"])
        user_selected_zip_code = st.selectbox(label="Only show Charging Stations in my zip code",
                                              options=helper.unique_values_of_column(df, "PLZ"))
        df_subset_user_zip_code = helper.subset_with_criteria(df=df, column="PLZ", criteria=user_selected_zip_code)

        user_selected_street = st.selectbox(label="Only show Charging Stations in that street",
                                              options=helper.unique_values_of_column(df_subset_user_zip_code, "Straße"))
        df_subset_user_street = helper.subset_with_criteria(df=df_subset_user_zip_code, column="Straße", criteria=user_selected_street)

        df_user_selected_subset_show = helper.drop_column_and_sort_by_column(df_subset_user_street,
                    list_drop_column_names=["geometry", "Breitengrad", "Längengrad", "Bundesland", "Ort", "Plug Types"],
                    sort_column_name="KW")
        
        st.dataframe(df_user_selected_subset_show, use_container_width=True, hide_index=True)

    return df_user_selected_subset_show

def init_user_db_if_needed(df_user_selected_subset_show: pd.DataFrame) -> pd.DataFrame:
    """User DB three cases: use as data 1. use session_state or
                                        2. load json or 
                                        3. initialize a user DB)"""
    # 1. use session_state as user DB
    if "df_stations_user_edit" in st.session_state:
        return st.session_state.df_stations_user_edit
    else:
        with open("application/data/data_user/DataBase_user_changes.json", "r") as file:
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
            helper.load_db_add_dict_save_db(path_to_db="application/data/data_user/DataBase_user_changes.json", 
                                            df_to_add=df_stations_user_edit)
            st.write("We have saved your post. Thank you for your support!")
            time.sleep(3)
            st.rerun()

    return

def show_address_and_availibility(df_user_selected_subset_show: pd.DataFrame) -> pd.DataFrame:
    """Show df_user_selected_subset_av as st.dataframe"""
    with st.container(border=True):
        st.header(body="Address and Availability",
                  help=st.session_state.text_for_page_help["show_address_and_availibility"])
        st.write("All Charging Stations you have selected with their address and availability:")
        st.dataframe(df_user_selected_subset_show, use_container_width=True, hide_index=True)

    return
# ----------------------------- streamlit page ------------------------------

def make_streamlit_page_elements(df_every_station: pd.DataFrame) -> None:

    # filter and drop and show
    df_user_selected_subset = filter_zip_code_widget(df_every_station)
    # df_user_selected_subset_show = helper.drop_column_and_sort_by_column(df_user_selected_subset,
    #                 list_drop_column_names=["geometry", "Breitengrad", "Längengrad", "Bundesland", "Ort", "Plug Types"],
    #                 sort_column_name="KW")
    #show_address_and_availibility(df_user_selected_subset_show)

    # Load or init user DB
    df_user_changes = init_user_db_if_needed(df_user_selected_subset)
    st.write("Here are the selected Charging Stations")
    # Spawn interactiv df for user comment
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