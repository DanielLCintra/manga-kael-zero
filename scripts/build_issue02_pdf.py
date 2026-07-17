#!/usr/bin/env python3
"""Monta o PDF da Revista #2 a partir das páginas em ISSUES/02/pages/."""
from __future__ import annotations

import io
from pathlib import Path

from PIL import Image
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "ISSUES" / "02" / "pages"
CLEAN = ROOT / "ISSUES" / "02" / "pages_clean"
OUT = ROOT / "ISSUES" / "02" / "KAEL_ZERO_02_PROTOCOLO_HELICE.pdf"

PAGE_W = 5.5 * 72
PAGE_H = PAGE_W * (4 / 3)


def main() -> None:
    files = []
    for base in (PAGES, CLEAN):
        for name in ("page_00_capa.jpg", "page_00_capa.png"):
            p = base / name
            if p.exists():
                files.append(p)
                break
        if files:
            break
    if not files:
        raise SystemExit("capa não encontrada")

    for i in range(1, 25):
        p = PAGES / f"page_{i:02d}.jpg"
        if not p.exists():
            raise SystemExit(f"missing {p}")
        files.append(p)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=(PAGE_W, PAGE_H))
    for f in files:
        im = Image.open(f).convert("RGB").resize((900, 1350), Image.Resampling.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, format="JPEG", quality=72, optimize=True)
        buf.seek(0)
        c.drawImage(ImageReader(buf), 0, 0, width=PAGE_W, height=PAGE_H, preserveAspectRatio=True, anchor="c")
        c.showPage()
        print("ok", f.name)
    c.save()
    print(f"wrote {OUT} ({OUT.stat().st_size / 1e6:.2f} MB)")


if __name__ == "__main__":
    main()
