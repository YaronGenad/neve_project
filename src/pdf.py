import os
from typing import List

try:
    from playwright.sync_api import sync_playwright
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    from pypdf import PdfWriter, PdfReader
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False


def save_html(content: str, path: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"   OK {os.path.basename(path)}")


def _make_cover_html(title: str, cover_subtitle: str) -> str:
    return f"""<!DOCTYPE html><html dir="rtl" lang="he"><head><meta charset="UTF-8">
    <style>
        @page{{size:A4;margin:0;}}
        body{{margin:0;display:flex;flex-direction:column;justify-content:center;
        align-items:center;height:100vh;
        background:linear-gradient(135deg,#4a235a,#8e44ad);
        font-family:Arial,sans-serif;color:white;text-align:center;direction:rtl;}}
        h1{{font-size:40px;margin-bottom:10px;font-weight:800;}}
        h2{{font-size:24px;font-weight:400;opacity:0.9;margin-bottom:20px;}}
        .badge{{background:rgba(255,255,255,0.2);padding:8px 20px;
        border-radius:16px;font-size:14px;margin:4px;display:inline-block;}}
    </style></head><body>
    <div style="font-size:60px;margin-bottom:16px;">&#128218;</div>
    <h1>א"ל השד"ה</h1>
    <h2>{title}</h2>
    <div class="badge">{cover_subtitle}</div>
    <div class="badge">הבנה | שיטות | דיוק | אוצר מילים</div>
    </body></html>"""


def _html_to_pdf(page, html_content: str, output_path: str):
    """Render HTML string to PDF using an already-open Playwright page."""
    page.set_content(html_content, wait_until="domcontentloaded")
    page.wait_for_timeout(300)
    page.pdf(
        path=output_path,
        format="A4",
        margin={"top": "1.4cm", "bottom": "1.4cm",
                "left": "1.6cm", "right": "1.6cm"},
        print_background=True,
    )


def _merge_pdfs(pdf_paths: List[str], output_path: str):
    writer = PdfWriter()
    for path in pdf_paths:
        if path and os.path.exists(path):
            reader = PdfReader(path)
            for page in reader.pages:
                writer.add_page(page)
    with open(output_path, "wb") as f:
        writer.write(f)


def make_pdf(html_files: List[str], output_path: str, title: str, cover_subtitle: str = "") -> bool:
    if not PDF_AVAILABLE:
        print("   WARNING: PDF skipped — run: pip install playwright && playwright install chromium")
        return False
    if not PYPDF_AVAILABLE:
        print("   WARNING: PDF skipped — run: pip install pypdf")
        return False

    tmp_pdfs = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()

            # Cover page
            cover_pdf = output_path.replace(".pdf", "_cover_tmp.pdf")
            _html_to_pdf(page, _make_cover_html(title, cover_subtitle), cover_pdf)
            tmp_pdfs.append(cover_pdf)

            # Each station HTML → individual PDF
            for i, html_file in enumerate(html_files):
                if not html_file or not os.path.exists(html_file):
                    continue
                with open(html_file, "r", encoding="utf-8") as fh:
                    html_content = fh.read()
                station_pdf = output_path.replace(".pdf", f"_part{i}_tmp.pdf")
                _html_to_pdf(page, html_content, station_pdf)
                tmp_pdfs.append(station_pdf)

            browser.close()

        # Merge all individual PDFs
        _merge_pdfs(tmp_pdfs, output_path)

        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"   OK PDF: {os.path.basename(output_path)} ({size_mb:.1f} MB)")
        return True

    except Exception as e:
        print(f"   ERROR PDF failed: {e}")
        return False

    finally:
        for p in tmp_pdfs:
            try:
                os.remove(p)
            except OSError:
                pass
