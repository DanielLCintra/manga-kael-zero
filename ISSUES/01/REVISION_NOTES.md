# Revista #1 — Notas de revisão

## v1.4 — Lettering engine com QC
- Motor reescrito: lê só `pages_clean/`, ancora por **painel**, `pos` explícito, rabicho em cunha clipado ao quadro.
- QC hard-fail: balão fora do painel, overlap, centro no rosto.
- Rebuild: `python3 scripts/letter_issue01.py` → `python3 scripts/build_issue01_pdf.py`.

## v1.3 — Coesão manhua + anti-clone
- Páginas 1, 3–7, 19–20 regeneradas em estilo **manhua/manhwa** (cel-shade; fundos ilustrados, sem fotoreal).
- Página 2 montada em colagem 2×2 (Helena / Kael criança / casa / olho) para impedir clone do Kael no mesmo quadro.
- Regra de produção: **um Kael por painel**; lettering só via `scripts/letter_issue01.py`.
- Bíblia visual: prompt base atualizado (proíbe photoreal + texto embutido).
- PDF: `KAEL_ZERO_01_ECO_NO_PISO.pdf` (capa + 24 págs).

## v1.1 — Continuidade de causa/efeito
Cortes de HQ espalhavam causa/efeito: o leitor podia achar que “perdeu” um pedaço (por que foi sozinho para casa? por que tocou sem procurar o protocolo? por que o parafuso? por que a ORION agora?).

### Solução
Pontes explícitas: objeto (chave), som (trilha no piso), decisão (recusa skate park), leak (`SIGNAL LEAK` → corte ORION), Pulse Cuff.

## Arte / PDF
Roteiro canônico: `REVISTA_01_ECO_NO_PISO.md` v1.3.  
Rebuild: `python3 scripts/letter_issue01.py` → `python3 scripts/build_issue01_pdf.py`.

