#!/usr/bin/env bash
set -euo pipefail

# --- Build frontend v1 ---
echo "🚀 Building st-transformers-js v1 component..."
FRONTEND_V1_SRC="st_transformers_js/frontend_v1"
BUILD_V1_DIR="st_transformers_js/frontend_v1/build"

mkdir -p "$BUILD_V1_DIR"

# --- Robust Download Function ---
download_file() {
    local url="$1"
    local output="$2"
    local max_retries=3
    local retry=0
    local success=false

    echo "Downloading $url to $output..."
    while [ $retry -lt $max_retries ]; do
        if curl -f -L --max-time 30 --connect-timeout 10 -o "$output" "$url"; then
            echo "Download successful."
            success=true
            break
        else
            retry=$((retry + 1))
            echo "Download failed. Retrying ($retry/$max_retries) in 2 seconds..."
            sleep 2
        fi
    done

    if [ "$success" = false ]; then
        echo "❌ ERROR: Failed to download $url after $max_retries attempts."
        exit 1
    fi
}

# Download streamlit-component-lib if not present
if [ ! -f "$BUILD_V1_DIR/streamlit.js" ]; then
    download_file \
        "https://cdn.jsdelivr.net/npm/streamlit-component-lib@2.0.0/dist/streamlit.js" \
        "$BUILD_V1_DIR/streamlit.js"
fi

cp "$FRONTEND_V1_SRC/index.html" "$BUILD_V1_DIR/"
cp "$FRONTEND_V1_SRC/transformers.min.js" "$BUILD_V1_DIR/"
echo "✅ v1 Build complete!"
echo "📂 Files in $BUILD_V1_DIR:"
ls -lh "$BUILD_V1_DIR"
echo "---"

# --- Build frontend v2 ---
echo "🚀 Building st-transformers-js v2 component..."
pushd frontend_v2 > /dev/null
echo "📦 Installing dependencies..."
npm ci
echo "🛠️  Building frontend..."
npm run build
popd > /dev/null

BUILD_V2_TARGET="st_transformers_js/frontend_v2/dist"
echo "🚚 Copying v2 build files to $BUILD_V2_TARGET..."
mkdir -p "$BUILD_V2_TARGET"
cp -r frontend_v2/dist/* "$BUILD_V2_TARGET/"
echo "✅ v2 Build complete!"
echo "📂 Files in $BUILD_V2_TARGET:"
ls -lh "$BUILD_V2_TARGET"
echo "---"
echo "📦 All builds finished."
