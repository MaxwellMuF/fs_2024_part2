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
    if "df_charging_berlin" not in st.session_state:
        st.session_state.df_charging_berlin = dp.data_process()
    return

# @ht.timer
def Make_berlin_mapp():
    """Make and start streamlit UI"""
    m1.make_streamlit_electric_Charging_resid_2(st.session_state.df_charging_berlin)
    return

# @ht.timer
def main():
    """Generation of Streamlit App for visualizing electric charging stations & residents in Berlin"""
    init_data()
    Make_berlin_mapp()
    return

main()

# does not work with streamlit.navigation(Page)
# if __name__ == "__main__":
#     main()
