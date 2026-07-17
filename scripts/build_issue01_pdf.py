#!/usr/bin/env python3
"""Monta o PDF da Revista #1 a partir das páginas em ISSUES/01/pages/."""
from __future__ import annotations

import io
from pathlib import Path

from PIL import Image
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "ISSUES" / "01" / "pages"
OUT = ROOT / "ISSUES" / "01" / "KAEL_ZERO_01_ECO_NO_PISO.pdf"

PAGE_W = 5.5 * 72
PAGE_H = PAGE_W * (4 / 3)


def main() -> None:
    files = []
    for name in ("page_00_capa.jpg", "page_00_capa.png"):
        p = PAGES / name
        if p.exists():
            files.append(p)
            break
    else:
        raise SystemExit("capa não encontrada")

    for i in range(1, 25):
        for ext in (".jpg", ".png"):
            p = PAGES / f"page_{i:02d}{ext}"
            if p.exists():
                files.append(p)
                break
        else:
            raise SystemExit(f"página {i} não encontrada")

    c = canvas.Canvas(str(OUT), pagesize=(PAGE_W, PAGE_H))
    c.setTitle("KAEL ZERO — Revista Nº 1: Eco no Piso")
    c.setAuthor("Kael Zero")
    c.setSubject("Mangá / HQ — origem")

    for path in files:
        im = Image.open(path).convert("RGB")
        iw, ih = im.size
        img_aspect = iw / ih
        page_aspect = PAGE_W / PAGE_H
        if img_aspect > page_aspect:
            draw_w, draw_h = PAGE_W, PAGE_W / img_aspect
        else:
            draw_h, draw_w = PAGE_H, PAGE_H * img_aspect
        x = (PAGE_W - draw_w) / 2
        y = (PAGE_H - draw_h) / 2
        c.setFillColorRGB(0, 0, 0)
        c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        buf = io.BytesIO()
        im.save(buf, format="JPEG", quality=92, optimize=True)
        buf.seek(0)
        c.drawImage(
            ImageReader(buf), x, y, width=draw_w, height=draw_h, preserveAspectRatio=True
        )
        c.showPage()
        print("ok", path.name)

    c.save()
    print("wrote", OUT, f"({OUT.stat().st_size / 1024 / 1024:.2f} MB)")


if __name__ == "__main__":
    main()
