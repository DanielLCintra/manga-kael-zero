#!/usr/bin/env python3
"""Carimba o crédito de autor nas capas das revistas."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

ROOT = Path(__file__).resolve().parents[1]
AUTHOR = "Daniel Cintra"
CREDIT = "por Daniel Cintra"

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def stamp(path: Path, out_paths: list[Path]) -> None:
    im = Image.open(path).convert("RGBA")
    w, h = im.size
    # Slight dark band at bottom for legibility
    band_h = max(48, h // 18)
    band = im.crop((0, h - band_h, w, h))
    band = ImageEnhance.Brightness(band).enhance(0.45)
    im.paste(band, (0, h - band_h))

    draw = ImageDraw.Draw(im)
    size = max(18, w // 28)
    font = ImageFont.truetype(FONT, size)
    bbox = draw.textbbox((0, 0), CREDIT, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (w - tw) // 2
    y = h - band_h + (band_h - th) // 2 - 2
    draw.text((x, y), CREDIT, font=font, fill=(245, 245, 245), stroke_width=2, stroke_fill=(0, 0, 0))

    rgb = im.convert("RGB")
    for out in out_paths:
        out.parent.mkdir(parents=True, exist_ok=True)
        if out.suffix.lower() == ".png":
            im.convert("RGBA").save(out)
        else:
            target = rgb
            if "page_00" in out.name:
                target = rgb.resize((1200, 1800), Image.Resampling.LANCZOS)
            target.save(out, quality=94)
        print("stamped", out)


def main() -> None:
    # Issue 1
    capa1 = ROOT / "ISSUES" / "01" / "CAPA.png"
    if capa1.exists():
        stamp(
            capa1,
            [
                capa1,
                ROOT / "ISSUES" / "01" / "pages" / "page_00_capa.jpg",
                ROOT / "ISSUES" / "01" / "pages_clean" / "page_00_capa.jpg",
                ROOT / "ISSUES" / "01" / "pages_lettered" / "page_00_capa.jpg",
            ],
        )

    # Issue 2
    capa2 = ROOT / "ISSUES" / "02" / "CAPA.jpg"
    if capa2.exists():
        stamp(
            capa2,
            [
                capa2,
                ROOT / "ISSUES" / "02" / "pages" / "page_00_capa.jpg",
                ROOT / "ISSUES" / "02" / "pages_clean" / "page_00_capa.jpg",
                ROOT / "ISSUES" / "02" / "pages_lettered" / "page_00_capa.jpg",
            ],
        )


if __name__ == "__main__":
    main()
