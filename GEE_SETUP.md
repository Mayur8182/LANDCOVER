# Google Earth Engine Setup Guide

Quick guide to set up Google Earth Engine for this project.

## Step 1: Install earthengine-api

```bash
pip install earthengine-api
```

Optional (for advanced features):
```bash
pip install geemap
```

## Step 2: Authenticate

### Method 1: Command Line (Recommended)
```bash
earthengine authenticate
```

This will:
1. Open your browser
2. Ask you to sign in with Google
3. Give you an authorization code
4. Paste the code back in terminal

### Method 2: Python Script
```python
import ee
ee.Authenticate()
```

## Step 3: Initialize Connection

### In Python:
```python
import ee
ee.Initialize()
```

### Test if it works:
```python
import ee
ee.Initialize()

# Test with a simple query
image = ee.ImageCollection('COPERNICUS/S2_SR').first()
print("Success! GEE is working.")
```

## Step 4: Run Test Script

We've provided a comprehensive test script:

```bash
python gee_connect_test.py
```

This will:
- ✓ Check if earthengine-api is installed
- ✓ Verify authentication
- ✓ Test GEE connection
- ✓ Fetch sample satellite data
- ✓ Calculate NDVI
- ✓ Confirm everything is working

## Common Issues

### Issue 1: "Please authenticate"
```bash
# Solution:
earthengine authenticate --force
```

### Issue 2: "Project not found"
```bash
# Solution: Initialize with project ID
earthengine authenticate --project=your-project-id
```

Or in Python:
```python
import ee
ee.Initialize(project='your-project-id')
```

### Issue 3: "Module not found: ee"
```bash
# Solution:
pip install earthengine-api
```

### Issue 4: "Computation timed out"
```python
# Solution: Use smaller areas or increase timeout
# This usually happens with large areas
```

## Verify Installation

Run this quick test:

```python
import ee

# Authenticate (first time only)
# ee.Authenticate()

# Initialize
ee.Initialize()

# Test
point = ee.Geometry.Point([77.2090, 28.6139])  # Delhi
collection = ee.ImageCollection('COPERNICUS/S2_SR') \
    .filterBounds(point) \
    .filterDate('2023-01-01', '2023-12-31')

count = collection.size().getInfo()
print(f"Found {count} images - GEE is working!")
```

## Usage in This Project

The project uses GEE in `backend/gee_handler.py`:

```python
from backend.gee_handler import GEEHandler

handler = GEEHandler()

# Search location
coords = handler.search_location("Mumbai, India")

# Fetch satellite data
bounds = {
    'north': 19.2,
    'south': 18.9,
    'east': 73.0,
    'west': 72.7
}
data = handler.fetch_satellite_data(bounds, '2023-01-01', '2023-12-31')
```

## GEE Account Types

### Free Tier (Non-commercial)
- ✓ Perfect for this project
- ✓ Sufficient quota for testing
- ✓ Access to all datasets
- ✓ Sign up at: https://earthengine.google.com/

### Commercial Tier
- For production/commercial use
- Higher quotas
- SLA support
- Contact Google for pricing

## Quota Limits

Free tier limits:
- Concurrent requests: Limited
- Storage: Limited
- Processing: Fair use policy

Tips to stay within limits:
1. Process smaller areas
2. Use appropriate date ranges
3. Cache results when possible
4. Don't make too many requests quickly

## Datasets Used

This project uses:
- **COPERNICUS/S2_SR**: Sentinel-2 Surface Reflectance
  - Resolution: 10m
  - Bands: RGB, NIR, SWIR
  - Global coverage
  - Updated regularly

## Additional Resources

- GEE Documentation: https://developers.google.com/earth-engine
- GEE Data Catalog: https://developers.google.com/earth-engine/datasets
- GEE Python API: https://developers.google.com/earth-engine/guides/python_install
- Community Forum: https://groups.google.com/g/google-earth-engine-developers

## Quick Reference

### Authentication
```bash
earthengine authenticate
```

### Test Connection
```bash
python gee_connect_test.py
```

### In Code
```python
import ee
ee.Initialize()
```

## Troubleshooting Checklist

- [ ] earthengine-api installed (`pip list | grep earthengine`)
- [ ] Authenticated (`earthengine authenticate`)
- [ ] Can import ee (`python -c "import ee; print('OK')"`)
- [ ] Can initialize (`python -c "import ee; ee.Initialize(); print('OK')"`)
- [ ] Test script passes (`python gee_connect_test.py`)

## Next Steps

After GEE is set up:
1. ✓ Install other dependencies: `pip install -r requirements.txt`
2. ✓ Set up frontend: `cd frontend && npm install`
3. ✓ Run the application: `python app.py`

---

**Need help?** Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more solutions.
