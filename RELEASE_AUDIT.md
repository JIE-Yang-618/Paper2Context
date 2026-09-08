# Release audit — v0.1.0

Release date: 2026-09-08

## Verified locally

- Source test suite: 16 passed.
- Smoke test: passed.
- Python bytecode compilation: passed.
- Wheel build from source: passed.
- Wheel metadata contains runtime dependencies for `pdfplumber` and `pypdf`.
- Wheel installation into an isolated virtual environment: passed.
- Installed CLI: `--version`, `doctor`, `inspect`, and `convert` passed.
- Installed end-to-end conversion created the documented Markdown/JSON/JSONL outputs.
- Regression check for short final reference pages: passed.
- Image-only PDF detection: passed.
- Password-protected PDF error handling: passed.

## Environment note

The build environment used for this release does not allow outbound package downloads. The isolated-wheel runtime test therefore supplied already-installed runtime dependencies on `PYTHONPATH`; the Paper2Context wheel itself was installed into the isolated environment. GitHub Actions installs all declared dependencies normally from `pyproject.toml` on Linux, Windows, and macOS.

## Scope reminder

v0.1.0 is built for born-digital papers. Two-column reading order is best-effort. OCR, complex table reconstruction, equation interpretation, and guaranteed figure-image extraction are not claimed.
