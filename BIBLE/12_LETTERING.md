# Lettering & Encenação — Padrão profissional

Baseado em práticas clássicas (Marvel/Shooter, lettering ocidental L→R / T→B).

## Regras absolutas

1. **Balão nunca tapa rosto** (olhos, nariz, boca). Se precisar, a arte ou o balão mudam — o rosto ganha.
2. **Planejar balão no thumbnail**, não depois. O painel tem “zona de lettering”.
3. **Rabicho** aponta para a **boca** do falante; curto; sai da borda do balão mais próxima da boca; **nunca atravessa gutter**.
4. **Ordem de leitura:** primeiro balão = mais alto / mais à esquerda; resposta = mais baixo / à direita.
5. **Ancorar balões** no topo do quadro ou na borda quando possível (não “chapéu” na cabeça).
6. **Máx. 2–3 falas por quadro** em diálogo; se passar, **dividir quadro**.
7. **Headroom:** em cenas de diálogo, deixar ~25–35% superior do painel limpo para lettering.
8. **Planos:**
   - Estabelecimento (wide) = pouco diálogo
   - Diálogo = medium com espaço acima das cabeças
   - Emoção = close **sem** balão em cima do rosto (balão ao lado / no gutter)

## Zona segura (produção)

```
+------------------+
|  LETTERING ZONE  |  ← balões / legendas
|------------------|
|                  |
|   PERSONAGENS    |  ← rostos livres
|                  |
+------------------+
```

## O que proibir

- Balão “chapéu” pousado na cabeça  
- Rabicho cruzando outro personagem ou gutter  
- Texto cobrindo olhos  
- 4 réplicas no mesmo painel  
- Balão gigante no centro do close  
- Lettering em cima de página já lettered (double balloons)

## Pipeline obrigatório (garantia)

1. Arte limpa em `ISSUES/01/pages_clean/` (sem balões embutidos).
2. `python3 scripts/letter_issue01.py` lê **só** `pages_clean/`.
3. Cada fala declara:
   - `panel=(x0,y0,x1,y1)` — bounds do quadro
   - `speaker=(x,y)` — boca (speech)
   - `pos=(x,y)` opcional — âncora relativa **dentro** do painel
4. Motor:
   - coloca balão na zona do painel
   - resolve colisão entre balões
   - rabicho = cunha curta clipada ao painel
   - **QC hard-fail** se: balão sai do painel, sobrepõe outro balão, ou centro do balão cai no rosto
5. Saída: `pages_lettered/` + sync em `pages/`.
6. `python3 scripts/build_issue01_pdf.py`

Sem limpar `pages_clean/`, o lettering **não** é confiável.
