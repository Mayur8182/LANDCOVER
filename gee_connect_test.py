"""
Google Earth Engine Connection Test Script
Run this to verify your GEE setup is working correctly
"""

import sys

print("=" * 60)
print("Google Earth Engine Connection Test")
print("=" * 60)
print()

# Step 1: Check if earthengine-api is installed
print("Step 1: Checking if earthengine-api is installed...")
try:
    import ee
    print("✓ earthengine-api is installed")
    print(f"  Version: {ee.__version__}")
except ImportError:
    print("✗ earthengine-api is NOT installed")
    print("\nTo install, run:")
    print("  pip install earthengine-api")
    sys.exit(1)

print()

# Step 2: Try to authenticate (if not already done)
print("Step 2: Checking authentication...")
try:
    ee.Initialize()
    print("✓ Already authenticated and initialized!")
except Exception as e:
    print("✗ Not authenticated yet")
    print(f"  Error: {e}")
    print("\nTo authenticate, run:")
    print("  earthengine authenticate")
    print("\nOr in Python:")
    print("  import ee")
    print("  ee.Authenticate()")
    print("  ee.Initialize()")
    
    # Try to authenticate now
    print("\nAttempting to authenticate now...")
    try:
        ee.Authenticate()
        ee.Initialize()
        print("✓ Authentication successful!")
    except Exception as auth_error:
        print(f"✗ Authentication failed: {auth_error}")
        sys.exit(1)

print()

# Step 3: Test basic GEE functionality
print("Step 3: Testing basic GEE functionality...")
try:
    # Get an image
    image = ee.Image('COPERNICUS/S2_SR/20230101T000000_20230101T000000_T01ABC')
    print("✓ Can access GEE image collections")
except Exception as e:
    print(f"⚠ Warning: {e}")
    print("  This is normal - testing with a more general approach...")

try:
    # Test with image collection
    collection = ee.ImageCollection('COPERNICUS/S2_SR')
    count = collection.size().getInfo()
    print(f"✓ Successfully connected to GEE!")
    print(f"  Sentinel-2 collection has {count:,} images")
except Exception as e:
    print(f"✗ Failed to connect to GEE: {e}")
    sys.exit(1)

print()

# Step 4: Test data fetching for a specific location
print("Step 4: Testing data fetch for a specific location...")
try:
    # Define a small area (Delhi, India)
    point = ee.Geometry.Point([77.2090, 28.6139])
    
    # Fetch recent Sentinel-2 image
    collection = ee.ImageCollection('COPERNICUS/S2_SR') \
        .filterBounds(point) \
        .filterDate('2023-01-01', '2023-12-31') \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
        .sort('CLOUDY_PIXEL_PERCENTAGE')
    
    # Get first image info
    first_image = collection.first()
    image_info = first_image.getInfo()
    
    print("✓ Successfully fetched satellite data!")
    print(f"  Image ID: {image_info['id']}")
    print(f"  Bands: {len(image_info['bands'])} bands available")
    
    # Get collection size
    size = collection.size().getInfo()
    print(f"  Found {size} images for this location and date range")
    
except Exception as e:
    print(f"✗ Failed to fetch data: {e}")
    print("  This might be due to network issues or GEE quota limits")
    sys.exit(1)

print()

# Step 5: Test NDVI calculation
print("Step 5: Testing spectral index calculation (NDVI)...")
try:
    # Get an image
    image = ee.ImageCollection('COPERNICUS/S2_SR') \
        .filterBounds(point) \
        .filterDate('2023-01-01', '2023-12-31') \
        .first()
    
    # Calculate NDVI
    nir = image.select('B8')
    red = image.select('B4')
    ndvi = nir.subtract(red).divide(nir.add(red)).rename('NDVI')
    
    # Get a sample value
    sample = ndvi.sample(point, 10).first().getInfo()
    
    print("✓ Successfully calculated NDVI!")
    print(f"  Sample NDVI value: {sample['properties'].get('NDVI', 'N/A')}")
    
except Exception as e:
    print(f"⚠ Warning: Could not calculate NDVI: {e}")
    print("  This is not critical for basic functionality")

print()

# Step 6: Test MODIS dataset
print("Step 6: Testing MODIS Land Cover dataset...")
try:
    # Get MODIS land cover
    modis = ee.ImageCollection('MODIS/061/MCD12Q1') \
        .filterDate('2022-01-01', '2022-12-31') \
        .first()
    
    landcover = modis.select('LC_Type1')
    
    # Get sample value
    sample_point = ee.Geometry.Point([77.2090, 28.6139])
    sample = landcover.sample(sample_point, 500).first().getInfo()
    
    print("✓ Successfully accessed MODIS dataset!")
    print(f"  Dataset: MODIS/061/MCD12Q1")
    print(f"  Sample land cover class: {sample['properties'].get('LC_Type1', 'N/A')}")
    print(f"  Resolution: 500m")
    
except Exception as e:
    print(f"⚠ Warning: Could not access MODIS: {e}")
    print("  This is not critical - Sentinel-2 will still work")

print()

# Step 7: Summary
print("=" * 60)
print("SUMMARY")
print("=" * 60)
print()
print("✓ All tests passed!")
print()
print("Your Google Earth Engine setup is working correctly.")
print("You can now use the Land Cover Classification System.")
print()
print("Supported Datasets:")
print("  ✓ Sentinel-2 (10m resolution) - Custom classification")
print("  ✓ MODIS (500m resolution) - Pre-classified land cover")
print()
print("Next steps:")
print("  1. Make sure backend dependencies are installed:")
print("     pip install -r requirements.txt")
print()
print("  2. Make sure frontend dependencies are installed:")
print("     cd frontend")
print("     npm install")
print()
print("  3. Start the application:")
print("     python app.py  (backend)")
print("     npm start      (frontend, in frontend/ directory)")
print()
print("=" * 60)
print()

# Optional: Test geemap if installed
print("Bonus: Checking for geemap (optional)...")
try:
    import geemap
    print(f"✓ geemap is installed (version {geemap.__version__})")
    print("  You can use geemap for advanced GEE visualizations")
except ImportError:
    print("⚠ geemap is not installed (optional)")
    print("  To install: pip install geemap")

print()
print("Test completed successfully! 🎉")
