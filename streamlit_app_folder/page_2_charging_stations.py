import time
import json
import folium  

import numpy        as np
import pandas       as pd
import streamlit    as st

from streamlit_folium       import st_folium
from branca.colormap        import LinearColormap

# Own python files
from streamlit_app_folder   import methods
from streamlit_app_folder   import helper_page_2_charging_stations as helper
from streamlit_app_folder   import data_pipeline


# ----------------------------- streamlit widgets ------------------------------

def filter_zip_code_widget(df: pd.DataFrame) -> pd.DataFrame:
    """User select zip code widget: selectbox for zip code and returns selected subset"""
    with st.container(border=True):
        st.header(body="Charging Stations in my zip code",
                  help=st.session_state.text_for_page_help["filter_zip_code_widget_help"])
        user_selected_zip_code = st.selectbox(label="Only show Charging Stations in my zip code",
                                              options=helper.unique_values_of_column(df, "PLZ"))

    return helper.subset_with_criteria(df=df, column="PLZ", criteria=user_selected_zip_code)


def filter_power_widget(df: pd.DataFrame) -> pd.DataFrame:
    """User select power widget: checkbox and selectbox for power in two columns.
    Returns selected subset"""
    with st.container(border=True):
        st.header(body="How much power is appropriate?",
                  help=st.session_state.text_for_page_help["filter_power_widget_help"])
        
        col1, col2 = st.columns(2)
        with col1:
            user_criteria_50kW = st.checkbox("Only show Charging Stations with 50kW and more!")
            if user_criteria_50kW:
                df = df[df["KW"] >= 50].copy()

        with col2:
            user_selected_kw = st.selectbox(
            "Select the preferred power [kW] of your Charging Station",
            helper.unique_values_of_column(df, "KW"))

    return helper.subset_with_criteria(df=df, column="KW", criteria=user_selected_kw)

def spawn_heatmap_berlin(df_numbers_per_kW: pd.DataFrame, df_numbers: pd.DataFrame) -> None:
    """Create folium map with given dfs containing 'KW' and 'Number' columns"""
    with st.container(border=True):
        st.header(body="Map of berlin with Charging Stations",
                  help=st.session_state.text_for_page_help["spawn_heatmap_berlin_help"])
        st.write("This is a map of Berlin with the number of electric charging stations per zip code")

        m = folium.Map(location=[52.52, 13.40], zoom_start=10)
        # catch case: empty df, i.e. no charging station found
        if len(df_numbers_per_kW) == 0:
            # st.write("Sorry, there is no such Charging Stations in berlin yet")
            st.warning("Sorry, there is no such Charging Stations in berlin yet", icon="⚠️")
            st_folium(m, width=800, height=600)
        else:
            color_map = LinearColormap(colors=['yellow', 'red'], vmin=1, vmax=df_numbers["Number"].max())
            
            # Add polygons to the map for Numbers
            for idx, row in df_numbers.iterrows():
                # make tooltip with 'sorted list of power' from selected stations
                list_kW_in_plz_sorted = helper.list_for_tooltip(df_numbers_per_kW,column_name="PLZ",criteria=row['PLZ'])
                # Add PLZ with geometry to map
                folium.GeoJson(
                    row['geometry'],
                    style_function=lambda x, color=color_map(row['Number']): {
                        'fillColor': color,
                        'color': 'black',
                        'weight': 1,
                        'fillOpacity': 0.7
                    },
                    tooltip=f"PLZ: {row['PLZ']}, Number: {row['Number']}, \
                            kW: {list_kW_in_plz_sorted}"
                ).add_to(m)

            # Add color_map to the folium_map
            color_map.add_to(m)

            # Show folium_map
            st_folium(m, width=670, height=500)

    return

def show_selected_stations_as_df(df_numbers_per_kW: pd.DataFrame, df_numbers: pd.DataFrame) -> None:
    """Show selected data in three dfs: 1. per KW and per zip code in two columns
                                        2. all selected stations with adress"""
    with st.container(border=True):
        st.header(body="Summary of my zip code",
                  help=st.session_state.text_for_page_help["show_selected_stations_as_df_help"])

        # Show df_numbers_per_kW and df_number as st.dataframe
        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.write("Number of Charging Stations per zip code:")
            st.dataframe(helper.drop_column_and_sort_by_column(df_numbers, ["geometry"], "Number"),
                         use_container_width=True, hide_index=True)
        with col2:
            st.write("Number of Charging Stations per kW:")
            st.dataframe(helper.drop_column_and_sort_by_column(df_numbers_per_kW, ["geometry"], "KW"), 
                         use_container_width=True, hide_index=True)

    return

def show_address_and_availibility(df_user_selected_subset_show: pd.DataFrame) -> pd.DataFrame:
    """Show df_user_selected_subset_av as st.dataframe"""
    with st.container(border=True):
        st.header(body="Address and Availability",
                  help=st.session_state.text_for_page_help["show_address_and_availibility"])
        st.write("All Charging Stations you have selected with their address and availability:")
        st.dataframe(df_user_selected_subset_show, use_container_width=True, hide_index=True)

    return 

def init_user_db_if_needed(df_user_selected_subset_show: pd.DataFrame) -> pd.DataFrame:
    """User DB three cases: use as data 1. use session_state or
                                        2. load json or 
                                        3. initialize a user DB)"""
    # 1. use session_state as user DB
    if "df_stations_user_edit" in st.session_state:
        return st.session_state.df_stations_user_edit
    else:
        with open("DataBase_user_changes.json", "r") as file:
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
        'Rating' : st.column_config.SelectboxColumn('Rating', options=list(range(1,6)), width='small'),
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
            helper.load_db_add_dict_save_db(path_to_db="DataBase_user_changes.json", df_to_add=df_stations_user_edit)
            st.write("We have saved your post. Thank you for your support!")
            time.sleep(3)
            st.rerun()
    return

# ----------------------------- streamlit page ------------------------------

# Make Heatmap of berlin with number of charging stations
# @methods.timer
def make_streamlit_page_elements(df: pd.DataFrame) -> None:
    """The sequence of streamlit elements on this page:
            Perform user selection and filter data.
            Makes heatmap of electric Charging Stations in berlin.
            And show selected data and offer post submission and save user posts."""

    if "text_for_page_help" not in st.session_state:
        # because of the funny behaior of load a json into python str into streamlit md, we need to trippe '\' in '\n'
        st.session_state.text_for_page_help = helper.load_json("text_for_page_help.json")
    # Add Available column: generate random values
    df_every_station = helper.add_col_available(df=df, chance=[0.7,0.3])

    # Filter zip code widget
    df_user_selected_subset = filter_zip_code_widget(df_every_station)

    # Filter power widget
    df_user_selected_subset = filter_power_widget(df_user_selected_subset)

    # Make grouped dfs
    df_numbers_per_kW = methods.count_plz_occurrences(df_user_selected_subset, sort_col=['PLZ', "KW"])
    df_numbers = methods.count_plz_occurrences(df_user_selected_subset, sort_col=('PLZ'))

    # Spawn heatmap berlin
    spawn_heatmap_berlin(df_numbers_per_kW, df_numbers)

    # drop unnessesary columns for the show data part
    df_user_selected_subset_show = helper.drop_column_and_sort_by_column(df_user_selected_subset,
                    list_drop_column_names=["geometry", "Breitengrad", "Längengrad", "Bundesland", "Ort", "Plug Types"],
                    sort_column_name="KW")
    
    # Show dataframes that user has filtered
    show_selected_stations_as_df(df_numbers_per_kW, df_numbers)
    show_address_and_availibility(df_user_selected_subset_show)

    # Load or init user DB
    df_user_changes = init_user_db_if_needed(df_user_selected_subset_show)

    # Spawn interactiv df for user comments
    spawn_interactiv_df_for_user_comment(df_user_changes)
    return

# @methods.timer
def init_data(geodata_path: str="data/datasets/geodata_berlin_plz.csv", 
              charging_data_path: str="data/datasets/Ladesaeulenregister.csv") -> None:
    """Init and process data only ones at the start of the app (instead of every tick)"""
    if "df_charging_berlin" not in st.session_state:
        df_geodat_plz = pd.read_csv(geodata_path, sep=';', low_memory=False)
        df_charging = pd.read_csv(charging_data_path, sep=';', low_memory=False)
        st.session_state.df_charging_berlin = data_pipeline.data_process(df_geodat_plz, df_charging)
    return

# @methods.timer
def main() -> None:
    """Main of the Charging Stations page: 
            Load and process data and save it as streamlit state.
            Makes heatmap of electric Charging Stations in berlin.
            And show selected data and submit and save user posts."""
    
    st.title(body="Find a suitable Charging Station",
             help="On this page you will find the charging station search. \
                  You can also write comments and add new charging stations. \
                  Look out for the question marks to find out more about each box.")
    init_data()
    make_streamlit_page_elements(st.session_state.df_charging_berlin)
    return

# call main directly because of st.navigation
main()

# does not work with streamlit.navigation(Page)
# if __name__ == "__main__":
#     main()
