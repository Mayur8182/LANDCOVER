import ee
import os
from geopy.geocoders import Nominatim
from backend.utils import generate_filename

class GEEHandler:
    def __init__(self):
        """Initialize Google Earth Engine - REQUIRED for this application"""
        self.initialized = False
        
        # Setup credentials from environment variable if available
        gee_creds = os.getenv('GEE_CREDENTIALS')
        if gee_creds:
            creds_dir = os.path.expanduser('~/.config/earthengine')
            os.makedirs(creds_dir, exist_ok=True)
            creds_path = os.path.join(creds_dir, 'credentials')
            
            # Write credentials to file
            with open(creds_path, 'w') as f:
                f.write(gee_creds)
            print("✓ GEE credentials loaded from environment variable")
        
        # Check for credentials file
        creds_path = os.path.expanduser('~/.config/earthengine/credentials')
        if not os.path.exists(creds_path):
            print("=" * 60)
            print("❌ ERROR: GEE credentials not found!")
            print("=" * 60)
            print("This application REQUIRES Google Earth Engine credentials.")
            print("Please add GEE_CREDENTIALS environment variable.")
            print("=" * 60)
        
        try:
            # Try to initialize with project ID from environment
            project_id = os.getenv('GEE_PROJECT_ID', 'gleaming-tube-445109-t2')
            ee.Initialize(project=project_id)
            print("=" * 60)
            print(f"✅ GEE initialized successfully!")
            print(f"📡 Project: {project_id}")
            print("=" * 60)
            self.initialized = True
        except Exception as e:
            print("=" * 60)
            print(f"❌ GEE initialization FAILED: {e}")
            print("=" * 60)
            print("⚠️  This application will NOT work without GEE!")
            print("⚠️  Please check GEE_CREDENTIALS and GEE_PROJECT_ID")
            print("=" * 60)
            # Try without project ID as fallback
            try:
                ee.Initialize()
                print("✓ GEE initialized without project ID")
                self.initialized = True
            except Exception as e2:
                print(f"❌ Final attempt failed: {e2}")
                self.initialized = False
    
    def search_location(self, location_name):
        """Search location by name and return coordinates"""
        geolocator = Nominatim(user_agent="land_cover_classifier")
        location = geolocator.geocode(location_name)
        
        if location:
            return {
                'lat': location.latitude,
                'lon': location.longitude,
                'display_name': location.address
            }
        else:
            raise ValueError(f"Location '{location_name}' not found")
    
    def fetch_satellite_data(self, bounds, start_date, end_date, dataset_type='sentinel'):
        """Fetch satellite imagery from Google Earth Engine
        
        Args:
            bounds: Dictionary with north, south, east, west coordinates
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            dataset_type: 'sentinel' or 'modis'
        """
        # Define area of interest
        aoi = ee.Geometry.Rectangle([
            bounds['west'], bounds['south'],
            bounds['east'], bounds['north']
        ])
        
        if dataset_type == 'modis':
            # Fetch MODIS Land Cover data
            collection = ee.ImageCollection('MODIS/061/MCD12Q1') \
                .filterDate(start_date, end_date) \
                .filterBounds(aoi)
            
            # Get most recent image
            image = collection.sort('system:time_start', False).first()
            
            # Select land cover type
            landcover = image.select('LC_Type1').clip(aoi)
            
            # Get download URL
            url = landcover.getDownloadURL({
                'scale': 500,  # MODIS resolution
                'region': aoi,
                'format': 'GEO_TIFF'
            })
            
            return {
                'image_id': 'MODIS_MCD12Q1',
                'download_url': url,
                'bounds': bounds,
                'date_range': {'start': start_date, 'end': end_date},
                'dataset': 'MODIS',
                'resolution': '500m',
                'cloud_cover': None
            }
        else:
            # Fetch Sentinel-2 imagery
            try:
                collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
                    .filterBounds(aoi) \
                    .filterDate(start_date, end_date) \
                    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 30))
                
                count = collection.size().getInfo()
                print(f"Sentinel-2: Found {count} images for {start_date} to {end_date}")
                
                if count == 0:
                    # Try with relaxed cloud cover
                    collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
                        .filterBounds(aoi) \
                        .filterDate(start_date, end_date) \
                        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 50))
                    
                    count = collection.size().getInfo()
                    print(f"Relaxed filter: Found {count} images")
                
                if count == 0:
                    raise Exception(f"No Sentinel-2 images found for {start_date} to {end_date}")
                
            except Exception as e:
                print(f"Harmonized collection error: {e}, trying original collection")
                collection = ee.ImageCollection('COPERNICUS/S2_SR') \
                    .filterBounds(aoi) \
                    .filterDate(start_date, end_date) \
                    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 30))
                
                count = collection.size().getInfo()
                if count == 0:
                    raise Exception(f"No Sentinel-2 images available for this area and dates")
            
            # Get median composite
            image = collection.median().clip(aoi)
            
            # Select RGB and NIR bands
            image = image.select(['B4', 'B3', 'B2', 'B8'])  # Red, Green, Blue, NIR
            
            # Calculate appropriate scale based on area size
            area_sqkm = aoi.area().divide(1000000).getInfo()
            
            # Adjust scale to keep request size under 50MB
            if area_sqkm > 100:
                scale = 100  # Very large area
            elif area_sqkm > 50:
                scale = 50   # Large area
            elif area_sqkm > 10:
                scale = 30   # Medium area
            else:
                scale = 10   # Small area (original resolution)
            
            print(f"Sentinel-2 Area: {area_sqkm:.2f} km², using scale: {scale}m")
            
            # Get download URL
            url = image.getDownloadURL({
                'scale': scale,
                'region': aoi,
                'format': 'GEO_TIFF',
                'filePerBand': False
            })
            
            cloud_cover = collection.aggregate_mean('CLOUDY_PIXEL_PERCENTAGE').getInfo()
            
            return {
                'image_id': 'sentinel2_composite',
                'download_url': url,
                'bounds': bounds,
                'date_range': {'start': start_date, 'end': end_date},
                'dataset': 'Sentinel-2',
                'resolution': '10m',
                'cloud_cover': cloud_cover,
                'image_count': count
            }
    
    def export_to_tif(self, image_id, bounds, dataset_type='sentinel'):
        """Export image to .tif file with size limits"""
        aoi = ee.Geometry.Rectangle([
            bounds['west'], bounds['south'],
            bounds['east'], bounds['north']
        ])
        
        # Calculate appropriate scale based on area size
        area = aoi.area().getInfo() / 1000000  # km²
        
        # Calculate dimensions at different scales to stay under 32768 pixel limit
        # Max pixels = 32768 x 32768 = 1,073,741,824 pixels
        # Safe limit = 30000 x 30000 = 900,000,000 pixels
        
        if dataset_type == 'modis':
            scale = 500
            collection = ee.ImageCollection('MODIS/061/MCD12Q1') \
                .filterBounds(aoi)
            
            image = collection.sort('system:time_start', False).first()
            landcover = image.select('LC_Type1').clip(aoi)
            
            filename = generate_filename('modis_landcover', 'tif')
            export_path = os.path.join('exports', filename)
            
            url = landcover.getDownloadURL({
                'scale': scale,
                'region': aoi,
                'format': 'GEO_TIFF',
                'crs': 'EPSG:4326'
            })
        else:
            # Calculate required scale to stay under pixel limit
            # Area in square meters
            area_m2 = area * 1000000
            
            # Calculate side length (assuming square for simplicity)
            side_length = (area_m2 ** 0.5)
            
            # Calculate minimum scale needed
            # pixels = side_length / scale
            # We want pixels < 30000
            min_scale = side_length / 30000
            
            # Choose appropriate scale
            if min_scale > 500:
                scale = 1000  # Very large area
            elif min_scale > 100:
                scale = 500   # Large area
            elif min_scale > 50:
                scale = 100   # Medium-large area
            elif min_scale > 20:
                scale = 50    # Medium area
            elif min_scale > 10:
                scale = 30    # Small-medium area
            else:
                scale = 10    # Small area
            
            print(f"Area: {area:.2f} km², Using scale: {scale}m")
            
            try:
                # Limit to recent 6 months and best 30 images
                from datetime import datetime, timedelta
                end_date = datetime.now()
                start_date = end_date - timedelta(days=180)
                
                collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
                    .filterBounds(aoi) \
                    .filterDate(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')) \
                    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
                    .sort('CLOUDY_PIXEL_PERCENTAGE') \
                    .limit(30)
                
                # Check if collection has images
                count = collection.size().getInfo()
                print(f"Found {count} Sentinel-2 images (limited to 30 best)")
                
                if count == 0:
                    raise Exception("No Sentinel-2 images found for this area")
                
                image = collection.median().clip(aoi)
                
                # Select available bands (B2=Blue, B3=Green, B4=Red, B8=NIR)
                image = image.select(['B4', 'B3', 'B2', 'B8'])
                
            except Exception as e:
                print(f"Sentinel-2 error: {e}")
                # Fallback to older collection with limit
                from datetime import datetime, timedelta
                end_date = datetime.now()
                start_date = end_date - timedelta(days=180)
                
                collection = ee.ImageCollection('COPERNICUS/S2_SR') \
                    .filterBounds(aoi) \
                    .filterDate(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')) \
                    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 30)) \
                    .sort('CLOUDY_PIXEL_PERCENTAGE') \
                    .limit(30)
                
                count = collection.size().getInfo()
                print(f"Fallback: Found {count} images")
                
                if count == 0:
                    raise Exception("No satellite images available for this area")
                
                image = collection.median().clip(aoi)
                image = image.select(['B4', 'B3', 'B2', 'B8'])
            
            filename = generate_filename('satellite_image', 'tif')
            export_path = os.path.join('exports', filename)
            
            try:
                url = image.getDownloadURL({
                    'scale': scale,
                    'region': aoi,
                    'format': 'GEO_TIFF',
                    'crs': 'EPSG:4326',
                    'filePerBand': False
                })
            except Exception as e:
                print(f"Download URL error: {e}")
                # Try with larger scale if download fails
                scale = scale * 2
                print(f"Retrying with scale: {scale}m")
                url = image.getDownloadURL({
                    'scale': scale,
                    'region': aoi,
                    'format': 'GEO_TIFF',
                    'crs': 'EPSG:4326',
                    'filePerBand': False
                })
        
        # Download file
        import urllib.request
        try:
            print(f"Downloading from GEE...")
            urllib.request.urlretrieve(url, export_path)
            print(f"Download complete: {export_path}")
        except Exception as e:
            print(f"Download failed: {e}")
            raise Exception(f"Failed to download satellite image: {str(e)}")
        
        return export_path
    
    def calculate_ndvi(self, image):
        """Calculate NDVI (Normalized Difference Vegetation Index)"""
        nir = image.select('B8')
        red = image.select('B4')
        ndvi = nir.subtract(red).divide(nir.add(red)).rename('NDVI')
        return ndvi
    
    def calculate_ndwi(self, image):
        """Calculate NDWI (Normalized Difference Water Index)"""
        green = image.select('B3')
        nir = image.select('B8')
        ndwi = green.subtract(nir).divide(green.add(nir)).rename('NDWI')
        return ndwi

    def get_modis_landcover(self, bounds, year='2022'):
        """Get MODIS Land Cover data for specific year
        
        MODIS Land Cover Classes (LC_Type1):
        0: Water
        1: Evergreen Needleleaf Forest
        2: Evergreen Broadleaf Forest
        3: Deciduous Needleleaf Forest
        4: Deciduous Broadleaf Forest
        5: Mixed Forests
        6: Closed Shrublands
        7: Open Shrublands
        8: Woody Savannas
        9: Savannas
        10: Grasslands
        11: Permanent Wetlands
        12: Croplands
        13: Urban and Built-up
        14: Cropland/Natural Vegetation Mosaic
        15: Snow and Ice
        16: Barren or Sparsely Vegetated
        17: Unclassified
        """
        aoi = ee.Geometry.Rectangle([
            bounds['west'], bounds['south'],
            bounds['east'], bounds['north']
        ])
        
        # Fetch MODIS Land Cover
        dataset = ee.ImageCollection('MODIS/061/MCD12Q1') \
            .filterDate(f'{year}-01-01', f'{year}-12-31') \
            .first()
        
        landcover = dataset.select('LC_Type1').clip(aoi)
        
        # Get statistics
        stats = landcover.reduceRegion(
            reducer=ee.Reducer.frequencyHistogram(),
            geometry=aoi,
            scale=500,
            maxPixels=1e9
        )
        
        return {
            'image': landcover,
            'statistics': stats.getInfo(),
            'year': year,
            'dataset': 'MODIS MCD12Q1',
            'resolution': '500m'
        }
    
    def get_modis_visualization_params(self):
        """Get visualization parameters for MODIS Land Cover"""
        return {
            'min': 0,
            'max': 17,
            'palette': [
                '05450a',  # 0: Water - Dark Blue
                '086a10',  # 1: Evergreen Needleleaf Forest
                '54a708',  # 2: Evergreen Broadleaf Forest
                '78d203',  # 3: Deciduous Needleleaf Forest
                '009900',  # 4: Deciduous Broadleaf Forest
                'c6b044',  # 5: Mixed Forests
                'dcd159',  # 6: Closed Shrublands
                'dade48',  # 7: Open Shrublands
                'fbff13',  # 8: Woody Savannas
                'b6ff05',  # 9: Savannas
                '27ff87',  # 10: Grasslands
                'c24f44',  # 11: Permanent Wetlands
                'a5a5a5',  # 12: Croplands
                'ff6d4c',  # 13: Urban and Built-up
                '69fff8',  # 14: Cropland/Natural Vegetation Mosaic
                'f9ffa4',  # 15: Snow and Ice
                '1c0dff',  # 16: Barren or Sparsely Vegetated
                '000000'   # 17: Unclassified
            ]
        }

    def detect_water_bodies(self, bounds, start_date, end_date):
        """Detect water bodies using NDWI (Normalized Difference Water Index)"""
        aoi = ee.Geometry.Rectangle([
            bounds['west'], bounds['south'],
            bounds['east'], bounds['north']
        ])
        
        # Fetch Sentinel-2 imagery
        collection = ee.ImageCollection('COPERNICUS/S2_SR') \
            .filterBounds(aoi) \
            .filterDate(start_date, end_date) \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
        
        # Get median composite
        image = collection.median().clip(aoi)
        
        # Calculate NDWI (Green - NIR) / (Green + NIR)
        green = image.select('B3')
        nir = image.select('B8')
        ndwi = green.subtract(nir).divide(green.add(nir)).rename('NDWI')
        
        # Threshold for water (NDWI > 0.3)
        water_mask = ndwi.gt(0.3)
        
        # Calculate water area
        water_area = water_mask.multiply(ee.Image.pixelArea()).reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=aoi,
            scale=10,
            maxPixels=1e9
        )
        
        return {
            'ndwi_image': ndwi,
            'water_mask': water_mask,
            'water_area_sqm': water_area.getInfo().get('NDWI', 0),
            'water_area_sqkm': water_area.getInfo().get('NDWI', 0) / 1000000,
            'threshold': 0.3
        }
    
    def calculate_ndvi_analysis(self, bounds, start_date, end_date):
        """Calculate NDVI for vegetation health analysis"""
        aoi = ee.Geometry.Rectangle([
            bounds['west'], bounds['south'],
            bounds['east'], bounds['north']
        ])
        
        # Fetch Sentinel-2 imagery
        collection = ee.ImageCollection('COPERNICUS/S2_SR') \
            .filterBounds(aoi) \
            .filterDate(start_date, end_date) \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
        
        # Get median composite
        image = collection.median().clip(aoi)
        
        # Calculate NDVI (NIR - Red) / (NIR + Red)
        nir = image.select('B8')
        red = image.select('B4')
        ndvi = nir.subtract(red).divide(nir.add(red)).rename('NDVI')
        
        # Get statistics
        stats = ndvi.reduceRegion(
            reducer=ee.Reducer.mean().combine(
                ee.Reducer.minMax(), '', True
            ).combine(
                ee.Reducer.stdDev(), '', True
            ),
            geometry=aoi,
            scale=10,
            maxPixels=1e9
        )
        
        stats_info = stats.getInfo()
        
        # Classify vegetation health
        # NDVI < 0.2: Barren/Urban
        # 0.2 - 0.4: Sparse vegetation
        # 0.4 - 0.6: Moderate vegetation
        # > 0.6: Dense vegetation
        
        return {
            'ndvi_image': ndvi,
            'mean_ndvi': stats_info.get('NDVI_mean', 0),
            'min_ndvi': stats_info.get('NDVI_min', 0),
            'max_ndvi': stats_info.get('NDVI_max', 0),
            'std_ndvi': stats_info.get('NDVI_stdDev', 0),
            'vegetation_health': self._classify_vegetation_health(stats_info.get('NDVI_mean', 0))
        }
    
    def _classify_vegetation_health(self, mean_ndvi):
        """Classify vegetation health based on NDVI"""
        if mean_ndvi < 0.2:
            return 'Poor (Barren/Urban)'
        elif mean_ndvi < 0.4:
            return 'Fair (Sparse Vegetation)'
        elif mean_ndvi < 0.6:
            return 'Good (Moderate Vegetation)'
        else:
            return 'Excellent (Dense Vegetation)'
    
    def detect_urban_sprawl(self, bounds, start_date_old, end_date_old, start_date_new, end_date_new):
        """Detect urban sprawl by comparing two time periods"""
        aoi = ee.Geometry.Rectangle([
            bounds['west'], bounds['south'],
            bounds['east'], bounds['north']
        ])
        
        # Get old period data
        old_collection = ee.ImageCollection('COPERNICUS/S2_SR') \
            .filterBounds(aoi) \
            .filterDate(start_date_old, end_date_old) \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
        
        old_image = old_collection.median().clip(aoi)
        
        # Get new period data
        new_collection = ee.ImageCollection('COPERNICUS/S2_SR') \
            .filterBounds(aoi) \
            .filterDate(start_date_new, end_date_new) \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
        
        new_image = new_collection.median().clip(aoi)
        
        # Calculate NDVI for both periods
        old_ndvi = self.calculate_ndvi(old_image.select(['B8', 'B4']))
        new_ndvi = self.calculate_ndvi(new_image.select(['B8', 'B4']))
        
        # Calculate NDBI (Normalized Difference Built-up Index)
        # NDBI = (SWIR - NIR) / (SWIR + NIR)
        old_ndbi = old_image.select('B11').subtract(old_image.select('B8')) \
            .divide(old_image.select('B11').add(old_image.select('B8'))).rename('NDBI')
        
        new_ndbi = new_image.select('B11').subtract(new_image.select('B8')) \
            .divide(new_image.select('B11').add(new_image.select('B8'))).rename('NDBI')
        
        # Detect urban areas (NDBI > 0 and NDVI < 0.2)
        old_urban = old_ndbi.gt(0).And(old_ndvi.lt(0.2))
        new_urban = new_ndbi.gt(0).And(new_ndvi.lt(0.2))
        
        # Calculate urban sprawl (new urban - old urban)
        urban_growth = new_urban.subtract(old_urban).gt(0)
        
        # Calculate areas
        old_urban_area = old_urban.multiply(ee.Image.pixelArea()).reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=aoi,
            scale=10,
            maxPixels=1e9
        )
        
        new_urban_area = new_urban.multiply(ee.Image.pixelArea()).reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=aoi,
            scale=10,
            maxPixels=1e9
        )
        
        growth_area = urban_growth.multiply(ee.Image.pixelArea()).reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=aoi,
            scale=10,
            maxPixels=1e9
        )
        
        old_area_sqkm = old_urban_area.getInfo().get('NDBI', 0) / 1000000
        new_area_sqkm = new_urban_area.getInfo().get('NDBI', 0) / 1000000
        growth_sqkm = growth_area.getInfo().get('NDBI', 0) / 1000000
        
        return {
            'old_urban_area_sqkm': old_area_sqkm,
            'new_urban_area_sqkm': new_area_sqkm,
            'urban_growth_sqkm': growth_sqkm,
            'growth_percentage': (growth_sqkm / old_area_sqkm * 100) if old_area_sqkm > 0 else 0,
            'old_period': f"{start_date_old} to {end_date_old}",
            'new_period': f"{start_date_new} to {end_date_new}",
            'urban_growth_mask': urban_growth
        }
    
    def detect_forest_change(self, bounds, start_date_old, end_date_old, start_date_new, end_date_new):
        """Detect forest cover change between two time periods"""
        aoi = ee.Geometry.Rectangle([
            bounds['west'], bounds['south'],
            bounds['east'], bounds['north']
        ])
        
        # Get old period data
        old_collection = ee.ImageCollection('COPERNICUS/S2_SR') \
            .filterBounds(aoi) \
            .filterDate(start_date_old, end_date_old) \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
        
        old_image = old_collection.median().clip(aoi)
        
        # Get new period data
        new_collection = ee.ImageCollection('COPERNICUS/S2_SR') \
            .filterBounds(aoi) \
            .filterDate(start_date_new, end_date_new) \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
        
        new_image = new_collection.median().clip(aoi)
        
        # Calculate NDVI for both periods
        old_ndvi = self.calculate_ndvi(old_image.select(['B8', 'B4']))
        new_ndvi = self.calculate_ndvi(new_image.select(['B8', 'B4']))
        
        # Define forest as NDVI > 0.6
        old_forest = old_ndvi.gt(0.6)
        new_forest = new_ndvi.gt(0.6)
        
        # Calculate forest loss and gain
        forest_loss = old_forest.And(new_forest.Not())
        forest_gain = old_forest.Not().And(new_forest)
        
        # Calculate areas
        old_forest_area = old_forest.multiply(ee.Image.pixelArea()).reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=aoi,
            scale=10,
            maxPixels=1e9
        )
        
        new_forest_area = new_forest.multiply(ee.Image.pixelArea()).reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=aoi,
            scale=10,
            maxPixels=1e9
        )
        
        loss_area = forest_loss.multiply(ee.Image.pixelArea()).reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=aoi,
            scale=10,
            maxPixels=1e9
        )
        
        gain_area = forest_gain.multiply(ee.Image.pixelArea()).reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=aoi,
            scale=10,
            maxPixels=1e9
        )
        
        old_area_sqkm = old_forest_area.getInfo().get('NDVI', 0) / 1000000
        new_area_sqkm = new_forest_area.getInfo().get('NDVI', 0) / 1000000
        loss_sqkm = loss_area.getInfo().get('NDVI', 0) / 1000000
        gain_sqkm = gain_area.getInfo().get('NDVI', 0) / 1000000
        
        net_change = new_area_sqkm - old_area_sqkm
        
        return {
            'old_forest_area_sqkm': old_area_sqkm,
            'new_forest_area_sqkm': new_area_sqkm,
            'forest_loss_sqkm': loss_sqkm,
            'forest_gain_sqkm': gain_sqkm,
            'net_change_sqkm': net_change,
            'change_percentage': (net_change / old_area_sqkm * 100) if old_area_sqkm > 0 else 0,
            'old_period': f"{start_date_old} to {end_date_old}",
            'new_period': f"{start_date_new} to {end_date_new}",
            'forest_loss_mask': forest_loss,
            'forest_gain_mask': forest_gain
        }
    
    def calculate_soil_moisture(self, bounds, start_date, end_date):
        """Estimate soil moisture using optical indices"""
        aoi = ee.Geometry.Rectangle([
            bounds['west'], bounds['south'],
            bounds['east'], bounds['north']
        ])
        
        # Fetch Sentinel-2 imagery
        collection = ee.ImageCollection('COPERNICUS/S2_SR') \
            .filterBounds(aoi) \
            .filterDate(start_date, end_date) \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
        
        # Get median composite
        image = collection.median().clip(aoi)
        
        # Calculate NDMI (Normalized Difference Moisture Index)
        # NDMI = (NIR - SWIR) / (NIR + SWIR)
        nir = image.select('B8')
        swir = image.select('B11')
        ndmi = nir.subtract(swir).divide(nir.add(swir)).rename('NDMI')
        
        # Calculate MSI (Moisture Stress Index)
        # MSI = SWIR / NIR (lower values = more moisture)
        msi = swir.divide(nir).rename('MSI')
        
        # Get statistics
        ndmi_stats = ndmi.reduceRegion(
            reducer=ee.Reducer.mean().combine(ee.Reducer.minMax(), '', True),
            geometry=aoi,
            scale=10,
            maxPixels=1e9
        )
        
        msi_stats = msi.reduceRegion(
            reducer=ee.Reducer.mean().combine(ee.Reducer.minMax(), '', True),
            geometry=aoi,
            scale=10,
            maxPixels=1e9
        )
        
        ndmi_info = ndmi_stats.getInfo()
        msi_info = msi_stats.getInfo()
        
        mean_ndmi = ndmi_info.get('NDMI_mean', 0)
        mean_msi = msi_info.get('MSI_mean', 0)
        
        return {
            'ndmi_image': ndmi,
            'msi_image': msi,
            'mean_ndmi': mean_ndmi,
            'min_ndmi': ndmi_info.get('NDMI_min', 0),
            'max_ndmi': ndmi_info.get('NDMI_max', 0),
            'mean_msi': mean_msi,
            'min_msi': msi_info.get('MSI_min', 0),
            'max_msi': msi_info.get('MSI_max', 0),
            'moisture_status': self._classify_moisture(mean_ndmi, mean_msi)
        }
    
    def _classify_moisture(self, ndmi, msi):
        """Classify soil moisture status"""
        if ndmi > 0.4 or msi < 0.5:
            return 'High Moisture'
        elif ndmi > 0.2 or msi < 0.8:
            return 'Moderate Moisture'
        elif ndmi > 0 or msi < 1.2:
            return 'Low Moisture'
        else:
            return 'Very Dry'
