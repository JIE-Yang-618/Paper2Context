from __future__ import annotations
import re
from collections import Counter
from pathlib import Path
import pdfplumber
from .models import Paragraph, Section, Asset
from .utils import clean_text

SECTION_PATTERNS = [
    re.compile(r'^(\d+(?:\.\d+)*)\s+[A-Z][^\n]{1,120}$'),
    re.compile(r'^(?:ABSTRACT|INTRODUCTION|BACKGROUND|RELATED WORK|LITERATURE REVIEW|METHODOLOGY|METHODS?|DATA|RESULTS?|DISCUSSION|CONCLUSION|CONCLUSIONS|REFERENCES|BIBLIOGRAPHY|APPENDIX)\s*$', re.I),
]
CAPTION_RE = re.compile(r'^(Figure|Fig\.|Table)\s*([A-Za-z0-9.\-]+)\s*[:.\-]?\s*(.*)$', re.I)

def _normalize_line(s: str) -> str:
    return re.sub(r'\s+', ' ', s.strip())

def _header_footer_candidates(page_lines: list[list[str]]) -> set[str]:
    c = Counter()
    for lines in page_lines:
        if not lines: continue
        # Count a candidate at most once per page. On short pages the first/last
        # slices overlap; double-counting would incorrectly classify unique text
        # (for example a one-line References heading) as a repeated footer.
        candidates = {_normalize_line(x) for x in (lines[:2] + lines[-2:])}
        for n in candidates:
            if n and len(n) < 140: c[n] += 1
    threshold = max(2, round(len(page_lines) * 0.5))
    return {k for k,v in c.items() if v >= threshold}

def _is_heading(line: str) -> tuple[bool,int]:
    s = _normalize_line(line)
    for p in SECTION_PATTERNS:
        m = p.match(s)
        if m:
            if m.lastindex and m.group(1) and m.group(1)[0].isdigit():
                return True, min(4, m.group(1).count('.') + 1)
            return True, 1
    if 3 <= len(s) <= 90 and s.isupper() and len(s.split()) <= 12:
        return True, 1
    return False, 0

def extract_structure(path: Path) -> tuple[list[Section], list[Asset], list[str], list[str]]:
    warnings: list[str] = []
    with pdfplumber.open(str(path)) as pdf:
        raw_pages = [(page.extract_text(x_tolerance=2, y_tolerance=3) or '') for page in pdf.pages]
        page_lines = [t.splitlines() for t in raw_pages]
        repeats = _header_footer_candidates(page_lines)
        cleaned_pages: list[str] = []
        assets: list[Asset] = []
        for idx, lines in enumerate(page_lines, start=1):
            kept=[]
            for line in lines:
                n=_normalize_line(line)
                if n in repeats: continue
                if re.fullmatch(r'(?:page\s*)?\d+', n, re.I): continue
                kept.append(line)
                cm=CAPTION_RE.match(n)
                if cm:
                    assets.append(Asset(kind='figure' if cm.group(1).lower().startswith('fig') else 'table', label=f"{cm.group(1)} {cm.group(2)}", caption=cm.group(3).strip(), page=idx))
            cleaned_pages.append(clean_text('\n'.join(kept)))

    sections: list[Section] = []
    current = Section(title='Front Matter', level=1, page_start=1, page_end=1)
    sections.append(current)
    for pageno, text in enumerate(cleaned_pages, start=1):
        current.page_end = pageno
        lines = text.splitlines()
        buffer: list[str] = []
        def flush():
            nonlocal buffer, current
            if buffer:
                txt=clean_text('\n'.join(buffer))
                if txt:
                    current.paragraphs.append(Paragraph(txt,pageno,pageno,current.title))
                buffer=[]
        for line in lines:
            is_head, level = _is_heading(line)
            if is_head:
                flush()
                current = Section(title=_normalize_line(line), level=level, page_start=pageno, page_end=pageno)
                sections.append(current)
            elif not line.strip():
                flush()
            else:
                buffer.append(line)
        flush()
    # merge overly fragmented paragraphs caused by line breaks
    for s in sections:
        merged=[]
        for para in s.paragraphs:
            para.text = re.sub(r'(?<![.!?:;])\n(?=\S)', ' ', para.text)
            para.text = clean_text(para.text)
            if para.text: merged.append(para)
        s.paragraphs=merged
    return sections, assets, cleaned_pages, warnings
