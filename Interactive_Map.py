import streamlit as st
import folium
import geopandas as gpd
import json
import geemap.foliumap as geemap
import ee
import pandas as pd
import os
from google.auth.transport.requests import Request
import google.auth.exceptions
from streamlit.components.v1 import html

# Path to your shapefiles and service account key
SHAPEFILE_DIR = 'C:/Users/piv/Desktop/y/media/shp'

def initialize_gee():
    service = os.getenv('SA')
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gee', 'ee-muzzamil1-37ebc3dece52.json')
    credentials = ee.ServiceAccountCredentials(service, file)
    try:
        ee.Initialize(credentials)
        st.success("Google Earth Engine initialized successfully.")
    except google.auth.exceptions.RefreshError:
        try:
            request = Request()
            credentials.refresh(request)
            ee.Initialize(credentials)
            st.success("Google Earth Engine token refreshed and initialized successfully.")
        except Exception as e:
            st.error(f"Error refreshing Google Earth Engine token: {e}")
    except Exception as e:
        st.error(f"Error initializing Google Earth Engine: {e}")

def create_folium_map(selected_dataset, ee_object, start_date_str, end_date_str):
    folium_map = folium.Map(location=[25.5973518, 65.54495724], zoom_start=7)

    try:
        if selected_dataset == "Modis":
            dataset = ee.ImageCollection('MODIS/006/MOD13Q1') \
                .filter(ee.Filter.date(start_date_str, end_date_str)) \
                .filterBounds(ee_object)
            
            def clip_image(img):
                return img.clip(ee_object).select('NDVI')
            
            clipped_collection = dataset.map(clip_image)
            modis_ndvi = clipped_collection.mean()
            vis_params_ndvi = {
                'min': 0,
                'max': 9000,
                'palette': ['FE8374', 'C0E5DE', '3A837C', '034B48']
            }
            modis_ndvi_map_id = modis_ndvi.getMapId(vis_params_ndvi)
            folium.TileLayer(
                tiles=modis_ndvi_map_id['tile_fetcher'].url_format,
                attr='Google Earth Engine',
                name='NDVI',
                overlay=True,
                control=True
            ).add_to(folium_map)

        elif selected_dataset == "dataset_nighttime":
            dataset_nighttime = ee.ImageCollection('NOAA/VIIRS/DNB/MONTHLY_V1/VCMCFG') \
                .filter(ee.Filter.date(start_date_str, end_date_str))
            
            nighttime = dataset_nighttime.select('avg_rad').mosaic()
            nighttime_clipped = nighttime.clip(ee_object)
            nighttime_vis = {
                'min': 0.0,
                'max': 60.0,
                'palette': ['1a3678', '2955bc', '5699ff', '8dbae9', 'acd1ff', 'caebff', 'e5f9ff', 'fdffb4', 'ffe6a2', 'ffc969', 'ffa12d', 'ff7c1f', 'ca531a', 'ff0000', 'ab0000']
            }
            nighttime_map_id = nighttime_clipped.getMapId(nighttime_vis)
            folium.TileLayer(
                tiles=nighttime_map_id['tile_fetcher'].url_format,
                attr='Google Earth Engine',
                name='Nighttime Lights',
                overlay=True,
                control=True
            ).add_to(folium_map)

        elif selected_dataset == "precipitation":
            dataset_precipitation = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY') \
                .filter(ee.Filter.date(start_date_str, end_date_str))
            
            precipitation = dataset_precipitation.mosaic().clip(ee_object)
            precip_vis = {
                'min': 0,
                'max': 300,
                'palette': ['blue', 'cyan', 'lime', 'yellow', 'red']
            }
            precip_map_id = precipitation.getMapId(precip_vis)
            folium.TileLayer(
                tiles=precip_map_id['tile_fetcher'].url_format,
                attr='Google Earth Engine',
                name='Precipitation',
                overlay=True,
                control=True
            ).add_to(folium_map)

        elif selected_dataset == "GlobalSurfaceWater":
            st.warning("GlobalSurfaceWater dataset is not configured.")
        
        elif selected_dataset == "WorldPop":
            dataset = ee.ImageCollection('WorldPop/GP/100m/pop') \
                .filterBounds(ee_object) \
                .filter(ee.Filter.date(start_date_str, end_date_str))
            
            population = dataset.mean().clip(ee_object)
            pop_vis = {
                'min': 0,
                'max': 1000,
                'palette': ['blue', 'green', 'yellow', 'red']
            }
            pop_map_id = population.getMapId(pop_vis)
            folium.TileLayer(
                tiles=pop_map_id['tile_fetcher'].url_format,
                attr='Google Earth Engine',
                name='World Population',
                overlay=True,
                control=True
            ).add_to(folium_map)

        elif selected_dataset == "COPERNICUS":
            dataset = ee.ImageCollection('COPERNICUS/S2') \
                .filterBounds(ee_object) \
                .filter(ee.Filter.date(start_date_str, end_date_str))
            
            sentinel = dataset.median().clip(ee_object)
            vis_params = {
                'bands': ['B4', 'B3', 'B2'],
                'min': 0,
                'max': 3000,
                'gamma': 1.4
            }
            copernicus_map_id = sentinel.getMapId(vis_params)
            folium.TileLayer(
                tiles=copernicus_map_id['tile_fetcher'].url_format,
                attr='Google Earth Engine',
                name='Copernicus Sentinel-2',
                overlay=True,
                control=True
            ).add_to(folium_map)

        folium_map.add_child(folium.LayerControl())
    except Exception as e:
        st.error(f"Error processing dataset: {e}")

    folium_map_html = folium_map._repr_html_()
    return folium_map_html

def handle_submit(selected_dataset, selected_date_range_From, selected_date_range_To, selected_shape):
    shapefile_name = f'{selected_shape}.shp'
    shapefile_path = os.path.join(SHAPEFILE_DIR, shapefile_name)

    if os.path.exists(shapefile_path):
        try:
            roi_gdf = gpd.read_file(shapefile_path)
            roi_geojson = roi_gdf.to_crs("EPSG:4326").to_json()
        except Exception as e:
            st.error(f"Error reading shapefile: {e}")
            return
        
        try:
            ee_object = geemap.geojson_to_ee(json.loads(roi_geojson))
        except Exception as e:
            st.error(f"Error converting GeoJSON to Earth Engine object: {e}")
            return
        
        st.markdown("### Satellite Data Map")
        folium_map_html = create_folium_map(
            selected_dataset,
            ee_object,
            selected_date_range_From.strftime('%Y-%m-%d'),
            selected_date_range_To.strftime('%Y-%m-%d')
        )
        html(folium_map_html, height=600)
    else:
        st.error("Selected shapefile does not exist.")

def submit_control():
    selected_dataset = st.sidebar.selectbox(
        "Select Dataset", 
        ["Modis", "dataset_nighttime", 'precipitation', 'GlobalSurfaceWater', 'WorldPop', 'COPERNICUS']
    )

    selected_date_range_From = st.sidebar.date_input("From", value=pd.to_datetime("2015-07-01"))
    selected_date_range_To = st.sidebar.date_input("To", value=pd.to_datetime("2023-09-30"))

    shape_options = [
        'District_Boundary', 'hydro_basins', 'karachi', 
        'National_Constituency_with_Projected_2010_Population', 
        'Provincial_Boundary', 'Provincial_Constituency', 
        'Tehsil_Boundary', 'Union_Council'
    ]

    selected_shape = st.sidebar.selectbox("Select Shape", shape_options)

    if st.sidebar.button("Submit"):
        st.session_state.selected_dataset = selected_dataset
        st.session_state.selected_date_range_From = selected_date_range_From
        st.session_state.selected_date_range_To = selected_date_range_To
        st.session_state.selected_shape = selected_shape
        st.session_state.submitted = True
    else:
        st.session_state.submitted = False

    if 'submitted' in st.session_state and st.session_state.submitted:
        handle_submit(
            st.session_state.selected_dataset,
            st.session_state.selected_date_range_From,
            st.session_state.selected_date_range_To,
            st.session_state.selected_shape
        )

def main():
    st.set_page_config(layout="wide")
    st.title("Satellite Data Visualization, Interactive Map")

    initialize_gee()
    submit_control()

if __name__ == "__main__":
    main()
