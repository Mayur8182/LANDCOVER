import React, { useState } from 'react';
import './ControlPanel.css';

const ControlPanel = ({ onProcess, onLocationSearch, loading }) => {
  const [locationName, setLocationName] = useState('');
  const [startDate, setStartDate] = useState('2023-01-01');
  const [endDate, setEndDate] = useState('2023-12-31');
  const [modelType, setModelType] = useState('random_forest');
  const [datasetType, setDatasetType] = useState('sentinel');
  const [analysisType, setAnalysisType] = useState('classification');

  const handleSearch = async () => {
    if (locationName.trim()) {
      const coords = await onLocationSearch(locationName);
      if (coords) {
        alert(`Found: ${coords.display_name}\nLat: ${coords.lat}, Lon: ${coords.lon}`);
      }
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onProcess({
      startDate,
      endDate,
      modelType,
      datasetType,
      analysisType
    });
  };

  return (
    <div className="control-panel">
      <h2>Control Panel</h2>
      
      <div className="section">
        <h3>📍 Search Location</h3>
        <div className="input-group">
          <input
            type="text"
            placeholder="Enter city, district, or place name"
            value={locationName}
            onChange={(e) => setLocationName(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
          />
          <button onClick={handleSearch} className="btn-secondary">
            Search
          </button>
        </div>
        <p className="hint">Or draw a rectangle/polygon on the map</p>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="section">
          <h3>📊 Analysis Type</h3>
          <select 
            value={analysisType} 
            onChange={(e) => setAnalysisType(e.target.value)}
            className="model-select"
          >
            <option value="classification">Land Cover Classification</option>
            <option value="water">Water Body Detection</option>
            <option value="ndvi">NDVI Analysis (Vegetation)</option>
            <option value="urban">Urban Sprawl Detection</option>
            <option value="forest">Forest Change Detection</option>
            <option value="moisture">Soil Moisture Analysis</option>
          </select>
          <p className="hint">
            {analysisType === 'classification' && 'Classify land into different cover types'}
            {analysisType === 'water' && 'Detect and map water bodies'}
            {analysisType === 'ndvi' && 'Analyze vegetation health'}
            {analysisType === 'urban' && 'Track city growth over time'}
            {analysisType === 'forest' && 'Monitor forest cover changes'}
            {analysisType === 'moisture' && 'Estimate soil moisture levels'}
          </p>
        </div>

        <div className="section">
          <h3>📅 Date Range</h3>
          <div className="date-inputs">
            <div className="input-group">
              <label>Start Date</label>
              <input
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                required
              />
            </div>
            <div className="input-group">
              <label>End Date</label>
              <input
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                required
              />
            </div>
          </div>
        </div>

        <div className="section">
          <h3>🛰️ Dataset Type</h3>
          <select 
            value={datasetType} 
            onChange={(e) => setDatasetType(e.target.value)}
            className="model-select"
          >
            <option value="sentinel">Sentinel-2 (10m resolution)</option>
            <option value="modis">MODIS Land Cover (500m resolution)</option>
          </select>
          <p className="hint">
            {datasetType === 'sentinel' 
              ? 'High resolution, requires ML classification' 
              : 'Pre-classified land cover, faster processing'}
          </p>
        </div>

        {datasetType === 'sentinel' && (
          <div className="section">
            <h3>🤖 Model Type</h3>
            <select 
              value={modelType} 
              onChange={(e) => setModelType(e.target.value)}
              className="model-select"
            >
              <option value="random_forest">Random Forest (ML)</option>
            </select>
          </div>
        )}

        <button 
          type="submit" 
          className="btn-primary"
          disabled={loading}
        >
          {loading ? '⏳ Processing...' : '🚀 Generate Land Cover Map'}
        </button>
      </form>

      <div className="info-box">
        <h4>ℹ️ How it works:</h4>
        <ol>
          <li>Select area on map or search location</li>
          <li>Choose date range for satellite imagery</li>
          <li>Select analysis type and dataset</li>
          <li>Click Generate to start processing</li>
          <li>Download classified .tif file</li>
        </ol>
      </div>
    </div>
  );
};

export default ControlPanel;
