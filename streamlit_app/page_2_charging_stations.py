import os
import pandas as pd
import geopandas as gpd
import streamlit as st  # Import streamlit here
import streamlit_authenticator as stauth

from core import methods as m1
from core import HelperTools as ht
from core.config import pdict
from core import data_pipeline as dp


def init_data():
    """Init and process data only ones at the start of the app (instead of every tick)"""
    if "gdf_lstat3" not in st.session_state:
        st.session_state.gdf_lstat3, st.session_state.gdf_residents2 = dp.data_process()

# @ht.timer
def Make_streamlit_ui():
    """Make and start streamlit UI"""
    # Streamlit app logic with radio button for function selection
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
        st.session_state.show_charging_map = True
    else:
        m1.make_streamlit_electric_Charging_resid_by_kw(st.session_state.gdf_lstat3, st.session_state.gdf_residents2)
        st.session_state.show_charging_map = True



# @ht.timer
def main():
    """Generation of Streamlit App for visualizing electric charging stations & residents in Berlin"""
    init_data()
    Make_streamlit_ui()

main()
# does not work with streamlit.navigation(Page)
# if __name__ == "__main__":
#     main()
