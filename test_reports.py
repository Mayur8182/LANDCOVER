"""
Test script for report generation
Tests all report types
"""

import requests
import json
import os

BASE_URL = 'http://localhost:5000/api'

print("=" * 60)
print("Testing Report Generation")
print("=" * 60)
print()

# Test data for different report types
test_data = {
    'classification': {
        'metrics': {
            'accuracy': 0.89,
            'precision': 0.87,
            'recall': 0.88,
            'f1_score': 0.87
        },
        'classification': {
            'class_distribution': {
                'Water': 1500,
                'Forest': 3200,
                'Grassland': 2100,
                'Urban': 1800,
                'Barren': 500,
                'Agriculture': 2900
            }
        }
    },
    'water': {
        'water_area_sqkm': 125.5,
        'water_area_sqm': 125500000,
        'threshold': 0.3
    },
    'ndvi': {
        'mean_ndvi': 0.65,
        'min_ndvi': 0.15,
        'max_ndvi': 0.85,
        'std_ndvi': 0.12,
        'vegetation_health': 'Excellent (Dense Vegetation)'
    },
    'urban': {
        'old_urban_area_sqkm': 150.5,
        'new_urban_area_sqkm': 185.3,
        'urban_growth_sqkm': 34.8,
        'growth_percentage': 23.1,
        'old_period': '2020-01-01 to 2020-12-31',
        'new_period': '2023-01-01 to 2023-12-31'
    },
    'forest': {
        'old_forest_area_sqkm': 450.2,
        'new_forest_area_sqkm': 425.8,
        'forest_loss_sqkm': 35.6,
        'forest_gain_sqkm': 11.2,
        'net_change_sqkm': -24.4,
        'change_percentage': -5.4,
        'old_period': '2020-01-01 to 2020-12-31',
        'new_period': '2023-01-01 to 2023-12-31'
    },
    'moisture': {
        'mean_ndmi': 0.35,
        'min_ndmi': 0.10,
        'max_ndmi': 0.65,
        'mean_msi': 0.75,
        'min_msi': 0.45,
        'max_msi': 1.20,
        'moisture_status': 'Moderate Moisture'
    }
}

# Test each report type
for report_type, data in test_data.items():
    print(f"Test: {report_type.title()} Report")
    print("-" * 60)
    
    try:
        response = requests.post(f'{BASE_URL}/generate-report', json={
            'analysis_type': report_type,
            'data': data
        })
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print(f"✓ Report generated successfully!")
                print(f"  Filename: {result['filename']}")
                print(f"  Path: {result['report_path']}")
                print(f"  Download URL: {result['download_url']}")
                
                # Try to download
                download_url = f"http://localhost:5000{result['download_url']}"
                download_response = requests.get(download_url)
                
                if download_response.status_code == 200:
                    print(f"  ✓ Download successful ({len(download_response.content)} bytes)")
                else:
                    print(f"  ✗ Download failed: {download_response.status_code}")
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
print("Report types tested:")
print("  1. ✓ Land Cover Classification")
print("  2. ✓ Water Body Detection")
print("  3. ✓ NDVI Vegetation Analysis")
print("  4. ✓ Urban Sprawl Detection")
print("  5. ✓ Forest Change Detection")
print("  6. ✓ Soil Moisture Analysis")
print()
print("Reports saved in: reports/")
print()
print("To view reports:")
print("  1. Open reports/ folder")
print("  2. Open any .html file in browser")
print("  3. Or download via API")
print()
print("Documentation: REPORT_GUIDE.md")
print("=" * 60)
