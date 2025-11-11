#!/bin/bash
set -e

echo "🚀 Building st-transformers-js component..."

FRONTEND_DIR="frontend"
BUILD_DIR="st_transformers_js/frontend/build"
PUBLIC_DIR="$FRONTEND_DIR"

# Create build directory
mkdir -p "$BUILD_DIR"

# Download transformers.js if needed
TRANSFORMERS_FILE="$PUBLIC_DIR/transformers.min.js"
TRANSFORMERS_URL="https://cdn.jsdelivr.net/npm/@xenova/transformers@3.2.0/dist/transformers.min.js"

if [ ! -f "$TRANSFORMERS_FILE" ]; then
    echo "⬇️  Downloading transformers.min.js..."
    curl -L "$TRANSFORMERS_URL" -o "$TRANSFORMERS_FILE"
fi

# Copy to build directory
cp -r "$PUBLIC_DIR"/* "$BUILD_DIR/"

echo "✅ Build complete!"
