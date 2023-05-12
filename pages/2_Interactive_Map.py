from osgeo import gdal
import streamlit as st
import bassmap.Foliumatic as bassmap
from streamlit_folium import st_folium
import folium
from osgeo import gdal

st.set_page_config(layout="wide")

col1, col2 = st.columns([7, 2])

# Define a dictionary of basemaps with their names and URLs
basemaps = {
    'OpenStreetMap': 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    'Mapbox Satellite': 'https://api.mapbox.com/styles/v1/mapbox/satellite-v9/tiles/{z}/{x}/{y}?access_token=<your-access-token>',
    'Esri.WorldImagery': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    'OpenTopoMap': 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
    'Esri.NatGeoWorldMap': 'https://server.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}',
    'CartoDB.Positron': 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png',
}

# Create a list of basemap names from the dictionary keys
basemap_names = list(basemaps.keys())

# Create a streamlit dropdown menu with the basemap names
with col2:
    dropdown = st.selectbox("Basemap", basemap_names)
    default_url = basemaps[dropdown]
    custom_url = st.text_input("Enter URL", default_url)

# Create a Foliumatic map object and add the selected basemap
m = bassmap.Foliumatic(center=(40, -100), zoom_start=8)
m.add_basemap(dropdown)

if custom_url:
    if custom_url:
        tile_layer = folium.TileLayer(
            tiles=custom_url,
            name='Custom Tile Layer',
            attr='Custom Attribution'
        )
        tile_layer.add_to(m)

# Display the map in the Streamlit app

with col1:
    st_folium(m, width=800, height=600)
