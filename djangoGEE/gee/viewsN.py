from django.shortcuts import render
import geopandas as gpd
from folium import GeoJson
import json
import geemap
import folium
import ee

# Generic base view
from django.views.generic import TemplateView

ee.Initialize()

# Frontend
# Home
class Home(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        figure = folium.Figure()

        m = folium.Map(
            location=[25.5973518, 65.54495724],
            zoom_start=7,
        )
        m.add_to(figure)

        style_roi = {'fillColor': '#228B22', 'color': '#228B22'}
        roi_gdf = gpd.read_file(r'C:\Users\piv\Desktop\y\media\shp')
        roi_geojson = roi_gdf.to_crs("EPSG:4326").to_json()

        # Create a folium GeoJson layer for visualization
        roi_geojson_layer = GeoJson(roi_geojson, name='ROI GeoJSON')
        roi_geojson_layer.add_to(m)

        # Convert the GeoJSON content to an Earth Engine object
        ee_object = geemap.geojson_to_ee(json.loads(roi_geojson))

        # Get the selected dataset and year from the request
        selected_dataset = self.request.GET.get('dataset', 'landsat8')
        selected_year = self.request.GET.get('year', '2022')

        # Define date range based on the selected year
        date_start = selected_year + '-01-01'
        date_end = selected_year + '-12-31'
        date_range = ee.DateRange(ee.Date(date_start), ee.Date(date_end))

        if selected_dataset == 'landsat8':
            # Add your logic to handle Landsat 8 data
            # Example:
            dataset = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA').filterDate(date_range)
            # Clip the Landsat layer to the region defined by ee_object
            dataset_clipped = dataset.map(lambda image: image.clip(ee_object))
            # Add the Landsat layer to the map
            map_info = dataset_clipped.first().getMapId({'bands': ['B4', 'B3', 'B2'], 'min': 0, 'max': 0.3})
            tms_url = map_info['tile_fetcher']['url_format']  # Updated line
            folium.raster_layers.TileLayer(
                tiles=tms_url,
                attr='Google Earth Engine',
                name='Landsat 8',
                overlay=True,
                control=True
            ).add_to(m)
        
        elif selected_dataset == 'sentinel2':
            # Add your logic to handle Sentinel 2 data
            # Example:
            dataset = ee.ImageCollection('COPERNICUS/S2').filterDate(date_range)
            # Clip the Sentinel 2 layer to the region defined by ee_object
            dataset_clipped = dataset.map(lambda image: image.clip(ee_object))
            # Add the Sentinel 2 layer to the map
            map_info = dataset_clipped.first().getMapId({'bands': ['B4', 'B3', 'B2'], 'min': 0, 'max': 3000})
            tms_url = map_info['tile_fetcher']['url_format']  # Updated line
            folium.raster_layers.TileLayer(
                tiles=tms_url,
                attr='Google Earth Engine',
                name='Sentinel 2',
                overlay=True,
                control=True
            ).add_to(m)

        m.add_child(folium.LayerControl())
        figure.render()

        return {"map": figure}
