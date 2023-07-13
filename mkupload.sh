#!/bin/sh
# This script is used for building and uploading this program to PyPi.

python setup.py bdist_wheel
python -m twine upload dist/*.whl
