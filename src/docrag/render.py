"""PDF -> page images.

Design rule from Project 1: failures must be loud. A PDF that renders zero pages,
or a page that renders blank, must raise or be reported, never enter the index silently.
"""

from dataclasses import dataclass
from pathlib import Path

import pypdfium2 as pdfium
from PIL import Image

# Rendering resolution is a modelling decision (affects patch count and cost), so it is
# explicit and must be the SAME at indexing time and query time.
DEFAULT_DPI = 144  # pdfium scale = dpi / 72


@dataclass(frozen=True)
class RenderedPage:
    doc_id: str
    page_number: int  # 1-based
    path: Path
    width: int
    height: int
    is_blank: bool


def is_blank(img: Image.Image, threshold: float = 0.999) -> bool:
    """True if at least `threshold` of the pixels are near-white."""
    gray = img.convert("L")
    hist = gray.histogram()
    near_white = sum(hist[245:])  # grayscale levels 245..255
    return near_white / (gray.width * gray.height) >= threshold


def render_pdf(pdf_path: Path, out_dir: Path, dpi: int = DEFAULT_DPI) -> list[RenderedPage]:
    """Render every page of `pdf_path` to PNG in `out_dir/<doc_id>/page_0001.png`.

    Raises FileNotFoundError if the file is missing and ValueError if it has no pages.
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.is_file():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    doc_id = pdf_path.stem
    doc_dir = Path(out_dir) / doc_id
    doc_dir.mkdir(parents=True, exist_ok=True)

    pdf = pdfium.PdfDocument(str(pdf_path))
    try:
        n_pages = len(pdf)
        if n_pages == 0:
            raise ValueError(f"PDF has zero pages: {pdf_path}")

        pages: list[RenderedPage] = []
        for i in range(n_pages):
            img = pdf[i].render(scale=dpi / 72).to_pil().convert("RGB")
            out_path = doc_dir / f"page_{i + 1:04d}.png"
            img.save(out_path)
            pages.append(
                RenderedPage(
                    doc_id=doc_id,
                    page_number=i + 1,
                    path=out_path,
                    width=img.width,
                    height=img.height,
                    is_blank=is_blank(img),
                )
            )
        return pages
    finally:
        pdf.close()
