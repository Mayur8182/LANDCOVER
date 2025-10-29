import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = FLASK_ENV == 'development'
    
    # Server settings
    HOST = '0.0.0.0'
    PORT = int(os.getenv('PORT', 5000))
    
    # Google Earth Engine
    GEE_PROJECT_ID = os.getenv('GEE_PROJECT_ID', '')
    
    # File paths
    DATA_DIR = 'data'
    EXPORTS_DIR = 'exports'
    MODELS_DIR = 'models/saved_models'
    LOGS_DIR = 'logs'
    
    # Satellite imagery settings
    DEFAULT_SCALE = 10  # meters per pixel
    MAX_CLOUD_COVER = 20  # percentage
    
    # ML settings
    RANDOM_FOREST_ESTIMATORS = 100
    RANDOM_FOREST_MAX_DEPTH = 20
    CNN_EPOCHS = 20
    CNN_BATCH_SIZE = 32
    CNN_PATCH_SIZE = 32
    
    # Land cover classes
    LAND_COVER_CLASSES = {
        0: 'Water',
        1: 'Forest',
        2: 'Grassland',
        3: 'Urban',
        4: 'Barren',
        5: 'Agriculture'
    }
    
    # Color mapping for visualization (RGB)
    CLASS_COLORS = {
        0: [52, 152, 219],   # Water - Blue
        1: [39, 174, 96],    # Forest - Dark Green
        2: [46, 204, 113],   # Grassland - Light Green
        3: [231, 76, 60],    # Urban - Red
        4: [149, 165, 166],  # Barren - Gray
        5: [243, 156, 18]    # Agriculture - Orange
    }

config = Config()
