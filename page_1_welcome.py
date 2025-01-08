import streamlit as st

st.write(f'Welcome *{st.session_state["name"]}*')
st.title('Find a charging station in your area.')
st.write(f'We are grateful for your selection of our services and will do our best to assist you in your search.')
st.image("data/evpstation-banner-1024x576.jpg",
            caption="This picture is from the competition. Our picture will follow soon.\
                (Source: https://www.plugndrive.ca/public-charging/)")