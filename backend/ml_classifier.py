import numpy as np
import rasterio
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import joblib
import os
from backend.utils import generate_filename, calculate_metrics, normalize_image

class MLClassifier:
    def __init__(self):
        self.rf_model = None
        self.cnn_model = None
        self.class_names = ['Water', 'Forest', 'Grassland', 'Urban', 'Barren', 'Agriculture']
    
    def load_image(self, image_path):
        """Load .tif image using rasterio"""
        with rasterio.open(image_path) as src:
            image = src.read()
            profile = src.profile
            transform = src.transform
        
        # Transpose to (height, width, bands)
        image = np.transpose(image, (1, 2, 0))
        return image, profile, transform
    
    def prepare_training_data(self, image):
        """Prepare training data with synthetic labels"""
        height, width, bands = image.shape
        
        # Reshape for classification
        X = image.reshape(-1, bands)
        
        # Generate synthetic labels based on spectral characteristics
        # This is a simplified approach - in production, use labeled training data
        y = self.generate_synthetic_labels(X)
        
        return X, y
    
    def generate_synthetic_labels(self, X):
        """Generate synthetic labels based on spectral indices"""
        labels = np.zeros(X.shape[0], dtype=int)
        
        # Normalize bands
        X_norm = normalize_image(X)
        
        for i in range(X.shape[0]):
            if X.shape[1] >= 4:
                red = X_norm[i, 0]
                green = X_norm[i, 1]
                blue = X_norm[i, 2]
                nir = X_norm[i, 3]
                
                # Calculate indices
                ndvi = (nir - red) / (nir + red + 1e-8)
                ndwi = (green - nir) / (green + nir + 1e-8)
                
                # Simple classification rules
                if ndwi > 0.3:
                    labels[i] = 0  # Water
                elif ndvi > 0.6:
                    labels[i] = 1  # Forest
                elif ndvi > 0.3:
                    labels[i] = 2  # Grassland
                elif red > 0.3 and green > 0.3 and blue > 0.3:
                    labels[i] = 3  # Urban
                elif ndvi < 0.1:
                    labels[i] = 4  # Barren
                else:
                    labels[i] = 5  # Agriculture
        
        return labels
    
    def train_random_forest(self, X, y):
        """Train Random Forest classifier"""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        self.rf_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=20,
            random_state=42,
            n_jobs=-1
        )
        
        self.rf_model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.rf_model.predict(X_test)
        metrics = calculate_metrics(y_test, y_pred)
        
        # Save model
        model_path = os.path.join('models', 'saved_models', 'random_forest.pkl')
        joblib.dump(self.rf_model, model_path)
        
        return metrics
    
    def build_cnn_model(self, input_shape, num_classes):
        """Build CNN model for land cover classification"""
        model = keras.Sequential([
            layers.Input(shape=input_shape),
            
            layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            
            layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            
            layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            
            layers.Flatten(),
            layers.Dense(256, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def train_cnn(self, image, labels):
        """Train CNN classifier"""
        height, width, bands = image.shape
        
        # Prepare patches
        patch_size = 32
        patches = []
        patch_labels = []
        
        for i in range(0, height - patch_size, patch_size // 2):
            for j in range(0, width - patch_size, patch_size // 2):
                patch = image[i:i+patch_size, j:j+patch_size, :]
                if patch.shape == (patch_size, patch_size, bands):
                    patches.append(patch)
                    # Get majority label in patch
                    patch_label = labels[i:i+patch_size, j:j+patch_size].flatten()
                    patch_labels.append(np.bincount(patch_label).argmax())
        
        X = np.array(patches)
        y = np.array(patch_labels)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Normalize
        X_train = normalize_image(X_train)
        X_test = normalize_image(X_test)
        
        # Build and train model
        self.cnn_model = self.build_cnn_model(
            input_shape=(patch_size, patch_size, bands),
            num_classes=len(self.class_names)
        )
        
        history = self.cnn_model.fit(
            X_train, y_train,
            validation_data=(X_test, y_test),
            epochs=20,
            batch_size=32,
            verbose=1
        )
        
        # Evaluate
        y_pred = np.argmax(self.cnn_model.predict(X_test), axis=1)
        metrics = calculate_metrics(y_test, y_pred)
        
        # Save model
        model_path = os.path.join('models', 'saved_models', 'cnn_model.h5')
        self.cnn_model.save(model_path)
        
        return metrics
    
    def classify(self, image_path, model_type='random_forest'):
        """Classify land cover using trained model"""
        image, profile, transform = self.load_image(image_path)
        height, width, bands = image.shape
        
        X = image.reshape(-1, bands)
        
        if model_type == 'random_forest':
            if self.rf_model is None:
                model_path = os.path.join('models', 'saved_models', 'random_forest.pkl')
                if os.path.exists(model_path):
                    self.rf_model = joblib.load(model_path)
                else:
                    raise ValueError("Model not trained. Train first.")
            
            predictions = self.rf_model.predict(X)
        else:
            raise ValueError(f"Model type '{model_type}' not supported yet")
        
        # Reshape predictions
        classified_image = predictions.reshape(height, width)
        
        # Save classified image
        output_path = generate_filename('classified_map', 'tif')
        output_path = os.path.join('exports', output_path)
        
        profile.update(dtype=rasterio.uint8, count=1)
        with rasterio.open(output_path, 'w', **profile) as dst:
            dst.write(classified_image.astype(rasterio.uint8), 1)
        
        return {
            'output_path': output_path,
            'class_distribution': {
                self.class_names[i]: int(np.sum(classified_image == i))
                for i in range(len(self.class_names))
            }
        }
    
    def train_and_classify(self, image_path, model_type='random_forest'):
        """Complete workflow: train model and classify"""
        image, profile, transform = self.load_image(image_path)
        
        # Prepare data
        X, y = self.prepare_training_data(image)
        
        # Train model
        if model_type == 'random_forest':
            metrics = self.train_random_forest(X, y)
        elif model_type == 'cnn':
            labels_2d = y.reshape(image.shape[0], image.shape[1])
            metrics = self.train_cnn(image, labels_2d)
        else:
            raise ValueError(f"Model type '{model_type}' not supported")
        
        # Classify
        classification_result = self.classify(image_path, model_type)
        
        return {
            'metrics': metrics,
            'classification': classification_result
        }
