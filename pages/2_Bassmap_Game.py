import streamlit as st
import bassmap
import bassmap.Foliumatic as bassmap
from streamlit_folium import st_folium
import folium

# Load the compressed shapefile and convert it to a geojson using the add_shp() method
geojson = bassmap.add_shp('path/to/shapefile.zip')

# Extract the country and region data from the attribute table
countries = {}
for feature in geojson['features']:
    country = feature['properties']['COUNTRY']
    region = feature['properties']['REGION']
    if region not in countries:
        countries[region] = []
    countries[region].append(country)

# Function to generate the dropdown options for a given round
def generate_options(correct_country, region):
    options = [correct_country]
    while len(options) < 3:
        random_country = random.choice(countries[region])
        if random_country != correct_country and random_country not in options:
            options.append(random_country)
    random.shuffle(options)
    return options

# Initialize variables for keeping track of the game state
score = 0
rounds = 5
round_number = 1

# Initialize the Foliumatic map
m = Foliumatic()
m.add_geojson(geojson)

# Start the game
st.title('Country Guessing Game')
st.markdown('Can you guess the country highlighted on the map?')
if st.button('Start'):
    # Loop through each round
    while round_number <= rounds:
        # Select a random country and region for this round
        region = random.choice(list(countries.keys()))
        correct_country = random.choice(countries[region])
        selected_feature = [feature for feature in geojson['features'] if feature['properties']['COUNTRY'] == correct_country][0]
        # Highlight the selected country on the map
        m.clear_layers()
        m.add_geojson(selected_feature)
        st.pydeck_chart(m.get_map())
        # Generate the dropdown options for this round
        options = generate_options(correct_country, region)
        # Prompt the user to guess the country
        guess = st.selectbox(f'Round {round_number}: Guess the country', options)
        if st.button('Submit'):
            # Check if the guess is correct
            if guess == correct_country:
                st.write('Correct!')
                score += 1
            else:
                st.write(f'Sorry, the correct answer was {correct_country}.')
            round_number += 1
    # Display the final score
    st.write(f'Final score: {score}/{rounds}')
    if st.button('Restart'):
        # Reset the game state
        score = 0
        round_number = 1