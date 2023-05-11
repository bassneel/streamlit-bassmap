import streamlit as st
import bassmap
import tempfile
import os
import numpy as np

tmp_dir = tempfile.TemporaryDirectory()

col1, col2 = st.columns([6, 4])

def get_truecolor(red_band, green_band, blue_band, georef):

    from osgeo import gdal

    # Combine the three bands into a single 3D array with 3 bands
    true_color = np.array([red_band, green_band, blue_band], dtype=np.uint16)

    # Get the dimensions and georeferencing information from one of the input files
    xsize = georef.RasterXSize
    ysize = georef.RasterYSize
    proj = georef.GetProjection()
    geotrans = georef.GetGeoTransform()
    driver = gdal.GetDriverByName('GTiff')

    # Create a new TIFF file and write the NDVI array to it
    true_color_path = os.path.join(tmp_dir.name, 'true_color_comp.tif')
    true_color_ds = driver.Create(true_color_path, xsize, ysize, 3, gdal.GDT_Float32)
    
    if true_color_ds is not None:
        true_color_ds.SetProjection(proj)
        true_color_ds.SetGeoTransform(geotrans)
        true_color_ds.GetRasterBand(1).WriteArray(true_color[0])
        true_color_ds.GetRasterBand(2).WriteArray(true_color[1])
        true_color_ds.GetRasterBand(3).WriteArray(true_color[2])
        true_color_ds.FlushCache()

    else:
        raise Exception("Failed to create TIFF file")
    
    return true_color_path

def get_truecolor_st(red_band_file, green_band_file, blue_band_file, georef_file):
    # Create temporary directory to store uploaded files
    tmp_dir = tempfile.TemporaryDirectory()

    from osgeo import gdal

    # Save uploaded files to temporary directory
    red_band_path = os.path.join(tmp_dir.name, 'red_band.tif')
    with open(red_band_path, 'wb') as f:
        f.write(red_band_file.read())
    green_band_path = os.path.join(tmp_dir.name, 'green_band.tif')
    with open(green_band_path, 'wb') as f:
        f.write(green_band_file.read())
    blue_band_path = os.path.join(tmp_dir.name, 'blue_band.tif')
    with open(blue_band_path, 'wb') as f:
        f.write(blue_band_file.read())
    georef_path = os.path.join(tmp_dir.name, 'georef.tif')
    with open(georef_path, 'wb') as f:
        f.write(georef_file.read())

    # Read uploaded files using GDAL and convert to numpy arrays
    red_band = gdal.Open(red_band_path).ReadAsArray()
    green_band = gdal.Open(green_band_path).ReadAsArray()
    blue_band = gdal.Open(blue_band_path).ReadAsArray()
    georef = gdal.Open(georef_path)

    # Generate true-color image and get path to created file
    true_color_path = get_truecolor(red_band, green_band, blue_band, georef)

    # Download the file using Streamlit's download button
    with open(true_color_path, "rb") as f:
        bytes = f.read()
        st.download_button(
            label="Download true color image",
            data=bytes,
            file_name=os.path.basename(true_color_path),
            mime="image/tiff",
        )

st.title("Landsat 8 Tools")

st.header("Upload files")

# File upload widgets
red_band = st.file_uploader("Upload red band file")
green_band = st.file_uploader("Upload green band file")
blue_band = st.file_uploader("Upload blue band file")
georef = st.file_uploader("Upload georeference file")

# Button to generate true-color image
if st.button("Generate true color image"):
    if red_band and green_band and blue_band and georef:
        # Generate and download true-color image
        get_truecolor_st(red_band, green_band, blue_band, georef)
    else:
        st.warning("Please upload all required files.")
