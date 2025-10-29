#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🔧 Starting build process..."

# Install Python dependencies
echo "📦 Installing Python packages..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data exports models/saved_models logs reports map_tiles

# Setup Earth Engine credentials (REQUIRED)
echo "🔑 Setting up GEE credentials..."
if [ ! -z "$GEE_CREDENTIALS" ]; then
    mkdir -p ~/.config/earthengine
    echo "$GEE_CREDENTIALS" > ~/.config/earthengine/credentials
    chmod 600 ~/.config/earthengine/credentials
    echo "✓ GEE credentials configured"
else
    echo "⚠️  WARNING: GEE_CREDENTIALS not found!"
    echo "⚠️  App will NOT work without GEE credentials!"
    echo "⚠️  Add GEE_CREDENTIALS environment variable in Render dashboard"
fi

echo "✅ Build complete!"
