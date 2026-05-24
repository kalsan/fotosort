#!/bin/sh
# Build and install locally.
# Override the interpreter via PYTHON=, e.g. PYTHON=.venv/bin/python ./mklocinstall.sh
set -eu
"${PYTHON:-python3}" -m pip install .
