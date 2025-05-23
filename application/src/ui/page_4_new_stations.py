import folium  

import pandas       as pd
import streamlit    as st

from streamlit_folium       import st_folium
from branca.colormap        import LinearColormap

# Own python files
from application.src.utilities   import helper_page_2 as helper2


# ----------------------------- Helper ------------------------------

def radio_selectors(df_charging: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    """Make two columns with radio selectors"""
    col1, col2 = st.columns(2)
    with col1:
        selected_df = st.radio("Select Data:",  ("Residents", "Charging Stations", "Density"))
    with col2:
        selected_filter = st.radio("Select Filter:",  ("All", "Slow Charger only", "Fast Charger only"))

    if selected_filter == "Slow Charger only":
        df_charging_2 = df_charging[df_charging["Art der Ladeeinrichung"] == "Normalladeeinrichtung"]
    elif selected_filter == "Fast Charger only":
        df_charging_2 = df_charging[df_charging["Art der Ladeeinrichung"] == "Schnellladeeinrichtung"]
    else:
        df_charging_2 = df_charging.copy()
    return df_charging_2, selected_df
        
def make_density_df(df_charging_numbers: pd.DataFrame, df_residents: pd.DataFrame) -> pd.DataFrame:
    """Make df_density with df_charging_numbers and df_residents. Also spawn checkbox for reciprocal density"""
    # Make df_density
    df_density = df_charging_numbers.merge(df_residents.drop("geometry", axis=1), how="left", on="PLZ")
    df_density["Density"] = df_density["Residents"] / df_density["Number"]

    # Make reciprocal of the density
    if st.checkbox(label="Reciprocal Density", 
                    help=st.session_state.text_for_page_4_help["make_density_df_help"]):
        df_density.loc[:,"Density"] = df_density["Density"].rdiv(1).round(5)
    else:
        df_density.loc[:,"Density"] = df_density["Density"].round(0)
        df_density = df_density.astype({"Density":int})
    
    return df_density

def select_show_df(selected_df: str, df_charging_numbers: pd.DataFrame, df_residents: pd.DataFrame, 
                   df_density: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    """Choose the data that the user has selected. Return a df and a specific column_name"""
    if selected_df == "Charging Stations":
        df_map_show = df_charging_numbers
        column_show = "Number"

    elif selected_df == "Residents":
        df_map_show = df_residents
        column_show = "Residents"
    
    elif selected_df == "Density":
        df_map_show = df_density
        column_show = "Density"

    return df_map_show, column_show

def count_plz_occurrences(df_lstat2, sort_col=("PLZ")):
    """Counts loading stations per PLZ"""
    # Group by PLZ and count occurrences, keeping geometry
    result_df = df_lstat2.groupby(sort_col).agg(
        Number=("Anzahl Ladepunkte","sum"),
        geometry=("geometry", "first")
    ).reset_index().astype({"Number":int})
    
    return result_df
# ----------------------------- streamlit widgets ------------------------------

def make_selector_widget(df_charging: pd.DataFrame, df_residents: pd.DataFrame) -> tuple[pd.DataFrame,pd.DataFrame,str]:
    """Make the widget with selectors. Return selected data, density data, show column"""
    with st.container(border=True):
        st.header(body="Select a data set and a filter",
                  help=st.session_state.text_for_page_4_help["make_selector_widget_help"])

        # Spawn radio selectors
        df_charging, selected_df    = radio_selectors(df_charging.copy())

        df_charging.dropna(subset   ="Anzahl Ladepunkte", inplace=True)
        df_residents.dropna(subset  ="Residents", inplace=True)
        df_residents                = df_residents.astype({"Residents":int})
        # Process data for map
        df_charging_numbers         = count_plz_occurrences(df_charging, sort_col=("PLZ"))
        df_density                  = make_density_df(df_charging_numbers, df_residents)
        df_map_show, column_show    = select_show_df(selected_df, df_charging_numbers, df_residents, df_density)
    
    return df_map_show, df_charging, df_density, column_show

def spawn_heatmap_berlin_widget(df_map_show: pd.DataFrame, column_show: str) -> None:
    """Create folium map with given dfs containing 'KW' and 'Number' columns"""
    with st.container(border=True):
        st.header(body="Map of berlin with Charging Stations",
                    help=st.session_state.text_for_page_4_help["spawn_heatmap_berlin_help"])
        st.write("This is a map of Berlin with the number of electric charging stations per zip code")
        exclude_top_n = st.select_slider(label="Exclude biggest PLZ:", options=range(len(df_map_show)), 
                                         help=st.session_state.text_for_page_4_help["spawn_heatmap_berlin_widget_help"])
        df_map_show = df_map_show.sort_values(by=column_show, ascending=False).iloc[exclude_top_n:,:]
        m = folium.Map(location=[52.52, 13.40], zoom_start=10)

        # catch case: empty df, i.e. no charging station found
        if len(df_map_show) == 0:
            st.warning("Sorry, there is no such Charging Stations in berlin yet", icon="⚠️")
            st_folium(m, width=800, height=600)
        else:
            color_map = LinearColormap(colors=["yellow", "red"], vmin=df_map_show[column_show].min(),
                                                                vmax=df_map_show[column_show].max())
            
            # Add polygons to the map for Numbers
            for idx, row in df_map_show.iterrows():
                # Add PLZ with geometry to map
                folium.GeoJson(
                    row["geometry"],
                    style_function=lambda x, color=color_map(row[column_show]): {
                        "fillColor": color,
                        "color": "black",
                        "weight": 1,
                        "fillOpacity": 0.7
                    },
                    tooltip=f"PLZ: {row['PLZ']}, {column_show}: {row[column_show]}"
                ).add_to(m)

            # Add color_map to the folium_map
            color_map.add_to(m)

            # Show folium_map
            st_folium(m, width=670, height=500)

    return

def show_df_charging_widget(df: pd.DataFrame) -> None:
    """Show df_charging as st.dataframe"""
    with st.container(border=True):
        st.header(body="Selected Charing Stations",
                  help=st.session_state.text_for_page_4_help["show_df_charging_help"])
        st.write("Charging Stations from the map as you have chosen above:")
        df = df.drop(["geometry"], axis=1)
        st.dataframe(df, column_order=["PLZ", "Straße","Hausnummer","KW","Anzahl Ladepunkte","Art der Ladeeinrichung"],
                     use_container_width=True, hide_index=True)
    return

def show_df_density_widget(df: pd.DataFrame) -> None:
    """Show df_charging as st.dataframe"""
    with st.container(border=True):
        st.header(body="Selected Density per zip code",
                  help=st.session_state.text_for_page_4_help["show_df_density_help"])
        st.write("Density data from the map as you have chosen above:")
        df = df.drop(["geometry"], axis=1)
        df = pd.DataFrame(df)
        st.dataframe(df, column_order=["PLZ", "Density", "Number", "Residents"],
                     use_container_width=True, hide_index=True)
    return

# ----------------------------- streamlit page ------------------------------

def init_data(geodata_path: str="domain/data/processed_data_for_ui/geodata_berlin_plz.csv", 
              charging_data_path: str="domain/data/processed_data_for_ui/Ladesaeulenregister.csv",
              residents_path: str="domain/data/processed_data_for_ui/plz_einwohner.csv") -> pd.DataFrame:
    """Init and process data only ones at the start of the app (instead of every tick)"""

    df_geodat_plz               = pd.read_csv(geodata_path, sep=",", low_memory=False)
    df_charging                 = pd.read_csv(charging_data_path, sep=",", low_memory=False)
    df_plz_res                  = pd.read_csv(residents_path, sep=",", low_memory=False)
    # charging_required_columns   = ('Postleitzahl', 'Bundesland', 'Straße', 'Hausnummer',
    #                                'Ort', 'Nennleistung Ladeeinrichtung [kW]', "Art der Ladeeinrichung")
    
    # apply data process
    df_charging                 = helper2.merge_with_geometry(df_charging, df_geodat_plz)
    df_residents                = helper2.merge_with_geometry(df_plz_res, df_geodat_plz)

    return df_charging, df_residents

def init_session_states():
    """Init the streamlit session states for this page"""
    if "df_charging_berlin_new_stations" not in st.session_state:
        st.session_state.df_charging_berlin_new_stations = init_data()[0]
    if "df_residents_new_stations" not in st.session_state:
        st.session_state.df_residents_new_stations = init_data()[1]
    if "text_for_page_4_help" not in st.session_state:
        # because of the funny behaior of load a json into python str into streamlit md, we need to trippe '\' in '\n'
        st.session_state.text_for_page_4_help = helper2.load_json("application/data/data_ui_texts/text_for_page_4_help.json")

    return

def make_streamlit_page_elements(df_charging: pd.DataFrame, df_residents: pd.DataFrame) -> None:
    """The sequence of streamlit elements on this page:
            Perform user selection and filter data.
            Makes heatmap of electric Charging Stations in berlin.
            And show selected data."""

    # Selector widget
    df_map_show, df_charging, df_density, column_show = make_selector_widget(df_charging.copy(), df_residents.copy())

    # Heatmap widget
    spawn_heatmap_berlin_widget(df_map_show, column_show)

    # Data Frames widgets
    show_df_charging_widget(df_charging)
    show_df_density_widget(df_density)

    return

def main() -> None:
    """Init session state and call make_streamlit_page_elements."""
    init_session_states()
    st.title(body="Coverage of Charging Stations",
             help=st.session_state.text_for_page_4_help["show_df_density_help"])
    make_streamlit_page_elements(st.session_state.df_charging_berlin_new_stations,
                                 st.session_state.df_residents_new_stations)
    
    return

# Call main
main()
