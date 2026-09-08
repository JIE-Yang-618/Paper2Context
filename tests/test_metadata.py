from paper2context.extraction import extract_structure
from paper2context.metadata import extract_metadata

def test_metadata(sample_pdf):
    _,_,pages,_=extract_structure(sample_pdf)
    m=extract_metadata(sample_pdf,pages[0])
    assert m['title']=='Forecasting Volatility with Small Models'
    assert 'Ada Researcher' in m['authors_raw']
    assert 'volatility' in [x.lower() for x in m['keywords']]
