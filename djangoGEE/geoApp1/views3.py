from django.shortcuts import render
import os
import folium
import geopandas as gpd
from folium import GeoJson
import ee
import geemap

def home(request):
    shp_dir = os.path.join(os.getcwd(), 'media', 'shp')

    m = folium.Map(location=[25, 67], zoom_start=5)

    # Styling for different layers
    style_pakistan_districts_dd = {'fillColor': '#228B22', 'color': '#228B22'}
    # Define other styles as needed...

    # Load GeoJSON data from shapefiles
    layers = [
        ('Pakistan_Districts', 'District_Boundary.shp', style_pakistan_districts_dd),
        # Add other layers here...
    ]

    for name, shapefile, style in layers:
        data = gpd.read_file(os.path.join(shp_dir, shapefile))
        data_geojson = data.to_crs("EPSG:4326").to_json()

        # Create a style function that takes feature and style as arguments
        def style_function(feature, style=style):
            return {
                'fillColor': style['fillColor'],
                'color': style['color']
            }

        GeoJson(data_geojson, name=name, style_function=style_function).add_to(m)

    # Earth Engine and geemap code (uncommented if authentication is resolved)
    # Authenticate the API using your credentials (only need to run this once)
    ee.Authenticate()

    # Initialize the Earth Engine API
    ee.Initialize()

    # Define the region of interest (ROI) as a geometry
    roi = ee.Geometry.Rectangle([67.56084171593015, 26.467647606743032,
                                  67.71053043663328, 28.467647606743032])

    # Load Sentinel-2 dataset
    s2_dataset = ee.ImageCollection('COPERNICUS/S2').filterBounds(roi) \
        .filterDate('2019-01-01', '2020-01-01')  # Define the date range

    # Get the first image in the collection
    image = s2_dataset.first()

    # Select the bands you need
    bands = ['B2', 'B3', 'B4']  # Customize according to your needs

    # Select the region and scale of the image
    image = image.select(bands).clip(roi)  # Adjust scale as needed

    # Use geemap to display the image (optional)
    Map = geemap.Map()
    Map.centerObject(roi, zoom=10)
    Map.addLayer(image, {'bands': bands, 'min': 0, 'max': 3000}, 'Sentinel-2 Image')
    # Map

    folium.LayerControl().add_to(m)

    m = m._repr_html_()
    context = {'my_map': m}
    return render(request, 'geoApp/home.html', context)
