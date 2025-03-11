import streamlit as st
# Own python files
from application.src.utilities import st_methods_login
from infrastructure.src.data_downloader import downloader_pipeline
from domain.src.berlin_data_process import data_pipeline_berlin

# Initialize st.session_state (st.Class properties) at start or reload of app/page. 
def init_st_session_state():
    """Initialize all streamlit.session_states that are needed or required in the app."""
    # ---- here were a lot of variables (session_state) bevor using st.authenticator and st.navigation -----
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = None
    if "path_credential_users" not in st.session_state:
        st.session_state["path_credential_users"] = "application/data/data_user/credential_users.yaml"
    return

@st.cache_resource()
def download_data_from_url():
    downloader_pipeline.activate_dowload()
    data_pipeline_berlin.activate_data_pipeline_berlin()
# ------------------------------- Pages --------------------------------------

def pages_bevor_login():
    """Pages of streamlit app bevor login defined by functions"""
    login = st.Page(st_methods_login.login_box, title="Login", icon=":material/login:")
    register_new_user = st.Page(st_methods_login.register_box, title="Sign Up", icon=":material/person_add:")
    
    return [login, register_new_user]

def pages_after_login():
    """Pages of streamlit app after login defined by functions and python files"""
    welcome = st.Page("application/src/ui/page_1_welcome.py", title="Welcome", icon=":material/home:")
    charging_stations = st.Page("application/src/ui/page_2_charging_stations.py", title="Charging Stations", icon=":material/dynamic_form:") #, default=True
    rate_and_comment = st.Page("application/src/ui/page_3_rate_and_comment.py", title="Rate and Comment", icon=":material/chat_bubble:")
    new_stations = st.Page("application/src/ui/page_4_new_stations.py", title="Add New Stations", icon=":material/add_circle:")    
    logout = st.Page(st_methods_login.logout_box, title="Logout", icon=":material/logout:")

    # add_notes
    return [welcome, charging_stations, rate_and_comment, new_stations, logout]

def main():
    """
    Main function of the entire steamlit app. 
    This is where the navigator is defined that leads to all scripts and functions. 
    And the authenticator process is called.
    """
    # download_data_from_url() 
    init_st_session_state()


    # Show pages before a user is logged in
    if not st.session_state["logged_in"]:
        page_navigator = st.navigation(pages_bevor_login())
        page_navigator.run()
    
    # Show pages after a user is logged in (Note: st.authenticator uses browser cookies)
    elif st.session_state["logged_in"]:
        page_navigator = st.navigation(pages_after_login())
        page_navigator.run()

    # Catches some unexpected login problems. Should not occur.
    else:
        print("We should never get here!")
    
    
    return

if __name__ == "__main__":
    main()