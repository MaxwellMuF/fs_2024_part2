import numpy                         as np
import pandas                        as pd
import geopandas                     as gpd
import core.HelperTools              as ht

import folium
# from folium.plugins import HeatMap
import streamlit as st
from streamlit_folium import folium_static
from branca.colormap import LinearColormap


@ht.timer
def sort_by_plz_add_geometry(dfr, dfg, pdict): 
    dframe                  = dfr.copy()
    df_geo                  = dfg.copy()
    
    sorted_df               = dframe\
        .sort_values(by='PLZ')\
        .reset_index(drop=True)\
        .sort_index()
        
    sorted_df2              = sorted_df.merge(df_geo, on=pdict["geocode"], how ='left')
    sorted_df3              = sorted_df2.dropna(subset=['geometry'])
    
    sorted_df3.loc[:,'geometry']  = gpd.GeoSeries.from_wkt(sorted_df3['geometry'])
    ret                     = gpd.GeoDataFrame(sorted_df3, geometry='geometry')
    
    return ret

# -----------------------------------------------------------------------------
@ht.timer
def preprop_lstat(dfr, dfg, pdict):
    """Preprocessing dataframe from Ladesaeulenregister.csv"""
    dframe                  = dfr.copy()
    df_geo                  = dfg.copy()
    
    dframe2               	= dframe.loc[:,['Postleitzahl', 'Bundesland', 'Breitengrad', 'Längengrad', 'Nennleistung Ladeeinrichtung [kW]']]
    dframe2.rename(columns  = {"Nennleistung Ladeeinrichtung [kW]":"KW", "Postleitzahl": "PLZ"}, inplace = True)

    # Convert to string
    dframe2['Breitengrad']  = dframe2['Breitengrad'].astype(str)
    dframe2['Längengrad']   = dframe2['Längengrad'].astype(str)

    # Now replace the commas with periods
    dframe2['Breitengrad']  = dframe2['Breitengrad'].str.replace(',', '.')
    dframe2['Längengrad']   = dframe2['Längengrad'].str.replace(',', '.')

    dframe3                 = dframe2[(dframe2["Bundesland"] == 'Berlin') & 
                                            (dframe2["PLZ"] > 10115) &  
                                            (dframe2["PLZ"] < 14200)]
    
    ret = sort_by_plz_add_geometry(dframe3, df_geo, pdict)
    
    return ret
    

# -----------------------------------------------------------------------------
@ht.timer
def count_plz_occurrences(df_lstat2, sort_col=("PLZ")):
    """Counts loading stations per PLZ"""
    # Group by PLZ and count occurrences, keeping geometry
    result_df = df_lstat2.groupby(sort_col).agg(
        Number=('KW', 'count'),
        geometry=('geometry', 'first')
    ).reset_index()
    
    return result_df
    
# -----------------------------------------------------------------------------
# @ht.timer
# def preprop_geb(dfr, pdict):
#     """Preprocessing dataframe from gebaeude.csv"""
#     dframe      = dfr.copy()
    
#     dframe2     = dframe .loc[:,['lag', 'bezbaw', 'geometry']]
#     dframe2.rename(columns      = {"bezbaw":"Gebaeudeart", "lag": "PLZ"}, inplace = True)
    
    
#     # Now, let's filter the DataFrame
#     dframe3 = dframe2[
#         dframe2['PLZ'].notna() &  # Remove NaN values
#         ~dframe2['PLZ'].astype(str).str.contains(',') &  # Remove entries with commas
#         (dframe2['PLZ'].astype(str).str.len() <= 5)  # Keep entries with 5 or fewer characters
#         ]
    
#     # Convert PLZ to numeric, coercing errors to NaN
#     dframe3['PLZ_numeric'] = pd.to_numeric(dframe3['PLZ'], errors='coerce')

#     # Filter for PLZ between 10000 and 14200
#     filtered_df = dframe3[
#         (dframe3['PLZ_numeric'] >= 10000) & 
#         (dframe3['PLZ_numeric'] <= 14200)
#     ]

#     # Drop the temporary numeric column
#     filtered_df2 = filtered_df.drop('PLZ_numeric', axis=1)
    
#     filtered_df3 = filtered_df2[filtered_df2['Gebaeudeart'].isin(['Freistehendes Einzelgebäude', 'Doppelhaushälfte'])]
    
#     filtered_df4 = (filtered_df3\
#                  .assign(PLZ=lambda x: pd.to_numeric(x['PLZ'], errors='coerce'))[['PLZ', 'Gebaeudeart', 'geometry']]
#                  .sort_values(by='PLZ')
#                  .reset_index(drop=True)
#                  )
    
#     ret                     = filtered_df4.dropna(subset=['geometry'])
        
#     return ret
    
# -----------------------------------------------------------------------------
@ht.timer
def preprop_resid(dfr, dfg, pdict):
    """Preprocessing dataframe from plz_einwohner.csv"""
    dframe                  = dfr.copy()
    df_geo                  = dfg.copy()    
    
    dframe2               	= dframe.loc[:,['plz', 'einwohner', 'lat', 'lon']]
    dframe2.rename(columns  = {"plz": "PLZ", "einwohner": "Einwohner", "lat": "Breitengrad", "lon": "Längengrad"}, inplace = True)

    # Convert to string
    dframe2['Breitengrad']  = dframe2['Breitengrad'].astype(str)
    dframe2['Längengrad']   = dframe2['Längengrad'].astype(str)

    # Now replace the commas with periods
    dframe2['Breitengrad']  = dframe2['Breitengrad'].str.replace(',', '.')
    dframe2['Längengrad']   = dframe2['Längengrad'].str.replace(',', '.')

    dframe3                 = dframe2[ 
                                            (dframe2["PLZ"] > 10000) &  
                                            (dframe2["PLZ"] < 14200)]
    
    ret = sort_by_plz_add_geometry(dframe3, df_geo, pdict)
    
    return ret


# -----------------------------------------------------------------------------
@ht.timer
def make_streamlit_electric_Charging_resid(dfr1, dfr2):
    """Makes Streamlit App with Heatmap of Electric Charging Stations and Residents"""
    
    dframe1 = dfr1.copy()
    dframe2 = dfr2.copy()


    # Streamlit app
    st.title('Heatmaps: Electric Charging Stations and Residents')

    # Create a radio button for layer selection
    # layer_selection = st.radio("Select Layer", ("Number of Residents per PLZ (Postal code)", "Number of Charging Stations per PLZ (Postal code)"))

    layer_selection = st.radio("Select Layer", ("Residents", "Charging_Stations"))

    # Create a Folium map
    m = folium.Map(location=[52.52, 13.40], zoom_start=10)

    if layer_selection == "Residents":
        
        # Create a color map for Residents
        color_map = LinearColormap(colors=['yellow', 'red'], vmin=dframe2['Einwohner'].min(), vmax=dframe2['Einwohner'].max())

        # Add polygons to the map for Residents
        for idx, row in dframe2.iterrows():
            folium.GeoJson(
                row['geometry'],
                style_function=lambda x, color=color_map(row['Einwohner']): {
                    'fillColor': color,
                    'color': 'black',
                    'weight': 1,
                    'fillOpacity': 0.7
                },
                tooltip=f"PLZ: {row['PLZ']}, Einwohner: {row['Einwohner']}"
            ).add_to(m)
        
        # Display the dataframe for Residents
        # st.subheader('Residents Data')
        # st.dataframe(gdf_residents2)

    else:
        # Create a color map for Numbers

        color_map = LinearColormap(colors=['yellow', 'red'], vmin=dframe1['Number'].min(), vmax=dframe1['Number'].max())

    # Add polygons to the map for Numbers
        for idx, row in dframe1.iterrows():
            folium.GeoJson(
                row['geometry'],
                style_function=lambda x, color=color_map(row['Number']): {
                    'fillColor': color,
                    'color': 'black',
                    'weight': 1,
                    'fillOpacity': 0.7
                },
                tooltip=f"PLZ: {row['PLZ']}, Number: {row['Number']}"
            ).add_to(m)

        # Display the dataframe for Numbers
        # st.subheader('Numbers Data')
        # st.dataframe(gdf_lstat3)

    # Add color map to the map
    color_map.add_to(m)
    
    folium_static(m, width=800, height=600)

# ----------------------------- New Funktions -------------------------------

def helper_subset_with_criteria(df_orig: pd.DataFrame, column: str, criteria):
    """Make subset with respect to user selected criteria"""
    df = df_orig.copy()
    if criteria != "All":
        return df[df[column] == criteria].copy()
    else:
        return df


# Make Heatmap of berlin with number of charging stations
@ht.timer
def make_streamlit_electric_Charging_resid_2(dfr1):
    """Makes Streamlit App with Heatmap of Electric Charging Stations"""
    df_every_station = dfr1.copy()
    df_numbers_per_kW = count_plz_occurrences(dfr1, sort_col=['PLZ', "KW"])
    df_numbers = count_plz_occurrences(dfr1, sort_col=('PLZ'))
    # print(dframe1.head(5))
    # dframe2 = dfr2.copy()

    # Streamlit app
    st.title('Find your Electric Charging Station')
    
    # Add user input for zip code
    user_zip_code = st.selectbox(
    "Only show Charging Station in my zip code",
    ["All"] + sorted(df_every_station["PLZ"].unique()))

    # Make subset with respect to user selected PLZ
    df_user_selected_subset = helper_subset_with_criteria(df_orig=df_every_station, column="PLZ", criteria=user_zip_code)

    col1, col2 = st.columns(2)
    with col1:
        user_criteria_50kW = st.checkbox("Only show Charging Station with 50kW and more!")
        if user_criteria_50kW:
            df_user_selected_subset = df_user_selected_subset[df_user_selected_subset["KW"] >= 50].copy() #.reset_index()

    with col2:
        # Add selector fpr KW
        user_selected_kw = st.selectbox(
        "Select the preferred power [kW] of your charging station",
        ["All"] + sorted(df_user_selected_subset["KW"].unique()),
        )

    # Make subset with respect to user selected kW
    if user_selected_kw != "All":
        df_user_selected_subset = df_user_selected_subset[df_user_selected_subset["KW"] == user_selected_kw].copy()
    else:
        df_user_selected_subset = df_user_selected_subset

    # Make grouped dfs
    df_numbers_per_kW = count_plz_occurrences(df_user_selected_subset, sort_col=['PLZ', "KW"])
    df_numbers = count_plz_occurrences(df_user_selected_subset, sort_col=('PLZ'))


    # Create a Folium map
    m = folium.Map(location=[52.52, 13.40], zoom_start=10)

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
                     kW: {sorted(df_numbers_per_kW[df_numbers_per_kW['PLZ']==row['PLZ']].loc[:,'KW'].to_list())[::-1]}"
        ).add_to(m)

    # Add color map to the map
    color_map.add_to(m)

    # Show map
    st.write("This is a map of Berlin with the number of electric charging stations per zip code")
    folium_static(m, width=800, height=600)


    # Display the dataframe for Numbers
    if df_user_selected_subset.shape[0] == 1:
        st.subheader("Here is your selected Charging Station")
    else:
        st.subheader("Here are your selected Charging Stations")

    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(df_numbers_per_kW.drop("geometry", axis=1).sort_values("KW", ascending=False))
    with col2:
        st.dataframe(df_numbers.drop("geometry", axis=1).sort_values("Number", ascending=False))
    
    df_user_selected_subset["Availability"] = np.random.choice(["✅","❌"], df_user_selected_subset.shape[0])
    st.dataframe(df_user_selected_subset.drop(["geometry", "Breitengrad",
                                                "Längengrad"], axis=1).sort_values("KW", ascending=False))










### Studito old stuff
@ht.timer
def make_streamlit_electric_Charging_resid_by_kw(dfr1, dfr2):
    """Makes Streamlit App with Separate Layers for Each KW Category of Electric Charging Stations and Residents"""
    
    dframe1 = dfr1.copy()
    dframe2 = dfr2.copy()

    # Streamlit app
    st.title('Heatmaps: Electric Charging Stations by KW and Residents')

    # Create a radio button for layer selection
    layer_selection = st.radio("Select Layer", ("Residents", "Charging_Stations by KW"))
    
    # Create a Folium map
    m = folium.Map(location=[52.52, 13.40], zoom_start=10)

    if layer_selection == "Residents":
        # Create a color map for Residents
        if 'Einwohner' in dframe2.columns:
            color_map = LinearColormap(colors=['yellow', 'red'], vmin=dframe2['Einwohner'].min(), vmax=dframe2['Einwohner'].max())
            # Add polygons to the map for Residents
            for idx, row in dframe2.iterrows():
                folium.GeoJson(
                    row['geometry'],
                    style_function=lambda x, color=color_map(row['Einwohner']): {
                        'fillColor': color,
                        'color': 'black',
                        'weight': 1,
                        'fillOpacity': 0.7
                    },
                    tooltip=f"PLZ: {row['PLZ']}, Einwohner: {row['Einwohner']}"
                ).add_to(m)
        else:
            st.warning("Residents data is not available.")
    else:
        # Separate layers for each KW value
        if 'KW' in dframe1.columns:
            unique_kws = dframe1['KW'].unique()
            # color_map = LinearColormap(colors=['yellow', 'red'], vmin=unique_kws.min(), vmax=unique_kws.max())
            for kw in unique_kws:
                kw_data = dframe1[dframe1['KW'] == kw]
                print(kw_data['Number'].min(), kw_data['Number'].max())
                if not kw_data.empty:
                    # Create a separate feature group for each KW layer
                    feature_group = folium.FeatureGroup(name=f'KW {kw}')
                    color_map = LinearColormap(colors=['yellow', 'red'], vmin=kw_data['Number'].min(), vmax=kw_data['Number'].max())

                    for idx, row in kw_data.iterrows():
                        folium.GeoJson(
                            row['geometry'],
                            style_function=lambda x, color=color_map(row['Number']): {
                                'fillColor': color,
                                'color': 'black',
                                'weight': 1,
                                'fillOpacity': 0.7
                            },
                            tooltip=f"PLZ: {row['PLZ']}, KW: {kw}, Number: {row['Number']}"
                        ).add_to(feature_group)
                    
                    # Add feature group to the map
                    feature_group.add_to(m)
        else:
            st.warning("KW column is not available in the data.")
    
    # Add layer control to toggle visibility
    # folium.LayerControl().add_to(m)
    # Add color map to the map
    color_map.add_to(m)

    folium_static(m, width=800, height=600)


