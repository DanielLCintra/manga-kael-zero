# KAEL ZERO — Bíblia Visual (Consistência de HQ)

Usar estes locks em **todo** prompt de página.  
Inconsistência visual = erro de produção.

---

## Estilo geral — LOCK MANHUA

- **Estilo único:** manhua / manhwa moderno (linha limpa, cel-shade, personagens estilizados)
- **Refs obrigatórias:** `REFS/kael/kael_sem_core_*` e `kael_com_core_*`
- **Âncora de produção:** revistas devem parecer a **mesma série** — usar Issue #1 + refs oficiais como referência visual em todo prompt
- **Proibido:** fotorealismo, cinematic live-action, photobash, pintura hiper-realista
- **Proibido:** o mesmo personagem **duplicado no mesmo quadro** (dois Kaels, clone, copy-paste)
- Um Kael por painel (exceto flashback criança vs presente em painéis **separados**)
- Influências de tom: thriller sci-fi + drama adolescente
- Linha limpa, contrastes claros
- Tecnologia: lab limpo, LEDs frios — ainda manhua, não CGI realista
- **Não** cyberpunk neon-purple padrão / overload de HUD / molduras sci-fi na capa
- **Não** auras de poder mágicas, runas, partículas fantasy
- **Sim** aura digital **clínica** só em Matéria de Fase Hélice
- **Kael no Arco 1:** techwear preto + forro/logo azul — **nunca** jaleco branco / gi / uniforme aleatório (exceto cena escolar com uniforme quando o roteiro pedir)
- **Capas:** composição full-bleed estilo Issue #1 (personagem + gancho visual + tipografia `KAEL ZERO` / `#N` / subtítulo) — sem collage de vinhetas
- **Lettering:** rabicho aponta para quem fala; nunca cobrir rostos — `12_LETTERING.md`

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

**Refs oficiais:** ver `06B_REFS_KAEL.md` e pasta `REFS/kael/`.

- 16 anos, magro/atlético leve, ombros de adolescente
- Cabelo volumoso bagunçado: azul safira/cobalto + sombras pretas
- Olhos azul-gelo; pele morena clara
- Brinco na orelha esquerda
- Techwear preto: jaqueta oversized com forro/zíper azul elétrico, logo azul no bíceps, camiseta preta, cargo/botas com detalhe azul
- Skate frequente no Arco 1
- Mãos: cortes leves, óleo, bandaid — maker, não modelo
- Expressão default: curiosidade + ironia leve (ainda não “mission ready”)
- Em dor/CORE: suor, tremor, epistaxe — visceral, não “modo power”
- **Revista #1:** apenas visual SEM CORE. HUD residual no máximo.
- **Com CORE (futuro):** headset + visor + materializações avançadas — refs `kael_com_core_*`

**Proibido no Arco 1:** espada/escudo energéticos, loadout de combate, olhar de escolhido constante.

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
- Materialização: wireframe → lattice → **sólido de Fase Hélice** (desde o 1º objeto)
- **Nunca** render mundano completo: constructs sempre com **aura digital** — translúcidos teal/ciano, circuit-glass, lattice; pesam, ocupam espaço, cortam/bloqueiam de verdade
- **Não** é Lanterna Verde: sem anel, sem vontade verde, sem glow mágico genérico — é compilação informacional
- Hold dissolvendo: construct desfaz em vapor de dados / fragmentação de lattice
- Refs futuras de combate: `REFS/kael/kael_com_core_*` (espada/escudo = Hard Compile visual alvo)

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
Kael Zero manhua/manhwa comic PAGE, cel-shade, clean ink, flat digital color,
stylized illustrated backgrounds (NOT photoreal, NOT live-action, NOT photo),
match REFS/kael character lock: Kael 16 messy cobalt-blue hair, black techwear
hoodie with electric-blue lining + wolf sleeve logo, teal clinical CORE only when
materializing, warm home vs cold lab, no magic auras/runes, NO text/speech bubbles
baked in, headroom for lettering, ONE Kael per panel — NEVER duplicate/clone Kael.
```

### QC obrigatório antes de aceitar arte
1. Estilo manhua em personagens **e** fundos (sem photobash)
2. Contagem: no máximo **um** Kael por quadro
3. Sem balões/texto gerados pela IA (lettering só via script)
4. Refs `REFS/kael/*` respeitadas (cabelo, jaqueta, logo)

Manter esse prefixo (adaptando) em todas as páginas.
