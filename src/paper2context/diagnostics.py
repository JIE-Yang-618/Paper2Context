from __future__ import annotations
from pathlib import Path
from pypdf import PdfReader
import pdfplumber
from .models import Diagnostics

class PDFInspectionError(RuntimeError): pass

def inspect_pdf(path: Path) -> Diagnostics:
    if not path.exists() or not path.is_file():
        raise PDFInspectionError(f"PDF not found: {path}")
    if path.suffix.lower() != '.pdf':
        raise PDFInspectionError('Input must be a .pdf file')
    try:
        reader = PdfReader(str(path), strict=False)
    except Exception as e:
        raise PDFInspectionError(f"Could not open PDF: {e}") from e
    encrypted = bool(reader.is_encrypted)
    if encrypted:
        try:
            unlocked = reader.decrypt("")
        except Exception as e:
            raise PDFInspectionError('PDF is encrypted and could not be opened without a password') from e
        if not unlocked:
            raise PDFInspectionError('PDF is encrypted and requires a password; password input is not supported in v0.1.0')
    pages = len(reader.pages)
    if pages == 0:
        raise PDFInspectionError('PDF contains no pages')
    sample_text = []
    widths = []
    try:
        with pdfplumber.open(str(path)) as pdf:
            for page in pdf.pages[: min(5, pages)]:
                t = page.extract_text() or ''
                sample_text.append(t)
                words = page.extract_words() or []
                if words:
                    mid = page.width / 2
                    left = sum(1 for w in words if float(w['x0']) < mid - 15)
                    right = sum(1 for w in words if float(w['x0']) > mid + 15)
                    widths.append((left, right))
    except Exception as e:
        raise PDFInspectionError(f"PDF layout extraction failed: {e}") from e
    chars = sum(len(x.strip()) for x in sample_text)
    text_layer = chars >= max(20, len(sample_text) * 8)
    layout = 'two-column-likely' if widths and sum(1 for l,r in widths if l > 20 and r > 20) >= max(1, len(widths)//2) else 'single-column-or-mixed'
    meta = getattr(reader, 'metadata', None)
    return Diagnostics(
        pages=pages,
        encrypted=encrypted,
        text_layer=text_layer,
        document_type='born-digital' if text_layer else 'scanned-or-image-only',
        layout=layout,
        metadata_available=bool(meta),
        ocr_required=not text_layer,
        confidence={
            'text': 'high' if text_layer else 'low',
            'structure': 'medium' if text_layer else 'low',
            'references': 'medium' if text_layer else 'low',
            'tables': 'low',
        },
    )
