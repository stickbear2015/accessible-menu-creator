# Accessible Menu Creator

This tool converts restaurant menu content from **web URLs**, **PDFs**, or **images** into a fully accessible Microsoft Word (.docx) document. The generated Word file uses semantic headings, clear descriptions, and complies with WCAG/Office accessibility best practices.

## Features

- Accepts input from:
  - HTML pages (any menu, not just breakfast or lunch)
  - PDF files containing menu text
  - Images (JPEG/PNG) via OCR (Tesseract)
- Parses categories, item names, descriptions, and prices
- Produces Word documents with:
  - Document title and metadata
  - Hierarchical headings (H1, H2), price appended to item titles
  - Paragraphs for descriptions
  - Automatic notes section with allergy warnings
- Command‑line interface; no IDE required
- Outputs file path of generated document

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/stickbear2015/accessible-menu-creator.git
   cd accessible-menu-creator
   ```

2. **Set up Python environment** (tested with Python 3.12+)
   ```bash
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1   # Windows PowerShell
   # or source .venv/bin/activate    # macOS / Linux
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
   > Requirements include `python-docx`, `requests`, `beautifulsoup4`, `pdfplumber`, `pillow`, `pytesseract`.

3. **Tesseract OCR** (for image support)
   - Install Tesseract executable on your system:
     - Windows: [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract)
     - macOS: `brew install tesseract`
     - Linux: `sudo apt install tesseract-ocr`

## Usage

Run the script directly from the command line:

```bash
python create_accessible_menu.py --url "https://example.com/menu" -o mymenu.docx

# or convert a PDF
python create_accessible_menu.py --pdf menu.pdf -o mymenu.docx

# or an image file
python create_accessible_menu.py --image menu.png -o mymenu.docx
```

Only one of `--url`, `--pdf`, or `--image` should be provided per run. The output file defaults to `menu.docx` but can be overridden with `-o`.

### Notes
- HTML parsing uses heuristics (headings `h2`/`h3`/`h4`) and may require manual editing for highly nonstandard pages.
- PDF and image parsing perform simple regex-based extraction; the resulting document may need light proofreading.
- The script includes an example `parse_html_menu` for the Akron Family Restaurant site but is generic enough for most menus.

## Running Without VS Code
This is a standalone script. After installing the dependencies and Tesseract, you can run it from any terminal session. It does not depend on VS Code or other editors.

## Repository Structure

- `create_accessible_menu.py` &ndash; main script and CLI
- `requirements.txt` &ndash; Python dependencies
- `README.md` &ndash; this documentation

## License

MIT License. Feel free to adapt and share.
