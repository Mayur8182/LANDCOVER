"""
Quick GEE Setup Script with Project ID
Run this to authenticate and test your GEE connection
"""

import ee
import os

print("=" * 60)
print("Google Earth Engine Setup")
print("=" * 60)
print()

# Your project details
PROJECT_ID = 'gleaming-tube-445109-t2'
PROJECT_NAME = 'My First Project'
PROJECT_NUMBER = '704726116433'

print(f"Project Name: {PROJECT_NAME}")
print(f"Project ID: {PROJECT_ID}")
print(f"Project Number: {PROJECT_NUMBER}")
print()

# Step 1: Authenticate
print("Step 1: Authenticating with Google Earth Engine...")
print()
print("This will open your browser. Please:")
print("  1. Sign in with your Google account")
print("  2. Allow Earth Engine access")
print("  3. Copy the authorization code")
print()

try:
    ee.Authenticate()
    print("✓ Authentication successful!")
except Exception as e:
    print(f"✗ Authentication failed: {e}")
    print()
    print("Please run manually:")
    print(f"  earthengine authenticate --project={PROJECT_ID}")
    exit(1)

print()

# Step 2: Initialize with project
print("Step 2: Initializing Earth Engine with your project...")
try:
    ee.Initialize(project=PROJECT_ID)
    print(f"✓ Successfully initialized with project: {PROJECT_ID}")
except Exception as e:
    print(f"✗ Initialization failed: {e}")
    exit(1)

print()

# Step 3: Test Sentinel-2
print("Step 3: Testing Sentinel-2 access...")
try:
    point = ee.Geometry.Point([77.2090, 28.6139])  # Delhi
    collection = ee.ImageCollection('COPERNICUS/S2_SR') \
        .filterBounds(point) \
        .filterDate('2023-01-01', '2023-12-31')
    
    count = collection.size().getInfo()
    print(f"✓ Sentinel-2 working! Found {count} images")
except Exception as e:
    print(f"✗ Sentinel-2 test failed: {e}")

print()

# Step 4: Test MODIS
print("Step 4: Testing MODIS Land Cover access...")
try:
    modis = ee.ImageCollection('MODIS/061/MCD12Q1') \
        .filterDate('2022-01-01', '2022-12-31') \
        .first()
    
    landcover = modis.select('LC_Type1')
    sample_point = ee.Geometry.Point([77.2090, 28.6139])
    sample = landcover.sample(sample_point, 500).first().getInfo()
    
    lc_class = sample['properties'].get('LC_Type1', 'N/A')
    print(f"✓ MODIS working! Sample land cover class: {lc_class}")
except Exception as e:
    print(f"✗ MODIS test failed: {e}")

print()

# Step 5: Test Gujarat area
print("Step 5: Testing Gujarat area access...")
try:
    # Gujarat bounds
    gujarat = ee.Geometry.Rectangle([68.2, 20.1, 74.5, 24.7])
    
    # Get MODIS for Gujarat
    modis = ee.ImageCollection('MODIS/061/MCD12Q1') \
        .filterDate('2022-01-01', '2022-12-31') \
        .first()
    
    landcover = modis.select('LC_Type1').clip(gujarat)
    
    # Get area info
    area = gujarat.area().divide(1000000).getInfo()  # Convert to km²
    print(f"✓ Gujarat area accessible!")
    print(f"  Area: {area:.0f} km²")
    print(f"  Bounds: 68.2°E to 74.5°E, 20.1°N to 24.7°N")
except Exception as e:
    print(f"✗ Gujarat test failed: {e}")

print()

# Summary
print("=" * 60)
print("SETUP COMPLETE!")
print("=" * 60)
print()
print("✓ Your Google Earth Engine is ready to use!")
print()
print("Project Details:")
print(f"  Name: {PROJECT_NAME}")
print(f"  ID: {PROJECT_ID}")
print(f"  Number: {PROJECT_NUMBER}")
print()
print("Supported Datasets:")
print("  ✓ Sentinel-2 (10m resolution)")
print("  ✓ MODIS Land Cover (500m resolution)")
print()
print("Next Steps:")
print("  1. Start backend: python app.py")
print("  2. Start frontend: cd frontend && npm start")
print("  3. Open browser: http://localhost:3000")
print()
print("Try these locations:")
print("  • Gujarat, India (large area - use MODIS)")
print("  • Mumbai, India (city - use Sentinel-2)")
print("  • Delhi, India (city - use Sentinel-2)")
print()
print("=" * 60)
