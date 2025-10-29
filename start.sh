#!/usr/bin/env bash

# Create necessary directories
mkdir -p data exports models/saved_models logs reports map_tiles

# Start the application
gunicorn app:app --bind 0.0.0.0:$PORT --timeout 600 --workers 2 --worker-class eventlet
