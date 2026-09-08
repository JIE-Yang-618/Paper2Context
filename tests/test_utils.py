from paper2context.utils import sha256_file,clean_text

def test_sha256(sample_pdf):
    h=sha256_file(sample_pdf)
    assert len(h)==64
    int(h,16)

def test_hyphen_cleanup():
    assert clean_text('fore-\ncasting')=='forecasting'
