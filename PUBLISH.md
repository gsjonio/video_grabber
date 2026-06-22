# Publishing vidgrab to PyPI

This guide explains how to publish vidgrab to PyPI so users can install it with `pip install vidgrab`.

## Prerequisites

1. Create an account at [pypi.org](https://pypi.org/account/register/)
2. Create an API token at [pypi.org/manage/account/](https://pypi.org/manage/account/#api-tokens)
   - Name: `vidgrab`
   - Scope: `Entire account (all projects)`
   - Copy the token (format: `pypi-AgEIcHlwaS5vcmc...`)

## Step 1: Build the Distribution

```bash
poetry build
# Creates:
#   dist/vidgrab-X.Y.Z-py3-none-any.whl
#   dist/vidgrab-X.Y.Z.tar.gz
```

## Step 2: Upload to PyPI

### Option A: Using Poetry (Recommended)

```bash
# Configure Poetry to use your PyPI token
poetry config pypi-token.pypi "pypi-AgEIcHlwaS5vcmc..."

# Upload
poetry publish
```

### Option B: Using Twine

```bash
# Install twine
pip install twine

# Upload
twine upload dist/*
```

## Step 3: Verify

```bash
# Wait ~5 minutes for PyPI to process

# Install from PyPI
pip install vidgrab

# Test
vidgrab --help
```

## After Publishing

Update README.md installation section to:

```text
### Via pip (recommended)

pip install vidgrab

### Via pipx (isolated)

pipx install vidgrab

### From source (development)

git clone https://github.com/gsjonio/video_grabber.git
cd video_grabber
poetry install
poetry run vidgrab --help
```

## Troubleshooting

### InvalidDistribution

Run `poetry lock --refresh` then `poetry build` again

### Repository not configured

Use `poetry config pypi-token.pypi "your-token"` instead of auth

### Invalid or expired authentication token

- Check your token at [pypi.org/manage/account](https://pypi.org/manage/account/#api-tokens)
- Regenerate if needed

## Release Checklist

- [ ] Update version in `pyproject.toml` and `vidgrab/__init__.py`
- [ ] Update `CHANGELOG.md`
- [ ] Create git tag: `git tag -a v0.X.Y -m "v0.X.Y"`
- [ ] Push: `git push origin main --tags`
- [ ] Run: `poetry build`
- [ ] Run: `poetry publish`
- [ ] Verify on [pypi.org/project/vidgrab](https://pypi.org/project/vidgrab/)

## Links

- [PyPI Project](https://pypi.org/project/vidgrab/)
- [PyPI Docs](https://packaging.python.org/tutorials/packaging-projects/)
- [Poetry Docs](https://python-poetry.org/docs/repositories/)
