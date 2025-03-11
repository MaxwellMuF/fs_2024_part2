import streamlit                    as st

from application.src.utilities.authenticator import (Authenticator,
                                            	     RegisterNewUser)
# ----------------------------- Data and inits ------------------------------

def login_box() -> None:
    """Spawn login box and errors"""
    with st.form(key="user_sign_in", enter_to_submit=True):
        st.header(body="Login")
        st.session_state.username = st.text_input(label="Username")
        st.session_state.user_password = st.text_input(label="Password", type='password')
        st.form_submit_button(label="Login")

    if st.session_state["FormSubmitter:user_sign_in-Login"]:
        login_user()
    return

def login_user() -> None:
    """"""
    authent = Authenticator(path_credential=st.session_state.path_credential_users)
    try:
        authent.username = st.session_state.username
        authent.password = st.session_state.user_password
    except Exception as error:
        st.error(body=f"Error: {error}", icon=":material/error:")
    else:
        st.session_state["logged_in"] = True
    finally:
        del st.session_state.user_password

    if st.session_state["logged_in"]:
        st.rerun()

    return


def logout_box() -> None:
    with st.container(border=True):
        st.header(body="Logout")
        st.write(f"Thank you for your visit *{st.session_state.username}*")

        if st.button(label="Logout"):
            st.session_state.username = None
            st.session_state["logged_in"] = False
            st.rerun()

    return

def register_box() -> None:
    """Make a register box"""
    with st.form(key="register", enter_to_submit=True):
        st.header(body="Register New User")
        register_new_user_dict = dict()
        # Name
        col_first_name, col_last_name = st.columns(2)
        with col_first_name:
            register_new_user_dict["first_name"] = st.text_input(label="First Name:")
        with col_last_name:
            register_new_user_dict["last_name"] = st.text_input(label="Last Name:")

        # user and key
        col_username, col_registerkey = st.columns(2)
        with col_username:
            register_new_user_dict["username"] = st.text_input(label="Username:")
        with col_registerkey:
            register_new_user_dict["register_key"] = st.text_input(label="Register Key:", type="password")
        
        # password
        col_password, col_repeat = st.columns(2)
        with col_password:
            register_new_user_dict["password"] = st.text_input(label="Password:", type="password")
        with col_repeat:
            register_new_user_dict["password_repeat"] = st.text_input(label="Repeat Password:", type="password")

        st.form_submit_button("Sign Up")

    if st.session_state["FormSubmitter:register-Sign Up"]:
        register_new_user(register_new_user_dict)

    return

def register_new_user(register_new_user_dict: dict) -> None:
    """Make RegisterNewUser object or throw error exceptions"""
    register = RegisterNewUser(path_credential=st.session_state.path_credential_users)
    try:
        register.new_user_credential = register_new_user_dict
    except Exception as error:
        st.error(body=f"Error: {error}", icon=":material/error:")
    else:
        register.save_new_user()
        st.success(body="Registration was successful!", icon=":material/check_circle:")
    
    return