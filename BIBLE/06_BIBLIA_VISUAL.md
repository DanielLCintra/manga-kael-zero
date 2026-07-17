# KAEL ZERO — Bíblia Visual (Consistência de HQ)

Usar estes locks em **todo** prompt de página.  
Inconsistência visual = erro de produção.

---

## Estilo geral

- HQ cinematográfica realista (não chibi, não super-deformed)
- Influências de tom: thriller sci-fi + drama adolescente contemporâneo
- Linha limpa, contrastes fortes, pouca “glow mágica”
- Tecnologia: industrial / lab realista, LEDs frios, metal, vidro, cabos
- **Não** cyberpunk neon-purple padrão
- **Não** auras de poder, runas, partículas mágicas

### Paleta (CSS mental)

```text
--bg-city: #1a1f26;
--bg-day: #c9d2dc;
--accent-core: #3ec7b8;      /* teal clínico — único “especial” */
--accent-orion: #8b1e2d;    /* sangue seco / alerta corporativo */
--skin-warm: naturalismo;   /* sem filtro fashion */
--lab-light: #9fd0ff;       /* fluorescente frio */
--home-warm: #e8d7c0;       /* luz doméstica Helena/Kael */
```

CORE = teal clínico.  
ORION = vermelho-escuro contido.  
Casa = quente.  
Lab = frio.

---

## Kael — design lock

- 16 anos, magro, ombros ainda de adolescente
- Cabelo escuro bagunçado (prático, não anime spikes extremos)
- Olhos expressivos; humor nos gestos
- Roupas: camiseta, hoodie, jeans, tênis de skate
- Skate frequente no Arco 1
- Mãos: cortes leves, óleo, bandaid — maker, não modelo
- Expressão default: curiosidade + ironia leve
- Em dor/CORE: suor, tremor, epistaxe — visceral, não “modo power”

**Proibido:** musculatura precoce, traje heróico cedo, olhar “escolhido” constante.

---

## Helena — design lock

- ~42, presença cansada e competente
- Cabelo preso prático em plantão; solto em casa
- Jaleco / scrubs no hospital; roupa simples em casa
- Olhos que leem pessoas (médica)
- Afeto em microgestos (mão no ombro, comida deixada)

---

## Adrian (flashback / fotos)

- Mais velho que Helena por pouco; olhar intenso de quem não dorme
- Lab coat ou camisa amarrotada
- Nunca glamouroso; genialidade bagunçada

---

## CORE ZERO — design lock

- Cilindro de vidro + metal, instrumentação realista
- Núcleo interno: geometria clara (esfera/anel) com luz **teal** estável, não explosiva
- Interface HUD: tipografia mono, logs, wireframes — UI de engenharia
- Materialização: “compilar” — poeira/partículas estruturando → sólido  
  Preferir look de **impressão molecular / vapor → sólido**, não magia

---

## Lab secreto

- Sob a casa; concreto, racks, mesa de trabalho, cabos, servidor antigo
- Entrada: painel técnico / manutenção — **sem** placa “PERIGO NÃO ENTRE”
- Atmosfera: pó, silêncio, um LED ainda vivo
- Mensagem de Adrian: display ou papel selado sóbrio

---

## ORION

- Visual corporativo limpo, quase chato — o horror é a banalidade
- Agentes: casacos escuros práticos, fones, vans sem logo
- Evitar skull logos; preferir geometria abstrata / constelação sutil

---

## Linguagem de câmera (para descrições de página)

| Enquadramento | Uso |
|---------------|-----|
| Extreme wide | Cidade / escala / solidão |
| Wide | Estabelecer local |
| Medium | Diálogo |
| Close-up | Emoção / detalhe de objeto |
| Extreme close-up | Olho, sangue, LED do CORE, parafuso materializando |
| Dutch / canted | Raro; só glitch neural / pânico |
| POV | Skate, HUD, descoberta |

Iluminação narrativa:
- Casa de dia = segura e mentirosa
- Lab = verdade fria
- Hospital = ética / corpo
- Noite na rua = vulnerabilidade

---

## Motion / comic timing

- Skate = liberdade e ritmo
- CORE boot = frames longos, silêncio, 1 SFX técnico
- Materialização = sequência de 3–5 beats (wireframe → fill → solid → custo no corpo)

---

## Prompt base (prefixo obrigatório)

```text
Kael Zero graphic novel page, cinematic realistic comic art, clean linework,
contemporary near-future city (not neon cyberpunk), consistent character designs:
Kael 16 skinny skater teen messy dark hair casual hoodie, teal clinical CORE tech,
warm home lighting vs cold lab fluorescents, no magic auras, no fantasy runes,
molecular assembly VFX only when materializing, Portuguese dialogue lettering space.
```

Manter esse prefixo (adaptando) em todas as páginas.
