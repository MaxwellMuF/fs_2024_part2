import time
import json

import numpy        as np
import pandas       as pd
import streamlit    as st

# from datetime       import datetime
# Own python files
# from application.src.utilities          import methods
from application.src.utilities          import helper_page_2 as helper2
from application.src.utilities          import helper_page_3 as helper3
from infrastructure.src.data_process    import data_pipeline



# ----------------------------- streamlit widgets ------------------------------

def filter_zip_code_widget(df: pd.DataFrame) -> pd.DataFrame:
    """User filter widget: selectbox for zip code and street. Returns selected subset"""
    with st.container(border=True):
        st.header(body="Charging Stations in my zip code",
                  help=st.session_state.text_for_page_3_help["filter_zip_code_widget_help"])
        
        # Filter zip code
        user_selected_zip_code = st.selectbox(label="Filter one zip code:",
                                              options=helper2.unique_values_of_column(df, "PLZ"))
        df_subset_user_zip_code = helper2.subset_with_criteria(df=df, column="PLZ", criteria=user_selected_zip_code)

        # Filter street
        user_selected_street = st.selectbox(label="Filter one street:",
                                              options=helper2.unique_values_of_column(df_subset_user_zip_code, "Straße"))
        df_subset_user_street = helper2.subset_with_criteria(df=df_subset_user_zip_code, column="Straße", 
                                                            criteria=user_selected_street)

        # make subset data to show it
        df_user_selected_subset_show = helper2.drop_column_and_sort_by_column(df_subset_user_street,
                    list_drop_column_names=["geometry", "Breitengrad", "Längengrad", "Bundesland"],
                    sort_column_name="KW")
        df_user_selected_subset_show.drop_duplicates(inplace=True)

        st.write("Here is your filtered data frame:")
        dict_user_selected_row = show_user_selected_df(df_user_selected_subset_show)
        df_selected_to_rate = helper3.user_selected_row_to_df(df_user_selected_subset_show, dict_user_selected_row)

    return df_selected_to_rate

def show_user_selected_df(df_user_selected_subset_show: pd.DataFrame) -> dict:
    """Show data frame and return the rows that the user has selected"""
    dict_user_selected_row = st.dataframe(df_user_selected_subset_show, use_container_width=True, 
                                          hide_index=True, on_select="rerun")
    
    return dict_user_selected_row


def config_edit_df_user_posts() -> dict[str:st.column_config]:
    """Define the configuration of the columns for the editable dataframes"""
    config = {
        'PLZ' : st.column_config.NumberColumn('PLZ', min_value=10115, max_value=14200, required=True, disabled=True),
        'Straße' : st.column_config.TextColumn('Straße', required=True, disabled=True), #width='medium',
        'Hausnummer' : st.column_config.TextColumn('Hausnummer', required=True, disabled=True, width='small'),
        'KW' : st.column_config.NumberColumn('KW', min_value=1, max_value=1000, disabled=True, width='small'),
        'Anzahl Ladepunkte' : st.column_config.NumberColumn('Anzahl Ladepunkte',min_value=1, max_value=10, 
                                                            disabled=True, width='small'),
        'Rating' : st.column_config.SelectboxColumn('Rating', options=["⭐"*i for i in range(1,6)], width=105),
        'Comment' : st.column_config.TextColumn('Comment', required=False),
        'Date' : st.column_config.TextColumn('Date', required=False, disabled=True)}
    
    return config

def interactiv_df_for_user_comment_widget(df_user_changes: pd.DataFrame) -> None:
    """Spawn interactiv df for user posts: 
            1. Create config
            2. Spawn interactiv dataframe
            3. Spawn submit button
            4. If submitted, save data in user DB
            """
    # 1. Define config for interactiv df with st.column_config
    config = config_edit_df_user_posts()

    # Create container user post
    with st.container(border=True):
        st.header(body="Rate and comment on your selection",
                  help=st.session_state.text_for_page_3_help["interactiv_df_for_user_comment_widget_help"])
        st.write("You can leave a recommendation or a comment for an selection recommendation:")
        
        # 2. Spawn interactiv df
        df_user_changes["Rating"] = [""] * len(df_user_changes)
        df_user_changes["Comment"] = [""] * len(df_user_changes)

        if len(df_user_changes) == 0:
            df_stations_user_edit = st.data_editor(df_user_changes,
                                                   use_container_width=True, hide_index=True, num_rows='fixed')
        else:
            df_stations_user_edit = st.data_editor(df_user_changes, column_config=config,
                                                   use_container_width=True, hide_index=True, num_rows='fixed')

        # 4. Spawn button to submit
        if st.button("Submit post", key="submited_post"):
            # Save post if submitted: add post to DB and save DB
            helper2.load_db_add_dict_save_db(path_to_db="application/data/data_user/DataBase_user_changes.json", 
                                            df_to_add=df_stations_user_edit)
            st.success("We have saved your post. Thank you for your support!", icon=":material/save:")
            time.sleep(3)
            st.rerun()

    return

def interactiv_df_users_previous_submissions_widget(df_user_comment_submitted: pd.DataFrame) -> None:
    """Spawn interactiv df for user posts: 
            1. Create config
            2. Spawn interactiv dataframe from loaded user DB
            3. Spawn submit button
            4. If submitted, save data in user DB
            """
    # 1. Define config for interactiv df with st.column_config
    config = config_edit_df_user_posts()

    # Create container user post
    with st.container(border=True):
        st.header(body="Your previous submissions", 
                  help=st.session_state.text_for_page_3_help["interactiv_df_users_previous_submissions_widget_help"])
        st.write("Do you want to change them? No Problem! Just make your modifications below and submit it.")
        
        # 2. Spawn interactiv df
        if df_user_comment_submitted.empty:
            df_user_rate_data_base = st.data_editor(df_user_comment_submitted, key="unused_df_edit",
                                                   use_container_width=True, hide_index=True, num_rows='fixed')
        else:
            df_user_rate_data_base = st.data_editor(df_user_comment_submitted, column_config=config, key="unused_df_edit",
                                                   use_container_width=True, hide_index=True, num_rows='dynamic')

        # 4. Spawn button to submit
        if st.button("Submit post", key="submited_post_changes"):
            # Save post if submitted: add post to DB and save DB
            helper2.load_db_add_dict_save_db(path_to_db="application/data/data_user/DataBase_user_changes.json", 
                                            df_to_add=df_user_rate_data_base,
                                            overwrite=True)
            st.success("We have saved your post. Thank you for your support!", icon=":material/save:")
            time.sleep(3)
            st.rerun()

    return

def all_users_submissions_widget():
    """Load user DBs and show them as one dataframe"""
    # data process
    df_all_users_posts = helper3.load_all_users_db()

    # steamlit elemets
    with st.container(border=True):
        st.header(body="Other users recommendations")
        st.dataframe(df_all_users_posts, column_config=config_edit_df_user_posts(), use_container_width=True,
                     hide_index=True)
        
    return 
# ----------------------------- streamlit page ------------------------------

def init_data(geodata_path: str="infrastructure/data/datasets/geodata_berlin_plz.csv", 
              charging_data_path: str="infrastructure/data/datasets/Ladesaeulenregister.csv") -> None:
    """Init and process data only ones at the start of the app (instead of every tick)"""
    if "df_charging_berlin_rate" not in st.session_state:
        df_geodat_plz = pd.read_csv(geodata_path, sep=';', low_memory=False)
        df_charging = pd.read_csv(charging_data_path, sep=',', low_memory=False)
        required_columns = ('Postleitzahl', 'Straße', 'Hausnummer', 'Anzahl Ladepunkte', 'Breitengrad', 'Bundesland',
                            'Längengrad', 'Nennleistung Ladeeinrichtung [kW]')

    return data_pipeline.data_process(df_geodat_plz, df_charging, required_columns)

def make_streamlit_page_elements(df_every_station: pd.DataFrame) -> None:

    # filter and drop and show
    df_user_selected_subset = filter_zip_code_widget(df_every_station)
   
    # Spawn interactiv df for user comment
    interactiv_df_for_user_comment_widget(df_user_selected_subset)

    # Load or init user DB
    df_user_db = helper3.load_or_init_user_db(df_user_selected_subset)

    # Spawn interactiv df show and change previous submissions
    interactiv_df_users_previous_submissions_widget(df_user_db)

    # Show all user submissions
    all_users_submissions_widget()

    return

def main() -> None:
    """Main of the Charging Stations page: 
            Load and process data and save it as streamlit state.
            Makes heatmap of electric Charging Stations in berlin.
            And show selected data and submit and save user posts."""
    if "text_for_page_3_help" not in st.session_state:
        # because of the funny behaior of load a json into python str into streamlit md, we need to trippe '\' in '\n'
        st.session_state.text_for_page_3_help = helper2.load_json("application/data/data_ui/text_for_page_3_help.json")

    st.title(body="Rate your Charging Station",
             help=st.session_state.text_for_page_3_help["main_help"])
    if "df_charging_berlin_rate" not in st.session_state:
        st.session_state.df_charging_berlin_rate = init_data()
    make_streamlit_page_elements(st.session_state.df_charging_berlin_rate)
    return

# call main directly because of st.navigation
main()