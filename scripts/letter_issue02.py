#!/usr/bin/env python3
"""
Lettering profissional — Kael Zero #2 (24 págs).

Garantias do motor:
1. Sempre parte de `pages_clean/` (nunca re-letter em cima de balão).
2. Cada fala declara o PAINEL (bounds) — balão fica preso na zona superior do painel.
3. Rabicho = cunha curta; nunca atravessa gutter nem outro personagem distante.
4. Colisão entre balões no mesmo painel é resolvida automaticamente.
5. QC no fim: falha se balões saírem do painel ou se sobrepuserem demais.
"""
from __future__ import annotations

import math
import sys
import textwrap
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "ISSUES" / "02" / "pages_clean"
PAGES = ROOT / "ISSUES" / "02" / "pages"
OUT = ROOT / "ISSUES" / "02" / "pages_lettered"
NUM_PAGES = 24

# ---------------------------------------------------------------------------
# Dados: cada item tem panel=(x0,y0,x1,y1) em fração da página.
# speaker = boca do falante (fração página). slot = ordem de leitura no painel.
# ---------------------------------------------------------------------------

# Helpers de layout frequentes
P_FULL = (0.02, 0.02, 0.98, 0.98)


def P(x0, y0, x1, y1):
    return (x0, y0, x1, y1)


LETTERING: dict[int, list[dict]] = {
    1: [
        {"text": "Ainda tá quente.", "kind": "speech", "panel": P(0.02, 0.02, 0.98, 0.28), "speaker": (0.55, 0.20), "slot": 0, "pos": (0.72, 0.16)},
        {"text": "Beleza.\nAgora… o resto.", "kind": "speech", "panel": P(0.02, 0.72, 0.98, 0.98), "speaker": (0.55, 0.88), "slot": 0, "pos": (0.72, 0.18)},
    ],
    2: [
        {"text": "MANHÃ", "kind": "caption", "panel": P(0.02, 0.02, 0.26, 0.09), "slot": 0, "pos": (0.50, 0.50)},
        {"text": "Você dormiu?", "kind": "speech", "panel": P(0.28, 0.02, 0.98, 0.28), "speaker": (0.40, 0.18), "slot": 0, "pos": (0.25, 0.14)},
        {"text": "Dormi. Tipo… horizontal.", "kind": "speech", "panel": P(0.28, 0.02, 0.98, 0.28), "speaker": (0.75, 0.20), "slot": 1, "pos": (0.78, 0.14)},
        {"text": "Tá quente.", "kind": "speech", "panel": P(0.02, 0.28, 0.48, 0.50), "speaker": (0.22, 0.40), "slot": 0, "pos": (0.55, 0.14)},
        {"text": "É o sol. Que ainda não nasceu. Lógica Zero.", "kind": "speech", "panel": P(0.50, 0.28, 0.98, 0.50), "speaker": (0.75, 0.42), "slot": 0, "pos": (0.55, 0.14)},
        {"text": "Depois da escola eu te levo no hospital. Check-up rápido.\nNão discute.", "kind": "speech", "panel": P(0.02, 0.50, 0.98, 0.72), "speaker": (0.45, 0.62), "slot": 0, "pos": (0.72, 0.14)},
        {"text": "…sim, senhora.", "kind": "speech", "panel": P(0.02, 0.72, 0.98, 0.98), "speaker": (0.55, 0.88), "slot": 0, "pos": (0.72, 0.16)},
    ],
    3: [
        {"text": "“Não toque no cilindro sem ler o Protocolo…”\nLegal. Eu já toquei.", "kind": "speech", "panel": P(0.02, 0.28, 0.98, 0.52), "speaker": (0.55, 0.42), "slot": 0, "pos": (0.72, 0.14)},
        {"text": "Cadê você ontem? Sumiu do group.", "kind": "speech", "panel": P(0.02, 0.52, 0.98, 0.74), "speaker": (0.28, 0.64), "slot": 0, "pos": (0.22, 0.14)},
        {"text": "Casa. Torradeira. Drama doméstico.", "kind": "speech", "panel": P(0.02, 0.52, 0.98, 0.74), "speaker": (0.70, 0.64), "slot": 1, "pos": (0.78, 0.14)},
        {"text": "…isso não é dever de física.", "kind": "speech", "panel": P(0.02, 0.74, 0.98, 0.98), "speaker": (0.55, 0.88), "slot": 0, "pos": (0.72, 0.16)},
    ],
    4: [
        {"text": "Ela não esquece. Assustador.", "kind": "speech", "panel": P(0.02, 0.28, 0.98, 0.52), "speaker": (0.55, 0.42), "slot": 0, "pos": (0.72, 0.16)},
    ],
    5: [
        {"text": "Um de doze.\nE o resto… cinza.", "kind": "speech", "panel": P(0.02, 0.36, 0.98, 0.62), "speaker": (0.55, 0.50), "slot": 0, "pos": (0.78, 0.14)},
        {"text": "Pai… você escondeu até de mim.", "kind": "speech", "panel": P(0.02, 0.64, 0.98, 0.98), "speaker": (0.55, 0.82), "slot": 0, "pos": (0.72, 0.16)},
    ],
    6: [
        {"text": "Ainda tá aí?", "kind": "speech", "panel": P(0.02, 0.02, 0.98, 0.28), "speaker": (0.45, 0.20), "slot": 0, "pos": (0.72, 0.14)},
        {"text": "RESIDUAL LINK: ACTIVE", "kind": "hud", "panel": P(0.20, 0.18, 0.80, 0.30), "slot": 1},
        {"text": "Me mostra o Protocolo. O resto.", "kind": "speech", "panel": P(0.02, 0.30, 0.98, 0.52), "speaker": (0.45, 0.42), "slot": 0, "pos": (0.72, 0.14)},
        {"text": "INDEX INCOMPLETE\nACCESS: BIOMARKER PARTIAL", "kind": "hud", "panel": P(0.18, 0.40, 0.82, 0.54), "slot": 1},
        {"text": "Ou seja: eu não sou… o bastante.", "kind": "speech", "panel": P(0.02, 0.54, 0.98, 0.74), "speaker": (0.50, 0.66), "slot": 0, "pos": (0.72, 0.14)},
        {"text": "Tá. Então a gente treina.", "kind": "speech", "panel": P(0.02, 0.74, 0.98, 0.98), "speaker": (0.55, 0.88), "slot": 0, "pos": (0.72, 0.16)},
    ],
    7: [
        {"text": "Você fez um parafuso.\nFaz uma chave de verdade?", "kind": "speech", "panel": P(0.02, 0.02, 0.98, 0.28), "speaker": (0.50, 0.20), "slot": 0, "pos": (0.72, 0.14)},
        {"text": "OBJECT MODEL: DRIVER\nPHASE: HELIX\nCOMPILE?", "kind": "hud", "panel": P(0.15, 0.28, 0.85, 0.48), "slot": 0},
        {"text": "…ok.\nCusto continua sendo eu.", "kind": "speech", "panel": P(0.02, 0.72, 0.98, 0.98), "speaker": (0.50, 0.88), "slot": 0, "pos": (0.72, 0.18)},
    ],
    8: [
        {"text": "Hospital às cinco.\nPerfeito timing, universo.", "kind": "speech", "panel": P(0.02, 0.28, 0.98, 0.52), "speaker": (0.55, 0.42), "slot": 0, "pos": (0.72, 0.14)},
    ],
    9: [
        {"text": "Kael! Se eu entrar e achar a torradeira em pedaços—", "kind": "speech", "panel": P(0.02, 0.02, 0.98, 0.28), "speaker": (0.30, 0.18), "slot": 0, "pos": (0.22, 0.14)},
        {"text": "Intacta. Eu juro pelo macarrão.", "kind": "speech", "panel": P(0.02, 0.02, 0.98, 0.28), "speaker": (0.70, 0.20), "slot": 1, "pos": (0.78, 0.14)},
        {"text": "Se for anemia, a gente trata.\nSe for outra coisa… a gente também trata.", "kind": "speech", "panel": P(0.02, 0.52, 0.98, 0.74), "speaker": (0.40, 0.64), "slot": 0, "pos": (0.72, 0.14)},
        {"text": "…outra coisa.", "kind": "speech", "panel": P(0.02, 0.74, 0.98, 0.98), "speaker": (0.55, 0.88), "slot": 0, "pos": (0.72, 0.16)},
    ],
    10: [
        {"text": "HOSPITAL MUNICIPAL — PORT HAVEN", "kind": "caption", "panel": P(0.02, 0.02, 0.70, 0.12), "slot": 0},
    ],
    11: [
        # silent recognition page — optional soft narration
        {"text": "Um menino. Desenhando. Como se o tempo fosse o inimigo.", "kind": "narration", "panel": P(0.02, 0.78, 0.98, 0.98), "slot": 0, "pos": (0.50, 0.55)},
    ],
    12: [
        {"text": "Seu cabelo é… barulhento.", "kind": "speech", "panel": P(0.02, 0.02, 0.98, 0.26), "speaker": (0.35, 0.18), "slot": 0, "pos": (0.72, 0.14)},
        {"text": "É o que todo mundo diz.\nMenos as pessoas educadas.", "kind": "speech", "panel": P(0.02, 0.26, 0.98, 0.50), "speaker": (0.55, 0.40), "slot": 0, "pos": (0.72, 0.14)},
        {"text": "Eu desenho pra passar o tempo.\nHospital é… lento.", "kind": "speech", "panel": P(0.02, 0.50, 0.98, 0.72), "speaker": (0.40, 0.62), "slot": 0, "pos": (0.72, 0.14)},
        {"text": "Kael — vem.", "kind": "speech", "panel": P(0.02, 0.72, 0.98, 0.98), "speaker": (0.25, 0.82), "slot": 0, "pos": (0.22, 0.14)},
        {"text": "…fica bem, tá?", "kind": "speech", "panel": P(0.02, 0.72, 0.98, 0.98), "speaker": (0.55, 0.88), "slot": 1, "pos": (0.78, 0.14)},
    ],
    13: [
        {"text": "…que joia estranha pra hospital.", "kind": "speech", "panel": P(0.02, 0.72, 0.98, 0.98), "speaker": (0.55, 0.88), "slot": 0, "pos": (0.72, 0.16)},
    ],
    14: [
        {"text": "Saturação ok. Pressão um pouco baixa.\nAlguma epistaxe recente?", "kind": "speech", "panel": P(0.02, 0.28, 0.98, 0.52), "speaker": (0.35, 0.40), "slot": 0, "pos": (0.72, 0.14)},
        {"text": "…uma vez. Ar seco.", "kind": "speech", "panel": P(0.02, 0.52, 0.98, 0.74), "speaker": (0.55, 0.64), "slot": 0, "pos": (0.72, 0.14)},
        {"text": "Ar seco. Claro.", "kind": "speech", "panel": P(0.02, 0.74, 0.98, 0.98), "speaker": (0.40, 0.88), "slot": 0, "pos": (0.72, 0.16)},
    ],
    15: [
        {"text": "Doutora Zero — o setor pediátrico agradece a escala de ontem.", "kind": "speech", "panel": P(0.02, 0.02, 0.98, 0.28), "speaker": (0.35, 0.18), "slot": 0, "pos": (0.28, 0.14)},
        {"text": "Foi plantão. Faz parte.", "kind": "speech", "panel": P(0.02, 0.02, 0.98, 0.28), "speaker": (0.70, 0.20), "slot": 1, "pos": (0.78, 0.14)},
    ],
    16: [
        {"text": "NOITE", "kind": "caption", "panel": P(0.02, 0.02, 0.22, 0.10), "slot": 0},
        {"text": "Você viu aquilo também?", "kind": "speech", "panel": P(0.02, 0.28, 0.98, 0.52), "speaker": (0.50, 0.42), "slot": 0, "pos": (0.72, 0.14)},
        {"text": "…dados insuficientes.", "kind": "hud", "panel": P(0.20, 0.40, 0.80, 0.54), "slot": 1},
        {"text": "Hospital. Menino. Pulseira.\nE eu fingindo que tô anêmico.", "kind": "speech", "panel": P(0.02, 0.54, 0.98, 0.76), "speaker": (0.50, 0.66), "slot": 0, "pos": (0.72, 0.14)},
    ],
    17: [
        {"text": "Dois de doze.\nVocê tava com medo de mim… ou por mim?", "kind": "speech", "panel": P(0.02, 0.72, 0.98, 0.98), "speaker": (0.50, 0.88), "slot": 0, "pos": (0.72, 0.16)},
        {"text": "02/12 — MATÉRIA / CUSTO BIOLÓGICO", "kind": "caption", "panel": P(0.10, 0.28, 0.90, 0.42), "slot": 0},
    ],
    18: [
        {"text": "Mais uma. Só mais uma.\nSem drama.", "kind": "speech", "panel": P(0.02, 0.02, 0.98, 0.28), "speaker": (0.50, 0.18), "slot": 0, "pos": (0.72, 0.14)},
        {"text": "WARNING: CHANNEL STRAIN", "kind": "hud", "panel": P(0.18, 0.52, 0.82, 0.68), "slot": 0},
        {"text": "…eu ouvi.\nMeça. Sempre meça.", "kind": "speech", "panel": P(0.02, 0.72, 0.98, 0.98), "speaker": (0.50, 0.88), "slot": 0, "pos": (0.72, 0.16)},
    ],
    19: [
        {"text": "Subiu.", "kind": "speech", "panel": P(0.02, 0.28, 0.98, 0.50), "speaker": (0.30, 0.40), "slot": 0, "pos": (0.22, 0.14)},
        {"text": "Ainda pode ser ruído doméstico.", "kind": "speech", "panel": P(0.02, 0.28, 0.98, 0.50), "speaker": (0.70, 0.42), "slot": 1, "pos": (0.78, 0.14)},
        {"text": "Ruído não materializa ferramenta duas vezes.", "kind": "speech", "panel": P(0.02, 0.50, 0.98, 0.72), "speaker": (0.35, 0.62), "slot": 0, "pos": (0.72, 0.14)},
        {"text": "…vivo. Intact.", "kind": "speech", "panel": P(0.02, 0.72, 0.98, 0.98), "speaker": (0.55, 0.88), "slot": 0, "pos": (0.72, 0.16)},
        {"text": "HELIX ANOMALY  58%", "kind": "hud", "panel": P(0.20, 0.10, 0.80, 0.24), "slot": 0},
    ],
    20: [
        {"text": "Mano some assim de novo que eu mando busca e apreensão.", "kind": "phone", "panel": P(0.10, 0.04, 0.90, 0.22), "slot": 0, "label": "RYO", "pos": (0.50, 0.35)},
        {"text": "Tô vivo. Hospital. Drama de mãe.", "kind": "phone", "panel": P(0.10, 0.04, 0.90, 0.22), "slot": 1, "label": "KAEL", "pos": (0.50, 0.75)},
        {"text": "Maya perguntou de você. Tipo… perguntou.", "kind": "phone", "panel": P(0.10, 0.22, 0.90, 0.40), "slot": 0, "label": "RYO", "pos": (0.50, 0.45)},
        {"text": "Ele tá escondendo alguma coisa.\nE não é torradeira.", "kind": "speech", "panel": P(0.02, 0.72, 0.98, 0.98), "speaker": (0.55, 0.88), "slot": 0, "pos": (0.72, 0.16)},
    ],
    21: [
        {"text": "Se o leitor for Kael… desculpa.", "kind": "speech", "panel": P(0.02, 0.28, 0.98, 0.52), "speaker": (0.55, 0.42), "slot": 0, "pos": (0.72, 0.14)},
        {"text": "Não deixa eles medirem você como peça.", "kind": "speech", "panel": P(0.02, 0.52, 0.98, 0.74), "speaker": (0.55, 0.64), "slot": 0, "pos": (0.72, 0.14)},
        {"text": "…então eu meço primeiro.", "kind": "speech", "panel": P(0.02, 0.74, 0.98, 0.98), "speaker": (0.55, 0.88), "slot": 0, "pos": (0.72, 0.16)},
    ],
    22: [
        {"text": "PROTOCOL TREE: 16%", "kind": "hud", "panel": P(0.20, 0.30, 0.80, 0.48), "slot": 0},
        {"text": "Dez pedaços faltando.\nE alguém lá fora subindo o volume.", "kind": "speech", "panel": P(0.02, 0.50, 0.98, 0.74), "speaker": (0.50, 0.64), "slot": 0, "pos": (0.72, 0.14)},
        {"text": "A gente vai achar.\nSem incendiar a casa. De novo.", "kind": "speech", "panel": P(0.02, 0.74, 0.98, 0.98), "speaker": (0.50, 0.88), "slot": 0, "pos": (0.72, 0.16)},
    ],
    23: [
        {"text": "“Eles”.\nAinda não sei quem.", "kind": "speech", "panel": P(0.02, 0.28, 0.98, 0.52), "speaker": (0.50, 0.42), "slot": 0, "pos": (0.72, 0.14)},
        {"text": "Mas eu sei que tão contando.", "kind": "speech", "panel": P(0.02, 0.74, 0.98, 0.98), "speaker": (0.50, 0.88), "slot": 0, "pos": (0.72, 0.16)},
    ],
    24: [
        {"text": "Aguenta.\nPor favor, aguenta.", "kind": "speech", "panel": P(0.02, 0.28, 0.98, 0.52), "speaker": (0.50, 0.42), "slot": 0, "pos": (0.72, 0.14)},
        {"text": "WATCH ELEVATED — 58%", "kind": "hud", "panel": P(0.20, 0.54, 0.80, 0.68), "slot": 0},
        {"text": "Protocolo Hélice…\neu vou terminar o que você não pôde.", "kind": "speech", "panel": P(0.02, 0.70, 0.98, 0.92), "speaker": (0.50, 0.84), "slot": 0, "pos": (0.72, 0.16)},
        {"text": "CONTINUA — Nº 3: RUÍDO NA REDE", "kind": "caption", "panel": P(0.10, 0.90, 0.90, 0.98), "slot": 0},
    ],
}


@dataclass
class Placed:
    kind: str
    text: str
    panel: tuple[float, float, float, float]
    speaker: tuple[float, float] | None
    slot: int
    anchor: str
    label: str = ""
    pos: tuple[float, float] | None = None  # relative inside panel (0–1)
    # computed in px
    bx: int = 0
    by: int = 0
    bw: int = 0
    bh: int = 0
    tw: int = 0
    th: int = 0
    font_obj: ImageFont.ImageFont | None = None
    fill: tuple = (255, 255, 255)
    outline: tuple = (18, 18, 18)
    tfill: tuple = (12, 12, 12)
    radius: int = 22
    is_rect: bool = False


def get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    # Comic-readable sans; Liberation as secondary
    candidates = [
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def wrap_text(text: str, width: int) -> str:
    lines: list[str] = []
    for para in text.split("\n"):
        if not para.strip():
            lines.append("")
            continue
        lines.extend(textwrap.wrap(para, width=width) or [""])
    return "\n".join(lines)


def measure(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.ImageFont) -> tuple[int, int]:
    bbox = draw.multiline_textbbox((0, 0), text, font=fnt, spacing=4, align="center")
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def panel_px(panel: tuple[float, float, float, float], w: int, h: int) -> tuple[int, int, int, int]:
    x0, y0, x1, y1 = panel
    return int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h)


def rects_overlap(a: tuple[int, int, int, int], b: tuple[int, int, int, int], pad: int = 6) -> bool:
    ax0, ay0, ax1, ay1 = a
    bx0, by0, bx1, by1 = b
    return not (ax1 + pad <= bx0 or bx1 + pad <= ax0 or ay1 + pad <= by0 or by1 + pad <= ay0)


def place_in_panel(items: list[Placed], w: int, h: int, draw: ImageDraw.ImageDraw) -> None:
    """Lay out balloons inside each panel's top lettering zone; resolve collisions."""
    # Prepare sizes
    for it in items:
        kind = it.kind
        if kind == "sfx":
            it.font_obj = get_font(max(26, w // 32), bold=True)
            it.text = wrap_text(it.text, 14)
            it.tw, it.th = measure(draw, it.text, it.font_obj)
            it.bw, it.bh = it.tw + 8, it.th + 8
            it.is_rect = True
            it.fill = (0, 0, 0, 0)
            continue
        if kind == "hud":
            it.font_obj = get_font(max(14, w // 58), bold=True)
            it.text = wrap_text(it.text, 28)
            it.tw, it.th = measure(draw, it.text, it.font_obj)
            it.bw, it.bh = it.tw + 28, it.th + 24
            it.is_rect = True
            it.fill = (8, 28, 32)
            it.outline = (62, 199, 184)
            it.tfill = (170, 250, 235)
            continue
        if kind == "phone":
            it.font_obj = get_font(max(14, w // 58))
            body = wrap_text(it.text, 26)
            it.text = f"{it.label}\n{body}" if it.label else body
            it.tw, it.th = measure(draw, it.text, it.font_obj)
            it.bw, it.bh = it.tw + 28, it.th + 24
            it.is_rect = True
            it.radius = 14
            it.fill = (245, 248, 252)
            it.outline = (35, 35, 45)
            it.tfill = (15, 15, 25)
            continue
        if kind in ("narration", "caption"):
            it.font_obj = get_font(max(14, w // 58), bold=(kind == "caption"))
            it.text = wrap_text(it.text, 32)
            it.tw, it.th = measure(draw, it.text, it.font_obj)
            it.bw, it.bh = it.tw + 26, it.th + 20
            it.is_rect = True
            it.radius = 4
            if kind == "caption":
                it.fill = (18, 18, 18)
                it.tfill = (250, 250, 250)
            else:
                it.fill = (252, 252, 248)
                it.tfill = (20, 20, 20)
            continue
        # speech
        it.font_obj = get_font(max(15, w // 54))
        it.text = wrap_text(it.text, 20)
        it.tw, it.th = measure(draw, it.text, it.font_obj)
        it.bw, it.bh = it.tw + 36, it.th + 28
        it.radius = max(18, min(30, it.bh // 2))
        it.fill = (255, 255, 255)
        it.outline = (18, 18, 18)
        it.tfill = (10, 10, 10)

    # Group by panel
    by_panel: dict[tuple, list[Placed]] = {}
    for it in items:
        by_panel.setdefault(it.panel, []).append(it)

    for panel, group in by_panel.items():
        group.sort(key=lambda x: x.slot)
        px0, py0, px1, py1 = panel_px(panel, w, h)
        pw, ph = max(1, px1 - px0), max(1, py1 - py0)
        # lettering zone = top ~30% of panel (or bottom if anchor=bottom for captions)
        zone_top = py0 + int(0.04 * ph)
        zone_bot = py0 + int(0.38 * ph)
        margin = 10

        # Initial placement: stack by slot in reading order (L→R within rows)
        n = len(group)
        for i, it in enumerate(group):
            if it.pos is not None:
                # Explicit relative position inside panel (guarantees intent)
                cx = px0 + int(it.pos[0] * pw)
                cy = py0 + int(it.pos[1] * ph)
            elif it.anchor == "bottom":
                cx = (px0 + px1) // 2
                cy = py1 - it.bh // 2 - margin - 4
            elif it.kind == "sfx":
                cx = px0 + int(0.75 * pw)
                cy = py0 + int(0.20 * ph)
            else:
                # distribute horizontally in lettering zone
                if n == 1:
                    frac_x = 0.50
                else:
                    frac_x = 0.18 + (0.64 * i / max(1, n - 1))
                # Prefer side near speaker if present
                if it.speaker:
                    sx = it.speaker[0] * w
                    sy = it.speaker[1] * h
                    # close-up: speaker low in panel → keep bubble in top corners
                    if sy > py0 + 0.45 * ph:
                        frac_x = 0.22 if sx > (px0 + px1) / 2 else 0.78
                    elif sx < (px0 + px1) / 2:
                        frac_x = min(frac_x, 0.35)
                    else:
                        frac_x = max(frac_x, 0.65)
                cx = px0 + int(frac_x * pw)
                # vertical stack inside zone
                row = i if n <= 3 else i % 2
                cy = zone_top + it.bh // 2 + row * (it.bh + 8)
                if cy + it.bh // 2 > zone_bot and it.kind == "speech":
                    cy = zone_bot - it.bh // 2

            # Clamp inside panel
            cx = max(px0 + it.bw // 2 + margin, min(px1 - it.bw // 2 - margin, cx))
            cy = max(py0 + it.bh // 2 + margin, min(py1 - it.bh // 2 - margin, cy))
            it.bx, it.by = cx, cy

        # Collision resolve (push down / sideways within panel)
        for _ in range(12):
            moved = False
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    a, b = group[i], group[j]
                    ra = (a.bx - a.bw // 2, a.by - a.bh // 2, a.bx + a.bw // 2, a.by + a.bh // 2)
                    rb = (b.bx - b.bw // 2, b.by - b.bh // 2, b.bx + b.bw // 2, b.by + b.bh // 2)
                    if not rects_overlap(ra, rb, pad=8):
                        continue
                    # push lower-slot down, or sideways if near bottom of zone
                    if b.by >= a.by:
                        b.by = a.by + a.bh // 2 + b.bh // 2 + 10
                    else:
                        a.by = b.by + b.bh // 2 + a.bh // 2 + 10
                    # re-clamp
                    for it in (a, b):
                        it.bx = max(px0 + it.bw // 2 + margin, min(px1 - it.bw // 2 - margin, it.bx))
                        it.by = max(py0 + it.bh // 2 + margin, min(py1 - it.bh // 2 - margin, it.by))
                    moved = True
            if not moved:
                break

        # Head clearance: never sit as a "hat" on the speaker
        for it in group:
            if it.kind != "speech" or not it.speaker:
                continue
            sx, sy = int(it.speaker[0] * w), int(it.speaker[1] * h)
            # If balloon is roughly above the head and close, push UP and SIDEWAYS
            if abs(it.bx - sx) < max(it.bw * 0.55, 0.08 * w) and 0 <= (sy - it.by) < max(it.bh * 1.4, 0.14 * h):
                # push sideways away from face center
                if it.bx <= sx:
                    it.bx = max(px0 + it.bw // 2 + margin, sx - int(0.14 * w) - it.bw // 2)
                else:
                    it.bx = min(px1 - it.bw // 2 - margin, sx + int(0.14 * w) + it.bw // 2)
                # and higher toward panel top
                it.by = max(py0 + it.bh // 2 + margin, min(it.by, py0 + int(0.14 * ph)))
            # If bubble body vertically overlaps mouth band, force to top corner
            if abs(it.bx - sx) < it.bw * 0.45 and abs(it.by - sy) < it.bh * 0.7:
                prefer_left = sx > (px0 + px1) / 2
                it.bx = px0 + it.bw // 2 + margin if prefer_left else px1 - it.bw // 2 - margin
                it.by = py0 + it.bh // 2 + margin + 4
            it.bx = max(px0 + it.bw // 2 + margin, min(px1 - it.bw // 2 - margin, it.bx))
            it.by = max(py0 + it.bh // 2 + margin, min(py1 - it.bh // 2 - margin, it.by))


def draw_wedge_tail(
    draw: ImageDraw.ImageDraw,
    bx: int,
    by: int,
    bw: int,
    bh: int,
    speaker: tuple[float, float],
    w: int,
    h: int,
    panel: tuple[float, float, float, float],
) -> None:
    """Short comic wedge from the bubble edge nearest the mouth — clipped to panel."""
    sx, sy = int(speaker[0] * w), int(speaker[1] * h)
    px0, py0, px1, py1 = panel_px(panel, w, h)

    sx = max(px0 + 10, min(px1 - 10, sx))
    sy = max(py0 + 10, min(py1 - 10, sy))

    # Pick attach point on bubble perimeter closest to speaker
    left, right = bx - bw // 2, bx + bw // 2
    top, bottom = by - bh // 2, by + bh // 2
    candidates = [
        (bx, bottom - 1),  # bottom center
        (right - 2, by),  # right mid
        (left + 2, by),  # left mid
        (bx + bw // 4, bottom - 1),
        (bx - bw // 4, bottom - 1),
    ]
    attach_x, attach_y = min(candidates, key=lambda p: (p[0] - sx) ** 2 + (p[1] - sy) ** 2)

    dx, dy = sx - attach_x, sy - attach_y
    dist = math.hypot(dx, dy) or 1.0
    # Allow a bit more length when bubble is intentionally offset (side lettering)
    max_len = min(int(0.09 * h), int(0.55 * dist), 110)
    length = max(24, max_len)

    tip_x = attach_x + int(dx / dist * length)
    tip_y = attach_y + int(dy / dist * length)
    tip_x = max(px0 + 6, min(px1 - 6, tip_x))
    tip_y = max(py0 + 6, min(py1 - 6, tip_y))

    # Stop short of mouth so tip doesn't cover lips/eyes
    stop = max(18, int(0.025 * h))
    if math.hypot(tip_x - sx, tip_y - sy) < stop:
        tip_x = sx - int(dx / dist * stop)
        tip_y = sy - int(dy / dist * stop)
        tip_x = max(px0 + 6, min(px1 - 6, tip_x))
        tip_y = max(py0 + 6, min(py1 - 6, tip_y))

    base = 13
    nx, ny = -dy / dist, dx / dist
    p1 = (attach_x + int(nx * base), attach_y + int(ny * base))
    p2 = (attach_x - int(nx * base), attach_y - int(ny * base))

    draw.polygon([p1, p2, (tip_x, tip_y)], fill=(255, 255, 255), outline=(18, 18, 18))
    draw.polygon(
        [
            (attach_x + int(nx * (base - 3)), attach_y + int(ny * (base - 3))),
            (attach_x - int(nx * (base - 3)), attach_y - int(ny * (base - 3))),
            (tip_x - int(dx / dist * 2), tip_y - int(dy / dist * 2)),
        ],
        fill=(255, 255, 255),
    )


def draw_placed(im: Image.Image, items: list[Placed]) -> None:
    draw = ImageDraw.Draw(im)
    w, h = im.size

    # tails first (under bubble body), then bodies, then text
    for it in items:
        if it.kind == "speech" and it.speaker:
            draw_wedge_tail(draw, it.bx, it.by, it.bw, it.bh, it.speaker, w, h, it.panel)

    for it in items:
        x0, y0 = it.bx - it.bw // 2, it.by - it.bh // 2
        x1, y1 = it.bx + it.bw // 2, it.by + it.bh // 2
        if it.kind == "sfx":
            draw.multiline_text(
                (it.bx - it.tw // 2, it.by - it.th // 2),
                it.text,
                font=it.font_obj,
                fill=(25, 25, 25),
                align="center",
                spacing=4,
            )
            continue
        if it.is_rect and it.kind != "speech":
            if it.kind in ("narration", "caption", "phone", "hud"):
                draw.rounded_rectangle(
                    [x0, y0, x1, y1],
                    radius=it.radius,
                    fill=it.fill,
                    outline=it.outline,
                    width=2,
                )
            draw.multiline_text(
                (it.bx - it.tw // 2, it.by - it.th // 2),
                it.text,
                font=it.font_obj,
                fill=it.tfill,
                align="center" if it.kind != "phone" and it.kind != "hud" else "left",
                spacing=4,
            )
            continue
        # speech body
        draw.rounded_rectangle(
            [x0, y0, x1, y1],
            radius=it.radius,
            fill=(255, 255, 255),
            outline=(18, 18, 18),
            width=2,
        )
        # redraw short tail tip over bottom edge seam
        if it.speaker:
            draw_wedge_tail(draw, it.bx, it.by, it.bw, it.bh, it.speaker, w, h, it.panel)
            draw.rounded_rectangle(
                [x0, y0, x1, y1],
                radius=it.radius,
                fill=(255, 255, 255),
                outline=(18, 18, 18),
                width=2,
            )
        draw.multiline_text(
            (it.bx - it.tw // 2, it.by - it.th // 2),
            it.text,
            font=it.font_obj,
            fill=(10, 10, 10),
            align="center",
            spacing=4,
        )


def qc_page(items: list[Placed], w: int, h: int, page_num: int) -> list[str]:
    errors: list[str] = []
    for it in items:
        px0, py0, px1, py1 = panel_px(it.panel, w, h)
        x0, y0 = it.bx - it.bw // 2, it.by - it.bh // 2
        x1, y1 = it.bx + it.bw // 2, it.by + it.bh // 2
        # Must stay mostly inside panel (allow 4px bleed)
        if x0 < px0 - 4 or y0 < py0 - 4 or x1 > px1 + 4 or y1 > py1 + 4:
            errors.append(
                f"p{page_num}: bubble '{it.text[:24]}' escapes panel "
                f"box=({x0},{y0},{x1},{y1}) panel=({px0},{py0},{px1},{py1})"
            )
        if it.kind == "speech" and it.speaker:
            sx, sy = it.speaker[0] * w, it.speaker[1] * h
            # Speaker should be inside same panel (or near edge — allow 12% pad for side balloons)
            pad = 0.12 * max(px1 - px0, 1)
            if not (px0 - pad <= sx <= px1 + pad and py0 - pad <= sy <= py1 + pad):
                errors.append(
                    f"p{page_num}: speaker for '{it.text[:24]}' outside panel"
                )
            # Bubble center must not sit on the face (both axes close)
            if abs(it.bx - sx) < max(24, 0.035 * w) and abs(it.by - sy) < max(28, 0.045 * h):
                errors.append(
                    f"p{page_num}: bubble covers face '{it.text[:24]}'"
                )
    # pairwise overlap inside page
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            a, b = items[i], items[j]
            if a.kind == "sfx" or b.kind == "sfx":
                continue
            ra = (a.bx - a.bw // 2, a.by - a.bh // 2, a.bx + a.bw // 2, a.by + a.bh // 2)
            rb = (b.bx - b.bw // 2, b.by - b.bh // 2, b.bx + b.bw // 2, b.by + b.bh // 2)
            if rects_overlap(ra, rb, pad=2):
                errors.append(
                    f"p{page_num}: overlap '{a.text[:18]}' vs '{b.text[:18]}'"
                )
    return errors


def letter_page(page_num: int, src: Path, dst: Path, strict: bool = True) -> list[str]:
    work = Image.open(src).convert("RGB")
    w, h = work.size
    draw = ImageDraw.Draw(work)
    raw = LETTERING.get(page_num, [])
    items: list[Placed] = []
    for item in raw:
        items.append(
            Placed(
                kind=item["kind"],
                text=item["text"],
                panel=item["panel"],
                speaker=item.get("speaker"),
                slot=item.get("slot", 0),
                anchor=item.get("anchor", "top"),
                label=item.get("label", ""),
                pos=item.get("pos"),
            )
        )
    place_in_panel(items, w, h, draw)
    errors = qc_page(items, w, h, page_num)
    # Face-cover warnings: demote to soft if only that — still draw, report
    hard = [e for e in errors if any(k in e for k in ("overlap", "escapes", "outside panel", "covers face"))]
    soft = [e for e in errors if e not in hard]
    if hard and strict:
        for e in hard:
            print("QC FAIL:", e, file=sys.stderr)
        raise SystemExit(f"lettering QC failed on page {page_num} ({len(hard)} hard errors)")
    for e in soft:
        print("QC warn:", e, file=sys.stderr)
    draw_placed(work, items)
    dst.parent.mkdir(parents=True, exist_ok=True)
    work.save(dst, quality=94)
    print(f"lettered {dst.name} ({len(items)} items)")
    return errors


def main() -> None:
    if not CLEAN.exists():
        raise SystemExit(f"missing clean pages dir: {CLEAN}")
    OUT.mkdir(parents=True, exist_ok=True)
    PAGES.mkdir(parents=True, exist_ok=True)

    cover = CLEAN / "page_00_capa.jpg"
    if cover.exists():
        Image.open(cover).convert("RGB").save(OUT / "page_00_capa.jpg", quality=94)
        Image.open(cover).convert("RGB").save(PAGES / "page_00_capa.jpg", quality=94)

    all_soft: list[str] = []
    for i in range(1, NUM_PAGES + 1):
        src = CLEAN / f"page_{i:02d}.jpg"
        if not src.exists():
            # pages 23/24 may lack clean — skip regenerate if present in pages already lettered
            legacy = PAGES / f"page_{i:02d}.jpg"
            if legacy.exists() and i in (23, 24):
                print(f"skip {i}: no clean source (keeping existing lettered page)")
                Image.open(legacy).convert("RGB").save(OUT / f"page_{i:02d}.jpg", quality=94)
                continue
            raise SystemExit(f"missing clean page: {src}")
        errs = letter_page(i, src, OUT / f"page_{i:02d}.jpg", strict=True)
        all_soft.extend(errs)
        # sync to pages/
        Image.open(OUT / f"page_{i:02d}.jpg").convert("RGB").save(PAGES / f"page_{i:02d}.jpg", quality=94)

    print(f"done. soft warnings: {len(all_soft)}")


if __name__ == "__main__":
    main()
