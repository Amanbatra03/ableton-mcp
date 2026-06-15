#!/bin/bash
# Ableton MCP PyPI Publication Script
# Run this script to publish the package to PyPI

set -e

echo "=========================================="
echo "Ableton MCP v1.0.0 Publication to PyPI"
echo "=========================================="
echo

# Step 1: Verify distributions
echo "[1/4] Verifying distributions..."
if ! python -m twine check dist/*; then
    echo "ERROR: Distribution check failed"
    exit 1
fi
echo "✓ Distributions verified"
echo

# Step 2: Display what will be uploaded
echo "[2/4] Distribution contents:"
ls -lh dist/
echo

# Step 3: Instructions
echo "[3/4] Publication instructions:"
echo
echo "To publish to PyPI, you need:"
echo "  1. A PyPI account (https://pypi.org/account/register/)"
echo "  2. An API token from PyPI"
echo
echo "Then run ONE of these commands:"
echo
echo "Option A (Interactive - recommended for first time):"
echo "  python -m twine upload dist/*"
echo "  When prompted:"
echo "    Username: __token__"
echo "    Password: pypi-YOUR_TOKEN_HERE"
echo
echo "Option B (Using environment variable):"
echo "  export TWINE_PASSWORD=pypi-YOUR_TOKEN_HERE"
echo "  python -m twine upload dist/*"
echo
echo "Option C (Using .pypirc file):"
echo "  Create ~/.pypirc with your credentials"
echo "  python -m twine upload dist/*"
echo
echo "[4/4] Ready to publish!"
echo
echo "After publishing, verify with:"
echo "  pip install --upgrade ableton-mcp"
echo "  python -c \"import ableton_mcp; print('Success!')\""
echo
echo "=========================================="
