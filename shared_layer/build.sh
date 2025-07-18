#!/bin/bash
set -e

echo "🧹 Cleaning previous builds"
rm -rf python shared_layer.zip

echo "📁 Creating layer folder structure: python/"
mkdir -p python

echo "📦 Installing third-party dependencies from requirements.txt"
pip install -r requirements.txt -t python/

echo "📂 Copying internal shared modules"
cp -r ../shared python/

echo "📦 Zipping layer to shared_layer.zip"
zip -r9 shared_layer.zip python > /dev/null

echo "✅ Shared layer built successfully!"

echo "🔍 Verifying shared_layer.zip structure..."
unzip -l shared_layer.zip
