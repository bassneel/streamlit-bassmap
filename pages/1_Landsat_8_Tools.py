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

def get_color_infrared(nir_band, red_band, green_band, georef):

    from osgeo import gdal

    # Combine the three bands into a single 3D array with 3 bands
    color_infrared = np.array([nir_band, red_band, green_band], dtype=np.uint16)

    # Get the dimensions and georeferencing information from one of the input files
    xsize = georef.RasterXSize
    ysize = georef.RasterYSize
    proj = georef.GetProjection()
    geotrans = georef.GetGeoTransform()
    driver = gdal.GetDriverByName('GTiff')

    # Create a new TIFF file and write the NDVI array to it
    color_infrared_path = os.path.join(tmp_dir.name, 'color_infrared_comp.tif')
    color_infrared_ds = driver.Create(color_infrared_path, xsize, ysize, 3, gdal.GDT_Float32)
    
    if color_infrared_ds is not None:
        color_infrared_ds.SetProjection(proj)
        color_infrared_ds.SetGeoTransform(geotrans)
        color_infrared_ds.GetRasterBand(1).WriteArray(color_infrared[0])
        color_infrared_ds.GetRasterBand(2).WriteArray(color_infrared[1])
        color_infrared_ds.GetRasterBand(3).WriteArray(color_infrared[2])
        color_infrared_ds.FlushCache()

    else:
        raise Exception("Failed to create TIFF file")
        
    return color_infrared_path

def get_false_color(swir2_band, swir_band, red_band, georef):

    from osgeo import gdal

    # Combine the three bands into a single 3D array with 3 bands
    false_color = np.array([swir2_band, swir_band, red_band], dtype=np.uint16)

    # Get the dimensions and georeferencing information from one of the input files
    xsize = georef.RasterXSize
    ysize = georef.RasterYSize
    proj = georef.GetProjection()
    geotrans = georef.GetGeoTransform()
    driver = gdal.GetDriverByName('GTiff')

    # Create a new TIFF file and write the NDVI array to it
    false_color_path = os.path.join(tmp_dir.name, 'false_color_comp.tif')
    false_color_ds = driver.Create(false_color_path, xsize, ysize, 3, gdal.GDT_Float32)
    
    if false_color_ds is not None:
        false_color_ds.SetProjection(proj)
        false_color_ds.SetGeoTransform(geotrans)
        false_color_ds.GetRasterBand(1).WriteArray(false_color[0])
        false_color_ds.GetRasterBand(2).WriteArray(false_color[1])
        false_color_ds.GetRasterBand(3).WriteArray(false_color[2])
        false_color_ds.FlushCache()

    else:
        raise Exception("Failed to create TIFF file")
        
    return false_color_path

def get_health_veg(nir_band, swir_band, blue_band, georef):

    from osgeo import gdal

    # Combine the three bands into a single 3D array with 3 bands
    healthy_veg = np.array([nir_band, swir_band, blue_band], dtype=np.uint16)

    # Get the dimensions and georeferencing information from one of the input files
    xsize = georef.RasterXSize
    ysize = georef.RasterYSize
    proj = georef.GetProjection()
    geotrans = georef.GetGeoTransform()
    driver = gdal.GetDriverByName('GTiff')

    # Create a new TIFF file and write the composite array to it
    healthy_veg_ds = driver.Create('/tmp/healthy_veg_comp.tif', xsize, ysize, 3, gdal.GDT_UInt16)
        
    # Create a new TIFF file and write the NDVI array to it
    healthy_veg_path = os.path.join(tmp_dir.name, 'healthy_veg_comp.tif')
    healthy_veg_ds = driver.Create(healthy_veg_path, xsize, ysize, 3, gdal.GDT_Float32)
    
    if healthy_veg_ds is not None:
        healthy_veg_ds.SetProjection(proj)
        healthy_veg_ds.SetGeoTransform(geotrans)
        healthy_veg_ds.GetRasterBand(1).WriteArray(healthy_veg[0])
        healthy_veg_ds.GetRasterBand(2).WriteArray(healthy_veg[1])
        healthy_veg_ds.GetRasterBand(3).WriteArray(healthy_veg[2])
        healthy_veg_ds.FlushCache()

    else:
        raise Exception("Failed to create TIFF file")
        
    return healthy_veg_path

def get_ndmi(nir_band, swir_band, georef):

    from osgeo import gdal

    # Scale the input bands to the range of 0-255
    nir_band = (nir_band / 65535.0) * 255.0
    swir_band = (swir_band / 65535.0) * 255.0

    # Calculate the NDMI from the NIR and SWIR bands
    ndmi = np.empty_like(nir_band, dtype=np.float32)
    ndmi.fill(np.nan)
    valid = np.logical_and(nir_band != 0, swir_band != 0)
    ndmi[valid] = (nir_band[valid] - swir_band[valid]) / (nir_band[valid] + swir_band[valid])

    # Get the dimensions and georeferencing information from one of the input files
    xsize = georef.RasterXSize
    ysize = georef.RasterYSize
    proj = georef.GetProjection()
    geotrans = georef.GetGeoTransform()
    driver = gdal.GetDriverByName('GTiff')

    # Create a new TIFF file and write the NDVI array to it
    ndmi_path = os.path.join(tmp_dir.name, 'ndmi_composite.tif')
    ndmi_ds = driver.Create(ndmi_path, xsize, ysize, 1, gdal.GDT_Float32)
    
    if ndmi_ds is not None:
        ndmi_ds.SetProjection(proj)
        ndmi_ds.SetGeoTransform(geotrans)
        ndmi_ds.GetRasterBand(1).WriteArray(ndmi)
        ndmi_ds.FlushCache()
    else:
        raise Exception("Failed to create TIFF file")
        
    return ndmi_path

def get_NDVI(red_band, nir_band, georef):

    from osgeo import gdal
    
    # Scale the input bands to the range of 0-255
    red_band = (red_band / 65535.0) * 255.0
    nir_band = (nir_band / 65535.0) * 255.0

    # Calculate the NDVI from the NIR and Red bands
    ndvi = np.empty_like(nir_band, dtype=np.float32)
    ndvi.fill(np.nan)
    valid = np.logical_and(red_band != 0, nir_band != 0)
    ndvi[valid] = (nir_band[valid] - red_band[valid]) / (nir_band[valid] + red_band[valid])

    # Get the dimensions and georeferencing information from one of the input files
    xsize = georef.RasterXSize
    ysize = georef.RasterYSize
    proj = georef.GetProjection()
    geotrans = georef.GetGeoTransform()
    driver = gdal.GetDriverByName('GTiff')

    # Create a new TIFF file and write the NDVI array to it
    ndvi_path = os.path.join(tmp_dir.name, 'ndvi_composite.tif')
    ndvi_ds = driver.Create(ndvi_path, xsize, ysize, 1, gdal.GDT_Float32)
    
    if ndvi_ds is not None:
        ndvi_ds.SetProjection(proj)
        ndvi_ds.SetGeoTransform(geotrans)
        ndvi_ds.GetRasterBand(1).WriteArray(ndvi)
        ndvi_ds.FlushCache()
    else:
        raise Exception("Failed to create TIFF file")
        
    return ndvi_path

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

def get_colorinfrared_st(nir_band_file, red_band_file, green_band_file, georef_file):
    # Create temporary directory to store uploaded files
    tmp_dir = tempfile.TemporaryDirectory()

    from osgeo import gdal

    # Save uploaded files to temporary directory
    nir_band_path = os.path.join(tmp_dir.name, 'nir_band.tif')
    with open(nir_band_path, 'wb') as f:
        f.write(nir_band_file.read())
    red_band_path = os.path.join(tmp_dir.name, 'red_band.tif')
    with open(red_band_path, 'wb') as f:
        f.write(red_band_file.read())
    green_band_path = os.path.join(tmp_dir.name, 'green_band.tif')
    with open(green_band_path, 'wb') as f:
        f.write(green_band_file.read())
    georef_path = os.path.join(tmp_dir.name, 'georef.tif')
    with open(georef_path, 'wb') as f:
        f.write(georef_file.read())

    # Read uploaded files using GDAL and convert to numpy arrays
    nir_band = gdal.Open(nir_band_path).ReadAsArray()
    red_band = gdal.Open(red_band_path).ReadAsArray()
    green_band = gdal.Open(green_band_path).ReadAsArray()
    georef = gdal.Open(georef_path)

    # Generate image and get path to created file
    color_infrared_path = get_color_infrared(nir_band, red_band, green_band, georef)

    # Download the file using Streamlit's download button
    with open(color_infrared_path, "rb") as f:
        bytes = f.read()
        st.download_button(
            label="Download color infrared image",
            data=bytes,
            file_name=os.path.basename(color_infrared_path),
            mime="image/tiff",
        )

def get_false_color_st(swir2_band_file, swir_band_file, red_band_file, georef_file):
    # Create temporary directory to store uploaded files
    tmp_dir = tempfile.TemporaryDirectory()

    from osgeo import gdal

    # Save uploaded files to temporary directory
    swir_band_path = os.path.join(tmp_dir.name, 'swir_band.tif')
    with open(swir_band_path, 'wb') as f:
        f.write(swir_band_file.read())
    swir2_band_path = os.path.join(tmp_dir.name, 'swir2_band.tif')
    with open(swir2_band_path, 'wb') as f:
        f.write(swir2_band_file.read())
    red_band_path = os.path.join(tmp_dir.name, 'red_band.tif')
    with open(red_band_path, 'wb') as f:
        f.write(red_band_file.read())
    georef_path = os.path.join(tmp_dir.name, 'georef.tif')
    with open(georef_path, 'wb') as f:
        f.write(georef_file.read())

    # Read uploaded files using GDAL and convert to numpy arrays
    swir_band = gdal.Open(swir_band_path).ReadAsArray()
    swir2_band = gdal.Open(swir_band_path).ReadAsArray()
    red_band = gdal.Open(red_band_path).ReadAsArray()
    georef = gdal.Open(georef_path)

    # Generate image and get path to created file
    false_color_path = get_false_color(swir2_band, swir_band, red_band, georef)

    # Download the file using Streamlit's download button
    with open(false_color_path, "rb") as f:
        bytes = f.read()
        st.download_button(
            label="Download false color image",
            data=bytes,
            file_name=os.path.basename(false_color_path),
            mime="image/tiff",
        )

def get_health_veg_st(nir_band_file, swir_band_file, blue_band_file, georef_file):
    # Create temporary directory to store uploaded files
    tmp_dir = tempfile.TemporaryDirectory()

    from osgeo import gdal

    # Save uploaded files to temporary directory
    nir_band_path = os.path.join(tmp_dir.name, 'nir_band.tif')
    with open(nir_band_path, 'wb') as f:
        f.write(nir_band_file.read())
    swir_band_path = os.path.join(tmp_dir.name, 'swir_band.tif')
    with open(swir_band_path, 'wb') as f:
        f.write(swir_band_file.read())
    blue_band_path = os.path.join(tmp_dir.name, 'blue_band.tif')
    with open(blue_band_path, 'wb') as f:
        f.write(blue_band_file.read())
    georef_path = os.path.join(tmp_dir.name, 'georef.tif')
    with open(georef_path, 'wb') as f:
        f.write(georef_file.read())

    # Read uploaded files using GDAL and convert to numpy arrays
    nir_band = gdal.Open(nir_band_path).ReadAsArray()
    swir_band = gdal.Open(swir_band_path).ReadAsArray()
    blue_band = gdal.Open(blue_band_path).ReadAsArray()
    georef = gdal.Open(georef_path)

    # Generate image and get path to created file
    healthy_veg_path = get_health_veg(nir_band, swir_band, blue_band, georef)

    # Download the file using Streamlit's download button
    with open(healthy_veg_path, "rb") as f:
        bytes = f.read()
        st.download_button(
            label="Download healthy vegetation image",
            data=bytes,
            file_name=os.path.basename(healthy_veg_path),
            mime="image/tiff",
        )

def get_ndmi_st(nir_band_file, swir_band_file, georef_file):
    # Create temporary directory to store uploaded files
    tmp_dir = tempfile.TemporaryDirectory()

    from osgeo import gdal

    # Save uploaded files to temporary directory
    nir_band_path = os.path.join(tmp_dir.name, 'nir_band.tif')
    with open(nir_band_path, 'wb') as f:
        f.write(nir_band_file.read())
    swir_band_path = os.path.join(tmp_dir.name, 'swir_band.tif')
    with open(swir_band_path, 'wb') as f:
        f.write(swir_band_file.read())
    georef_path = os.path.join(tmp_dir.name, 'georef.tif')
    with open(georef_path, 'wb') as f:
        f.write(georef_file.read())

    # Read uploaded files using GDAL and convert to numpy arrays
    nir_band = gdal.Open(nir_band_path).ReadAsArray()
    swir_band = gdal.Open(swir_band_path).ReadAsArray()
    georef = gdal.Open(georef_path)

    # Generate image and get path to created file
    ndmi_path = get_ndmi(nir_band, swir_band, georef)

    # Download the file using Streamlit's download button
    with open(ndmi_path, "rb") as f:
        bytes = f.read()
        st.download_button(
            label="Download NDMI image",
            data=bytes,
            file_name=os.path.basename(ndmi_path),
            mime="image/tiff",
        )

def get_ndvi_st(red_band_file, nir_band_file, georef_file):
    # Create temporary directory to store uploaded files
    tmp_dir = tempfile.TemporaryDirectory()

    from osgeo import gdal

    # Save uploaded files to temporary directory
    red_band_path = os.path.join(tmp_dir.name, 'red_band.tif')
    with open(red_band_path, 'wb') as f:
        f.write(red_band_file.read())
    nir_band_path = os.path.join(tmp_dir.name, 'nir_band.tif')
    with open(nir_band_path, 'wb') as f:
        f.write(nir_band_file.read())
    georef_path = os.path.join(tmp_dir.name, 'georef.tif')
    with open(georef_path, 'wb') as f:
        f.write(georef_file.read())

    # Read uploaded files using GDAL and convert to numpy arrays
    red_band = gdal.Open(red_band_path).ReadAsArray()
    nir_band = gdal.Open(nir_band_path).ReadAsArray()
    georef = gdal.Open(georef_path)

    # Generate image and get path to created file
    ndvi_path = get_NDVI(red_band, nir_band, georef)

    # Download the file using Streamlit's download button
    with open(ndvi_path, "rb") as f:
        bytes = f.read()
        st.download_button(
            label="Download NDVI image",
            data=bytes,
            file_name=os.path.basename(ndvi_path),
            mime="image/tiff",
        )

st.title("Landsat 8 Tools")

col1, col2 = st.columns([1, 1])

with col1:
    st.header("Upload files")

    # File upload widgets
    red_band = st.file_uploader("Upload red band (4) file")
    green_band = st.file_uploader("Upload green band (3) file")
    blue_band = st.file_uploader("Upload blue band file (2)")
    nir_band = st.file_uploader("Upload near infrared band (5) file")
    swir_band = st.file_uploader("Upload shortwave infrared band (6) file")
    swir2_band = st.file_uploader("Upload shortwave infrared band (7) file")
    georef = st.file_uploader("Upload georeference file")

with col2:
    st.header("Download Composites")
    # Button to generate true-color image
    if st.button("Generate true color image"):
        if red_band and green_band and blue_band and georef:
            # Generate and download image
            get_truecolor_st(red_band, green_band, blue_band, georef)
        else:
            st.warning("Please upload all required files.")

    # Button to generate false color image
    if st.button("Generate false color image"):
        if red_band and green_band and blue_band and georef:
            # Generate and download image
            get_truecolor_st(red_band, green_band, blue_band, georef)
        else:
            st.warning("Please upload all required files.")

    # Button to generate color infrared image
    if st.button("Generate color infrared image"):
        if red_band and green_band and blue_band and georef:
            # Generate and download image
            get_colorinfrared_st(nir_band, red_band, green_band, georef)
        else:
            st.warning("Please upload all required files.")

    # Button to generate healthy vegetation image
    if st.button("Generate healthy vegetation image"):
        if red_band and green_band and blue_band and georef:
            # Generate and download image
            get_truecolor_st(red_band, green_band, blue_band, georef)
        else:
            st.warning("Please upload all required files.")

    # Button to generate NDMI image
    if st.button("Generate NDMI image"):
        if red_band and green_band and blue_band and georef:
            # Generate and download image
            get_truecolor_st(red_band, green_band, blue_band, georef)
        else:
            st.warning("Please upload all required files.")

    # Button to generate NDVI image
    if st.button("Generate NDVI image"):
        if red_band and green_band and blue_band and georef:
            # Generate and download image
            get_truecolor_st(red_band, green_band, blue_band, georef)
        else:
            st.warning("Please upload all required files.")