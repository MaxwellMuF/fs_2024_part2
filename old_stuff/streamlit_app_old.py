"""
Script description: This script imports tests the Streamlit-Authenticator package. 

Libraries imported:
- yaml: Module implementing the data serialization used for human readable documents.
- streamlit: Framework used to build pure Python web applications.
"""

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

# Creating a login widget
def login_widget():
    try:
        authenticator.login(key="Login")
        st.session_state.new_user = st.button("Register here", on_click=reset_go_to_login())
        if st.session_state.new_user:
            st.rerun()
    except LoginError as e:
        st.error(e)

# Creating a new user registration widget
def register_user():
    try:
        (email_of_registered_user,
            username_of_registered_user,
            name_of_registered_user) = authenticator.register_user()
        if email_of_registered_user:
            st.success('User registered successfully')
        st.session_state.go_to_login = st.button("Go to login")
        if st.session_state.go_to_login:
            st.rerun()
    except RegisterError as e:
        st.error(e)
        st.session_state.go_to_login = st.button("Go to login")

# Welcome page
def welcome():
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title('Find a charging station in your area.')
    st.write(f'We are grateful for your selection of our services and will do our best to assist you in your search.')
    st.image("data/evpstation-banner-1024x576.jpg",
             caption="This picture is from the competition. Our picture will follow soon.\
                  (Source: https://www.plugndrive.ca/public-charging/)")

# Creating a password reset widget
def reset_password():
    if st.session_state['authentication_status']:
        try:
            if authenticator.reset_password(st.session_state['username']):
                st.success('Password modified successfully')
        except (CredentialsError, ResetError) as e:
            st.error(e)

# Creating an update user details widget
def update_user_details():
    if st.session_state['authentication_status']:
        try:
            if authenticator.update_user_details(st.session_state['username']):
                st.success('Entry updated successfully')
        except UpdateError as e:
            st.error(e)

# helper
def reset_new_user_state():
    st.session_state.new_user = False
def reset_go_to_login():
    st.session_state.go_to_login = False

# ---------------------------------------------------------------------------
## Data and inits 

# Loading config file
with open('data/config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)

# init website
#st.set_page_config(page_title="Electric Charging Stations")

# Creating the authenticator object
global authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    key="streamlit_app"
)
# ---------------------------------------------------------------------------

## Init session_states aka class streamlit properties 
if "new_user" not in st.session_state:
    st.session_state.new_user = False
if "go_to_login" not in st.session_state:
    st.session_state.go_to_login = False
if "go_to_settings" not in st.session_state:
    st.session_state.go_to_settings = False
if "settings" not in st.session_state or st.session_state.go_to_settings:
    st.session_state.settings = False





# Creating a login widget
if (not st.session_state.new_user or st.session_state.go_to_login) and not st.session_state.authentication_status:
    login_widget()
elif st.session_state.new_user and not st.session_state.authentication_status:
    register_user()
if st.session_state['authentication_status'] and not st.session_state.settings:
    reset_password()
    update_user_details()
    st.session_state.settings = st.button("Leave settings")
    if st.session_state.settings:
        st.session_state.go_to_settings = False
        st.rerun()
    st.stop()



# Authenticating user
# https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Rounded&icon.size=24&icon.color=%23e8eaed
if st.session_state['authentication_status']:
    page_1_welcome = st.Page("page_1_welcome.py", title="Welcome", icon=":material/home:")
    page_2_charging_stations = st.Page("page_2_charging_stations.py", title="Charging Stations", icon=":material/dynamic_form:")
    page_3_reset_password = st.Page(reset_password, title="Reset Password", icon=":material/key:")
    
    pg = st.navigation([page_1_welcome, 
                        page_2_charging_stations,
                        page_3_reset_password
                        ])
    with st.sidebar:
        st.session_state.go_to_settings = st.button("Settings")
        if st.session_state.go_to_settings:
            st.rerun()
        authenticator.logout()
    pg.run()
#     # Using object notation
#     add_selectbox = st.sidebar.selectbox(
#         "How would you like to be contacted?",
#         ("Email", "Home phone", "Mobile phone")
# )

    # Using "with" notation
#     with st.sidebar:
#         welcome_page = st.button("Welcome")
#         show_charging_map = st.button("Find Charging Station")
#         reset_pw = st.button("Reset Password")
#         update_user = st.button("Change your user profile")
#         authenticator.logout()
#     if not (welcome_page or reset_pw or show_charging_map or update_user):
#         welcome_page = True
#     if welcome_page:
#         welcome()
#     elif reset_pw:
#         reset_password()
#     elif show_charging_map:
#         charging_stations.main()
#     elif update_user:
#         update_user_details()
#     else:
#         charging_stations.main()
# elif st.session_state['authentication_status'] is False:
#     st.error('Username/password is incorrect')
# elif st.session_state['authentication_status'] is None and not st.session_state.new_user:
#     st.warning('Please enter your username and password or register as a new user')



# # Creating a new user registration widget
# try:
#     (email_of_registered_user,
#         username_of_registered_user,
#         name_of_registered_user) = authenticator.register_user()
#     if email_of_registered_user:
#         st.success('User registered successfully')
# except RegisterError as e:
#     st.error(e)

# # Creating a forgot password widget
# try:
#     (username_of_forgotten_password,
#         email_of_forgotten_password,
#         new_random_password) = authenticator.forgot_password()
#     if username_of_forgotten_password:
#         st.success('New password sent securely')
#         # Random password to be transferred to the user securely
#     elif not username_of_forgotten_password:
#         st.error('Username not found')
# except ForgotError as e:
#     st.error(e)

# # Creating a forgot username widget
# try:
#     (username_of_forgotten_username,
#         email_of_forgotten_username) = authenticator.forgot_username()
#     if username_of_forgotten_username:
#         st.success('Username sent securely')
#         # Username to be transferred to the user securely
#     elif not username_of_forgotten_username:
#         st.error('Email not found')
# except ForgotError as e:
#     st.error(e)

# # Creating an update user details widget
# if st.session_state['authentication_status']:
#     try:
#         if authenticator.update_user_details(st.session_state['username']):
#             st.success('Entry updated successfully')
#     except UpdateError as e:
#         st.error(e)

# Saving config file
with open('data/config.yaml', 'w', encoding='utf-8') as file:
    yaml.dump(config, file, default_flow_style=False)