from __future__ import annotations
from .models import Section, Chunk
from .utils import slug, estimate_tokens

def build_chunks(sections: list[Section], target_chars: int=3200) -> list[Chunk]:
    out=[]
    seq=0
    for sec in sections:
        buf=[]; pages=[]
        def flush():
            nonlocal seq,buf,pages
            if not buf: return
            seq+=1
            text='\n\n'.join(buf).strip()
            out.append(Chunk(f"{slug(sec.title)}_{seq:04d}",sec.title,sorted(set(pages)),text,estimate_tokens(text)))
            buf=[]; pages=[]
        for p in sec.paragraphs:
            if buf and sum(len(x) for x in buf)+len(p.text)>target_chars: flush()
            buf.append(p.text); pages.extend(range(p.page_start,p.page_end+1))
        flush()
    return out
