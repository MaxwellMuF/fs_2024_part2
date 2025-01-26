import streamlit as st
# Own python files
from application.src.utilities import methods_login
from infrastructure.src.data_downloader import downloader_pipeline
from domain.src.berlin_data_process import data_pipeline_berlin_old

# Initialize st.session_state (st.Class properties) at start or reload of app/page. 
def init_st_session_state():
    """Initialize all streamlit.session_states that are needed or required in the app."""
    # ---- here were a lot of variables (session_state) bevor using st.authenticator and st.navigation -----
    return

@st.cache_resource()
def download_data_from_url():
    downloader_pipeline.activate_dowload()
    data_pipeline_berlin_old.activate_pipeline_berlin()
# ------------------------------- Pages --------------------------------------

def pages_bevor_login():
    """Pages of streamlit app bevor login defined by functions"""
    login = st.Page(methods_login.login_widget, title="Login", icon=":material/login:")
    register_new_user = st.Page(methods_login.register_new_user_widget, title="Sign Up", icon=":material/person_add:")
    forgot_password = st.Page(methods_login.forgot_password_widget, title="Forget Password", icon=":material/lock_reset:")
    forgot_username = st.Page(methods_login.forgot_username_widget, title="Forget Username", icon=":material/help_outline:")

    return [login, register_new_user, forgot_password, forgot_username]

def pages_after_login():
    """Pages of streamlit app after login defined by functions and python files"""
    welcome = st.Page("application/src/ui/page_1_welcome.py", title="Welcome", icon=":material/home:")
    charging_stations = st.Page("application/src/ui/page_2_charging_stations.py", title="Charging Stations", icon=":material/dynamic_form:") #, default=True
    rate_and_comment = st.Page("application/src/ui/page_3_rate_and_comment.py", title="Rate and Comment", icon=":material/chat_bubble:")
    new_stations = st.Page("application/src/ui/page_4_new_stations.py", title="Add New Stations", icon=":material/add_circle:")    
    reset_password = st.Page(methods_login.reset_password_widget, title="Reset Password", icon=":material/lock_reset:")
    logout = st.Page(methods_login.logout_widget, title="Logout", icon=":material/logout:")

    # add_notes
    return [welcome, charging_stations, rate_and_comment, new_stations, reset_password, logout]

def main():
    """
    Main function of the entire steamlit app. 
    This is where the navigator is defined that leads to all scripts and functions. 
    And the authenticator process is called.
    """
    # download_data_from_url()
    # init_st_session_state()

    # load authenticator config and create login st.authenticator
    config = methods_login.load_config(config_path="application/data/data_user/config.yaml")
    methods_login.create_authenticator(config)

    # Show pages before a user is logged in
    if not st.session_state.authentication_status:
        page_navigator = st.navigation(pages_bevor_login())
        page_navigator.run()
    
    # Show pages after a user is logged in (Note: st.authenticator uses browser cookies)
    elif st.session_state.authentication_status:
        page_navigator = st.navigation(pages_after_login())
        page_navigator.run()

    # Catches some unexpected login problems. Should not occur.
    else:
        print("We should never get here!")
    
    # save authenticator config
    methods_login.save_config(config, config_path="application/data/data_user/config.yaml")
    
    return

if __name__ == "__main__":
    main()