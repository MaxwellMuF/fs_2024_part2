import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities import (CredentialsError,
                                               ForgotError,
                                               Hasher,
                                               LoginError,
                                               RegisterError,
                                               ResetError,
                                               UpdateError)


# Pre-hashing all plain text passwords once
# stauth.Hasher.hash_passwords(config['credentials'])

# ---------------------------------------------------------------------------
## ---------------------------- FUNKTIONS -----------------------------------
# ---------------------------------------------------------------------------

# ----------------------------- Data and inits ------------------------------

def load_config(config_path="data/config.yaml"):
    """Loading config file"""
    with open(config_path, 'r', encoding='utf-8') as file:
        config = yaml.load(file, Loader=SafeLoader)
    return config

def save_config(config, config_path="data/config.yaml"):
    """Saving config file"""
    with open(config_path, 'w', encoding='utf-8') as file:
        yaml.dump(config, file, default_flow_style=False)
    return

def create_authenticator(config:yaml):
    """Creating the authenticator object"""
    global authenticator
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
        )
    return

def init_st_session_state():
    """Initialize all streamlit.session_states that are needed or required in the app."""
    if "new_user" not in st.session_state:
        st.session_state.new_user = False
    if "go_to_login" not in st.session_state:
        st.session_state.go_to_login = False
    if "go_to_settings" not in st.session_state:
        st.session_state.go_to_settings = False
    if "settings" not in st.session_state or st.session_state.go_to_settings:
        st.session_state.settings = False
    return

# ----------------------------- Bevor login -----------------------------------

# Creating a login widget
def login_widget():
    """Spawn a login widget"""
    try:
        authenticator.login()
    except LoginError as e:
        st.error(e)
    return

def logout_widget():
    """Logout user instant"""
    st.title(f"Thank you for a visit *{st.session_state.name}*")
    authenticator.logout()
    return

# Creating a new user registration widget
def register_new_user_widget():
    """Spawn a new user registration widget"""
    try:
        (email_of_registered_user,
            username_of_registered_user,
            name_of_registered_user) = authenticator.register_user()
        if email_of_registered_user:
            st.success('User registered successfully')
    except RegisterError as e:
        st.error(e)
    return

# Creating a forgot password widget
def forgot_password_widget():
    """Spawn a forgot password widget"""
    try:
        (username_of_forgotten_password,
            email_of_forgotten_password,
            new_random_password) = authenticator.forgot_password()
        if username_of_forgotten_password:
            st.success('New password sent securely')
            # Random password to be transferred to the user securely
        elif not username_of_forgotten_password:
            st.error('Username not found')
    except ForgotError as e:
        st.error(e)
    return

# Creating a forgot username widget
def forgot_username_widget():
    """Spawn a forgot password widget"""
    try:
        (username_of_forgotten_username,
            email_of_forgotten_username) = authenticator.forgot_username()
        if username_of_forgotten_username:
            st.success('Username sent securely')
            # Username to be transferred to the user securely
        elif not username_of_forgotten_username:
            st.error('Email not found')
    except ForgotError as e:
        st.error(e)
    return

# ----------------------------- After login -----------------------------------

# Welcome page
def welcome():
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title('Find a charging station in your area.')
    st.write(f'We are grateful for your selection of our services and will do our best to assist you in your search.')
    st.image("data/evpstation-banner-1024x576.jpg",
             caption="This picture is from the competition. Our picture will follow soon.\
                  (Source: https://www.plugndrive.ca/public-charging/)")

# Creating a password reset widget
def reset_password_widget():
    """Spawn a npassword reset widget"""
    if st.session_state['authentication_status']:
        try:
            if authenticator.reset_password(st.session_state['username']):
                st.success('Password modified successfully')
        except (CredentialsError, ResetError) as e:
            st.error(e)

# Creating an update user details widget
def update_user_details():
    """Spawn an update user details widget"""
    if st.session_state['authentication_status']:
        try:
            if authenticator.update_user_details(st.session_state['username']):
                st.success('Entry updated successfully')
        except UpdateError as e:
            st.error(e)

# ------------------------------- Pages --------------------------------------
# init website
#st.set_page_config(page_title="Electric Charging Stations")

def pages_bevor_login():
    login = st.Page(login_widget, title="Login", icon=":material/home:")
    register_new_user = st.Page(register_new_user_widget, title="Reset Password", icon=":material/key:")
    forgot_password = st.Page(forgot_password_widget, title="Forget Password", icon=":material/key:")
    forgot_username = st.Page(forgot_username_widget, title="Forget Username", icon=":material/key:")
    result_page_list = [login, register_new_user, forgot_password, forgot_username]
    return result_page_list

def pages_after_login():
    welcome = st.Page("streamlit_app/page_1_welcome.py", title="Welcome", icon=":material/home:")
    charging_stations = st.Page("streamlit_app/page_2_charging_stations.py", title="Charging Stations", icon=":material/dynamic_form:")
    reset_password = st.Page(reset_password_widget, title="Reset Password", icon=":material/key:")
    logout = st.Page(logout_widget, title="Logout", icon=":material/home:")
    result_page_list = [welcome, charging_stations, reset_password, logout]
    return result_page_list


## Init session_states aka class streamlit properties
def main():
    init_st_session_state()
    config = load_config(config_path="data/config.yaml")
    create_authenticator(config)

    if not st.session_state['authentication_status']:
        page_navigator = st.navigation(pages_bevor_login())
        page_navigator.run()
    elif st.session_state['authentication_status']:
        page_navigator = st.navigation(pages_after_login())
        page_navigator.run()
    else:
        print("We should never get here!")

    save_config(config, config_path="data/config.yaml")
    return

if __name__ == "__main__":
    main()