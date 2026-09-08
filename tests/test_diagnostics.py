from paper2context.diagnostics import inspect_pdf

def test_inspect_born_digital(sample_pdf):
    d=inspect_pdf(sample_pdf)
    assert d.pages==4
    assert d.text_layer is True
    assert d.ocr_required is False
    assert d.document_type=='born-digital'

def test_inspect_image_only(image_only_pdf):
    d=inspect_pdf(image_only_pdf)
    assert d.text_layer is False
    assert d.ocr_required is True

def test_encrypted_pdf_reports_clear_error(sample_pdf,tmp_path):
    import pytest
    from pypdf import PdfReader,PdfWriter
    from paper2context.diagnostics import PDFInspectionError
    reader=PdfReader(str(sample_pdf)); writer=PdfWriter()
    for page in reader.pages: writer.add_page(page)
    writer.encrypt('secret')
    locked=tmp_path/'locked.pdf'
    with locked.open('wb') as f: writer.write(f)
    with pytest.raises(PDFInspectionError,match='password'):
        inspect_pdf(locked)
