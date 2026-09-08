from __future__ import annotations
from pathlib import Path
from .diagnostics import inspect_pdf, PDFInspectionError
from .metadata import extract_metadata
from .extraction import extract_structure
from .references import extract_references
from .chunking import build_chunks
from .models import PaperDocument
from .utils import sha256_file
from .renderers import render_all

def build_document(path: Path) -> PaperDocument:
    diag=inspect_pdf(path)
    if diag.ocr_required:
        raise PDFInspectionError('No usable text layer detected. OCR is not enabled by default in v0.1.0.')
    sections,assets,pages,warnings=extract_structure(path)
    metadata=extract_metadata(path,pages[0] if pages else '')
    refs=extract_references(sections)
    chunks=build_chunks(sections)
    return PaperDocument(path.name,sha256_file(path),diag,metadata,sections,refs,assets,chunks,warnings)

def convert_pdf(path: Path, output: Path | None=None) -> tuple[PaperDocument,Path]:
    doc=build_document(path)
    out=output or path.with_name(path.stem+'_context')
    render_all(doc,out)
    return doc,out
