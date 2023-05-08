import streamlit as st
import geopandas as gpd
import random
from streamlit_folium import folium_static
import folium
import json

# Load the shapefile and convert it to GeoJSON
shapefile_url = 'https://raw.githubusercontent.com/bassneel/basspublicfiles/main/world_countries.zip'
gdf = gpd.read_file(shapefile_url)
geojson = gdf.to_crs(epsg='4326').to_json()

# Convert the GeoJSON string to a dictionary
geojson_dict = json.loads(geojson)

# Initialize the Folium map
m = folium.Map(location=[0, 0], zoom_start=2)

# Add the GeoJSON layer to the map
folium.GeoJson(
    geojson_dict,
    name='geojson'
).add_to(m)

# Extract the country and region data from the attribute table
countries = {}
for feature in gdf['COUNTRY']:
    country = feature
    region = gdf[gdf['COUNTRY'] == country]['REGION'].iloc[0]
    if region not in countries:
        countries[region] = []
    countries[region].append(country)

# Initialize variables for keeping track of the game state
score = 0
rounds = 5
round_number = 1
answer_submitted = False

# Function to generate the dropdown options for a given round
def generate_options(correct_country, region):
    options = [correct_country]
    while len(options) < 3:
        random_country = random.choice(countries[region])
        if random_country != correct_country and random_country not in options:
            options.append(random_country)
    random.shuffle(options)
    return options

# Start the game
st.title('Country Guessing Game')
st.markdown('Can you guess the country highlighted on the map?')
if st.button('Start'):
    # Display the map at the beginning of the game
    folium_static(m)
    # Loop through each round
    for round_number in range(1, rounds + 1):
        if answer_submitted:
            # Select a random country and region for this round
            region = random.choice(list(countries.keys()))
            correct_country = random.choice(countries[region])
            selected_feature = [feature for feature in geojson_dict['features'] if feature['properties']['COUNTRY'] == correct_country][0]
            # Remove the previous GeoJSON layer from the map
            for layer in m._children:
                if layer == 'selected_feature.geojson':
                    del m._children[layer]
            # Highlight the selected country on the map
            folium.GeoJson(
                selected_feature,
                name='selected_feature',
                style_function=lambda x: {'fill_color': 'red', 'fillOpacity': 0.5, 'weight': 0.5}
                ).add_to(m)
            # Generate the dropdown options for this round
            options = generate_options(correct_country, region)
            # Display the dropdown for the user to make their guess
            guess = st.selectbox(f'Round {round_number}: Guess the country', options, key=f'guess_{round_number}')
            # Check if the user's guess is correct and update the score
            if guess == correct_country:
                st.success('Correct!')
                score += 1
            else:
                st.error(f'Sorry, the correct answer was {correct_country}.')
            # Update the game state
            round_number += 1
            answer_submitted = False

        else:
            answer_submitted = st.button('Submit')
    
    # End the game and display the final score\
    st.markdown('## Game over!')
    st.markdown(f'Your final score is {score}/{rounds}')

    # Add a button to restart the game
    if st.button('Play again'):
        # Reset the game state
        score = 0
        round_number = 1
        answer_submitted = False