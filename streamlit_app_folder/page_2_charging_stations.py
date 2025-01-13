import time
import json
import folium  

import numpy        as np
import pandas       as pd
import streamlit    as st

from streamlit_folium       import st_folium
from branca.colormap        import LinearColormap

from streamlit_app_folder   import methods
from streamlit_app_folder   import data_pipeline


def helper_subset_with_criteria(df_orig: pd.DataFrame, column: str, criteria):
    """Make subset with respect to user selected criteria"""
    df = df_orig.copy()
    if criteria != "All":
        return df[df[column] == criteria].copy()
    else:
        return df

# ----------------------------- streamlit widgets ------------------------------

def filter_zip_code_widget(df):
    """User select zip code widget: selectbox for zip code and returns selected subset"""
    with st.container(border=True):
        st.subheader("Charging Stations in my zip code")
        user_selected_zip_code = st.selectbox(
        "Only show Charging Stations in my zip code",
        ["All"] + sorted(df["PLZ"].unique()))

    return helper_subset_with_criteria(df_orig=df, column="PLZ", criteria=user_selected_zip_code)


def filter_power_widget(df):
    """User select power widget: checkbox and selectbox for power in two columns.
    Returns selected subset"""
    with st.container(border=True):
        st.subheader("How much power is appropriate?")
        col1, col2 = st.columns(2)

        with col1:
            user_criteria_50kW = st.checkbox("Only show Charging Stations with 50kW and more!")
            if user_criteria_50kW:
                df = df[df["KW"] >= 50].copy()

        with col2:
            user_selected_kw = st.selectbox(
            "Select the preferred power [kW] of your Charging Station",
            ["All"] + sorted(df["KW"].unique()),
            )

    return helper_subset_with_criteria(df_orig=df, column="KW", criteria=user_selected_kw)

def spawn_heatmap_berlin(df_numbers_per_kW, df_numbers):
    """Create folium map with given dfs containing 'KW' and 'Number' columns"""
    m = folium.Map(location=[52.52, 13.40], zoom_start=10)

    with st.container(border=True):
        st.subheader("Map of berlin with Charging Stations")
        st.write("This is a map of Berlin with the number of electric charging stations per zip code")

        # catch case: empty df, i.e. no charging station found
        if len(df_numbers_per_kW) == 0:
            st.write("Sorry, there is no such Charging Stations in berlin yet")
            st_folium(m, width=800, height=600)
        else:
            color_map = LinearColormap(colors=['yellow', 'red'], vmin=1, vmax=df_numbers["Number"].max())
            
            # Add polygons to the map for Numbers
            for idx, row in df_numbers.iterrows():
                # make tooltip with 'sorted list of power' from selected stations
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

            # Add color_map to the folium_map
            color_map.add_to(m)

            # Show folium_map
            st_folium(m, width=670, height=500)

    return

def show_selected_stations_as_df(df_numbers_per_kW, df_numbers, df_user_selected_subset_show):
    """Show selected data in three dfs: 1. per KW and per zip code in two columns
                                        2. all selected stations with adress"""
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

def init_user_db_if_needed(df_user_selected_subset_show):
    """User DB three cases: use as data 1. load json or 
                                        2. initialize a user DB or 
                                        3. use session_state)"""

    if "df_stations_user_edit" not in st.session_state:
        # 1. Load user DB from json
        try: 
            with open("DataBase_user_changes.json", "r") as file:
                user_database = json.load(file)
            return pd.DataFrame(user_database[st.session_state.username])
        
        # 2. Init user DB
        except:
            return pd.DataFrame(columns=df_user_selected_subset_show.columns.to_list()+["Rating", "Comment"])
        
    # 3. Take user DB in session_state
    else:
        return st.session_state.df_stations_user_edit

def spawn_interactiv_df_for_user_comment(df_user_changes):
    """Spawn interactiv df for user posts: 
            1. Create config
            2. Spawn interactiv dataframe
            3. Show post bevor submit it
            4. Submit post, i.e. save it in user DB
            """
    # 1. Define config for interactiv df with st.column_config
    config = {
        'PLZ' : st.column_config.NumberColumn('PLZ', min_value=10115, max_value=14200, required=True), #width='large',
        'Straße' : st.column_config.TextColumn('Straße', required=True), #width='medium',
        'Hausnummer' : st.column_config.TextColumn('Hausnummer', required=True, width='small'),
        'KW' : st.column_config.NumberColumn('KW', min_value=1, max_value=1000, width='small'),
        'Available' : st.column_config.SelectboxColumn('Available', options=["✔️", "❌"], width='small'),
        'Rating' : st.column_config.SelectboxColumn('Rating', options=list(range(1,6)), width='small'),
        'Comment' : st.column_config.TextColumn('Comment')
    }

    # Create container user post
    with st.container(border=True):
        st.subheader("Do you want to add a Charging Station or leave a comment?")
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
                time.sleep(2)

        # init session state if not exist
        if "submited_post" not in st.session_state:
            st.session_state.submited_post = False

        # Save post if submitted
        elif st.session_state.submited_post == True:
            # Load DB of previous post
            with open("DataBase_user_changes.json", "r") as file:
                user_database = json.load(file)

            # make new entry in user DB: key=user : value=user_post  
            user_database[st.session_state.username] = df_stations_user_edit.to_dict()

            # save data of the currently submitted post
            with open("DataBase_user_changes.json", "w") as file:
                json.dump(user_database, file)

            # print "Thanks for submittion" and reload the page after sleep 3s
            st.write("We have saved your post. Thank you for your support!")
            time.sleep(3)
            st.rerun()
    return

# ----------------------------- streamlit page ------------------------------

# Make Heatmap of berlin with number of charging stations
@methods.timer
def make_streamlit_page_elements(df):
    """The sequence of streamlit elements on this page:
            Perform user selection and filter data.
            Makes heatmap of electric Charging Stations in berlin.
            And show selected data and offer post submission and save user posts."""

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
                                                    "Längengrad", "Bundesland", "Ort", "Plug Types"])).sort_values("KW", ascending=False)
    # Show dataframes that user has filtered
    show_selected_stations_as_df(df_numbers_per_kW, df_numbers, df_user_selected_subset_show)

    # Load or init user DB
    df_user_changes = init_user_db_if_needed(df_user_selected_subset_show)

    # Spawn interactiv df for user comments
    spawn_interactiv_df_for_user_comment(df_user_changes)
    return

# @methods.timer
def init_data():
    """Init and process data only ones at the start of the app (instead of every tick)"""
    if "df_charging_berlin" not in st.session_state:
        st.session_state.df_charging_berlin = data_pipeline.data_process()
    return

@methods.timer
def main():
    """Main of the Charging Stations page: 
            Load and process data and save it as streamlit state.
            Makes heatmap of electric Charging Stations in berlin.
            And show selected data and submit and save user posts."""
    init_data()
    make_streamlit_page_elements(st.session_state.df_charging_berlin)
    return

# call main directly because of st.navigation
main()

# does not work with streamlit.navigation(Page)
# if __name__ == "__main__":
#     main()
