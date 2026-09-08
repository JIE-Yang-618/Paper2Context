from pathlib import Path
import pytest
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

@pytest.fixture
def sample_pdf(tmp_path: Path) -> Path:
    p=tmp_path/'sample.pdf'
    c=canvas.Canvas(str(p),pagesize=letter)
    c.setTitle('Forecasting Volatility with Small Models')
    c.setAuthor('Ada Researcher; Ben Scholar')
    width,height=letter
    pages=[
        [
            ('Forecasting Volatility with Small Models',16),
            ('Ada Researcher; Ben Scholar',11),
            ('Abstract',12),
            ('We study realized volatility forecasting using a transparent benchmark.',10),
            ('Keywords: volatility; forecasting; finance',10),
            ('1 Introduction',13),
            ('Volatility forecasting is important for risk management and trading.',10),
        ],
        [
            ('2 Methodology',13),
            ('We construct realized volatility from five-minute returns.',10),
            ('2.1 HAR Model',12),
            ('The HAR model uses daily, weekly, and monthly components.',10),
            ('Figure 1: Forecasting pipeline',10),
            ('Table 1: Model comparison',10),
        ],
        [
            ('3 Results',13),
            ('The benchmark remains competitive out of sample.',10),
            ('4 Conclusion',13),
            ('Simple models remain useful baselines.',10),
        ],
        [
            ('References',13),
            ('Corsi, F. (2009). A simple approximate long-memory model of realized volatility. Journal of Financial Econometrics.',9),
            ('Smith, J. (2024). Forecasting with careful benchmarks. doi:10.1234/example.2024.1',9),
        ],
    ]
    for page_num, lines in enumerate(pages,1):
        y=height-60
        c.setFont('Helvetica',9); c.drawString(60,height-25,'Journal of Synthetic Finance')
        c.drawRightString(width-50,25,str(page_num))
        for text,size in lines:
            c.setFont('Helvetica-Bold' if size>=12 else 'Helvetica',size)
            c.drawString(60,y,text)
            y-=28
        c.showPage()
    c.save()
    return p

@pytest.fixture
def image_only_pdf(tmp_path: Path) -> Path:
    from PIL import Image, ImageDraw
    img=Image.new('RGB',(500,700),'white'); d=ImageDraw.Draw(img); d.text((30,30),'Scanned paper page',fill='black')
    image_path=tmp_path/'page.png'; img.save(image_path)
    p=tmp_path/'scan.pdf'
    c=canvas.Canvas(str(p),pagesize=letter); c.drawImage(str(image_path),20,20,width=570,height=750); c.showPage(); c.save()
    return p
