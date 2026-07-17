#!/usr/bin/env python3
"""
Lettering profissional — Kael Zero #1 (24 págs).

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
CLEAN = ROOT / "ISSUES" / "01" / "pages_clean"
PAGES = ROOT / "ISSUES" / "01" / "pages"
OUT = ROOT / "ISSUES" / "01" / "pages_lettered"
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
        # 2x3: TL city | TR Helena | ML door | MR Kael sleep | BL hand | BR paper
        {"text": "PORT HAVEN", "kind": "caption", "panel": P(0.02, 0.02, 0.49, 0.34), "slot": 0},
        {
            "text": "Adrian?\nCheguei cedo hoje.",
            "kind": "speech",
            "panel": P(0.51, 0.02, 0.98, 0.34),
            "speaker": (0.74, 0.22),
            "slot": 0,
        },
        {
            "text": "Eu tentei de tudo...",
            "kind": "caption",
            "panel": P(0.02, 0.68, 0.49, 0.98),
            "slot": 0,
            "anchor": "bottom",
        },
    ],
    2: [
        # 2x2 collage
        {
            "text": "Vem.\nFica comigo.",
            "kind": "speech",
            "panel": P(0.02, 0.02, 0.49, 0.49),
            "speaker": (0.28, 0.32),
            "slot": 0,
        },
        {
            "text": "Mãe…?\nO pai tá dormindo?",
            "kind": "speech",
            "panel": P(0.51, 0.02, 0.98, 0.49),
            "speaker": (0.72, 0.28),
            "slot": 0,
        },
        {
            "text": "Oficialmente, a causa nunca ficou clara.\nNa vizinhança, alguém murmurou suicídio.\nHelena não discutiu. Só trabalhou.",
            "kind": "narration",
            "panel": P(0.02, 0.51, 0.49, 0.98),
            "slot": 0,
            "anchor": "top",
        },
        {
            "text": "SEIS ANOS DEPOIS",
            "kind": "caption",
            "panel": P(0.51, 0.51, 0.98, 0.98),
            "slot": 0,
            "anchor": "bottom",
        },
    ],
    3: [
        # top | mid L/R | bottom
        {
            "text": "Kael Zero tem dezesseis anos.\nAnda de skate. Conserta o que quebra.\nNão é popular. Não treina luta. Não é herói.",
            "kind": "narration",
            "panel": P(0.02, 0.02, 0.98, 0.36),
            "slot": 0,
            "anchor": "top",
        },
        {"text": "KRRRASH", "kind": "sfx", "panel": P(0.02, 0.38, 0.49, 0.62), "slot": 0},
        {
            "text": "Ai…\nTá. Quase.",
            "kind": "speech",
            "panel": P(0.51, 0.38, 0.98, 0.62),
            "speaker": (0.72, 0.54),
            "slot": 0,
        },
        {
            "text": "Beleza. Mais um dia sem incendiar nada.",
            "kind": "speech",
            "panel": P(0.02, 0.64, 0.98, 0.98),
            "speaker": (0.55, 0.82),
            "slot": 0,
        },
    ],
    4: [
        # Ryo esquerda / Kael direita — falantes corretos
        {
            "text": "Kael! Se você se matar antes da prova de física, eu não vou na sua missa.",
            "kind": "speech",
            "panel": P(0.02, 0.02, 0.48, 0.34),
            "speaker": (0.28, 0.24),
            "slot": 0,
            "pos": (0.45, 0.22),
        },
        {
            "text": "Relaxa. Você ia só pelo lanche depois.",
            "kind": "speech",
            "panel": P(0.52, 0.02, 0.98, 0.34),
            "speaker": (0.72, 0.24),
            "slot": 0,
            "pos": (0.55, 0.22),
        },
        {
            "text": "…justo.",
            "kind": "speech",
            "panel": P(0.02, 0.02, 0.48, 0.34),
            "speaker": (0.28, 0.28),
            "slot": 1,
            "pos": (0.45, 0.62),
        },
        {
            "text": "Poucos amigos. Pouca grana. Muita casa vazia.",
            "kind": "narration",
            "panel": P(0.02, 0.36, 0.98, 0.66),
            "slot": 0,
            "pos": (0.50, 0.82),
        },
    ],
    5: [
        # Painéis reais da arte; pos = âncora do balão dentro do painel
        {
            "text": "Plantão esticou de novo. Tem macarrão na geladeira. Não desmonta a torradeira. Te amo.",
            "kind": "phone",
            "panel": P(0.02, 0.02, 0.98, 0.58),
            "slot": 0,
            "label": "HELENA",
            "pos": (0.55, 0.10),
        },
        {
            "text": "Ela me conhece demais. Assustador.",
            "kind": "speech",
            "panel": P(0.02, 0.02, 0.98, 0.58),
            "speaker": (0.22, 0.30),
            "slot": 1,
            "pos": (0.18, 0.12),
        },
        {
            "text": "Skate park depois da última?",
            "kind": "speech",
            "panel": P(0.02, 0.02, 0.98, 0.58),
            "speaker": (0.58, 0.28),
            "slot": 2,
            "pos": (0.82, 0.12),
        },
        {
            "text": "Hoje não dá. Casa vazia… se eu for, acabo abrindo alguma coisa que não devia.",
            "kind": "speech",
            "panel": P(0.02, 0.02, 0.98, 0.58),
            "speaker": (0.22, 0.34),
            "slot": 3,
            "pos": (0.42, 0.72),
        },
        {
            "text": "Tipo a torradeira.",
            "kind": "speech",
            "panel": P(0.02, 0.60, 0.49, 0.98),
            "speaker": (0.34, 0.72),
            "slot": 0,
            "pos": (0.85, 0.12),
        },
        {
            "text": "Tipo a torradeira.",
            "kind": "speech",
            "panel": P(0.51, 0.60, 0.98, 0.98),
            "speaker": (0.72, 0.78),
            "slot": 0,
            "pos": (0.18, 0.12),
        },
        {
            "text": "Helena é médica. Trabalha demais.\nDesde que Adrian morreu, a casa aprendeu a ficar em silêncio.",
            "kind": "narration",
            "panel": P(0.02, 0.60, 0.49, 0.98),
            "slot": 1,
            "pos": (0.50, 0.88),
        },
    ],
    6: [
        {
            "text": "Energia não some. Ela só muda de forma. Anotem isso antes que eu cobrem na prova.",
            "kind": "speech",
            "panel": P(0.02, 0.02, 0.98, 0.36),
            "speaker": (0.45, 0.22),
            "slot": 0,
        },
        {
            "text": "DEPOIS DA AULA",
            "kind": "caption",
            "panel": P(0.51, 0.70, 0.98, 0.98),
            "slot": 0,
            "anchor": "bottom",
        },
    ],
    7: [
        {
            "text": "…mais um dia de casa sozinho. Que novidade.",
            "kind": "speech",
            "panel": P(0.02, 0.02, 0.98, 0.34),
            "speaker": (0.55, 0.22),
            "slot": 0,
            "pos": (0.55, 0.20),
        },
        {
            "text": "Come. Dorme. Existe.\n— Mãe",
            "kind": "caption",
            "panel": P(0.02, 0.70, 0.40, 0.92),
            "slot": 0,
            "pos": (0.50, 0.45),
        },
        {
            "text": "Sim, senhora.",
            "kind": "speech",
            "panel": P(0.42, 0.36, 0.98, 0.98),
            "speaker": (0.70, 0.55),
            "slot": 0,
            "pos": (0.70, 0.18),
        },
    ],
    8: [
        # sala: game → foto → mesa/SFX → ajoelha
        {
            "text": "…melhor fase do jogo. Finalmente.",
            "kind": "speech",
            "panel": P(0.02, 0.02, 0.98, 0.42),
            "speaker": (0.55, 0.28),
            "slot": 0,
            "pos": (0.72, 0.16),
        },
        {"text": "VMM—tik—VMM", "kind": "sfx", "panel": P(0.51, 0.44, 0.98, 0.68), "slot": 0, "pos": (0.50, 0.55)},
        {
            "text": "Não foi a geladeira.",
            "kind": "speech",
            "panel": P(0.02, 0.70, 0.98, 0.98),
            "speaker": (0.55, 0.82),
            "slot": 0,
            "pos": (0.28, 0.22),
        },
        {
            "text": "…oi?",
            "kind": "speech",
            "panel": P(0.02, 0.70, 0.98, 0.98),
            "speaker": (0.55, 0.86),
            "slot": 1,
            "pos": (0.78, 0.35),
        },
    ],
    9: [
        {
            "text": "Se for rato, a gente negocia.",
            "kind": "speech",
            "panel": P(0.02, 0.02, 0.98, 0.34),
            "speaker": (0.55, 0.22),
            "slot": 0,
            "pos": (0.70, 0.18),
        },
        {
            "text": "Manutenção… que nunca ninguém manteve.",
            "kind": "speech",
            "panel": P(0.02, 0.68, 0.98, 0.98),
            "speaker": (0.55, 0.82),
            "slot": 0,
            "pos": (0.70, 0.20),
        },
    ],
    10: [
        {
            "text": "Tá.\nIsso aqui não é caixa de luz.",
            "kind": "speech",
            "panel": P(0.51, 0.36, 0.98, 0.62),
            "speaker": (0.72, 0.52),
            "slot": 0,
            "pos": (0.55, 0.28),
        },
    ],
    11: [
        {
            "text": "…pai?",
            "kind": "speech",
            "panel": P(0.02, 0.36, 0.49, 0.62),
            "speaker": (0.28, 0.52),
            "slot": 0,
        },
        {
            "text": "Seis anos. Embaixo da casa dele.\nO silêncio tinha endereço.",
            "kind": "narration",
            "panel": P(0.02, 0.64, 0.98, 0.98),
            "slot": 0,
            "anchor": "bottom",
        },
    ],
    12: [
        {
            "text": "Se você está lendo isto, o isolamento falhou.\nNão toque no cilindro sem ler o Protocolo Hélice.\n\nSe o leitor for Kael…\ndesculpa.\n\nEu tentei de tudo.",
            "kind": "caption",
            "panel": P(0.08, 0.18, 0.92, 0.72),
            "slot": 0,
        },
        {
            "text": "…o quê que você tentou?",
            "kind": "speech",
            "panel": P(0.02, 0.74, 0.98, 0.98),
            "speaker": (0.50, 0.90),
            "slot": 0,
        },
    ],
    13: [
        {
            "text": "Um de doze.\nSério, pai?",
            "kind": "speech",
            "panel": P(0.02, 0.02, 0.98, 0.40),
            "speaker": (0.55, 0.26),
            "slot": 0,
        },
        {
            "text": "Eu só… quero ver.\nNão vou mexer. Só ver.",
            "kind": "speech",
            "panel": P(0.02, 0.42, 0.98, 0.98),
            "speaker": (0.55, 0.72),
            "slot": 0,
        },
    ],
    14: [
        {
            "text": "Ei— espera— eu não pedi—",
            "kind": "speech",
            "panel": P_FULL,
            "speaker": (0.55, 0.55),
            "slot": 0,
        },
    ],
    15: [
        {
            "text": "Para! Desliga!",
            "kind": "speech",
            "panel": P_FULL,
            "speaker": (0.55, 0.60),
            "slot": 0,
        },
    ],
    16: [
        {
            "text": "Legal.\nAchei o porão secreto do meu pai e quase desmaiei. Dia normal.",
            "kind": "speech",
            "panel": P(0.02, 0.02, 0.98, 0.48),
            "speaker": (0.50, 0.28),
            "slot": 0,
        },
        {
            "text": "A gente… termina essa conversa depois.",
            "kind": "speech",
            "panel": P(0.02, 0.50, 0.98, 0.98),
            "speaker": (0.50, 0.70),
            "slot": 0,
        },
    ],
    17: [
        {
            "text": "Tudo bem aí?",
            "kind": "phone",
            "panel": P(0.15, 0.18, 0.85, 0.40),
            "slot": 0,
            "label": "HELENA",
        },
        {
            "text": "Tô bem. Macarrão tava bom.",
            "kind": "phone",
            "panel": P(0.15, 0.42, 0.85, 0.62),
            "slot": 0,
            "label": "KAEL",
        },
        {
            "text": "…desculpa, mãe.",
            "kind": "speech",
            "panel": P(0.02, 0.64, 0.98, 0.98),
            "speaker": (0.55, 0.85),
            "slot": 0,
        },
    ],
    18: [
        {"text": "MESMA NOITE", "kind": "caption", "panel": P(0.02, 0.02, 0.45, 0.14), "slot": 0},
        {
            "text": "Ainda tá aí?",
            "kind": "speech",
            "panel": P(0.02, 0.16, 0.98, 0.48),
            "speaker": (0.55, 0.36),
            "slot": 0,
        },
        {
            "text": "…aguardando input.",
            "kind": "hud",
            "panel": P(0.20, 0.50, 0.80, 0.68),
            "slot": 0,
        },
        {
            "text": "…você ficou.\nClaro que você ficou.",
            "kind": "speech",
            "panel": P(0.02, 0.70, 0.98, 0.98),
            "speaker": (0.55, 0.88),
            "slot": 0,
        },
    ],
    19: [
        # 3 bandas iguais ~0.33
        {"text": "MANHÃ", "kind": "caption", "panel": P(0.02, 0.02, 0.20, 0.08), "slot": 0, "pos": (0.50, 0.50)},
        {
            "text": "Você tá gelado. Dormiu direito?",
            "kind": "speech",
            "panel": P(0.02, 0.02, 0.48, 0.33),
            "speaker": (0.22, 0.22),
            "slot": 0,
            "pos": (0.55, 0.22),
        },
        {
            "text": "Mais ou menos. Prova hoje. Cabeça zoada.",
            "kind": "speech",
            "panel": P(0.52, 0.02, 0.98, 0.33),
            "speaker": (0.78, 0.22),
            "slot": 0,
            "pos": (0.45, 0.22),
        },
        {
            "text": "Sangrou o nariz?",
            "kind": "speech",
            "panel": P(0.02, 0.34, 0.48, 0.50),
            "speaker": (0.22, 0.48),
            "slot": 0,
            "pos": (0.55, 0.35),
        },
        {
            "text": "Não. Só… dormi mal.",
            "kind": "speech",
            "panel": P(0.52, 0.34, 0.98, 0.50),
            "speaker": (0.72, 0.48),
            "slot": 0,
            "pos": (0.45, 0.35),
        },
        {
            "text": "Se passar mal, me liga. E Kael… eu sei quando você tá escondendo coisa. Sempre soube.",
            "kind": "speech",
            "panel": P(0.08, 0.50, 0.92, 0.66),
            "speaker": (0.28, 0.58),
            "slot": 0,
            "pos": (0.50, 0.40),
        },
        {
            "text": "Eu sei.",
            "kind": "speech",
            "panel": P(0.02, 0.68, 0.98, 0.98),
            "speaker": (0.72, 0.78),
            "slot": 0,
            "pos": (0.38, 0.16),
        },
    ],
    20: [
        {
            "text": "…mano. Alô?",
            "kind": "speech",
            "panel": P(0.02, 0.02, 0.54, 0.34),
            "speaker": (0.20, 0.22),
            "slot": 0,
            "pos": (0.28, 0.16),
        },
        {
            "text": "Você tá estranho hoje.",
            "kind": "speech",
            "panel": P(0.02, 0.02, 0.54, 0.34),
            "speaker": (0.20, 0.24),
            "slot": 1,
            "pos": (0.28, 0.48),
        },
        {
            "text": "Desculpa. Tô aqui. Continua.",
            "kind": "speech",
            "panel": P(0.56, 0.02, 0.98, 0.34),
            "speaker": (0.78, 0.20),
            "slot": 0,
            "pos": (0.30, 0.16),
        },
        {
            "text": "Dormi três horas. Me julga depois.",
            "kind": "speech",
            "panel": P(0.56, 0.02, 0.98, 0.34),
            "speaker": (0.78, 0.22),
            "slot": 1,
            "pos": (0.72, 0.16),
        },
        {
            "text": "Não sei. Só… diferente.",
            "kind": "speech",
            "panel": P(0.02, 0.36, 0.34, 0.64),
            "speaker": (0.18, 0.50),
            "slot": 0,
            "pos": (0.50, 0.16),
        },
        {
            "text": "Você tá diferente hoje.",
            "kind": "caption",
            "panel": P(0.66, 0.36, 0.98, 0.64),
            "slot": 0,
            "pos": (0.50, 0.25),
        },
        {
            "text": "Diferente como?",
            "kind": "speech",
            "panel": P(0.36, 0.36, 0.64, 0.64),
            "speaker": (0.50, 0.55),
            "slot": 0,
            "pos": (0.50, 0.14),
        },
        {
            "text": "Ah, não…",
            "kind": "speech",
            "panel": P(0.02, 0.66, 0.98, 0.98),
            "speaker": (0.55, 0.82),
            "slot": 0,
            "pos": (0.22, 0.18),
        },
    ],
    21: [
        {
            "text": "Sumiu. Claro que sumiu.",
            "kind": "speech",
            "panel": P_FULL,
            "speaker": (0.55, 0.45),
            "slot": 0,
        },
        {
            "text": "OBJECT MODEL: FASTENER\nPHASE: HELIX\nLOW COST / COMPILE?",
            "kind": "hud",
            "panel": P(0.08, 0.28, 0.55, 0.48),
            "slot": 0,
        },
        {
            "text": "…você consegue fazer um parafuso?\nSó um. Sem drama.",
            "kind": "speech",
            "panel": P_FULL,
            "speaker": (0.55, 0.55),
            "slot": 1,
        },
        {
            "text": "…ok.",
            "kind": "speech",
            "panel": P_FULL,
            "speaker": (0.55, 0.62),
            "slot": 2,
        },
    ],
    22: [
        {
            "text": "Ele… pesa.\nMas parece que eu tô segurando uma mentira.\nPai… o que era isso?",
            "kind": "speech",
            "panel": P_FULL,
            "speaker": (0.50, 0.50),
            "slot": 0,
        },
    ],
    23: [
        {
            "text": "Quarenta e um por cento é ruído.",
            "kind": "speech",
            "panel": P(0.02, 0.40, 0.49, 0.98),
            "speaker": (0.25, 0.70),
            "slot": 0,
        },
        {
            "text": "Ruído é como a gente chama o que ainda não quer ver.\nMantém o watch.",
            "kind": "speech",
            "panel": P(0.51, 0.40, 0.98, 0.98),
            "speaker": (0.75, 0.70),
            "slot": 0,
        },
    ],
    24: [
        {
            "text": "“Eles”?\nQuem é “eles”?",
            "kind": "speech",
            "panel": P(0.02, 0.02, 0.98, 0.45),
            "speaker": (0.55, 0.30),
            "slot": 0,
        },
        {
            "text": "Pai…\no que você deixou em mim?",
            "kind": "speech",
            "panel": P(0.02, 0.47, 0.98, 0.82),
            "speaker": (0.50, 0.68),
            "slot": 0,
        },
        {
            "text": "CONTINUA — Nº 2: PROTOCOLO HÉLICE",
            "kind": "caption",
            "panel": P(0.10, 0.86, 0.90, 0.98),
            "slot": 0,
            "anchor": "bottom",
        },
    ],
}


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------

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
