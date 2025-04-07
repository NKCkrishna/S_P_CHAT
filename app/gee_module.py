import ee
import folium
import io
import numpy as np
from PIL import Image
from folium import Map, TileLayer
from streamlit.components.v1 import html
import os
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent))

# Initialize GEE with error handling
def initialize_gee():
    try:
        # Check if running on Windows
        if os.name == 'nt':
            # Windows-specific initialization
            ee.Authenticate()
        ee.Initialize()
        return True
    except Exception as e:
        print("⚠️ GEE Initialization failed:", e)
        return False

# Initialize GEE
gee_initialized = initialize_gee()

def get_ndvi(lat, lon):
    if not gee_initialized:
        print("⚠️ GEE not initialized, returning default NDVI value")
        return 0.0
        
    try:
        point = ee.Geometry.Point([lon, lat])
        collection = ee.ImageCollection('MODIS/061/MOD13A2') \
            .filterDate('2023-01-01', '2023-12-31') \
            .filterBounds(point) \
            .select('NDVI')

        image = collection.mean()

        ndvi_value = image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=point,
            scale=500,
            maxPixels=1e9
        ).get('NDVI').getInfo()

        return ndvi_value if ndvi_value is not None else 0.0
    except Exception as e:
        print("⚠️ NDVI Fetch Error:", e)
        return 0.0


def get_ndvi_image(lat, lon):
    if not gee_initialized:
        print("⚠️ GEE not initialized, cannot generate NDVI image")
        return None
        
    try:
        point = ee.Geometry.Point([lon, lat])
        image = ee.ImageCollection('MODIS/061/MOD13A2') \
            .filterDate('2023-01-01', '2023-12-31') \
            .filterBounds(point) \
            .select('NDVI') \
            .mean() \
            .clip(point.buffer(10000))  # 10km buffer

        # Visualization parameters
        vis_params = {
            'min': -1,
            'max': 1,
            'palette': ['red', 'yellow', 'green']
        }

        # Create a map centered on the point
        m = Map(location=[lat, lon], zoom_start=10)
        
        # Add the NDVI layer
        m.add_ee_layer(image, vis_params, 'NDVI')
        
        # Add a marker for the point
        folium.Marker([lat, lon]).add_to(m)
        
        # Convert to HTML
        html_string = m.get_root().render()
        
        return html_string
    except Exception as e:
        print("⚠️ NDVI Image Error:", e)
        return None
