#!/bin/bash
# vidgrab installer script

set -e

echo "Installing vidgrab..."
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3.11+ is required but not installed."
    echo "Download from: https://www.python.org/downloads/"
    exit 1
fi

python_version=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Python $python_version detected"

# Check ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo ""
    echo "WARNING: ffmpeg is required but not found in PATH"
    echo ""
    echo "Install it with:"
    echo "  macOS:  brew install ffmpeg"
    echo "  Linux:  sudo apt install ffmpeg"
    echo "  Windows: winget install ffmpeg"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Install via pip
echo ""
echo "Installing vidgrab via pip..."
pip install --upgrade vidgrab

echo ""
echo "✓ Installation complete!"
echo ""
echo "Test it:"
echo "  vidgrab --help"
echo ""
echo "Download a video:"
echo "  vidgrab https://youtu.be/dQw4w9WgXcQ"
