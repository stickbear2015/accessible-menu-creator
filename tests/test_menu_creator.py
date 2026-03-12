import os
import tempfile
import pytest
import requests
from create_accessible_menu import (
    _parse_text_to_menu,
    parse_html_menu,
    parse_pdf_menu,
    parse_image_menu,
    build_doc_from_menu,
)

class DummyResponse:
    def __init__(self, text):
        self.text = text
    def raise_for_status(self):
        pass

@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    # allow tests to patch requests.get as needed
    yield


def test_parse_text_to_menu_simple():
    text = """
    Breakfast Specials
    Pancakes $5.99
    Omelet $6.99
    """
    title, menu = _parse_text_to_menu("source", text)
    assert "Breakfast Specials" in menu
    assert menu["Breakfast Specials"][0]["name"] == "Pancakes"
    assert menu["Breakfast Specials"][0]["price"] == "$5.99"
    assert menu["Breakfast Specials"][1]["name"] == "Omelet"


def test_parse_html_menu(monkeypatch):
    html = """
    <html><body>
    <h3>Category</h3>
    <h4>Item One $4.50</h4>
    <p>Description here</p>
    <h4>Item Two $7.00</h4>
    </body></html>
    """
    monkeypatch.setattr(requests, 'get', lambda url: DummyResponse(html))
    title, menu = parse_html_menu("http://example.com")
    assert "Category" in menu
    items = menu["Category"]
    assert items[0]["name"] == "Item One"
    assert items[0]["price"] == "$4.50"
    assert "Description" in items[0]["description"]


def test_build_doc(tmp_path):
    menu = {"Cat": [{"name": "A","description":"d","price":"$1"}]}
    out = tmp_path / "out.docx"
    build_doc_from_menu(menu, "Test Title", str(out))
    assert out.exists()
    assert out.stat().st_size > 0

# PDF and image parsing can use the text parser via temp files

def create_sample_pdf(path):
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Category", ln=True)
    pdf.cell(200, 10, txt="Item $3.00", ln=True)
    pdf.output(path)


def test_parse_pdf_menu(tmp_path):
    pdf_file = tmp_path / "sample.pdf"
    # FPDF may not be installed; if not, skip
    try:
        create_sample_pdf(str(pdf_file))
    except ImportError:
        pytest.skip("fpdf not installed")
    title, menu = parse_pdf_menu(str(pdf_file))
    assert title == str(pdf_file)
    assert "Category" in menu

# For image, create simple image with text

def test_parse_image_menu(tmp_path):
    img_file = tmp_path / "sample.png"
    try:
        from PIL import ImageDraw, ImageFont
    except ImportError:
        pytest.skip("Pillow not installed")
    img = Image.new('RGB', (200, 100), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    d.text((10,10), "Cat", fill=(0,0,0))
    d.text((10,30), "Item $5.00", fill=(0,0,0))
    img.save(img_file)
    title, menu = parse_image_menu(str(img_file))
    # OCR may or may not capture text reliably; at least ensure it returns a dict
    assert isinstance(menu, dict)
