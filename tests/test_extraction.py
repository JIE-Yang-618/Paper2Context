from paper2context.extraction import extract_structure

def test_sections_and_headers(sample_pdf):
    sections,assets,pages,warnings=extract_structure(sample_pdf)
    names=[s.title for s in sections]
    assert '1 Introduction' in names
    assert '2 Methodology' in names
    assert '2.1 HAR Model' in names
    assert 'References' in names
    all_text=' '.join(pages)
    assert 'Journal of Synthetic Finance' not in all_text
    assert len(assets)==2
    assert assets[0].page==2

def test_short_last_page_not_mistaken_for_repeated_footer(tmp_path):
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    p=tmp_path/'short-last-page.pdf'; c=canvas.Canvas(str(p),pagesize=letter)
    c.drawString(50,740,'1 Introduction'); c.drawString(50,710,'Body text.'); c.showPage()
    c.drawString(50,740,'2 Results'); c.drawString(50,710,'More body text.'); c.showPage()
    c.drawString(50,740,'References'); c.drawString(50,710,'Doe, J. (2026). A reference entry.'); c.showPage(); c.save()
    sections,_,pages,_=extract_structure(p)
    assert 'References' in [s.title for s in sections]
    assert 'References' in pages[-1]
