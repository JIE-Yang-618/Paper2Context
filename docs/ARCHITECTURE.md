# Architecture

```text
PDF
 │
 ▼
Diagnostics / ingestion
 │
 ▼
Layout-aware text extraction
 │
 ▼
Scholarly structure recovery
 │
 ▼
PaperDocument data model
 ├───────────────┬───────────────┐
 ▼               ▼               ▼
References      Assets          Chunks
 └───────────────┴───────────────┘
                 │
                 ▼
        Markdown + JSON context pack
```

The CLI is an adapter around `service.convert_pdf`; extraction logic is kept out of command parsing. The internal `PaperDocument` model is the stable boundary between parsers and renderers.
