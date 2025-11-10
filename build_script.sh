#!/bin/bash

# Build script for st-transformers-js component
# This script downloads transformers.js and prepares the component for distribution

set -e  # Exit on error

echo "🚀 Building st-transformers-js component..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Create directory structure
echo -e "${YELLOW}📁 Creating directory structure...${NC}"
mkdir -p frontend/public
mkdir -p st_transformers_js/frontend/build

# Step 2: Download transformers.min.js if not present
TRANSFORMERS_FILE="frontend/public/transformers.min.js"
TRANSFORMERS_URL="https://cdn.jsdelivr.net/npm/@xenova/transformers@3.2.0/dist/transformers.min.js"

if [ ! -f "$TRANSFORMERS_FILE" ]; then
    echo -e "${YELLOW}⬇️  Downloading transformers.min.js...${NC}"
    curl -L "$TRANSFORMERS_URL" -o "$TRANSFORMERS_FILE"
    echo -e "${GREEN}✓ Downloaded transformers.min.js${NC}"
else
    echo -e "${GREEN}✓ transformers.min.js already exists${NC}"
fi

# Step 3: Copy files to build directory
echo -e "${YELLOW}📋 Copying files to build directory...${NC}"
cp frontend/public/index.html st_transformers_js/frontend/build/
cp frontend/public/transformers.min.js st_transformers_js/frontend/build/

echo -e "${GREEN}✓ Files copied to build directory${NC}"

# Step 4: Verify build
echo -e "${YELLOW}🔍 Verifying build...${NC}"
if [ -f "st_transformers_js/frontend/build/index.html" ] && [ -f "st_transformers_js/frontend/build/transformers.min.js" ]; then
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
