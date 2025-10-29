import React from 'react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement } from 'chart.js';
import { Pie, Bar } from 'react-chartjs-2';
import './ResultsPanel.css';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement);

const ResultsPanel = ({ results }) => {
  if (!results) {
    return null;
  }

  // Handle different result types
  const resultType = results.type || 'classification';
  
  if (resultType === 'classification' && !results.classification) {
    return null;
  }

  const { classification, imagery, analysis } = results;
  const classDistribution = classification?.classification?.class_distribution || {};
  const metrics = classification?.metrics || {};

  const pieData = {
    labels: Object.keys(classDistribution),
    datasets: [{
      data: Object.values(classDistribution),
      backgroundColor: [
        '#3498db', // Water
        '#27ae60', // Forest
        '#2ecc71', // Grassland
        '#e74c3c', // Urban
        '#95a5a6', // Barren
        '#f39c12', // Agriculture
      ],
      borderWidth: 2,
      borderColor: '#fff'
    }]
  };

  const barData = {
    labels: ['Accuracy', 'Precision', 'Recall', 'F1 Score'],
    datasets: [{
      label: 'Model Performance',
      data: [
        (metrics.accuracy * 100).toFixed(2),
        (metrics.precision * 100).toFixed(2),
        (metrics.recall * 100).toFixed(2),
        (metrics.f1_score * 100).toFixed(2)
      ],
      backgroundColor: 'rgba(102, 126, 234, 0.6)',
      borderColor: 'rgba(102, 126, 234, 1)',
      borderWidth: 2
    }]
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom'
      }
    }
  };

  const barOptions = {
    ...chartOptions,
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        ticks: {
          callback: (value) => value + '%'
        }
      }
    }
  };

  const handleDownload = () => {
    const outputPath = classification?.classification?.output_path || results.export_path;
    if (outputPath) {
      // Get just the filename, remove 'exports/' if present
      let filename = outputPath;
      if (filename.includes('/')) {
        filename = filename.split('/').pop();
      }
      
      console.log('Downloading file:', filename);
      const downloadUrl = `http://localhost:5000/api/download/${encodeURIComponent(filename)}`;
      
      // Create a temporary link and click it
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = filename;
      link.target = '_blank';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } else {
      alert('No file available for download');
    }
  };
  
  const handleViewOnMap = () => {
    // Get filename from results
    const outputPath = classification?.classification?.output_path || results.export_path;
    if (outputPath) {
      // Get just the filename, remove 'exports/' if present
      let filename = outputPath;
      if (filename.includes('/') || filename.includes('\\')) {
        filename = filename.split(/[/\\]/).pop();
      }
      
      console.log('Opening 2D map viewer for file:', filename);
      // Open map viewer with filename
      window.open(`/map-viewer.html?file=${encodeURIComponent(filename)}`, '_blank');
    } else {
      alert('No file available for map view');
    }
  };
  
  const handleView3D = () => {
    // Get filename from results
    const outputPath = classification?.classification?.output_path || results.export_path;
    if (outputPath) {
      // Get just the filename, remove 'exports/' if present
      let filename = outputPath;
      if (filename.includes('/') || filename.includes('\\')) {
        filename = filename.split(/[/\\]/).pop();
      }
      
      console.log('Opening 3D viewer for file:', filename);
      // Open 3D viewer with filename
      window.open(`/3d-viewer.html?file=${encodeURIComponent(filename)}`, '_blank');
    } else {
      alert('No file available for 3D view');
    }
  };

  // Check if we have valid class distribution data
  const hasClassData = classDistribution && Object.keys(classDistribution).length > 0;

  return (
    <div className="results-panel">
      <h2>✅ Results</h2>

      {metrics && Object.keys(metrics).length > 0 && (
        <div className="result-section">
          <h3>📊 Model Performance</h3>
          <div className="metrics-grid">
            <div className="metric-card">
              <div className="metric-value">{(metrics.accuracy * 100).toFixed(2)}%</div>
              <div className="metric-label">Accuracy</div>
            </div>
            <div className="metric-card">
              <div className="metric-value">{(metrics.precision * 100).toFixed(2)}%</div>
              <div className="metric-label">Precision</div>
            </div>
            <div className="metric-card">
              <div className="metric-value">{(metrics.recall * 100).toFixed(2)}%</div>
              <div className="metric-label">Recall</div>
            </div>
            <div className="metric-card">
              <div className="metric-value">{(metrics.f1_score * 100).toFixed(2)}%</div>
              <div className="metric-label">F1 Score</div>
            </div>
          </div>
          <div className="chart-container">
            <Bar data={barData} options={barOptions} />
          </div>
        </div>
      )}

      {hasClassData && (
        <div className="result-section">
          <h3>🗺️ Land Cover Distribution</h3>
          <div className="chart-container">
            <Pie data={pieData} options={chartOptions} />
          </div>
          <div className="class-stats">
            <table>
              <thead>
                <tr>
                  <th>Class</th>
                  <th>Pixels</th>
                  <th>Percentage</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(classDistribution).map(([className, count]) => {
                  const total = Object.values(classDistribution).reduce((a, b) => a + b, 0);
                  const percentage = ((count / total) * 100).toFixed(2);
                  return (
                    <tr key={className}>
                      <td>{className}</td>
                      <td>{count.toLocaleString()}</td>
                      <td>{percentage}%</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      <div className="result-section">
        <h3>📥 Actions</h3>
        <div className="action-buttons">
          <button onClick={handleViewOnMap} className="view-map-btn">
            🗺️ View 2D Map
          </button>
          <button onClick={handleView3D} className="view-map-btn" style={{background: '#9b59b6'}}>
            🌍 View 3D Globe
          </button>
          <button onClick={handleDownload} className="download-btn">
            ⬇️ Download Results (.tif)
          </button>
        </div>
        {imagery && (
          <div className="file-info">
            <p><strong>Dataset:</strong> {imagery.dataset || 'Sentinel-2'}</p>
            <p><strong>Date Range:</strong> {imagery.date_range?.start} to {imagery.date_range?.end}</p>
            {imagery.cloud_cover && (
              <p><strong>Avg Cloud Cover:</strong> {imagery.cloud_cover.toFixed(2)}%</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ResultsPanel;
