import streamlit as st

st.title('BassMap')
st.image('https://rawgithubusercontent.com/bassneel/basspublicfiles/blob/main/bassmap_logo.png')
st.divider()
st.markdown("""
    BassMap is an intuitive Python Package that allows the user to display a variety of features on an iPyLeaflet and Folium map display. In addition the Landsat 8 Tools allows the user to create a variety of multispectral composites using local GeoTIFFs from Landsat 8 spectral bands
""")
st.divider()
st.subheader('Features')

st.markdown("""
-   [Landsat 8 Tools](https://bassneel.github.io/bassmap/examples/Landsat_8_Tools/)
    -   Multispectral Composites
        -   Create True Color Composite
        -   Create False Color (Buildings) Composite
        -   Create Color Infrared (Vegetation) Composite
        -   Create Healthy Vegetation Composite
    -   Spectral Indicies
        -   Create Normalized Difference Moisture Index (NDMI) Composite
        -   Create Normalized Difference Vegetation Index (NDVI) Composite


-   With IPyLeaflet ([Mapomatic](https://bassneel.github.io/bassmap/examples/Mapomatic/))
    -   Change basemap
    -   Display shapefiles
    -   Display GeoJSON files
    -   Display vector files
    -   Display Cloud Optimized GeoTIFFs
    
-   With Folium ([Foliumatic](https://bassneel.github.io/bassmap/examples/Foliumatic/))
    -   Change basemap
    -   Display shapefiles
    -   Display GeoJSON files
    -   Display vector files
""")
st.divider()
st.subheader('Demo')

# Add your demo code here
st.divider()
st.subheader('Credits')

st.markdown("""
This package was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [giswqs/pypackage](https://github.com/giswqs/pypackage) project template.
""")
