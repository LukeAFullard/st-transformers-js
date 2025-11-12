#!/bin/bash
set -e

echo "🚀 Building st-transformers-js v1 component..."

FRONTEND_SRC="st_transformers_js/frontend_v1"
BUILD_DIR="st_transformers_js/frontend_v1/build"

# Create build directory
mkdir -p "$BUILD_DIR"

# Verify files exist
if [ ! -f "$FRONTEND_SRC/index.html" ]; then
    echo "❌ Error: index.html not found in $FRONTEND_SRC"
    exit 1
fi

# Copy files to build directory
echo "📋 Copying files to build directory..."
cp "$FRONTEND_SRC/index.html" "$BUILD_DIR/"
cp "$FRONTEND_SRC/transformers.min.js" "$BUILD_DIR/"

echo "✅ v1 Build complete!"
echo "📂 Files in $BUILD_DIR:"
ls -lh "$BUILD_DIR"
