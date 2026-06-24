#!/bin/bash
# vidgrab release automation script
# Usage: ./release.sh 1.0.0

set -e

VERSION=${1:-}

if [ -z "$VERSION" ]; then
    echo "Usage: ./release.sh <version>"
    echo "Example: ./release.sh 1.0.0"
    exit 1
fi

echo "🚀 Releasing vidgrab v$VERSION"
echo ""

# 1. Update version in files
echo "📝 Updating version in files..."
sed -i "s/__version__ = .*/\__version__ = \"$VERSION\"/" vidgrab/__init__.py
# Update only the [tool.poetry] version line
sed -i "/^\[tool.poetry\]/,/^version = /{s/^version = .*/version = \"$VERSION\"/}" pyproject.toml
sed -i "s/badge\/version-[^-]*-/badge\/version-$VERSION-/" README.md

# 2. Run tests
echo "🧪 Running tests..."
poetry run pytest -q

# 3. Run linters
echo "🔍 Running linters..."
poetry run ruff check vidgrab/
poetry run pylint vidgrab/ > /dev/null 2>&1 || true
poetry run mypy vidgrab/ > /dev/null 2>&1 || true

# 4. Generate changelog with git-cliff
echo "📚 Generating CHANGELOG..."
poetry run git-cliff --output docs/CHANGELOG.md || echo "⚠️  Skip changelog generation (git-cliff not available)"

# 5. Commit
echo "📦 Committing changes..."
git add vidgrab/__init__.py pyproject.toml README.md docs/CHANGELOG.md
git commit -m "chore: bump version to $VERSION"

# 6. Create git tag
echo "🏷️  Creating git tag..."
git tag -a "v$VERSION" -m "v$VERSION — Ready for production"

# 7. Build
echo "🔨 Building distribution..."
poetry build

# 8. Show what's next
echo ""
echo "✅ Done! Next steps:"
echo ""
echo "  1. Review the changes:"
echo "     git log --oneline -5"
echo "     git diff HEAD~1"
echo ""
echo "  2. Push (only if changes look good):"
echo "     git push origin main --tags"
echo ""
echo "  3. Publish to PyPI:"
echo "     poetry publish"
echo ""
echo "  4. Create GitHub Release:"
echo "     gh release create v$VERSION --generate-notes"
echo ""
