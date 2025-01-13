import streamlit as st

# st.title('Find a charging station in your area.')
st.header(f'Welcome *{st.session_state["name"]}*')
st.write(f'We are grateful for your selection of our services and will do our best to assist you in your search.')


with st.container(border=True):
    st.header("Let's create the future")
    col1, col2 = st.columns(2)
    with col1:
        st.image("data/Ai_pic_berlin_for_welcome.jpeg")
    with col2:
        st.image("data/Ai_pic_berlin_for_welcome2.jpeg")
    st.write("Berlin as it should be. And with your help, we are already one step closer.\
                        (Source: https://designer.microsoft.com/image-creator")

# Prompt that was used to create the picture:
# A row of sleek, modern charging stations for electric cars, designed with a green innovative style. The stations are lined up neatly, each with a futuristic look and eco-friendly design. In the background, we see partly the outskirts of the Berlin city and partly a green meadow. Solar panels glisten under the sunlight, capturing the energy of the sun. The scene is bathed in natural light, with a clear blue sky overhead, creating a serene and sustainable atmosphere. The charging stations are made of smooth, metallic materials with a glossy finish, reflecting the sunlight. The green meadow is lush and vibrant, with wildflowers scattered throughout. The Berlin cityscape in the background and the berlin television tower features modern skyscrapers and historic buildings, creating a contrast between urban and natural elements. The overall scene exudes a sense of harmony between technology and nature, emphasizing the importance of sustainable energy solutions.