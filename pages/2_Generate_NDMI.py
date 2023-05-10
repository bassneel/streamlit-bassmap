import streamlit as st
import numpy as np
from osgeo import gdal

def ndmi_composite(nir_band, swir_band):

    # Load the red and NIR bands as NumPy arrays
    nir = gdal.Open(nir_band.name).ReadAsArray()
    swir = gdal.Open(swir_band.name).ReadAsArray()

    # Scale the input bands to the range of 0-255
    nir_band = (nir_band / 65535.0) * 255.0
    swir_band = (swir_band / 65535.0) * 255.0

    # Calculate the NDMI from the NIR and SWIR bands
    ndmi = np.empty_like(nir_band, dtype=np.float32)
    ndmi.fill(np.nan)
    valid = np.logical_and(nir_band != 0, swir_band != 0)
    ndmi[valid] = (nir_band[valid] - swir_band[valid]) / (nir_band[valid] + swir_band[valid])

    # Get the dimensions and georeferencing information from one of the input files
    nir_ds = gdal.Open(nir_band.name)
    xsize = nir_ds.RasterXSize
    ysize = nir_ds.RasterYSize
    proj = nir_ds.GetProjection()
    geotrans = nir_ds.GetGeoTransform()
    driver = gdal.GetDriverByName('GTiff')

    # Create a new TIFF file and write the NDMI array to it
    ndmi_ds = driver.Create('ndmi_composite.tif', xsize, ysize, 1, gdal.GDT_Float32)
    ndmi_ds.SetProjection(proj)
    ndmi_ds.SetGeoTransform(geotrans)
    ndmi_ds.GetRasterBand(1).WriteArray(ndmi)
    ndmi_ds.FlushCache()

    return ndmi

# Set up the Streamlit app
st.title('NDMI Composite App')
st.write('Upload a Landsat 8 NIR(5) and SWIR band(6) to generate an NDMI composite')

# Allow the user to upload the red and NIR bands
nir_band = st.file_uploader('Upload NIR band (band 5)')
swir_band = st.file_uploader('Upload WWIR band (band 6)')

# Process the bands and show the resulting NDMI composite
if nir_band and swir_band:
    ndmi = ndmi_composite(nir_band, swir_band)
    st.image(ndmi, caption='NDMI Composite')
    st.download_button('Download NDMI Composite', 'ndmi_composite.tif', 'Click to download the NDMI composite')