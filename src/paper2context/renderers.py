from __future__ import annotations
import json
from dataclasses import asdict
from pathlib import Path
from .models import PaperDocument

def _dump(path: Path, obj):
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')

def render_all(doc: PaperDocument, out: Path) -> None:
    out.mkdir(parents=True,exist_ok=True)
    (out/'figures').mkdir(exist_ok=True)
    (out/'source').mkdir(exist_ok=True)
    md=[f"# {doc.metadata.get('title','Untitled paper')}",""]
    if doc.metadata.get('authors_raw'): md += [f"**Authors:** {doc.metadata['authors_raw']}",""]
    if doc.metadata.get('abstract'): md += ["## Abstract", "", doc.metadata['abstract'],""]
    for sec in doc.sections:
        if sec.title == 'Front Matter': continue
        md += [('#'*(min(5,sec.level+1)))+' '+sec.title,""]
        for p in sec.paragraphs: md += [p.text, f"<!-- source: p. {p.page_start} -->",""]
    (out/'PAPER.md').write_text('\n'.join(md).strip()+'\n',encoding='utf-8')
    ctx=["# PAPER CONTEXT","",f"**Title:** {doc.metadata.get('title','')}",f"**Source SHA-256:** `{doc.source_sha256}`",f"**Pages:** {doc.diagnostics.pages}",""]
    if doc.metadata.get('authors_raw'): ctx.append(f"**Authors:** {doc.metadata['authors_raw']}")
    if doc.metadata.get('doi'): ctx.append(f"**DOI:** {doc.metadata['doi']}")
    ctx += ["","## Extraction confidence",""]
    for k,v in doc.diagnostics.confidence.items(): ctx.append(f"- {k}: **{v}**")
    ctx += ["","## Section map",""]
    for s in doc.sections:
        if s.title!='Front Matter': ctx.append(f"- {s.title} — pp. {s.page_start}–{s.page_end}")
    ctx += ["","## Assets",""]
    if doc.assets:
        for a in doc.assets: ctx.append(f"- {a.label} (p. {a.page}): {a.caption}")
    else: ctx.append('- No figure/table captions detected.')
    ctx += ["","## References", "", f"Detected references: **{len(doc.references)}**", "", "## AI-ready chunks", "", f"Chunks: **{len(doc.chunks)}**. See `chunks.jsonl`." ]
    (out/'PAPER_CONTEXT.md').write_text('\n'.join(ctx).strip()+'\n',encoding='utf-8')
    _dump(out/'metadata.json',doc.metadata)
    _dump(out/'structure.json',{'sections':[asdict(x) for x in doc.sections]})
    _dump(out/'references.json',[asdict(x) for x in doc.references])
    _dump(out/'assets.json',[asdict(x) for x in doc.assets])
    with (out/'chunks.jsonl').open('w',encoding='utf-8') as f:
        for c in doc.chunks: f.write(json.dumps(asdict(c),ensure_ascii=False)+'\n')
    manifest={'paper2context_version':'0.1.0','source_file':doc.source_file,'source_sha256':doc.source_sha256,'pages':doc.diagnostics.pages,'document_type':doc.diagnostics.document_type,'layout':doc.diagnostics.layout,'extraction':doc.diagnostics.confidence,'warnings':doc.warnings,'outputs':['PAPER.md','PAPER_CONTEXT.md','metadata.json','structure.json','references.json','assets.json','chunks.jsonl']}
    _dump(out/'manifest.json',manifest)
    _dump(out/'source'/'extraction.json',doc.to_dict())
