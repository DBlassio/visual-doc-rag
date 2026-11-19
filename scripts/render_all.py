"""Render every PDF in data/raw to page images in data/pages and print a summary."""

import sys

from docrag.config import pages_dir, raw_dir
from docrag.render import render_pdf


def main() -> int:
    pdfs = sorted(raw_dir().glob("*.pdf"))
    if not pdfs:
        print(f"No PDFs found in {raw_dir()}. Nothing to do.")
        return 1

    total, blank = 0, 0
    for pdf in pdfs:
        pages = render_pdf(pdf, pages_dir())
        n_blank = sum(p.is_blank for p in pages)
        total += len(pages)
        blank += n_blank
        print(f"{pdf.name}: {len(pages)} pages, {n_blank} blank")

    print(f"TOTAL: {len(pdfs)} PDFs, {total} pages, {blank} blank")
    return 0


if __name__ == "__main__":
    sys.exit(main())
