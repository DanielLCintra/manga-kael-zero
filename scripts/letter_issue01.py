#!/usr/bin/env python3
"""
Lettering compositor for Kael Zero #1.
Draws speech balloons with tails pointing to speaker anchors.
Page art should be clean (minimal/no baked-in dialogue).
"""
from __future__ import annotations

import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "ISSUES" / "01" / "pages"
OUT = ROOT / "ISSUES" / "01" / "pages_lettered"
ASSETS = Path("/opt/cursor/artifacts/assets")

# Balloon entries: page, text, speaker_xy (tail target as fraction of W,H),
# bubble_xy (bubble center as fraction), kind: speech|narration|caption|phone|sfx
# Optional: panel hint only for humans

LETTERING: dict[int, list[dict]] = {
    1: [
        {
            "text": "Eu tentei de tudo...",
            "kind": "caption",
            "bubble": (0.50, 0.14),
            "tail": None,
        },
        {
            "text": "Ele achou que sabia o que aquilo significava.\nA casa deixou ele acreditar.",
            "kind": "narration",
            "bubble": (0.50, 0.88),
            "tail": None,
        },
        {
            "text": "SEIS ANOS DEPOIS",
            "kind": "caption",
            "bubble": (0.78, 0.72),
            "tail": None,
        },
    ],
    2: [
        {"text": "KRRRASH", "kind": "sfx", "bubble": (0.72, 0.12), "tail": None},
        {
            "text": "Ai…\nTá. Quase.",
            "kind": "speech",
            "bubble": (0.78, 0.32),
            "tail": (0.55, 0.42),  # Kael
        },
        {
            "text": "Kael! Se você se matar antes da prova de física, eu não vou na sua missa.",
            "kind": "speech",
            "bubble": (0.28, 0.58),
            "tail": (0.32, 0.70),  # Ryo left
        },
        {
            "text": "Relaxa. Você ia só pelo lanche depois.",
            "kind": "speech",
            "bubble": (0.72, 0.58),
            "tail": (0.62, 0.70),  # Kael right
        },
        {
            "text": "…justo.",
            "kind": "speech",
            "bubble": (0.22, 0.72),
            "tail": (0.30, 0.70),  # Ryo in conversation panel — never Maya
        },
    ],
    3: [
        {
            "text": "Plantão esticou de novo. Tem macarrão na geladeira. Por favor, não desmonta a torradeira hoje. Te amo.",
            "kind": "phone",
            "bubble": (0.55, 0.22),
            "tail": None,
            "label": "HELENA",
        },
        {
            "text": "Ela me conhece demais. Assustador.",
            "kind": "speech",
            "bubble": (0.72, 0.42),
            "tail": (0.55, 0.50),  # Kael
        },
        {
            "text": "Skate park depois da última?",
            "kind": "speech",
            "bubble": (0.28, 0.62),
            "tail": (0.32, 0.72),  # Ryo
        },
        {
            "text": "Hoje não dá. Casa vazia… se eu for, acabo abrindo alguma coisa que não devia.",
            "kind": "speech",
            "bubble": (0.72, 0.62),
            "tail": (0.62, 0.72),  # Kael
        },
        {
            "text": "Tipo a torradeira.",
            "kind": "speech",
            "bubble": (0.28, 0.82),
            "tail": (0.32, 0.78),  # Ryo
        },
        {
            "text": "Tipo a torradeira.",
            "kind": "speech",
            "bubble": (0.72, 0.82),
            "tail": (0.62, 0.78),  # Kael
        },
    ],
    4: [
        {
            "text": "Energia não some. Ela só muda de forma. Anotem isso antes que eu cobrem na prova.",
            "kind": "speech",
            "bubble": (0.55, 0.18),
            "tail": (0.45, 0.32),  # Professor
        },
        {"text": "DEPOIS DA AULA", "kind": "caption", "bubble": (0.78, 0.90), "tail": None},
    ],
    5: [
        {
            "text": "…mais um dia de casa sozinha. Que novidade.",
            "kind": "speech",
            "bubble": (0.55, 0.42),
            "tail": (0.48, 0.55),  # Kael
        },
        {
            "text": "Come. Dorme. Existe.\n— Mãe",
            "kind": "caption",
            "bubble": (0.55, 0.68),
            "tail": None,
        },
        {
            "text": "Sim, senhora.",
            "kind": "speech",
            "bubble": (0.70, 0.82),
            "tail": (0.55, 0.88),  # Kael
        },
    ],
    6: [
        {
            "text": "Não foi a geladeira.",
            "kind": "speech",
            "bubble": (0.70, 0.52),
            "tail": (0.50, 0.58),  # Kael
        },
        {"text": "VMM—tik—VMM", "kind": "sfx", "bubble": (0.50, 0.78), "tail": None},
        {
            "text": "…oi?",
            "kind": "speech",
            "bubble": (0.72, 0.88),
            "tail": (0.55, 0.90),  # Kael
        },
    ],
    7: [
        {
            "text": "Se for rato, a gente negocia.",
            "kind": "speech",
            "bubble": (0.65, 0.18),
            "tail": (0.50, 0.28),  # Kael
        },
        {
            "text": "Manutenção… que nunca ninguém manteve.",
            "kind": "speech",
            "bubble": (0.55, 0.82),
            "tail": (0.48, 0.90),  # Kael
        },
    ],
    8: [
        {
            "text": "Tá.\nIsso aqui não é caixa de luz.",
            "kind": "speech",
            "bubble": (0.65, 0.38),
            "tail": (0.48, 0.48),  # Kael
        },
    ],
    9: [
        {
            "text": "…pai?",
            "kind": "speech",
            "bubble": (0.30, 0.55),
            "tail": (0.35, 0.68),  # Kael
        },
    ],
    10: [
        {
            "text": "Se você está lendo isto, o isolamento falhou.\nNão toque no cilindro sem ler o Protocolo Hélice.\n\nSe o leitor for Kael…\ndesculpa.\n\nEu tentei de tudo.",
            "kind": "caption",
            "bubble": (0.50, 0.42),
            "tail": None,
        },
        {
            "text": "…o quê que você tentou?",
            "kind": "speech",
            "bubble": (0.55, 0.88),
            "tail": (0.50, 0.92),  # Kael
        },
    ],
    11: [
        {
            "text": "Um de doze.\nSério, pai?",
            "kind": "speech",
            "bubble": (0.70, 0.18),
            "tail": (0.55, 0.28),  # Kael
        },
        {
            "text": "Eu só… quero ver.\nNão vou mexer. Só ver.",
            "kind": "speech",
            "bubble": (0.70, 0.68),
            "tail": (0.50, 0.78),  # Kael
        },
    ],
    12: [
        {
            "text": "Ei— espera— eu não pedi—",
            "kind": "speech",
            "bubble": (0.70, 0.55),
            "tail": (0.55, 0.65),  # Kael
        },
    ],
    13: [
        {
            "text": "Para! Desliga!",
            "kind": "speech",
            "bubble": (0.70, 0.62),
            "tail": (0.50, 0.72),  # Kael
        },
    ],
    14: [
        {
            "text": "Legal.\nAchei o porão secreto do meu pai e quase desmaiei. Dia normal.",
            "kind": "speech",
            "bubble": (0.55, 0.18),
            "tail": (0.45, 0.32),  # Kael
        },
        {
            "text": "A gente… termina essa conversa depois.",
            "kind": "speech",
            "bubble": (0.55, 0.58),
            "tail": (0.48, 0.68),  # Kael
        },
    ],
    15: [
        {
            "text": "Tudo bem aí?",
            "kind": "phone",
            "bubble": (0.55, 0.35),
            "tail": None,
            "label": "HELENA",
        },
        {
            "text": "Tô bem. Macarrão tava bom.",
            "kind": "phone",
            "bubble": (0.55, 0.55),
            "tail": None,
            "label": "KAEL",
        },
        {
            "text": "…desculpa, mãe.",
            "kind": "speech",
            "bubble": (0.65, 0.82),
            "tail": (0.50, 0.88),  # Kael
        },
    ],
    16: [
        {"text": "MESMA NOITE", "kind": "caption", "bubble": (0.20, 0.08), "tail": None},
        {
            "text": "Ainda tá aí?",
            "kind": "speech",
            "bubble": (0.70, 0.48),
            "tail": (0.55, 0.55),  # Kael
        },
        {
            "text": "…aguardando input.",
            "kind": "hud",
            "bubble": (0.50, 0.68),
            "tail": None,
        },
        {
            "text": "…você ficou.\nClaro que você ficou.",
            "kind": "speech",
            "bubble": (0.65, 0.88),
            "tail": (0.50, 0.90),  # Kael
        },
    ],
    17: [
        # Art: Kael (blue hair) = RIGHT · Helena = LEFT
        {"text": "MANHÃ", "kind": "caption", "bubble": (0.12, 0.05), "tail": None},
        {
            "text": "Você tá gelado. Dormiu direito?",
            "kind": "speech",
            "bubble": (0.28, 0.14),
            "tail": (0.30, 0.28),  # Helena LEFT
        },
        {
            "text": "Mais ou menos. Prova hoje. Cabeça zoada.",
            "kind": "speech",
            "bubble": (0.72, 0.22),
            "tail": (0.68, 0.34),  # Kael RIGHT
        },
        {
            "text": "Sangrou o nariz?",
            "kind": "speech",
            "bubble": (0.28, 0.48),
            "tail": (0.32, 0.56),  # Helena LEFT
        },
        {
            "text": "Não.\nSó… dormi mal.",
            "kind": "speech",
            "bubble": (0.72, 0.52),
            "tail": (0.66, 0.60),  # Kael RIGHT
        },
        {
            "text": "Se passar mal, me liga.\nE Kael… eu sei quando você tá escondendo coisa. Sempre soube.",
            "kind": "speech",
            "bubble": (0.30, 0.74),
            "tail": (0.34, 0.84),  # Helena LEFT
        },
        {
            "text": "Eu sei.",
            "kind": "speech",
            "bubble": (0.72, 0.82),
            "tail": (0.66, 0.88),  # Kael RIGHT
        },
    ],
    18: [
        {
            "text": "…aí eu falei pra ela que não ia— mano. Alô?",
            "kind": "speech",
            "bubble": (0.30, 0.16),
            "tail": (0.35, 0.28),  # Ryo
        },
        {
            "text": "Desculpa. Tô aqui. Continua.",
            "kind": "speech",
            "bubble": (0.72, 0.16),
            "tail": (0.60, 0.28),  # Kael
        },
        {
            "text": "Você tá estranho hoje.",
            "kind": "speech",
            "bubble": (0.30, 0.36),
            "tail": (0.35, 0.40),  # Ryo
        },
        {
            "text": "Dormi três horas. Me julga depois.",
            "kind": "speech",
            "bubble": (0.72, 0.36),
            "tail": (0.60, 0.40),  # Kael
        },
        {
            "text": "Você tá diferente hoje.",
            "kind": "caption",
            "bubble": (0.55, 0.55),
            "tail": None,
        },
        {
            "text": "Diferente como?",
            "kind": "speech",
            "bubble": (0.30, 0.68),
            "tail": (0.40, 0.72),  # Kael
        },
        {
            "text": "Não sei. Só… diferente.",
            "kind": "speech",
            "bubble": (0.72, 0.68),
            "tail": (0.62, 0.72),  # Maya
        },
        {
            "text": "Ah, não…",
            "kind": "speech",
            "bubble": (0.70, 0.90),
            "tail": (0.55, 0.92),  # Kael
        },
    ],
    19: [
        {
            "text": "Sumiu. Claro que sumiu.",
            "kind": "speech",
            "bubble": (0.70, 0.16),
            "tail": (0.55, 0.28),  # Kael
        },
        {
            "text": "OBJECT MODEL: FASTENER\nPHASE: HELIX\nLOW COST / COMPILE?",
            "kind": "hud",
            "bubble": (0.50, 0.45),
            "tail": None,
        },
        {
            "text": "…você consegue fazer um parafuso?\nSó um. Sem drama.",
            "kind": "speech",
            "bubble": (0.70, 0.62),
            "tail": (0.50, 0.70),  # Kael
        },
        {
            "text": "…ok.",
            "kind": "speech",
            "bubble": (0.72, 0.88),
            "tail": (0.55, 0.90),  # Kael
        },
    ],
    20: [
        {
            "text": "Ele… pesa.\nMas parece que eu tô segurando uma mentira.\nPai… o que era isso?",
            "kind": "speech",
            "bubble": (0.55, 0.55),
            "tail": (0.48, 0.68),  # Kael
        },
    ],
    21: [
        {
            "text": "Quarenta e um por cento é ruído.",
            "kind": "speech",
            "bubble": (0.30, 0.62),
            "tail": (0.25, 0.78),  # off voice near left
        },
        {
            "text": "Ruído é como a gente chama o que ainda não quer ver.\nMantém o watch.",
            "kind": "speech",
            "bubble": (0.70, 0.62),
            "tail": (0.78, 0.78),  # Orin off near cuff hand
        },
    ],
    22: [
        {
            "text": "“Eles”?\nQuem é “eles”?",
            "kind": "speech",
            "bubble": (0.70, 0.42),
            "tail": (0.55, 0.52),  # Kael
        },
        {
            "text": "Pai…\no que você deixou em mim?",
            "kind": "speech",
            "bubble": (0.55, 0.68),
            "tail": (0.48, 0.75),  # Kael
        },
        {
            "text": "CONTINUA — Nº 2: PROTOCOLO HÉLICE",
            "kind": "caption",
            "bubble": (0.50, 0.94),
            "tail": None,
        },
    ],
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
    ]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, size=size)
    return ImageFont.load_default()


def wrap(text: str, width: int) -> str:
    lines = []
    for para in text.split("\n"):
        if not para.strip():
            lines.append("")
            continue
        lines.extend(textwrap.wrap(para, width=width) or [""])
    return "\n".join(lines)


def measure(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.ImageFont) -> tuple[int, int]:
    bbox = draw.multiline_textbbox((0, 0), text, font=fnt, spacing=4, align="center")
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def draw_tail(draw: ImageDraw.ImageDraw, bubble_cx: int, bubble_cy: int, bubble_w: int, bubble_h: int, tail_xy: tuple[int, int], fill=(255, 255, 255), outline=(20, 20, 20)):
    tx, ty = tail_xy
    # attach from bottom or nearest edge of bubble toward speaker
    if ty >= bubble_cy:
        base_y = bubble_cy + bubble_h // 2 - 4
    else:
        base_y = bubble_cy - bubble_h // 2 + 4
    base_x = bubble_cx
    # slight offset so tail doesn't cover text center
    if tx < bubble_cx:
        base_x = bubble_cx - bubble_w // 6
    else:
        base_x = bubble_cx + bubble_w // 6
    p1 = (base_x - 14, base_y)
    p2 = (base_x + 14, base_y)
    p3 = (tx, ty)
    draw.polygon([p1, p2, p3], fill=fill, outline=outline)


def draw_balloon(im: Image.Image, item: dict) -> None:
    draw = ImageDraw.Draw(im)
    w, h = im.size
    kind = item["kind"]
    text = item["text"]
    bx = int(item["bubble"][0] * w)
    by = int(item["bubble"][1] * h)

    if kind == "sfx":
        fnt = font(max(28, w // 28), bold=True)
        text = wrap(text, 18)
        tw, th = measure(draw, text, fnt)
        draw.multiline_text((bx - tw // 2, by - th // 2), text, font=fnt, fill=(30, 30, 30), spacing=2, align="center")
        return

    if kind == "hud":
        fnt = font(max(18, w // 45), bold=True)
        text = wrap(text, 28)
        tw, th = measure(draw, text, fnt)
        pad = 16
        x0, y0 = bx - tw // 2 - pad, by - th // 2 - pad
        x1, y1 = bx + tw // 2 + pad, by + th // 2 + pad
        draw.rectangle([x0, y0, x1, y1], fill=(10, 30, 35), outline=(62, 199, 184), width=3)
        draw.multiline_text((bx - tw // 2, by - th // 2), text, font=fnt, fill=(180, 255, 240), spacing=4, align="left")
        return

    if kind == "phone":
        fnt = font(max(18, w // 48))
        label = item.get("label", "")
        body = wrap(text, 26)
        full = f"{label}\n{body}" if label else body
        tw, th = measure(draw, full, fnt)
        pad = 18
        x0, y0 = bx - tw // 2 - pad, by - th // 2 - pad
        x1, y1 = bx + tw // 2 + pad, by + th // 2 + pad
        draw.rounded_rectangle([x0, y0, x1, y1], radius=18, fill=(245, 248, 252), outline=(40, 40, 50), width=3)
        draw.multiline_text((bx - tw // 2, by - th // 2), full, font=fnt, fill=(20, 20, 30), spacing=4, align="left")
        return

    if kind in ("narration", "caption"):
        fnt = font(max(18, w // 48), bold=(kind == "caption"))
        text = wrap(text, 32 if kind == "caption" else 36)
        tw, th = measure(draw, text, fnt)
        pad = 16
        x0, y0 = bx - tw // 2 - pad, by - th // 2 - pad
        x1, y1 = bx + tw // 2 + pad, by + th // 2 + pad
        fill = (250, 250, 245) if kind == "narration" else (20, 20, 20)
        text_fill = (25, 25, 25) if kind == "narration" else (250, 250, 250)
        draw.rectangle([x0, y0, x1, y1], fill=fill, outline=(30, 30, 30), width=2)
        draw.multiline_text((bx - tw // 2, by - th // 2), text, font=fnt, fill=text_fill, spacing=4, align="center")
        return

    # speech
    fnt = font(max(20, w // 46))
    text = wrap(text, 24)
    tw, th = measure(draw, text, fnt)
    pad_x, pad_y = 22, 16
    bw, bh = tw + pad_x * 2, th + pad_y * 2
    x0, y0 = bx - bw // 2, by - bh // 2
    x1, y1 = bx + bw // 2, by + bh // 2

    tail = item.get("tail")
    if tail:
        txy = (int(tail[0] * w), int(tail[1] * h))
        draw_tail(draw, bx, by, bw, bh, txy)

    draw.rounded_rectangle([x0, y0, x1, y1], radius=28, fill=(255, 255, 255), outline=(15, 15, 15), width=3)
    # redraw tail tip over outline seam: fill only polygon again without dark edge on tip
    if tail:
        txy = (int(tail[0] * w), int(tail[1] * h))
        if txy[1] >= by:
            base_y = by + bh // 2 - 4
        else:
            base_y = by - bh // 2 + 4
        base_x = bx - bw // 6 if txy[0] < bx else bx + bw // 6
        draw.polygon([(base_x - 12, base_y), (base_x + 12, base_y), txy], fill=(255, 255, 255))
        draw.line([(base_x - 12, base_y), txy], fill=(15, 15, 15), width=3)
        draw.line([(base_x + 12, base_y), txy], fill=(15, 15, 15), width=3)

    draw.multiline_text((bx - tw // 2, by - th // 2), text, font=fnt, fill=(10, 10, 10), spacing=4, align="center")


def letter_page(page_num: int, src: Path, dst: Path) -> None:
    im = Image.open(src).convert("RGBA")
    # soft top gradient band? skip — just overlay
    base = im.convert("RGB")
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    # draw on RGB copy for simplicity
    work = base.copy()
    for item in LETTERING.get(page_num, []):
        draw_balloon(work, item)
    work.save(dst, quality=92)
    print("lettered", dst.name, f"({len(LETTERING.get(page_num, []))} balloons)")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    # cover: copy only
    cover = PAGES / "page_00_capa.jpg"
    if cover.exists():
        Image.open(cover).convert("RGB").save(OUT / "page_00_capa.jpg", quality=92)

    for i in range(1, 23):
        src = PAGES / f"page_{i:02d}.jpg"
        if not src.exists():
            raise SystemExit(f"missing {src}")
        letter_page(i, src, OUT / f"page_{i:02d}.jpg")


if __name__ == "__main__":
    main()
