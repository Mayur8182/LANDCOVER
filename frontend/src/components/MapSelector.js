import React, { useState, useRef } from 'react';
import { MapContainer, TileLayer, FeatureGroup } from 'react-leaflet';
import { EditControl } from 'react-leaflet-draw';
import 'leaflet/dist/leaflet.css';
import 'leaflet-draw/dist/leaflet.draw.css';
import './MapSelector.css';

const MapSelector = ({ onBoundsChange }) => {
  const [center] = useState([20.5937, 78.9629]); // India center
  const mapRef = useRef();

  const handleCreated = (e) => {
    const layer = e.layer;
    const bounds = layer.getBounds();
    
    const boundsData = {
      north: bounds.getNorth(),
      south: bounds.getSouth(),
      east: bounds.getEast(),
      west: bounds.getWest()
    };
    
    onBoundsChange(boundsData);
  };

  const handleEdited = (e) => {
    const layers = e.layers;
    layers.eachLayer((layer) => {
      const bounds = layer.getBounds();
      const boundsData = {
        north: bounds.getNorth(),
        south: bounds.getSouth(),
        east: bounds.getEast(),
        west: bounds.getWest()
      };
      onBoundsChange(boundsData);
    });
  };

  const handleDeleted = () => {
    onBoundsChange(null);
  };

  return (
    <div className="map-selector">
      <MapContainer
        center={center}
        zoom={5}
        style={{ height: '100%', width: '100%' }}
        ref={mapRef}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        />
        
        <FeatureGroup>
          <EditControl
            position="topright"
            onCreated={handleCreated}
            onEdited={handleEdited}
            onDeleted={handleDeleted}
            draw={{
              rectangle: true,
              polygon: true,
              circle: false,
              circlemarker: false,
              marker: false,
              polyline: false
            }}
          />
        </FeatureGroup>
      </MapContainer>
    </div>
  );
};

export default MapSelector;
