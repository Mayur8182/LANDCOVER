import os
import numpy as np
from datetime import datetime

def create_directories():
    """Create necessary directories for the project"""
    directories = ['data', 'exports', 'models/saved_models', 'logs']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def generate_filename(prefix, extension='tif'):
    """Generate unique filename with timestamp"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{prefix}_{timestamp}.{extension}"

def normalize_image(image):
    """Normalize image data to 0-1 range"""
    return (image - np.min(image)) / (np.max(image) - np.min(image) + 1e-8)

def calculate_metrics(y_true, y_pred):
    """Calculate classification metrics"""
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
    
    return {
        'accuracy': float(accuracy_score(y_true, y_pred)),
        'precision': float(precision_score(y_true, y_pred, average='weighted', zero_division=0)),
        'recall': float(recall_score(y_true, y_pred, average='weighted', zero_division=0)),
        'f1_score': float(f1_score(y_true, y_pred, average='weighted', zero_division=0)),
        'confusion_matrix': confusion_matrix(y_true, y_pred).tolist()
    }
