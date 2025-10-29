"""
Real-time Model Training with Live Updates
Trains model and sends progress updates via WebSocket
"""

import numpy as np
import rasterio
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os
import json
from datetime import datetime

class RealtimeTrainer:
    def __init__(self, progress_callback=None):
        """
        Initialize real-time trainer
        progress_callback: Function to call with progress updates
        """
        self.progress_callback = progress_callback
        self.model = None
        self.class_names = ['Water', 'Forest', 'Grassland', 'Urban', 'Barren', 'Agriculture']
        self.class_colors = {
            0: [52, 152, 219],   # Water - Blue
            1: [39, 174, 96],    # Forest - Dark Green
            2: [46, 204, 113],   # Grassland - Light Green
            3: [231, 76, 60],    # Urban - Red
            4: [149, 165, 166],  # Barren - Gray
            5: [243, 156, 18]    # Agriculture - Orange
        }
    
    def send_progress(self, stage, progress, message, data=None):
        """Send progress update"""
        update = {
            'stage': stage,
            'progress': progress,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'data': data or {}
        }
        
        if self.progress_callback:
            self.progress_callback(update)
        
        print(f"[{stage}] {progress}% - {message}")
    
    def load_and_prepare_data(self, image_path):
        """Load image and prepare training data with progress updates"""
        
        self.send_progress('loading', 0, 'Loading satellite image...')
        
        with rasterio.open(image_path) as src:
            image = src.read()
            profile = src.profile
            transform = src.transform
            bounds = src.bounds
        
        # Transpose to (height, width, bands)
        image = np.transpose(image, (1, 2, 0))
        height, width, bands = image.shape
        
        self.send_progress('loading', 50, f'Image loaded: {width}x{height} pixels, {bands} bands')
        
        # Reshape for classification
        X = image.reshape(-1, bands)
        
        self.send_progress('loading', 75, 'Preparing training data...')
        
        # Generate labels based on spectral characteristics
        y = self.generate_labels_with_progress(X)
        
        self.send_progress('loading', 100, 'Data preparation complete!')
        
        return X, y, image, profile, transform, bounds
    
    def generate_labels_with_progress(self, X):
        """Generate synthetic labels with progress updates"""
        
        self.send_progress('labeling', 0, 'Generating training labels...')
        
        labels = np.zeros(X.shape[0], dtype=int)
        total_pixels = X.shape[0]
        
        # Normalize bands
        X_norm = (X - np.min(X, axis=0)) / (np.max(X, axis=0) - np.min(X, axis=0) + 1e-8)
        
        # Process in chunks for progress updates
        chunk_size = total_pixels // 10
        
        for i in range(0, total_pixels, chunk_size):
            end_idx = min(i + chunk_size, total_pixels)
            
            for j in range(i, end_idx):
                if X.shape[1] >= 4:
                    red = X_norm[j, 0]
                    green = X_norm[j, 1]
                    blue = X_norm[j, 2]
                    nir = X_norm[j, 3]
                    
                    # Calculate indices
                    ndvi = (nir - red) / (nir + red + 1e-8)
                    ndwi = (green - nir) / (green + nir + 1e-8)
                    
                    # Classification rules
                    if ndwi > 0.3:
                        labels[j] = 0  # Water
                    elif ndvi > 0.6:
                        labels[j] = 1  # Forest
                    elif ndvi > 0.3:
                        labels[j] = 2  # Grassland
                    elif red > 0.3 and green > 0.3 and blue > 0.3:
                        labels[j] = 3  # Urban
                    elif ndvi < 0.1:
                        labels[j] = 4  # Barren
                    else:
                        labels[j] = 5  # Agriculture
            
            progress = int((end_idx / total_pixels) * 100)
            self.send_progress('labeling', progress, f'Labeled {end_idx:,} / {total_pixels:,} pixels')
        
        # Calculate class distribution
        unique, counts = np.unique(labels, return_counts=True)
        class_dist = {self.class_names[i]: int(counts[np.where(unique == i)[0][0]]) 
                      for i in unique if i < len(self.class_names)}
        
        self.send_progress('labeling', 100, 'Label generation complete!', 
                          {'class_distribution': class_dist})
        
        return labels
    
    def train_model_with_progress(self, X, y):
        """Train Random Forest model with progress updates"""
        
        self.send_progress('splitting', 0, 'Splitting data into train/test sets...')
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        self.send_progress('splitting', 100, 
                          f'Train: {len(X_train):,} samples, Test: {len(X_test):,} samples')
        
        # Train model
        self.send_progress('training', 0, 'Initializing Random Forest model...')
        
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=20,
            random_state=42,
            n_jobs=-1,
            verbose=0
        )
        
        self.send_progress('training', 25, 'Training model (this may take a few minutes)...')
        
        # Train
        self.model.fit(X_train, y_train)
        
        self.send_progress('training', 75, 'Model training complete! Evaluating...')
        
        # Evaluate
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        
        # Get predictions for detailed metrics
        y_pred = self.model.predict(X_test)
        
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        
        metrics = {
            'train_accuracy': float(train_score),
            'test_accuracy': float(test_score),
            'accuracy': float(accuracy_score(y_test, y_pred)),
            'precision': float(precision_score(y_test, y_pred, average='weighted', zero_division=0)),
            'recall': float(recall_score(y_test, y_pred, average='weighted', zero_division=0)),
            'f1_score': float(f1_score(y_test, y_pred, average='weighted', zero_division=0))
        }
        
        self.send_progress('training', 100, 'Model evaluation complete!', {'metrics': metrics})
        
        # Save model
        model_path = os.path.join('models', 'saved_models', 'random_forest_realtime.pkl')
        joblib.dump(self.model, model_path)
        
        self.send_progress('saving', 100, f'Model saved to {model_path}')
        
        return metrics
    
    def classify_with_progress(self, X, image_shape):
        """Classify image with progress updates"""
        
        self.send_progress('classifying', 0, 'Starting classification...')
        
        total_pixels = X.shape[0]
        chunk_size = total_pixels // 10
        predictions = np.zeros(total_pixels, dtype=int)
        
        for i in range(0, total_pixels, chunk_size):
            end_idx = min(i + chunk_size, total_pixels)
            predictions[i:end_idx] = self.model.predict(X[i:end_idx])
            
            progress = int((end_idx / total_pixels) * 100)
            self.send_progress('classifying', progress, 
                             f'Classified {end_idx:,} / {total_pixels:,} pixels')
        
        # Reshape to image
        classified_image = predictions.reshape(image_shape[0], image_shape[1])
        
        # Calculate class distribution
        unique, counts = np.unique(classified_image, return_counts=True)
        class_dist = {self.class_names[i]: int(counts[np.where(unique == i)[0][0]]) 
                      for i in unique if i < len(self.class_names)}
        
        self.send_progress('classifying', 100, 'Classification complete!', 
                          {'class_distribution': class_dist})
        
        return classified_image, class_dist
    
    def save_classified_image(self, classified_image, profile, output_path):
        """Save classified image with progress"""
        
        self.send_progress('saving', 0, 'Saving classified image...')
        
        profile.update(dtype=rasterio.uint8, count=1)
        
        with rasterio.open(output_path, 'w', **profile) as dst:
            dst.write(classified_image.astype(rasterio.uint8), 1)
        
        self.send_progress('saving', 100, f'Classified image saved to {output_path}')
        
        return output_path
    
    def generate_map_tiles(self, classified_image, bounds, output_dir='map_tiles'):
        """Generate map tiles for web visualization"""
        
        self.send_progress('tiles', 0, 'Generating map tiles...')
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Create RGB image from classified data
        height, width = classified_image.shape
        rgb_image = np.zeros((height, width, 3), dtype=np.uint8)
        
        for class_id, color in self.class_colors.items():
            mask = classified_image == class_id
            rgb_image[mask] = color
        
        # Save as PNG for web display
        from PIL import Image
        img = Image.fromarray(rgb_image, 'RGB')
        
        tile_path = os.path.join(output_dir, 'classification_overlay.png')
        img.save(tile_path)
        
        # Generate metadata
        metadata = {
            'bounds': {
                'north': bounds.top,
                'south': bounds.bottom,
                'east': bounds.right,
                'west': bounds.left
            },
            'size': {
                'width': width,
                'height': height
            },
            'classes': self.class_names,
            'colors': self.class_colors
        }
        
        metadata_path = os.path.join(output_dir, 'metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        self.send_progress('tiles', 100, 'Map tiles generated!', 
                          {'tile_path': tile_path, 'metadata': metadata})
        
        return tile_path, metadata
    
    def complete_workflow(self, image_path, output_path):
        """Complete training and classification workflow with progress"""
        
        self.send_progress('start', 0, 'Starting complete workflow...')
        
        # 1. Load and prepare data
        X, y, image, profile, transform, bounds = self.load_and_prepare_data(image_path)
        
        # 2. Train model
        metrics = self.train_model_with_progress(X, y)
        
        # 3. Classify
        classified_image, class_dist = self.classify_with_progress(X, image.shape)
        
        # 4. Save classified image
        saved_path = self.save_classified_image(classified_image, profile, output_path)
        
        # 5. Generate map tiles
        tile_path, metadata = self.generate_map_tiles(classified_image, bounds)
        
        self.send_progress('complete', 100, 'Workflow complete!', {
            'metrics': metrics,
            'class_distribution': class_dist,
            'output_path': saved_path,
            'tile_path': tile_path,
            'metadata': metadata
        })
        
        return {
            'metrics': metrics,
            'classification': {
                'output_path': saved_path,
                'class_distribution': class_dist
            },
            'visualization': {
                'tile_path': tile_path,
                'metadata': metadata
            }
        }
