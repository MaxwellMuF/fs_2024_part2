import time
import json
import folium  

import numpy        as np
import pandas       as pd
import streamlit    as st

from streamlit_folium       import st_folium
from branca.colormap        import LinearColormap

# Own python files
from application.src.utilities   import methods
from application.src.utilities   import helper_page_2_charging_stations as helper
from infrastructure.src.data_process   import data_pipeline, data_pipeline_residents


# ----------------------------- streamlit widgets ------------------------------


def spawn_heatmap_berlin(df_map_show: pd.DataFrame, column_show: str) -> None:
    """Create folium map with given dfs containing 'KW' and 'Number' columns"""

    m = folium.Map(location=[52.52, 13.40], zoom_start=10)
    # catch case: empty df, i.e. no charging station found
    if len(df_map_show) == 0:
        # st.write("Sorry, there is no such Charging Stations in berlin yet")
        st.warning("Sorry, there is no such Charging Stations in berlin yet", icon="⚠️")
        st_folium(m, width=800, height=600)
    else:
        color_map = LinearColormap(colors=['yellow', 'red'], vmin=df_map_show[column_show].min(),
                                                             vmax=df_map_show[column_show].max())
        
        # Add polygons to the map for Numbers
        for idx, row in df_map_show.iterrows():
            # Add PLZ with geometry to map
            folium.GeoJson(
                row['geometry'],
                style_function=lambda x, color=color_map(row[column_show]): {
                    'fillColor': color,
                    'color': 'black',
                    'weight': 1,
                    'fillOpacity': 0.7
                },
                tooltip=f"PLZ: {row['PLZ']}, {column_show}: {row[column_show]}"
            ).add_to(m)

        # Add color_map to the folium_map
        color_map.add_to(m)

        # Show folium_map
        st_folium(m, width=670, height=500)

    return

def radio_selectors(df_charging: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    # Make two columns with radio selectors
    col1, col2 = st.columns(2)
    with col1:
        selected_df = st.radio("Select DataFrame",  ("Residents", "Charging_Stations", "Density"))
    with col2:
        selected_filter = st.radio("Filter",  ("All", "Slow Charger only", "Fast Charger only"))

    if selected_filter == "Slow Charger only":
        df_charging = df_charging[df_charging["Art der Ladeeinrichung"] == "Normalladeeinrichtung"]
    elif selected_filter == "Fast Charger only":
        df_charging = df_charging[df_charging["Art der Ladeeinrichung"] == "Schnellladeeinrichtung"]
    
    return df_charging, selected_df
        
def make_density_df(df_charging_numbers: pd.DataFrame, df_residents: pd.DataFrame) -> pd.DataFrame:
    # Make df_density
    df_density = df_charging_numbers.merge(df_residents.drop("geometry", axis=1), how='left', on="PLZ")
    df_density["Density"] = df_density["Einwohner"] / df_density["Number"]

    # Make reciprocal of the density
    if st.checkbox(label="Reciprocal Density", 
                    help="Not checked: Show residents per charging station (Where are few stations)\
                            \nChecked: Show charging stations per inhabitant (Where are many stations)"):
        df_density.loc[:,"Density"] = df_density["Density"].rdiv(1).round(5)
    else:
        df_density = df_density.round(0)
    
    return df_density

def select_show_df(selected_df: str, df_charging_numbers: pd.DataFrame, df_residents: pd.DataFrame, 
                   df_density: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    if selected_df == "Charging_Stations":
        df_map_show = df_charging_numbers
        column_show = "Number"

    elif selected_df == "Residents":
        df_map_show = df_residents
        column_show = "Einwohner"
    
    elif selected_df == "Density":
        df_map_show = df_density
        column_show = "Density"

    return df_map_show, column_show
    

def show_address(df: pd.DataFrame) -> pd.DataFrame:
    """Show df_user_selected_subset_av as st.dataframe"""
    with st.container(border=True):
        st.header(body="Selected Charing Stations",
                  help=st.session_state.text_for_page_help["show_address_and_availibility"])
        st.write("All Charging Stations you have selected with their address:")
        st.dataframe(df, column_order=["PLZ", "Straße", "Hausnummer", "KW", "Art der Ladeeinrichung",
                                       "Density", "Number", "Einwohner"],
                     use_container_width=True, hide_index=True)

    return

# ----------------------------- streamlit page ------------------------------

# Make Heatmap of berlin with number of charging stations
# @methods.timer
def make_streamlit_page_elements(df_charging: pd.DataFrame, df_residents: pd.DataFrame) -> None:
    """The sequence of streamlit elements on this page:
            Perform user selection and filter data.
            Makes heatmap of electric Charging Stations in berlin.
            And show selected data and offer post submission and save user posts."""

    if "text_for_page_help" not in st.session_state:
        # because of the funny behaior of load a json into python str into streamlit md, we need to trippe '\' in '\n'
        st.session_state.text_for_page_help = helper.load_json("application/data/data_ui/text_for_page_help.json")

    # df_charging_numbers = methods.count_plz_occurrences(df_charging, sort_col=('PLZ'))

    # df_density = df_charging_numbers.merge(df_residents.drop("geometry", axis=1), how='left', on="PLZ")
    # df_density["Density"] = df_density["Einwohner"] / df_density["Number"]
    # df_density["Density"] = df_density["Density"].round(5)
    # print(df_density.columns)

    with st.container(border=True):
        st.header(body="Map of berlin with Charging Stations",
                  help=st.session_state.text_for_page_help["spawn_heatmap_berlin_help"])
        st.write("This is a map of Berlin with the number of electric charging stations per zip code")


        df_charging, selected_df = radio_selectors(df_charging)
        # # Make two columns with radio selectors
        # col1, col2 = st.columns(2)
        # with col1:
        #     selected_df = st.radio("Select DataFrame",  ("Residents", "Charging_Stations", "Density"))
        # with col2:
        #     selected_filter = st.radio("Filter",  ("All", "Slow Charger only", "Fast Charger only"))

        # if selected_filter == "Slow Charger only":
        #     df_charging = df_charging[df_charging["Art der Ladeeinrichung"] == "Normalladeeinrichtung"]
        # elif selected_filter == "Fast Charger only":
        #     df_charging = df_charging[df_charging["Art der Ladeeinrichung"] == "Schnellladeeinrichtung"]
        

        df_charging_numbers = methods.count_plz_occurrences(df_charging, sort_col=('PLZ'))

        df_density = make_density_df(df_charging_numbers, df_residents)
        # # Make df_density
        # df_density = df_charging_numbers.merge(df_residents.drop("geometry", axis=1), how='left', on="PLZ")
        # df_density["Density"] = df_density["Einwohner"] / df_density["Number"]

        # # Make reciprocal of the density
        # if st.checkbox(label="Reciprocal Density", 
        #                help="Not checked: Show residents per charging station (Where are few stations)\
        #                      \nChecked: Show charging stations per inhabitant (Where are many stations)"):
        #     df_density.loc[:,"Density"] = df_density["Density"].rdiv(1).round(5)

        # if selected_df == "Charging_Stations":
        #     df_map_show = df_charging_numbers
        #     column_show = "Number"

        # elif selected_df == "Residents":
        #     df_map_show = df_residents
        #     column_show = "Einwohner"
        
        # elif selected_df == "Density":
        #     df_map_show = df_density
        #     column_show = "Density"

        df_map_show, column_show = select_show_df(selected_df, df_charging_numbers, df_residents, df_density)

        spawn_heatmap_berlin(df_map_show, column_show)

    show_address(df_charging)
    show_address(df_density)

    return


# @methods.timer
def init_data(geodata_path: str="infrastructure/data/datasets/geodata_berlin_plz.csv", 
              charging_data_path: str="infrastructure/data/datasets/Ladesaeulenregister.csv",
              residents_path: str="infrastructure/data/datasets/plz_einwohner.csv") -> None:
    """Init and process data only ones at the start of the app (instead of every tick)"""

    df_geodat_plz = pd.read_csv(geodata_path, sep=';', low_memory=False)
    df_charging = pd.read_csv(charging_data_path, sep=',', low_memory=False)
    df_plz_res = pd.read_csv(residents_path, sep=",", low_memory=False)
    charging_required_columns = ('Postleitzahl', 'Breitengrad','Längengrad','Bundesland', 'Straße', 'Hausnummer',
                                'Ort', 'Nennleistung Ladeeinrichtung [kW]', "Art der Ladeeinrichung")
    
    # apply data process
    df_charging = data_pipeline.data_process(df_geodat_plz, df_charging, charging_required_columns)
    df_residents = data_pipeline_residents.data_process_res(df_geodat_plz, df_plz_res)

    return df_charging, df_residents
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
    
    if "df_charging_berlin_search" not in st.session_state:
        st.session_state.df_charging_berlin_search = init_data()[0]
    if "df_residents_new_stations" not in st.session_state:
        st.session_state.df_residents_new_stations = init_data()[1]
        
    make_streamlit_page_elements(st.session_state.df_charging_berlin_search,
                                 st.session_state.df_residents_new_stations)
    
    return

# call main directly because of st.navigation
main()

# does not work with streamlit.navigation(Page)
# if __name__ == "__main__":
#     main()
