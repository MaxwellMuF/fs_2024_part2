import streamlit as st

def welcome_text():
    """Welcome text with user """
    st.header(f'Welcome *{st.session_state.get("name", "Guest")}*')
    st.write(f'We are grateful for your selection of our services and will do our best to assist you in your search.')

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
        # (Source: https://designer.microsoft.com/image-creator)
        
def main():
    """Main of the Welcome page: Calls up text and images."""
    welcome_text()
    image_with_motivation()

# call main directly because of st.navigation
main()