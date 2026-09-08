from paper2context.extraction import extract_structure
from paper2context.references import extract_references

def test_references(sample_pdf):
    sections,_,_,_=extract_structure(sample_pdf)
    refs=extract_references(sections)
    assert len(refs)>=1
    assert any(r.year==2009 for r in refs)
    assert any(r.doi=='10.1234/example.2024.1' for r in refs)
