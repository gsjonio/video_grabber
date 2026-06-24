#!/bin/bash
# Test vidgrab with a real YouTube video (dry-run)
# This validates that the entire pipeline works without downloading

set -e

echo "🧪 Testing vidgrab with real YouTube video (dry-run)..."
echo ""

# Use a short, stable video for testing
TEST_URL="https://youtu.be/dQw4w9WgXcQ"

echo "URL: $TEST_URL"
echo ""

# Test 1: Dry-run
echo "1️⃣  Testing --dry-run (should show metadata without downloading)..."
poetry run vidgrab "$TEST_URL" --dry-run
echo "✅ Dry-run passed"
echo ""

# Test 2: Help
echo "2️⃣  Testing --help..."
poetry run vidgrab --help > /dev/null
echo "✅ Help passed"
echo ""

# Test 3: Version
echo "3️⃣  Testing --version..."
poetry run vidgrab --version
echo "✅ Version passed"
echo ""

# Test 4: Batch file with URL
echo "4️⃣  Testing --batch with dry-run..."
echo "$TEST_URL" > /tmp/test_urls.txt
poetry run vidgrab --batch /tmp/test_urls.txt --dry-run > /dev/null
rm /tmp/test_urls.txt
echo "✅ Batch passed"
echo ""

echo "🎉 All real-world tests passed!"
echo ""
echo "Note: These are dry-run tests. For actual download test, run:"
echo "  vidgrab '$TEST_URL' --max-height 480 --output ./test_download"
