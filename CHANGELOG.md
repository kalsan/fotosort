# unreleased

- By HappyTetrahedron:
  - Anchor relative paths to the path that is being sorted
  - Create inexisting directories even for permanent target locations
  - Enhance autocomplete by specifying proper ordering of criteria
  - Make timestamp for temporary directories customisable
- Fix crash when launching without `-l`/`--location` (now shows the no-image screen)
- Fix crash when the config file exists but is empty
- Modernise packaging: replace `setup.py` with `pyproject.toml` (PEP 621), entry point via `[project.scripts]`, drop the `bin/fotosort` stub
- Rewrite EXIF timestamp extraction using the modern Pillow API and close file handles deterministically
- Remove dead code (`get_orientation`, `getCurrentImageRotation`) that was unused since QML took over rotation
- Update to Qt 6 idiom `app.exec()` (replaces deprecated `app.exec_()`)
- Use `os.makedirs(..., exist_ok=True)` for target directory creation (atomic, no TOCTOU race)
- Release scripts: `mkupload.sh` now prompts before uploading to PyPI; both scripts use `set -eu` and modern build tooling (`python -m build`, `pip install .`)

# 1.3.1

- Fix reading of VERSION

# 1.3.0

- Update to pyside 6 and Qt 6.5, remove now unnecessary resize workaround

# 1.2.0

- Implement "first" and "last" jump menues
- Fix an undesired behavior where the window was resized on picture load
- Build using current libraries and python 3.11.4

# 1.1

- If no config file exists, Fotosort automatically creates it.
- Created settings dialog

# 1.0

Initial version
