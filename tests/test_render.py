import pytest
from PIL import Image, ImageDraw

from docrag.render import is_blank, render_pdf


def make_pdf(path, n_pages: int, blank_last: bool = False):
    """Build a small PDF with Pillow (no external fixtures needed)."""
    imgs = []
    for i in range(n_pages):
        img = Image.new("RGB", (300, 400), "white")
        if not (blank_last and i == n_pages - 1):
            ImageDraw.Draw(img).rectangle([40, 40, 260, 120], fill="black")
        imgs.append(img)
    imgs[0].save(path, save_all=True, append_images=imgs[1:])


def test_render_returns_one_entry_per_page(tmp_path):
    pdf = tmp_path / "report.pdf"
    make_pdf(pdf, 3)
    pages = render_pdf(pdf, tmp_path / "out")
    assert [p.page_number for p in pages] == [1, 2, 3]
    assert all(p.path.is_file() for p in pages)
    assert all(p.doc_id == "report" for p in pages)


def test_blank_page_is_flagged_not_dropped(tmp_path):
    # Silent-failure guard: blank pages must be visible, not silently indexed.
    pdf = tmp_path / "r.pdf"
    make_pdf(pdf, 2, blank_last=True)
    pages = render_pdf(pdf, tmp_path / "out")
    assert [p.is_blank for p in pages] == [False, True]


def test_missing_pdf_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        render_pdf(tmp_path / "nope.pdf", tmp_path / "out")


def test_dpi_changes_resolution(tmp_path):
    # Index-time and query-time DPI must match: make the dependency explicit.
    pdf = tmp_path / "r.pdf"
    make_pdf(pdf, 1)
    low = render_pdf(pdf, tmp_path / "lo", dpi=72)[0]
    high = render_pdf(pdf, tmp_path / "hi", dpi=144)[0]
    assert high.width == pytest.approx(2 * low.width, abs=2)


def test_is_blank_helper():
    assert is_blank(Image.new("RGB", (50, 50), "white"))
    assert not is_blank(Image.new("RGB", (50, 50), "black"))
