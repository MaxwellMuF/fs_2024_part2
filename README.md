# This repository contains project 1 and project 2 of the lecture advanced software engineering of the BHT.
The associated streamlit app was applied via streamlit.io and can be accessed under https://maxwell0charging0berlin.streamlit.app/. You can create your own account or use one of the test user accounts. Please note that each widget of the app has a helper (<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0&icon_names=help" />) that describes the content of this section.

Test_user   : user1 or user2

Passwort    : 123

# project 1
First, the data is automatically downloaded [Data dowload](infrastructure/src/data_downloader/download_data.py) and converted into the correct format [Data cleaner](infrastructure/src/data_downloader/data_cleaner.py).
This process is triggered (@st.cache_resource()) when the app is deployed again and is intended to keep the data up to date (see app main script: [streamlit_app.py](streamlit_app.py)).

The main part of project 1 takes place in the file [Add New Stations](application/src/ui/page_4_new_stations.py), which is accessible under this name in the app via the navigator bar on the left.
