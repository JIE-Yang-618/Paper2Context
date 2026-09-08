from paper2context.models import Section,Paragraph
from paper2context.chunking import build_chunks

def test_chunks_keep_pages():
    s=Section('2 Methodology',1,2,3,[Paragraph('A'*200,2,2,'2 Methodology'),Paragraph('B'*200,3,3,'2 Methodology')])
    chunks=build_chunks([s],target_chars=250)
    assert len(chunks)==2
    assert chunks[0].pages==[2]
    assert chunks[1].pages==[3]
