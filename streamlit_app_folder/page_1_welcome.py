import streamlit as st

def welcome_text():
    """Welcome text with user """
    with st.container(border=True):
        st.subheader(body="About the project:",
                     help="")
        st.write(f'Hello *{st.session_state.get("name", "Guest_default_for_testing")}*! \
                Thank you for your interest in the project. \
                Here you will find a short description of what the project is about:') # Use get method to run tests
        st.write("*ChargeHub Berlin* is an interactive platform designed to provide Berlin residents \
                with a user-friendly way to locate charging stations in their area (postal code), \
                check usage and availability, and contribute to the enhancement of the charging infrastructure. \
                *ChargeHub Berlin* is a digital platform designed to provide Berlin residents with a seamless way to \
                locate charging stations in their area (postal code), check their status and availability, \
                and actively contribute to enhancing the city's charging infrastructure. \
                The platform empowers users with the ability to search for available charging stations, \
                rate their locations, report malfunctions, and submit new proposals for charging stations \
                within their postal code area.")

    return

def image_with_motivation():
    """Show images and motiavtion text"""
    with st.container(border=True):
        st.header("Let's create the future")
        col1, col2 = st.columns(2)
        with col1:
            st.image("data/Ai_pic_berlin_for_welcome.jpeg")
        with col2:
            st.image("data/Ai_pic_berlin_for_welcome2.jpeg")
        st.write("Berlin as it should be. And with your help, we are already one step closer.")

    return
        
def main():
    """Main of the Welcome page: Calls up text and images."""
    st.title(body="Welcome to ChargeHub Berlin", 
             help="On this page you will find a greeting and a short description of the project.")
    image_with_motivation()
    welcome_text()

# call main directly because of st.navigation
main()