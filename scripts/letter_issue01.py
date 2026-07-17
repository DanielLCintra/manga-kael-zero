#!/usr/bin/env python3
"""
Lettering profissional — Kael Zero #1 (24 págs).
Regras: balões pequenos, ancorados no TOPO, nunca cobrem rostos;
rabicho aponta para a boca; ordem L→R / T→B (Shooter / lettering clássico).
"""
from __future__ import annotations

import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "ISSUES" / "01" / "pages"
OUT = ROOT / "ISSUES" / "01" / "pages_lettered"
NUM_PAGES = 24

# bubble = centro do balão (fracão); tail = boca do falante (fracão)
# Para speech: bubble.y deve ficar ACIMA da cabeça (tipicamente < tail.y - 0.08)

LETTERING: dict[int, list[dict]] = {
    1: [
        {"text": "PORT HAVEN", "kind": "caption", "bubble": (0.18, 0.06), "tail": None},
        {
            "text": "Adrian?\nCheguei cedo hoje.",
            "kind": "speech",
            "bubble": (0.55, 0.28),
            "tail": (0.48, 0.40),
        },
        {
            "text": "Eu tentei de tudo...",
            "kind": "caption",
            "bubble": (0.50, 0.88),
            "tail": None,
        },
    ],
    2: [
        {
            "text": "Mãe…?\nO pai tá dormindo?",
            "kind": "speech",
            "bubble": (0.28, 0.22),
            "tail": (0.35, 0.38),
        },
        {
            "text": "Vem.\nFica comigo.",
            "kind": "speech",
            "bubble": (0.70, 0.22),
            "tail": (0.62, 0.38),
        },
        {
            "text": "Oficialmente, a causa nunca ficou clara.\nNa vizinhança, alguém murmurou suicídio.\nHelena não discutiu. Só trabalhou.",
            "kind": "narration",
            "bubble": (0.50, 0.62),
            "tail": None,
        },
        {"text": "SEIS ANOS DEPOIS", "kind": "caption", "bubble": (0.72, 0.88), "tail": None},
    ],
    3: [
        {
            "text": "Kael Zero tem dezesseis anos.\nAnda de skate. Conserta o que quebra.\nNão é popular. Não treina luta. Não é herói.",
            "kind": "narration",
            "bubble": (0.50, 0.14),
            "tail": None,
        },
        {"text": "KRRRASH", "kind": "sfx", "bubble": (0.78, 0.36), "tail": None},
        {
            "text": "Ai…\nTá. Quase.",
            "kind": "speech",
            "bubble": (0.78, 0.48),
            "tail": (0.55, 0.58),
        },
        {
            "text": "Beleza. Mais um dia sem incendiar nada.",
            "kind": "speech",
            "bubble": (0.70, 0.78),
            "tail": (0.55, 0.88),
        },
    ],
    4: [
        {
            "text": "Kael! Se você se matar antes da prova de física, eu não vou na sua missa.",
            "kind": "speech",
            "bubble": (0.26, 0.12),
            "tail": (0.32, 0.28),
        },
        {
            "text": "Relaxa. Você ia só pelo lanche depois.",
            "kind": "speech",
            "bubble": (0.74, 0.16),
            "tail": (0.66, 0.30),
        },
        {
            "text": "…justo.",
            "kind": "speech",
            "bubble": (0.26, 0.34),
            "tail": (0.32, 0.40),
        },
        {
            "text": "Poucos amigos. Pouca grana. Muita casa vazia.",
            "kind": "narration",
            "bubble": (0.50, 0.58),
            "tail": None,
        },
    ],
    5: [
        {
            "text": "Plantão esticou de novo. Tem macarrão na geladeira. Por favor, não desmonta a torradeira hoje. Te amo.",
            "kind": "phone",
            "bubble": (0.55, 0.16),
            "tail": None,
            "label": "HELENA",
        },
        {
            "text": "Ela me conhece demais. Assustador.",
            "kind": "speech",
            "bubble": (0.74, 0.36),
            "tail": (0.58, 0.46),
        },
        {
            "text": "Skate park depois da última?",
            "kind": "speech",
            "bubble": (0.26, 0.52),
            "tail": (0.32, 0.64),
        },
        {
            "text": "Hoje não dá. Casa vazia… se eu for, acabo abrindo alguma coisa que não devia.",
            "kind": "speech",
            "bubble": (0.74, 0.54),
            "tail": (0.64, 0.66),
        },
        {
            "text": "Tipo a torradeira.",
            "kind": "speech",
            "bubble": (0.26, 0.74),
            "tail": (0.32, 0.78),
        },
        {
            "text": "Tipo a torradeira.",
            "kind": "speech",
            "bubble": (0.74, 0.74),
            "tail": (0.64, 0.78),
        },
        {
            "text": "Helena é médica. Trabalha demais.\nDesde que Adrian morreu, a casa aprendeu a ficar em silêncio.",
            "kind": "narration",
            "bubble": (0.50, 0.92),
            "tail": None,
        },
    ],
    6: [
        {
            "text": "Energia não some. Ela só muda de forma. Anotem isso antes que eu cobrem na prova.",
            "kind": "speech",
            "bubble": (0.50, 0.10),
            "tail": (0.45, 0.26),
        },
        {"text": "DEPOIS DA AULA", "kind": "caption", "bubble": (0.78, 0.90), "tail": None},
    ],
    7: [
        {
            "text": "…mais um dia de casa sozinha. Que novidade.",
            "kind": "speech",
            "bubble": (0.55, 0.28),
            "tail": (0.48, 0.42),
        },
        {
            "text": "Come. Dorme. Existe.\n— Mãe",
            "kind": "caption",
            "bubble": (0.50, 0.58),
            "tail": None,
        },
        {
            "text": "Sim, senhora.",
            "kind": "speech",
            "bubble": (0.72, 0.76),
            "tail": (0.55, 0.86),
        },
    ],
    8: [
        {
            "text": "Não foi a geladeira.",
            "kind": "speech",
            "bubble": (0.72, 0.40),
            "tail": (0.52, 0.52),
        },
        {"text": "VMM—tik—VMM", "kind": "sfx", "bubble": (0.50, 0.70), "tail": None},
        {
            "text": "…oi?",
            "kind": "speech",
            "bubble": (0.74, 0.82),
            "tail": (0.55, 0.90),
        },
    ],
    9: [
        {
            "text": "Se for rato, a gente negocia.",
            "kind": "speech",
            "bubble": (0.68, 0.10),
            "tail": (0.50, 0.24),
        },
        {
            "text": "Manutenção… que nunca ninguém manteve.",
            "kind": "speech",
            "bubble": (0.55, 0.78),
            "tail": (0.48, 0.90),
        },
    ],
    10: [
        {
            "text": "Tá.\nIsso aqui não é caixa de luz.",
            "kind": "speech",
            "bubble": (0.68, 0.28),
            "tail": (0.48, 0.42),
        },
    ],
    11: [
        {
            "text": "…pai?",
            "kind": "speech",
            "bubble": (0.28, 0.42),
            "tail": (0.35, 0.58),
        },
        {
            "text": "Seis anos. Embaixo da casa dele.\nO silêncio tinha endereço.",
            "kind": "narration",
            "bubble": (0.50, 0.90),
            "tail": None,
        },
    ],
    12: [
        {
            "text": "Se você está lendo isto, o isolamento falhou.\nNão toque no cilindro sem ler o Protocolo Hélice.\n\nSe o leitor for Kael…\ndesculpa.\n\nEu tentei de tudo.",
            "kind": "caption",
            "bubble": (0.50, 0.40),
            "tail": None,
        },
        {
            "text": "…o quê que você tentou?",
            "kind": "speech",
            "bubble": (0.55, 0.86),
            "tail": (0.50, 0.92),
        },
    ],
    13: [
        {
            "text": "Um de doze.\nSério, pai?",
            "kind": "speech",
            "bubble": (0.72, 0.12),
            "tail": (0.55, 0.26),
        },
        {
            "text": "Eu só… quero ver.\nNão vou mexer. Só ver.",
            "kind": "speech",
            "bubble": (0.72, 0.62),
            "tail": (0.52, 0.76),
        },
    ],
    14: [
        {
            "text": "Ei— espera— eu não pedi—",
            "kind": "speech",
            "bubble": (0.72, 0.42),
            "tail": (0.55, 0.58),
        },
    ],
    15: [
        {
            "text": "Para! Desliga!",
            "kind": "speech",
            "bubble": (0.72, 0.52),
            "tail": (0.52, 0.68),
        },
    ],
    16: [
        {
            "text": "Legal.\nAchei o porão secreto do meu pai e quase desmaiei. Dia normal.",
            "kind": "speech",
            "bubble": (0.55, 0.12),
            "tail": (0.45, 0.28),
        },
        {
            "text": "A gente… termina essa conversa depois.",
            "kind": "speech",
            "bubble": (0.55, 0.52),
            "tail": (0.48, 0.66),
        },
    ],
    17: [
        {
            "text": "Tudo bem aí?",
            "kind": "phone",
            "bubble": (0.55, 0.28),
            "tail": None,
            "label": "HELENA",
        },
        {
            "text": "Tô bem. Macarrão tava bom.",
            "kind": "phone",
            "bubble": (0.55, 0.48),
            "tail": None,
            "label": "KAEL",
        },
        {
            "text": "…desculpa, mãe.",
            "kind": "speech",
            "bubble": (0.70, 0.78),
            "tail": (0.52, 0.88),
        },
    ],
    18: [
        {"text": "MESMA NOITE", "kind": "caption", "bubble": (0.18, 0.06), "tail": None},
        {
            "text": "Ainda tá aí?",
            "kind": "speech",
            "bubble": (0.72, 0.40),
            "tail": (0.55, 0.52),
        },
        {
            "text": "…aguardando input.",
            "kind": "hud",
            "bubble": (0.50, 0.62),
            "tail": None,
        },
        {
            "text": "…você ficou.\nClaro que você ficou.",
            "kind": "speech",
            "bubble": (0.68, 0.82),
            "tail": (0.52, 0.90),
        },
    ],
    19: [
        {"text": "MANHÃ", "kind": "caption", "bubble": (0.10, 0.035), "tail": None},
        {
            "text": "Você tá gelado. Dormiu direito?",
            "kind": "speech",
            "bubble": (0.24, 0.07),
            "tail": (0.30, 0.22),
        },
        {
            "text": "Mais ou menos. Prova hoje. Cabeça zoada.",
            "kind": "speech",
            "bubble": (0.76, 0.08),
            "tail": (0.70, 0.22),
        },
        {
            "text": "Sangrou o nariz?",
            "kind": "speech",
            "bubble": (0.24, 0.30),
            "tail": (0.30, 0.42),
        },
        {
            "text": "Não.\nSó… dormi mal.",
            "kind": "speech",
            "bubble": (0.76, 0.30),
            "tail": (0.70, 0.42),
        },
        {
            "text": "Se passar mal, me liga.\nE Kael… eu sei quando você tá escondendo coisa. Sempre soube.",
            "kind": "speech",
            "bubble": (0.28, 0.58),
            "tail": (0.32, 0.72),
        },
        {
            "text": "Eu sei.",
            "kind": "speech",
            "bubble": (0.76, 0.62),
            "tail": (0.70, 0.74),
        },
    ],
    20: [
        {
            "text": "…mano. Alô?",
            "kind": "speech",
            "bubble": (0.26, 0.10),
            "tail": (0.32, 0.24),
        },
        {
            "text": "Desculpa. Tô aqui. Continua.",
            "kind": "speech",
            "bubble": (0.74, 0.10),
            "tail": (0.66, 0.24),
        },
        {
            "text": "Você tá estranho hoje.",
            "kind": "speech",
            "bubble": (0.26, 0.30),
            "tail": (0.32, 0.38),
        },
        {
            "text": "Dormi três horas. Me julga depois.",
            "kind": "speech",
            "bubble": (0.74, 0.30),
            "tail": (0.66, 0.38),
        },
        {
            "text": "Você tá diferente hoje.",
            "kind": "caption",
            "bubble": (0.50, 0.52),
            "tail": None,
        },
        {
            "text": "Diferente como?",
            "kind": "speech",
            "bubble": (0.28, 0.64),
            "tail": (0.40, 0.72),
        },
        {
            "text": "Não sei. Só… diferente.",
            "kind": "speech",
            "bubble": (0.74, 0.64),
            "tail": (0.62, 0.72),
        },
        {
            "text": "Ah, não…",
            "kind": "speech",
            "bubble": (0.72, 0.86),
            "tail": (0.55, 0.92),
        },
    ],
    21: [
        {
            "text": "Sumiu. Claro que sumiu.",
            "kind": "speech",
            "bubble": (0.72, 0.10),
            "tail": (0.55, 0.24),
        },
        {
            "text": "OBJECT MODEL: FASTENER\nPHASE: HELIX\nLOW COST / COMPILE?",
            "kind": "hud",
            "bubble": (0.50, 0.40),
            "tail": None,
        },
        {
            "text": "…você consegue fazer um parafuso?\nSó um. Sem drama.",
            "kind": "speech",
            "bubble": (0.72, 0.58),
            "tail": (0.52, 0.70),
        },
        {
            "text": "…ok.",
            "kind": "speech",
            "bubble": (0.74, 0.84),
            "tail": (0.55, 0.90),
        },
    ],
    22: [
        {
            "text": "Ele… pesa.\nMas parece que eu tô segurando uma mentira.\nPai… o que era isso?",
            "kind": "speech",
            "bubble": (0.55, 0.22),
            "tail": (0.48, 0.42),
        },
    ],
    23: [
        {
            "text": "Quarenta e um por cento é ruído.",
            "kind": "speech",
            "bubble": (0.28, 0.55),
            "tail": (0.22, 0.72),
        },
        {
            "text": "Ruído é como a gente chama o que ainda não quer ver.\nMantém o watch.",
            "kind": "speech",
            "bubble": (0.72, 0.55),
            "tail": (0.80, 0.72),
        },
    ],
    24: [
        {
            "text": "“Eles”?\nQuem é “eles”?",
            "kind": "speech",
            "bubble": (0.72, 0.28),
            "tail": (0.55, 0.42),
        },
        {
            "text": "Pai…\no que você deixou em mim?",
            "kind": "speech",
            "bubble": (0.55, 0.58),
            "tail": (0.48, 0.70),
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
    path = (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    )
    if Path(path).exists():
        return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def wrap(text: str, width: int) -> str:
    lines: list[str] = []
    for para in text.split("\n"):
        if not para.strip():
            lines.append("")
            continue
        lines.extend(textwrap.wrap(para, width=width) or [""])
    return "\n".join(lines)


def measure(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.ImageFont) -> tuple[int, int]:
    bbox = draw.multiline_textbbox((0, 0), text, font=fnt, spacing=3, align="center")
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def face_safe_bubble_y(by: float, tail: tuple[float, float] | None, bh_frac: float = 0.08) -> float:
    """Keep balloon body above the speaker's face/mouth."""
    if not tail:
        return min(by, 0.35)
    # balloon center must sit well above mouth
    max_by = tail[1] - 0.10 - bh_frac
    return min(by, max(0.06, max_by))


def draw_tail(draw, bx, by, bw, bh, txy):
    tx, ty = txy
    base_y = by + bh // 2 - 2
    base_x = bx - bw // 5 if tx < bx else bx + bw // 5
    # short pointer toward mouth — stop before covering face center
    draw.polygon(
        [(base_x - 10, base_y), (base_x + 10, base_y), (tx, ty)],
        fill=(255, 255, 255),
        outline=(20, 20, 20),
    )
    draw.polygon([(base_x - 8, base_y), (base_x + 8, base_y), (tx, ty)], fill=(255, 255, 255))
    draw.line([(base_x - 10, base_y), (tx, ty)], fill=(20, 20, 20), width=2)
    draw.line([(base_x + 10, base_y), (tx, ty)], fill=(20, 20, 20), width=2)


def draw_balloon(im: Image.Image, item: dict) -> None:
    draw = ImageDraw.Draw(im)
    w, h = im.size
    kind = item["kind"]
    text = item["text"]
    bx = int(item["bubble"][0] * w)
    by_frac = item["bubble"][1]
    tail = item.get("tail")

    if kind == "sfx":
        fnt = font(max(22, w // 36), bold=True)
        text = wrap(text, 16)
        tw, th = measure(draw, text, fnt)
        draw.multiline_text((bx - tw // 2, int(by_frac * h) - th // 2), text, font=fnt, fill=(25, 25, 25), align="center")
        return

    if kind == "hud":
        fnt = font(max(15, w // 55), bold=True)
        text = wrap(text, 30)
        tw, th = measure(draw, text, fnt)
        pad = 12
        by = int(by_frac * h)
        draw.rectangle(
            [bx - tw // 2 - pad, by - th // 2 - pad, bx + tw // 2 + pad, by + th // 2 + pad],
            fill=(8, 28, 32),
            outline=(62, 199, 184),
            width=2,
        )
        draw.multiline_text((bx - tw // 2, by - th // 2), text, font=fnt, fill=(170, 250, 235), spacing=3, align="left")
        return

    if kind == "phone":
        fnt = font(max(14, w // 58))
        label = item.get("label", "")
        body = wrap(text, 28)
        full = f"{label}\n{body}" if label else body
        tw, th = measure(draw, full, fnt)
        pad = 12
        by = int(min(by_frac, 0.22) * h)  # phones stay high
        draw.rounded_rectangle(
            [bx - tw // 2 - pad, by - th // 2 - pad, bx + tw // 2 + pad, by + th // 2 + pad],
            radius=14,
            fill=(245, 248, 252),
            outline=(35, 35, 45),
            width=2,
        )
        draw.multiline_text((bx - tw // 2, by - th // 2), full, font=fnt, fill=(15, 15, 25), spacing=3, align="left")
        return

    if kind in ("narration", "caption"):
        fnt = font(max(14, w // 58), bold=(kind == "caption"))
        text = wrap(text, 34)
        tw, th = measure(draw, text, fnt)
        pad = 12
        by = int(by_frac * h)
        fill = (252, 252, 248) if kind == "narration" else (18, 18, 18)
        tfill = (20, 20, 20) if kind == "narration" else (250, 250, 250)
        draw.rectangle(
            [bx - tw // 2 - pad, by - th // 2 - pad, bx + tw // 2 + pad, by + th // 2 + pad],
            fill=fill,
            outline=(25, 25, 25),
            width=2,
        )
        draw.multiline_text((bx - tw // 2, by - th // 2), text, font=fnt, fill=tfill, spacing=3, align="center")
        return

    # speech — smaller, top-biased, face-safe
    fnt = font(max(15, w // 56))
    text = wrap(text, 22)
    tw, th = measure(draw, text, fnt)
    pad_x, pad_y = 14, 10
    bw, bh = tw + pad_x * 2, th + pad_y * 2
    by_frac = face_safe_bubble_y(by_frac, tail, bh / h)
    by = int(by_frac * h)
    # keep balloon inside page
    bx = max(bw // 2 + 8, min(w - bw // 2 - 8, bx))
    by = max(bh // 2 + 8, min(h - bh // 2 - 8, by))

    txy = None
    if tail:
        # aim at mouth but stop short of face center (don't bury tip in eyes)
        tx, ty = int(tail[0] * w), int(tail[1] * h)
        # if balloon would still overlap mouth vertically, push higher
        if by + bh // 2 > ty - int(0.04 * h):
            by = max(bh // 2 + 8, ty - int(0.04 * h) - bh // 2)
        txy = (tx, ty)
        draw_tail(draw, bx, by, bw, bh, txy)

    draw.rounded_rectangle(
        [bx - bw // 2, by - bh // 2, bx + bw // 2, by + bh // 2],
        radius=18,
        fill=(255, 255, 255),
        outline=(18, 18, 18),
        width=2,
    )
    if txy:
        draw_tail(draw, bx, by, bw, bh, txy)
        draw.rounded_rectangle(
            [bx - bw // 2, by - bh // 2, bx + bw // 2, by + bh // 2],
            radius=18,
            fill=(255, 255, 255),
            outline=(18, 18, 18),
            width=2,
        )
    draw.multiline_text((bx - tw // 2, by - th // 2), text, font=fnt, fill=(10, 10, 10), spacing=3, align="center")


def letter_page(page_num: int, src: Path, dst: Path) -> None:
    work = Image.open(src).convert("RGB")
    for item in LETTERING.get(page_num, []):
        draw_balloon(work, item)
    work.save(dst, quality=93)
    print("lettered", dst.name, f"({len(LETTERING.get(page_num, []))} items)")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    cover = PAGES / "page_00_capa.jpg"
    if cover.exists():
        Image.open(cover).convert("RGB").save(OUT / "page_00_capa.jpg", quality=93)

    for i in range(1, NUM_PAGES + 1):
        src = PAGES / f"page_{i:02d}.jpg"
        if not src.exists():
            raise SystemExit(f"missing {src}")
        letter_page(i, src, OUT / f"page_{i:02d}.jpg")


if __name__ == "__main__":
    main()
