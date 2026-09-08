# Limitations

- Scanned/image-only PDFs require OCR and are rejected in v0.1.0.
- Reading order in complex two-column or mixed layouts can be imperfect.
- Mathematical notation may lose spatial semantics.
- Table reconstruction is intentionally not attempted.
- Figure/table support is caption-manifest-first; not every embedded image is exported.
- Reference parsing is conservative and preserves raw strings when structure is uncertain.
- Metadata embedded by publishers can be missing or wrong.
