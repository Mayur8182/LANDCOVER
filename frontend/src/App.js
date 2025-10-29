import React, { useState } from 'react';
import './App.css';
import MapSelector from './components/MapSelector';
import ControlPanel from './components/ControlPanel';
import ResultsPanel from './components/ResultsPanel';
import axios from 'axios';

function App() {
  const [selectedBounds, setSelectedBounds] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleProcess = async (params) => {
    if (!selectedBounds) {
      setError('Please select an area on the map first');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await axios.post('/api/process-complete', {
        bounds: selectedBounds,
        start_date: params.startDate,
        end_date: params.endDate,
        model_type: params.modelType,
        dataset_type: params.datasetType || 'sentinel'
      });

      if (response.data.success) {
        setResults(response.data);
      } else {
        setError(response.data.error || 'Processing failed');
      }
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleLocationSearch = async (locationName) => {
    try {
      const response = await axios.post('/api/search-location', {
        location: locationName
      });

      if (response.data.success) {
        return response.data.coordinates;
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Location not found');
      return null;
    }
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>🛰️ Land Use/Land Cover Classification System</h1>
        <p>Select area, fetch satellite data, and classify land cover automatically</p>
      </header>

      <div className="app-container">
        <div className="left-panel">
          <ControlPanel 
            onProcess={handleProcess}
            onLocationSearch={handleLocationSearch}
            loading={loading}
          />
          {error && (
            <div className="error-message">
              <strong>Error:</strong> {error}
            </div>
          )}
          {results && <ResultsPanel results={results} />}
        </div>

        <div className="right-panel">
          <MapSelector 
            onBoundsChange={setSelectedBounds}
            searchCoordinates={null}
          />
        </div>
      </div>
    </div>
  );
}

export default App;
