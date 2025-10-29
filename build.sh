#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p data exports models/saved_models logs reports map_tiles

# Authenticate Earth Engine (if credentials available)
if [ ! -z "$GEE_CREDENTIALS" ]; then
    echo "$GEE_CREDENTIALS" > ~/.config/earthengine/credentials
fi

echo "Build complete!"
