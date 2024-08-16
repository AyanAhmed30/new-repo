from django.shortcuts import render,redirect
import geopandas as gpd
from folium import GeoJson
import json
import geemap
import os
# generic base view
from django.views.generic import TemplateView 

# folium
import folium
from folium import plugins

# gee
import ee

#---
from .forms import *
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from .gee import type_map, data_gee
from django.contrib.auth.decorators import login_required
import geemap.foliumap as geemap
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as auth_login
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.shortcuts import render
import ee
import pandas as pd
import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize


from django.shortcuts import render
import ee
import pandas as pd
import numpy as np
from scipy import optimize
from django.http import JsonResponse
import plotly.graph_objs as go
from datetime import datetime






#e.Authenticate()
 ## Credenciales de EE


# D:\Desktop\Django_app_12_sep-2023\gee\ee-muzzamil.json

def index(request):
    
    print("I am in index")
    return render (request, "index.html")

# ee.Initialize()
@csrf_exempt

@login_required
def home(request):
    template_name = 'home.html'
    
    

    if request.method == 'GET':
        selected_dataset = request.GET.get('dataset')
        selected_shapefile = request.GET.get('shapefile')
        selected_date_range_From = request.GET.get('dateRangeFrom')
        selected_date_range_To = request.GET.get('dateRangeTo')

        print(f'Selected Dataset: {selected_dataset}')
        print(f'Selected Dataset: {selected_shapefile}')
        
    figure = folium.Figure()

    m = folium.Map(
        location=[25.5973518, 65.54495724],
        zoom_start=7,
    )
    m.add_to(figure)

#----------------------------------------------------------------------------------------------------------------------#
    if selected_dataset == "Modis":
        if selected_shapefile != None:

            shapefile_path = ('C:\\Users\\piv\\Desktop\\y\\media\\shp')
           


            roi_gdf = gpd.read_file(shapefile_path)
            roi_geojson = roi_gdf.to_crs("EPSG:4326").to_json()
            
            # Create a folium GeoJson layer for visualization
            roi_geojson_layer = folium.GeoJson(roi_geojson, name='ROI GeoJSON')
            roi_geojson_layer.add_to(m)
            
            # Convert the GeoJSON content to Earth Engine object
            ee_object = geemap.geojson_to_ee(json.loads(roi_geojson))
            if selected_date_range_From != None:
                if selected_date_range_To != None:
                    print("I am here")
                    F = selected_date_range_From
                    T = selected_date_range_To
                    print(F,"==>",T)


                    dataset = ee.ImageCollection('MODIS/006/MOD13Q1').filter(ee.Filter.date(F, T)).filterBounds(ee_object)
            
                    modisndvi = dataset.select('NDVI')

                    modisndvi = modisndvi.clip(ee_object)
                    
                    

                    vis_paramsNDVI = {
                        'min': 0,
                        'max': 9000,
                        'palette': ['FE8374', 'C0E5DE', '3A837C', '034B48']}

                    map_id_dict = ee.Image(modisndvi).getMapId(vis_paramsNDVI)
                    folium.raster_layers.TileLayer(
                        tiles=map_id_dict['tile_fetcher'].url_format,
                        attr='Google Earth Engine',
                        name='NDVI',
                        overlay=True,
                        control=True
                    ).add_to(m)
                    
                
                    
                    m.add_child(folium.LayerControl())
                    figure.render()

                else:
                    F = "2015-07-01"
                    T = "2019-11-30"
                    print("Date TO is Missing")
            else:
                F = "2015-07-01"
                T = "2019-11-30"
                print("Date From is Missing")

        else:
            pass

        






#--------------------------------------------------------------------------------------------------------------------------------#   
    elif selected_dataset == "dataset_nighttime":
        if selected_shapefile != None:

            shapefile_path = ('C:\\Users\\piv\\Desktop\\y\\media\\shp')
           
                                # D:\Desktop\final_working1-New-2023\final\media

            roi_gdf = gpd.read_file(shapefile_path)
            roi_geojson = roi_gdf.to_crs("EPSG:4326").to_json()
            
            # Create a folium GeoJson layer for visualization
            roi_geojson_layer = folium.GeoJson(roi_geojson, name='ROI GeoJSON')
            roi_geojson_layer.add_to(m)
            
            # Convert the GeoJSON content to Earth Engine object
            ee_object = geemap.geojson_to_ee(json.loads(roi_geojson))
            if selected_date_range_From != None:
                if selected_date_range_To != None:
                    print("I am here")
                    F = selected_date_range_From
                    T = selected_date_range_To
                    print(F,"==>",T)


                    dataset_nighttime = ee.ImageCollection('NOAA/VIIRS/DNB/MONTHLY_V1/VCMCFG').filter(ee.Filter.date(F, T))
              


                    # Mosaic the image collection to a single image
                    nighttime = dataset_nighttime.select('avg_rad').mosaic()
                    
                    # Clip the nighttime lights image to the defined region
                    nighttime_clipped = nighttime.clip(ee_object)
                    
                    nighttimeVis = {'min': 0.0, 'max': 60.0,'palette': ['1a3678', '2955bc', '5699ff', '8dbae9', 'acd1ff', 'caebff', 'e5f9ff',
                    'fdffb4', 'ffe6a2', 'ffc969', 'ffa12d', 'ff7c1f', 'ca531a', 'ff0000',
                    'ab0000']}
                    nighttime_layer = folium.TileLayer(
                        tiles=nighttime_clipped.getMapId(nighttimeVis)['tile_fetcher'].url_format,
                        attr='Google Earth Engine',
                        name='Nighttime Lights',
                        overlay=True,
                        control=True
                    ).add_to(m)
                                
                    m.add_child(folium.LayerControl())
                    figure.render()

                else:
                    F = "2015-07-01"
                    T = "2023-09-30"
                    print("Date TO is Missing")
            else:
                F = "2015-07-01"
                T = "2023-09-30"
                print("Date From is Missing")

        else:
            pass
#------------------------------------------------------------------------------------------------------------------------------------#

#------------------------------------------------------------------------------------------------------------------------------------#
    elif selected_dataset == "precipitation":
        if selected_shapefile != None:

            shapefile_path = ('C:\\Users\\piv\\Desktop\\y\\media\\shp')
            


            roi_gdf = gpd.read_file(shapefile_path)
            roi_geojson = roi_gdf.to_crs("EPSG:4326").to_json()
            
            # Create a folium GeoJson layer for visualization
            roi_geojson_layer = folium.GeoJson(roi_geojson, name='ROI GeoJSON')
            roi_geojson_layer.add_to(m)
            
            # Convert the GeoJSON content to Earth Engine object
            ee_object = geemap.geojson_to_ee(json.loads(roi_geojson))
            if selected_date_range_From != None:
                if selected_date_range_To != None:
                    print("I am here")
                    F = selected_date_range_From
                    T = selected_date_range_To
                    print(F,"==>",T)


                  
                    # Load the dataset
                    dataset = (ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY').filterBounds(ee_object).filter(ee.Filter.date(F, T)))

                  
                 
                  
                    # Calculate the sum of the dataset
                    dataset1 = dataset.sum()
             
                    # Clip the summed dataset to the defined region
                    dataset2 = dataset1.clip(ee_object)
             
                    # Select the 'precipitation' band
                    precipitation = dataset2.select('precipitation')
             
                    # Define visualization parameters
                    imageVisParam = {
                        'min': 80,
                        'max': 460,
                        'palette': ["001137","0aab1e","e7eb05","ff4a2d","e90000"]
                    }
             
                    # Clip the precipitation data to the region
                    precipitation_clipped = precipitation.clip(ee_object)
             
                    # Add precipitation layer to the map
                    folium.TileLayer(
                        tiles=precipitation_clipped.getMapId(imageVisParam)['tile_fetcher'].url_format,
                        attr='Google Earth Engine',
                        name='Precipitation',
                        overlay=True,
                        control=True
                    ).add_to(m)
                    
                    m.add_child(folium.LayerControl())
                    figure.render()

            else:
                    F = "2015-07-01"
                    T = "2023-09-30"
                    print("Date TO is Missing")
        else:
                F = "2015-07-01"
                T = "2023-09-30"
                print("Date From is Missing")

    else:
            pass

#------------------------------------------------------------------------------------------------------------------------------------#
                

#------------------------------------------------------------------------------------------------------------------------------------#



#to be rendered 
    dataset_options = ['Modis',  
                    'dataset_nighttime',
                    'precipitation',
                    'GlobalSurfaceWater',
                    'WorldPop',
                    'COPERNICUS']




    shapes_options = ['District_Boundary',
                    'hydro_basins',
                    'karachi',
                    'National_Constituency_with_Projected_2010_Population',
                    'Provincial_Boundary',
                    'Provincial_Constituency',
                    'Tehsil_Boundary',
                    'Union_Council']
    # print(figure)
    # map_html = m._repr_html_()
    m.save('ndvi_map.html')
    
    
    

    context = {"map": figure,"dataset_options":dataset_options,"shapes_options": shapes_options}
    return render(request, template_name , context)
@login_required
def generate_ndvi_map(request):
    # Create a response object for the HTML file
    response = HttpResponse(content_type='text/html')
    # Open and read the HTML file
    with open('ndvi_map.html', 'rb') as html_file:
        response.write(html_file.read())
    
    # Set the Content-Disposition header to suggest a filename for download
    response['Content-Disposition'] = 'attachment; filename="ndvi_map.html"'
    
    return response
@login_required
def generate_chart(request):
    template_name = 'results.html'

    water_threshold=0.2
    if request.method == 'GET':
        selected_dataset = request.GET.get('dataset')
        selected_shapefile = request.GET.get('shapefile')
        selected_date_range_From = request.GET.get('dateRangeFrom')
        selected_date_range_To = request.GET.get('dateRangeTo')

        print(f'Selected Dataset: {selected_dataset}')
        print(f'Selected Dataset: {selected_shapefile}')
        
    figure = folium.Figure()

    m = folium.Map(
        location=[25.5973518, 65.54495724],
        zoom_start=7,
    )
    m.add_to(figure)


#----------------------------------------------------------------------------------------------------------------------#
    if selected_dataset == "Modis":
        if selected_shapefile != None:

            shapefile_path = ('C:\\Users\\piv\\Desktop\\y\\media\\shp')
           

            roi_gdf = gpd.read_file(shapefile_path)
            roi_geojson = roi_gdf.to_crs("EPSG:4326").to_json()
            
            # Create a folium GeoJson layer for visualization
            roi_geojson_layer = folium.GeoJson(roi_geojson, name='ROI GeoJSON')
            roi_geojson_layer.add_to(m)
            
            # Convert the GeoJSON content to Earth Engine object
            ee_object = geemap.geojson_to_ee(json.loads(roi_geojson))
            if selected_date_range_From != None:
                if selected_date_range_To != None:
                    print("I am here")
                    F = selected_date_range_From
                    T = selected_date_range_To
                    print(F,"==>",T)


                    dataset = ee.ImageCollection('MODIS/006/MOD13Q1').filter(ee.Filter.date(F, T)).filterBounds(ee_object).first()
            
                    modisndvi = dataset.select('NDVI')

                    def water_function(image):
                        ndwi = image.normalizedDifference(['B3', 'B5']).rename('NDWI')
                        ndwi1 = ndwi.select('NDWI')
                        water01 = ndwi1.gt(water_threshold)
                        image = image.updateMask(water01).addBands(ndwi1)
                        area = ee.Image.pixelArea()
                        water_area = water01.multiply(area).rename('waterArea')
                        image = image.addBands(water_area)
                        stats = water_area.reduceRegion({
                            'reducer': ee.Reducer.sum(),
                            'geometry': shapefile_path,
                            'scale': 30,
                        })
                        return image.set(stats)
                    
                    

                    modisndvi = modisndvi.clip(ee_object)

                    vis_paramsNDVI = {
                        'min': 0,
                        'max': 9000,
                        'palette': ['FE8374', 'C0E5DE', '3A837C', '034B48']}

                    map_id_dict = ee.Image(modisndvi).getMapId(vis_paramsNDVI)
                    folium.raster_layers.TileLayer(
                        tiles=map_id_dict['tile_fetcher'].url_format,
                        attr='Google Earth Engine',
                        name='NDVI',
                        overlay=True,
                        control=True
                    ).add_to(m)
                    
                    m.add_child(folium.LayerControl())
                    figure.render()

                else:
                    F = "2015-07-01"
                    T = "2019-11-30"
                    print("Date TO is Missing")
            else:
                F = "2015-07-01"
                T = "2019-11-30"
                print("Date From is Missing")

        else:
            pass




#--------------------------------------------------------------------------------------------------------------------------------#   
    elif selected_dataset == "dataset_nighttime":
        if selected_shapefile != None:

            shapefile_path =('C:\\Users\\piv\\Desktop\\y\\media\\shp')
                                # D:\Desktop\final_working1-New-2023\final\media

            roi_gdf = gpd.read_file(shapefile_path)
            roi_geojson = roi_gdf.to_crs("EPSG:4326").to_json()
            
            # Create a folium GeoJson layer for visualization
            roi_geojson_layer = folium.GeoJson(roi_geojson, name='ROI GeoJSON')
            roi_geojson_layer.add_to(m)
            
            # Convert the GeoJSON content to Earth Engine object
            ee_object = geemap.geojson_to_ee(json.loads(roi_geojson))
            if selected_date_range_From != None:
                if selected_date_range_To != None:
                    print("I am here")
                    F = selected_date_range_From
                    T = selected_date_range_To
                    print(F,"==>",T)


                    dataset_nighttime = ee.ImageCollection('NOAA/VIIRS/DNB/MONTHLY_V1/VCMCFG').filter(ee.Filter.date(F, T))
              


                    # Mosaic the image collection to a single image
                    nighttime = dataset_nighttime.select('avg_rad').mosaic()
                    
                    # Clip the nighttime lights image to the defined region
                    nighttime_clipped = nighttime.clip(ee_object)
                    
                    nighttimeVis = {'min': 0.0, 'max': 60.0,'palette': ['1a3678', '2955bc', '5699ff', '8dbae9', 'acd1ff', 'caebff', 'e5f9ff',
                    'fdffb4', 'ffe6a2', 'ffc969', 'ffa12d', 'ff7c1f', 'ca531a', 'ff0000',
                    'ab0000']}
                    nighttime_layer = folium.TileLayer(
                        tiles=nighttime_clipped.getMapId(nighttimeVis)['tile_fetcher'].url_format,
                        attr='Google Earth Engine',
                        name='Nighttime Lights',
                        overlay=True,
                        control=True
                    ).add_to(m)
                                
                    m.add_child(folium.LayerControl())
                    figure.render()

                else:
                    F = "2015-07-01"
                    T = "2023-09-30"
                    print("Date TO is Missing")
            else:
                F = "2015-07-01"
                T = "2023-09-30"
                print("Date From is Missing")

        else:
            pass

    elif selected_dataset == "precipitation":
        if selected_shapefile != None:
            shapefile_path = ('C:\\Users\\piv\\Desktop\\y\\media\\shp')
           
            roi_gdf = gpd.read_file(shapefile_path)
            roi_geojson = roi_gdf.to_crs("EPSG:4326").to_json()

            # Create a folium GeoJson layer for visualization
            roi_geojson_layer = folium.GeoJson(roi_geojson, name='ROI GeoJSON')
            roi_geojson_layer.add_to(m)

            # Convert the GeoJSON content to Earth Engine object
            ee_object = geemap.geojson_to_ee(json.loads(roi_geojson))
            if selected_date_range_From != None:
                if selected_date_range_To != None:
                    print("I am here")
                    F = selected_date_range_From
                    T = selected_date_range_To
                    print(F, "=>", T)

                    # Load the dataset
                    dataset = (ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY').filterBounds(ee_object).filter(ee.Filter.date(F, T)))

                    # Calculate the sum of the dataset
                    dataset1 = dataset.sum()

                    # Clip the summed dataset to the defined region
                    dataset2 = dataset1.clip(ee_object)

                    # Select the 'precipitation' band
                    precipitation = dataset2.select('precipitation')

                    # Define visualization parameters
                    imageVisParam = {
                        'min': 80,
                        'max': 460,
                        'palette': ["001137", "0aab1e", "e7eb05", "ff4a2d", "e90000"]
                    }

                    # Clip the precipitation data to the region
                    precipitation_clipped = precipitation.clip(ee_object)

                    # Add precipitation layer to the map
                    folium.TileLayer(
                        tiles=precipitation_clipped.getMapId(imageVisParam)['tile_fetcher'].url_format,
                        attr='Google Earth Engine',
                        name='Precipitation',
                        overlay=True,
                        control=True
                    ).add_to(m)

                    m.add_child(folium.LayerControl())
                    figure.render()
            else:
                F = "2015-07-01"
                T = "2023-09-30"
                print("Date TO is Missing")
        else:
            F = "2015-07-01"
            T = "2023-09-30"
            print("Date From is Missing")
    


    elif selected_dataset == "WorldPop": 
        shapefile_path = ('C:\\Users\\piv\\Desktop\\y\\media\\shp')

        roi_gdf = gpd.read_file(shapefile_path)
        roi_geojson = roi_gdf.to_crs("EPSG:4326").to_json()

        # Create a folium GeoJson layer for visualization
        m = folium.Map(location=[25.5, 61], zoom_start=6)
        roi_geojson_layer = folium.GeoJson(roi_geojson, name='ROI GeoJSON')
        roi_geojson_layer.add_to(m)

        # Convert the GeoJSON content to Earth Engine object
        ee_object = geemap.geojson_to_ee(json.loads(roi_geojson))

        if selected_date_range_From and selected_date_range_To:
            F = selected_date_range_From
            T = selected_date_range_To

            # Load the image collection
            collection = (ee.ImageCollection("WorldPop/GP/100m/pop")
                        .filterBounds(ee_object)
                        .filter(ee.Filter.date(F, T)))

            # Calculate the sum of population for the specified region and time range
            s2median = collection.sum()

            # Clip the result to the ROI
            roi = s2median.clip(ee_object)

            # Create an image time series chart
            chart = (ee.Image.cat(collection)
                    .reduceRegion(ee.Reducer.sum(), roi, 200)
                    .getInfo())

            # Return the chart as JSON and map HTML as a response
            clipped_image_url = roi.getThumbUrl({
                'min': 0,
                'max': 2000,
                'dimensions': 512,
                'palette': ['000000', 'ffffff']
            })

            # Add the clipped population image as a layer to the map
            folium.TileLayer(
                tiles=clipped_image_url,
                attr="Population year17",
                overlay=True,
                control=True,
            ).add_to(m)

            # Return the folium map as HTML in the JSON response
            map_html = m.get_root().render()
            response_data = {'chart': chart, 'map_html': map_html}
            return JsonResponse(response_data)



#to be rendered 
    dataset_options = ['Modis',  
                    'dataset_nighttime',
                    'precipitation',
                    'GlobalSurfaceWater',
                    'WorldPop',
                    'COPERNICUS']




    shapes_options = ['District_Boundary',
                    'hydro_basins',
                    'karachi',
                    'National_Constituency_with_Projected_2010_Population',
                    'Provincial_Boundary',
                    'Provincial_Constituency',
                    'Tehsil_Boundary',
                    'Union_Council']
    # print(figure)
    # map_html = m._repr_html_()
    m.save('ndvi_map.html')
    
    
    

    context = {"map": figure,"dataset_options":dataset_options,"shapes_options": shapes_options}
    return render(request, template_name , context)
    # You can continue with the existing code or add more logic as needed
@login_required
def map (request):
    template_name='map.html'


    return render(request,template_name)

@login_required
def GEE(request):
    if request.method == 'POST':
        formulario = dataset_geemap(data=request.POST)
        if formulario.is_valid():
            option = formulario.cleaned_data['option']
            
            # Apply custom styles to the form fields or widgets
            formulario.fields['option'].widget.attrs['class'] = 'custom-select'
            
            figure = folium.Figure()
            Map = geemap.Map(
                        plugin_Draw = True, 
                        Draw_export = False,
                        plugin_LayerControl = False,
                        location = [25, 67],
                        zoom_start = 10,
                        plugin_LatLngPopup = False)
            Map.add_basemap('HYBRID')
            type_map(Map, option)
            file, url_d = data_gee()
            Map.add_layer_control()
            url = url_d[url_d['id'] == option].reset_index()
            url = url['asset_url'].iloc[0]
            form = dataset_geemap(data=request.POST)
    else:
        form = dataset_geemap()

        figure = folium.Figure()
        Map = geemap.Map(
                    plugin_Draw = True, 
                    Draw_export = False,
                    plugin_LayerControl = False,
                    location = [25, 67],
                    zoom_start = 10,
                    plugin_LatLngPopup = False)
        Map.add_basemap('HYBRID')
        dataset = ee.ImageCollection('BIOPAMA/GlobalOilPalm/v1')
        opClass = dataset.select('classification')
        mosaic = opClass.mosaic()
        classificationVis = {
            'min': 1,
            'max': 3,
            'palette': ['ff0000','ef00ff', '696969']
            }
        mask = mosaic.neq(3)
        mask = mask.where(mask.eq(0), 0.6)

        Map.addLayer(mosaic.updateMask(mask),
                        classificationVis, 'Oil palm plantation type', True)
        Map.setCenter(25,67,8)

        url = 'https://developers.google.com/earth-engine/datasets/catalog/BIOPAMA_GlobalOilPalm_v1#terms-of-use'
    

    Map.add_to(figure)
    figure = figure._repr_html_() #updated

    return render(request, 'gee.html', {'form':form, 'map':figure, 'url':url})







# Define your ee_array_to_df, t_modis_to_celsius, and fit_func functions here


def result_options(request):

    return render (request, "result_options.html" )

def temp_result(request):

    if request.method == 'GET':
        selected_shapefile = request.GET.get('shapefile')
        selected_date_range_From = request.GET.get('dateRangeFrom')
        selected_date_range_To = request.GET.get('dateRangeTo')

        print(selected_shapefile)
        print(selected_date_range_From)
        print(selected_date_range_To)

        if selected_date_range_From == None or selected_date_range_To == None:
            i_date ='2022-06-24'
            f_date ='2023-09-19'
        else:
            i_date = selected_date_range_From
            f_date = selected_date_range_To

        # Import the MODIS land surface temperature collection.
        lst = ee.ImageCollection('MODIS/006/MOD11A1')

        # Selection of appropriate bands and dates for LST.
        lst = lst.select('LST_Day_1km', 'QC_Day').filterDate(i_date, f_date)

        if selected_shapefile == None:
            u_lon = 4.8148
            u_lat = 45.7758
            u_poi = ee.Geometry.Point(u_lon, u_lat)
        else:
            shapefile_path = ('C:\\Users\\piv\\Desktop\\y\\media\\shp')
            

            roi_gdf = gpd.read_file(shapefile_path)
            roi_geojson = roi_gdf.to_crs("EPSG:4326").to_json()
            
            # Create a folium GeoJson layer for visualization
            ee_object = geemap.geojson_to_ee(json.loads(roi_geojson))

            u_poi = ee_object

        # Get the data for the pixel intersecting the point in the urban area.
        scale = 1000  # scale in meters
        lst_u_poi = lst.getRegion(u_poi, scale).getInfo()

        # Convert the Earth Engine data to a DataFrame using the provided function.
        lst_df_urban = ee_array_to_df(lst_u_poi, ['LST_Day_1km'])

        # Apply the function to convert temperature units to Celsius.
        lst_df_urban['LST_Day_1km'] = lst_df_urban['LST_Day_1km'].apply(t_modis_to_celsius)

        # Fitting curves.
        ## First, extract x values (times) from the df.
        x_data_u = np.asanyarray(lst_df_urban['time'].apply(float))

        ## Then, extract y values (LST) from the df.
        y_data_u = np.asanyarray(lst_df_urban['LST_Day_1km'].apply(float))

        ## Define the fitting function with parameters.
        def fit_func(t, lst0, delta_lst, tau, phi):
            return lst0 + (delta_lst/2)*np.sin(2*np.pi*t/tau + phi)

        ## Optimize the parameters using a good start p0.
        lst0 = 20
        delta_lst = 40
        tau = 365*24*3600*1000   # milliseconds in a year
        phi = 2*np.pi*4*30.5*3600*1000/tau  # offset regarding when we expect LST(t)=LST0

        params_u, params_covariance_u = optimize.curve_fit(
            fit_func, x_data_u, y_data_u, p0=[lst0, delta_lst, tau, phi])


        x_data_u_formatted = [datetime.utcfromtimestamp(ts / 1000).strftime('%d %m %Y') for ts in x_data_u]
        # x_data_r_formatted = [datetime.utcfromtimestamp(ts / 1000).strftime('%d %m %Y') for ts in x_data_r]

        # return render(request, 'chart.html', {'chart_data': chart_data})
        urban_trace = go.Scatter(
            x=x_data_u_formatted,  # Use the formatted dates
            y=fit_func(x_data_u, *params_u),  # Use your fit_func to generate y values
            mode='lines',
            name='Urban Area'
        )

        # Create a Plotly figure for the rural data


        data = [urban_trace]

        layout = go.Layout(
            title='Land Surface Temperature over Time',
            xaxis=dict(title='Time'),
            yaxis=dict(title='LST (°C)'),
            showlegend=True
        )

        fig = go.Figure(data=data, layout=layout)

        # Convert the Plotly figure to HTML
        plot_div = fig.to_html(full_html=False, default_height=500, default_width=700)

        shapes_options = ['District_Boundary',
        'hydro_basins',
        'karachi',
        'National_Constituency_with_Projected_2010_Population',
        'Provincial_Boundary',
        'Provincial_Constituency',
        'Tehsil_Boundary',
        'Union_Council']
        

        context={
            "shapes_options":shapes_options,
            "plot_div":plot_div

        }



        return render(request, "temp_result.html",context )


    else:





        shapes_options = ['District_Boundary',
                'hydro_basins',
                'karachi',
                'National_Constituency_with_Projected_2010_Population',
                'Provincial_Boundary',
                'Provincial_Constituency',
                'Tehsil_Boundary',
                'Union_Council']
        

        context={
            "shapes_options":shapes_options

        }



        return render(request, "temp_result.html",context )


def chart(request):
# Define the date range of interest.


    #replaceble with dates 
    i_date = '2017-01-01'
    f_date = '2020-01-01'

    # Import the MODIS land surface temperature collection.
    lst = ee.ImageCollection('MODIS/006/MOD11A1')

    # Selection of appropriate bands and dates for LST.
    lst = lst.select('LST_Day_1km', 'QC_Day').filterDate(i_date, f_date)

    # Define the urban location of interest as a point near Lyon, France.
    #replaceble with shapefile
    u_lon = 4.8148
    u_lat = 45.7758
    u_poi = ee.Geometry.Point(u_lon, u_lat)

    # Get the data for the pixel intersecting the point in the urban area.
    scale = 1000  # scale in meters
    lst_u_poi = lst.getRegion(u_poi, scale).getInfo()

    # Convert the Earth Engine data to a DataFrame using the provided function.
    lst_df_urban = ee_array_to_df(lst_u_poi, ['LST_Day_1km'])

    # Apply the function to convert temperature units to Celsius.
    lst_df_urban['LST_Day_1km'] = lst_df_urban['LST_Day_1km'].apply(t_modis_to_celsius)

    # Fitting curves.
    ## First, extract x values (times) from the df.
    x_data_u = np.asanyarray(lst_df_urban['time'].apply(float))

    ## Then, extract y values (LST) from the df.
    y_data_u = np.asanyarray(lst_df_urban['LST_Day_1km'].apply(float))

    ## Define the fitting function with parameters.
    def fit_func(t, lst0, delta_lst, tau, phi):
        return lst0 + (delta_lst/2)*np.sin(2*np.pi*t/tau + phi)

    ## Optimize the parameters using a good start p0.
    lst0 = 20
    delta_lst = 40
    tau = 365*24*3600*1000   # milliseconds in a year
    phi = 2*np.pi*4*30.5*3600*1000/tau  # offset regarding when we expect LST(t)=LST0

    params_u, params_covariance_u = optimize.curve_fit(
        fit_func, x_data_u, y_data_u, p0=[lst0, delta_lst, tau, phi])


    x_data_u_formatted = [datetime.utcfromtimestamp(ts / 1000).strftime('%d %m %Y') for ts in x_data_u]
    # x_data_r_formatted = [datetime.utcfromtimestamp(ts / 1000).strftime('%d %m %Y') for ts in x_data_r]

    # return render(request, 'chart.html', {'chart_data': chart_data})
    urban_trace = go.Scatter(
        x=x_data_u_formatted,  # Use the formatted dates
        y=fit_func(x_data_u, *params_u),  # Use your fit_func to generate y values
        mode='lines',
        name='Urban Area'
    )

    # Create a Plotly figure for the rural data


    data = [urban_trace]

    layout = go.Layout(
        title='Land Surface Temperature over Time',
        xaxis=dict(title='Time'),
        yaxis=dict(title='LST (°C)'),
        showlegend=True
    )

    fig = go.Figure(data=data, layout=layout)

    # Convert the Plotly figure to HTML
    plot_div = fig.to_html(full_html=False, default_height=500, default_width=700)

    return render(request, 'chart.html', {'plot_div': plot_div})










#Auth
def signup (request):
    form = SignUpForm()
    if request.method == "POST":
        
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request,user)
            return redirect('index')
           
           

    return render(request, 'signup.html', {'form':form})


class UserUpdateView(UpdateView):
    model=User
    fields =('first_name','last_name', 'email',)
    template_name = 'my_account.html'
    success_url = reverse_lazy('my_account')

    def get_object(self):
        return self.request.user
    


































def ee_array_to_df(arr, list_of_bands):
    """Transforms client-side ee.Image.getRegion array to pandas.DataFrame."""
    df = pd.DataFrame(arr)

    # Rearrange the header.
    headers = df.iloc[0]
    df = pd.DataFrame(df.values[1:], columns=headers)

    # Remove rows without data inside.
    df = df[['longitude', 'latitude', 'time', *list_of_bands]].dropna()

    # Convert the data to numeric values.
    for band in list_of_bands:
        df[band] = pd.to_numeric(df[band], errors='coerce')

    # Convert the time field into a datetime.
    df['datetime'] = pd.to_datetime(df['time'], unit='ms')

    # Keep the columns of interest.
    df = df[['time', 'datetime', *list_of_bands]]
    print(df)

    return df

def t_modis_to_celsius(t_modis):
    """Converts MODIS LST units to degrees Celsius."""
    t_celsius = 0.02 * t_modis - 273.15
    return t_celsius

def fit_func(t, lst0, delta_lst, tau, phi):
    """Fitting function for the curve."""
    return lst0 + (delta_lst / 2) * np.sin(2 * np.pi * t / tau + phi)