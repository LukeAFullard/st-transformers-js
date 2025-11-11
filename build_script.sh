#!/bin/bash
set -e

echo "🚀 Building st-transformers-js component..."

FRONTEND_SRC="frontend"
BUILD_DIR="st_transformers_js/frontend/build"

# Create build directory
mkdir -p "$BUILD_DIR"

# Download transformers.js if not present
TRANSFORMERS_FILE="$FRONTEND_SRC/transformers.min.js"
TRANSFORMERS_URL="https://cdn.jsdelivr.net/npm/@xenova/transformers@3.2.0/dist/transformers.min.js"

if [ ! -f "$TRANSFORMERS_FILE" ]; then
    echo "⬇️  Downloading transformers.min.js..."
    curl -L "$TRANSFORMERS_URL" -o "$TRANSFORMERS_FILE"
    echo "✓ Downloaded transformers.min.js"
fi

# Verify files exist
if [ ! -f "$FRONTEND_SRC/index.html" ]; then
    echo "❌ Error: index.html not found in $FRONTEND_SRC"
    exit 1
fi

# Copy files to build directory
echo "📋 Copying files to build directory..."
cp "$FRONTEND_SRC/index.html" "$BUILD_DIR/"
cp "$FRONTEND_SRC/transformers.min.js" "$BUILD_DIR/"

echo "✅ Build complete!"
echo "📂 Files in $BUILD_DIR:"
ls -lh "$BUILD_DIR"
