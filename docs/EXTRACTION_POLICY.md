# Extraction policy

Paper2Context follows four rules:

1. **Provenance before polish.** Extracted text should retain a path back to the source page.
2. **Deterministic before generative.** v0.1.0 does not require an LLM to infer paper content.
3. **Uncertainty must be visible.** Weakly supported structure remains raw or is labelled with lower confidence.
4. **Fail clearly rather than fabricate.** Image-only PDFs are reported as OCR-required instead of receiving invented text.

The tool may normalize line breaks, repeated headers/footers, page numbers and soft hyphenation. It should not rewrite claims, interpret results, or manufacture bibliographic fields.
