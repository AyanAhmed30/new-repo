import ee
import os
import pandas as pd

def data_gee():
    file = (os.path.dirname(os.path.abspath(__file__)) + '/data_gee/gee_catalog.csv')
    data = pd.read_csv(file)
    delete = []
    for i in range(len(data)):
        d = data['title'].iloc[i]
        f = d.find('deprecated')
        if f != -1:
            delete.append(i)
            
    data = data.drop(delete, axis=0).reset_index(drop=True)
    f = data[['id', 'title']]
    return(f, data)

def type_map(Map, cod):
    if cod == 'AAFC/ACI':
        dataset = ee.ImageCollection('AAFC/ACI')
        crop2016 = dataset.filter(ee.Filter.date('2016-01-01', '2016-12-31')).first()
        Map.setCenter(-103.8881, 53.0371, 10)
        Map.addLayer(crop2016)
        
    elif cod == 'ACA/reef_habitat/v2_0':
        dataset = ee.Image('ACA/reef_habitat/v2_0')
        reefExtent = dataset.select('reef_mask').selfMask()
        geomorphicZonation = dataset.select('geomorphic').selfMask()
        benthicHabitat = dataset.select('benthic').selfMask()
        Map.setCenter(-149.56194, -17.00872, 13);
        Map.setOptions('SATELLITE')
        Map.addLayer(reefExtent, {}, 'Global reef extent')
        Map.addLayer(geomorphicZonation, {}, 'Geomorphic zonation')
        Map.addLayer(benthicHabitat, {}, 'Benthic habitat')
        
    elif cod == 'AHN/AHN2_05M_INT':
        dataset = ee.Image('AHN/AHN2_05M_INT')
        elevation = dataset.select('elevation')
        elevationVis = {'min': -5.0,'max': 30.0}
        Map.setCenter(5.76583, 51.855276, 16)
        Map.addLayer(elevation, elevationVis, 'Elevation')
        
    elif cod == 'AHN/AHN2_05M_NON':
        dataset = ee.Image('AHN/AHN2_05M_NON')
        elevation = dataset.select('elevation')
        elevationVis = {
          'min': -5.0,
          'max': 30.0
        }
        Map.setCenter(5.80258, 51.78547, 14)
        Map.addLayer(elevation, elevationVis, 'Elevation')
        
    elif cod == 'AHN/AHN2_05M_RUW':
        dataset = ee.Image('AHN/AHN2_05M_RUW')
        elevation = dataset.select('elevation')
        elevationVis = {
          'min': -5.0,
          'max': 30.0
        }
        Map.setCenter(5.76583, 51.855276, 16)
        Map.addLayer(elevation, elevationVis, 'Elevation')
        
    elif cod == 'ASTER/AST_L1T_003':
        dataset = ee.ImageCollection('ASTER/AST_L1T_003').filter(ee.Filter.date('2018-01-01', '2018-08-15'))
        falseColor = dataset.select(['B3N', 'B02', 'B01'])
        falseColorVis = {
          'min': 0.0,
          'max': 255.0,
        }
        Map.setCenter(-122.0272, 39.6734, 11)
        Map.addLayer(falseColor.median(), falseColorVis, 'False Color')
        
    elif cod == 'AU/GA/AUSTRALIA_5M_DEM':
        dataset = ee.ImageCollection('AU/GA/AUSTRALIA_5M_DEM')
        elevation = dataset.select('elevation')
        elevationVis = {
          'min': 0.0,
          'max': 150.0,
          'palette': ['0000ff', '00ffff', 'ffff00', 'ff0000', 'ffffff']
        }
        Map.setCenter(140.1883, -35.9113, 8)
        Map.addLayer(elevation, elevationVis, 'Elevation')
        
    elif cod == 'AU/GA/DEM_1SEC/v10/DEM-H':
        dataset = ee.Image('AU/GA/DEM_1SEC/v10/DEM-H')
        elevation = dataset.select('elevation')
        elevationVis = {
          'min': -10.0,
          'max': 1300.0,
          'palette': [
            '3ae237', 'b5e22e', 'd6e21f', 'fff705', 'ffd611', 'ffb613', 'ff8b13',
            'ff6e08', 'ff500d', 'ff0000', 'de0101', 'c21301', '0602ff', '235cb1',
            '307ef3', '269db1', '30c8e2', '32d3ef', '3be285', '3ff38f', '86e26f'
          ],
        }
        Map.setCenter(133.95, -24.69, 5)
        Map.addLayer(elevation, elevationVis, 'Elevation')
        
    elif cod == 'AU/GA/DEM_1SEC/v10/DEM-S':
        dataset = ee.Image('AU/GA/DEM_1SEC/v10/DEM-S')
        elevation = dataset.select('elevation')
        elevationVis = {
          'min': -10.0,
          'max': 1300.0,
          'palette': [
            '3ae237', 'b5e22e', 'd6e21f', 'fff705', 'ffd611', 'ffb613', 'ff8b13',
            'ff6e08', 'ff500d', 'ff0000', 'de0101', 'c21301', '0602ff', '235cb1',
            '307ef3', '269db1', '30c8e2', '32d3ef', '3be285', '3ff38f', '86e26f'
          ],
        }
        Map.setCenter(133.95, -24.69, 5)
        Map.addLayer(elevation, elevationVis, 'Elevation')
        
    elif cod == 'BIOPAMA/GlobalOilPalm/v1':
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

        Map.addLayer(mosaic.updateMask(mask), classificationVis, 'Oil palm plantation type', True)
        Map.setCenter(-73.628998,7.320244,8)
        
    elif cod == "BLM/AIM/v1/TerrADat/TerrestrialAIM":
        greens = ee.List(["#00441B", "#00682A", "#37A055", "#5DB96B", "#AEDEA7", "#E7F6E2", "#F7FCF5"])
        reds = ee.List(["#67000D", "#9E0D14", "#E32F27", "#F6553D", "#FCA082", "#FEE2D5", "#FFF5F0"])

        def normalize(value, min, max):
            return value.subtract(min).divide(ee.Number(max).subtract(min))

        def setColor(feature, property, min, max, palette):
            value = normalize(feature.getNumber(property), min, max).multiply(palette.size()).min(palette.size().subtract(1)).max(0)
            return feature.set({"style": {"color": palette.get(value.int())}})

        fc = ee.FeatureCollection("BLM/AIM/v1/TerrADat/TerrestrialAIM")
        woodyHeightStyle = lambda f:setColor(f, "WoodyHgt_Avg", 0, 100, greens)
        bareSoilStyle = lambda f: setColor(f, "BareSoilCover_FH", 0, 100, reds)

        treeHeight = fc.filter("WoodyHgt_Avg > 1").map(woodyHeightStyle)
        bareSoil = fc.filter("BareSoilCover_FH > 1").map(bareSoilStyle)
        Map.addLayer(bareSoil.style({"styleProperty": "style", "pointSize": 3}))
        Map.addLayer(treeHeight.style({"styleProperty": "style", "pointSize": 1}))
        Map.setCenter(-110, 40, 6)

    elif cod == "BNU/FGS/CCNL/v1":
        dataset = ee.ImageCollection("BNU/FGS/CCNL/v1").filter(ee.Filter.date("2010-01-01", "2010-12-31"))
        nighttimeLights = dataset.select("b1")
        nighttimeLightsVis = {
            "min": 3.0,
            "max": 60.0,
        }
        Map.setCenter(31.4, 30, 6)
        Map.addLayer(nighttimeLights, nighttimeLightsVis, "Nighttime Lights")

    elif cod == "CAS/IGSNRR/PML/V2_v017":
        dataset = ee.ImageCollection("CAS/IGSNRR/PML/V2_v017")
        visualization = {
            'bands': ["GPP"],
            "min": 0.0,
            "max": 9.0,
            "palette": ["a50026", "d73027", "f46d43", "fdae61", "fee08b", "ffffbf",
                  "d9ef8b", "a6d96a", "66bd63", "1a9850", "006837"]}
        Map.setCenter(0.0, 15.0, 2)
        Map.addLayer(dataset, visualization, "PML_V2 0.1.7 Gross Primary Product (GPP)")

    elif cod == "CGIAR/SRTM90_V4":
        dataset = ee.Image("CGIAR/SRTM90_V4")
        elevation = dataset.select("elevation")
        slope = ee.Terrain.slope(elevation)
        Map.setCenter(-112.8598, 36.2841, 10)
        Map.addLayer(slope, {"min": 0, "max": 60}, "slope")

    elif cod == "CIESIN/GPWv411/GPW_Basic_Demographic_Characteristics":
        dataset = ee.ImageCollection("CIESIN/GPWv411/GPW_Basic_Demographic_Characteristics").first()
        raster = dataset.select("basic_demographic_characteristics")
        raster_vis = {
            "max": 1000.0,
            "palette": ["ffffe7","86a192","509791","307296","2c4484","000066"],
            "min": 0.0
        }
        Map.setCenter(79.1, 19.81, 3)
        Map.addLayer(raster, raster_vis, "basic_demographic_characteristics")

    elif cod == "CIESIN/GPWv411/GPW_Data_Context":
        dataset = ee.Image("CIESIN/GPWv411/GPW_Data_Context")
        raster = dataset.select("data_context")
        raster_vis = {
            "min": 200.0,
            "palette": ["ffffff","099506","f04923","e62440","706984","a5a5a5","ffe152","d4cc11","000000"],
            "max": 207.0
        }
        Map.setCenter(-88.6, 26.4, 1)
        Map.addLayer(raster, raster_vis, "data_context")

    elif cod == "CIESIN/GPWv411/GPW_Land_Area":
        dataset = ee.Image("CIESIN/GPWv411/GPW_Land_Area")
        raster = dataset.select("land_area")
        raster_vis = {
            "min": 0.0,
            "palette": ["ecefb7","745638"],
            "max": 0.86
        }
        Map.setCenter(26.4, 19.81, 1)
        Map.addLayer(raster, raster_vis, "land_area")

    elif cod == "CIESIN/GPWv411/GPW_Mean_Administrative_Unit_Area":
        dataset = ee.Image("CIESIN/GPWv411/GPW_Mean_Administrative_Unit_Area")
        raster = dataset.select("mean_administrative_unit_area")
        raster_vis = {
            "min": 0.0,
            "palette": ["ffffff","747474","656565","3c3c3c","2f2f2f","000000"],
            "max": 40000.0
        }
        Map.setCenter(-88.6, 26.4, 1)
        Map.addLayer(raster, raster_vis, "mean_administrative_unit_area")

    elif cod == "CIESIN/GPWv411/GPW_National_Identifier_Grid":
        dataset = ee.Image("CIESIN/GPWv411/GPW_National_Identifier_Grid")
        raster = dataset.select("national_identifier_grid")
        raster_vis = {
        "min": 4.0,
        "palette": ["000000","ffffff"],
        "max": 999.0
        }
        Map.setCenter(-88.6, 26.4, 1)
        Map.addLayer(raster, raster_vis, "national_identifier_grid")
        
    elif cod == "CIESIN/GPWv411/GPW_Population_Count":
        dataset = ee.ImageCollection("CIESIN/GPWv411/GPW_Population_Count").first()
        raster = dataset.select("population_count")
        raster_vis = {
        "max": 1000.0, 
        "palette": ["ffffe7","86a192","509791","307296","2c4484","000066"],
        "min": 0.0}
        Map.setCenter(79.1, 19.81, 3)
        Map.addLayer(raster, raster_vis, "population_count")
        
    elif cod == "CIESIN/GPWv411/GPW_Population_Density":
        dataset = ee.ImageCollection("CIESIN/GPWv411/GPW_Population_Density").first()
        raster = dataset.select("population_density")
        raster_vis = {
            "max": 1000.0,
            "palette": ["ffffe7","FFc869","ffac1d","e17735","f2552c","9f0c21"],
            "min": 200.0
        }
        Map.setCenter(79.1, 19.81, 3)
        Map.addLayer(raster, raster_vis, "population_density")

    elif cod == "CIESIN/GPWv411/GPW_UNWPP-Adjusted_Population_Count":
        dataset = ee.ImageCollection("CIESIN/GPWv411/GPW_UNWPP-Adjusted_Population_Count").first()
        raster = dataset.select("unwpp-adjusted_population_count")
        raster_vis = {"max": 1000.0, "palette": ["ffffe7","86a192","509791","307296","2c4484","000066"], "min": 0.0}
        Map.setCenter(79.1, 19.81, 3)
        Map.addLayer(raster, raster_vis, "unwpp-adjusted_population_count")

    elif cod == "CIESIN/GPWv411/GPW_UNWPP-Adjusted_Population_Density":
        dataset = ee.ImageCollection("CIESIN/GPWv411/GPW_UNWPP-Adjusted_Population_Density").first()
        raster = dataset.select("unwpp-adjusted_population_density")
        raster_vis = {"max": 1000.0, "palette": ["ffffe7","FFc869","ffac1d","e17735","f2552c","9f0c21"], "min": 0.0}
        Map.setCenter(79.1, 19.81, 3)
        Map.addLayer(raster, raster_vis, "unwpp-adjusted_population_density")

    elif cod == "CIESIN/GPWv411/GPW_Water_Area":
        dataset = ee.Image("CIESIN/GPWv411/GPW_Water_Area")
        raster = dataset.select("water_area")
        raster_vis = {
            "min": 0.0,
            "palette": ["f5f6da","180d02"],
            "max": 0.860558}
        Map.setCenter(79.1, 19.81, 3)
        Map.addLayer(raster, raster_vis, "water_area")

    elif cod == "CIESIN/GPWv411/GPW_Water_Mask":
        dataset = ee.Image("CIESIN/GPWv411/GPW_Water_Mask")
        raster = dataset.select("water_mask")
        raster_vis = {
        "min": 0.0,
        "palette": ["005ce6","00ffc5","bed2ff","aed0f1"],
        "max": 3.0
        }
        Map.setCenter(-88.6, 26.4, 1)
        Map.addLayer(raster, raster_vis, "water_mask")

    elif cod == "COPERNICUS/CORINE/V20/100m/2012":
        dataset = ee.Image("COPERNICUS/CORINE/V20/100m/2012")
        landCover = dataset.select("landcover")
        Map.setCenter(16.436, 39.825, 6)
        Map.addLayer(landCover, {}, "Land Cover")


    elif cod == "COPERNICUS/DEM/GLO30":
        dataset = ee.ImageCollection("COPERNICUS/DEM/GLO30")
        elevation = dataset.select("DEM")
        elevationVis = {
        "min": 0.0,
        "max": 1000.0,
        'palette': ["0000ff","00ffff","ffff00","ff0000","ffffff"],
        }
        Map.setCenter(-73.388672,5.353521, 4)
        Map.addLayer(elevation, elevationVis, "DEM")

    elif cod == "COPERNICUS/Landcover/100m/Proba-V-C3/Global": 
        dataset = ee.Image("COPERNICUS/Landcover/100m/Proba-V-C3/Global/2019").select("discrete_classification")
        Map.setCenter(-88.6, 26.4, 1)
        Map.addLayer(dataset, {}, "Land Cover")

    elif cod == "COPERNICUS/S1_GRD":
        def ff(image):
            edge = image.lt(-30.0)
            maskedImage = image.mask()
            maskedImage = maskedImage.And(edge.Not())
            return image.updateMask(maskedImage)
        
        imgVV = ee.ImageCollection("COPERNICUS/S1_GRD") \
        .filter(ee.Filter.listContains("transmitterReceiverPolarisation", "VV")) \
        .filter(ee.Filter.eq("instrumentMode", "IW")) \
        .select("VV") \
        .map(lambda x:ff(x))
        
        desc = imgVV.filter(ee.Filter.eq("orbitProperties_pass", "DESCENDING"))
        asc = imgVV.filter(ee.Filter.eq("orbitProperties_pass", "ASCENDING"))
    
        spring = ee.Filter.date("2015-03-01", "2015-04-20")
        lateSpring = ee.Filter.date("2015-04-21", "2015-06-10")
        summer = ee.Filter.date("2015-06-11", "2015-08-31")

        descChange = ee.Image.cat(desc.filter(spring).mean(),desc.filter(lateSpring).mean(),desc.filter(summer).mean())
        ascChange = ee.Image.cat(asc.filter(spring).mean(),asc.filter(lateSpring).mean(),asc.filter(summer).mean())
        Map.setCenter(-73.388672,5.353521, 6)
        Map.addLayer(ascChange, {"min": -25, "max": 5}, "Multi-T Mean ASC", True)
        Map.addLayer(descChange, {"min": -25, "max": 5}, "Multi-T Mean DESC", True)

    elif cod == "COPERNICUS/S2":
        def maskS2clouds(image):
            qa = image.select("QA60")
            cloudBitMask = 1 << 10
            cirrusBitMask = 1 << 11
            mask = qa.bitwiseAnd(cloudBitMask).eq(0).And(qa.bitwiseAnd(cirrusBitMask).eq(0))
            return image.updateMask(mask).divide(10000)
        
        dataset = ee.ImageCollection("COPERNICUS/S2").filterDate("2018-01-01", "2018-01-31").filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20)).map(maskS2clouds)
        rgbVis = {"min": 0.0, "max": 0.3,"bands": ["B4", "B3", "B2"]
                 }
        Map.setCenter(-73.388672,5.353521, 6)
        Map.addLayer(dataset.median(), rgbVis, "RGB")
        
    elif cod == "COPERNICUS/S2_CLOUD_PROBABILITY":
        s2Sr = ee.ImageCollection("COPERNICUS/S2_SR")
        s2Clouds = ee.ImageCollection("COPERNICUS/S2_CLOUD_PROBABILITY")
        START_DATE = ee.Date("2019-01-01")
        END_DATE = ee.Date("2019-03-01")
        MAX_CLOUD_PROBABILITY = 65
        region = ee.Geometry.Rectangle([[-76.5, 2.0], [-74, 4.0]])
        Map.setCenter(-75, 3, 12)
        
        def maskClouds(img):
            clouds = ee.Image(img.get("cloud_mask")).select("probability")
            isNotCloud = clouds.lt(MAX_CLOUD_PROBABILITY)
            return img.updateMask(isNotCloud)

        def maskEdges(s2_img):
            return s2_img.updateMask(s2_img.select("B8A").mask().updateMask(s2_img.select("B9").mask()))
    
        criteria = ee.Filter.And(ee.Filter.bounds(region), ee.Filter.date(START_DATE, END_DATE))
        s2Sr = s2Sr.filter(criteria).map(maskEdges)
        s2Clouds = s2Clouds.filter(criteria)
        
        s2SrWithCloudMask = ee.Join.saveFirst("cloud_mask").apply({
            'primary': s2Sr,
            'secondary': s2Clouds,
            'condition': ee.Filter.equals(leftField= "system:index", rightField= "system:index")
        })
        
        s2CloudMasked = ee.ImageCollection(s2SrWithCloudMask).map(maskClouds).median()
        rgbVis = {"min": 0, "max": 3000, "bands": ["B4", "B3", "B2"]}
        
        Map.addLayer(s2CloudMasked, rgbVis, "S2 SR masked at " + MAX_CLOUD_PROBABILITY + "%", True)

    elif cod == "COPERNICUS/S2_HARMONIZED":
        def maskS2clouds(image):
            qa = image.select("QA60")
            cloudBitMask = 1 << 10
            cirrusBitMask = 1 << 11
            mask = qa.bitwiseAnd(cloudBitMask).eq(0).And(qa.bitwiseAnd(cirrusBitMask).eq(0))
            return image.updateMask(mask).divide(10000)

        dataset = ee.ImageCollection("COPERNICUS/S2_HARMONIZED") \
        .filterDate("2022-01-01", "2022-01-31") \
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20)) \
        .map(maskS2clouds)
        rgbVis = {
            "min": 0.0,
            "max": 0.3,
            "bands": ["B4", "B3", "B2"],
        }

        Map.setCenter(-73.388672,5.353521, 6)
        Map.addLayer(dataset.median(), rgbVis, "RGB")

    elif cod == "COPERNICUS/S2_SR":
        def maskS2clouds(image):
            qa = image.select("QA60")
            cloudBitMask = 1 << 10
            cirrusBitMask = 1 << 11
            mask = qa.bitwiseAnd(cloudBitMask).eq(0).And(qa.bitwiseAnd(cirrusBitMask).eq(0))
            return image.updateMask(mask).divide(10000)
        dataset = ee.ImageCollection("COPERNICUS/S2_SR") \
        .filterDate("2020-01-01", "2020-01-30") \
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE",20)) \
        .map(maskS2clouds)
        visualization = {
            "min": 0.0,
            "max": 0.3,
            'bands': ["B4", "B3", "B2"],
        }
        Map.setCenter(83.277, 17.7009, 12)
        Map.addLayer(dataset.mean(), visualization, "RGB")
    

    elif cod == "COPERNICUS/S2_SR_HARMONIZED":
        def maskS2clouds(image):
            qa = image.select("QA60")
            cloudBitMask = 1 << 10
            cirrusBitMask = 1 << 11
            mask = qa.bitwiseAnd(cloudBitMask).eq(0).And(qa.bitwiseAnd(cirrusBitMask).eq(0))
            return image.updateMask(mask).divide(10000)
        dataset = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
        .filterDate("2020-01-01", "2020-01-30") \
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE",20)) \
        .map(maskS2clouds)
        visualization = {
          "min": 0.0,
          "max": 0.3,
          "bands": ["B4", "B3", "B2"],
        }
        Map.setCenter(83.277, 17.7009, 12)
        Map.addLayer(dataset.mean(), visualization, "RGB")

    elif cod == "COPERNICUS/S3/OLCI":
        dataset = ee.ImageCollection("COPERNICUS/S3/OLCI") \
        .filterDate("2018-04-01", "2018-04-04")
        rgb = dataset.select(["Oa08_radiance", "Oa06_radiance", "Oa04_radiance"]) \
        .median().multiply(ee.Image([0.00876539, 0.0123538, 0.0115198]))
        visParams = {"min": 0, "max": 6, "gamma": 1.5,}
        Map.setCenter(46.043, 1.45, 5)
        Map.addLayer(rgb, visParams, "RGB")

    elif cod == "COPERNICUS/S5P/NRTI/L3_AER_AI":
        collection = ee.ImageCollection("COPERNICUS/S5P/NRTI/L3_AER_AI") \
        .select("absorbing_aerosol_index") \
        .filterDate("2019-06-01", "2019-06-06")
        band_viz = {
          "min": -1,
          "max": 2.0,
          "palette": ["black", "blue", "purple", "cyan", "green", "yellow", "red"]
          }
        Map.addLayer(collection.mean(), band_viz, "S5P Aerosol")
        Map.setCenter(-118.82, 36.1, 5)

    elif cod == "COPERNICUS/S5P/NRTI/L3_AER_LH":
        collection = ee.ImageCollection("COPERNICUS/S5P/NRTI/L3_AER_LH") \
        .select("aerosol_height") \
        .filterDate("2019-06-01", "2019-06-06")
        band_viz = {
          "min": -81.17,
          "max": 67622.56,
          "palette": ["blue", "purple", "cyan", "green", "yellow", "red"]
          }
        Map.addLayer(collection.mean(), band_viz, "S5P Aerosol Height")
        Map.setCenter(44.09, 24.27, 4)

    elif cod == "COPERNICUS/S5P/NRTI/L3_CLOUD":
        collection = ee.ImageCollection("COPERNICUS/S5P/NRTI/L3_CLOUD") \
        .select("cloud_fraction") \
        .filterDate("2019-06-01", "2019-06-02")
        band_viz = {
          "min": 0,
          "max": 0.95,
          "palette": ["black", "blue", "purple", "cyan", "green", "yellow", "red"]
          }
        Map.addLayer(collection.mean(), band_viz, "S5P Cloud")
        Map.setCenter(-58.14, -10.47, 2)

    elif cod == "COPERNICUS/S5P/NRTI/L3_CO":
        collection = ee.ImageCollection("COPERNICUS/S5P/NRTI/L3_CO") \
        .select("CO_column_number_density") \
        .filterDate("2019-06-01", "2019-06-11")
        band_viz = {
          "min": 0,
          "max": 0.05,
          "palette": ["black", "blue", "purple", "cyan", "green", "yellow", "red"]
          }
        Map.addLayer(collection.mean(), band_viz, "S5P CO")
        Map.setCenter(-25.01, -4.28, 4)

    elif cod == "COPERNICUS/S5P/NRTI/L3_HCHO":
        collection = ee.ImageCollection("COPERNICUS/S5P/NRTI/L3_HCHO") \
        .select("tropospheric_HCHO_column_number_density") \
        .filterDate("2019-06-01", "2019-06-06")
        band_viz = {
          "min": 0.0,
          "max": 0.0003,
          "palette": ["black", "blue", "purple", "cyan", "green", "yellow", "red"]
        }
        Map.addLayer(collection.mean(), band_viz, "S5P HCHO")
        Map.setCenter(0.0, 0.0, 2)

    elif cod == "COPERNICUS/S5P/NRTI/L3_NO2":
        collection = ee.ImageCollection("COPERNICUS/S5P/NRTI/L3_NO2") \
        .select("NO2_column_number_density") \
        .filterDate("2019-06-01", "2019-06-06")
        band_viz = {
          "min": 0,
          "max": 0.0002,
          "palette": ["black", "blue", "purple", "cyan", "green", "yellow", "red"]
        }
        Map.addLayer(collection.mean(), band_viz, "S5P N02")
        Map.setCenter(65.27, 24.11, 4)

    elif cod == "COPERNICUS/S5P/NRTI/L3_O3":
        collection = ee.ImageCollection("COPERNICUS/S5P/NRTI/L3_O3") \
        .select("O3_column_number_density") \
        .filterDate("2019-06-01", "2019-06-05")
        band_viz = {
          "min": 0.12,
          "max": 0.15,
          "palette": ["black", "blue", "purple", "cyan", "green", "yellow", "red"]
        }
        Map.addLayer(collection.mean(), band_viz, "S5P O3")
        Map.setCenter(0.0, 0.0, 2)

    elif cod == "COPERNICUS/S5P/NRTI/L3_SO2":
        collection = ee.ImageCollection("COPERNICUS/S5P/NRTI/L3_SO2") \
        .select("SO2_column_number_density") \
        .filterDate("2019-06-01", "2019-06-11")
        band_viz = {
          "min": 0.0,
          "max": 0.0005,
          "palette": ["black", "blue", "purple", "cyan", "green", "yellow", "red"]
        }
        Map.addLayer(collection.mean(), band_viz, "S5P SO2")
        Map.setCenter(0.0, 0.0, 2)

    elif cod == "COPERNICUS/S5P/OFFL/L3_AER_AI":
        collection = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_AER_AI") \
        .select("absorbing_aerosol_index") \
        .filterDate("2019-06-01", "2019-06-06")
        band_viz = {
          "min": -1,
          "max": 2.0,
          "palette": ["black", "blue", "purple", "cyan", "green", "yellow", "red"]
        }
        Map.addLayer(collection.mean(), band_viz, "S5P Aerosol")
        Map.setCenter(-118.82, 36.1, 5)

    elif cod == "COPERNICUS/S5P/OFFL/L3_AER_LH":
        collection = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_AER_LH") \
        .select("aerosol_height") \
        .filterDate("2019-06-01", "2019-06-05")
        visualization = {
          "min": 0,
          "max": 6000,
          "palette": ["blue", "purple", "cyan", "green", "yellow", "red"]
        }
        Map.setCenter(44.09, 24.27, 4)
        Map.addLayer(collection.mean(), visualization, "S5P Aerosol Height")
    
    elif cod == "COPERNICUS/S5P/OFFL/L3_CH4":
        collection = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_CH4") \
        .select("CH4_column_volume_mixing_ratio_dry_air") \
        .filterDate("2019-06-01", "2019-07-16")
        band_viz = {
          "min": 1750,
          "max": 1900,
          "palette": ["black", "blue", "purple", "cyan", "green", "yellow", "red"]
        }
        Map.addLayer(collection.mean(), band_viz, "S5P CH4")
        Map.setCenter(0.0, 0.0, 2)

    elif cod == "COPERNICUS/S5P/OFFL/L3_CLOUD":
        collection = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_CLOUD") \
        .select("cloud_fraction") \
        .filterDate("2019-06-01", "2019-06-02")
        band_viz = {
          "min": 0,
          "max": 0.95,
          "palette": ["black", "blue", "purple", "cyan", "green", "yellow", "red"]
        }
        Map.addLayer(collection.mean(), band_viz, "S5P Cloud")
        Map.setCenter(-58.14, -10.47, 2)

    elif cod == "COPERNICUS/S5P/OFFL/L3_CO":
        collection = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_CO") \
        .select("CO_column_number_density") \
        .filterDate("2019-06-01", "2019-06-11")
        band_viz = {
          "min": 0,
          "max": 0.05,
          "palette": ["black", "blue", "purple", "cyan", "green", "yellow", "red"]
        }
        Map.addLayer(collection.mean(), band_viz, "S5P CO")
        Map.setCenter(-25.01, -4.28, 4)

    elif cod == "COPERNICUS/S5P/OFFL/L3_HCHO":
        collection = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_HCHO") \
        .select("tropospheric_HCHO_column_number_density") \
        .filterDate("2019-06-01", "2019-06-06")
        band_viz = {
          "min": 0.0,
          "max": 0.0003,
          "palette": ["black", "blue", "purple", "cyan", "green", "yellow", "red"]
        }
        Map.addLayer(collection.mean(), band_viz, "S5P HCHO")
        Map.setCenter(0.0, 0.0, 2)

    elif cod == "COPERNICUS/S5P/OFFL/L3_NO2":
        collection = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_NO2") \
        .select("tropospheric_NO2_column_number_density") \
        .filterDate("2019-06-01", "2019-06-06")
        band_viz = {
          "min": 0,
          "max": 0.0002,
          "palette": ["black", "blue", "purple", "cyan", "green", "yellow", "red"]
        }
        Map.addLayer(collection.mean(), band_viz, "S5P N02")
        Map.setCenter(65.27, 24.11, 4)

    elif cod == "COPERNICUS/S5P/OFFL/L3_O3":
        collection = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_O3") \
        .select("O3_column_number_density") \
        .filterDate("2019-06-01", "2019-06-05")
        band_viz = {
          "min": 0.12,
          "max": 0.15,
          "palette": ["black", "blue", "purple", "cyan", "green", "yellow", "red"]
        }
        Map.addLayer(collection.mean(), band_viz, "S5P O3")
        Map.setCenter(0.0, 0.0, 2)

    elif cod == "COPERNICUS/S5P/OFFL/L3_O3_TCL":
        collection = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_O3_TCL") \
        .select("ozone_tropospheric_vertical_column") \
        .filterDate("2019-06-01", "2019-07-01")
        band_viz = {
          "min": 0,
          "max": 0.02,
          "palette": ["black", "blue", "purple", "cyan", "green", "yellow", "red"]
        }
        Map.addLayer(collection.mean(), band_viz, "S5P O3")
        Map.setCenter(0.0, 0.0, 2)

    elif cod == "COPERNICUS/S5P/OFFL/L3_SO2":
        collection = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_SO2") \
        .select("SO2_column_number_density") \
        .filterDate("2019-06-01", "2019-06-11")
        band_viz = {
          "min": 0.0,
          "max": 0.0005,
          "palette": ["black", "blue", "purple", "cyan", "green", "yellow", "red"]
        }
        Map.addLayer(collection.mean(), band_viz, "S5P SO2")
        Map.setCenter(0.0, 0.0, 2)

    elif cod == "CPOM/CryoSat2/ANTARCTICA_DEM":
        dataset = ee.Image("CPOM/CryoSat2/ANTARCTICA_DEM")
        visualization = {
          "bands": ["elevation"],
          "min": 0.0,
          "max": 4000.0,
          "palette": ["001fff", "00ffff", "fbff00", "ff0000"]
        }
        Map.setCenter(17.0, -76.0, 3)
        Map.addLayer(dataset, visualization, "Elevation")

    elif cod == "CSIRO/SLGA":
        dataset = ee.ImageCollection("CSIRO/SLGA") \
        .filter(ee.Filter.eq("attribute_code", "DES"))
        soilDepth = dataset.select("DES_000_200_EV")
        soilDepthVis = {
          "min": 0.1,
          "max": 1.84,
          "palette": ["8d6738", "252525"],
        }
        Map.setCenter(132.495, -21.984, 5)
        Map.addLayer(soilDepth, soilDepthVis, "Soil Depth")

    elif cod == "CSP/ERGo/1_0/Global/ALOS_CHILI":
        dataset = ee.Image("CSP/ERGo/1_0/Global/ALOS_CHILI")
        alosChili = dataset.select("constant")
        alosChiliVis = {
            "min": 0.0,
            "max": 255.0,
        }
        Map.setCenter(-105.8636, 40.3439, 11)
        Map.addLayer(alosChili, alosChiliVis, "ALOS CHILI")
        
    elif cod == "CSP/ERGo/1_0/Global/ALOS_landforms":
        dataset = ee.Image("CSP/ERGo/1_0/Global/ALOS_landforms")
        landforms = dataset.select("constant")
        landformsVis = {
            "min": 11.0,
            "max": 42.0,
            "palette": [
            "141414", "383838", "808080", "EBEB8F", "F7D311", "AA0000", "D89382",
            "DDC9C9", "DCCDCE", "1C6330", "68AA63", "B5C98E", "E1F0E5", "a975ba",
            "6f198c"
            ],
        }
        Map.setCenter(-105.58, 40.5498, 11)
        Map.addLayer(landforms, landformsVis, "Landforms")

    elif cod == "CSP/ERGo/1_0/Global/ALOS_mTPI":
        dataset = ee.Image("CSP/ERGo/1_0/Global/ALOS_mTPI")
        alosMtpi = dataset.select("AVE")
        alosMtpiVis = {
            "min": -200.0,
            "max": 200.0,
            "palette": ["0b1eff", "4be450", "fffca4", "ffa011", "ff0000"],
        }
        Map.setCenter(-105.8636, 40.3439, 11)
        Map.addLayer(alosMtpi, alosMtpiVis, "ALOS mTPI")

    elif cod == "CSP/ERGo/1_0/Global/ALOS_topoDiversity":
        dataset = ee.Image("CSP/ERGo/1_0/Global/ALOS_topoDiversity")
        alosTopographicDiversity = dataset.select("constant")
        alosTopographicDiversityVis = {
            "min": 0.0,
            "max": 1.0,
        }
        Map.setCenter(-111.313, 39.724, 6)
        Map.addLayer(alosTopographicDiversity, alosTopographicDiversityVis, "ALOS Topographic Diversity")
            
    elif cod == "CSP/ERGo/1_0/Global/SRTM_CHILI":
        dataset = ee.Image("CSP/ERGo/1_0/Global/SRTM_CHILI")
        srtmChili = dataset.select("constant")
        srtmChiliVis = {
            "min": 0.0,
            "max": 255.0,
        }
        Map.setCenter(-105.8636, 40.3439, 11)
        Map.addLayer(srtmChili, srtmChiliVis, "SRTM CHILI")
        
    elif cod == "CSP/ERGo/1_0/Global/SRTM_landforms":
        dataset = ee.Image("CSP/ERGo/1_0/Global/SRTM_landforms")
        landforms = dataset.select("constant")
        landformsVis = {
            "min": 11.0,
            "max": 42.0,
            "palette": [
            "141414", "383838", "808080", "EBEB8F", "F7D311", "AA0000", "D89382",
            "DDC9C9", "DCCDCE", "1C6330", "68AA63", "B5C98E", "E1F0E5", "a975ba",
            "6f198c"
            ],
        }
        Map.setCenter(-105.58, 40.5498, 11)
        Map.addLayer(landforms, landformsVis, "Landforms")

    elif cod == "CSP/ERGo/1_0/Global/SRTM_mTPI":
        dataset = ee.Image("CSP/ERGo/1_0/Global/SRTM_mTPI")
        srtmMtpi = dataset.select("elevation")
        srtmMtpiVis = {
            "min": -200.0,
            "max": 200.0,
            "palette": ["0b1eff", "4be450", "fffca4", "ffa011", "ff0000"],
        }
        Map.setCenter(-105.8636, 40.3439, 11)
        Map.addLayer(srtmMtpi, srtmMtpiVis, "SRTM mTPI")

    elif cod == "CSP/ERGo/1_0/Global/SRTM_topoDiversity":
        dataset = ee.Image("CSP/ERGo/1_0/Global/SRTM_topoDiversity")
        srtmTopographicDiversity = dataset.select("constant")
        srtmTopographicDiversityVis = {
            "min": 0.0,
            "max": 1.0,
        }
        Map.setCenter(-111.313, 39.724, 6)
        Map.addLayer(srtmTopographicDiversity, srtmTopographicDiversityVis,"SRTM Topographic Diversity")

    elif cod == "CSP/ERGo/1_0/US/CHILI":
        dataset = ee.Image("CSP/ERGo/1_0/US/CHILI")
        usChili = dataset.select("constant")
        usChiliVis = {
            "min": 0.0,
            "max": 255.0,
        }
        Map.setCenter(-105.8636, 40.3439, 11)
        Map.addLayer(usChili, usChiliVis, "US CHILI")

    elif cod == "CSP/ERGo/1_0/US/landforms":
        dataset = ee.Image("CSP/ERGo/1_0/US/landforms")
        landforms = dataset.select("constant")
        landformsVis = {
            "min": 11.0,
            "max": 42.0,
            "palette": [
            "141414", "383838", "808080", "EBEB8F", "F7D311", "AA0000", "D89382",
            "DDC9C9", "DCCDCE", "1C6330", "68AA63", "B5C98E", "E1F0E5", "a975ba",
            "6f198c"
            ],
        }
        Map.setCenter(-105.58, 40.5498, 11)
        Map.addLayer(landforms, landformsVis, "Landforms")

    elif cod == "CSP/ERGo/1_0/US/lithology":
        dataset = ee.Image("CSP/ERGo/1_0/US/lithology")
        lithology = dataset.select("b1")
        lithologyVis = {
            "min": 0.0,
            "max": 20.0,
            "palette": [
            "356EFF", "ACB6DA", "D6B879", "313131", "EDA800", "616161", "D6D6D6",
            "D0DDAE", "B8D279", "D5D378", "141414", "6DB155", "9B6D55", "FEEEC9",
            "D6B879", "00B7EC", "FFDA90", "F8B28C"
            ],
        }
        Map.setCenter(-105.8636, 40.3439, 11)
        Map.addLayer(lithology, lithologyVis, "Lithology")

    elif cod == "CSP/ERGo/1_0/US/mTPI":
        dataset = ee.Image("CSP/ERGo/1_0/US/mTPI") 
        usMtpi = dataset.select("elevation")
        usMtpiVis = {
            "min": -200.0,
            "max": 200.0,
            "palette": ["0b1eff", "4be450", "fffca4", "ffa011", "ff0000"],
        }
        Map.setCenter(-105.8636, 40.3439, 11)
        Map.addLayer(usMtpi, usMtpiVis, "US mTPI")

    elif cod == "CSP/ERGo/1_0/US/physioDiversity":
        dataset = ee.Image("CSP/ERGo/1_0/US/physioDiversity")
        physiographicDiversity = dataset.select("b1")
        physiographicDiversityVis = {
            "min": 0.0,
            "max": 1.0,
        }
        Map.setCenter(-94.625, 39.825, 7)
        Map.addLayer(physiographicDiversity, physiographicDiversityVis,"Physiographic Diversity")

    elif cod == "CSP/ERGo/1_0/US/physiography":
        dataset = ee.Image("CSP/ERGo/1_0/US/physiography")
        physiography = dataset.select("constant")
        physiographyVis = {
            "min": 1100.0,
            "max": 4220.0,
        }
        Map.setCenter(-105.4248, 40.5242, 8)
        Map.addLayer(physiography, physiographyVis, "Physiography")
        
    elif cod == "CSP/ERGo/1_0/US/topoDiversity":
        dataset = ee.Image("CSP/ERGo/1_0/US/topoDiversity")
        usTopographicDiversity = dataset.select("constant")
        usTopographicDiversityVis = {
            "min": 0.0,
            "max": 1.0,
        }
        Map.setCenter(-111.313, 39.724, 6)
        Map.addLayer(usTopographicDiversity, usTopographicDiversityVis, "US Topographic Diversity")

    elif cod == "CSP/HM/GlobalHumanModification":
        dataset = ee.ImageCollection("CSP/HM/GlobalHumanModification")
        visualization = {"bands": ["gHM"],
                        "min": 0.0,
                        "max": 1.0,
                        "palette": ["0c0c0c", "071aff", "ff0000", "ffbd03", "fbff05", "fffdfd"]
        }
        Map.centerObject(dataset)
        Map.addLayer(dataset, visualization, "Human modification")

    elif cod == "DLR/WSF/WSF2015/v1":
        dataset = ee.Image("DLR/WSF/WSF2015/v1")
        opacity = 0.75
        blackBackground = ee.Image(0)
        Map.addLayer(blackBackground, None, "Black background", True, opacity)
        visualization = {
          "min": 0,
          "max": 255,
        }
        Map.addLayer(dataset, visualization, "Human settlement areas")
        Map.setCenter(90.45, 23.7, 7)

    elif cod == "DOE/ORNL/LandScan_HD/Ukraine_202201":
        dataset = ee.Image("DOE/ORNL/LandScan_HD/Ukraine_202201")
        vis = {
          "min": 0.0,
          "max": 10.0,
          "palette":["lemonchiffon", "khaki", "orange","orangered", "red", "maroon"],
        }
        Map.centerObject(dataset)
        Map.addLayer(dataset, vis, "Population Count")

    elif cod == "ECMWF/CAMS/NRT":
        dataset = ee.ImageCollection("ECMWF/CAMS/NRT").filter(ee.Filter.date("2019-01-01", "2019-01-31"))
        aod = dataset.select("total_aerosol_optical_depth_at_550nm_surface")
        visParams = {
          "min": 0.000096,
          "max": 3.582552,
          "palette": [
          "5E4FA2", "3288BD", "66C2A5", "ABE0A4",
          "E6F598", "FFFFBF", "FEE08B", "FDAE61",
          "F46D43", "D53E4F", "9E0142"
          ]
        }
        Map.setCenter(-94.18, 16.8, 1)
        Map.addLayer(aod, visParams, "Total Aerosal Optical Depth")
    
    elif cod == "ECMWF/ERA5/DAILY":
        era5_2mt = ee.ImageCollection("ECMWF/ERA5/DAILY").select("mean_2m_air_temperature").filter(ee.Filter.date("2019-07-01", "2019-07-31"))
        
        era5_tp = ee.ImageCollection("ECMWF/ERA5/DAILY").select("total_precipitation").filter(ee.Filter.date("2019-07-01", "2019-07-31"))
        era5_2d = ee.ImageCollection("ECMWF/ERA5/DAILY").select("dewpoint_2m_temperature").filter(ee.Filter.date("2019-07-01", "2019-07-31"))
        era5_mslp = ee.ImageCollection("ECMWF/ERA5/DAILY").select("mean_sea_level_pressure").filter(ee.Filter.date("2019-07-01", "2019-07-31")) 
        era5_sp = ee.ImageCollection("ECMWF/ERA5/DAILY").select("surface_pressure").filter(ee.Filter.date("2019-07-01", "2019-07-31"))
        era5_u_wind_10m = ee.ImageCollection("ECMWF/ERA5/DAILY").select("u_component_of_wind_10m").filter(ee.Filter.date("2019-07-01", "2019-07-31"))
        era5_sp = era5_sp.map(lambda image: image.divide(100).set("system:time_start", image.get("system:time_start")))
        visTp = {"min": 0, "max": 0.1, "palette": ["#FFFFFF", "#00FFFF", "#0080FF", "#DA00FF", "#FFA400", "#FF0000"]}
        vis2mt = {"min": 250, 
                  "max": 320, 
                  "palette": [
                          "#000080", "#0000D9", "#4000FF", "#8000FF", "#0080FF", "#00FFFF", "#00FF80",
                          "#80FF00", "#DAFF00", "#FFFF00", "#FFF500", "#FFDA00", "#FFB000", "#FFA400",
                          "#FF4F00", "#FF2500", "#FF0A00", "#FF00FF"]
        }
        visWind = {"min": 0, 
                   "max": 30, 
                   "palette": [
                           "#FFFFFF", "#FFFF71", "#DEFF00", "#9EFF00", "#77B038", "#007E55", "#005F51",
                           "#004B51", "#013A7B", "#023AAD"]
        }
        visPressure = {"min": 500, 
                       "max": 1150,
                       "palette": ["#01FFFF", "#058BFF", "#0600FF", "#DF00FF", "#FF00FF", "#FF8C00", "#FF8C00"]
        }
        Map.addLayer(era5_tp.filter(ee.Filter.date("2019-07-15")), visTp, "Daily total precipitation sums")
        Map.addLayer(era5_2d.filter(ee.Filter.date("2019-07-15")), vis2mt, "Daily mean 2m dewpoint temperature")
        Map.addLayer(era5_2mt.filter(ee.Filter.date("2019-07-15")), vis2mt, "Daily mean 2m air temperature")
        Map.addLayer(era5_u_wind_10m.filter(ee.Filter.date("2019-07-15")), visWind, "Daily mean 10m u-component of wind")
        Map.addLayer(era5_sp.filter(ee.Filter.date("2019-07-15")), visPressure, "Daily mean surface pressure")
        Map.setCenter(21.2, 22.2, 2)
                                
    elif cod == "ECMWF/ERA5/MONTHLY":
        dataset = ee.ImageCollection("ECMWF/ERA5/MONTHLY")
        visualization = {
             "bands": ["mean_2m_air_temperature"],
             "min": 250.0,
             "max": 320.0,
             "palette": ["#000080","#0000D9","#4000FF","#8000FF","#0080FF","#00FFFF","#00FF80","#80FF00","#DAFF00","#FFFF00","#FFF500","#FFDA00","#FFB000","#FFA400","#FF4F00","#FF2500","#FF0A00","#FF00FF"]
             }
        Map.setCenter(22.2, 21.2, 0)
        Map.addLayer(dataset, visualization, "Monthly average air temperature [K] at 2m height")

    elif cod == "ECMWF/ERA5_LAND/DAILY_RAW":
        dataset = ee.ImageCollection("ECMWF/ERA5_LAND/DAILY_RAW").filter(ee.Filter.date("2021-06-01", "2021-07-01"))
        visualization = {
             "bands": ["temperature_2m"],
             "min": 250.0,
             "max": 320.0,
             "palette": ["#000080","#0000D9","#4000FF","#8000FF","#0080FF","#00FFFF","#00FF80","#80FF00","#DAFF00","#FFFF00","#FFF500","#FFDA00","#FFB000","#FFA400","#FF4F00","#FF2500","#FF0A00","#FF00FF"]
             }
        Map.setCenter(-170.13, 45.62, 2)
        Map.addLayer(dataset, visualization, "Air temperature [K] at 2m height")

    elif cod == "ECMWF/ERA5_LAND/HOURLY":
        dataset = ee.ImageCollection("ECMWF/ERA5_LAND/HOURLY").filter(ee.Filter.date("2020-07-01", "2020-07-02"))
        visualization = {
             "bands": ["temperature_2m"],
             "min": 250.0,
             "max": 320.0,
             "palette": ["#000080","#0000D9","#4000FF","#8000FF","#0080FF","#00FFFF","#00FF80","#80FF00","#DAFF00","#FFFF00","#FFF500","#FFDA00","#FFB000","#FFA400","#FF4F00","#FF2500","#FF0A00","#FF00FF"]
             }
        Map.setCenter(22.2, 21.2, 0)
        Map.addLayer(dataset, visualization, "Air temperature [K] at 2m height")
                     
    elif cod == "ECMWF/ERA5_LAND/MONTHLY_AGGR":
        dataset = ee.ImageCollection("ECMWF/ERA5_LAND/MONTHLY_AGGR").filter(ee.Filter.date("2020-02-01", "2020-07-10"))
        visualization = {
             "bands": ["temperature_2m"],
             "min": 250.0,
             "max": 320.0,
             "palette": ["#000080","#0000D9","#4000FF","#8000FF","#0080FF","#00FFFF","#00FF80","#80FF00","#DAFF00","#FFFF00","#FFF500","#FFDA00","#FFB000","#FFA400","#FF4F00","#FF2500","#FF0A00","#FF00FF"]
             }
        Map.setCenter(-170.13, 45.62, 2)
        Map.addLayer(dataset, visualization, "Air temperature [K] at 2m height")
                     
    elif cod == "ECMWF/ERA5_LAND/MONTHLY_BY_HOUR": 
        dataset = ee.ImageCollection("ECMWF/ERA5_LAND/MONTHLY_BY_HOUR").filter(ee.Filter.date("2020-07-01", "2020-08-01"))
        visualization = {
             "bands": ["temperature_2m"],
             "min": 250.0,
             "max": 320.0,
             "palette": ["#000080","#0000D9","#4000FF","#8000FF","#0080FF","#00FFFF","#00FF80","#80FF00","#DAFF00","#FFFF00","#FFF500","#FFDA00","#FFB000","#FFA400","#FF4F00","#FF2500","#FF0A00","#FF00FF"]
             }
        Map.setCenter(22.2, 21.2, 0)
        Map.addLayer(dataset, visualization, "Air temperature [K] at 2m height")

    elif cod == "EO1/HYPERION":
        dataset = ee.ImageCollection("EO1/HYPERION").filter(ee.Filter.date("2016-01-01", "2017-03-01"))
        rgb = dataset.select(["B050", "B023", "B015"])
        rgbVis = {
             "min": 1000.0,
             "max": 14000.0,
             "gamma": 2.5,
             }
        Map.setCenter(162.0044, -77.3463, 9)
        Map.addLayer(rgb.median(), rgbVis, "RGB")

    elif cod == "EPA/Ecoregions/2013/L3":
        dataset = ee.FeatureCollection("EPA/Ecoregions/2013/L3")
        visParams = {
             "palette": ["0a3b04", "1a9924", "15d812"],
             "min": 23.0,
             "max": 3.57e+11,
             "opacity": 0.8,
             }
        image = ee.Image().float().paint(dataset, "shape_area")
        Map.setCenter(-99.814, 40.166, 5)
        Map.addLayer(image, visParams, "EPA/Ecoregions/2013/L3")
        Map.addLayer(dataset, None, "for Inspector", False)

    elif cod == "EPA/Ecoregions/2013/L4":
        dataset = ee.FeatureCollection("EPA/Ecoregions/2013/L4")
        visParams = {
             "palette": ["0a3b04", "1a9924", "15d812"],
             "min": 0.0,
             "max": 67800000000.0,
             "opacity": 0.8,
             }
        image = ee.Image().float().paint(dataset, "shape_area")
        Map.setCenter(-99.814, 40.166, 5)
        Map.addLayer(image, visParams, "EPA/Ecoregions/2013/L4")
        Map.addLayer(dataset, None, "for Inspector", False)

    elif cod == "ESA/CCI/FireCCI/5_1":
        dataset = ee.ImageCollection("ESA/CCI/FireCCI/5_1").filterDate("2020-01-01", "2020-12-31")
        burnedArea = dataset.select("BurnDate")
        baVis = {
             "min": 1,
             "max": 366,
             "palette": ["ff0000", "fd4100", "fb8200", "f9c400", "f2ff00", "b6ff05","7aff0a", "3eff0f", "02ff15", "00ff55", "00ff99", "00ffdd","00ddff", "0098ff", "0052ff", "0210ff", "3a0dfb", "7209f6","a905f1", "e102ed", "ff00cc", "ff0089", "ff0047", "ff0004"]
             }
        maxBA = burnedArea.max()
        Map.setCenter(0, 18, 2.1)
        Map.addLayer(maxBA, baVis, "Burned Area")

    elif cod == "ESA/GLOBCOVER_L4_200901_200912_V2_3":
        dataset = ee.Image("ESA/GLOBCOVER_L4_200901_200912_V2_3")
        landcover = dataset.select("landcover")
        Map.setCenter(-88.6, 26.4, 3)
        Map.addLayer(landcover, {}, "Landcover")

    elif cod == "ESA/WorldCover/v100":
        dataset = ee.ImageCollection("ESA/WorldCover/v100").first()
        visualization = {
             "bands": ["Map"],
             }
        Map.centerObject(dataset)
        Map.addLayer(dataset, visualization, "Landcover")
                     
    elif cod == "ESA/WorldCover/v200":
        dataset = ee.ImageCollection("ESA/WorldCover/v200").first()
        visualization = {
             "bands": ["Map"],
             }
        Map.centerObject(dataset)
        Map.addLayer(dataset, visualization, "Landcover")
                     
    elif cod == "FAO/GAUL/2015/level0":
        dataset = ee.FeatureCollection("FAO/GAUL/2015/level0")
        Map.setCenter(7.82, 49.1, 4)
        styleParams = {
             "fillColor": "#b5ffb4",
             "color": "#00909F",
             "width": 1.0,
             }
        dataset = dataset.style(styleParams)
        Map.addLayer(dataset, {}, "Country Boundaries")

    elif cod == "FAO/GAUL/2015/level1":
        dataset = ee.FeatureCollection("FAO/GAUL/2015/level1")
        Map.setCenter(7.82, 49.1, 4)
        styleParams = {
             "fillColor": "b5ffb4",
             "color": "#00909F",
             "width": 1.0,
             }
        dataset = dataset.style(styleParams)
        Map.addLayer(dataset, {}, "First Level Administrative Units")
                     
    elif cod == "FAO/GAUL/2015/level2":
        dataset = ee.FeatureCollection("FAO/GAUL/2015/level2")
        Map.setCenter(12.876, 42.682, 5)
        styleParams = {
             "fillColor": "#b5ffb4",
             "color": "#00909F",
             "width": 1.0,
             }
        dataset = dataset.style(styleParams)
        Map.addLayer(dataset, {}, "Second Level Administrative Units")

    elif cod == "FAO/GAUL_SIMPLIFIED_500m/2015/level0": 
        dataset = ee.FeatureCollection("FAO/GAUL_SIMPLIFIED_500m/2015/level0")
        Map.setCenter(7.82, 49.1, 4)
        styleParams = {
             "fillColor": "#b5ffb4",
             "color": "#00909F",
             "width": 1.0,
             }
        dataset = dataset.style(styleParams)
        Map.addLayer(dataset, {}, "Country Boundaries")
                     
    elif cod == "FAO/GAUL_SIMPLIFIED_500m/2015/level1":
        dataset = ee.FeatureCollection("FAO/GAUL_SIMPLIFIED_500m/2015/level1")
        Map.setCenter(7.82, 49.1, 4)
        styleParams = {
             "fillColor": "#b5ffb4",
             "color": "#00909F",
             "width": 1.0,
             }
        dataset = dataset.style(styleParams)
        Map.addLayer(dataset, {}, "First Level Administrative Units")

    elif cod == "FAO/GAUL_SIMPLIFIED_500m/2015/level2":
        dataset = ee.FeatureCollection("FAO/GAUL_SIMPLIFIED_500m/2015/level2")
        Map.setCenter(12.876, 42.682, 5)
        styleParams = {
             "fillColor": "b5ffb4",
             "color": "00909F",
             "width": 1.0,
             }
        dataset = dataset.style(styleParams)
        Map.addLayer(dataset, {}, "Second Level Administrative Units")
        
    elif cod == "FAO/GHG/1/DROSA_A":
        dataset = ee.ImageCollection("FAO/GHG/1/DROSA_A")
        visualization = {
        "bands": ["cropland"],
        "min": 1.0,
        "max": 60.0,
        "palette": ["white", "red"]
        }
        Map.setCenter(108.0, -0.4, 6)
        Map.addLayer(dataset, visualization, "Cropland area drained (Annual)")

    elif cod == "FAO/GHG/1/DROSE_A":
        dataset = ee.ImageCollection("FAO/GHG/1/DROSE_A")
        visualization = {
        "bands": ["croplandc"],
        "min": 0.1,
        "max": 0.1,
        "palette": ["yellow", "red"]
        }
        Map.setCenter(108.0, -0.4, 6)
        Map.addLayer(dataset, visualization, "Cropland C emissions (Annual)")

    elif cod == "FAO/SOFO/1/FPP":
        coll = ee.ImageCollection("FAO/SOFO/1/FPP")
        image = coll.first().select("FPP_1km")
        Map.setCenter(17.5, 20, 3)
        Map.addLayer(image, {"min": 0, "max": 12, "palette": ["blue", "yellow", "red"]},"Forest proximate people – 1km cutoff distance")

    elif cod == "FAO/SOFO/1/TPP":
        coll = ee.ImageCollection("FAO/SOFO/1/TPP")
        image = coll.first().select("TPP_1km")
        Map.setCenter(17.5, 20, 3)
        Map.addLayer(
        image, {"min": 0, "max": 12, "palette": ["blue", "yellow", "red"]}, "Tree proximate people – 1km cutoff distance")

    elif cod == "FAO/WAPOR/2/L1_AETI_D":
        coll = ee.ImageCollection("FAO/WAPOR/2/L1_AETI_D")
        image = coll.first()
        Map.setCenter(17.5, 20, 3)
        Map.addLayer(image, {"min": 0, "max": 50})

    elif cod == "FAO/WAPOR/2/L1_E_D":
        coll = ee.ImageCollection("FAO/WAPOR/2/L1_E_D")
        image = coll.first()
        Map.setCenter(17.5, 20, 3)
        Map.addLayer(image, {"min": 0, "max": 10})

    elif cod == "FAO/WAPOR/2/L1_I_D":
        coll = ee.ImageCollection("FAO/WAPOR/2/L1_I_D")
        image = coll.first()
        Map.setCenter(17.5, 20, 3)
        Map.addLayer(image, {"min": 0, "max": 50})
        
    elif cod == "FAO/WAPOR/2/L1_NPP_D":
        coll = ee.ImageCollection("FAO/WAPOR/2/L1_NPP_D")
        image = coll.first()
        Map.setCenter(17.5, 20, 3)
        Map.addLayer(image, {"min": 0, "max": 5000})

    elif cod == "FAO/WAPOR/2/L1_RET_D":
        coll = ee.ImageCollection("FAO/WAPOR/2/L1_RET_D")
        image = coll.first()
        Map.setCenter(17.5, 20, 3)
        Map.addLayer(image, {"min": 0, "max": 100})

    elif cod == "FAO/WAPOR/2/L1_RET_E":
        coll = ee.ImageCollection("FAO/WAPOR/2/L1_RET_E")
        image = coll.first()
        Map.setCenter(17.5, 20, 3)
        Map.addLayer(image, {"min": 0, "max": 100})

    elif cod == "FAO/WAPOR/2/L1_T_D":
        coll = ee.ImageCollection("FAO/WAPOR/2/L1_T_D")
        image = coll.first()
        Map.setCenter(17.5, 20, 3)
        Map.addLayer(image, {"min": 0, "max": 50})

    elif cod == "FIRMS":
        dataset = ee.ImageCollection("FIRMS").filter(
        ee.Filter.date("2018-08-01", "2018-08-10"))
        fires = dataset.select("T21")
        firesVis = {
        "min": 325.0,
        "max": 400.0,
        "palette": ["red", "orange", "yellow"],
        }
        Map.setCenter(-119.086, 47.295, 6)
        Map.addLayer(fires, firesVis, "Fires")

    elif cod == "Finland/MAVI/VV/50cm":
        dataset = ee.ImageCollection("Finland/MAVI/VV/50cm")
        Map.setCenter(25.7416, 62.2446, 16)
        Map.addLayer(dataset, None, "Finland 50 cm(False color)")

    elif cod == "GFW/GFF/V1/fishing_hours":
        dataset = ee.ImageCollection("GFW/GFF/V1/fishing_hours").filter(ee.Filter.date("2016-12-01", "2017-01-01"))
        trawlers = dataset.select("trawlers")
        trawlersVis = {
        "min": 0.0,
        "max": 5.0,
        }
        Map.setCenter(16.201, 36.316, 7)
        Map.addLayer(trawlers.max(), trawlersVis, "Trawlers")

    elif cod == "GFW/GFF/V1/vessel_hours":
        dataset = ee.ImageCollection("GFW/GFF/V1/vessel_hours").filter(ee.Filter.date("2016-12-01", "2017-01-01"))
        trawlers = dataset.select("trawlers")
        trawlersVis = {
        "min": 0.0,
        "max": 5.0,
        }
        Map.setCenter(130.61, 34.287, 8)
        Map.addLayer(trawlers.max(), trawlersVis, "Trawlers")

    elif cod == "GLCF/GLS_WATER":
        dataset = ee.ImageCollection("GLCF/GLS_WATER")
        water = dataset.select("water")
        waterVis = {
        "min": 1.0,
        "max": 4.0,
        "palette": ["FAFAFA", "00C5FF", "DF73FF", "828282", "CCCCCC"],
        }
        Map.setCenter(-79.3094, 44.5693, 8)
        Map.addLayer(water, waterVis, "Water")

    elif cod == "GLIMS/20210914":
        dataset = ee.FeatureCollection("GLIMS/20210914")
        visParams = {
        "palette": ["gray", "cyan", "blue"],
        "min": 0.0,
        "max": 10.0,
        "opacity": 0.8,
        }
        image = ee.Image().float().paint(dataset, "area")
        Map.setCenter(-35.618, 66.743, 7)
        Map.addLayer(image, visParams, "GLIMS/20210914")
        Map.addLayer(dataset, None, "for Inspector", False)

    elif cod == "Finland/SMK/VV/50cm":
        dataset = ee.ImageCollection("Finland/SMK/VV/50cm")
        Map.setCenter(25.7416, 62.2446, 16)
        Map.addLayer(dataset, None, "Finland 50 cm(False color)")

    elif cod == "Finland/SMK/V/50cm":
        dataset = ee.ImageCollection("Finland/SMK/V/50cm")
        Map.setCenter(24.9, 60.2, 17)
        Map.addLayer(dataset, None, "Finland 50 cm(color)")

    elif cod == "GLIMS/current":
        dataset = ee.FeatureCollection("GLIMS/current")
        visParams = {
        "palette": ["gray", "cyan", "blue"],
        "min": 0.0,
        "max": 10.0,
        "opacity": 0.8,
        }
        image = ee.Image().float().paint(dataset, "area")
        Map.setCenter(-35.618, 66.743, 7)
        Map.addLayer(image, visParams, "GLIMS/current")
        Map.addLayer(dataset, None, "for Inspector", False)

    elif cod == "GLOBAL_FLOOD_DB/MODIS_EVENTS/V1":
        gfd = ee.ImageCollection("GLOBAL_FLOOD_DB/MODIS_EVENTS/V1")
        hurricaneIsaacDartmouthId = 3977
        hurricaneIsaacUsa = ee.Image(gfd.filterMetadata("id", "equals", hurricaneIsaacDartmouthId).first())
        Map.setOptions("SATELLITE")
        Map.setCenter(-90.2922, 29.4064, 9)
        Map.addLayer(
        hurricaneIsaacUsa.select("flooded").selfMask(),{"min": 0, "max": 1, "palette": "001133"},"Hurricane Isaac - Inundation Extent")
        durationPalette = ["C3EFFE", "1341E8", "051CB0", "001133"]
        Map.addLayer(hurricaneIsaacUsa.select("duration").selfMask(),{"min": 0, "max": 4, "palette": durationPalette},"Hurricane Isaac - Duration")
        gfdFloodedSum = gfd.select("flooded").sum()
        Map.addLayer(gfdFloodedSum.selfMask(),{"min": 0, "max": 10, "palette": durationPalette},"GFD Satellite Observed Flood Plain")
        jrc = gfd.select("jrc_perm_water").sum().gte(1)
        Map.addLayer(jrc.selfMask(),{"min": 0, "max": 1, "palette": "C3EFFE"},"JRC Permanent Water")

    elif cod == "GOOGLE/DYNAMICWORLD/V1":
        COL_FILTER = ee.Filter.And(ee.Filter.bounds(ee.Geometry.Point(20.6729, 52.4305)),ee.Filter.date("2021-04-02", "2021-04-03"))
        dwCol = ee.ImageCollection("GOOGLE/DYNAMICWORLD/V1").filter(COL_FILTER)
        s2Col = ee.ImageCollection("COPERNICUS/S2").filter(COL_FILTER)
        DwS2Col = ee.Join.saveFirst("s2_img").apply(dwCol, s2Col,
        ee.Filter.equals({"leftField": "system:index", "rightField": "system:index"}))
        dwImage = ee.Image(DwS2Col.first())
        s2Image = ee.Image(dwImage.get("s2_img"))
        CLASS_NAMES = ["water", "trees", "grass", "flooded_vegetation", "crops","shrub_and_scrub", "built", "bare", "snow_and_ice"]
        VIS_PALETTE = ["419BDF", "397D49", "88B053", "7A87C6","E49635", "DFC35A", "C4281B", "A59B8F","B39FE1"]
        dwRgb = dwImage.select("label").visualize({"min": 0, "max": 8, "palette": VIS_PALETTE}).divide(255)
        top1Prob = dwImage.select(CLASS_NAMES).reduce(ee.Reducer.max())
        top1ProbHillshade = ee.Terrain.hillshade(top1Prob.multiply(100)).divide(255)
        dwRgbHillshade = dwRgb.multiply(top1ProbHillshade)
        Map.setCenter(20.6729, 52.4305, 12)
        Map.addLayer(s2Image,{"min": 0, "max": 3000, "bands": ["B4", "B3", "B2"]},"Sentinel-2 L1C")
        Map.addLayer(dwRgbHillshade,{"min": 0, "max": 0.65},"Dynamic World")

    elif cod == "GOOGLE/Research/open-buildings/v2/polygons":
        t = ee.FeatureCollection("GOOGLE/Research/open-buildings/v2/polygons")
        t_060_065 = t.filter("confidence >= 0.60 && confidence < 0.65")
        t_065_070 = t.filter("confidence >= 0.65 && confidence < 0.70")
        t_gte_070 = t.filter("confidence >= 0.70")
        Map.addLayer(t_060_065, {"color": "FF0000"}, "Buildings confidence [0.60 0.65)")
        Map.addLayer(t_065_070, {"color": "FFFF00"}, "Buildings confidence [0.65 0.70)")
        Map.addLayer(t_gte_070, {"color": "00FF00"}, "Buildings confidence >= 0.70")
        Map.setCenter(3.389, 6.492, 17)
        Map.setOptions("SATELLITE")

    elif cod == "GRIDMET/DROUGHT":
        collection = ee.ImageCollection("GRIDMET/DROUGHT")
        dS = "2020-03-30"
        dE = "2020-03-30"
        dSUTC = ee.Date(dS, "GMT")
        dEUTC = ee.Date(dE, "GMT")
        filtered = collection.filterDate(dSUTC, dEUTC.advance(1, "day"))
        PDSI = filtered.select("pdsi")
        Z = filtered.select("z")
        SPI2y = filtered.select("spi2y")
        SPEI2y = filtered.select("spei2y")
        EDDI2y = filtered.select("spei2y")
        usdmColors = ["0000aa","0000ff","00aaff","00ffff","aaff55","ffffff","ffff00","fcd37f","ffaa00","e60000","730000"]
        minColorbar= -2.5
        maxColorbar= 2.5
        colorbarOptions1 = {
            "min":minColorbar,
            "max":maxColorbar,
            "palette": usdmColors}
        minColorbar= -6
        maxColorbar= 6
        colorbarOptions2 = {
            "min":minColorbar,
            "max":maxColorbar,
            "palette": usdmColors}
        Map.addLayer(ee.Image(PDSI.first()), colorbarOptions2, "PDSI")
        Map.addLayer(ee.Image(Z.first()), colorbarOptions2, "Palmer-Z")
        Map.addLayer(ee.Image(SPI2y.first()), colorbarOptions1, "SPI-48months")
        Map.addLayer(ee.Image(SPEI2y.first()), colorbarOptions1, "SPEI-48months")
        Map.addLayer(ee.Image(EDDI2y.first()), colorbarOptions1, "EDDI-48months")

    elif cod == "Germany/Brandenburg/orthos/20cm":
        dataset = ee.Image("Germany/Brandenburg/orthos/20cm")
        Map.setCenter(13.386091, 52.507899, 18)
        Map.addLayer(dataset, None, "Brandenburg 20cm")

    elif cod == "HYCOM/sea_surface_elevation":
        dataset = ee.ImageCollection("HYCOM/sea_surface_elevation").filter(ee.Filter.date("2018-08-01", "2018-08-15"))
        surfaceElevation = dataset.select("surface_elevation")
        surfaceElevationVis = {
        "min": -2000.0,
        "max": 2000.0,
        "palette": ["blue", "cyan", "yellow", "red"],
        }
        Map.setCenter(-28.1, 28.3, 1)
        Map.addLayer(surfaceElevation, surfaceElevationVis, "Surface Elevation")

    elif cod == "HYCOM/sea_temp_salinity":
        dataset = ee.ImageCollection("HYCOM/sea_temp_salinity").filter(ee.Filter.date("2018-08-01", "2018-08-15"))
        seaWaterTemperature = dataset.select("water_temp_0").map(lambda image: ee.Image(image).multiply(0.001).add(20))
        visParams = {
        "min": -2.0,
        "max": 34.0,
        "palette": ["000000", "005aff", "43c8c8", "fff700", "ff0000"],
        }
        Map.setCenter(-88.6, 26.4, 1)
        Map.addLayer(seaWaterTemperature.mean(), visParams, "Sea Water Temperature")


    elif cod == "HYCOM/sea_water_velocity":
        velocity = ee.Image("HYCOM/sea_water_velocity/2014040700").divide(1000)
        Map.addLayer(velocity.select("velocity_u_0").hypot(velocity.select("velocity_v_0")))
        Map.setCenter(-60, 33, 5)

    elif cod == "IDAHO_EPSCOR/GRIDMET":
        dataset = ee.ImageCollection("IDAHO_EPSCOR/GRIDMET").filter(ee.Filter.date("2018-08-01", "2018-08-15"))
        maximumTemperature = dataset.select("tmmx")
        maximumTemperatureVis = {
        "min": 290.0,
        "max": 314.0,
        "palette": ["d8d8d8", "4addff", "5affa3", "f2ff89", "ff725c"],
        }
        Map.setCenter(-115.356, 38.686, 5)
        Map.addLayer(maximumTemperature, maximumTemperatureVis, "Maximum Temperature")

    elif cod == "IDAHO_EPSCOR/MACAv2_METDATA":
        dataset = ee.ImageCollection("IDAHO_EPSCOR/MACAv2_METDATA").filter(ee.Filter.date("2018-08-01", "2018-08-15"))
        maximumTemperature = dataset.select("tasmax")
        maximumTemperatureVis = {
        "min": 290.0,
        "max": 314.0,
        "palette": ["d8d8d8", "4addff", "5affa3", "f2ff89", "ff725c"],
        }
        Map.setCenter(-84.37, 33.5, 5)
        Map.addLayer(maximumTemperature, maximumTemperatureVis, "Maximum Temperature")

    elif cod == "IDAHO_EPSCOR/MACAv2_METDATA_MONTHLY":
        dataset = ee.ImageCollection("IDAHO_EPSCOR/MACAv2_METDATA_MONTHLY").filter(ee.Filter.date("2018-07-01", "2018-08-01"))
        maximumTemperature = dataset.select("tasmax")
        maximumTemperatureVis = {
        "min": 290.0,
        "max": 314.0,
        "palette": ["d8d8d8", "4addff", "5affa3", "f2ff89", "ff725c"],
        }
        Map.setCenter(-115.356, 38.686, 5)
        Map.addLayer(maximumTemperature, maximumTemperatureVis, "Maximum Temperature")

    elif cod == "IDAHO_EPSCOR/TERRACLIMATE":
        dataset = ee.ImageCollection("IDAHO_EPSCOR/TERRACLIMATE").filter(ee.Filter.date("2017-07-01", "2017-08-01"))
        maximumTemperature = dataset.select("tmmx")
        maximumTemperatureVis = {
        "min": -300.0,
        "max": 300.0,
        "palette": ["1a3678", "2955bc", "5699ff", "8dbae9", "acd1ff", "caebff", "e5f9ff",
                    "fdffb4", "ffe6a2", "ffc969", "ffa12d", "ff7c1f", "ca531a", "ff0000", "ab0000"]}
        Map.setCenter(71.72, 52.48, 3)
        Map.addLayer(maximumTemperature, maximumTemperatureVis, "Maximum Temperature")

    elif cod == "IGN/RGE_ALTI/1M/2_0/FXX":
        dataset = ee.Image("IGN/RGE_ALTI/1M/2_0/FXX")
        elevation = dataset.select("MNT")
        elevationVis = {
            "min": 0,
            "max": 1000,
            "palette": ["006600", "002200", "fff700", "ab7634", "c4d0ff", "ffffff"]}
        Map.addLayer(elevation, elevationVis, "Elevation")
        Map.setCenter(3, 47, 5)

    ###https://developers.google.com/earth-engine/datasets/catalog/ISDASOIL_Africa_v1_aluminium_extractable

    elif cod == "ISDASOIL/Africa/v1/aluminium_extractable":
        mean_0_20 = """
            <RasterSymbolizer>
            <ColorMap type="ramp">
            <ColorMapEntry color="#000004" label="0-21.2" opacity="1" quantity="31"/>
            <ColorMapEntry color="#0C0927" label="21.2-35.6" opacity="1" quantity="36"/>
            <ColorMapEntry color="#231151" label="35.6-53.6" opacity="1" quantity="40"/>
            <ColorMapEntry color="#410F75" label="53.6-65.7" opacity="1" quantity="42"/>
            <ColorMapEntry color="#5F187F" label="65.7-72.7" opacity="1" quantity="43"/>
            <ColorMapEntry color="#7B2382" label="72.7-80.5" opacity="1" quantity="44"/>
            <ColorMapEntry color="#982D80" label="80.5-89" opacity="1" quantity="45"/>
            <ColorMapEntry color="#B63679" label="89-98.5" opacity="1" quantity="46"/>
            <ColorMapEntry color="#D3436E" label="98.5-108.9" opacity="1" quantity="47"/>
            <ColorMapEntry color="#EB5760" label="108.9-120.5" opacity="1" quantity="48"/>
            <ColorMapEntry color="#F8765C" label="120.5-133.3" opacity="1" quantity="49"/>
            <ColorMapEntry color="#FD9969" label="133.3-147.4" opacity="1" quantity="50"/>
            <ColorMapEntry color="#FEBA80" label="147.4-163" opacity="1" quantity="51"/>
            <ColorMapEntry color="#FDDC9E" label="163-199.3" opacity="1" quantity="53"/>
            <ColorMapEntry color="#FCFDBF" label="199.3-1800" opacity="1" quantity="55"/>
            </ColorMap>
            <ContrastEnhancement/>
            </RasterSymbolizer> """
        mean_20_50 = """
            <RasterSymbolizer>
            <ColorMap type="ramp">
            <ColorMapEntry color="#000004" label="0-21.2" opacity="1" quantity="31"/>
            <ColorMapEntry color="#0C0927" label="21.2-35.6" opacity="1" quantity="36"/>
            <ColorMapEntry color="#231151" label="35.6-53.6" opacity="1" quantity="40"/>
            <ColorMapEntry color="#410F75" label="53.6-65.7" opacity="1" quantity="42"/>
            <ColorMapEntry color="#5F187F" label="65.7-72.7" opacity="1" quantity="43"/>
            <ColorMapEntry color="#7B2382" label="72.7-80.5" opacity="1" quantity="44"/>
            <ColorMapEntry color="#982D80" label="80.5-89" opacity="1" quantity="45"/>
            <ColorMapEntry color="#B63679" label="89-98.5" opacity="1" quantity="46"/>
            <ColorMapEntry color="#D3436E" label="98.5-108.9" opacity="1" quantity="47"/>
            <ColorMapEntry color="#EB5760" label="108.9-120.5" opacity="1" quantity="48"/>
            <ColorMapEntry color="#F8765C" label="120.5-133.3" opacity="1" quantity="49"/>
            <ColorMapEntry color="#FD9969" label="133.3-147.4" opacity="1" quantity="50"/>
            <ColorMapEntry color="#FEBA80" label="147.4-163" opacity="1" quantity="51"/>
            <ColorMapEntry color="#FDDC9E" label="163-199.3" opacity="1" quantity="53"/>
            <ColorMapEntry color="#FCFDBF" label="199.3-1800" opacity="1" quantity="55"/>
            </ColorMap>
            <ContrastEnhancement/>
            </RasterSymbolizer> """
        stdev_0_20 = """
            <RasterSymbolizer>
            <ColorMap type="ramp">
            <ColorMapEntry color="#fde725" label="low" opacity="1" quantity="5"/>
            <ColorMapEntry color="#5dc962" label=" " opacity="1" quantity="9"/>
            <ColorMapEntry color="#20908d" label=" " opacity="1" quantity="10"/>
            <ColorMapEntry color="#3a528b" label=" " opacity="1" quantity="12"/>
            <ColorMapEntry color="#440154" label="high" opacity="1" quantity="14"/>
            </ColorMap>
            <ContrastEnhancement/>
            </RasterSymbolizer> """
        stdev_20_50 = """
            <RasterSymbolizer>
            <ColorMap type="ramp">
            <ColorMapEntry color="#fde725" label="low" opacity="1" quantity="5"/>
            <ColorMapEntry color="#5dc962" label=" " opacity="1" quantity="9"/>
            <ColorMapEntry color="#20908d" label=" " opacity="1" quantity="10"/>
            <ColorMapEntry color="#3a528b" label=" " opacity="1" quantity="12"/>
            <ColorMapEntry color="#440154" label="high" opacity="1" quantity="14"/>
            </ColorMap>
            <ContrastEnhancement/>
            </RasterSymbolizer> """
        Map.setCenter(25, -3, 2)
        raw = ee.Image("ISDASOIL/Africa/v1/aluminium_extractable")
        Map.addLayer(
        raw.select(0).sldStyle(mean_0_20), {},"Aluminium, extractable, mean visualization, 0-20 cm")
        Map.addLayer(raw.select(1).sldStyle(mean_20_50), {},"Aluminium, extractable, mean visualization, 20-50 cm")
        Map.addLayer(raw.select(2).sldStyle(stdev_0_20), {},"Aluminium, extractable, stdev visualization, 0-20 cm")
        Map.addLayer(raw.select(3).sldStyle(stdev_20_50), {},"Aluminium, extractable, stdev visualization, 20-50 cm")
        converted = raw.divide(10).exp().subtract(1)
        Map.addLayer(converted.select(0), {"min": 0, "max": 100},"Aluminium, extractable, mean, 0-20 cm")

    elif cod == "ISDASOIL/Africa/v1/bedrock_depth":
        mean_0_200 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#00204D" label="0-13" opacity="1" quantity="13"/>
        <ColorMapEntry color="#002D6C" label="13-26" opacity="1" quantity="26"/>
        <ColorMapEntry color="#16396D" label="26-39" opacity="1" quantity="39"/>
        <ColorMapEntry color="#36476B" label="39-52" opacity="1" quantity="52"/>
        <ColorMapEntry color="#4B546C" label="52-65" opacity="1" quantity="65"/>
        <ColorMapEntry color="#5C616E" label="65-78" opacity="1" quantity="78"/>
        <ColorMapEntry color="#6C6E72" label="78-91" opacity="1" quantity="91"/>
        <ColorMapEntry color="#7C7B78" label="91-104" opacity="1" quantity="104"/>
        <ColorMapEntry color="#8E8A79" label="104-117" opacity="1" quantity="117"/>
        <ColorMapEntry color="#A09877" label="117-130" opacity="1" quantity="130"/>
        <ColorMapEntry color="#B3A772" label="130-143" opacity="1" quantity="143"/>
        <ColorMapEntry color="#C6B66B" label="143-156" opacity="1" quantity="156"/>
        <ColorMapEntry color="#DBC761" label="156-169" opacity="1" quantity="169"/>
        <ColorMapEntry color="#F0D852" label="169-182" opacity="1" quantity="182"/>
        <ColorMapEntry color="#FFEA46" label="182-200" opacity="1" quantity="195"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        stdev_0_200 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#fde725" label="low" opacity="1" quantity="14"/>
        <ColorMapEntry color="#5dc962" label=" " opacity="1" quantity="18"/>
        <ColorMapEntry color="#20908d" label=" " opacity="1" quantity="21"/>
        <ColorMapEntry color="#3a528b" label=" " opacity="1" quantity="22"/>
        <ColorMapEntry color="#440154" label="high" opacity="1" quantity="25"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        raw = ee.Image("ISDASOIL/Africa/v1/bedrock_depth")
        Map.addLayer(raw.select(0).sldStyle(mean_0_200), {},"Bedrock depth, mean visualization, 0-200 cm")
        Map.addLayer(raw.select(1).sldStyle(stdev_0_200), {},"Bedrock depth, stdev visualization, 0-200 cm")
        visualization = {"min": 27, "max": 200}
        Map.setCenter(25, -3, 2)
        Map.addLayer(raw.select(0), visualization, "Bedrock depth, mean, 0-200 cm")

    elif cod == "ISDASOIL/Africa/v1/bulk_density":
        mean_0_20 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#00204D" label="0.8-1.05" opacity="1" quantity="105"/>
        <ColorMapEntry color="#002D6C" label="1.05-1.19" opacity="1" quantity="119"/>
        <ColorMapEntry color="#16396D" label="1.19-1.23" opacity="1" quantity="123"/>
        <ColorMapEntry color="#36476B" label="1.23-1.25" opacity="1" quantity="125"/>
        <ColorMapEntry color="#4B546C" label="1.25-1.28" opacity="1" quantity="128"/>
        <ColorMapEntry color="#5C616E" label="1.28-1.31" opacity="1" quantity="131"/>
        <ColorMapEntry color="#6C6E72" label="1.31-1.34" opacity="1" quantity="134"/>
        <ColorMapEntry color="#7C7B78" label="1.34-1.36" opacity="1" quantity="136"/>
        <ColorMapEntry color="#8E8A79" label="1.36-1.38" opacity="1" quantity="138"/>
        <ColorMapEntry color="#A09877" label="1.38-1.41" opacity="1" quantity="141"/>
        <ColorMapEntry color="#B3A772" label="1.41-1.43" opacity="1" quantity="143"/>
        <ColorMapEntry color="#C6B66B" label="1.43-1.45" opacity="1" quantity="145"/>
        <ColorMapEntry color="#DBC761" label="1.45-1.48" opacity="1" quantity="148"/>
        <ColorMapEntry color="#F0D852" label="1.48-1.51" opacity="1" quantity="151"/>
        <ColorMapEntry color="#FFEA46" label="1.51-1.85" opacity="1" quantity="154"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        mean_20_50 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#00204D" label="0.8-1.05" opacity="1" quantity="105"/>
        <ColorMapEntry color="#002D6C" label="1.05-1.19" opacity="1" quantity="119"/>
        <ColorMapEntry color="#16396D" label="1.19-1.23" opacity="1" quantity="123"/>
        <ColorMapEntry color="#36476B" label="1.23-1.25" opacity="1" quantity="125"/>
        <ColorMapEntry color="#4B546C" label="1.25-1.28" opacity="1" quantity="128"/>
        <ColorMapEntry color="#5C616E" label="1.28-1.31" opacity="1" quantity="131"/>
        <ColorMapEntry color="#6C6E72" label="1.31-1.34" opacity="1" quantity="134"/>
        <ColorMapEntry color="#7C7B78" label="1.34-1.36" opacity="1" quantity="136"/>
        <ColorMapEntry color="#8E8A79" label="1.36-1.38" opacity="1" quantity="138"/>
        <ColorMapEntry color="#A09877" label="1.38-1.41" opacity="1" quantity="141"/>
        <ColorMapEntry color="#B3A772" label="1.41-1.43" opacity="1" quantity="143"/>
        <ColorMapEntry color="#C6B66B" label="1.43-1.45" opacity="1" quantity="145"/>
        <ColorMapEntry color="#DBC761" label="1.45-1.48" opacity="1" quantity="148"/>
        <ColorMapEntry color="#F0D852" label="1.48-1.51" opacity="1" quantity="151"/>
        <ColorMapEntry color="#FFEA46" label="1.51-1.85" opacity="1" quantity="154"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        stdev_0_20 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#fde725" label="low" opacity="1" quantity="2"/>
        <ColorMapEntry color="#5dc962" label=" " opacity="1" quantity="4"/>
        <ColorMapEntry color="#20908d" label=" " opacity="1" quantity="5"/>
        <ColorMapEntry color="#3a528b" label=" " opacity="1" quantity="7"/>
        <ColorMapEntry color="#440154" label="high" opacity="1" quantity="9"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        stdev_20_50 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#fde725" label="low" opacity="1" quantity="2"/>
        <ColorMapEntry color="#5dc962" label=" " opacity="1" quantity="4"/>
        <ColorMapEntry color="#20908d" label=" " opacity="1" quantity="5"/>
        <ColorMapEntry color="#3a528b" label=" " opacity="1" quantity="7"/>
        <ColorMapEntry color="#440154" label="high" opacity="1" quantity="9"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        raw = ee.Image("ISDASOIL/Africa/v1/bulk_density")
        Map.addLayer(raw.select(0).sldStyle(mean_0_20), {},"Bulk density, mean visualization, 0-20 cm")
        Map.addLayer(raw.select(1).sldStyle(mean_20_50), {},"Bulk density, mean visualization, 20-50 cm")
        Map.addLayer(raw.select(2).sldStyle(stdev_0_20), {},"Bulk density, stdev visualization, 0-20 cm")
        Map.addLayer(raw.select(3).sldStyle(stdev_20_50), {},"Bulk density, stdev visualization, 20-50 cm")
        converted = raw.divide(100)
        visualization = {"min": 1, "max": 1.5}
        Map.setCenter(25, -3, 2)
        Map.addLayer(converted.select(0), visualization, "Bulk density, mean, 0-20 cm")

    elif cod == "ISDASOIL/Africa/v1/calcium_extractable":
        mean_0_20 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#0D0887" label="0-65.7" opacity="1" quantity="42"/>
        <ColorMapEntry color="#350498" label="65.7-120.5" opacity="1" quantity="48"/>
        <ColorMapEntry color="#5402A3" label="120.5-163" opacity="1" quantity="51"/>
        <ColorMapEntry color="#7000A8" label="163-199.3" opacity="1" quantity="53"/>
        <ColorMapEntry color="#8B0AA5" label="199.3-269.4" opacity="1" quantity="56"/>
        <ColorMapEntry color="#A31E9A" label="269.4-329.3" opacity="1" quantity="58"/>
        <ColorMapEntry color="#B93289" label="329.3-402.4" opacity="1" quantity="60"/>
        <ColorMapEntry color="#CC4678" label="402.4-491.7" opacity="1" quantity="62"/>
        <ColorMapEntry color="#DB5C68" label="491.7-600.8" opacity="1" quantity="64"/>
        <ColorMapEntry color="#E97158" label="600.8-664.1" opacity="1" quantity="65"/>
        <ColorMapEntry color="#F48849" label="664.1-811.4" opacity="1" quantity="67"/>
        <ColorMapEntry color="#FBA139" label="811.4-896.8" opacity="1" quantity="68"/>
        <ColorMapEntry color="#FEBC2A" label="896.8-1095.6" opacity="1" quantity="70"/>
        <ColorMapEntry color="#FADA24" label="1095.6-1479.3" opacity="1" quantity="73"/>
        <ColorMapEntry color="#F0F921" label="1479.3-12000" opacity="1" quantity="77"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        mean_20_50 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#0D0887" label="0-65.7" opacity="1" quantity="42"/>
        <ColorMapEntry color="#350498" label="65.7-120.5" opacity="1" quantity="48"/>
        <ColorMapEntry color="#5402A3" label="120.5-163" opacity="1" quantity="51"/>
        <ColorMapEntry color="#7000A8" label="163-199.3" opacity="1" quantity="53"/>
        <ColorMapEntry color="#8B0AA5" label="199.3-269.4" opacity="1" quantity="56"/>
        <ColorMapEntry color="#A31E9A" label="269.4-329.3" opacity="1" quantity="58"/>
        <ColorMapEntry color="#B93289" label="329.3-402.4" opacity="1" quantity="60"/>
        <ColorMapEntry color="#CC4678" label="402.4-491.7" opacity="1" quantity="62"/>
        <ColorMapEntry color="#DB5C68" label="491.7-600.8" opacity="1" quantity="64"/>
        <ColorMapEntry color="#E97158" label="600.8-664.1" opacity="1" quantity="65"/>
        <ColorMapEntry color="#F48849" label="664.1-811.4" opacity="1" quantity="67"/>
        <ColorMapEntry color="#FBA139" label="811.4-896.8" opacity="1" quantity="68"/>
        <ColorMapEntry color="#FEBC2A" label="896.8-1095.6" opacity="1" quantity="70"/>
        <ColorMapEntry color="#FADA24" label="1095.6-1479.3" opacity="1" quantity="73"/>
        <ColorMapEntry color="#F0F921" label="1479.3-12000" opacity="1" quantity="77"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        stdev_0_20 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#fde725" label="low" opacity="1" quantity="1"/>
        <ColorMapEntry color="#5dc962" label=" " opacity="1" quantity="2"/>
        <ColorMapEntry color="#20908d" label=" " opacity="1" quantity="3"/>
        <ColorMapEntry color="#3a528b" label=" " opacity="1" quantity="4"/>
        <ColorMapEntry color="#440154" label="high" opacity="1" quantity="5"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        stdev_20_50 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#fde725" label="low" opacity="1" quantity="1"/>
        <ColorMapEntry color="#5dc962" label=" " opacity="1" quantity="2"/>
        <ColorMapEntry color="#20908d" label=" " opacity="1" quantity="3"/>
        <ColorMapEntry color="#3a528b" label=" " opacity="1" quantity="4"/>
        <ColorMapEntry color="#440154" label="high" opacity="1" quantity="5"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        raw = ee.Image("ISDASOIL/Africa/v1/calcium_extractable")
        Map.addLayer(raw.select(0).sldStyle(mean_0_20), {},"Calcium, extractable, mean visualization, 0-20 cm")
        Map.addLayer(raw.select(1).sldStyle(mean_20_50), {},"Calcium, extractable, mean visualization, 20-50 cm")
        Map.addLayer(raw.select(2).sldStyle(stdev_0_20), {},"Calcium, extractable, stdev visualization, 0-20 cm")
        Map.addLayer(raw.select(3).sldStyle(stdev_20_50), {},"Calcium, extractable, stdev visualization, 20-50 cm")
        converted = raw.divide(10).exp().subtract(1)
        visualization = {"min": 100, "max": 2000}
        Map.setCenter(25, -3, 2)
        Map.addLayer(converted.select(0), visualization, "Calcium, extractable, mean, 0-20 cm")

    elif cod == "ISDASOIL/Africa/v1/carbon_organic":
        mean_0_20 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#000004" label="0-2.3" opacity="1" quantity="12"/>
        <ColorMapEntry color="#0C0927" label="2.3-3.5" opacity="1" quantity="15"/>
        <ColorMapEntry color="#231151" label="3.5-4" opacity="1" quantity="16"/>
        <ColorMapEntry color="#410F75" label="4-4.5" opacity="1" quantity="17"/>
        <ColorMapEntry color="#5F187F" label="4.5-5" opacity="1" quantity="18"/>
        <ColorMapEntry color="#7B2382" label="5-5.7" opacity="1" quantity="19"/>
        <ColorMapEntry color="#982D80" label="5.7-6.4" opacity="1" quantity="20"/>
        <ColorMapEntry color="#B63679" label="6.4-7.2" opacity="1" quantity="21"/>
        <ColorMapEntry color="#D3436E" label="7.2-8" opacity="1" quantity="22"/>
        <ColorMapEntry color="#EB5760" label="8-9" opacity="1" quantity="23"/>
        <ColorMapEntry color="#F8765C" label="9-10" opacity="1" quantity="24"/>
        <ColorMapEntry color="#FD9969" label="10-11.2" opacity="1" quantity="25"/>
        <ColorMapEntry color="#FEBA80" label="11.2-12.5" opacity="1" quantity="26"/>
        <ColorMapEntry color="#FDDC9E" label="12.5-13.9" opacity="1" quantity="27"/>
        <ColorMapEntry color="#FCFDBF" label="13.9-40" opacity="1" quantity="28"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        mean_20_50 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#000004" label="0-2.3" opacity="1" quantity="12"/>
        <ColorMapEntry color="#0C0927" label="2.3-3.5" opacity="1" quantity="15"/>
        <ColorMapEntry color="#231151" label="3.5-4" opacity="1" quantity="16"/>
        <ColorMapEntry color="#410F75" label="4-4.5" opacity="1" quantity="17"/>
        <ColorMapEntry color="#5F187F" label="4.5-5" opacity="1" quantity="18"/>
        <ColorMapEntry color="#7B2382" label="5-5.7" opacity="1" quantity="19"/>
        <ColorMapEntry color="#982D80" label="5.7-6.4" opacity="1" quantity="20"/>
        <ColorMapEntry color="#B63679" label="6.4-7.2" opacity="1" quantity="21"/>
        <ColorMapEntry color="#D3436E" label="7.2-8" opacity="1" quantity="22"/>
        <ColorMapEntry color="#EB5760" label="8-9" opacity="1" quantity="23"/>
        <ColorMapEntry color="#F8765C" label="9-10" opacity="1" quantity="24"/>
        <ColorMapEntry color="#FD9969" label="10-11.2" opacity="1" quantity="25"/>
        <ColorMapEntry color="#FEBA80" label="11.2-12.5" opacity="1" quantity="26"/>
        <ColorMapEntry color="#FDDC9E" label="12.5-13.9" opacity="1" quantity="27"/>
        <ColorMapEntry color="#FCFDBF" label="13.9-40" opacity="1" quantity="28"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        stdev_0_20 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#fde725" label="low" opacity="1" quantity="1"/>
        <ColorMapEntry color="#5dc962" label=" " opacity="1" quantity="2"/>
        <ColorMapEntry color="#20908d" label=" " opacity="1" quantity="3"/>
        <ColorMapEntry color="#3a528b" label=" " opacity="1" quantity="4"/>
        <ColorMapEntry color="#440154" label="high" opacity="1" quantity="5"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        stdev_20_50 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#fde725" label="low" opacity="1" quantity="1"/>
        <ColorMapEntry color="#5dc962" label=" " opacity="1" quantity="2"/>
        <ColorMapEntry color="#20908d" label=" " opacity="1" quantity="3"/>
        <ColorMapEntry color="#3a528b" label=" " opacity="1" quantity="4"/>
        <ColorMapEntry color="#440154" label="high" opacity="1" quantity="5"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        raw = ee.Image("ISDASOIL/Africa/v1/carbon_organic")
        Map.addLayer(raw.select(0).sldStyle(mean_0_20), {},"Carbon, organic, mean visualization, 0-20 cm")
        Map.addLayer(raw.select(1).sldStyle(mean_20_50), {},"Carbon, organic, mean visualization, 20-50 cm")
        Map.addLayer(raw.select(2).sldStyle(stdev_0_20), {},"Carbon, organic, stdev visualization, 0-20 cm")
        Map.addLayer(raw.select(3).sldStyle(stdev_20_50), {},"Carbon, organic, stdev visualization, 20-50 cm")
        converted = raw.divide(10).exp().subtract(1)
        visualization = {"min": 0, "max": 20}
        Map.setCenter(25, -3, 2)
        Map.addLayer(converted.select(0), visualization, "Carbon, organic, mean, 0-20 cm")

    elif cod == "ISDASOIL/Africa/v1/carbon_total":
        mean_0_20 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#000004" label="0-2" opacity="1" quantity="11"/>
        <ColorMapEntry color="#0C0927" label="2-5.7" opacity="1" quantity="19"/>
        <ColorMapEntry color="#231151" label="5.7-10" opacity="1" quantity="24"/>
        <ColorMapEntry color="#410F75" label="10-12.5" opacity="1" quantity="26"/>
        <ColorMapEntry color="#5F187F" label="12.5-13.9" opacity="1" quantity="27"/>
        <ColorMapEntry color="#7B2382" label="13.9-15.4" opacity="1" quantity="28"/>
        <ColorMapEntry color="#982D80" label="15.4-17.2" opacity="1" quantity="29"/>
        <ColorMapEntry color="#B63679" label="17.2-19.1" opacity="1" quantity="30"/>
        <ColorMapEntry color="#D3436E" label="19.1-21.2" opacity="1" quantity="31"/>
        <ColorMapEntry color="#EB5760" label="21.2-23.5" opacity="1" quantity="32"/>
        <ColorMapEntry color="#F8765C" label="23.5-26.1" opacity="1" quantity="33"/>
        <ColorMapEntry color="#FD9969" label="26.1-29" opacity="1" quantity="34"/>
        <ColorMapEntry color="#FEBA80" label="29-32.1" opacity="1" quantity="35"/>
        <ColorMapEntry color="#FDDC9E" label="32.1-35.6" opacity="1" quantity="36"/>
        <ColorMapEntry color="#FCFDBF" label="35.6-40" opacity="1" quantity="39"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        mean_20_50 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#000004" label="0-2" opacity="1" quantity="11"/>
        <ColorMapEntry color="#0C0927" label="2-5.7" opacity="1" quantity="19"/>
        <ColorMapEntry color="#231151" label="5.7-10" opacity="1" quantity="24"/>
        <ColorMapEntry color="#410F75" label="10-12.5" opacity="1" quantity="26"/>
        <ColorMapEntry color="#5F187F" label="12.5-13.9" opacity="1" quantity="27"/>
        <ColorMapEntry color="#7B2382" label="13.9-15.4" opacity="1" quantity="28"/>
        <ColorMapEntry color="#982D80" label="15.4-17.2" opacity="1" quantity="29"/>
        <ColorMapEntry color="#B63679" label="17.2-19.1" opacity="1" quantity="30"/>
        <ColorMapEntry color="#D3436E" label="19.1-21.2" opacity="1" quantity="31"/>
        <ColorMapEntry color="#EB5760" label="21.2-23.5" opacity="1" quantity="32"/>
        <ColorMapEntry color="#F8765C" label="23.5-26.1" opacity="1" quantity="33"/>
        <ColorMapEntry color="#FD9969" label="26.1-29" opacity="1" quantity="34"/>
        <ColorMapEntry color="#FEBA80" label="29-32.1" opacity="1" quantity="35"/>
        <ColorMapEntry color="#FDDC9E" label="32.1-35.6" opacity="1" quantity="36"/>
        <ColorMapEntry color="#FCFDBF" label="35.6-40" opacity="1" quantity="39"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        stdev_0_20 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#fde725" label="low" opacity="1" quantity="1"/>
        <ColorMapEntry color="#5dc962" label=" " opacity="1" quantity="3"/>
        <ColorMapEntry color="#20908d" label=" " opacity="1" quantity="4"/>
        <ColorMapEntry color="#3a528b" label=" " opacity="1" quantity="5"/>
        <ColorMapEntry color="#440154" label="high" opacity="1" quantity="6"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        stdev_20_50 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#fde725" label="low" opacity="1" quantity="1"/>
        <ColorMapEntry color="#5dc962" label=" " opacity="1" quantity="3"/>
        <ColorMapEntry color="#20908d" label=" " opacity="1" quantity="4"/>
        <ColorMapEntry color="#3a528b" label=" " opacity="1" quantity="5"/>
        <ColorMapEntry color="#440154" label="high" opacity="1" quantity="6"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        raw = ee.Image("ISDASOIL/Africa/v1/carbon_total")
        Map.addLayer(raw.select(0).sldStyle(mean_0_20), {},"Carbon, total, mean visualization, 0-20 cm")
        Map.addLayer(raw.select(1).sldStyle(mean_20_50), {},"Carbon, total, mean visualization, 20-50 cm")
        Map.addLayer(raw.select(2).sldStyle(stdev_0_20), {},"Carbon, total, stdev visualization, 0-20 cm")
        Map.addLayer(raw.select(3).sldStyle(stdev_20_50), {},"Carbon, total, stdev visualization, 20-50 cm")
        converted = raw.divide(10).exp().subtract(1)
        visualization = {"min": 0, "max": 60}
        Map.setCenter(25, -3, 2)
        Map.addLayer(converted.select(0), visualization, "Carbon, total, mean, 0-20 cm")

    elif cod == "ISDASOIL/Africa/v1/cation_exchange_capacity":
        mean_0_20 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#000004" label="0-3.5" opacity="1" quantity="15"/>
        <ColorMapEntry color="#0C0927" label="3.5-4.5" opacity="1" quantity="17"/>
        <ColorMapEntry color="#231151" label="4.5-5" opacity="1" quantity="18"/>
        <ColorMapEntry color="#410F75" label="5-6.4" opacity="1" quantity="20"/>
        <ColorMapEntry color="#5F187F" label="6.4-7.2" opacity="1" quantity="21"/>
        <ColorMapEntry color="#7B2382" label="7.2-8" opacity="1" quantity="22"/>
        <ColorMapEntry color="#982D80" label="8-9" opacity="1" quantity="23"/>
        <ColorMapEntry color="#B63679" label="9-10" opacity="1" quantity="24"/>
        <ColorMapEntry color="#D3436E" label="10-11.2" opacity="1" quantity="25"/>
        <ColorMapEntry color="#EB5760" label="11.2-12.5" opacity="1" quantity="26"/>
        <ColorMapEntry color="#F8765C" label="12.5-13.9" opacity="1" quantity="27"/>
        <ColorMapEntry color="#FD9969" label="13.9-15.4" opacity="1" quantity="28"/>
        <ColorMapEntry color="#FEBA80" label="15.4-17.2" opacity="1" quantity="29"/>
        <ColorMapEntry color="#FDDC9E" label="17.2-19.1" opacity="1" quantity="30"/>
        <ColorMapEntry color="#FCFDBF" label="19.1-130" opacity="1" quantity="31"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        mean_20_50 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#000004" label="0-3.5" opacity="1" quantity="15"/>
        <ColorMapEntry color="#0C0927" label="3.5-4.5" opacity="1" quantity="17"/>
        <ColorMapEntry color="#231151" label="4.5-5" opacity="1" quantity="18"/>
        <ColorMapEntry color="#410F75" label="5-6.4" opacity="1" quantity="20"/>
        <ColorMapEntry color="#5F187F" label="6.4-7.2" opacity="1" quantity="21"/>
        <ColorMapEntry color="#7B2382" label="7.2-8" opacity="1" quantity="22"/>
        <ColorMapEntry color="#982D80" label="8-9" opacity="1" quantity="23"/>
        <ColorMapEntry color="#B63679" label="9-10" opacity="1" quantity="24"/>
        <ColorMapEntry color="#D3436E" label="10-11.2" opacity="1" quantity="25"/>
        <ColorMapEntry color="#EB5760" label="11.2-12.5" opacity="1" quantity="26"/>
        <ColorMapEntry color="#F8765C" label="12.5-13.9" opacity="1" quantity="27"/>
        <ColorMapEntry color="#FD9969" label="13.9-15.4" opacity="1" quantity="28"/>
        <ColorMapEntry color="#FEBA80" label="15.4-17.2" opacity="1" quantity="29"/>
        <ColorMapEntry color="#FDDC9E" label="17.2-19.1" opacity="1" quantity="30"/>
        <ColorMapEntry color="#FCFDBF" label="19.1-130" opacity="1" quantity="31"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        stdev_0_20 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#fde725" label="low" opacity="1" quantity="1"/>
        <ColorMapEntry color="#5dc962" label=" " opacity="1" quantity="2"/>
        <ColorMapEntry color="#20908d" label=" " opacity="1" quantity="3"/>
        <ColorMapEntry color="#3a528b" label=" " opacity="1" quantity="4"/>
        <ColorMapEntry color="#440154" label="high" opacity="1" quantity="5"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        stdev_20_50 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#fde725" label="low" opacity="1" quantity="1"/>
        <ColorMapEntry color="#5dc962" label=" " opacity="1" quantity="2"/>
        <ColorMapEntry color="#20908d" label=" " opacity="1" quantity="3"/>
        <ColorMapEntry color="#3a528b" label=" " opacity="1" quantity="4"/>
        <ColorMapEntry color="#440154" label="high" opacity="1" quantity="5"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        raw = ee.Image("ISDASOIL/Africa/v1/cation_exchange_capacity")
        Map.addLayer(raw.select(0).sldStyle(mean_0_20), {},"Cation exchange capacity, mean visualization, 0-20 cm")
        Map.addLayer(raw.select(1).sldStyle(mean_20_50), {},"Cation exchange capacity, mean visualization, 20-50 cm")
        Map.addLayer(raw.select(2).sldStyle(stdev_0_20), {},"Cation exchange capacity, stdev visualization, 0-20 cm")
        Map.addLayer(raw.select(3).sldStyle(stdev_20_50), {},"Cation exchange capacity, stdev visualization, 20-50 cm")
        converted = raw.divide(10).exp().subtract(1)
        visualization = {"min": 0, "max": 25}
        Map.setCenter(25, -3, 2)
        Map.addLayer(converted.select(0), visualization, "Cation exchange capacity, mean, 0-20 cm")

    elif cod == "ISDASOIL/Africa/v1/clay_content":
        mean_0_20 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#00204D" label="0-8" opacity="1" quantity="8"/>
        <ColorMapEntry color="#002D6C" label="8-14" opacity="1" quantity="14"/>
        <ColorMapEntry color="#16396D" label="14-17" opacity="1" quantity="17"/>
        <ColorMapEntry color="#36476B" label="17-19" opacity="1" quantity="19"/>
        <ColorMapEntry color="#4B546C" label="19-21" opacity="1" quantity="21"/>
        <ColorMapEntry color="#5C616E" label="21-22" opacity="1" quantity="22"/>
        <ColorMapEntry color="#6C6E72" label="22-24" opacity="1" quantity="24"/>
        <ColorMapEntry color="#7C7B78" label="24-25" opacity="1" quantity="25"/>
        <ColorMapEntry color="#8E8A79" label="25-26" opacity="1" quantity="26"/>
        <ColorMapEntry color="#A09877" label="26-28" opacity="1" quantity="28"/>
        <ColorMapEntry color="#B3A772" label="28-30" opacity="1" quantity="30"/>
        <ColorMapEntry color="#C6B66B" label="30-31" opacity="1" quantity="31"/>
        <ColorMapEntry color="#DBC761" label="31-33" opacity="1" quantity="33"/>
        <ColorMapEntry color="#F0D852" label="33-36" opacity="1" quantity="36"/>
        <ColorMapEntry color="#FFEA46" label="36-70" opacity="1" quantity="40"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        mean_20_50 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#00204D" label="0-8" opacity="1" quantity="8"/>
        <ColorMapEntry color="#002D6C" label="8-14" opacity="1" quantity="14"/>
        <ColorMapEntry color="#16396D" label="14-17" opacity="1" quantity="17"/>
        <ColorMapEntry color="#36476B" label="17-19" opacity="1" quantity="19"/>
        <ColorMapEntry color="#4B546C" label="19-21" opacity="1" quantity="21"/>
        <ColorMapEntry color="#5C616E" label="21-22" opacity="1" quantity="22"/>
        <ColorMapEntry color="#6C6E72" label="22-24" opacity="1" quantity="24"/>
        <ColorMapEntry color="#7C7B78" label="24-25" opacity="1" quantity="25"/>
        <ColorMapEntry color="#8E8A79" label="25-26" opacity="1" quantity="26"/>
        <ColorMapEntry color="#A09877" label="26-28" opacity="1" quantity="28"/>
        <ColorMapEntry color="#B3A772" label="28-30" opacity="1" quantity="30"/>
        <ColorMapEntry color="#C6B66B" label="30-31" opacity="1" quantity="31"/>
        <ColorMapEntry color="#DBC761" label="31-33" opacity="1" quantity="33"/>
        <ColorMapEntry color="#F0D852" label="33-36" opacity="1" quantity="36"/>
        <ColorMapEntry color="#FFEA46" label="36-70" opacity="1" quantity="40"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        stdev_0_20 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#fde725" label="low" opacity="1" quantity="1"/>
        <ColorMapEntry color="#5dc962" label=" " opacity="1" quantity="2"/>
        <ColorMapEntry color="#20908d" label=" " opacity="1" quantity="3"/>
        <ColorMapEntry color="#3a528b" label=" " opacity="1" quantity="4"/>
        <ColorMapEntry color="#440154" label="high" opacity="1" quantity="6"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        stdev_20_50 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#fde725" label="low" opacity="1" quantity="1"/>
        <ColorMapEntry color="#5dc962" label=" " opacity="1" quantity="2"/>
        <ColorMapEntry color="#20908d" label=" " opacity="1" quantity="3"/>
        <ColorMapEntry color="#3a528b" label=" " opacity="1" quantity="4"/>
        <ColorMapEntry color="#440154" label="high" opacity="1" quantity="6"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        raw = ee.Image("ISDASOIL/Africa/v1/clay_content")
        Map.addLayer(raw.select(0).sldStyle(mean_0_20), {},"Clay content, mean visualization, 0-20 cm")
        Map.addLayer(raw.select(1).sldStyle(mean_20_50), {},"Clay content, mean visualization, 20-50 cm")
        Map.addLayer(raw.select(2).sldStyle(stdev_0_20), {},"Clay content, stdev visualization, 0-20 cm")
        Map.addLayer(raw.select(3).sldStyle(stdev_20_50), {},"Clay content, stdev visualization, 20-50 cm")
        converted = raw.divide(10).exp().subtract(1)
        visualization = {"min": 0, "max": 50}
        Map.setCenter(25, -3, 2)
        Map.addLayer(converted.select(0), visualization, "Clay content, mean, 0-20 cm")

    elif cod == "ISDASOIL/Africa/v1/fcc":
        raw = ee.Image("ISDASOIL/Africa/v1/fcc").select(0)
        converted = ee.Image(raw.mod(3000).copyProperties(raw))
        Map.setCenter(25, -3, 2)
        Map.addLayer(converted, {}, "Fertility Capability Classification")

    elif cod == "ISDASOIL/Africa/v1/iron_extractable":
        mean_0_20 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#0D0887" label="0-6.4" opacity="1" quantity="20"/>
        <ColorMapEntry color="#350498" label="6.4-13.9" opacity="1" quantity="27"/>
        <ColorMapEntry color="#5402A3" label="13.9-29" opacity="1" quantity="34"/>
        <ColorMapEntry color="#7000A8" label="29-35.6" opacity="1" quantity="36"/>
        <ColorMapEntry color="#8B0AA5" label="35.6-43.7" opacity="1" quantity="38"/>
        <ColorMapEntry color="#A31E9A" label="43.7-48.4" opacity="1" quantity="39"/>
        <ColorMapEntry color="#B93289" label="48.4-53.6" opacity="1" quantity="40"/>
        <ColorMapEntry color="#CC4678" label="53.6-59.3" opacity="1" quantity="41"/>
        <ColorMapEntry color="#DB5C68" label="59.3-65.7" opacity="1" quantity="42"/>
        <ColorMapEntry color="#E97158" label="65.7-72.7" opacity="1" quantity="43"/>
        <ColorMapEntry color="#F48849" label="72.7-80.5" opacity="1" quantity="44"/>
        <ColorMapEntry color="#FBA139" label="80.5-89" opacity="1" quantity="45"/>
        <ColorMapEntry color="#FEBC2A" label="89-98.5" opacity="1" quantity="46"/>
        <ColorMapEntry color="#FADA24" label="98.5-108.9" opacity="1" quantity="47"/>
        <ColorMapEntry color="#F0F921" label="108.9-1200" opacity="1" quantity="48"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        mean_20_50 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#0D0887" label="0-6.4" opacity="1" quantity="20"/>
        <ColorMapEntry color="#350498" label="6.4-13.9" opacity="1" quantity="27"/>
        <ColorMapEntry color="#5402A3" label="13.9-29" opacity="1" quantity="34"/>
        <ColorMapEntry color="#7000A8" label="29-35.6" opacity="1" quantity="36"/>
        <ColorMapEntry color="#8B0AA5" label="35.6-43.7" opacity="1" quantity="38"/>
        <ColorMapEntry color="#A31E9A" label="43.7-48.4" opacity="1" quantity="39"/>
        <ColorMapEntry color="#B93289" label="48.4-53.6" opacity="1" quantity="40"/>
        <ColorMapEntry color="#CC4678" label="53.6-59.3" opacity="1" quantity="41"/>
        <ColorMapEntry color="#DB5C68" label="59.3-65.7" opacity="1" quantity="42"/>
        <ColorMapEntry color="#E97158" label="65.7-72.7" opacity="1" quantity="43"/>
        <ColorMapEntry color="#F48849" label="72.7-80.5" opacity="1" quantity="44"/>
        <ColorMapEntry color="#FBA139" label="80.5-89" opacity="1" quantity="45"/>
        <ColorMapEntry color="#FEBC2A" label="89-98.5" opacity="1" quantity="46"/>
        <ColorMapEntry color="#FADA24" label="98.5-108.9" opacity="1" quantity="47"/>
        <ColorMapEntry color="#F0F921" label="108.9-1200" opacity="1" quantity="48"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        stdev_0_20 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#fde725" label="low" opacity="1" quantity="1"/>
        <ColorMapEntry color="#5dc962" label=" " opacity="1" quantity="2"/>
        <ColorMapEntry color="#20908d" label=" " opacity="1" quantity="3"/>
        <ColorMapEntry color="#3a528b" label=" " opacity="1" quantity="4"/>
        <ColorMapEntry color="#440154" label="high" opacity="1" quantity="6"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        stdev_20_50 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#fde725" label="low" opacity="1" quantity="1"/>
        <ColorMapEntry color="#5dc962" label=" " opacity="1" quantity="2"/>
        <ColorMapEntry color="#20908d" label=" " opacity="1" quantity="3"/>
        <ColorMapEntry color="#3a528b" label=" " opacity="1" quantity="4"/>
        <ColorMapEntry color="#440154" label="high" opacity="1" quantity="6"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        raw = ee.Image("ISDASOIL/Africa/v1/iron_extractable")
        Map.addLayer(raw.select(0).sldStyle(mean_0_20), {},"Iron, extractable, mean visualization, 0-20 cm")
        Map.addLayer(raw.select(1).sldStyle(mean_20_50), {},"Iron, extractable, mean visualization, 20-50 cm")
        Map.addLayer(raw.select(2).sldStyle(stdev_0_20), {},"Iron, extractable, stdev visualization, 0-20 cm")
        Map.addLayer(raw.select(3).sldStyle(stdev_20_50), {},"Iron, extractable, stdev visualization, 20-50 cm")
        converted = raw.divide(10).exp().subtract(1)
        visualization = {"min": 0, "max": 140}
        Map.setCenter(25, -3, 2)
        Map.addLayer(converted.select(0), visualization, "Iron, extractable, mean, 0-20 cm")

    elif cod == "ISDASOIL/Africa/v1/magnesium_extractable":
        mean_0_20 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#0D0887" label="0-19.1" opacity="1" quantity="30"/>
        <ColorMapEntry color="#350498" label="19.1-29" opacity="1" quantity="34"/>
        <ColorMapEntry color="#5402A3" label="29-39.4" opacity="1" quantity="37"/>
        <ColorMapEntry color="#7000A8" label="39.4-53.6" opacity="1" quantity="40"/>
        <ColorMapEntry color="#8B0AA5" label="53.6-72.7" opacity="1" quantity="43"/>
        <ColorMapEntry color="#A31E9A" label="72.7-89" opacity="1" quantity="45"/>
        <ColorMapEntry color="#B93289" label="89-108.9" opacity="1" quantity="47"/>
        <ColorMapEntry color="#CC4678" label="108.9-120.5" opacity="1" quantity="48"/>
        <ColorMapEntry color="#DB5C68" label="120.5-133.3" opacity="1" quantity="49"/>
        <ColorMapEntry color="#E97158" label="133.3-163" opacity="1" quantity="51"/>
        <ColorMapEntry color="#F48849" label="163-180.3" opacity="1" quantity="52"/>
        <ColorMapEntry color="#FBA139" label="180.3-220.4" opacity="1" quantity="54"/>
        <ColorMapEntry color="#FEBC2A" label="220.4-243.7" opacity="1" quantity="55"/>
        <ColorMapEntry color="#FADA24" label="243.7-297.9" opacity="1" quantity="57"/>
        <ColorMapEntry color="#F0F921" label="243.7-1200" opacity="1" quantity="60"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        mean_20_50 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#0D0887" label="0-19.1" opacity="1" quantity="30"/>
        <ColorMapEntry color="#350498" label="19.1-29" opacity="1" quantity="34"/>
        <ColorMapEntry color="#5402A3" label="29-39.4" opacity="1" quantity="37"/>
        <ColorMapEntry color="#7000A8" label="39.4-53.6" opacity="1" quantity="40"/>
        <ColorMapEntry color="#8B0AA5" label="53.6-72.7" opacity="1" quantity="43"/>
        <ColorMapEntry color="#A31E9A" label="72.7-89" opacity="1" quantity="45"/>
        <ColorMapEntry color="#B93289" label="89-108.9" opacity="1" quantity="47"/>
        <ColorMapEntry color="#CC4678" label="108.9-120.5" opacity="1" quantity="48"/>
        <ColorMapEntry color="#DB5C68" label="120.5-133.3" opacity="1" quantity="49"/>
        <ColorMapEntry color="#E97158" label="133.3-163" opacity="1" quantity="51"/>
        <ColorMapEntry color="#F48849" label="163-180.3" opacity="1" quantity="52"/>
        <ColorMapEntry color="#FBA139" label="180.3-220.4" opacity="1" quantity="54"/>
        <ColorMapEntry color="#FEBC2A" label="220.4-243.7" opacity="1" quantity="55"/>
        <ColorMapEntry color="#FADA24" label="243.7-297.9" opacity="1" quantity="57"/>
        <ColorMapEntry color="#F0F921" label="243.7-1200" opacity="1" quantity="60"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        stdev_0_20 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#fde725" label="low" opacity="1" quantity="1"/>
        <ColorMapEntry color="#5dc962" label=" " opacity="1" quantity="2"/>
        <ColorMapEntry color="#20908d" label=" " opacity="1" quantity="3"/>
        <ColorMapEntry color="#3a528b" label=" " opacity="1" quantity="4"/>
        <ColorMapEntry color="#440154" label="high" opacity="1" quantity="5"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        stdev_20_50 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#fde725" label="low" opacity="1" quantity="1"/>
        <ColorMapEntry color="#5dc962" label=" " opacity="1" quantity="2"/>
        <ColorMapEntry color="#20908d" label=" " opacity="1" quantity="3"/>
        <ColorMapEntry color="#3a528b" label=" " opacity="1" quantity="4"/>
        <ColorMapEntry color="#440154" label="high" opacity="1" quantity="5"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        raw = ee.Image("ISDASOIL/Africa/v1/magnesium_extractable")
        Map.addLayer(raw.select(0).sldStyle(mean_0_20), {},"Magnesium, extractable, mean visualization, 0-20 cm")
        Map.addLayer(raw.select(1).sldStyle(mean_20_50), {},"Magnesium, extractable, mean visualization, 20-50 cm")
        Map.addLayer(raw.select(2).sldStyle(stdev_0_20), {},"Magnesium, extractable, stdev visualization, 0-20 cm")
        Map.addLayer(raw.select(3).sldStyle(stdev_20_50), {},"Magnesium, extractable, stdev visualization, 20-50 cm")
        converted = raw.divide(10).exp().subtract(1)
        visualization = {"min": 0, "max": 500}
        Map.setCenter(25, -3, 2)
        Map.addLayer(converted.select(0), visualization, "Magnesium, extractable, mean, 0-20 cm")

    elif cod == "ISDASOIL/Africa/v1/nitrogen_total":
        mean_0_20 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#000004" label="0-0.2" opacity="1" quantity="20"/>
        <ColorMapEntry color="#0C0927" label="0.2-0.3" opacity="1" quantity="30"/>
        <ColorMapEntry color="#231151" label="0.3-0.4" opacity="1" quantity="36"/>
        <ColorMapEntry color="#410F75" label="0.4-0.5" opacity="1" quantity="43"/>
        <ColorMapEntry color="#5F187F" label="0.5-0.6" opacity="1" quantity="48"/>
        <ColorMapEntry color="#7B2382" label="0.6-0.7" opacity="1" quantity="52"/>
        <ColorMapEntry color="#982D80" label="0.7-0.8" opacity="1" quantity="58"/>
        <ColorMapEntry color="#B63679" label="0.8-0.9" opacity="1" quantity="64"/>
        <ColorMapEntry color="#D3436E" label="0.9-1" opacity="1" quantity="67"/>
        <ColorMapEntry color="#EB5760" label="1-1.1" opacity="1" quantity="75"/>
        <ColorMapEntry color="#F8765C" label="1.1-1.2" opacity="1" quantity="79"/>
        <ColorMapEntry color="#FD9969" label="1.2-1.3" opacity="1" quantity="83"/>
        <ColorMapEntry color="#FEBA80" label="1.3-1.4" opacity="1" quantity="89"/>
        <ColorMapEntry color="#FDDC9E" label="1.4-1.5" opacity="1" quantity="93"/>
        <ColorMapEntry color="#FCFDBF" label="1.5-10" opacity="1" quantity="99"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        mean_20_50 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#000004" label="0-0.2" opacity="1" quantity="20"/>
        <ColorMapEntry color="#0C0927" label="0.2-0.3" opacity="1" quantity="30"/>
        <ColorMapEntry color="#231151" label="0.3-0.4" opacity="1" quantity="36"/>
        <ColorMapEntry color="#410F75" label="0.4-0.5" opacity="1" quantity="43"/>
        <ColorMapEntry color="#5F187F" label="0.5-0.6" opacity="1" quantity="48"/>
        <ColorMapEntry color="#7B2382" label="0.6-0.7" opacity="1" quantity="52"/>
        <ColorMapEntry color="#982D80" label="0.7-0.8" opacity="1" quantity="58"/>
        <ColorMapEntry color="#B63679" label="0.8-0.9" opacity="1" quantity="64"/>
        <ColorMapEntry color="#D3436E" label="0.9-1" opacity="1" quantity="67"/>
        <ColorMapEntry color="#EB5760" label="1-1.1" opacity="1" quantity="75"/>
        <ColorMapEntry color="#F8765C" label="1.1-1.2" opacity="1" quantity="79"/>
        <ColorMapEntry color="#FD9969" label="1.2-1.3" opacity="1" quantity="83"/>
        <ColorMapEntry color="#FEBA80" label="1.3-1.4" opacity="1" quantity="89"/>
        <ColorMapEntry color="#FDDC9E" label="1.4-1.5" opacity="1" quantity="93"/>
        <ColorMapEntry color="#FCFDBF" label="1.5-10" opacity="1" quantity="99"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        stdev_0_20 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#fde725" label="low" opacity="1" quantity="1"/>
        <ColorMapEntry color="#5dc962" label=" " opacity="1" quantity="8"/>
        <ColorMapEntry color="#20908d" label=" " opacity="1" quantity="10"/>
        <ColorMapEntry color="#3a528b" label=" " opacity="1" quantity="14"/>
        <ColorMapEntry color="#440154" label="high" opacity="1" quantity="60"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        stdev_20_50 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#fde725" label="low" opacity="1" quantity="1"/>
        <ColorMapEntry color="#5dc962" label=" " opacity="1" quantity="8"/>
        <ColorMapEntry color="#20908d" label=" " opacity="1" quantity="10"/>
        <ColorMapEntry color="#3a528b" label=" " opacity="1" quantity="14"/>
        <ColorMapEntry color="#440154" label="high" opacity="1" quantity="60"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        raw = ee.Image("ISDASOIL/Africa/v1/nitrogen_total")
        Map.addLayer(raw.select(0).sldStyle(mean_0_20), {},"Nitrogen, total, mean visualization, 0-20 cm")
        Map.addLayer(raw.select(1).sldStyle(mean_20_50), {},"Nitrogen, total, mean visualization, 20-50 cm")
        Map.addLayer(raw.select(2).sldStyle(stdev_0_20), {},"Nitrogen, total, stdev visualization, 0-20 cm")
        Map.addLayer(raw.select(3).sldStyle(stdev_20_50), {},"Nitrogen, total, stdev visualization, 20-50 cm")
        converted = raw.divide(100).exp().subtract(1)
        visualization = {"min": 0, "max": 10000}
        Map.setCenter(25, -3, 2)
        Map.addLayer(converted.select(0), visualization, "Nitrogen, total, mean, 0-20 cm")

    elif cod == "ISDASOIL/Africa/v1/ph":
        mean_0_20 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#CC0000" label="3.5-4.6" opacity="1" quantity="46"/>
        <ColorMapEntry color="#FF0000" label="4.6-4.9" opacity="1" quantity="49"/>
        <ColorMapEntry color="#FF5500" label="4.9-5.2" opacity="1" quantity="52"/>
        <ColorMapEntry color="#FFAA00" label="5.2-5.4" opacity="1" quantity="54"/>
        <ColorMapEntry color="#FFFF00" label="5.4-5.5" opacity="1" quantity="55"/>
        <ColorMapEntry color="#D4FF2B" label="5.5-5.6" opacity="1" quantity="56"/>
        <ColorMapEntry color="#AAFF55" label="5.6-5.7" opacity="1" quantity="57"/>
        <ColorMapEntry color="#80FF80" label="5.7-5.9" opacity="1" quantity="59"/>
        <ColorMapEntry color="#55FFAA" label="5.9-6" opacity="1" quantity="60"/>
        <ColorMapEntry color="#2BFFD5" label="6-6.2" opacity="1" quantity="62"/>
        <ColorMapEntry color="#00FFFF" label="6.2-6.3" opacity="1" quantity="63"/>
        <ColorMapEntry color="#00AAFF" label="6.3-6.6" opacity="1" quantity="66"/>
        <ColorMapEntry color="#0055FF" label="6.6-6.8" opacity="1" quantity="68"/>
        <ColorMapEntry color="#0000FF" label="6.8-7.1" opacity="1" quantity="71"/>
        <ColorMapEntry color="#0000CC" label="7.1-10.5" opacity="1" quantity="76"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        mean_20_50 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#CC0000" label="3.5-4.6" opacity="1" quantity="46"/>
        <ColorMapEntry color="#FF0000" label="4.6-4.9" opacity="1" quantity="49"/>
        <ColorMapEntry color="#FF5500" label="4.9-5.2" opacity="1" quantity="52"/>
        <ColorMapEntry color="#FFAA00" label="5.2-5.4" opacity="1" quantity="54"/>
        <ColorMapEntry color="#FFFF00" label="5.4-5.5" opacity="1" quantity="55"/>
        <ColorMapEntry color="#D4FF2B" label="5.5-5.6" opacity="1" quantity="56"/>
        <ColorMapEntry color="#AAFF55" label="5.6-5.7" opacity="1" quantity="57"/>
        <ColorMapEntry color="#80FF80" label="5.7-5.9" opacity="1" quantity="59"/>
        <ColorMapEntry color="#55FFAA" label="5.9-6" opacity="1" quantity="60"/>
        <ColorMapEntry color="#2BFFD5" label="6-6.2" opacity="1" quantity="62"/>
        <ColorMapEntry color="#00FFFF" label="6.2-6.3" opacity="1" quantity="63"/>
        <ColorMapEntry color="#00AAFF" label="6.3-6.6" opacity="1" quantity="66"/>
        <ColorMapEntry color="#0055FF" label="6.6-6.8" opacity="1" quantity="68"/>
        <ColorMapEntry color="#0000FF" label="6.8-7.1" opacity="1" quantity="71"/>
        <ColorMapEntry color="#0000CC" label="7.1-10.5" opacity="1" quantity="76"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        stdev_0_20 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#fde725" label="low" opacity="1" quantity="1"/>
        <ColorMapEntry color="#5dc962" label=" " opacity="1" quantity="2"/>
        <ColorMapEntry color="#20908d" label=" " opacity="1" quantity="3"/>
        <ColorMapEntry color="#3a528b" label=" " opacity="1" quantity="4"/>
        <ColorMapEntry color="#440154" label="high" opacity="1" quantity="5"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        stdev_20_50 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#fde725" label="low" opacity="1" quantity="1"/>
        <ColorMapEntry color="#5dc962" label=" " opacity="1" quantity="2"/>
        <ColorMapEntry color="#20908d" label=" " opacity="1" quantity="3"/>
        <ColorMapEntry color="#3a528b" label=" " opacity="1" quantity="4"/>
        <ColorMapEntry color="#440154" label="high" opacity="1" quantity="5"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        raw = ee.Image("ISDASOIL/Africa/v1/ph")
        Map.addLayer(raw.select(0).sldStyle(mean_0_20), {},"ph, mean visualization, 0-20 cm")
        Map.addLayer(raw.select(1).sldStyle(mean_20_50), {},"ph, mean visualization, 20-50 cm")
        Map.addLayer(raw.select(2).sldStyle(stdev_0_20), {},"ph, stdev visualization, 0-20 cm")
        Map.addLayer(raw.select(3).sldStyle(stdev_20_50), {},"ph, stdev visualization, 20-50 cm")
        converted = raw.divide(10)
        visualization = {"min": 4, "max": 8}
        Map.setCenter(25, -3, 2)
        Map.addLayer(converted.select(0), visualization, "ph, mean, 0-20 cm")

    elif cod == "ISDASOIL/Africa/v1/phosphorus_extractable":
        mean_0_20 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#0D0887" label="0-2.7" opacity="1" quantity="13"/>
        <ColorMapEntry color="#350498" label="2.7-3" opacity="1" quantity="14"/>
        <ColorMapEntry color="#5402A3" label="3-3.5" opacity="1" quantity="15"/>
        <ColorMapEntry color="#7000A8" label="3.5-4" opacity="1" quantity="16"/>
        <ColorMapEntry color="#8B0AA5" label="4-4.5" opacity="1" quantity="17"/>
        <ColorMapEntry color="#A31E9A" label="4.5-5" opacity="1" quantity="18"/>
        <ColorMapEntry color="#B93289" label="5-5.7" opacity="1" quantity="19"/>
        <ColorMapEntry color="#CC4678" label="5.7-6.4" opacity="1" quantity="20"/>
        <ColorMapEntry color="#DB5C68" label="6.4-7.2" opacity="1" quantity="21"/>
        <ColorMapEntry color="#E97158" label="7.2-8" opacity="1" quantity="22"/>
        <ColorMapEntry color="#F48849" label="8-9" opacity="1" quantity="23"/>
        <ColorMapEntry color="#FBA139" label="9-10" opacity="1" quantity="24"/>
        <ColorMapEntry color="#FEBC2A" label="10-11.2" opacity="1" quantity="25"/>
        <ColorMapEntry color="#FADA24" label="11.2-12.5" opacity="1" quantity="26"/>
        <ColorMapEntry color="#F0F921" label="12.5-125" opacity="1" quantity="27"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        mean_20_50 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#0D0887" label="0-2.7" opacity="1" quantity="13"/>
        <ColorMapEntry color="#350498" label="2.7-3" opacity="1" quantity="14"/>
        <ColorMapEntry color="#5402A3" label="3-3.5" opacity="1" quantity="15"/>
        <ColorMapEntry color="#7000A8" label="3.5-4" opacity="1" quantity="16"/>
        <ColorMapEntry color="#8B0AA5" label="4-4.5" opacity="1" quantity="17"/>
        <ColorMapEntry color="#A31E9A" label="4.5-5" opacity="1" quantity="18"/>
        <ColorMapEntry color="#B93289" label="5-5.7" opacity="1" quantity="19"/>
        <ColorMapEntry color="#CC4678" label="5.7-6.4" opacity="1" quantity="20"/>
        <ColorMapEntry color="#DB5C68" label="6.4-7.2" opacity="1" quantity="21"/>
        <ColorMapEntry color="#E97158" label="7.2-8" opacity="1" quantity="22"/>
        <ColorMapEntry color="#F48849" label="8-9" opacity="1" quantity="23"/>
        <ColorMapEntry color="#FBA139" label="9-10" opacity="1" quantity="24"/>
        <ColorMapEntry color="#FEBC2A" label="10-11.2" opacity="1" quantity="25"/>
        <ColorMapEntry color="#FADA24" label="11.2-12.5" opacity="1" quantity="26"/>
        <ColorMapEntry color="#F0F921" label="12.5-125" opacity="1" quantity="27"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        stdev_0_20 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#fde725" label="low" opacity="1" quantity="1"/>
        <ColorMapEntry color="#5dc962" label=" " opacity="1" quantity="2"/>
        <ColorMapEntry color="#20908d" label=" " opacity="1" quantity="3"/>
        <ColorMapEntry color="#3a528b" label=" " opacity="1" quantity="4"/>
        <ColorMapEntry color="#440154" label="high" opacity="1" quantity="5"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        stdev_20_50 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#fde725" label="low" opacity="1" quantity="1"/>
        <ColorMapEntry color="#5dc962" label=" " opacity="1" quantity="2"/>
        <ColorMapEntry color="#20908d" label=" " opacity="1" quantity="3"/>
        <ColorMapEntry color="#3a528b" label=" " opacity="1" quantity="4"/>
        <ColorMapEntry color="#440154" label="high" opacity="1" quantity="5"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        raw = ee.Image("ISDASOIL/Africa/v1/phosphorus_extractable")
        Map.addLayer(raw.select(0).sldStyle(mean_0_20), {},"Phosphorus extractable, mean visualization, 0-20 cm")
        Map.addLayer(raw.select(1).sldStyle(mean_20_50), {},"Phosphorus extractable, mean visualization, 20-50 cm")
        Map.addLayer(raw.select(2).sldStyle(stdev_0_20), {},"Phosphorus extractable, stdev visualization, 0-20 cm")
        Map.addLayer(raw.select(3).sldStyle(stdev_20_50), {},"Phosphorus extractable, stdev visualization, 20-50 cm")
        converted = raw.divide(10).exp().subtract(1)
        visualization = {"min": 0, "max": 15}
        Map.setCenter(25, -3, 2)
        Map.addLayer(converted.select(0), visualization, "Phosphorus extractable, mean, 0-20 cm")

    elif cod == "ISDASOIL/Africa/v1/potassium_extractable":
        mean_0_20 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#0D0887" label="0-32.1" opacity="1" quantity="35"/>
        <ColorMapEntry color="#350498" label="32.1-43.7" opacity="1" quantity="38"/>
        <ColorMapEntry color="#5402A3" label="43.7-48.4" opacity="1" quantity="39"/>
        <ColorMapEntry color="#7000A8" label="48.4-53.6" opacity="1" quantity="40"/>
        <ColorMapEntry color="#8B0AA5" label="53.6-59.3" opacity="1" quantity="41"/>
        <ColorMapEntry color="#A31E9A" label="59.3-65.7" opacity="1" quantity="42"/>
        <ColorMapEntry color="#B93289" label="65.7-72.7" opacity="1" quantity="43"/>
        <ColorMapEntry color="#CC4678" label="72.7-89" opacity="1" quantity="45"/>
        <ColorMapEntry color="#DB5C68" label="89-98.5" opacity="1" quantity="46"/>
        <ColorMapEntry color="#E97158" label="98.5-108.9" opacity="1" quantity="47"/>
        <ColorMapEntry color="#F48849" label="108.9-120.5" opacity="1" quantity="48"/>
        <ColorMapEntry color="#FBA139" label="120.5-133.3" opacity="1" quantity="49"/>
        <ColorMapEntry color="#FEBC2A" label="133.3-163" opacity="1" quantity="51"/>
        <ColorMapEntry color="#FADA24" label="163-199.3" opacity="1" quantity="53"/>
        <ColorMapEntry color="#F0F921" label="163-1200" opacity="1" quantity="55"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        mean_20_50 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#0D0887" label="0-32.1" opacity="1" quantity="35"/>
        <ColorMapEntry color="#350498" label="32.1-43.7" opacity="1" quantity="38"/>
        <ColorMapEntry color="#5402A3" label="43.7-48.4" opacity="1" quantity="39"/>
        <ColorMapEntry color="#7000A8" label="48.4-53.6" opacity="1" quantity="40"/>
        <ColorMapEntry color="#8B0AA5" label="53.6-59.3" opacity="1" quantity="41"/>
        <ColorMapEntry color="#A31E9A" label="59.3-65.7" opacity="1" quantity="42"/>
        <ColorMapEntry color="#B93289" label="65.7-72.7" opacity="1" quantity="43"/>
        <ColorMapEntry color="#CC4678" label="72.7-89" opacity="1" quantity="45"/>
        <ColorMapEntry color="#DB5C68" label="89-98.5" opacity="1" quantity="46"/>
        <ColorMapEntry color="#E97158" label="98.5-108.9" opacity="1" quantity="47"/>
        <ColorMapEntry color="#F48849" label="108.9-120.5" opacity="1" quantity="48"/>
        <ColorMapEntry color="#FBA139" label="120.5-133.3" opacity="1" quantity="49"/>
        <ColorMapEntry color="#FEBC2A" label="133.3-163" opacity="1" quantity="51"/>
        <ColorMapEntry color="#FADA24" label="163-199.3" opacity="1" quantity="53"/>
        <ColorMapEntry color="#F0F921" label="163-1200" opacity="1" quantity="55"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        stdev_0_20 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#fde725" label="low" opacity="1" quantity="1"/>
        <ColorMapEntry color="#5dc962" label=" " opacity="1" quantity="2"/>
        <ColorMapEntry color="#20908d" label=" " opacity="1" quantity="3"/>
        <ColorMapEntry color="#3a528b" label=" " opacity="1" quantity="4"/>
        <ColorMapEntry color="#440154" label="high" opacity="1" quantity="5"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        stdev_20_50 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#fde725" label="low" opacity="1" quantity="1"/>
        <ColorMapEntry color="#5dc962" label=" " opacity="1" quantity="2"/>
        <ColorMapEntry color="#20908d" label=" " opacity="1" quantity="3"/>
        <ColorMapEntry color="#3a528b" label=" " opacity="1" quantity="4"/>
        <ColorMapEntry color="#440154" label="high" opacity="1" quantity="5"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        raw = ee.Image("ISDASOIL/Africa/v1/potassium_extractable")
        Map.addLayer(raw.select(0).sldStyle(mean_0_20), {},"Potassium extractable, mean visualization, 0-20 cm")
        Map.addLayer(raw.select(1).sldStyle(mean_20_50), {},"Potassium extractable, mean visualization, 20-50 cm")
        Map.addLayer(raw.select(2).sldStyle(stdev_0_20), {},"Potassium extractable, stdev visualization, 0-20 cm")
        Map.addLayer(raw.select(3).sldStyle(stdev_20_50), {},"Potassium extractable, stdev visualization, 20-50 cm")
        converted = raw.divide(10).exp().subtract(1)
        visualization = {"min": 0, "max": 250}
        Map.setCenter(25, -3, 2)
        Map.addLayer(converted.select(0), visualization, "Potassium extractable, mean, 0-20 cm")

    elif cod == "ISDASOIL/Africa/v1/sand_content":
        mean_0_20 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#00204D" label="0-31" opacity="1" quantity="31"/>
        <ColorMapEntry color="#002D6C" label="31-39" opacity="1" quantity="39"/>
        <ColorMapEntry color="#16396D" label="39-43" opacity="1" quantity="43"/>
        <ColorMapEntry color="#36476B" label="43-46" opacity="1" quantity="46"/>
        <ColorMapEntry color="#4B546C" label="46-49" opacity="1" quantity="49"/>
        <ColorMapEntry color="#5C616E" label="49-52" opacity="1" quantity="52"/>
        <ColorMapEntry color="#6C6E72" label="52-54" opacity="1" quantity="54"/>
        <ColorMapEntry color="#7C7B78" label="54-56" opacity="1" quantity="56"/>
        <ColorMapEntry color="#8E8A79" label="56-58" opacity="1" quantity="58"/>
        <ColorMapEntry color="#A09877" label="58-60" opacity="1" quantity="60"/>
        <ColorMapEntry color="#B3A772" label="60-63" opacity="1" quantity="63"/>
        <ColorMapEntry color="#C6B66B" label="63-65" opacity="1" quantity="65"/>
        <ColorMapEntry color="#DBC761" label="65-68" opacity="1" quantity="68"/>
        <ColorMapEntry color="#F0D852" label="68-71" opacity="1" quantity="71"/>
        <ColorMapEntry color="#FFEA46" label="71-100" opacity="1" quantity="75"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        mean_20_50 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#00204D" label="0-31" opacity="1" quantity="31"/>
        <ColorMapEntry color="#002D6C" label="31-39" opacity="1" quantity="39"/>
        <ColorMapEntry color="#16396D" label="39-43" opacity="1" quantity="43"/>
        <ColorMapEntry color="#36476B" label="43-46" opacity="1" quantity="46"/>
        <ColorMapEntry color="#4B546C" label="46-49" opacity="1" quantity="49"/>
        <ColorMapEntry color="#5C616E" label="49-52" opacity="1" quantity="52"/>
        <ColorMapEntry color="#6C6E72" label="52-54" opacity="1" quantity="54"/>
        <ColorMapEntry color="#7C7B78" label="54-56" opacity="1" quantity="56"/>
        <ColorMapEntry color="#8E8A79" label="56-58" opacity="1" quantity="58"/>
        <ColorMapEntry color="#A09877" label="58-60" opacity="1" quantity="60"/>
        <ColorMapEntry color="#B3A772" label="60-63" opacity="1" quantity="63"/>
        <ColorMapEntry color="#C6B66B" label="63-65" opacity="1" quantity="65"/>
        <ColorMapEntry color="#DBC761" label="65-68" opacity="1" quantity="68"/>
        <ColorMapEntry color="#F0D852" label="68-71" opacity="1" quantity="71"/>
        <ColorMapEntry color="#FFEA46" label="71-100" opacity="1" quantity="75"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        stdev_0_20 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#fde725" label="low" opacity="1" quantity="2"/>
        <ColorMapEntry color="#5dc962" label=" " opacity="1" quantity="3"/>
        <ColorMapEntry color="#20908d" label=" " opacity="1" quantity="4"/>
        <ColorMapEntry color="#3a528b" label=" " opacity="1" quantity="6"/>
        <ColorMapEntry color="#440154" label="high" opacity="1" quantity="7"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        stdev_20_50 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#fde725" label="low" opacity="1" quantity="2"/>
        <ColorMapEntry color="#5dc962" label=" " opacity="1" quantity="3"/>
        <ColorMapEntry color="#20908d" label=" " opacity="1" quantity="4"/>
        <ColorMapEntry color="#3a528b" label=" " opacity="1" quantity="6"/>
        <ColorMapEntry color="#440154" label="high" opacity="1" quantity="7"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        raw = ee.Image("ISDASOIL/Africa/v1/sand_content")
        Map.addLayer(raw.select(0).sldStyle(mean_0_20), {},"Sand content, mean visualization, 0-20 cm")
        Map.addLayer(raw.select(1).sldStyle(mean_20_50), {},"Sand content, mean visualization, 20-50 cm")
        Map.addLayer(raw.select(2).sldStyle(stdev_0_20), {},"Sand content, stdev visualization, 0-20 cm")
        Map.addLayer(raw.select(3).sldStyle(stdev_20_50), {},"Sand content, stdev visualization, 20-50 cm")
        converted = raw.divide(10).exp().subtract(1)
        visualization = {"min": 0, "max": 3000}
        Map.setCenter(25, -3, 2)
        Map.addLayer(converted.select(0), visualization, "Sand content, mean, 0-20 cm")

    elif cod == "ISDASOIL/Africa/v1/silt_content":
        mean_0_20 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#00204D" label="0-7" opacity="1" quantity="7"/>
        <ColorMapEntry color="#002D6C" label="7-9" opacity="1" quantity="9"/>
        <ColorMapEntry color="#16396D" label="9-10" opacity="1" quantity="10"/>
        <ColorMapEntry color="#36476B" label="10-11" opacity="1" quantity="11"/>
        <ColorMapEntry color="#4B546C" label="11-12" opacity="1" quantity="12"/>
        <ColorMapEntry color="#5C616E" label="12-13" opacity="1" quantity="13"/>
        <ColorMapEntry color="#6C6E72" label="13-14" opacity="1" quantity="14"/>
        <ColorMapEntry color="#7C7B78" label="14-15" opacity="1" quantity="15"/>
        <ColorMapEntry color="#8E8A79" label="15-16" opacity="1" quantity="16"/>
        <ColorMapEntry color="#A09877" label="16-17" opacity="1" quantity="17"/>
        <ColorMapEntry color="#B3A772" label="17-18" opacity="1" quantity="18"/>
        <ColorMapEntry color="#C6B66B" label="18-19" opacity="1" quantity="19"/>
        <ColorMapEntry color="#DBC761" label="19-20" opacity="1" quantity="20"/>
        <ColorMapEntry color="#F0D852" label="20-22" opacity="1" quantity="22"/>
        <ColorMapEntry color="#FFEA46" label="22-70" opacity="1" quantity="24"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        mean_20_50 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#00204D" label="0-7" opacity="1" quantity="7"/>
        <ColorMapEntry color="#002D6C" label="7-9" opacity="1" quantity="9"/>
        <ColorMapEntry color="#16396D" label="9-10" opacity="1" quantity="10"/>
        <ColorMapEntry color="#36476B" label="10-11" opacity="1" quantity="11"/>
        <ColorMapEntry color="#4B546C" label="11-12" opacity="1" quantity="12"/>
        <ColorMapEntry color="#5C616E" label="12-13" opacity="1" quantity="13"/>
        <ColorMapEntry color="#6C6E72" label="13-14" opacity="1" quantity="14"/>
        <ColorMapEntry color="#7C7B78" label="14-15" opacity="1" quantity="15"/>
        <ColorMapEntry color="#8E8A79" label="15-16" opacity="1" quantity="16"/>
        <ColorMapEntry color="#A09877" label="16-17" opacity="1" quantity="17"/>
        <ColorMapEntry color="#B3A772" label="17-18" opacity="1" quantity="18"/>
        <ColorMapEntry color="#C6B66B" label="18-19" opacity="1" quantity="19"/>
        <ColorMapEntry color="#DBC761" label="19-20" opacity="1" quantity="20"/>
        <ColorMapEntry color="#F0D852" label="20-22" opacity="1" quantity="22"/>
        <ColorMapEntry color="#FFEA46" label="22-70" opacity="1" quantity="24"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        stdev_0_20 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#fde725" label="low" opacity="1" quantity="1"/>
        <ColorMapEntry color="#5dc962" label=" " opacity="1" quantity="2"/>
        <ColorMapEntry color="#20908d" label=" " opacity="1" quantity="3"/>
        <ColorMapEntry color="#3a528b" label=" " opacity="1" quantity="4"/>
        <ColorMapEntry color="#440154" label="high" opacity="1" quantity="4.19000000000005"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        stdev_20_50 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#fde725" label="low" opacity="1" quantity="1"/>
        <ColorMapEntry color="#5dc962" label=" " opacity="1" quantity="2"/>
        <ColorMapEntry color="#20908d" label=" " opacity="1" quantity="3"/>
        <ColorMapEntry color="#3a528b" label=" " opacity="1" quantity="4"/>
        <ColorMapEntry color="#440154" label="high" opacity="1" quantity="4.19000000000005"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        raw = ee.Image("ISDASOIL/Africa/v1/silt_content")
        Map.addLayer(raw.select(0).sldStyle(mean_0_20), {},"Silt content, mean visualization, 0-20 cm")
        Map.addLayer(raw.select(1).sldStyle(mean_20_50), {},"Silt content, mean visualization, 20-50 cm")
        Map.addLayer(raw.select(2).sldStyle(stdev_0_20), {},"Silt content, stdev visualization, 0-20 cm")
        Map.addLayer(raw.select(3).sldStyle(stdev_20_50), {},"Silt content, stdev visualization, 20-50 cm")
        converted = raw.divide(10).exp().subtract(1)
        visualization = {"min": 0, "max": 15}
        Map.setCenter(25, -3, 2)
        Map.addLayer(converted.select(0), visualization, "Silt content, mean, 0-20 cm")

    elif cod == "ISDASOIL/Africa/v1/stone_content":
        mean_0_20 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#00204D" label="0-0.1" opacity="1" quantity="1"/>
        <ColorMapEntry color="#002D6C" label="0.1-0.3" opacity="1" quantity="3"/>
        <ColorMapEntry color="#16396D" label="0.3-0.5" opacity="1" quantity="4"/>
        <ColorMapEntry color="#36476B" label="0.5-0.6" opacity="1" quantity="5"/>
        <ColorMapEntry color="#4B546C" label="0.6-0.8" opacity="1" quantity="6"/>
        <ColorMapEntry color="#5C616E" label="0.8-1" opacity="1" quantity="7"/>
        <ColorMapEntry color="#6C6E72" label="1-1.2" opacity="1" quantity="8"/>
        <ColorMapEntry color="#7C7B78" label="1.2-1.5" opacity="1" quantity="9"/>
        <ColorMapEntry color="#8E8A79" label="1.5-1.7" opacity="1" quantity="10"/>
        <ColorMapEntry color="#A09877" label="1.7-2" opacity="1" quantity="11"/>
        <ColorMapEntry color="#B3A772" label="2-2.3" opacity="1" quantity="12"/>
        <ColorMapEntry color="#C6B66B" label="2.3-2.7" opacity="1" quantity="13"/>
        <ColorMapEntry color="#DBC761" label="2.7-3.1" opacity="1" quantity="14"/>
        <ColorMapEntry color="#F0D852" label="3.1-3.5" opacity="1" quantity="15"/>
        <ColorMapEntry color="#FFEA46" label="3.5-80" opacity="1" quantity="16"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        mean_20_50 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#00204D" label="0-0.1" opacity="1" quantity="1"/>
        <ColorMapEntry color="#002D6C" label="0.1-0.3" opacity="1" quantity="3"/>
        <ColorMapEntry color="#16396D" label="0.3-0.5" opacity="1" quantity="4"/>
        <ColorMapEntry color="#36476B" label="0.5-0.6" opacity="1" quantity="5"/>
        <ColorMapEntry color="#4B546C" label="0.6-0.8" opacity="1" quantity="6"/>
        <ColorMapEntry color="#5C616E" label="0.8-1" opacity="1" quantity="7"/>
        <ColorMapEntry color="#6C6E72" label="1-1.2" opacity="1" quantity="8"/>
        <ColorMapEntry color="#7C7B78" label="1.2-1.5" opacity="1" quantity="9"/>
        <ColorMapEntry color="#8E8A79" label="1.5-1.7" opacity="1" quantity="10"/>
        <ColorMapEntry color="#A09877" label="1.7-2" opacity="1" quantity="11"/>
        <ColorMapEntry color="#B3A772" label="2-2.3" opacity="1" quantity="12"/>
        <ColorMapEntry color="#C6B66B" label="2.3-2.7" opacity="1" quantity="13"/>
        <ColorMapEntry color="#DBC761" label="2.7-3.1" opacity="1" quantity="14"/>
        <ColorMapEntry color="#F0D852" label="3.1-3.5" opacity="1" quantity="15"/>
        <ColorMapEntry color="#FFEA46" label="3.5-80" opacity="1" quantity="16"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        stdev_0_20 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#fde725" label="low" opacity="1" quantity="1"/>
        <ColorMapEntry color="#5dc962" label=" " opacity="1" quantity="2"/>
        <ColorMapEntry color="#20908d" label=" " opacity="1" quantity="3"/>
        <ColorMapEntry color="#3a528b" label=" " opacity="1" quantity="4"/>
        <ColorMapEntry color="#440154" label="high" opacity="1" quantity="5"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        stdev_20_50 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#fde725" label="low" opacity="1" quantity="1"/>
        <ColorMapEntry color="#5dc962" label=" " opacity="1" quantity="2"/>
        <ColorMapEntry color="#20908d" label=" " opacity="1" quantity="3"/>
        <ColorMapEntry color="#3a528b" label=" " opacity="1" quantity="4"/>
        <ColorMapEntry color="#440154" label="high" opacity="1" quantity="5"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        raw = ee.Image("ISDASOIL/Africa/v1/stone_content")
        Map.addLayer(raw.select(0).sldStyle(mean_0_20), {},"Stone content, mean visualization, 0-20 cm")
        Map.addLayer(raw.select(1).sldStyle(mean_20_50), {},"Stone content, mean visualization, 20-50 cm")
        Map.addLayer(raw.select(2).sldStyle(stdev_0_20), {},"Stone content, stdev visualization, 0-20 cm")
        Map.addLayer(raw.select(3).sldStyle(stdev_20_50), {},"Stone content, stdev visualization, 20-50 cm")
        converted = raw.divide(10).exp().subtract(1)
        visualization = {"min": 0, "max": 6}
        Map.setCenter(25, -3, 2)
        Map.addLayer(converted.select(0), visualization, "Stone content, mean, 0-20 cm")

    elif cod == "ISDASOIL/Africa/v1/sulphur_extractable":
        mean_0_20 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#0D0887" label="0-2.3" opacity="1" quantity="12"/>
        <ColorMapEntry color="#350498" label="2.3-3.1" opacity="1" quantity="14"/>
        <ColorMapEntry color="#5402A3" label="3.1-3.5" opacity="1" quantity="15"/>
        <ColorMapEntry color="#7000A8" label="3.5-4" opacity="1" quantity="16"/>
        <ColorMapEntry color="#8B0AA5" label="4-5" opacity="1" quantity="18"/>
        <ColorMapEntry color="#A31E9A" label="5-5.7" opacity="1" quantity="19"/>
        <ColorMapEntry color="#B93289" label="5.7-6.4" opacity="1" quantity="20"/>
        <ColorMapEntry color="#CC4678" label="6.4-7.2" opacity="1" quantity="21"/>
        <ColorMapEntry color="#DB5C68" label="7.2-8" opacity="1" quantity="22"/>
        <ColorMapEntry color="#E97158" label="8-9" opacity="1" quantity="23"/>
        <ColorMapEntry color="#F48849" label="9-10" opacity="1" quantity="24"/>
        <ColorMapEntry color="#FBA139" label="10-11.2" opacity="1" quantity="25"/>
        <ColorMapEntry color="#FEBC2A" label="11.2-12.5" opacity="1" quantity="26"/>
        <ColorMapEntry color="#FADA24" label="12.5-15.4" opacity="1" quantity="28"/>
        <ColorMapEntry color="#F0F921" label="15.4-125" opacity="1" quantity="30"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        mean_20_50 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#0D0887" label="0-2.3" opacity="1" quantity="12"/>
        <ColorMapEntry color="#350498" label="2.3-3.1" opacity="1" quantity="14"/>
        <ColorMapEntry color="#5402A3" label="3.1-3.5" opacity="1" quantity="15"/>
        <ColorMapEntry color="#7000A8" label="3.5-4" opacity="1" quantity="16"/>
        <ColorMapEntry color="#8B0AA5" label="4-5" opacity="1" quantity="18"/>
        <ColorMapEntry color="#A31E9A" label="5-5.7" opacity="1" quantity="19"/>
        <ColorMapEntry color="#B93289" label="5.7-6.4" opacity="1" quantity="20"/>
        <ColorMapEntry color="#CC4678" label="6.4-7.2" opacity="1" quantity="21"/>
        <ColorMapEntry color="#DB5C68" label="7.2-8" opacity="1" quantity="22"/>
        <ColorMapEntry color="#E97158" label="8-9" opacity="1" quantity="23"/>
        <ColorMapEntry color="#F48849" label="9-10" opacity="1" quantity="24"/>
        <ColorMapEntry color="#FBA139" label="10-11.2" opacity="1" quantity="25"/>
        <ColorMapEntry color="#FEBC2A" label="11.2-12.5" opacity="1" quantity="26"/>
        <ColorMapEntry color="#FADA24" label="12.5-15.4" opacity="1" quantity="28"/>
        <ColorMapEntry color="#F0F921" label="15.4-125" opacity="1" quantity="30"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        stdev_0_20 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#fde725" label="low" opacity="1" quantity="1"/>
        <ColorMapEntry color="#5dc962" label=" " opacity="1" quantity="3"/>
        <ColorMapEntry color="#20908d" label=" " opacity="1" quantity="4"/>
        <ColorMapEntry color="#3a528b" label=" " opacity="1" quantity="6"/>
        <ColorMapEntry color="#440154" label="high" opacity="1" quantity="14"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        stdev_20_50 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#fde725" label="low" opacity="1" quantity="1"/>
        <ColorMapEntry color="#5dc962" label=" " opacity="1" quantity="3"/>
        <ColorMapEntry color="#20908d" label=" " opacity="1" quantity="4"/>
        <ColorMapEntry color="#3a528b" label=" " opacity="1" quantity="6"/>
        <ColorMapEntry color="#440154" label="high" opacity="1" quantity="14"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        raw = ee.Image("ISDASOIL/Africa/v1/sulphur_extractable")
        Map.addLayer(raw.select(0).sldStyle(mean_0_20), {},"Sulphur extractable, mean visualization, 0-20 cm")
        Map.addLayer(raw.select(1).sldStyle(mean_20_50), {},"Sulphur extractable, mean visualization, 20-50 cm")
        Map.addLayer(raw.select(2).sldStyle(stdev_0_20), {},"Sulphur extractable, stdev visualization, 0-20 cm")
        Map.addLayer(raw.select(3).sldStyle(stdev_20_50), {},"Sulphur extractable, stdev visualization, 20-50 cm")
        converted = raw.divide(10).exp().subtract(1)
        visualization = {"min": 0, "max": 20}
        Map.setCenter(25, -3, 2)
        Map.addLayer(converted.select(0), visualization, "Sulphur extractable, mean, 0-20 cm")



    elif cod == "ISDASOIL/Africa/v1/texture_class":
        raw = ee.Image("ISDASOIL/Africa/v1/texture_class")
        Map.addLayer(raw.select(0), {}, "Texture class, 0-20 cm")
        Map.addLayer(raw.select(1), {}, "Texture class, 20-50 cm")
        Map.setCenter(25, -3, 2)

    elif cod == "ISDASOIL/Africa/v1/zinc_extractable":
        mean_0_20 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#0D0887" label="0-0.6" opacity="1" quantity="5"/>
        <ColorMapEntry color="#350498" label="0.6-0.8" opacity="1" quantity="6"/>
        <ColorMapEntry color="#5402A3" label="0.8-1" opacity="1" quantity="7"/>
        <ColorMapEntry color="#7000A8" label="1-1.2" opacity="1" quantity="8"/>
        <ColorMapEntry color="#8B0AA5" label="1.2-1.5" opacity="1" quantity="9"/>
        <ColorMapEntry color="#A31E9A" label="1.5-1.7" opacity="1" quantity="10"/>
        <ColorMapEntry color="#B93289" label="1.7-2" opacity="1" quantity="11"/>
        <ColorMapEntry color="#CC4678" label="2-2.3" opacity="1" quantity="12"/>
        <ColorMapEntry color="#DB5C68" label="2.3-2.7" opacity="1" quantity="13"/>
        <ColorMapEntry color="#E97158" label="2.7-3.1" opacity="1" quantity="14"/>
        <ColorMapEntry color="#F48849" label="3.1-3.5" opacity="1" quantity="15"/>
        <ColorMapEntry color="#FBA139" label="3.5-4" opacity="1" quantity="16"/>
        <ColorMapEntry color="#FEBC2A" label="4-4.5" opacity="1" quantity="17"/>
        <ColorMapEntry color="#FADA24" label="4.5-5" opacity="1" quantity="18"/>
        <ColorMapEntry color="#F0F921" label="5-125" opacity="1" quantity="19"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        mean_20_50 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#0D0887" label="0-0.6" opacity="1" quantity="5"/>
        <ColorMapEntry color="#350498" label="0.6-0.8" opacity="1" quantity="6"/>
        <ColorMapEntry color="#5402A3" label="0.8-1" opacity="1" quantity="7"/>
        <ColorMapEntry color="#7000A8" label="1-1.2" opacity="1" quantity="8"/>
        <ColorMapEntry color="#8B0AA5" label="1.2-1.5" opacity="1" quantity="9"/>
        <ColorMapEntry color="#A31E9A" label="1.5-1.7" opacity="1" quantity="10"/>
        <ColorMapEntry color="#B93289" label="1.7-2" opacity="1" quantity="11"/>
        <ColorMapEntry color="#CC4678" label="2-2.3" opacity="1" quantity="12"/>
        <ColorMapEntry color="#DB5C68" label="2.3-2.7" opacity="1" quantity="13"/>
        <ColorMapEntry color="#E97158" label="2.7-3.1" opacity="1" quantity="14"/>
        <ColorMapEntry color="#F48849" label="3.1-3.5" opacity="1" quantity="15"/>
        <ColorMapEntry color="#FBA139" label="3.5-4" opacity="1" quantity="16"/>
        <ColorMapEntry color="#FEBC2A" label="4-4.5" opacity="1" quantity="17"/>
        <ColorMapEntry color="#FADA24" label="4.5-5" opacity="1" quantity="18"/>
        <ColorMapEntry color="#F0F921" label="5-125" opacity="1" quantity="19"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        stdev_0_20 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#fde725" label="low" opacity="1" quantity="1"/>
        <ColorMapEntry color="#5dc962" label=" " opacity="1" quantity="2"/>
        <ColorMapEntry color="#20908d" label=" " opacity="1" quantity="3"/>
        <ColorMapEntry color="#3a528b" label=" " opacity="1" quantity="4"/>
        <ColorMapEntry color="#440154" label="high" opacity="1" quantity="5"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        stdev_20_50 = """
        <RasterSymbolizer>
        <ColorMap type="ramp">
        <ColorMapEntry color="#fde725" label="low" opacity="1" quantity="1"/>
        <ColorMapEntry color="#5dc962" label=" " opacity="1" quantity="2"/>
        <ColorMapEntry color="#20908d" label=" " opacity="1" quantity="3"/>
        <ColorMapEntry color="#3a528b" label=" " opacity="1" quantity="4"/>
        <ColorMapEntry color="#440154" label="high" opacity="1" quantity="5"/>
        </ColorMap>
        <ContrastEnhancement/>
        </RasterSymbolizer> """
        raw = ee.Image("ISDASOIL/Africa/v1/zinc_extractable")
        Map.addLayer(raw.select(0).sldStyle(mean_0_20), {},"Zinc, extractable, mean visualization, 0-20 cm")
        Map.addLayer(raw.select(1).sldStyle(mean_20_50), {},"Zinc, extractable, mean visualization, 20-50 cm")
        Map.addLayer(raw.select(2).sldStyle(stdev_0_20), {},"Zinc, extractable, stdev visualization, 0-20 cm")
        Map.addLayer(raw.select(3).sldStyle(stdev_20_50), {},"Zinc, extractable, stdev visualization, 20-50 cm")
        converted = raw.divide(10).exp().subtract(1)
        visualization = {"min": 0, "max": 10}
        Map.setCenter(25, -3, 2)
        Map.addLayer(converted.select(0), visualization, "Zinc, extractable, mean, 0-20 cm")
        
    elif cod == "JAXA/ALOS/AVNIR-2/ORI":
        dataset = ee.ImageCollection("JAXA/ALOS/AVNIR-2/ORI").filter(ee.Filter.date("2011-01-01", "2011-04-01"))
        avnir2OriRgb = dataset.select(["B3", "B2", "B1"])
        avnir2OriRgbVis = {
        "min": 0.0,
        "max": 255.0,
        }
        Map.setCenter(138.7302, 35.3641, 12)
        Map.addLayer(avnir2OriRgb, avnir2OriRgbVis, "AVNIR-2 ORI RGB")

    elif cod == "JAXA/ALOS/AW3D30/V3_2":
        dataset = ee.ImageCollection("JAXA/ALOS/AW3D30/V3_2")
        elevation = dataset.select("DSM")
        elevationVis = {
        "min": 0,
        "max": 5000,
        "palette": ["0000ff", "00ffff", "ffff00", "ff0000", "ffffff"]
        }
        Map.setCenter(138.73, 35.36, 11)
        Map.addLayer(elevation, elevationVis, "Elevation")
        proj = elevation.first().select(0).projection()
        slopeReprojected = ee.Terrain.slope(elevation.mosaic().setDefaultProjection(proj))
        Map.addLayer(slopeReprojected, {"min": 0, "max": 45}, "Slope")

    elif cod == "JAXA/ALOS/PALSAR-2/Level2_2/ScanSAR":
        collection = ee.ImageCollection("JAXA/ALOS/PALSAR-2/Level2_2/ScanSAR").filterBounds(ee.Geometry.Point(143, -5))
        image = collection.first()
        Map.addLayer(image.select(["HH"]), {"min": 0, "max": 8000}, "HH polarization")
        Map.centerObject(image)

    elif cod =="JAXA/ALOS/PALSAR/YEARLY/FNF":
        dataset = ee.ImageCollection("JAXA/ALOS/PALSAR/YEARLY/FNF").filterDate("2017-01-01", "2017-12-31")
        forestNonForest = dataset.select("fnf")
        forestNonForestVis = {
        "min": 1.0,
        "max": 3.0,
        "palette": ["006400", "FEFF99", "0000FF"],
        }
        Map.setCenter(136.85, 37.37, 4)
        Map.addLayer(forestNonForest, forestNonForestVis, "Forest/Non-Forest")

    elif cod == "JAXA/ALOS/PALSAR/YEARLY/FNF4":
        dataset = ee.ImageCollection("JAXA/ALOS/PALSAR/YEARLY/FNF4").filterDate("2018-01-01", "2018-12-31")
        forestNonForest = dataset.select("fnf")
        forestNonForestVis = {
        "min": 1.0,
        "max": 4.0,
        "palette": ["00B200","83EF62","FFFF99","0000FF"],
        }
        Map.setCenter(136.85, 37.37, 4)
        Map.addLayer(forestNonForest, forestNonForestVis, "Forest/Non-Forest")

    elif cod == "JAXA/ALOS/PALSAR/YEARLY/SAR":
        dataset = ee.ImageCollection("JAXA/ALOS/PALSAR/YEARLY/SAR").filter(ee.Filter.date("2017-01-01", "2018-01-01"))
        sarHh = dataset.select("HH")
        sarHhVis = {
        "min": 0.0,
        "max": 10000.0,
        }
        Map.setCenter(136.85, 37.37, 4)
        Map.addLayer(sarHh, sarHhVis, "SAR HH")

    elif cod == "JAXA/ALOS/PALSAR/YEARLY/SAR_EPOCH":
        dataset = ee.ImageCollection("JAXA/ALOS/PALSAR/YEARLY/SAR_EPOCH").filter(ee.Filter.date("2017-01-01", "2018-01-01"))
        sarHh = dataset.select("HH")
        sarHhVis = {
        "min": 0.0,
        "max": 10000.0,
        }
        Map.setCenter(136.85, 37.37, 4)
        Map.addLayer(sarHh, sarHhVis, "SAR HH")

    elif cod == "JAXA/GCOM-C/L3/LAND/LAI/V1":
        dataset = ee.ImageCollection("JAXA/GCOM-C/L3/LAND/LAI/V1").filterDate("2020-01-01", "2020-02-01").filter(ee.Filter.eq("SATELLITE_DIRECTION", "D"))
        dataset = dataset.mean().multiply(0.001)
        visualization = {
        "bands": ["LAI_AVE"],
        "min": -7,
        "max": 7,
        "palette": [
        "040274","040281","0502a3","0502b8","0502ce","0502e6",
        "0602ff","235cb1","307ef3","269db1","30c8e2","32d3ef",
        "3be285","3ff38f","86e26f","3ae237","b5e22e","d6e21f",
        "fff705","ffd611","ffb613","ff8b13","ff6e08","ff500d",
        "ff0000","de0101","c21301","a71001","911003",
        ]
        }
        Map.setCenter(128.45, 33.33, 5)
        Map.addLayer(dataset, visualization, "Leaf Area Index")

    elif cod == "JAXA/GCOM-C/L3/LAND/LAI/V2":
        dataset = ee.ImageCollection("JAXA/GCOM-C/L3/LAND/LAI/V2").filterDate("2020-01-01", "2020-02-01").filter(ee.Filter.eq("SATELLITE_DIRECTION", "D"))
        dataset = dataset.mean().multiply(0.001)
        visualization = {
        "bands": ["LAI_AVE"],
        "min": -7,
        "max": 7,
        "palette": [
        "040274","040281","0502a3","0502b8","0502ce","0502e6",
        "0602ff","235cb1","307ef3","269db1","30c8e2","32d3ef",
        "3be285","3ff38f","86e26f","3ae237","b5e22e","d6e21f",
        "fff705","ffd611","ffb613","ff8b13","ff6e08","ff500d",
        "ff0000","de0101","c21301","a71001","911003",
        ]
        }
        Map.setCenter(128.45, 33.33, 5)
        Map.addLayer(dataset, visualization, "Leaf Area Index")

    elif cod == "JAXA/GCOM-C/L3/LAND/LAI/V3":
        dataset = ee.ImageCollection("JAXA/GCOM-C/L3/LAND/LAI/V3").filterDate("2021-12-01", "2022-01-01").filter(ee.Filter.eq("SATELLITE_DIRECTION", "D"))
        dataset = dataset.mean().multiply(0.001)
        visualization = {
        "bands": ["LAI_AVE"],
        "min": -7,
        "max": 7,
        "palette": [
        "040274","040281","0502a3","0502b8","0502ce","0502e6",
        "0602ff","235cb1","307ef3","269db1","30c8e2","32d3ef",
        "3be285","3ff38f","86e26f","3ae237","b5e22e","d6e21f",
        "fff705","ffd611","ffb613","ff8b13","ff6e08","ff500d",
        "ff0000","de0101","c21301","a71001","911003",
        ]
        }
        Map.setCenter(128.45, 33.33, 5)
        Map.addLayer(dataset, visualization, "Leaf Area Index")

    elif cod == "JAXA/GCOM-C/L3/LAND/LST/V1":
        dataset = ee.ImageCollection("JAXA/GCOM-C/L3/LAND/LST/V1").filterDate("2020-01-01", "2020-02-01").filter(ee.Filter.eq("SATELLITE_DIRECTION", "D"))
        dataset = dataset.mean().multiply(0.02)
        visualization = {
        "bands": ["LST_AVE"],
        "min": 250,
        "max": 316,
        "palette": [
        "040274","040281","0502a3","0502b8","0502ce","0502e6",
        "0602ff","235cb1","307ef3","269db1","30c8e2","32d3ef",
        "3be285","3ff38f","86e26f","3ae237","b5e22e","d6e21f",
        "fff705","ffd611","ffb613","ff8b13","ff6e08","ff500d",
        "ff0000","de0101","c21301","a71001","911003",
        ]
        }
        Map.setCenter(128.45, 33.33, 5)
        Map.addLayer(dataset, visualization, "Land Surface Temperature")

    elif cod == "JAXA/GCOM-C/L3/LAND/LST/V2":
        dataset = ee.ImageCollection("JAXA/GCOM-C/L3/LAND/LST/V2").filterDate("2020-01-01", "2020-02-01").filter(ee.Filter.eq("SATELLITE_DIRECTION", "D"))
        dataset = dataset.mean().multiply(0.02)
        visualization = {
        "bands": ["LST_AVE"],
        "min": 250,
        "max": 316,
        "palette": [
        "040274","040281","0502a3","0502b8","0502ce","0502e6",
        "0602ff","235cb1","307ef3","269db1","30c8e2","32d3ef",
        "3be285","3ff38f","86e26f","3ae237","b5e22e","d6e21f",
        "fff705","ffd611","ffb613","ff8b13","ff6e08","ff500d",
        "ff0000","de0101","c21301","a71001","911003",
        ]
        }
        Map.setCenter(128.45, 33.33, 5)
        Map.addLayer(dataset, visualization, "Land Surface Temperature")

    elif cod == "JAXA/GCOM-C/L3/LAND/LST/V3":
        dataset = ee.ImageCollection("JAXA/GCOM-C/L3/LAND/LST/V3").filterDate("2021-12-01", "2022-01-01").filter(ee.Filter.eq("SATELLITE_DIRECTION", "D"))
        dataset = dataset.mean().multiply(0.02)
        visualization = {
        "bands": ["LST_AVE"],
        "min": 250,
        "max": 316,
        "palette": [
        "040274","040281","0502a3","0502b8","0502ce","0502e6",
        "0602ff","235cb1","307ef3","269db1","30c8e2","32d3ef",
        "3be285","3ff38f","86e26f","3ae237","b5e22e","d6e21f",
        "fff705","ffd611","ffb613","ff8b13","ff6e08","ff500d",
        "ff0000","de0101","c21301","a71001","911003",
        ]
        }
        Map.setCenter(128.45, 33.33, 5)
        Map.addLayer(dataset, visualization, "Land Surface Temperature")

    elif cod == "JAXA/GCOM-C/L3/OCEAN/CHLA/V1":
        dataset = ee.ImageCollection("JAXA/GCOM-C/L3/OCEAN/CHLA/V1").filterDate("2020-01-01", "2020-02-01").filter(ee.Filter.eq("SATELLITE_DIRECTION", "D"))
        image = dataset.mean().multiply(0.0016).log10()
        vis = {
        "bands": ["CHLA_AVE"],
        "min": -2,
        "max": 2,
        "palette": [
        "3500a8","0800ba","003fd6",
        "00aca9","77f800","ff8800",
        "b30000","920000","880000"
        ]
        }
        Map.addLayer(image, vis, "Chlorophyll-a concentration")
        Map.setCenter(128.45, 33.33, 5)

    elif cod == "JAXA/GCOM-C/L3/OCEAN/CHLA/V2":
        dataset = ee.ImageCollection("JAXA/GCOM-C/L3/OCEAN/CHLA/V2").filterDate("2020-01-01", "2020-02-01").filter(ee.Filter.eq("SATELLITE_DIRECTION", "D"))
        image = dataset.mean().multiply(0.0016).log10()
        vis = {
        "bands": ["CHLA_AVE"],
        "min": -2,
        "max": 2,
        "palette": [
        "3500a8","0800ba","003fd6",
        "00aca9","77f800","ff8800",
        "b30000","920000","880000"
        ]
        }
        Map.addLayer(image, vis, "Chlorophyll-a concentration")
        Map.setCenter(128.45, 33.33, 5)

    elif cod == "JAXA/GCOM-C/L3/OCEAN/CHLA/V3":
        dataset = ee.ImageCollection("JAXA/GCOM-C/L3/OCEAN/CHLA/V3").filterDate("2021-12-01", "2022-01-01").filter(ee.Filter.eq("SATELLITE_DIRECTION", "D"))
        image = dataset.mean().multiply(0.0016).log10()
        vis = {
        "bands": ["CHLA_AVE"],
        "min": -2,
        "max": 2,
        "palette": [
        "3500a8","0800ba","003fd6",
        "00aca9","77f800","ff8800",
        "b30000","920000","880000"
        ]
        }
        Map.addLayer(image, vis, "Chlorophyll-a concentration")
        Map.setCenter(128.45, 33.33, 5)

    elif cod == "JAXA/GCOM-C/L3/OCEAN/SST/V1":
        dataset = ee.ImageCollection("JAXA/GCOM-C/L3/OCEAN/SST/V1").filterDate("2020-01-01", "2020-02-01").filter(ee.Filter.eq("SATELLITE_DIRECTION", "D"))
        dataset = dataset.mean().multiply(0.0012).add(-10)
        vis = {
        "bands": ["SST_AVE"],
        "min": 0,
        "max": 30,
        "palette": ["000000", "005aff", "43c8c8", "fff700", "ff0000"],
        }
        Map.setCenter(128.45, 33.33, 5)
        Map.addLayer(dataset, vis, "Sea Surface Temperature")

    elif cod == "JAXA/GCOM-C/L3/OCEAN/SST/V2":
        dataset = ee.ImageCollection("JAXA/GCOM-C/L3/OCEAN/SST/V2").filterDate("2020-01-01", "2020-02-01").filter(ee.Filter.eq("SATELLITE_DIRECTION", "D"))
        dataset = dataset.mean().multiply(0.0012).add(-10)
        vis = {
        "bands": ["SST_AVE"],
        "min": 0,
        "max": 30,
        "palette": ["000000", "005aff", "43c8c8", "fff700", "ff0000"],
        }
        Map.setCenter(128.45, 33.33, 5)
        Map.addLayer(dataset, vis, "Sea Surface Temperature")

    elif cod == "JAXA/GCOM-C/L3/OCEAN/SST/V3":
        dataset = ee.ImageCollection("JAXA/GCOM-C/L3/OCEAN/SST/V3").filterDate("2021-12-01", "2022-01-01").filter(ee.Filter.eq("SATELLITE_DIRECTION", "D"))
        dataset = dataset.mean().multiply(0.0012).add(-10)
        vis = {
        "bands": ["SST_AVE"],
        "min": 0,
        "max": 30,
        "palette": ["000000", "005aff", "43c8c8", "fff700", "ff0000"],
        }
        Map.setCenter(128.45, 33.33, 5)
        Map.addLayer(dataset, vis, "Sea Surface Temperature")

    elif cod == "JAXA/GPM_L3/GSMaP/v6/operational":
        dataset = ee.ImageCollection("JAXA/GPM_L3/GSMaP/v6/operational").filter(ee.Filter.date("2018-08-06", "2018-08-07"))
        precipitation = dataset.select("hourlyPrecipRate")
        precipitationVis = {
        "min": 0.0,
        "max": 30.0,
        "palette":
        ["1621a2", "ffffff", "03ffff", "13ff03", "efff00", "ffb103", "ff2300"],
        }
        Map.setCenter(-90.7, 26.12, 2)
        Map.addLayer(precipitation, precipitationVis, "Precipitation")

    elif cod == "JAXA/GPM_L3/GSMaP/v6/reanalysis":
        dataset = ee.ImageCollection("JAXA/GPM_L3/GSMaP/v6/reanalysis").filter(ee.Filter.date("2014-02-01", "2014-02-02"))
        precipitation = dataset.select("hourlyPrecipRate")
        precipitationVis = {
        "min": 0.0,
        "max": 30.0,
        "palette":
        ["1621a2", "ffffff", "03ffff", "13ff03", "efff00", "ffb103", "ff2300"],
        }
        Map.setCenter(-90.7, 26.12, 2)
        Map.addLayer(precipitation, precipitationVis, "Precipitation")

    elif cod == "JCU/Murray/GIC/global_tidal_wetland_change/2019":
        dataset = ee.Image("JCU/Murray/GIC/global_tidal_wetland_change/2019")
        Map.setCenter(103.7, 1.3, 12)
        Map.setOptions("SATELLITE")
        plasma = [
        "0d0887", "3d049b", "6903a5", "8d0fa1", "ae2891", "cb4679", "df6363",
        "f0844c", "faa638", "fbcc27", "f0f921"
        ]
        Map.addLayer(dataset.select("twprobabilityStart"), {"palette": plasma, "min": 0, "max": 100},"twprobabilityStart", False, 1)
        Map.addLayer(dataset.select("twprobabilityEnd"), {"palette": plasma, "min": 0, "max": 100},"twprobabilityEnd", False, 1)
        lossPalette = ["FE4A49"]
        gainPalette = ["2AB7CA"]
        Map.addLayer(dataset.select("loss"), {"palette": lossPalette, "min": 1, "max": 1},"Tidal wetland loss", True, 1)
        Map.addLayer(dataset.select("gain"), {"palette": gainPalette, "min": 1, "max": 1},"Tidal wetland gain", True, 1)
        viridis = ["440154", "414487", "2a788e", "22a884", "7ad151", "fde725"]
        Map.addLayer(dataset.select("lossYear"), {"palette": viridis, "min": 4, "max": 19},"Year of loss", False, 0.9)
        Map.addLayer(dataset.select("gainYear"), {"palette": viridis, "min": 4, "max": 19},"Year of gain", False, 0.9)
        classPalette = ["9e9d9d", "ededed", "FF9900", "009966", "960000", "006699"]
        classNames = ["None", "None", "Tidal flat", "Mangrove", "None", "Tidal marsh"]
        Map.addLayer(dataset.select("lossType"), {"palette": classPalette, "min": 0, "max": 5}, "Loss type", False, 0.9)
        Map.addLayer(dataset.select("gainType"), {"palette": classPalette, "min": 0, "max": 5}, "Gain type", False, 0.9)

    elif cod == "JRC/D5/EUCROPMAP/V1":
        image = ee.Image("JRC/D5/EUCROPMAP/V1/2018")
        Map.addLayer(image, {}, "EUCROPMAP 2018")
        Map.setCenter(10, 48, 4)

    elif cod == "JRC/GHSL/P2016/BUILT_LDSMT_GLOBE_V1":
        dataset = ee.Image("JRC/GHSL/P2016/BUILT_LDSMT_GLOBE_V1")
        builtUpMultitemporal = dataset.select("built")
        visParams = {
        "min": 1.0,
        "max": 6.0,
        "palette": ["0c1d60", "000000", "448564", "70daa4", "83ffbf", "ffffff"],
        }
        Map.setCenter(8.9957, 45.5718, 12)
        Map.addLayer(builtUpMultitemporal, visParams, "Built-Up Multitemporal")

    elif cod == "JRC/GHSL/P2016/POP_GPW_GLOBE_V1":
        dataset = ee.ImageCollection("JRC/GHSL/P2016/POP_GPW_GLOBE_V1").filter(ee.Filter.date("2015-01-01", "2015-12-31"))
        populationCount = dataset.select("population_count")
        populationCountVis = {
        "min": 0.0,
        "max": 200.0,
        "palette": ["060606", "337663", "337663", "ffffff"],
        }
        Map.setCenter(78.22, 22.59, 3)
        Map.addLayer(populationCount, populationCountVis, "Population Count")

    elif cod == "JRC/GHSL/P2016/SMOD_POP_GLOBE_V1":
        dataset = ee.ImageCollection("JRC/GHSL/P2016/SMOD_POP_GLOBE_V1").filter(ee.Filter.date("2015-01-01", "2015-12-31"))
        degreeOfUrbanization = dataset.select("smod_code")
        visParams = {
        "min": 0.0,
        "max": 3.0,
        "palette": ["000000", "448564", "70daa4", "ffffff"],
        }
        Map.setCenter(114.96, 31.13, 4)
        Map.addLayer(degreeOfUrbanization, visParams, "Degree of Urbanization")

    elif cod == "JRC/GSW1_4/GlobalSurfaceWater":
        dataset = ee.Image("JRC/GSW1_4/GlobalSurfaceWater")
        visualization = {
        "bands": ["occurrence"],
        "min": 0.0,
        "max": 100.0,
        "palette": ["ffffff", "ffbbbb", "0000ff"]
        }
        Map.setCenter(59.414, 45.182, 6)
        Map.addLayer(dataset, visualization, "Occurrence")

    elif cod == "JRC/GSW1_4/Metadata":
        dataset = ee.Image("JRC/GSW1_4/Metadata")
        visualization = {
        "bands": ["detections", "valid_obs", "total_obs"],
        "min": 100.0,
        "max": 900.0,
        }
        Map.setCenter(71.72, 52.48, 0)
        Map.addLayer(dataset, visualization, "Detections/Observations")

    elif cod == "JRC/GSW1_4/MonthlyHistory":
        dataset = ee.Image("JRC/GSW1_4/MonthlyHistory/2020_06")
        visualization = {
        "bands": ["water"],
        "min": 0.0,
        "max": 2.0,
        "palette": ["ffffff", "fffcb8", "0905ff"]
        }
        Map.setCenter(-121.234, 38.109, 7)
        Map.addLayer(dataset, visualization, "Water")

    elif cod == "JRC/GSW1_4/MonthlyRecurrence":
        dataset = ee.ImageCollection("JRC/GSW1_4/MonthlyRecurrence")
        visualization = {
        "bands": ["monthly_recurrence"],
        "min": 0.0,
        "max": 100.0,
        "palette": ["ffffff", "ffbbbb", "0000ff"]
        }
        Map.setCenter(-51.482, -0.835, 6)
        Map.addLayer(dataset, visualization, "Monthly Recurrence")

    elif cod == "JRC/GSW1_4/YearlyHistory":
        dataset = ee.ImageCollection("JRC/GSW1_4/YearlyHistory")
        visualization = {
        "bands": ["waterClass"],
        "min": 0.0,
        "max": 3.0,
        "palette": ["cccccc", "ffffff", "99d9ea", "0000ff"]
        }
        Map.setCenter(59.414, 45.182, 7)
        Map.addLayer(dataset, visualization, "Water Class")

    elif cod == "JRC/GWIS/GlobFire/v2/DailyPerimeters":
        folder = "JRC/GWIS/GlobFire/v2/DailyPerimeters"
        def printAssetList(listAssetsOutput):
            print("Asset list:", listAssetsOutput["assets"])
            ee.data.listAssets(folder, {}, printAssetList)

        tableName = "JRC/GWIS/GlobFire/v2/DailyPerimeters/2020"
        computeArea = lambda f: f.set({"area": f.area()})
        
        features = ee.FeatureCollection(tableName).map(computeArea)
        visParams = {
        "palette": ["f5ff64", "b5ffb4", "beeaff", "ffc0e8", "8e8dff", "adadad"],
        "min": 0.0,
        "max": 600000000.0,
        "opacity": 0.8,
        }
        image = ee.Image().float().paint(features, "area")
        Map.addLayer(image, visParams, "GlobFire 2020")
        Map.addLayer(features, None, "For Inspector", False)
        Map.setCenter(-121.23, 39.7, 12)

    elif cod == "JRC/GWIS/GlobFire/v2/FinalPerimeters":
        dataset = ee.FeatureCollection("JRC/GWIS/GlobFire/v2/FinalPerimeters")
        visParams = {
        "palette": ["f5ff64", "b5ffb4", "beeaff", "ffc0e8", "8e8dff", "adadad"],
        "min": 0.0,
        "max": 600000000.0,
        "opacity": 0.8,
        }
        image = ee.Image().float().paint(dataset, "area")
        Map.addLayer(image, visParams, "GlobFire Final")
        Map.addLayer(dataset, None, "for Inspector", False)
        Map.setCenter(-122.121, 38.56, 12)

    elif cod == "JRC/LUCAS_HARMO/COPERNICUS_POLYGONS/V1/2018":
        dataset = ee.FeatureCollection("JRC/LUCAS_HARMO/COPERNICUS_POLYGONS/V1/2018")
        visParams = {
        "min": 35,
        "max": 60
        }
        dataset2 = dataset.map(lambda f: ee.Feature(f.buffer(5000)))
        image = ee.Image().float().paint(dataset2, "gps_lat").randomVisualizer()
        Map.addLayer(ee.Image(1), {"min":0, "max":1}, "background")
        Map.addLayer(image, visParams, "LUCAS Polygons")
        Map.addLayer(dataset, None, "for Inspector", False)
        Map.setCenter(19.514, 51.82, 8)

    elif cod == "JRC/LUCAS_HARMO/THLOC/V1":
        dataset = ee.FeatureCollection("JRC/LUCAS_HARMO/THLOC/V1")
        Map.addLayer(dataset, {}, "LUCAS Points (data)", False)
        dataset = dataset.style({
        "color": "489734",
        "pointSize": 3
        })
        Map.setCenter(-3.8233, 40.609, 10)
        Map.addLayer(dataset, {}, "LUCAS Points (styled green)")

    elif cod == "KNTU/LiDARLab/IranLandCover/V1":
        dataset = ee.Image("KNTU/LiDARLab/IranLandCover/V1")
        visualization = {
        "bands": ["classification"]
        }
        Map.setCenter(54.0, 33.0, 5)
        Map.addLayer(dataset, visualization, "Classification")

    elif cod == "LANDFIRE/Fire/FRG/v1_2_0":
        dataset = ee.ImageCollection("LANDFIRE/Fire/FRG/v1_2_0")
        visualization = {
        "bands": ["FRG"]
        }
        Map.setCenter(-121.671, 40.699, 5)
        Map.addLayer(dataset, visualization, "FRG")

    elif cod == "LANDFIRE/Fire/MFRI/v1_2_0":
        dataset = ee.ImageCollection("LANDFIRE/Fire/MFRI/v1_2_0")
        visualization = {
        "bands": ["MFRI"]
        }
        Map.setCenter(-121.671, 40.699, 5)
        Map.addLayer(dataset, visualization, "MFRI")

    elif cod == "LANDFIRE/Fire/PLS/v1_2_0":
        dataset = ee.ImageCollection("LANDFIRE/Fire/PLS/v1_2_0")
        visualization = {
        "bands": ["PLS"]
        }
        Map.setCenter(-121.671, 40.699, 5)
        Map.addLayer(dataset, visualization, "PLS")

    elif cod == "LANDFIRE/Fire/PMS/v1_2_0":
        dataset = ee.ImageCollection("LANDFIRE/Fire/PMS/v1_2_0")
        visualization = {
        "bands": ["PMS"]
        }
        Map.setCenter(-121.671, 40.699, 5)
        Map.addLayer(dataset, visualization, "PMS")

    elif cod == "LANDFIRE/Fire/PRS/v1_2_0":
        dataset = ee.ImageCollection("LANDFIRE/Fire/PRS/v1_2_0")
        visualization = {
        "bands": ["PRS"]
        }
        Map.setCenter(-121.671, 40.699, 5)
        Map.addLayer(dataset, visualization, "PRS")

    elif cod == "LANDFIRE/Fire/SClass/v1_4_0":
        dataset = ee.ImageCollection("LANDFIRE/Fire/SClass/v1_4_0")
        visualization = {
        "bands": ["SClass"]
        }
        Map.setCenter(-121.671, 40.699, 5)
        Map.addLayer(dataset, visualization, "SClass")

    elif cod == "LANDFIRE/Fire/VCC/v1_4_0":
        dataset = ee.ImageCollection("LANDFIRE/Fire/VCC/v1_4_0")
        visualization = {
        "bands": ["VCC"]
        }
        Map.setCenter(-121.671, 40.699, 5)
        Map.addLayer(dataset, visualization, "VCC")

    elif cod == "LANDFIRE/Fire/VDep/v1_4_0":
        dataset = ee.ImageCollection("LANDFIRE/Fire/VDep/v1_4_0")
        visualization = {
        "bands": ["VDep"]
        }
        Map.setCenter(-121.671, 40.699, 5)
        Map.addLayer(dataset, visualization, "VDep")

    elif cod == "LANDFIRE/Vegetation/BPS/v1_4_0":
        dataset = ee.ImageCollection("LANDFIRE/Vegetation/BPS/v1_4_0")
        visualization = {
            "bands": ["BPS"]
        }
        Map.setCenter(-121.671, 40.699, 5)
        Map.addLayer(dataset, visualization, "BPS")

    elif cod == "LANDFIRE/Vegetation/ESP/v1_2_0/AK":
        dataset = ee.Image("LANDFIRE/Vegetation/ESP/v1_2_0/AK")
        visualization = {
            "bands": ["ESP"]
        }
        Map.setCenter(-151.011, 63.427, 8)
        Map.addLayer(dataset, visualization, "ESP")

    elif cod == "LANDFIRE/Vegetation/ESP/v1_2_0/CONUS":
        dataset = ee.Image("LANDFIRE/Vegetation/ESP/v1_2_0/CONUS")
        visualization = {
            "bands": ["ESP"]
        }
        Map.setCenter(-121.671, 40.699, 5)
        Map.addLayer(dataset, visualization, "ESP")

    elif cod == "LANDFIRE/Vegetation/ESP/v1_2_0/HI":
        dataset = ee.Image("LANDFIRE/Vegetation/ESP/v1_2_0/HI")
        visualization = {
            "bands": ["ESP"]
        }
        Map.setCenter(-155.3, 19.627, 8)
        Map.addLayer(dataset, visualization, "ESP")

    elif cod == "LANDFIRE/Vegetation/EVC/v1_4_0":
        dataset = ee.ImageCollection("LANDFIRE/Vegetation/EVC/v1_4_0")
        visualization = {
            "bands": ["EVC"]
        }
        Map.setCenter(-121.671, 40.699, 5)
        Map.addLayer(dataset, visualization, "EVC")

    elif cod == "LANDFIRE/Vegetation/EVH/v1_4_0":
        dataset = ee.ImageCollection("LANDFIRE/Vegetation/EVH/v1_4_0")
        visualization = {
            "bands": ["EVH"]
        }
        Map.setCenter(-121.671, 40.699, 5)
        Map.addLayer(dataset, visualization, "EVH")

    elif cod == "LANDFIRE/Vegetation/EVT/v1_4_0":
        dataset = ee.ImageCollection("LANDFIRE/Vegetation/EVT/v1_4_0")
        visualization = {
            "bands": ["EVT"]
        }
        Map.setCenter(-121.671, 40.699, 5)
        Map.addLayer(dataset, visualization, "EVT")

    elif cod == "LANDSAT/GLS1975":
        dataset = ee.ImageCollection("LANDSAT/GLS1975")
        FalseColor = dataset.select(["30", "20", "10"])
        FalseColorVis = {
            "gamma": 1.6
        }
        Map.setCenter(44.517, 25.998, 5)
        Map.addLayer(FalseColor, FalseColorVis, "False Color")

    elif cod == "LANDSAT/GLS2005":
        dataset = ee.ImageCollection("LANDSAT/GLS2005")
        trueColor321 = dataset.select(["30", "20", "10"])
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(trueColor321, {}, "True Color (321)")

    elif cod == "LANDSAT/GLS2005_L5":
        dataset = ee.ImageCollection("LANDSAT/GLS2005_L5")
        trueColor321 = dataset.select(["30", "20", "10"])
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(trueColor321, {}, "True Color (321)")

    elif cod == "LANDSAT/GLS2005_L7":
        dataset = ee.ImageCollection("LANDSAT/GLS2005_L7")
        trueColor321 = dataset.select(["30", "20", "10"])
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(trueColor321, {}, "True Color (321)")

    elif cod == "LANDSAT/LC08/C02/T1":
        dataset = ee.ImageCollection("LANDSAT/LC08/C02/T1").filterDate("2017-01-01", "2017-12-31")
        trueColor432 = dataset.select(["B4", "B3", "B2"])
        trueColor432Vis = {
        "min": 0.0,
        "max": 30000.0
        }
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(trueColor432, trueColor432Vis, "True Color (432)")

    elif cod == "LANDSAT/LC08/C02/T1_L2":
        dataset = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2").filterDate("2021-05-01", "2021-06-01")
        def applyScaleFactors(image):
            opticalBands = image.select("SR_B.").multiply(0.0000275).add(-0.2)
            thermalBands = image.select("ST_B.*").multiply(0.00341802).add(149.0)
            return image.addBands(opticalBands, None, True).addBands(thermalBands, None, True)
        dataset = dataset.map(applyScaleFactors)
        visualization = {
        "bands": ["SR_B4", "SR_B3", "SR_B2"],
        "min": 0.0,
        "max": 0.3
        }
        Map.setCenter(-114.2579, 38.9275, 8)
        Map.addLayer(dataset, visualization, "True Color (432)")

    elif cod == "LANDSAT/LC08/C02/T1_RT":
        dataset = ee.ImageCollection("LANDSAT/LC08/C02/T1_RT").filterDate("2017-01-01", "2017-12-31")
        trueColor432 = dataset.select(["B4", "B3", "B2"])
        trueColor432Vis = {
        "min": 0.0,
        "max": 30000.0
        }
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(trueColor432, trueColor432Vis, "True Color (432)")

    elif cod == "LANDSAT/LC08/C02/T1_RT_TOA":
        dataset = ee.ImageCollection("LANDSAT/LC08/C02/T1_RT_TOA").filterDate("2017-01-01", "2017-12-31")
        trueColor432 = dataset.select(["B4", "B3", "B2"])
        trueColor432Vis = {
            "min": 0.0,
            "max": 0.4
            }
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(trueColor432, trueColor432Vis, "True Color (432)")

    elif cod == "LANDSAT/LC08/C02/T1_TOA":
        dataset = ee.ImageCollection("LANDSAT/LC08/C02/T1_TOA").filterDate("2017-01-01", "2017-12-31")
        trueColor432 = dataset.select(["B4", "B3", "B2"])
        trueColor432Vis = {
            "min": 0.0,
            "max": 0.4}
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(trueColor432, trueColor432Vis, "True Color (432)")

    elif cod == "LANDSAT/LC08/C02/T2":
        dataset = ee.ImageCollection("LANDSAT/LC08/C02/T2").filterDate("2017-01-01", "2017-12-31")
        trueColor432 = dataset.select(["B4", "B3", "B2"])
        trueColor432Vis = {
            "min": 0.0,
            "max": 30000.0
            }
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(trueColor432, trueColor432Vis, "True Color (432)")

    elif cod == "LANDSAT/LC08/C02/T2_L2":
        dataset = ee.ImageCollection("LANDSAT/LC08/C02/T2_L2").filterDate("2021-05-01", "2021-06-01")
        def applyScaleFactors(image):
            opticalBands = image.select("SR_B.").multiply(0.0000275).add(-0.2)
            thermalBands = image.select("ST_B.*").multiply(0.00341802).add(149.0)
            return image.addBands(opticalBands, None, True) .addBands(thermalBands, None, True)
        dataset = dataset.map(applyScaleFactors)
        visualization = {
            "bands": ["SR_B4", "SR_B3", "SR_B2"],
            "min": 0.0,
            "max": 0.3
        }
        Map.setCenter(-83, 24, 8)
        Map.addLayer(dataset, visualization, "True Color (432)")

    elif cod == "LANDSAT/LC08/C02/T2_TOA":
        dataset = ee.ImageCollection("LANDSAT/LC08/C02/T2_TOA").filterDate("2017-01-01", "2017-12-31")
        trueColor432 = dataset.select(["B4", "B3", "B2"])
        trueColor432Vis = {
            "min": 0.0,
            "max": 0.4
        }
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(trueColor432, trueColor432Vis, "True Color (432)")

    elif cod == "LANDSAT/LC09/C02/T1":
        dataset = ee.ImageCollection("LANDSAT/LC09/C02/T1").filterDate("2022-01-01", "2022-02-01")
        trueColor432 = dataset.select(["B4", "B3", "B2"])
        trueColor432Vis = {
            "min": 0.0,
            "max": 30000.0
            }
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(trueColor432, trueColor432Vis, "True Color (432)")

    elif cod == "LANDSAT/LC09/C02/T1_L2":
        dataset = ee.ImageCollection("LANDSAT/LC09/C02/T1_L2").filterDate("2022-01-01", "2022-02-01")
        def applyScaleFactors(image):
            opticalBands = image.select("SR_B.").multiply(0.0000275).add(-0.2)
            thermalBands = image.select("ST_B.*").multiply(0.00341802).add(149.0)
            return image.addBands(opticalBands, None, True).addBands(thermalBands, None, True)
        dataset = dataset.map(applyScaleFactors)
        visualization = {
            "bands": ["SR_B4", "SR_B3", "SR_B2"],
            "min": 0.0,
            "max": 0.3
        }
        Map.setCenter(-114.2579, 38.9275, 8)
        Map.addLayer(dataset, visualization, "True Color (432)")

    elif cod == "LANDSAT/LC09/C02/T1_TOA":
        dataset = ee.ImageCollection("LANDSAT/LC09/C02/T1_TOA").filterDate("2022-01-01", "2022-02-01")
        trueColor432 = dataset.select(["B4", "B3", "B2"])
        trueColor432Vis = {
            "min": 0.0,
            "max": 0.4}
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(trueColor432, trueColor432Vis, "True Color (432)")

    elif cod == "LANDSAT/LC09/C02/T2":
        dataset = ee.ImageCollection("LANDSAT/LC09/C02/T2").filterDate("2022-01-01", "2022-02-01")
        trueColor432 = dataset.select(["B4", "B3", "B2"])
        trueColor432Vis = {
            "min": 0.0,
            "max": 30000.0}
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(trueColor432, trueColor432Vis, "True Color (432)")

    elif cod == "LANDSAT/LC09/C02/T2_L2":
        dataset = ee.ImageCollection("LANDSAT/LC09/C02/T2_L2").filterDate("2022-01-01", "2022-02-01")
        def applyScaleFactors(image):
            opticalBands = image.select("SR_B.").multiply(0.0000275).add(-0.2)
            thermalBands = image.select("ST_B.*").multiply(0.00341802).add(149.0)
            return image.addBands(opticalBands, None, True).addBands(thermalBands, None, True)
        dataset = dataset.map(applyScaleFactors)
        visualization = {
            "bands": ["SR_B4", "SR_B3", "SR_B2"],
            "min": 0.0,
            "max": 0.3}
        Map.setCenter(-83, 24, 8)
        Map.addLayer(dataset, visualization, "True Color (432)")

    elif cod == "LANDSAT/LC09/C02/T2_TOA":
        dataset = ee.ImageCollection("LANDSAT/LC09/C02/T2_TOA").filterDate("2022-01-01", "2022-02-01")
        trueColor432 = dataset.select(["B4", "B3", "B2"])
        trueColor432Vis = {
            "min": 0.0,
            "max": 0.4}
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(trueColor432, trueColor432Vis, "True Color (432)")

    elif cod == "LANDSAT/LE07/C02/T1":
        dataset = ee.ImageCollection("LANDSAT/LE07/C02/T1").filterDate("1999-01-01", "2002-12-31")
        trueColor321 = dataset.select(["B3", "B2", "B1"])
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(trueColor321, {}, "True Color (321)")

    elif cod == "LANDSAT/LE07/C02/T1_L2":
        dataset = ee.ImageCollection("LANDSAT/LE07/C02/T1_L2").filterDate("2017-06-01", "2017-07-01")
        def applyScaleFactors(image):
            opticalBands = image.select("SR_B.").multiply(0.0000275).add(-0.2)
            thermalBand = image.select("ST_B6").multiply(0.00341802).add(149.0)
            return image.addBands(opticalBands, None, True).addBands(thermalBand, None, True)
        dataset = dataset.map(applyScaleFactors)
        visualization = {
            "bands": ["SR_B3", "SR_B2", "SR_B1"],
            "min": 0.0,
            "max": 0.3}
        Map.setCenter(-114.2579, 38.9275, 8)
        Map.addLayer(dataset, visualization, "True Color (321)")

    elif cod == "LANDSAT/LE07/C02/T1_RT":
        dataset = ee.ImageCollection("LANDSAT/LE07/C02/T1_RT").filterDate("1999-01-01", "2002-12-31")
        trueColor321 = dataset.select(["B3", "B2", "B1"])
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(trueColor321, {}, "True Color (321)")

    elif cod == "LANDSAT/LE07/C02/T1_RT_TOA":
        dataset = ee.ImageCollection("LANDSAT/LE07/C02/T1_RT_TOA").filterDate("1999-01-01", "2002-12-31")
        trueColor321 = dataset.select(["B3", "B2", "B1"])
        trueColor321Vis = {
            "min": 0.0,
            "max": 0.4,
            "gamma": 1.2}
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(trueColor321, trueColor321Vis, "True Color (321)")

    elif cod == "LANDSAT/LE07/C02/T1_TOA":
        dataset = ee.ImageCollection("LANDSAT/LE07/C02/T1_TOA").filterDate("1999-01-01", "2002-12-31")
        trueColor321 = dataset.select(["B3", "B2", "B1"])
        trueColor321Vis = {
            "min": 0.0,
            "max": 0.4,
            "gamma": 1.2}
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(trueColor321, trueColor321Vis, "True Color (321)")

    elif cod == "LANDSAT/LE07/C02/T2":
        dataset = ee.ImageCollection("LANDSAT/LE07/C02/T2").filterDate("1999-01-01", "2002-12-31")
        trueColor321 = dataset.select(["B3", "B2", "B1"])
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(trueColor321, {}, "True Color (321)")

    elif cod == "LANDSAT/LE07/C02/T2_L2":
        dataset = ee.ImageCollection("LANDSAT/LE07/C02/T2_L2").filterDate("2017-06-01", "2017-07-01")
        def applyScaleFactors(image):
            opticalBands = image.select("SR_B.").multiply(0.0000275).add(-0.2)
            thermalBand = image.select("ST_B6").multiply(0.00341802).add(149.0)
            return image.addBands(opticalBands, None, True).addBands(thermalBand, None, True)
        dataset = dataset.map(applyScaleFactors)
        visualization = {
            "bands": ["SR_B3", "SR_B2", "SR_B1"],
            "min": 0.0,
            "max": 0.3}
        Map.setCenter(-83, 24, 8)
        Map.addLayer(dataset, visualization, "True Color (321)")

    elif cod == "LANDSAT/LE07/C02/T2_TOA":
        dataset = ee.ImageCollection("LANDSAT/LE07/C02/T2_TOA").filterDate("1999-01-01", "2002-12-31")
        trueColor321 = dataset.select(["B3", "B2", "B1"])
        trueColor321Vis = {
            "min": 0.0,
            "max": 0.4,
            "gamma": 1.2}
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(trueColor321, trueColor321Vis, "True Color (321)")

    elif cod == "LANDSAT/LM01/C02/T1":
        dataset = ee.ImageCollection("LANDSAT/LM01/C02/T1").filterDate("1974-01-01", "1978-12-31")
        nearInfrared321 = dataset.select(["B6", "B5", "B4"])
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(nearInfrared321, {}, "Near Infrared (321)")

    elif cod == "LANDSAT/LM01/C02/T2":
        dataset = ee.ImageCollection("LANDSAT/LM01/C02/T2").filterDate("1974-01-01", "1978-12-31")
        nearInfrared321 = dataset.select(["B6", "B5", "B4"])
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(nearInfrared321, {}, "Near Infrared (321)")

    elif cod == "LANDSAT/LM02/C02/T1":
        dataset = ee.ImageCollection("LANDSAT/LM02/C02/T1").filterDate("1978-01-01", "1980-12-31")
        nearInfrared321 = dataset.select(["B6", "B5", "B4"])
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(nearInfrared321, {}, "Near Infrared (321)")

    elif cod == "LANDSAT/LM02/C02/T2":
        dataset = ee.ImageCollection("LANDSAT/LM02/C02/T2").filterDate("1978-01-01", "1980-12-31")
        nearInfrared321 = dataset.select(["B6", "B5", "B4"])
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(nearInfrared321, {}, "Near Infrared (321)")

    elif cod == "LANDSAT/LM03/C02/T1":
        dataset = ee.ImageCollection("LANDSAT/LM03/C02/T1").filterDate("1978-01-01", "1980-12-31")
        nearInfrared321 = dataset.select(["B6", "B5", "B4"])
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(nearInfrared321, {}, "Near Infrared (321)")

    elif cod == "LANDSAT/LM03/C02/T2":
        dataset = ee.ImageCollection("LANDSAT/LM03/C02/T2").filterDate("1978-01-01", "1980-12-31")
        nearInfrared321 = dataset.select(["B6", "B5", "B4"])
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(nearInfrared321, {}, "Near Infrared (321)")

    elif cod == "LANDSAT/LM04/C02/T1":
        dataset = ee.ImageCollection("LANDSAT/LM04/C02/T1").filterDate("1989-01-01", "1992-12-31")
        nearInfrared321 = dataset.select(["B3", "B2", "B1"])
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(nearInfrared321, {}, "Near Infrared (321)")

    elif cod == "LANDSAT/LM04/C02/T2":
        dataset = ee.ImageCollection("LANDSAT/LM04/C02/T2").filterDate("1989-01-01", "1992-12-31")
        nearInfrared321 = dataset.select(["B3", "B2", "B1"])
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(nearInfrared321, {}, "Near Infrared (321)")

    elif cod == "LANDSAT/LM05/C02/T1":
        dataset = ee.ImageCollection("LANDSAT/LM05/C02/T1").filterDate("1985-01-01", "1989-12-31")
        nearInfrared321 = dataset.select(["B3", "B2", "B1"])
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(nearInfrared321, {}, "Near Infrared (321)")

    elif cod == "LANDSAT/LM05/C02/T2":
        dataset = ee.ImageCollection("LANDSAT/LM05/C02/T2").filterDate("1985-01-01", "1989-12-31")
        nearInfrared321 = dataset.select(["B3", "B2", "B1"])
        nearInfrared321Vis = {}
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(nearInfrared321, nearInfrared321Vis, "Near Infrared (321)")

    elif cod == "LANDSAT/LT04/C02/T1":
        dataset = ee.ImageCollection("LANDSAT/LT04/C02/T1").filterDate("1989-01-01", "1992-12-31")
        trueColor321 = dataset.select(["B3", "B2", "B1"])
        trueColor321Vis = {}
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(trueColor321, trueColor321Vis, "True Color (321)")

    elif cod == "LANDSAT/LT04/C02/T1_L2":
        dataset = ee.ImageCollection("LANDSAT/LT04/C02/T1_L2").filterDate("1990-04-01", "1990-05-01")
        def applyScaleFactors(image):
                     opticalBands = image.select("SR_B.").multiply(0.0000275).add(-0.2)
                     thermalBand = image.select("ST_B6").multiply(0.00341802).add(149.0)
                     return image.addBands(opticalBands, None, True).addBands(thermalBand, None, True)
        dataset = dataset.map(applyScaleFactors)
        visualization = {
        "bands": ["SR_B3", "SR_B2", "SR_B1"],
        "min": 0.0,
        "max": 0.3,
        }
        Map.setCenter(15, 53, 8)
        Map.addLayer(dataset, visualization, "True Color (321)")

    elif cod == "LANDSAT/LT04/C02/T1_TOA":
        dataset = ee.ImageCollection("LANDSAT/LT04/C02/T1_TOA").filterDate("1989-01-01", "1992-12-31")
        trueColor321 = dataset.select(["B3", "B2", "B1"])
        trueColor321Vis = {
        "min": 0.0,
        "max": 0.4,
        "gamma": 1.2,
        }
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(trueColor321, trueColor321Vis, "True Color (321)")

    elif cod == "LANDSAT/LT04/C02/T2":
        dataset = ee.ImageCollection("LANDSAT/LT04/C02/T2").filterDate("1989-01-01", "1992-12-31")
        trueColor321 = dataset.select(["B3", "B2", "B1"])
        trueColor321Vis = {}
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(trueColor321, trueColor321Vis, "True Color (321)")

    elif cod == "LANDSAT/LT04/C02/T2_L2":
        dataset = ee.ImageCollection("LANDSAT/LT04/C02/T2_L2").filterDate("1990-04-01", "1990-05-01")
        def applyScaleFactors(image):
                     opticalBands = image.select("SR_B.").multiply(0.0000275).add(-0.2)
                     thermalBand = image.select("ST_B6").multiply(0.00341802).add(149.0)
                     return image.addBands(opticalBands, None, True).addBands(thermalBand, None, True)
        dataset = dataset.map(applyScaleFactors)
        visualization = {
        "bands": ["SR_B3", "SR_B2", "SR_B1"],
        "min": 0.0,
        "max": 0.3,
        }
        Map.setCenter(-83, 24, 8)
        Map.addLayer(dataset, visualization, "True Color (321)")

    elif cod == "LANDSAT/LT04/C02/T2_TOA":
        dataset = ee.ImageCollection("LANDSAT/LT04/C02/T2_TOA").filterDate("1989-01-01", "1992-12-31")
        trueColor321 = dataset.select(["B3", "B2", "B1"])
        trueColor321Vis = {
        "min": 0.0,
        "max": 0.4,
        "gamma": 1.2,
        }
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(trueColor321, trueColor321Vis, "True Color (321)")

    elif cod == "LANDSAT/LT05/C02/T1":
        dataset = ee.ImageCollection("LANDSAT/LT05/C02/T1").filterDate("2011-01-01", "2011-12-31")
        trueColor321 = dataset.select(["B3", "B2", "B1"])
        trueColor321Vis = {}
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(trueColor321, trueColor321Vis, "True Color (321)")

    elif cod == "LANDSAT/LT05/C02/T1_L2":
        dataset = ee.ImageCollection("LANDSAT/LT05/C02/T1_L2").filterDate("2000-06-01", "2000-07-01")
        def applyScaleFactors(image):
                     opticalBands = image.select("SR_B.").multiply(0.0000275).add(-0.2)
                     thermalBand = image.select("ST_B6").multiply(0.00341802).add(149.0)
                     return image.addBands(opticalBands, None, True).addBands(thermalBand, None, True)
        dataset = dataset.map(applyScaleFactors)
        visualization = {
        "bands": ["SR_B3", "SR_B2", "SR_B1"],
        "min": 0.0,
        "max": 0.3,
        }
        Map.setCenter(-114.2579, 38.9275, 8)
        Map.addLayer(dataset, visualization, "True Color (321)")

    elif cod == "LANDSAT/LT05/C02/T1_TOA":
        dataset = ee.ImageCollection("LANDSAT/LT05/C02/T1_TOA").filterDate("2011-01-01", "2011-12-31")
        trueColor321 = dataset.select(["B3", "B2", "B1"])
        trueColor321Vis = {
        "min": 0.0,
        "max": 0.4,
        "gamma": 1.2,
        }
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(trueColor321, trueColor321Vis, "True Color (321)")

    elif cod == "LANDSAT/LT05/C02/T2":
        dataset = ee.ImageCollection("LANDSAT/LT05/C02/T2").filterDate("2011-01-01", "2011-12-31")
        trueColor321 = dataset.select(["B3", "B2", "B1"])
        trueColor321Vis = {}
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(trueColor321, trueColor321Vis, "True Color (321)")

    elif cod == "LANDSAT/LT05/C02/T2_L2":
        dataset = ee.ImageCollection("LANDSAT/LT05/C02/T2_L2").filterDate("2000-06-01", "2000-07-01")
        def applyScaleFactors(image):
                     opticalBands = image.select("SR_B.").multiply(0.0000275).add(-0.2)
                     thermalBand = image.select("ST_B6").multiply(0.00341802).add(149.0)
                     return image.addBands(opticalBands, None, True).addBands(thermalBand, None, True)
        dataset = dataset.map(applyScaleFactors)
        visualization = {
        "bands": ["SR_B3", "SR_B2", "SR_B1"],
        "min": 0.0,
        "max": 0.3,
        }
        Map.setCenter(-83, 24, 8)
        Map.addLayer(dataset, visualization, "True Color (321)")

    elif cod == "LANDSAT/LT05/C02/T2_TOA":
        dataset = ee.ImageCollection("LANDSAT/LT05/C02/T2_TOA").filterDate("2011-01-01", "2011-12-31")
        trueColor321 = dataset.select(["B3", "B2", "B1"])
        trueColor321Vis = {
        "min": 0.0,
        "max": 0.4,
        "gamma": 1.2,
        }
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(trueColor321, trueColor321Vis, "True Color (321)")

    elif cod == "LANDSAT/MANGROVE_FORESTS":
        dataset = ee.ImageCollection("LANDSAT/MANGROVE_FORESTS")
        mangrovesVis = {
        "min": 0,
        "max": 1.0,
        "palette": ["d40115"],
        }
        Map.setCenter(-44.5626, -2.0164, 9)
        Map.addLayer(dataset, mangrovesVis, "Mangroves")

    elif cod == "LARSE/GEDI/GEDI02_A_002/GEDI02_A_2021244154857_O15413_04_T05622_02_003_02_V002":
        dataset = ee.FeatureCollection("LARSE/GEDI/GEDI02_A_002/GEDI02_A_2021244154857_O15413_04_T05622_02_003_02_V002")
        dataset = dataset.style({"color": "black", "pointSize": 1})
        Map.setCenter(-64.88, -31.77, 15)
        Map.addLayer(dataset)

    elif cod == "LARSE/GEDI/GEDI02_A_002_INDEX":
        rectangle = ee.Geometry.Rectangle([-111.22, 24.06, -6.54, 51.9])
        filter_index = ee.FeatureCollection("LARSE/GEDI/GEDI02_A_002_INDEX").filter("time_start > 2020-10-10T15:57:18Z" & "time_end < 2020-10-11T01:20:45Z").filterBounds(rectangle)
        Map.addLayer(filter_index)

    elif cod == "LARSE/GEDI/GEDI02_A_002_MONTHLY":
        qualityMask = lambda im: im.updateMask(im.select("quality_flag").eq(1)).updateMask(im.select("degrade_flag").eq(0))
        dataset = ee.ImageCollection("LARSE/GEDI/GEDI02_A_002_MONTHLY").map(qualityMask).select("rh98")
        gediVis = {
        "min": 1,
        "max": 60,
        "palette": "darkred,red,orange,green,darkgreen",
        }
        Map.setCenter(-74.803466, -9.342209, 10)
        Map.addLayer(dataset, gediVis, "rh98")

    elif cod == "LARSE/GEDI/GEDI02_B_002/GEDI02_B_2021043114136_O12295_03_T07619_02_003_01_V002":
        dataset = ee.FeatureCollection("LARSE/GEDI/GEDI02_B_002/GEDI02_B_2021043114136_O12295_03_T07619_02_003_01_V002")
        Map.setCenter(12.60033, 51.01051, 14)
        Map.addLayer(dataset)
            
    elif cod == "LARSE/GEDI/GEDI02_B_002_INDEX":
        rectangle = ee.Geometry.Rectangle([-111.22, 24.06, -6.54, 51.9])
        filter_index = ee.FeatureCollection("LARSE/GEDI/GEDI02_B_002_INDEX").filter("time_start > 2020-10-10T15:57:18Z" & "time_end < 2020-10-11T01:20:45Z").filterBounds(rectangle)
        Map.addLayer(filter_index)

    elif cod == "LARSE/GEDI/GEDI02_B_002_MONTHLY":
        qualityMask = lambda im: im.updateMask(im.select("l2b_quality_flag").eq(1)).updateMask(im.select("degrade_flag").eq(0))
        dataset = ee.ImageCollection("LARSE/GEDI/GEDI02_B_002_MONTHLY").map(qualityMask).select("solar_elevation")
        gediVis = {
        "min": 1,
        "max": 60,
        "palette": "red, green, blue",
        }
        Map.setCenter(12.60033, 51.01051, 12)
        Map.addLayer(dataset, gediVis, "Solar Elevation")

    elif cod == "LARSE/GEDI/GEDI04_A_002/GEDI04_A_2022157233128_O19728_03_T11129_02_003_01_V002":
        dataset = ee.FeatureCollection("LARSE/GEDI/GEDI04_A_002/GEDI04_A_2022157233128_O19728_03_T11129_02_003_01_V002")
        Map.setCenter(-94.77616, 38.9587, 14)
        Map.addLayer(dataset)

    elif cod == "LARSE/GEDI/GEDI04_A_002_INDEX":
        rectangle = ee.Geometry.Rectangle([-111.22, 24.06, -6.54, 51.9])
        filter_index = ee.FeatureCollection("LARSE/GEDI/GEDI04_A_002_INDEX").filter("time_start > 2020-10-10T15:57:18Z" & "time_end < 2020-10-11T01:20:45Z").filterBounds(rectangle)
        Map.addLayer(filter_index)

    elif cod == "LARSE/GEDI/GEDI04_A_002_MONTHLY":
        qualityMask = lambda im : im.updateMask(im.select("l4_quality_flag").eq(1)).updateMask(im.select("degrade_flag").eq(0))
        dataset = ee.ImageCollection("LARSE/GEDI/GEDI04_A_002_MONTHLY").map(qualityMask).select("solar_elevation")
        gediVis = {
        "min": 1,
        "max": 60,
        "palette": "red, green, blue",
        }
        Map.setCenter(5.0198, 51.7564, 12)
        Map.addLayer(dataset, gediVis, "Solar Elevation")

    elif cod == "LARSE/GEDI/GEDI04_B_002":
        l4b = ee.Image("LARSE/GEDI/GEDI04_B_002")
        Map.addLayer(
            l4b.select("MU"), {"min": 10, "max": 250, "palette": "440154,414387,2a788e,23a884,7ad151,fde725"}, "Mean Biomass"
        )
        Map.addLayer( l4b.select("SE"), {"min": 10, "max": 50, "palette": "000004,3b0f6f,8c2981,dd4a69,fe9f6d,fcfdbf"}, "Standard Error"
                    )

    elif cod == "MERIT/DEM/v1_0_3":
        dataset = ee.Image("MERIT/DEM/v1_0_3")
        visualization = {
        "bands": ["dem"],
        "min": -3,
        "max": 18,
        "palette": ["000000", "478FCD", "86C58E", "AFC35E", "8F7131",
                    "B78D4F", "E2B8A6", "FFFFFF"]
        }
        Map.setCenter(90.301, 23.052, 10)
        Map.addLayer(dataset, visualization, "Elevation")

    elif cod == "MERIT/Hydro/v1_0_1":
        dataset = ee.Image("MERIT/Hydro/v1_0_1")
        visualization = {
        "bands": ["viswth"],
        }
        Map.setCenter(90.301, 23.052, 10)
        Map.addLayer(dataset, visualization, "River width")

    elif cod == "MERIT/Hydro_reduced/v1_0_1":
        dataset = ee.Image("MERIT/Hydro_reduced/v1_0_1")
        visualization = {
        "bands": "wth",
        "min": 0,
        "max": 400
        }
        Map.setCenter(90.301, 23.052, 10)
        Map.addLayer(dataset, visualization, "River width")

    elif cod == "MODIS/006/MCD19A2_GRANULES":
        collection = ee.ImageCollection("MODIS/006/MCD19A2_GRANULES").select("Optical_Depth_047").filterDate("2019-01-01", "2019-01-15")
        band_viz = {
        "min": 0,
        "max": 500,
        "palette": ["black", "blue", "purple", "cyan", "green", "yellow", "red"]
        }
        Map.addLayer(collection.mean(), band_viz, "Optical Depth 047")
        Map.setCenter(76, 13, 6)

    elif cod == "MODIS/006/MOD10A1":
        dataset = ee.ImageCollection("MODIS/006/MOD10A1").filter(ee.Filter.date("2018-01-01", "2018-05-01"))
        snowCover = dataset.select("NDSI_Snow_Cover")
        snowCoverVis = {
        "min": 0.0,
        "max": 100.0,
        "palette": ["black", "0dffff", "0524ff", "ffffff"],
        }
        Map.setCenter(-41.13, 76.35, 2)
        Map.addLayer(snowCover, snowCoverVis, "Snow Cover")

    elif cod == "MODIS/006/MOD16A2":
        dataset = ee.ImageCollection("MODIS/006/MOD16A2").filter(ee.Filter.date("2018-01-01", "2018-05-01"))
        evapotranspiration = dataset.select("ET")
        evapotranspirationVis = {
        "min": 0.0,
        "max": 300.0,
        "palette": [
            "ffffff", "fcd163", "99b718", "66a000", "3e8601", "207401", "056201",
            "004c00", "011301"
        ],
        }
        Map.setCenter(6.746, 46.529, 2)
        Map.addLayer(evapotranspiration, evapotranspirationVis, "Evapotranspiration")

    elif cod == "MODIS/006/MOD17A2H":
        dataset = ee.ImageCollection("MODIS/006/MOD17A2H").filter(ee.Filter.date("2018-01-01", "2018-05-01"))
        gpp = dataset.select("Gpp")
        gppVis = {
        "min": 0.0,
        "max": 600.0,
        "palette": ["bbe029", "0a9501", "074b03"],
        }
        Map.setCenter(6.746, 46.529, 2)
        Map.addLayer(gpp, gppVis, "GPP")

    elif cod == "MODIS/006/MOD44B":
        dataset = ee.ImageCollection("MODIS/006/MOD44B")
        visualization = {
        "bands": ["Percent_Tree_Cover"],
        "min": 0.0,
        "max": 100.0,
        "palette": ["bbe029", "0a9501", "074b03"]
        }
        Map.centerObject(dataset)
        Map.addLayer(dataset, visualization, "Percent Tree Cover")

    elif cod == "MODIS/006/MOD44W":
        dataset = ee.ImageCollection("MODIS/006/MOD44W").filter(ee.Filter.date("2015-01-01", "2015-05-01"))
        waterMask = dataset.select("water_mask")
        waterMaskVis = {
        "min": 0.0,
        "max": 1.0,
        "palette": ["bcba99", "2d0491"],
        }
        Map.setCenter(6.746, 46.529, 2)
        Map.addLayer(waterMask, waterMaskVis, "Water Mask")

    elif cod == "MODIS/006/MOD44W":
        dataset = ee.ImageCollection("MODIS/006/MOD44W").filter(ee.Filter.date("2015-01-01", "2015-05-01"))
        waterMask = dataset.select("water_mask")
        waterMaskVis = {
        "min": 0.0,
        "max": 1.0,
        "palette": ["bcba99", "2d0491"],
        }
        Map.setCenter(6.746, 46.529, 2)
        Map.addLayer(waterMask, waterMaskVis, "Water Mask")

    elif cod == "MODIS/006/MODOCGA":
        dataset = ee.ImageCollection("MODIS/006/MODOCGA").filter(ee.Filter.date("2018-01-01", "2018-05-01"))
        FalseColor = dataset.select(["sur_refl_b11", "sur_refl_b10", "sur_refl_b09"])
        FalseColorVis = {
        "min": 0.0,
        "max": 2000.0}
        Map.setCenter(6.746, 46.529, 2)
        Map.addLayer(FalseColor, FalseColorVis, "False Color")

    elif cod == "MODIS/006/MYD10A1":
        dataset = ee.ImageCollection("MODIS/006/MYD10A1").filter(ee.Filter.date("2018-01-01", "2018-05-01"))
        snowCover = dataset.select("NDSI_Snow_Cover")
        snowCoverVis = {
        "min": 0.0,
        "max": 100.0,
        "palette": ["black", "0dffff", "0524ff", "ffffff"],
        }
        Map.setCenter(-38.13, 40, 2)
        Map.addLayer(snowCover, snowCoverVis, "Snow Cover")

    elif cod == "MODIS/006/MYD17A2H":
        dataset = ee.ImageCollection("MODIS/006/MYD17A2H").filter(ee.Filter.date("2018-01-01", "2018-05-01"))
        gpp = dataset.select("Gpp")
        gppVis = {
        "min": 0.0,
        "max": 600.0,
        "palette": ["bbe029", "0a9501", "074b03"],
        }
        Map.setCenter(6.746, 46.529, 2)
        Map.addLayer(gpp, gppVis, "GPP")

    elif cod == "MODIS/006/MYDOCGA":
        dataset = ee.ImageCollection("MODIS/006/MYDOCGA").filter(ee.Filter.date("2018-01-01", "2018-05-01"))
        FalseColor = dataset.select(["sur_refl_b11", "sur_refl_b10", "sur_refl_b09"])
        FalseColorVis = {
        "min": 0.0,
        "max": 2000.0,
        }
        Map.setCenter(6.746, 46.529, 2)
        Map.addLayer(FalseColor, FalseColorVis, "False Color")

    elif cod == "MODIS/061/MCD12Q1":
        dataset = ee.ImageCollection("MODIS/061/MCD12Q1")
        igbpLandCover = dataset.select("LC_Type1")
        igbpLandCoverVis = {
        "min": 1.0,
        "max": 17.0,
        "palette": [
        "05450a", "086a10", "54a708", "78d203", "009900", "c6b044", "dcd159",
        "dade48", "fbff13", "b6ff05", "27ff87", "c24f44", "a5a5a5", "ff6d4c",
        "69fff8", "f9ffa4", "1c0dff"
        ],
        }
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(igbpLandCover, igbpLandCoverVis, "IGBP Land Cover")

    elif cod == "MODIS/061/MCD12Q2":
        dataset = ee.ImageCollection("MODIS/061/MCD12Q2").filter(ee.Filter.date("2001-01-01", "2002-01-01"))
        vegetationPeak = dataset.select("Peak_1")
        vegetationPeakVis = {
        "min": 11400,
        "max": 11868,
        "palette": ["0f17ff", "b11406", "f1ff23"],
        }
        Map.setCenter(6.746, 46.529, 2)
        Map.addLayer(vegetationPeak, vegetationPeakVis, "Vegetation Peak 2001")

    elif cod == "MODIS/061/MCD15A3H":
        dataset = ee.ImageCollection("MODIS/061/MCD15A3H")
        defaultVisualization = dataset.first().select("Fpar")
        defaultVisualizationVis = {
        "min": 0.0,
        "max": 100.0,
        "palette": ["e1e4b4", "999d60", "2ec409", "0a4b06"],
        }
        Map.setCenter(6.746, 46.529, 6)
        Map.addLayer(
        defaultVisualization, defaultVisualizationVis, "Default visualization")

    elif cod == "MODIS/061/MCD18C2":
        dataset = ee.ImageCollection("MODIS/061/MCD18C2").filter(ee.Filter.date("2001-01-01", "2001-02-01"))
        gmt_1200_par = dataset.select("GMT_1200_PAR")
        gmt_1200_par_vis = {
        "min": -236,
        "max": 316,
        "palette": ["0f17ff", "b11406", "f1ff23"],
        }
        Map.setCenter(6.746, 46.529, 2)
        Map.addLayer(gmt_1200_par, gmt_1200_par_vis,"Total PAR at GMT 12:00")

    elif cod == "COPERNICUS/CORINE/V20/100m":
        dataset = ee.Image('COPERNICUS/CORINE/V20/100m/2012')
        landCover = dataset.select('landcover')
        Map.setCenter(16.436, 39.825, 6)
        Map.addLayer(landCover, {}, 'Land Cover')
    
    elif cod == "LANDSAT/GLS1975_MOSAIC":
        dataset = ee.ImageCollection('LANDSAT/GLS1975_MOSAIC')
        falseColor = dataset.select(['30', '20', '10'])
        falseColorVis = {
        "gamma": 1.6,
        }
        Map.setCenter(-72.882406,5.181746, 5);
        Map.addLayer(falseColor, falseColorVis, 'False Color')
    
    elif cod == "LANDSAT/LC08/C01/T1_8DAY_BAI":
        dataset = ee.ImageCollection('LANDSAT/LC08/C01/T1_8DAY_BAI').filterDate('2017-01-01', '2017-12-31')
        scaled = dataset.select('BAI')
        scaledVis = {
        "min": 0.0,
        "max": 100.0,
        }
        Map.setCenter(-72.882406,5.181746, 6)
        Map.addLayer(scaled, scaledVis, 'Scaled')
    
    elif cod == "LANDSAT/LC08/C01/T1_8DAY_EVI":
        dataset = ee.ImageCollection('LANDSAT/LC08/C01/T1_8DAY_EVI').filterDate('2017-01-01', '2017-12-31')
        colorized = dataset.select('EVI')
        colorizedVis = {
        "min": 0.0,
        "max": 1.0,
        "palette": [
            'FFFFFF', 'CE7E45', 'DF923D', 'F1B555', 'FCD163', '99B718', '74A901',
            '66A000', '529400', '3E8601', '207401', '056201', '004C00', '023B01',
            '012E01', '011D01', '011301']
        }
        Map.setCenter(-72.882406,5.181746, 6)
        Map.addLayer(colorized, colorizedVis, 'Colorized')
    
    elif cod == "LANDSAT/LC08/C01/T1_8DAY_NDSI":
        dataset = ee.ImageCollection('LANDSAT/LC08/C01/T1_8DAY_NDSI').filterDate('2017-01-01', '2017-12-31')
        colorized = dataset.select('NDSI')
        colorizedVis = {
        "palette": ['000088', '0000FF', '8888FF', 'FFFFFF'],
        }
        Map.setCenter(-72.882406,5.181746, 6);
        Map.addLayer(colorized, colorizedVis, 'Colorized')
    
    elif cod == "LANDSAT/LC08/C01/T1_8DAY_NDVI":
        dataset = ee.ImageCollection('LANDSAT/LC08/C01/T1_8DAY_NDVI').filterDate('2017-01-01', '2017-12-31')
        colorized = dataset.select('NDVI')
        colorizedVis = {
        "min": 0.0,
        "max": 1.0,
        "palette": [
            'FFFFFF', 'CE7E45', 'DF923D', 'F1B555', 'FCD163', '99B718', '74A901',
            '66A000', '529400', '3E8601', '207401', '056201', '004C00', '023B01',
            '012E01', '011D01', '011301']}
        Map.setCenter(-72.882406,5.181746, 6)
        Map.addLayer(colorized, colorizedVis, 'Colorized')
    
    elif cod == "LANDSAT/LC08/C01/T1_8DAY_NDWI":
        dataset = ee.ImageCollection('LANDSAT/LC08/C01/T1_8DAY_NDWI').filterDate('2017-01-01', '2017-12-31')
        colorized = dataset.select('NDWI')
        colorizedVis = {
        "min": 0.0,
        "max": 1.0,
        "palette": ['0000ff', '00ffff', 'ffff00', 'ff0000', 'ffffff'],
        };
        Map.setCenter(-72.882406,5.181746, 6)
        Map.addLayer(colorized, colorizedVis, 'Colorized')
    
    elif cod == "LANDSAT/LC08/C01/T1_8DAY_RAW":
        dataset = ee.ImageCollection('LANDSAT/LC08/C01/T1_8DAY_RAW').filterDate('2017-01-01', '2017-12-31')
        visParams = {
        "min": 0,
        "max": 20000,
        "gamma": 1.2,
        "bands": ['B4', 'B3', 'B2'],
        }
        Map.setCenter(-72.882406,5.181746, 6)
        Map.addLayer(dataset, visParams, 'LANDSAT/LC08/C01/T1_8DAY_RAW')
    
    elif cod == "LANDSAT/LC08/C01/T1_8DAY_TOA":
        dataset = ee.ImageCollection('LANDSAT/LC08/C01/T1_8DAY_TOA').filterDate('2017-01-01', '2017-12-31')
        trueColor = dataset.select(['B4', 'B3', 'B2'])
        trueColorVis = {
        "min": 0,
        "max": 0.4,
        "gamma": 1.2,
        }
        Map.setCenter(-72.882406,5.181746, 6)
        Map.addLayer(trueColor, trueColorVis, 'True Color (432)')
    
    elif cod == "LANDSAT/LC08/C01/T1_32DAY_BAI":
        dataset = ee.ImageCollection('LANDSAT/LC08/C01/T1_32DAY_BAI').filterDate('2017-01-01', '2017-12-31')
        scaled = dataset.select('BAI')
        scaledVis = {
        "min": 0.0,
        "max": 100.0,
        }
        Map.setCenter(-72.882406,5.181746, 6)
        Map.addLayer(scaled, scaledVis, 'Scaled')
    
    elif cod == "LANDSAT/LC08/C01/T1_32DAY_EVI":
        dataset = ee.ImageCollection('LANDSAT/LC08/C01/T1_32DAY_EVI').filterDate('2017-01-01', '2017-12-31')
        colorized = dataset.select('EVI')
        colorizedVis = {
        "min": 0.0,
        "max": 1.0,
        "palette": [
            'FFFFFF', 'CE7E45', 'DF923D', 'F1B555', 'FCD163', '99B718', '74A901',
            '66A000', '529400', '3E8601', '207401', '056201', '004C00', '023B01',
            '012E01', '011D01', '011301']
        }
        Map.setCenter(-72.882406,5.181746, 6)
        Map.addLayer(colorized, colorizedVis, 'Colorized')
    
    elif cod == "LANDSAT/LC08/C01/T1_32DAY_NBRT":
        dataset = ee.ImageCollection('LANDSAT/LC08/C01/T1_32DAY_NBRT').filterDate('2017-01-01', '2017-12-31')
        colorized = dataset.select('NBRT')
        colorizedVis = {
        "min": 0.9,
        "max": 1.0,
        "palette": ['000000', 'FFFFFF'],
        }
        Map.setCenter(-72.882406,5.181746, 6)
        Map.addLayer(colorized, colorizedVis, 'Colorized')
    
    elif cod == "LANDSAT/LC08/C01/T1_32DAY_NDSI":
        dataset = ee.ImageCollection('LANDSAT/LC08/C01/T1_32DAY_NDSI').filterDate('2017-01-01', '2017-12-31')
        colorized = dataset.select('NDSI')
        colorizedVis = {
        "palette": ['000088', '0000FF', '8888FF', 'FFFFFF'],
        };
        Map.setCenter(-72.882406,5.181746, 6)
        Map.addLayer(colorized, colorizedVis, 'Colorized')
    
    elif cod == "LANDSAT/LC08/C01/T1_32DAY_NDVI":
        dataset = ee.ImageCollection('LANDSAT/LC08/C01/T1_32DAY_NDVI').filterDate('2017-01-01', '2017-12-31')
        colorized = dataset.select('NDVI')
        colorizedVis = {
        "min": 0.0,
        "max": 1.0,
        "palette": [
            'FFFFFF', 'CE7E45', 'DF923D', 'F1B555', 'FCD163', '99B718', '74A901',
            '66A000', '529400', '3E8601', '207401', '056201', '004C00', '023B01',
            '012E01', '011D01', '011301']
        }
        Map.setCenter(-72.882406,5.181746, 6)
        Map.addLayer(colorized, colorizedVis, 'Colorized')
    
    elif cod == "LANDSAT/LC08/C01/T1_32DAY_NDWI":
        dataset = ee.ImageCollection('LANDSAT/LC08/C01/T1_32DAY_NDWI').filterDate('2017-01-01', '2017-12-31')        
        colorized = dataset.select('NDWI');
        colorizedVis = {
        "min": 0.0,
        "max": 1.0,
        "palette": ['0000ff', '00ffff', 'ffff00', 'ff0000', 'ffffff']
        }
        Map.setCenter(-72.882406,5.181746, 6)
        Map.addLayer(colorized, colorizedVis, 'Colorized')
    
    elif cod == "LANDSAT/LC08/C01/T1_32DAY_RAW":
        dataset = ee.ImageCollection('LANDSAT/LC08/C01/T1_32DAY_RAW').filterDate('2017-01-01', '2017-12-31')
        visParams = {
        "min": 0,
        "max": 20000,
        "gamma": 1.2,
        "bands": ['B4', 'B3', 'B2']
        }
        Map.setCenter(-72.882406,5.181746, 6)
        Map.addLayer(dataset, visParams, 'LANDSAT/LC08/C01/T1_32DAY_RAW')
    
    elif cod == "LANDSAT/LC08/C01/T1_32DAY_TOA":
        dataset = ee.ImageCollection('LANDSAT/LC08/C01/T1_32DAY_TOA').filterDate('2017-01-01', '2017-12-31')
        trueColor = dataset.select(['B4', 'B3', 'B2'])
        trueColorVis = {
        "min": 0,
        "max": 0.4,
        "gamma": 1.2,
        }
        Map.setCenter(-72.882406,5.181746, 6)
        Map.addLayer(trueColor, trueColorVis, 'True Color (432)')
    
    elif cod == "LANDSAT/LC08/C01/T1_ANNUAL_BAI":
        dataset = ee.ImageCollection('LANDSAT/LC08/C01/T1_ANNUAL_BAI') \
                  .filterDate('2017-01-01', '2017-12-31')
        scaled = dataset.select('BAI')
        scaledVis = {
        "min": 0.0,
        "max": 100.0,
        }
        Map.setCenter(-72.882406,5.181746, 6)
        Map.addLayer(scaled, scaledVis, 'Scaled')

    elif cod == "NOAA/DMSP-OLS/CALIBRATED_LIGHTS_V4":
        dataset = ee.ImageCollection('NOAA/DMSP-OLS/CALIBRATED_LIGHTS_V4')\
                  .filterDate('2010-01-01', '2010-12-31')
        nighttimeLights = dataset.select('avg_vis')
        nighttimeLightsVis = {
        "min": 3.0,
        "max": 60.0,
        }
        Map.setCenter(7.82, 49.1, 4)
        Map.addLayer(nighttimeLights, nighttimeLightsVis, 'Nighttime Lights')

    elif cod == "NOAA/VIIRS/DNB/MONTHLY_V1/VCMCFG":
        dataset = ee.ImageCollection('NOAA/VIIRS/DNB/MONTHLY_V1/VCMCFG').filterDate('2022-01-01', '2023-12-31')
        nighttime = dataset.select('avg_rad')
        nighttimeVis = {
            "min": 0.0,
            "max": 60.0,
        }
        Map.setCenter(67.1056, 24.8904, 8)
        Map.addLayer(nighttime, nighttimeVis, 'Nighttime')
