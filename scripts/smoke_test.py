from __future__ import annotations
import tempfile
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from paper2context.service import convert_pdf

def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root=Path(td); pdf=root/'paper.pdf'; out=root/'context'
        c=canvas.Canvas(str(pdf),pagesize=letter)
        c.setTitle('Smoke Test Paper'); c.setAuthor('Paper2Context')
        c.drawString(50,740,'Smoke Test Paper')
        c.drawString(50,710,'Abstract')
        c.drawString(50,690,'This paper tests deterministic PDF extraction.')
        c.drawString(50,650,'1 Introduction')
        c.drawString(50,630,'The smoke test verifies the release pipeline.')
        c.showPage(); c.save()
        doc,_=convert_pdf(pdf,out)
        required=['PAPER.md','PAPER_CONTEXT.md','manifest.json','chunks.jsonl']
        assert all((out/name).exists() for name in required)
        assert doc.diagnostics.pages==1
        print('Paper2Context smoke test: PASS')
    return 0

if __name__=='__main__': raise SystemExit(main())
