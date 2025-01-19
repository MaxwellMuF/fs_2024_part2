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
    if "df_charging_berlin_rate" not in st.session_state:
        df_geodat_plz = pd.read_csv(geodata_path, sep=';', low_memory=False)
        df_charging = pd.read_csv(charging_data_path, sep=';', low_memory=False)
        required_columns = ('Postleitzahl', 'Straße', 'Hausnummer', 'Anzahl Ladepunkte', 'Breitengrad', 'Bundesland',
                            'Längengrad', 'Nennleistung Ladeeinrichtung [kW]')
        df_processed_data = data_pipeline.data_process(df_geodat_plz, df_charging, required_columns)
        st.session_state.df_charging_berlin_rate = df_processed_data
    return # df_processed_data # return just for testin, user session_state to avoid data process at any click

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
                    list_drop_column_names=["geometry", "Breitengrad", "Längengrad", "Bundesland"],
                    sort_column_name="KW")
        df_user_selected_subset_show.drop_duplicates(inplace=True)

        st.write("Here is your filtered data frame:")
        dict_user_selected_row = show_user_selected_df(df_user_selected_subset_show)
        df_selected_to_rate = user_selected_row_to_df(df_user_selected_subset_show, dict_user_selected_row)
        # st.write("Here are your selected rows:")
        # st.dataframe(df_selected_to_rate, use_container_width=True, hide_index=True,)

    return df_selected_to_rate

def show_user_selected_df(df_user_selected_subset_show: pd.DataFrame) -> dict:
    dict_user_selected_row = st.dataframe(df_user_selected_subset_show, use_container_width=True, hide_index=True, on_select="rerun")
    
    return dict_user_selected_row

def user_selected_row_to_df(df_user_selected_subset: pd.DataFrame, dict_user_selected_row: dict) -> pd.DataFrame:
    row_idx = dict_user_selected_row.selection.rows
    df_selected_to_rate = df_user_selected_subset.iloc[row_idx,:]

    return df_selected_to_rate


def init_user_db_if_needed(df_user_selected_subset_show: pd.DataFrame) -> pd.DataFrame:
    """User DB three cases: use as data 1. use session_state or
                                        2. load json or 
                                        3. initialize a user DB)"""
    # # 1. use session_state as user DB
    # if "df_user_rate_data_base" in st.session_state:
    #     return st.session_state.df_user_rate_data_base
    # else:
    with open("application/data/data_user/DataBase_user_changes.json", "r") as file:
        loaded_database = json.load(file)
    # 2. use loaded json as user DB
    if st.session_state.username in loaded_database.keys():
        return pd.DataFrame(loaded_database[st.session_state.username])
    # 3. initialize a new user DB
    else:

        return pd.DataFrame(columns=df_user_selected_subset_show)

def config_edit_df_user_posts() -> dict:
    config = {
        'PLZ' : st.column_config.NumberColumn('PLZ', min_value=10115, max_value=14200, required=True), #width='large',
        'Straße' : st.column_config.TextColumn('Straße', required=True), #width='medium',
        'Hausnummer' : st.column_config.TextColumn('Hausnummer', required=True, width='small'),
        'KW' : st.column_config.NumberColumn('KW', min_value=1, max_value=1000, width='small'),
        'Anzahl Ladepunkte' : st.column_config.NumberColumn('Anzahl Ladepunkte',min_value=1, max_value=10, width='small'),
        'Rating' : st.column_config.SelectboxColumn('Rating', options=["⭐"*i for i in range(1,6)], width=105),
        'Comment' : st.column_config.TextColumn('Comment', required=False)}
    
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
        st.header("Rate and comment on your selection")
        st.write("Tank you for helping the project and other users! Here you can add \
                a new Charging Station? You can also leave a recommendation or a comment for an existing recommendation:")
        
        # 2. Spawn interactiv df
        df_user_changes["Rating"] = [""] * len(df_user_changes)
        df_user_changes["Comment"] = [""] * len(df_user_changes)

        if len(df_user_changes) == 0:
            df_stations_user_edit = st.data_editor(df_user_changes,
                                                   use_container_width=True, hide_index=True, num_rows='dynamic')
        else:
            df_stations_user_edit = st.data_editor(df_user_changes, column_config=config,
                                                   use_container_width=True, hide_index=True, num_rows='dynamic')

        # 4. Spawn button to submit
        if st.button("Submit post", key="submited_post"):
            # Save post if submitted: add post to DB and save DB
            helper.load_db_add_dict_save_db(path_to_db="application/data/data_user/DataBase_user_changes.json", 
                                            df_to_add=df_stations_user_edit)
            st.success("We have saved your post. Thank you for your support!", icon=":material/save:")
            time.sleep(3)
            st.rerun()

    return

def spawn_interactiv_df_for_user_comment_previous_submissions(df_user_comment_submitted: pd.DataFrame) -> None:
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
        st.header("Your previous submissions")
        st.write("Do you want to change them? No Problem! Just make your modifications below and submit it.")
        
        # 2. Spawn interactiv df
        if df_user_comment_submitted.empty:
            df_user_rate_data_base = st.data_editor(df_user_comment_submitted, key="unused_df_edit",
                                                   use_container_width=True, hide_index=True, num_rows='dynamic')
        else:
            df_user_rate_data_base = st.data_editor(df_user_comment_submitted, column_config=config, key="unused_df_edit",
                                                   use_container_width=True, hide_index=True, num_rows='dynamic')

        # Reload page iusse solution: save it in a session state
        # st.session_state.df_user_rate_data_base = df_user_rate_data_base

        # # 3. Spawn button to check post bevor submit
        # if st.button("Get results", key="unused_get_res_2"):
        #     st.write("Here is your post. You can change it at any time.")
        #     st.dataframe(df_user_rate_data_base)

        # 4. Spawn button to submit
        if st.button("Submit post", key="submited_post_changes"):
            # Save post if submitted: add post to DB and save DB
            helper.load_db_add_dict_save_db(path_to_db="application/data/data_user/DataBase_user_changes.json", 
                                            df_to_add=df_user_rate_data_base)
            st.success("We have saved your post. Thank you for your support!", icon=":material/save:")
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

    
    if "text_for_page_help" not in st.session_state:
        # because of the funny behaior of load a json into python str into streamlit md, we need to trippe '\' in '\n'
        st.session_state.text_for_page_help = helper.load_json("application/data/data_ui/text_for_page_help.json")

    # filter and drop and show
    df_user_selected_subset = filter_zip_code_widget(df_every_station)
   


    # Spawn interactiv df for user comment
    spawn_interactiv_df_for_user_comment(df_user_selected_subset)

    # Load or init user DB
    df_user_db = init_user_db_if_needed(df_user_selected_subset)

    # Spawn interactiv df show and change previous submissions
    spawn_interactiv_df_for_user_comment_previous_submissions(df_user_db)

    return

def main() -> None:
    """Main of the Charging Stations page: 
            Load and process data and save it as streamlit state.
            Makes heatmap of electric Charging Stations in berlin.
            And show selected data and submit and save user posts."""
    
    st.title(body="Rate and comment Charging Station",
             help="On this page you will find the charging station search. \
                  You can also write comments and add new charging stations. \
                  Look out for the question marks to find out more about each box.")
    init_data()
    make_streamlit_page_elements(st.session_state.df_charging_berlin_rate)
    return

# call main directly because of st.navigation
main()