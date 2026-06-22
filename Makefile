.PHONY: help install test lint mypy pylint ruff fmt clean release

help:
	@echo "vidgrab development commands"
	@echo ""
	@echo "  make install          Install dependencies"
	@echo "  make test             Run pytest"
	@echo "  make lint             Run ruff, pylint, mypy (full check)"
	@echo "  make fmt              Auto-format with ruff"
	@echo "  make mypy             Type check with mypy strict"
	@echo "  make pylint           Lint with pylint"
	@echo "  make ruff             Lint with ruff"
	@echo "  make clean            Remove cache and build artifacts"
	@echo "  make release          Bump version, update CHANGELOG, create tag"
	@echo ""

install:
	poetry install

test:
	poetry run pytest

lint: ruff pylint mypy

ruff:
	poetry run ruff check vidgrab/

pylint:
	poetry run pylint vidgrab/

mypy:
	poetry run mypy vidgrab/ --ignore-missing-imports --strict

fmt:
	poetry run ruff check --fix vidgrab/
	poetry run ruff format vidgrab/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov coverage.xml
	rm -rf build dist *.egg-info

release:
	@echo "Release workflow:"
	@echo "1. Update version in vidgrab/__init__.py and pyproject.toml"
	@echo "2. Update CHANGELOG.md manually (or use git-cliff)"
	@echo "3. git add <files> && git commit -m 'chore: bump to vX.Y.Z'"
	@echo "4. git tag -a vX.Y.Z -m 'vX.Y.Z — <description>'"
	@echo "5. git push origin main --tags"
	@echo ""
	@echo "CI will automatically create the GitHub Release from the tag."
