# Publishing to PyPI (Maintainer Only)

**⚠️ Internal document — Only for project maintainer with PyPI token.**

---

## Release Workflow

1. **Update version:**

   ```bash
   # Edit vidgrab/__init__.py and pyproject.toml
   # Update CHANGELOG.md
   ```

1. **Commit and tag:**

   ```bash
   git add vidgrab/__init__.py pyproject.toml CHANGELOG.md
   git commit -m "chore: bump to v0.X.Y"
   git tag -a v0.X.Y -m "v0.X.Y — description"
   git push origin main --tags
   ```

1. **Build:**

   ```bash
   poetry build
   # Creates: dist/vidgrab-X.Y.Z-py3-none-any.whl
   #          dist/vidgrab-X.Y.Z.tar.gz
   ```

1. **Publish:**

   ```bash
   poetry publish
   ```

1. **Verify:**

   - Wait ~5 minutes for PyPI to process
   - Check: [pypi.org/project/vidgrab](https://pypi.org/project/vidgrab/)

---

## Using Make

```bash
make build    # Step 3
make publish  # Step 4
```

Or combined:

```bash
make clean build publish
```

---

## Token Setup (One-time)

```bash
poetry config pypi-token.pypi "your-token-here"
```

⚠️ **Never commit tokens!** Never share in public!
