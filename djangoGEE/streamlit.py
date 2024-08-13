import streamlit as st
import folium
from folium import GeoJson
import geopandas as gpd
import json
import geemap
import ee
import pandas as pd

# Initialize Earth Engine
ee.Initialize()

def main():
    st.title("Geospatial Data Viewer")
    
    # Sidebar for user inputs
    st.sidebar.header("Inputs")
    
    selected_dataset = st.sidebar.selectbox('Select Dataset', ['Modis'])
    selected_shapefile = st.sidebar.file_uploader('Upload Shapefile', type=['shp'])
    
    selected_date_range_From = st.sidebar.date_input('Start Date', value=pd.to_datetime('2015-07-01'))
    selected_date_range_To = st.sidebar.date_input('End Date', value=pd.to_datetime('2019-11-30'))
    
    if selected_shapefile is not None:
        shapefile_path = f'./temp_shapefile.shp'
        with open(shapefile_path, 'wb') as f:
            f.write(selected_shapefile.read())
        
        # Read the uploaded shapefile
        roi_gdf = gpd.read_file(shapefile_path)
        roi_geojson = roi_gdf.to_crs("EPSG:4326").to_json()

        # Create a folium map
        figure = folium.Figure()
        m = folium.Map(location=[25.5973518, 65.54495724], zoom_start=7)
        m.add_to(figure)

        # Add GeoJson layer
        roi_geojson_layer = GeoJson(roi_geojson, name='ROI GeoJSON')
        roi_geojson_layer.add_to(m)

        # Convert the GeoJSON content to Earth Engine object
        ee_object = geemap.geojson_to_ee(json.loads(roi_geojson))
        
        if selected_dataset == "Modis":
            F = selected_date_range_From.strftime('%Y-%m-%d')
            T = selected_date_range_To.strftime('%Y-%m-%d')
            
            # Fetch MODIS data from Earth Engine
            dataset = ee.ImageCollection('MODIS/006/MOD13Q1').filter(ee.Filter.date(F, T)).filterBounds(ee_object)
            modisndvi = dataset.select('NDVI').clip(ee_object)
            
            vis_paramsNDVI = {
                'min': 0,
                'max': 9000,
                'palette': ['FE8374', 'C0E5DE', '3A837C', '034B48']
            }
            map_id_dict = ee.Image(modisndvi.mean()).getMapId(vis_paramsNDVI)  # Use mean image for visualization
            
            folium.raster_layers.TileLayer(
                tiles=map_id_dict['tile_fetcher'].url_format,
                attr='Google Earth Engine',
                name='NDVI',
                overlay=True,
                control=True
            ).add_to(m)

        m.add_child(folium.LayerControl())
        
        # Render the map in Streamlit
        st_data = st.components.v1.html(figure.render(), height=600, scrolling=True)
    
if __name__ == "__main__":
    main()
