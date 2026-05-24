#!/bin/sh
# Build and upload to PyPI.
# Override the interpreter via PYTHON=, e.g. PYTHON=.venv/bin/python ./mkupload.sh
set -eu
PY="${PYTHON:-python3}"
rm -rf dist/
"$PY" -m build --wheel
printf 'Upload dist/*.whl to PyPI? [y/N] '
read -r reply
case "$reply" in
    y|Y|yes|YES) "$PY" -m twine upload dist/*.whl ;;
    *) echo "Aborted."; exit 1 ;;
esac
