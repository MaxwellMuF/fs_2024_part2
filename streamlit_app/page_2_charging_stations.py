import os
import time
import json
import folium
import functools   

import numpy as np
import pandas as pd
import geopandas as gpd
import streamlit as st

from streamlit_folium import folium_static
from branca.colormap import LinearColormap

#import streamlit_authenticator as stauth

# from core import methods as m1
# from core import HelperTools as ht
# from core.config import pdict
from core import data_pipeline as dp

def timer(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()  # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()  # 2
        run_time = end_time - start_time  # 3
        print(" ====> Duration {:.2f} secs: {}".format(run_time, func.__doc__))
        return value

    return wrapper_timer 

# @timer
def count_plz_occurrences(df_lstat2, sort_col=("PLZ")):
    """Counts loading stations per PLZ"""
    # Group by PLZ and count occurrences, keeping geometry
    result_df = df_lstat2.groupby(sort_col).agg(
        Number=('KW', 'count'),
        geometry=('geometry', 'first')
    ).reset_index()
    
    return result_df

# @timer
def helper_subset_with_criteria(df_orig: pd.DataFrame, column: str, criteria):
    """Make subset with respect to user selected criteria"""
    df = df_orig.copy()
    if criteria != "All":
        return df[df[column] == criteria].copy()
    else:
        return df


# Make Heatmap of berlin with number of charging stations
@timer
def make_streamlit_electric_Charging_resid_2(dfr1):
    """Makes Streamlit App with Heatmap of Electric Charging Stations"""

    # Add Available column
    df_every_station = dfr1.copy()
    df_every_station["Available"] = np.random.choice(["✔️", "❌"], df_every_station.shape[0]).tolist()


    # Streamlit page title
    st.title('Find your Electric Charging Station')
    
    # Add user input for zip code
    st.subheader("Charging Stations in my zip code")
    user_selected_zip_code = st.selectbox(
    "Only show Charging Stations in my zip code",
    ["All"] + sorted(df_every_station["PLZ"].unique()))

    # Make subset with respect to user selected PLZ
    df_user_selected_subset = helper_subset_with_criteria(df_orig=df_every_station, column="PLZ", criteria=user_selected_zip_code)

    # Add power selection
    st.subheader("How much power is appropriate?")
    col1, col2 = st.columns(2)
    with col1:
        user_criteria_50kW = st.checkbox("Only show Charging Stations with 50kW and more!")
        if user_criteria_50kW:
            df_user_selected_subset = df_user_selected_subset[df_user_selected_subset["KW"] >= 50].copy() #.reset_index()

    with col2:
        # Add selector fpr KW
        user_selected_kw = st.selectbox(
        "Select the preferred power [kW] of your Charging Station",
        ["All"] + sorted(df_user_selected_subset["KW"].unique()),
        )

    # Make subset with respect to user selected kW
    df_user_selected_subset = helper_subset_with_criteria(df_orig=df_user_selected_subset, column="KW", criteria=user_selected_kw)

    # Make grouped dfs
    df_numbers_per_kW = count_plz_occurrences(df_user_selected_subset, sort_col=['PLZ', "KW"])
    df_numbers = count_plz_occurrences(df_user_selected_subset, sort_col=('PLZ'))

    # Create a Folium map
    m = folium.Map(location=[52.52, 13.40], zoom_start=10)


    if len(df_numbers_per_kW) == 0:
        color_map = LinearColormap(colors=['yellow', 'red'], vmin=0, vmax=0)
        # folium.GeoJson().add_to(m)
        # Add color map to the map
        color_map.add_to(m)

        # Show map
        st.write("This is a map of Berlin with the number of electric charging stations per zip code")
        st.write("Sorry, there is no such Charging Stations in berlin yet")
        folium_static(m, width=800, height=600)
    else:
        # Create a color map for Numbers
        color_map = LinearColormap(colors=['yellow', 'red'], vmin=1, vmax=df_numbers["Number"].max())
        # Add polygons to the map for Numbers
        for idx, row in df_numbers.iterrows():
            folium.GeoJson(
                row['geometry'],
                style_function=lambda x, color=color_map(row['Number']): {
                    'fillColor': color,
                    'color': 'black',
                    'weight': 1,
                    'fillOpacity': 0.7
                },
                tooltip=f"PLZ: {row['PLZ']}, Number: {row['Number']}, \
                        kW: {sorted(df_numbers_per_kW[df_numbers_per_kW['PLZ']==row['PLZ']].round({'KW':0}).astype({'KW':int}).loc[:,'KW'].to_list())[::-1]}"
            ).add_to(m)

        # Add color map to the map
        color_map.add_to(m)

        # Show map
        st.write("This is a map of Berlin with the number of electric charging stations per zip code")
        folium_static(m, width=800, height=600)


    # Display the dataframe for Numbers
    # if df_user_selected_subset.shape[0] == 1:
    #     st.subheader("Here is your selected Charging Station")
    # else:
    st.subheader("Here are your selected Charging Stations")

    col1, col2 = st.columns(2)
    with col1:
        st.write("Number of Charging Stations per kW")
        st.dataframe(df_numbers_per_kW.drop("geometry", axis=1).sort_values("KW", ascending=False))
    with col2:
        st.write("Number of Charging Stations per zip code")
        st.dataframe(df_numbers.drop("geometry", axis=1).sort_values("Number", ascending=False))

    # drop unnessesary columns
    df_user_selected_subset_av = pd.DataFrame(df_user_selected_subset.drop(columns=["geometry", "Breitengrad",
                                                "Längengrad", "Bundesland", "Ort"])).sort_values("KW", ascending=False)
    
    # if "df_stations_user_edit" not in st.session_state:
    #     st.session_state.df_stations_user_edit = False
    # Spawn interactiv df
    st.write("All Charging Stations you have selected with their address and availability:")
    st.dataframe(df_user_selected_subset_av)
    # df_user_selected_subset_av.copy()


    # Spawn a new df to add user input
    if "df_stations_user_edit" not in st.session_state:
        try:
            with open("DataBase_user_changes.json", "r") as file:
                user_database = json.load(file)
            df_user_changes = user_database[st.session_state.username]
        except:
            df_user_changes = pd.DataFrame(columns=df_user_selected_subset_av.columns.to_list()+["Rating", "Comment"])
    else:
        df_user_changes = st.session_state.df_stations_user_edit

    st.subheader("")
    st.subheader("Do you want to add a Charging Station or leave a comment?")
    st.write("Tank you for helping the project and other users! Here you can add \
             a new Charging Station? You can also leave a recommendation or a comment for an existing recommendation:")
    
    #df = pd.DataFrame(columns=['name','age','color'])
    # colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
    config = {
        'PLZ' : st.column_config.NumberColumn('PLZ', min_value=10115, max_value=14200, required=True), #width='large',
        'Straße' : st.column_config.TextColumn('Straße', required=True), #width='medium',
        'Hausnummer' : st.column_config.TextColumn('Hausnummer', required=True),
        'KW' : st.column_config.NumberColumn('KW', min_value=1, max_value=1000),
        'Available' : st.column_config.SelectboxColumn('Available', options=["✔️", "❌"]),
        'Rating' : st.column_config.SelectboxColumn('Rating', options=list(range(1,6))),
        'Comment' : st.column_config.TextColumn('Comment')
    }

    df_stations_user_edit = st.data_editor(df_user_changes, column_config = config, num_rows='dynamic')
    st.session_state.df_stations_user_edit = df_stations_user_edit
    
    if st.button('Get results'):
        st.write("Here is your post. You can change it at any time.")
        st.dataframe(df_stations_user_edit)
        if st.button("Submit post", key="submited_post"):
            st.write("We have saved your post. Thank you for your support!")
            time.sleep(2)

    if "submited_post" not in st.session_state:
        st.session_state.submited_post = False

    elif st.session_state.submited_post == True:
        # Save user changes as json (easy DB)
        with open("DataBase_user_changes.json", "r") as file:
            user_database = json.load(file)
        print("Here Load DB\n")
        print(df_stations_user_edit)
        try:
            user_database[st.session_state.username] = df_stations_user_edit.to_dict()
        except:
            user_database[st.session_state.username] = df_stations_user_edit
        with open("DataBase_user_changes.json", "w") as file:
            json.dump(user_database, file)
            print("Here Dump DB \n")
            print(df_stations_user_edit)
        st.write("We have saved your post. Thank you for your support!")
        time.sleep(3)
        st.rerun()

    return

def init_data():
    """Init and process data only ones at the start of the app (instead of every tick)"""
    if "df_charging_berlin" not in st.session_state:
        st.session_state.df_charging_berlin = dp.data_process()
    return

def Make_berlin_mapp():
    """Make and start streamlit UI"""
    make_streamlit_electric_Charging_resid_2(st.session_state.df_charging_berlin)
    return

def main():
    """Generation of Streamlit App for visualizing electric charging stations & residents in Berlin"""
    init_data()
    Make_berlin_mapp()
    return


main()

# does not work with streamlit.navigation(Page)
# if __name__ == "__main__":
#     main()
