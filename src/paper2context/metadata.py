from __future__ import annotations
import re
from pathlib import Path
from pypdf import PdfReader

DOI_RE = re.compile(r'10\.\d{4,9}/[-._;()/:A-Z0-9]+', re.I)

def extract_metadata(path: Path, first_page_text: str) -> dict:
    reader = PdfReader(str(path), strict=False)
    md = reader.metadata or {}
    title = (getattr(md, 'title', None) or md.get('/Title') or '').strip() if md else ''
    author = (getattr(md, 'author', None) or md.get('/Author') or '').strip() if md else ''
    lines = [x.strip() for x in first_page_text.splitlines() if x.strip()]
    if not title and lines:
        title = max(lines[:8], key=len)[:300]
    abstract = ''
    m = re.search(r'(?is)\babstract\b\s*[:\-]?\s*(.+?)(?=\n\s*(?:keywords?|1\.?\s+introduction|introduction)\b)', first_page_text)
    if m: abstract = re.sub(r'\s+', ' ', m.group(1)).strip()
    doi_match = DOI_RE.search(first_page_text)
    keywords = []
    km = re.search(r'(?im)^\s*keywords?\s*[:\-]\s*(.+)$', first_page_text)
    if km: keywords = [x.strip() for x in re.split(r'[,;•]', km.group(1)) if x.strip()]
    return {'title': title or 'Untitled paper', 'authors_raw': author, 'abstract': abstract, 'keywords': keywords, 'doi': doi_match.group(0).rstrip('.,;)') if doi_match else None}
