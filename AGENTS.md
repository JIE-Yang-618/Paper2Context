# Agent instructions

Paper2Context is deterministic-first and local-first.

- Do not add required cloud or LLM dependencies.
- Preserve page provenance in all transformations.
- Prefer raw uncertain data over fabricated structured fields.
- Treat scanned PDFs, complex equations, and tables as explicit limitations unless tests prove support.
- Every extraction change should include a regression test.
