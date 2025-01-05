import os
import pandas as pd
import geopandas as gpd
import streamlit as st  # Import streamlit here
import streamlit_authenticator as stauth

from core import methods as m1
from core import HelperTools as ht
from config import pdict

@ht.timer
def data_process():
    """Data process: Load and process data"""
    # Load data
    df_geodat_plz = pd.read_csv('datasets/geodata_berlin_plz.csv', sep=';')  # For geospatial data
    df_lstat = pd.read_excel('datasets/Ladesaeulenregister_SEP.xlsx', header=10)

    # Inspect data (optional debugging statements)
    # print("Initial columns in df_lstat:", df_lstat.columns)
    # print("Sample data from df_lstat:", df_lstat.head())

    df_residents = pd.read_csv('datasets/plz_einwohner.csv')  # Adjust the path accordingly

    # Data Quality Checks
    required_columns_charging = ['Postleitzahl', 'Bundesland', 'Breitengrad', 'Längengrad', 'Nennleistung Ladeeinrichtung [kW]']
    column_formats_charging = {
        'Postleitzahl': int,
        'Bundesland': str,
        'Breitengrad': (float, str),  # Allow strings due to conversion step
        'Längengrad': (float, str),
        'Nennleistung Ladeeinrichtung [kW]': float
    }
    value_ranges_charging = {
        'Postleitzahl': (10000, 14200),
        'Nennleistung Ladeeinrichtung [kW]': (0, 1000)
    }
    quality_issues_lstat = ht.check_data_quality(df_lstat, required_columns_charging, column_formats_charging, value_ranges_charging)
    if quality_issues_lstat:
        print("Data Quality Issues for Charging Stations:", quality_issues_lstat)

    required_columns_residents = ['plz', 'einwohner', 'lat', 'lon']
    column_formats_residents = {
        'plz': int,
        'einwohner': int,
        'lat': float,
        'lon': float
    }
    value_ranges_residents = {
        'plz': (10000, 14200),
        'einwohner': (0, 50000)
    }
    quality_issues_residents = ht.check_data_quality(df_residents, required_columns_residents, column_formats_residents, value_ranges_residents)
    if quality_issues_residents:
        print("Data Quality Issues for Residents Data:", quality_issues_residents)

    # Preprocess data
    gdf_lstat = m1.preprop_lstat(df_lstat, df_geodat_plz, pdict)
    gdf_lstat3 = m1.count_plz_occurrences(gdf_lstat)
    gdf_residents2 = m1.preprop_resid(df_residents, df_geodat_plz, pdict)

    return gdf_lstat3, gdf_residents2

def init_data():
    """Init and process data only ones at the start of the app (instead of every tick)"""
    if "gdf_lstat3" not in st.session_state:
        st.session_state.gdf_lstat3, st.session_state.gdf_residents2 = data_process()

# @ht.timer
def Make_streamlit_ui():
    """Make and start streamlit UI"""
    # Streamlit app logic with radio button for function selection
    st.set_page_config(page_title="Electric Charging Stations")
    st.title('Berlin Electric Charging Station Heatmaps')
    function_selection = st.radio(
        "Select Visualization Type",
        (
            "Heatmap: Electric Charging Stations and Residents",
            "Heatmap: Electric Charging Stations by KW and Residents"
        )
    )

    if function_selection == "Heatmap: Electric Charging Stations and Residents":
        m1.make_streamlit_electric_Charging_resid(st.session_state.gdf_lstat3, st.session_state.gdf_residents2)
    else:
        m1.make_streamlit_electric_Charging_resid_by_kw(st.session_state.gdf_lstat3, st.session_state.gdf_residents2)

# import streamlit as st
# import streamlit_authenticator as stauth

# --- User Details ---
names = ["John Doe", "Jane Smith"]
usernames = ["johndoe", "janesmith"]
hashed_passwords = [
    '$2b$12$N9qo8uLOickgx2ZMRZo5e.8.k7xl1TTQ1y.wKGzDYi99JejO9Txue',  # Example hash
    '$2b$12$5o8QFZJg6ZG..XHQefPI5uo0FrwxrQzBh4cq/TZW5e8xtDANUs8ly'   # Example hash
]

# Authentication setup
authenticator = stauth.Authenticate(
    names, usernames, hashed_passwords, 
    "some_cookie_name", "some_signature_key"
    )

# Login form
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    st.success(f"Welcome {name}!")
    st.sidebar.button("Logout", on_click=authenticator.logout)
    # Your app logic here
elif authentication_status == False:
    st.error("Username or password is incorrect")
elif authentication_status == None:
    st.warning("Please enter your username and password")



# @ht.timer
def main():
    """Generation of Streamlit App for visualizing electric charging stations & residents in Berlin"""
    init_data()
    Make_streamlit_ui()

if __name__ == "__main__":
    main()
