import os
import time
import json
import folium  

import numpy as np
import pandas as pd
import geopandas as gpd
import streamlit as st

from streamlit_folium import st_folium
from branca.colormap import LinearColormap

#import streamlit_authenticator as stauth


# from core import methods as m1
# from core import HelperTools as ht
# from core.config import pdict
from streamlit_app_folder import methods
from streamlit_app_folder import data_pipeline as dp


# @timer
def helper_subset_with_criteria(df_orig: pd.DataFrame, column: str, criteria):
    """Make subset with respect to user selected criteria"""
    df = df_orig.copy()
    if criteria != "All":
        return df[df[column] == criteria].copy()
    else:
        return df


def filter_zip_code_widget(df):
    with st.container(border=True):
        # Add user input for zip code
        st.subheader("Charging Stations in my zip code")
        user_selected_zip_code = st.selectbox(
        "Only show Charging Stations in my zip code",
        ["All"] + sorted(df["PLZ"].unique()))

        # Make subset with respect to user selected PLZ
        df_user_selected_subset = helper_subset_with_criteria(df_orig=df, column="PLZ", criteria=user_selected_zip_code)
    return df_user_selected_subset

def filter_power_widget(df):
    with st.container(border=True):
        st.subheader("How much power is appropriate?")
        col1, col2 = st.columns(2)
        with col1:
            user_criteria_50kW = st.checkbox("Only show Charging Stations with 50kW and more!")
            if user_criteria_50kW:
                df = df[df["KW"] >= 50].copy() #.reset_index()

        with col2:
            # Add selector fpr KW
            user_selected_kw = st.selectbox(
            "Select the preferred power [kW] of your Charging Station",
            ["All"] + sorted(df["KW"].unique()),
            )

    # Make subset with respect to user selected kW
    df_user_selected_subset = helper_subset_with_criteria(df_orig=df, column="KW", criteria=user_selected_kw)
    return df_user_selected_subset

def spawn_heatmap_berlin(df_numbers_per_kW, df_numbers):
    # Create a Folium map
    m = folium.Map(location=[52.52, 13.40], zoom_start=10)

    with st.container(border=True):
        st.subheader("Map of berlin with Charging Stations")
        st.write("This is a map of Berlin with the number of electric charging stations per zip code")
        if len(df_numbers_per_kW) == 0:
            color_map = LinearColormap(colors=['yellow', 'red'], vmin=0, vmax=0)
            # folium.GeoJson().add_to(m)
            # Add color map to the map
            color_map.add_to(m)

            # Show map
            st.write("Sorry, there is no such Charging Stations in berlin yet")
            st_folium(m, width=800, height=600)
        else:
            # Create a color map for Numbers
            color_map = LinearColormap(colors=['yellow', 'red'], vmin=1, vmax=df_numbers["Number"].max())
            # Add polygons to the map for Numbers
            for idx, row in df_numbers.iterrows():
                list_kW_in_row_sorted = sorted(df_numbers_per_kW.round({'KW':0})
                                               .astype({'KW':int})[df_numbers_per_kW['PLZ']==row['PLZ']].loc[:,'KW'].to_list())[::-1]
                folium.GeoJson(
                    row['geometry'],
                    style_function=lambda x, color=color_map(row['Number']): {
                        'fillColor': color,
                        'color': 'black',
                        'weight': 1,
                        'fillOpacity': 0.7
                    },
                    tooltip=f"PLZ: {row['PLZ']}, Number: {row['Number']}, \
                            kW: {list_kW_in_row_sorted}"
                ).add_to(m)

            # Add color map to the map
            color_map.add_to(m)

            # Show map
            st_folium(m, width=670, height=500) #, width=725 , height=600
    return

def show_selected_stations_as_df(df_numbers_per_kW, df_numbers, df_user_selected_subset_show):
    with st.container(border=True):
        st.subheader("Here are your selected Charging Stations")

        # Show df_numbers_per_kW and df_number as st.dataframe
        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.write("Number of Charging Stations per kW:")
            st.dataframe(df_numbers_per_kW.drop("geometry", axis=1).sort_values("KW", ascending=False), 
                         use_container_width=True, hide_index=True)
        with col2:
            st.write("Number of Charging Stations per zip code:")
            st.dataframe(df_numbers.drop("geometry", axis=1).sort_values("Number", ascending=False),
                         use_container_width=True, hide_index=True)

        # Show df_user_selected_subset_av as st.dataframe
        st.write("All Charging Stations you have selected with their address and availability:")
        st.dataframe(df_user_selected_subset_show, use_container_width=True, hide_index=True)
    return

def spawn_interactiv_df_for_user_comment(df_user_selected_subset_show):
    # init df if new user or load data if page is refreshed
    if "df_stations_user_edit" not in st.session_state:
        try:
            with open("DataBase_user_changes.json", "r") as file:
                user_database = json.load(file)
            df_user_changes = pd.DataFrame(user_database[st.session_state.username])
            df_user_changes.set_index("PLZ", drop=True, inplace=True)
            print(df_user_changes.head(5))
        except:
            df_user_changes = pd.DataFrame(columns=df_user_selected_subset_show.columns.to_list()+["Rating", "Comment"])
    else:
        df_user_changes = st.session_state.df_stations_user_edit
    
    # define config for interactiv df with st.column_config
    config = {
        'PLZ' : st.column_config.NumberColumn('PLZ', min_value=10115, max_value=14200, required=True), #width='large',
        'Straße' : st.column_config.TextColumn('Straße', required=True), #width='medium',
        'Hausnummer' : st.column_config.TextColumn('Hausnummer', required=True, width='small'),
        'KW' : st.column_config.NumberColumn('KW', min_value=1, max_value=1000, width='small'),
        'Available' : st.column_config.SelectboxColumn('Available', options=["✔️", "❌"]),
        'Rating' : st.column_config.SelectboxColumn('Rating', options=list(range(1,6))),
        'Comment' : st.column_config.TextColumn('Comment')
    }

    
    with st.container(border=True):
        st.subheader("Do you want to add a Charging Station or leave a comment?")
        st.write("Tank you for helping the project and other users! Here you can add \
                a new Charging Station? You can also leave a recommendation or a comment for an existing recommendation:")
        
        # Spawn interactiv df
        df_stations_user_edit = st.data_editor(df_user_changes, column_config=config, num_rows='dynamic',
                                               use_container_width=False)

        # Reload page iusse solution: save it in a session state
        st.session_state.df_stations_user_edit = df_stations_user_edit

        # Spawn button to check post bevor submit
        if st.button('Get results'):
            st.write("Here is your post. You can change it at any time.")
            st.dataframe(df_stations_user_edit)

            # Spawn button to submit
            if st.button("Submit post", key="submited_post"):
                st.write("We have saved your post. Thank you for your support!")
                time.sleep(2)

        # init session state if not exist
        if "submited_post" not in st.session_state:
            st.session_state.submited_post = False

        # Save post if submitted
        elif st.session_state.submited_post == True:
            # Load DB of previous post
            with open("DataBase_user_changes.json", "r") as file:
                user_database = json.load(file)

            # try to convert df to dict, except that it is already a dict (happens when refresh the page)  
            try:
                user_database[st.session_state.username] = df_stations_user_edit.to_dict()
            except:
                user_database[st.session_state.username] = df_stations_user_edit

            # save data of the currently submitted post
            with open("DataBase_user_changes.json", "w") as file:
                json.dump(user_database, file)

            # print "Thanks for submittion" and reload the page after sleep 3s
            st.write("We have saved your post. Thank you for your support!")
            time.sleep(3)
            st.rerun()
    return

# Make Heatmap of berlin with number of charging stations
@methods.timer
def make_streamlit_electric_Charging_plz(df):
    """Makes Streamlit App with Heatmap of Electric Charging Stations"""

    # Add Available column
    df_every_station = df.copy()
    df_every_station["Available"] = np.random.choice(["✔️", "❌"], df_every_station.shape[0]).tolist()

    # Streamlit page title
    st.title('Find your Electric Charging Station')
    
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
    df_user_selected_subset_show = pd.DataFrame(df_user_selected_subset.copy().drop(columns=["geometry", "Breitengrad",
                                                    "Längengrad", "Bundesland", "Ort"])).sort_values("KW", ascending=False)
    # Show dataframes that user has filtered
    show_selected_stations_as_df(df_numbers_per_kW, df_numbers, df_user_selected_subset_show)

    # Spawn interactiv df for user comments
    spawn_interactiv_df_for_user_comment(df_user_selected_subset_show)

    return

# @methods.timer
def init_data():
    """Init and process data only ones at the start of the app (instead of every tick)"""
    if "df_charging_berlin" not in st.session_state:
        st.session_state.df_charging_berlin = dp.data_process()
    return

def Make_berlin_mapp():
    """Make and start streamlit UI"""
    make_streamlit_electric_Charging_plz(st.session_state.df_charging_berlin)
    return

@methods.timer
def main():
    """Generation of Streamlit App for visualizing electric charging stations & residents in Berlin"""
    init_data()
    Make_berlin_mapp()
    return

# call main directly because of st.navigation
main()

# does not work with streamlit.navigation(Page)
# if __name__ == "__main__":
#     main()