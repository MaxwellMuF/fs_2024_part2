import streamlit as st
# import streamlit_app
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities import (CredentialsError,
                                               ResetError)

st.title("Hello")
print(st.session_state.__getitem__(key="new_key"))
# Loading config file
with open('data/config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)

# # init website
# #st.set_page_config(page_title="Electric Charging Stations")
# del st.session_state.init
# #del st.session_state.user_key
# st.session_state.user_key = "new_key"
# print(st.session_state)

# # Creating the authenticator object
# authenticator = stauth.Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days'],
#     key="reset_password"
# )

# # streamlit_app.reset_password()

# st.title("Reset Password")
# if st.session_state['authentication_status']:
#     try:
#         if authenticator.reset_password(st.session_state['username']):
#             st.success('Password modified successfully')
#     except (CredentialsError, ResetError) as e:
#         st.error(e)

# # Saving config file
# with open('data/config.yaml', 'w', encoding='utf-8') as file:
#     yaml.dump(config, file, default_flow_style=False)