import json
import pytest
from paper2context.service import convert_pdf
from paper2context.diagnostics import PDFInspectionError

def test_full_conversion(sample_pdf,tmp_path):
    out=tmp_path/'out'
    doc,path=convert_pdf(sample_pdf,out)
    for name in ['PAPER.md','PAPER_CONTEXT.md','metadata.json','structure.json','references.json','assets.json','chunks.jsonl','manifest.json']:
        assert (out/name).exists()
    manifest=json.loads((out/'manifest.json').read_text())
    assert len(manifest['source_sha256'])==64
    assert manifest['pages']==4
    assert '<!-- source: p.' in (out/'PAPER.md').read_text()

def test_scanned_pdf_stops(image_only_pdf,tmp_path):
    with pytest.raises(PDFInspectionError,match='OCR'):
        convert_pdf(image_only_pdf,tmp_path/'out')
