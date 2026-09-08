from __future__ import annotations
import argparse, json, sys, importlib.util
from dataclasses import asdict
from pathlib import Path
from . import __version__
from .diagnostics import inspect_pdf, PDFInspectionError
from .service import convert_pdf, build_document

def _p(path): return Path(path).expanduser().resolve()

def parser():
    p=argparse.ArgumentParser(prog='paper2context',description='Turn academic PDFs into provenance-rich AI context packs.')
    p.add_argument('--version',action='version',version=f'paper2context {__version__}')
    s=p.add_subparsers(dest='cmd')
    i=s.add_parser('inspect',help='Inspect PDF readiness'); i.add_argument('pdf'); i.add_argument('--json',action='store_true')
    c=s.add_parser('convert',help='Convert a PDF into a context pack'); c.add_argument('pdf'); c.add_argument('-o','--output')
    m=s.add_parser('metadata',help='Print extracted metadata'); m.add_argument('pdf')
    st=s.add_parser('structure',help='Print detected section map'); st.add_argument('pdf')
    r=s.add_parser('references',help='Print detected references'); r.add_argument('pdf')
    f=s.add_parser('figures',help='Print detected figure/table captions'); f.add_argument('pdf')
    s.add_parser('doctor',help='Check runtime dependencies')
    return p

def main(argv=None):
    argv=list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0].lower().endswith('.pdf'): argv=['convert']+argv
    args=parser().parse_args(argv)
    try:
        if args.cmd=='doctor':
            mods=['pdfplumber','pypdf']; ok=True
            print(f'Paper2Context {__version__}')
            for m in mods:
                present=importlib.util.find_spec(m) is not None; ok &= present; print(f"{'✓' if present else '✗'} {m}")
            print('✓ local-only: no network or API key required')
            return 0 if ok else 1
        if not args.cmd: parser().print_help(); return 0
        path=_p(args.pdf)
        if args.cmd=='inspect':
            d=inspect_pdf(path); obj=asdict(d)
            if args.json: print(json.dumps(obj,indent=2))
            else:
                print(f'Pages: {d.pages}\nText layer: {"available" if d.text_layer else "not found"}\nDocument type: {d.document_type}\nLayout: {d.layout}\nOCR required: {"yes" if d.ocr_required else "no"}')
            return 0
        if args.cmd=='convert':
            doc,out=convert_pdf(path, _p(args.output) if getattr(args,'output',None) else None)
            print(f'✓ {doc.diagnostics.pages} pages processed\n✓ {len(doc.sections)} sections detected\n✓ {len(doc.assets)} figure/table captions\n✓ {len(doc.references)} references\n✓ {len(doc.chunks)} AI context chunks\n\nOutput: {out}')
        else:
            doc=build_document(path)
            if args.cmd=='metadata': print(json.dumps(doc.metadata,ensure_ascii=False,indent=2))
            elif args.cmd=='structure':
                for s in doc.sections: print(f'{s.title}\tpp. {s.page_start}-{s.page_end}')
            elif args.cmd=='references':
                for idx,r in enumerate(doc.references,1): print(f'[{idx}] p.{r.page} {r.raw}')
            elif args.cmd=='figures':
                for a in doc.assets: print(f'{a.label}\tp.{a.page}\t{a.caption}')
        return 0
    except PDFInspectionError as e:
        print(f'error: {e}',file=sys.stderr); return 2

if __name__=='__main__': raise SystemExit(main())
