#!/usr/bin/env bash
set -euo pipefail

# --- Build frontend v1 ---
echo "🚀 Building st-transformers-js v1 component..."

FRONTEND_V1_SRC="st_transformers_js/frontend_v1"
BUILD_V1_DIR="st_transformers_js/frontend_v1/build"

# Create build directory
mkdir -p "$BUILD_V1_DIR"

# Verify files exist
if [ ! -f "$FRONTEND_V1_SRC/index.html" ]; then
    echo "❌ Error: index.html not found in $FRONTEND_V1_SRC"
    exit 1
fi

# Copy files to build directory
echo "📋 Copying v1 files to build directory..."
cp "$FRONTEND_V1_SRC/index.html" "$BUILD_V1_DIR/"
cp "$FRONTEND_V1_SRC/transformers.min.js" "$BUILD_V1_DIR/"

echo "✅ v1 Build complete!"
echo "📂 Files in $BUILD_V1_DIR:"
ls -lh "$BUILD_V1_DIR"

echo "---"

# --- Build frontend v2 ---
echo "🚀 Building st-transformers-js v2 component..."

# Install dependencies and build frontend
pushd frontend_v2
npm ci
npm run build
popd

# Copy v2 build into Python package
BUILD_V2_TARGET="st_transformers_js/frontend_v2/dist"
rm -rf "$BUILD_V2_TARGET" || true
mkdir -p "$BUILD_V2_TARGET"
cp -r frontend_v2/dist/* "$BUILD_V2_TARGET/"

echo "✅ v2 Build complete!"
echo "📂 Files in $BUILD_V2_TARGET:"
ls -lh "$BUILD_V2_TARGET"

echo "---"
echo "📦 All builds finished."
