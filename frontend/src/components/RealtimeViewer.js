import React, { useState, useEffect } from 'react';
import './RealtimeViewer.css';
import io from 'socket.io-client';

const RealtimeViewer = ({ sessionId, onComplete }) => {
  const [progress, setProgress] = useState([]);
  const [currentStage, setCurrentStage] = useState('');
  const [currentProgress, setCurrentProgress] = useState(0);
  const [isComplete, setIsComplete] = useState(false);
  const [result, setResult] = useState(null);
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    // Connect to WebSocket
    const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
    const newSocket = io(API_URL);
    
    newSocket.on('connect', () => {
      console.log('Connected to server');
      newSocket.emit('join_session', { session_id: sessionId });
    });

    newSocket.on('training_progress', (update) => {
      console.log('Progress update:', update);
      setProgress(prev => [...prev, update]);
      setCurrentStage(update.stage);
      setCurrentProgress(update.progress);
    });

    newSocket.on('training_complete', (data) => {
      console.log('Training complete:', data);
      setIsComplete(true);
      setResult(data.result);
      if (onComplete) {
        onComplete(data.result);
      }
    });

    newSocket.on('training_error', (data) => {
      console.error('Training error:', data);
      alert(`Error: ${data.error}`);
    });

    setSocket(newSocket);

    return () => {
      newSocket.disconnect();
    };
  }, [sessionId, onComplete]);

  const getStageIcon = (stage) => {
    const icons = {
      'loading': '📥',
      'labeling': '🏷️',
      'splitting': '✂️',
      'training': '🤖',
      'classifying': '🗺️',
      'saving': '💾',
      'tiles': '🎨',
      'complete': '✅'
    };
    return icons[stage] || '⏳';
  };

  const getStageColor = (stage) => {
    const colors = {
      'loading': '#3498db',
      'labeling': '#9b59b6',
      'splitting': '#e67e22',
      'training': '#e74c3c',
      'classifying': '#2ecc71',
      'saving': '#1abc9c',
      'tiles': '#f39c12',
      'complete': '#27ae60'
    };
    return colors[stage] || '#95a5a6';
  };

  return (
    <div className="realtime-viewer">
      <div className="viewer-header">
        <h2>🔴 Live Training Progress</h2>
        <div className="session-id">Session: {sessionId}</div>
      </div>

      <div className="current-stage">
        <div className="stage-icon" style={{ color: getStageColor(currentStage) }}>
          {getStageIcon(currentStage)}
        </div>
        <div className="stage-info">
          <div className="stage-name">{currentStage.toUpperCase()}</div>
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{ 
                width: `${currentProgress}%`,
                backgroundColor: getStageColor(currentStage)
              }}
            />
          </div>
          <div className="progress-text">{currentProgress}%</div>
        </div>
      </div>

      <div className="progress-log">
        <h3>Progress Log</h3>
        <div className="log-entries">
          {progress.map((entry, index) => (
            <div key={index} className="log-entry">
              <span className="log-icon">{getStageIcon(entry.stage)}</span>
              <span className="log-stage">[{entry.stage}]</span>
              <span className="log-progress">{entry.progress}%</span>
              <span className="log-message">{entry.message}</span>
              <span className="log-time">
                {new Date(entry.timestamp).toLocaleTimeString()}
              </span>
            </div>
          ))}
        </div>
      </div>

      {isComplete && result && (
        <div className="completion-summary">
          <h3>✅ Training Complete!</h3>
          
          {result.metrics && (
            <div className="metrics-grid">
              <div className="metric-card">
                <div className="metric-label">Accuracy</div>
                <div className="metric-value">
                  {(result.metrics.accuracy * 100).toFixed(1)}%
                </div>
              </div>
              <div className="metric-card">
                <div className="metric-label">Precision</div>
                <div className="metric-value">
                  {(result.metrics.precision * 100).toFixed(1)}%
                </div>
              </div>
              <div className="metric-card">
                <div className="metric-label">Recall</div>
                <div className="metric-value">
                  {(result.metrics.recall * 100).toFixed(1)}%
                </div>
              </div>
              <div className="metric-card">
                <div className="metric-label">F1 Score</div>
                <div className="metric-value">
                  {(result.metrics.f1_score * 100).toFixed(1)}%
                </div>
              </div>
            </div>
          )}

          {result.classification && result.classification.class_distribution && (
            <div className="class-distribution">
              <h4>Land Cover Distribution</h4>
              {Object.entries(result.classification.class_distribution).map(([className, count]) => (
                <div key={className} className="class-item">
                  <span className="class-name">{className}</span>
                  <span className="class-count">{count.toLocaleString()} pixels</span>
                </div>
              ))}
            </div>
          )}

          <button 
            className="view-map-btn"
            onClick={() => window.open(`/map-viewer?tile=${result.visualization.tile_path}`, '_blank')}
          >
            🗺️ View Classification Map
          </button>
        </div>
      )}
    </div>
  );
};

export default RealtimeViewer;
