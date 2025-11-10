#!/bin/bash

# Build script for st-transformers-js component
# This script downloads transformers.js and prepares the component for distribution

set -e  # Exit on error

echo "🚀 Building st-transformers-js component..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Define paths
FRONTEND_DIR="st_transformers_js/frontend"
PUBLIC_DIR="$FRONTEND_DIR/public"
BUILD_DIR="$FRONTEND_DIR/build"
TRANSFORMERS_FILE="$PUBLIC_DIR/transformers.min.js"
TRANSFORMERS_URL="https://cdn.jsdelivr.net/npm/@xenova/transformers"

# Step 1: Create directory structure
echo -e "${YELLOW}📁 Creating directory structure...${NC}"
mkdir -p "$PUBLIC_DIR"
mkdir -p "$BUILD_DIR"

# Step 2: Download transformers.min.js if not present
if [ ! -f "$TRANSFORMERS_FILE" ]; then
    echo -e "${YELLOW}⬇️  Downloading transformers.min.js...${NC}"
    curl -L --fail "$TRANSFORMERS_URL" -o "$TRANSFORMERS_FILE"
    echo -e "${GREEN}✓ Downloaded transformers.min.js${NC}"
else
    echo -e "${GREEN}✓ transformers.min.js already exists${NC}"
fi

# Step 3: Copy files to build directory
echo -e "${YELLOW}📋 Copying files to build directory...${NC}"
cp "$PUBLIC_DIR/index.html" "$BUILD_DIR/"
cp "$PUBLIC_DIR/transformers.min.js" "$BUILD_DIR/"

echo -e "${GREEN}✓ Files copied to build directory${NC}"

# Step 4: Verify build
echo -e "${YELLOW}🔍 Verifying build...${NC}"
if [ -f "$BUILD_DIR/index.html" ] && [ -f "$BUILD_DIR/transformers.min.js" ]; then
    echo -e "${GREEN}✓ Build verification successful${NC}"
else
    echo -e "${RED}✗ Build verification failed${NC}"
    exit 1
fi

# Step 5: Build Python package
echo -e "${YELLOW}📦 Building Python package...${NC}"
python -m build

echo -e "${GREEN}✅ Build complete!${NC}"
echo ""
echo "Next steps:"
echo "  1. Install locally: pip install -e ."
echo "  2. Test: streamlit run demo_app.py"
echo "  3. Publish: twine upload dist/*"
