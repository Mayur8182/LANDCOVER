# 📄 Report Generation Guide

## 🎯 Overview

Aapka system ab professional HTML reports generate kar sakta hai with:
- 📊 Charts and graphs
- 📈 Statistics tables
- 🗺️ Analysis results
- 📝 Detailed metadata
- 🎨 Professional styling

---

## 🚀 How to Generate Reports

### Method 1: Via API

```python
import requests

# After running analysis, generate report
response = requests.post('http://localhost:5000/api/generate-report', json={
    'analysis_type': 'water',  # or 'ndvi', 'urban', 'forest', 'moisture', 'classification'
    'data': {
        'water_area_sqkm': 125.5,
        'threshold': 0.3,
        # ... other analysis results
    }
})

result = response.json()
if result['success']:
    print(f"Report generated: {result['filename']}")
    print(f"Download URL: {result['download_url']}")
```

### Method 2: Programmatically

```python
from backend.report_generator import ReportGenerator

generator = ReportGenerator()

# Generate report
report_path = generator.generate_html_report(
    analysis_data={
        'water_area_sqkm': 125.5,
        'threshold': 0.3
    },
    analysis_type='water'
)

print(f"Report saved to: {report_path}")
```

---

## 📊 Report Types

### 1. Land Cover Classification Report
```python
data = {
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
}

report = generator.generate_html_report(data, 'classification')
```

**Report Includes:**
- Model performance metrics
- Accuracy, Precision, Recall, F1-Score
- Land cover distribution pie chart
- Class-wise statistics table
- Percentage breakdown

---

### 2. Water Body Detection Report
```python
data = {
    'water_area_sqkm': 125.5,
    'water_area_sqm': 125500000,
    'threshold': 0.3
}

report = generator.generate_html_report(data, 'water')
```

**Report Includes:**
- Water area in km²
- NDWI threshold used
- Analysis methodology
- Formula and bands used

---

### 3. NDVI Vegetation Report
```python
data = {
    'mean_ndvi': 0.65,
    'min_ndvi': 0.15,
    'max_ndvi': 0.85,
    'std_ndvi': 0.12,
    'vegetation_health': 'Excellent (Dense Vegetation)'
}

report = generator.generate_html_report(data, 'ndvi')
```

**Report Includes:**
- Mean, Min, Max NDVI values
- Vegetation health classification
- NDVI classification table
- Health status interpretation

---

### 4. Urban Sprawl Report
```python
data = {
    'old_urban_area_sqkm': 150.5,
    'new_urban_area_sqkm': 185.3,
    'urban_growth_sqkm': 34.8,
    'growth_percentage': 23.1,
    'old_period': '2020-01-01 to 2020-12-31',
    'new_period': '2023-01-01 to 2023-12-31'
}

report = generator.generate_html_report(data, 'urban')
```

**Report Includes:**
- Old and new urban areas
- Urban growth in km²
- Growth percentage
- Time period comparison
- NDBI methodology

---

### 5. Forest Change Report
```python
data = {
    'old_forest_area_sqkm': 450.2,
    'new_forest_area_sqkm': 425.8,
    'forest_loss_sqkm': 35.6,
    'forest_gain_sqkm': 11.2,
    'net_change_sqkm': -24.4,
    'change_percentage': -5.4,
    'old_period': '2020-01-01 to 2020-12-31',
    'new_period': '2023-01-01 to 2023-12-31'
}

report = generator.generate_html_report(data, 'forest')
```

**Report Includes:**
- Old and new forest areas
- Forest loss and gain
- Net change calculation
- Change percentage
- Time period comparison

---

### 6. Soil Moisture Report
```python
data = {
    'mean_ndmi': 0.35,
    'min_ndmi': 0.10,
    'max_ndmi': 0.65,
    'mean_msi': 0.75,
    'min_msi': 0.45,
    'max_msi': 1.20,
    'moisture_status': 'Moderate Moisture'
}

report = generator.generate_html_report(data, 'moisture')
```

**Report Includes:**
- NDMI and MSI values
- Moisture status classification
- Moisture classification table
- Status interpretation

---

## 🎨 Report Features

### Professional Styling
- ✅ Modern, clean design
- ✅ Responsive layout
- ✅ Print-friendly
- ✅ Color-coded sections
- ✅ Professional typography

### Visual Elements
- ✅ Pie charts for distributions
- ✅ Info cards with key metrics
- ✅ Statistics tables
- ✅ Color-coded indicators
- ✅ Gradient backgrounds

### Content Sections
- ✅ Header with title and date
- ✅ Key metrics in cards
- ✅ Detailed statistics
- ✅ Methodology explanation
- ✅ Analysis metadata
- ✅ Professional footer

---

## 📥 Downloading Reports

### Via API
```python
import requests

# Download report
response = requests.get('http://localhost:5000/api/download-report/report_water_20231201_120000.html')

with open('my_report.html', 'wb') as f:
    f.write(response.content)
```

### Via Browser
```
http://localhost:5000/api/download-report/report_water_20231201_120000.html
```

---

## 🔧 Customization

### Custom Colors
Edit `backend/report_generator.py`:

```python
self.class_colors = {
    'Water': '#your_color',
    'Forest': '#your_color',
    # ... etc
}
```

### Custom Styling
Modify the CSS in `_create_html_content()` method.

### Custom Charts
Add new chart types in `_create_pie_chart()` or create new methods.

---

## 📊 Complete Workflow Example

```python
import requests

# 1. Run water detection analysis
analysis_response = requests.post('http://localhost:5000/api/detect-water', json={
    'bounds': {
        'north': 23.5,
        'south': 23.0,
        'east': 73.0,
        'west': 72.5
    },
    'start_date': '2023-01-01',
    'end_date': '2023-12-31'
})

analysis_data = analysis_response.json()['data']

# 2. Generate report
report_response = requests.post('http://localhost:5000/api/generate-report', json={
    'analysis_type': 'water',
    'data': analysis_data
})

report_info = report_response.json()

# 3. Download report
if report_info['success']:
    filename = report_info['filename']
    download_url = f"http://localhost:5000{report_info['download_url']}"
    
    print(f"Report generated: {filename}")
    print(f"Download from: {download_url}")
    
    # Download
    report_content = requests.get(download_url)
    with open(f'my_{filename}', 'wb') as f:
        f.write(report_content.content)
    
    print("Report downloaded successfully!")
```

---

## 📁 Report Storage

Reports are saved in:
```
reports/
├── report_classification_20231201_120000.html
├── report_water_20231201_120500.html
├── report_ndvi_20231201_121000.html
├── report_urban_20231201_121500.html
├── report_forest_20231201_122000.html
└── report_moisture_20231201_122500.html
```

---

## 🎯 Use Cases

### 1. Project Documentation
Generate reports for each analysis to document your project progress.

### 2. Client Presentations
Professional reports for presenting results to clients or stakeholders.

### 3. Research Papers
Include generated reports as supplementary material in research.

### 4. Monitoring Programs
Regular reports for environmental monitoring programs.

### 5. Compliance Reporting
Generate reports for regulatory compliance and audits.

---

## 📝 Report Sections Explained

### Header Section
- Project title
- Analysis type
- Generation date and time

### Metrics Section
- Key performance indicators
- Color-coded cards
- Large, readable numbers

### Charts Section
- Visual representation of data
- Pie charts for distributions
- Bar charts for comparisons

### Statistics Table
- Detailed breakdown
- Sortable columns
- Percentage calculations

### Metadata Section
- Analysis methodology
- Formulas used
- Bands and thresholds
- Time periods

### Footer Section
- System information
- Copyright notice
- Generation timestamp

---

## 🖨️ Printing Reports

Reports are print-optimized:
1. Open report in browser
2. Press `Ctrl+P` (Windows) or `Cmd+P` (Mac)
3. Select printer or "Save as PDF"
4. Print/Save

Print settings automatically:
- Remove shadows
- Optimize spacing
- Maintain colors
- Preserve layout

---

## 🌟 Advanced Features

### Summary Reports
Generate summary of multiple analyses:

```python
from backend.report_generator import ReportGenerator

generator = ReportGenerator()

analyses = [
    {
        'type': 'water',
        'date': '2023-12-01',
        'location': 'Sardar Sarovar Dam',
        'summary': 'Water area: 125.5 km²'
    },
    {
        'type': 'ndvi',
        'date': '2023-12-02',
        'location': 'Agricultural Area',
        'summary': 'Vegetation health: Excellent'
    }
]

summary_report = generator.generate_summary_report('Gujarat Project', analyses)
print(f"Summary report: {summary_report}")
```

---

## 🔍 Report Quality

### High-Quality Output
- ✅ 150 DPI charts
- ✅ Vector-quality text
- ✅ Professional fonts
- ✅ Optimized file size

### Browser Compatibility
- ✅ Chrome
- ✅ Firefox
- ✅ Safari
- ✅ Edge

### Mobile Responsive
- ✅ Adapts to screen size
- ✅ Touch-friendly
- ✅ Readable on mobile

---

## 📞 Support

For report generation issues:
1. Check `reports/` directory exists
2. Verify matplotlib is installed
3. Check analysis data format
4. Review error messages

---

## 🎉 Summary

Your system can now generate:
- ✅ Professional HTML reports
- ✅ 6 different report types
- ✅ Charts and visualizations
- ✅ Detailed statistics
- ✅ Print-ready documents
- ✅ Downloadable files

**Start generating reports!** 📊

```python
# Quick test
import requests

response = requests.post('http://localhost:5000/api/generate-report', json={
    'analysis_type': 'water',
    'data': {'water_area_sqkm': 125.5, 'threshold': 0.3}
})

print(response.json())
```

**Happy Reporting!** 📄✨
