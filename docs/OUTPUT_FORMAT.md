# Output format

A conversion creates one self-contained context directory.

- `PAPER.md` — cleaned paper text with page provenance comments.
- `PAPER_CONTEXT.md` — compact navigation/context overview; deterministic, not an LLM summary.
- `metadata.json` — title, author string, abstract/keywords when detected, DOI when detected.
- `structure.json` — sections and provenance-bearing paragraphs.
- `references.json` — conservative reference records with raw strings preserved.
- `assets.json` — detected figure/table captions and source pages.
- `chunks.jsonl` — section-aware chunks for downstream AI/RAG tools.
- `manifest.json` — source fingerprint, diagnostics, confidence and output inventory.
- `source/extraction.json` — complete internal document model for debugging/reproducibility.

The format is intentionally plain Markdown/JSON/JSONL so users are not locked into a Paper2Context runtime.
