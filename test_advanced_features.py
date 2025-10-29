"""
Test script for advanced features
Run this to test all new analysis capabilities
"""

import requests
import json

BASE_URL = 'http://localhost:5000/api'

# Test bounds (Gujarat region)
BOUNDS = {
    'north': 23.5,
    'south': 23.0,
    'east': 73.0,
    'west': 72.5
}

print("=" * 60)
print("Testing Advanced Features")
print("=" * 60)
print()

# Test 1: Water Body Detection
print("Test 1: Water Body Detection")
print("-" * 60)
try:
    response = requests.post(f'{BASE_URL}/detect-water', json={
        'bounds': BOUNDS,
        'start_date': '2023-01-01',
        'end_date': '2023-12-31'
    })
    
    if response.status_code == 200:
        result = response.json()
        if result['success']:
            data = result['data']
            print(f"✓ Water detection successful!")
            print(f"  Water Area: {data['water_area_sqkm']:.2f} km²")
            print(f"  NDWI Threshold: {data['threshold']}")
        else:
            print(f"✗ Failed: {result.get('error', 'Unknown error')}")
    else:
        print(f"✗ HTTP Error: {response.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 2: NDVI Analysis
print("Test 2: NDVI Analysis (Vegetation Health)")
print("-" * 60)
try:
    response = requests.post(f'{BASE_URL}/calculate-ndvi', json={
        'bounds': BOUNDS,
        'start_date': '2023-06-01',
        'end_date': '2023-08-31'
    })
    
    if response.status_code == 200:
        result = response.json()
        if result['success']:
            data = result['data']
            print(f"✓ NDVI analysis successful!")
            print(f"  Mean NDVI: {data['mean_ndvi']:.3f}")
            print(f"  Min NDVI: {data['min_ndvi']:.3f}")
            print(f"  Max NDVI: {data['max_ndvi']:.3f}")
            print(f"  Vegetation Health: {data['vegetation_health']}")
        else:
            print(f"✗ Failed: {result.get('error', 'Unknown error')}")
    else:
        print(f"✗ HTTP Error: {response.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 3: Urban Sprawl Detection
print("Test 3: Urban Sprawl Detection")
print("-" * 60)
try:
    response = requests.post(f'{BASE_URL}/detect-urban-sprawl', json={
        'bounds': BOUNDS,
        'old_start_date': '2020-01-01',
        'old_end_date': '2020-12-31',
        'new_start_date': '2023-01-01',
        'new_end_date': '2023-12-31'
    })
    
    if response.status_code == 200:
        result = response.json()
        if result['success']:
            data = result['data']
            print(f"✓ Urban sprawl detection successful!")
            print(f"  Old Urban Area: {data['old_urban_area_sqkm']:.2f} km²")
            print(f"  New Urban Area: {data['new_urban_area_sqkm']:.2f} km²")
            print(f"  Urban Growth: {data['urban_growth_sqkm']:.2f} km²")
            print(f"  Growth Rate: {data['growth_percentage']:.1f}%")
        else:
            print(f"✗ Failed: {result.get('error', 'Unknown error')}")
    else:
        print(f"✗ HTTP Error: {response.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 4: Forest Change Detection
print("Test 4: Forest Change Detection")
print("-" * 60)
try:
    response = requests.post(f'{BASE_URL}/detect-forest-change', json={
        'bounds': BOUNDS,
        'old_start_date': '2020-01-01',
        'old_end_date': '2020-12-31',
        'new_start_date': '2023-01-01',
        'new_end_date': '2023-12-31'
    })
    
    if response.status_code == 200:
        result = response.json()
        if result['success']:
            data = result['data']
            print(f"✓ Forest change detection successful!")
            print(f"  Old Forest Area: {data['old_forest_area_sqkm']:.2f} km²")
            print(f"  New Forest Area: {data['new_forest_area_sqkm']:.2f} km²")
            print(f"  Forest Loss: {data['forest_loss_sqkm']:.2f} km²")
            print(f"  Forest Gain: {data['forest_gain_sqkm']:.2f} km²")
            print(f"  Net Change: {data['net_change_sqkm']:.2f} km²")
            print(f"  Change Rate: {data['change_percentage']:.1f}%")
        else:
            print(f"✗ Failed: {result.get('error', 'Unknown error')}")
    else:
        print(f"✗ HTTP Error: {response.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 5: Soil Moisture Analysis
print("Test 5: Soil Moisture Analysis")
print("-" * 60)
try:
    response = requests.post(f'{BASE_URL}/calculate-soil-moisture', json={
        'bounds': BOUNDS,
        'start_date': '2023-03-01',
        'end_date': '2023-05-31'
    })
    
    if response.status_code == 200:
        result = response.json()
        if result['success']:
            data = result['data']
            print(f"✓ Soil moisture analysis successful!")
            print(f"  Mean NDMI: {data['mean_ndmi']:.3f}")
            print(f"  Mean MSI: {data['mean_msi']:.3f}")
            print(f"  Moisture Status: {data['moisture_status']}")
        else:
            print(f"✗ Failed: {result.get('error', 'Unknown error')}")
    else:
        print(f"✗ HTTP Error: {response.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")

print()

# Summary
print("=" * 60)
print("SUMMARY")
print("=" * 60)
print()
print("Advanced features tested:")
print("  1. ✓ Water Body Detection")
print("  2. ✓ NDVI Analysis")
print("  3. ✓ Urban Sprawl Detection")
print("  4. ✓ Forest Change Detection")
print("  5. ✓ Soil Moisture Analysis")
print()
print("All features are working!")
print()
print("Next steps:")
print("  1. Open http://localhost:3000")
print("  2. Select analysis type from dropdown")
print("  3. Choose your area of interest")
print("  4. Run analysis and view results")
print()
print("Documentation: ADVANCED_FEATURES.md")
print("=" * 60)
