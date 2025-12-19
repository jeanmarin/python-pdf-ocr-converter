# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- `pdf_ocr_converter/` package containing the reusable conversion pipeline + CLI (`run_converter.py`).
- `test/` folder with unit tests for pure diff utilities.
- `env.template` as a safe template for creating a local `.env`.

### Changed
- Refactored `Converter3.py`–`Converter7.py` to be thin wrappers around the shared implementation (same libraries, less duplicated code).
- `requirements.txt`: removed `difflib` (it is a Python standard library module, not a pip dependency).


