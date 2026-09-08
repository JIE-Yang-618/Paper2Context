from __future__ import annotations
import re
from .models import Section, Reference
DOI_RE=re.compile(r'10\.\d{4,9}/[-._;()/:A-Z0-9]+',re.I)
YEAR_RE=re.compile(r'\b(19|20)\d{2}\b')

def extract_references(sections: list[Section]) -> list[Reference]:
    refs=[]
    ref_sections=[s for s in sections if re.search(r'\b(references|bibliography)\b',s.title,re.I)]
    for s in ref_sections:
        for p in s.paragraphs:
            chunks=re.split(r'\n(?=(?:\[?\d+\]?\.?\s+|[A-Z][A-Za-z\-]+,))',p.text)
            for raw in chunks:
                raw=' '.join(raw.split())
                if len(raw)<20: continue
                ym=YEAR_RE.search(raw); dm=DOI_RE.search(raw)
                refs.append(Reference(raw=raw,page=p.page_start,year=int(ym.group(0)) if ym else None,doi=dm.group(0).rstrip('.,;)') if dm else None))
    return refs
