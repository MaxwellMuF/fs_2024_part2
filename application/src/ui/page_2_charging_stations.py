import folium  

import pandas       as pd
import streamlit    as st

from streamlit_folium       import st_folium
from branca.colormap        import LinearColormap

# Own python files
from application.src.utilities   import methods
from application.src.utilities   import helper_page_2 as helper2


# ----------------------------- streamlit widgets ------------------------------

def filter_zip_code_widget(df: pd.DataFrame) -> pd.DataFrame:
    """User select zip code widget: selectbox for zip code and returns selected subset"""
    with st.container(border=True):
        st.header(body="Charging Stations in my zip code",
                  help=st.session_state.text_for_page_2_help["filter_zip_code_widget_help"])
        user_selected_zip_code = st.selectbox(label="Only show Charging Stations in my zip code",
                                              options=helper2.unique_values_of_column(df, "PLZ"))

    return helper2.subset_with_criteria(df=df, column="PLZ", criteria=user_selected_zip_code)


def filter_power_widget(df: pd.DataFrame) -> pd.DataFrame:
    """User select power widget: checkbox and selectbox for power in two columns.
    Returns selected subset"""
    with st.container(border=True):
        st.header(body="How much power is appropriate?",
                  help=st.session_state.text_for_page_2_help["filter_power_widget_help"])
        
        col1, col2 = st.columns(2)
        with col1:
            user_criteria_50kW = st.checkbox("Only show Charging Stations with 50kW and more!")
            if user_criteria_50kW:
                df = df[df["KW"] >= 50].copy()

        with col2:
            user_selected_kw = st.selectbox(
            "Select the preferred power [kW] of your Charging Station",
            helper2.unique_values_of_column(df, "KW"))

    return helper2.subset_with_criteria(df=df, column="KW", criteria=user_selected_kw)

def spawn_heatmap_berlin_widget(df_numbers_per_kW: pd.DataFrame, df_numbers: pd.DataFrame) -> None:
    """Create folium map with given dfs containing 'KW' and 'Number' columns"""
    with st.container(border=True):
        st.header(body="Map of berlin with Charging Stations",
                  help=st.session_state.text_for_page_2_help["spawn_heatmap_berlin_help"])
        st.write("This is a map of Berlin with the number of electric charging stations per zip code")

        m = folium.Map(location=[52.52, 13.40], zoom_start=10)
        # catch case: empty df, i.e. no charging station found
        if len(df_numbers_per_kW) == 0:
            st.warning("Sorry, there is no such Charging Stations in berlin yet", icon="⚠️")
            st_folium(m, width=800, height=600)
        else:
            color_map = LinearColormap(colors=['yellow', 'red'], vmin=0, vmax=df_numbers["Number"].max(), 
                                       caption="Number of Charging Stations")
            
            # Add polygons to the map for Numbers
            for idx, row in df_numbers.iterrows():
                # make tooltip with 'sorted list of power' from selected stations
                list_kW_in_plz_sorted = helper2.list_for_tooltip(df_numbers_per_kW,column_name="PLZ",criteria=row['PLZ'])
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

def show_selected_stations_as_df_widget(df_numbers_per_kW: pd.DataFrame, df_numbers: pd.DataFrame) -> None:
    """Show selected data in three dfs: 1. per KW and per zip code in two columns
                                        2. all selected stations with adress"""
    with st.container(border=True):
        st.header(body="Summary of my zip code",
                  help=st.session_state.text_for_page_2_help["show_selected_stations_as_df_help"])

        # Show df_numbers_per_kW and df_number as st.dataframe
        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.write("Number of Charging Stations per zip code:")
            st.dataframe(helper2.drop_column_and_sort_by_column(df_numbers, ["geometry"], "Number"),
                         use_container_width=True, hide_index=True)
        with col2:
            st.write("Number of Charging Stations per kW:")
            st.dataframe(helper2.drop_column_and_sort_by_column(df_numbers_per_kW, ["geometry"], "KW"), 
                         use_container_width=True, hide_index=True)

    return

def config_edit_df_user_posts() -> dict[str:st.column_config]:
    """Define the configuration of the columns for the editable dataframes"""
    config = {
        'PLZ' : st.column_config.NumberColumn('PLZ', min_value=10115, max_value=14200, required=True, disabled=True),
        'Straße' : st.column_config.TextColumn('Straße', required=True, disabled=True), #width='medium',
        'Hausnummer' : st.column_config.TextColumn('Hausnummer', required=True, disabled=True, width='small'),
        'KW' : st.column_config.NumberColumn('KW', min_value=1, max_value=1000, disabled=True, width='small'),
        'Anzahl Ladepunkte' : st.column_config.NumberColumn('Anzahl Ladepunkte',min_value=1, max_value=10, 
                                                            disabled=True, width='small'),
        'Availability' : st.column_config.TextColumn('Availability', required=False)}
    
    return config

def calculate_number_charging_stations(df: pd.DataFrame) -> int:
    """Sum of certain column"""
    return int(df["Anzahl Ladepunkte"].sum())

def show_address_and_availibility_widget(df_user_selected_subset_show: pd.DataFrame) -> pd.DataFrame:
    """Show df_user_selected_subset_av as st.dataframe"""
    with st.container(border=True):
        st.header(body="Address and Availability",
                  help=st.session_state.text_for_page_2_help["show_address_and_availibility"])
        st.write(f"We have found {calculate_number_charging_stations(df_user_selected_subset_show)} \
                 charging stations that match your selection. Here you can see their address and availability:")
        st.dataframe(df_user_selected_subset_show, column_config=config_edit_df_user_posts(),
                     use_container_width=True, hide_index=True)

    return


# ----------------------------- streamlit page ------------------------------
# @methods.timer
def init_data(geodata_path: str="domain/data/processed_data_for_ui/geodata_berlin_plz.csv", 
              charging_data_path: str="domain/data/processed_data_for_ui/Ladesaeulenregister.csv") -> None:
    """Init and process data only ones at the start of the app (instead of every tick)"""

    df_geodat_plz = pd.read_csv(geodata_path, sep=',', low_memory=False)
    df_charging = pd.read_csv(charging_data_path, sep=',', low_memory=False)

    return helper2.merge_with_geometry(df=df_charging, df_geo=df_geodat_plz)

def init_session_states():
    """Init the streamlit session states for this page"""
    if "text_for_page_2_help" not in st.session_state:
        # because of the funny behaior of load a json into python str into streamlit md, we need to trippe '\' in '\n'
        st.session_state.text_for_page_2_help = helper2.load_json("application/data/data_ui_texts/text_for_page_2_help.json")
    if "df_charging_berlin_search" not in st.session_state:
        st.session_state.df_charging_berlin_search = init_data()

    return

# Make Heatmap of berlin with number of charging stations
def make_streamlit_page_elements(df: pd.DataFrame) -> None:
    """The sequence of streamlit elements on this page:
            Perform user selection and filter data.
            Makes heatmap of electric Charging Stations in berlin.
            And show selected data and offer post submission and save user posts."""

    # Add Available column: generate random values
    df_every_station = helper2.add_col_available(df=df, chance=[0.7,0.3])

    # Filter zip code widget
    df_user_selected_subset_zip = filter_zip_code_widget(df_every_station)

    # Filter power widget
    df_user_selected_subset_zip_power = filter_power_widget(df_user_selected_subset_zip)

    # Make grouped dfs
    df_numbers_per_kW = methods.count_plz_occurrences(df_user_selected_subset_zip_power, sort_col=['PLZ', "KW"])
    df_numbers = methods.count_plz_occurrences(df_user_selected_subset_zip_power, sort_col=('PLZ'))

    # Spawn heatmap berlin
    spawn_heatmap_berlin_widget(df_numbers_per_kW, df_numbers)

    # drop unnessesary columns for the show data part
    df_user_selected_subset_show = helper2.drop_column_and_sort_by_column(df_user_selected_subset_zip_power,
                    list_drop_column_names=["geometry"],
                    sort_column_name="KW")
    
    # Show dataframes that user has filtered
    show_selected_stations_as_df_widget(df_numbers_per_kW, df_numbers)
    show_address_and_availibility_widget(df_user_selected_subset_show)

    return

# @methods.timer
def main() -> None:
    """Main of the Charging Stations page: Make title and call init and sequence of elements"""
    init_session_states()
    st.title(body="Find a suitable Charging Station",
             help=st.session_state.text_for_page_2_help["main_help"])
    make_streamlit_page_elements(st.session_state.df_charging_berlin_search)
    
    return

# call main directly because of st.navigation
main()

# does not work with streamlit.navigation(Page)
# if __name__ == "__main__":
#     main()
