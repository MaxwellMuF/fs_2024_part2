# This repository contains project 1 and project 2 of the lecture advanced software engineering of the BHT.
The associated streamlit app was applied via streamlit.io and can be accessed under https://maxwell0charging0berlin.streamlit.app/. You can create your own account or use one of the test user accounts. Please note that each widget of the app has a helper (?) that describes the content of this section.

Test users  : `user1` or `user2`

Passwort    : `123`
---

# Project 1
First, the data is automatically downloaded [Data dowload](infrastructure/src/data_downloader/download_data.py) and converted into the correct format [Data cleaner](infrastructure/src/data_downloader/data_cleaner.py).
This process is triggered (@st.cache_resource()) when the app is deployed again and is intended to keep the data up to date (see app main script: [streamlit_app.py](streamlit_app.py)).

The main part of project 1 takes place in the file [Add New Stations](application/src/ui/page_4_new_stations.py), which is accessible under this name in the app via the navigator bar on the left. Here you can see an impression of the page with the corresponding options to select data and filters:
![ui_part_1_screen](https://github.com/user-attachments/assets/9ed0e891-d46a-496c-ab24-4956a343aed7)
The functions of the page elements are explained in the help (?) texts and are therefore not explained in detail here. 

## Findings and results
The analysis of the geovisualizations shows:
1. Populations and charging stations are not equally distributed in Berlin. If you switch between the data sets of `Residents` and `Charging Stations`, you can see that some zip codes have only a few stations although they have a high population.
2. The zip code 12683 attracts attention because it has the most charging stations with a number of 101 (set 'Select Data' to `Charging Stations`). However, this only applies to slow charging stations. If you set the filter to fast charging stations, a different picture emerges (set 'Select Filter' to `Fast Charger only`): Now zip code 12683 has only 7 stations left and other zip codes are better equipped. Please note that this differentiation could be important, as slow charging stations are only for residents or people with very long parking times (e.g. over night, over 5-8 hours).
3. The density shows a similarly imbalanced situation (set 'Select Data' to `Density` and 'Select Filter' to `All`): Some zip codes have a reddish color and thus a high density of residents per charging station. If you set the fast charging filter again, the picture becomes even worse ('Select Filter' to `Fast Charger only`): Many zip codes are now no longer displayed in color. This means that there are no fast charging stations. Especially the areas within the ring (the inner part of Berlin) show significant deficits.
4. It is also possible to check which zip codes are relatively well equipped by activating the `Reciprocal Density` checkbox. The density of charging stations per resident is now displayed. ZIP codes with a red color are therefore well supplied in this setting.
5. At the bottom of the page, the data of the charging stations and the density data sets are displayed. This allows you to check the exact values again in some settings. Furthermore, other problems become visible: for example, if you set the filter to `Slow Charger only` and look at the data frame below ('Selected Charing Stations'), you will notice the following. Most charging stations are considered to be fast chargers if they have an output of 50kW or more. But some stations are far above 50kW although they are labeled as slow chargers (Click on the `KW` column to sort by that column). This is either an error or a technical problem.
However, fast charging is an important part of the acceptance of electromobility. If you look at the center of Berlin, the problem becomes clear. And it should be supported privately as well as statewide in order to encourage electromobility.

## Code and program structure
The python file of the page [Add New Stations](application/src/ui/page_4_new_stations.py) contains many functions, including name_widget() for streamlit boxes on the page and some helpers and date processors. However, this file has not been split into other files to clearly separate the work for part 1 from part 2.

The code is structured in such a way that it is best read from bottom to top (since all parts are functions, this could also be reversed): 
1. layer, `main()`: The function at the end of the script is main() and forms the top layer. It loads the data (init_session_states[init_data]) and calls the streamlit elements (make_streamlit_page_elements).
2. layer, `make_streamlit_page_elements()`: All 4 streamlit widgets are called here (the 4 boxes on the website). Each of these forms a subpart of the page and calls its own elements.
3. layer, `make_selector_widget()`: Look at this widget, for example. Here again 4 functions are called. Some of them are responsible for streamlit elements like radio_selectors(). And others are just data processors like make_density_df().
4. layer `radio_selectors()`: On this 4th and last level are the helper functions and the smallest streamlit methods. radio_selectors(), for example, makes the ratio options and sorts a pd df. Like these functions, most functions can be reduced and atomized in further refactoring cycles. This is of course essential for larger software products, but it might only make this MVP a little clearer.

