#!/usr/bin/env bash
# Usage ./scripts/build-docs.sh

if [ ! -f "pyproject.toml" ]; then
    echo "Error: must be run from the project root directory (where pyproject.toml lives)"
    exit 1
fi

poetry run generate-readme
poetry run sphinx-build -M html docs/source docs/build