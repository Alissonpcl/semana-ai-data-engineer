# Knowledge Bases Locais e Confidence Scoring — Estudo da Sessão

> Documento de estudo derivado da exploração do projeto ShopAgent (Semana AI Data Engineer 2026).
> Foco: como o sistema de KBs locais funciona e o que é o protocolo de `confidence` usado pelos subagents.

---

## 1. Como as KBs locais são utilizadas

### 1.1 O que são

O projeto possui 18 domínios de Knowledge Base em [`.claude/kb/`](../.claude/kb/), cada um seguindo a estrutura:

```
kb/<domain>/
  index.md             # Entry point humano
  quick-reference.md   # Lookup rápido (< 100 linhas)
  concepts/*.md        # Conceitos atômicos (< 150 linhas cada)
  patterns/*.md        # Padrões aplicados (< 200 linhas cada)
  specs/*.yaml         # Specs machine-readable
```

E um índice global em [`.claude/kb/_index.yaml`](../.claude/kb/_index.yaml) que registra todos os domínios, seus concepts/patterns/specs e qual subagent é "dono" de cada um.

### 1.2 NÃO existe carregamento automático

A descoberta-chave: **o `CLAUDE.md` apenas documenta a existência das KBs**, não instrui Claude principal a carregá-las automaticamente. Se o usuário menciona "Chainlit" diretamente, Claude principal **não lê** `.claude/kb/chainlit/` por conta própria.

**Não há:**

- Hook em `settings.json` fazendo pattern-matching de tópico → KB
- Instrução em `CLAUDE.md` tipo "ao detectar domínio X, leia `kb/X/index.md`"
- Script/binário que parsea `_index.yaml`

### 1.3 O carregamento é delegado a SubAgents

O verdadeiro mecanismo de loading é **declarativo dentro do system prompt de cada subagent**. Exemplo concreto: [`shopagent-builder.md`](../.claude/agents/domain/shopagent-builder.md) tem uma seção literal:

```markdown
## MANDATORY: Read Before Building

Before generating ANY ShopAgent component, read these KB files based on the day:

### Day 3: Agent + Chainlit
8. `.claude/kb/chainlit/patterns/langchain-integration.md` — KEY: Streaming chat...
```

### 1.4 Fluxo real de uso

```
User: "monta o Chainlit do ShopAgent"
   ↓
Claude principal reconhece domínio → invoca shopagent-builder via Task tool
   ↓
shopagent-builder (subagent) carrega seu próprio system prompt
   ↓
System prompt diz "MANDATORY: leia kb/chainlit/patterns/..."
   ↓
SubAgent usa Read tool nos arquivos do KB
   ↓
Constrói com aquele contexto carregado
```

### 1.5 Mapeamento bidirecional KB ↔ Agent

Três pontos redundantes registram a relação domínio ↔ agent:

| Local | Conteúdo |
|---|---|
| [`_index.yaml`](../.claude/kb/_index.yaml) | Campo `agents:` em cada domínio (ex.: `chainlit.agents: [shopagent-builder]`) |
| `kb/<domain>/index.md` | Seção "Agent Usage" |
| `agents/<agent>.md` | Seção "MANDATORY: Read Before..." com paths explícitos |

**Esses três são convenção/documentação, não execução.** Quem realmente "puxa o gatilho" é o system prompt do subagent quando ele é invocado.

### 1.6 Implicações práticas

1. Para que o KB seja consultado, **invoque o subagent certo** (ou peça explicitamente "leia kb/chainlit antes de responder").
2. Para **automatizar** o carregamento, seria necessário um hook em `settings.json` ou uma instrução no `CLAUDE.md`.
3. O `_index.yaml` é "machine-readable" mas **ninguém o lê automaticamente** — serve para o `kb-architect` agent gerenciar saúde do KB e para humanos navegarem.

---

## 2. O conceito de `confidence`

`confidence` aparece em **dois lugares distintos** com semânticas diferentes. Spoiler: **nada disso é executado por código** — é um protocolo declarativo que os subagents seguem (ou não) por instrução em prompt.

### 2.1 `confidence` estático no `_index.yaml` (KB-level)

Cada `concept` no `_index.yaml` carrega um campo `confidence`:

```yaml
concepts:
  - name: base-model
    path: concepts/base-model.md
    confidence: 0.95
```

É um **selo de qualidade** atribuído pelo `kb-architect` quando o concept é criado/validado. Significa: "esse arquivo foi validado contra MCP/Context7 na data `mcp_validated`, está atualizado, tem exemplos reais".

**Observação:** todos os concepts hoje estão em 0.95 — é praticamente um booleano disfarçado de float ("validado / não validado"). Não há nada abaixo de 0.90.

### 2.2 `confidence` dinâmico nos SubAgents (runtime)

Esse é o lado interessante. Cada agent (ex: [`shopagent-builder`](../.claude/agents/domain/shopagent-builder.md), [`_template.md.example`](../.claude/agents/_template.md.example)) define um protocolo: para **cada tarefa**, o subagent deve calcular um score e comparar com um threshold.

#### Fluxo

```
1. CLASSIFY → tarefa é CRITICAL / IMPORTANT / STANDARD / ADVISORY?
2. LOAD     → ler KB do domínio
3. VALIDATE → consultar MCP (Context7, etc.)
4. CALCULATE → base score + modifiers = score final
5. DECIDE   → score ≥ threshold? Execute / Ask / Refuse
```

#### Base score (Agreement Matrix)

Cruza presença do KB com resposta do MCP:

|  | MCP concorda | MCP discorda | MCP silente |
|---|---|---|---|
| **KB tem pattern** | 0.95 → Executa | 0.50 → Investiga | 0.75 → Procede |
| **KB silente** | 0.85 → Procede | — | 0.50 → Pergunta |

#### Modifiers

Ajustes finos sobre o base score:

| Condição | Δ |
|---|---|
| Info fresca (< 1 mês) | +0.05 |
| Info stale (> 6 meses) | -0.05 |
| Breaking change conhecido | -0.15 |
| Exemplos de produção | +0.05 |
| Sem exemplos | -0.05 |
| Match exato do caso | +0.05 |
| Match tangencial | -0.05 |

#### Thresholds por categoria de tarefa

| Categoria | Threshold | Se abaixo |
|---|---|---|
| CRITICAL | 0.98 | RECUSA (security, secrets, MCP configs) |
| IMPORTANT | 0.95 | PERGUNTA primeiro (arquitetura, routing) |
| STANDARD | 0.90 | PROCEDE com disclaimer |
| ADVISORY | 0.80 | PROCEDE livremente (docs, comentários) |

### 2.3 Como os dois confidences se conectam

O `0.95` do `_index.yaml` é, na prática, **o "KB HAS PATTERN + MCP AGREES" pré-calculado**. Quando o subagent cita `kb/pydantic/concepts/base-model.md`, ele já parte de ~0.95 (porque o KB foi MCP-validado em `mcp_validated: 2026-02-17`). Daí aplica modifiers conforme a tarefa específica.

### 2.4 Caveat importante: não é mecânico

Esses scores são **calculados pelo próprio LLM** seguindo instruções no system prompt do subagent. Não há código Python somando 0.95 + 0.05 - 0.15. É um **frame de raciocínio** que força o subagent a:

1. Verbalizar a validação (KB sim/não, MCP sim/não)
2. Ser explícito sobre o nível de confiança
3. Recusar/perguntar em vez de alucinar quando o score cai

Em outras palavras: é uma técnica de **prompt engineering tipo "self-critique numérico"** que reduz alucinação e força citação de fontes. O número em si é menos importante do que o **ritual de cálculo**, que obriga o agent a parar e checar antes de gerar código.

### 2.5 Execution Template

O ritual completo está em [`.claude/agents/_template.md.example`](../.claude/agents/_template.md.example) (linhas 88-119):

```text
════════════════════════════════════════════════════════════════
TASK: _______________________________________________
TYPE: [ ] CRITICAL  [ ] IMPORTANT  [ ] STANDARD  [ ] ADVISORY
THRESHOLD: _____

VALIDATION
├─ KB: .claude/kb/{domain}/_______________
│     Result: [ ] FOUND  [ ] NOT FOUND
│     Summary: ________________________________
│
└─ MCP: ______________________________________
      Result: [ ] AGREES  [ ] DISAGREES  [ ] SILENT
      Summary: ________________________________

AGREEMENT: [ ] HIGH  [ ] CONFLICT  [ ] MCP-ONLY  [ ] MEDIUM  [ ] LOW
BASE SCORE: _____

MODIFIERS APPLIED:
  [ ] Recency: _____
  [ ] Community: _____
  [ ] Specificity: _____
  FINAL SCORE: _____

DECISION: _____ >= _____ ?
  [ ] EXECUTE (confidence met)
  [ ] ASK USER (below threshold, not critical)
  [ ] REFUSE (critical task, low confidence)
  [ ] DISCLAIM (proceed with caveats)
════════════════════════════════════════════════════════════════
```

---

## 3. Fundamentação acadêmica do protocolo de confidence

### 3.1 Nome técnico da técnica geral: **Verbalized Confidence**

O ato de pedir ao LLM para emitir um número de confiança em palavras (não via logits) tem nome próprio: **Verbalized Confidence Estimation**. Foi formalizado por:

- **Lin, Hilton, Evans (2022)** — *"Teaching Models to Express Their Uncertainty in Words"* (paper seminal da OpenAI/Oxford)
- **Tian et al. (2023)** — *"Just Ask for Calibration"* — mostra que pedir o número direto pode ser melhor calibrado que extrair de logits
- **Xiong et al. (2024)** — *"Can LLMs Express Their Uncertainty?"* — survey

### 3.2 Área-mãe: **Uncertainty Quantification (UQ) em LLMs** / **LLM Calibration**

Subcampo de Machine Learning preocupado com: o score que o modelo produz reflete a probabilidade real de acerto? "Calibração" significa que quando o modelo diz 0.90, ele acerta ~90% das vezes. Em LLMs isso é difícil porque modelos pós-RLHF tendem a ser **overconfident**.

### 3.3 Mapeamento técnico das peças do template

| Peça do template | Nome técnico | Referências |
|---|---|---|
| Score numérico verbalizado | **Verbalized Confidence** | Lin 2022, Tian 2023 |
| Cruzar KB + MCP antes de responder | **Retrieval-Augmented Generation** + **Grounding/Groundedness check** | Lewis 2020 (RAG); Es et al. 2023 (RAGAS) |
| Agreement Matrix (KB ↔ MCP) | **Multi-source verification** / **Cross-source consistency** | Manakul 2023 (SelfCheckGPT) |
| Modifiers (recency, examples) | **Confidence calibration with auxiliary signals** | parte de UQ |
| Threshold por categoria de tarefa | **Selective Prediction** / **Selective Classification** / **Abstention** | El-Yaniv 2010 (clássico ML); Kamath 2020 |
| EXECUTE / ASK / REFUSE / DISCLAIM | **Deferral / Abstention policy** ou **Conformal Decision** | Geifman & El-Yaniv 2017 |
| Forçar o agent a preencher checklist | **Structured reasoning / Scaffolded prompting** | parte de Prompt Engineering |
| Auto-questionamento antes de agir | **Self-critique** / **Self-refine** / **Reflexion** | Madaan 2023; Shinn 2023 |
| Verificação passo-a-passo | **Chain-of-Verification (CoVe)** | Dhuliawala 2023 |

### 3.4 Padrão maior: **Confidence-aware Agentic Systems**

Quando você combina **verbalized confidence + retrieval grounding + selective abstention + structured self-critique**, isso vira o que hoje se chama:

- **Confidence-aware agentic systems** (termo mais usado em engenharia)
- **Guardrailed LLM agents** (visão de produção/safety)
- **Decision-theoretic prompting** (visão acadêmica)

E entra no guarda-chuva maior de **Trustworthy AI / Responsible AI** — junto com fairness, robustness, interpretability.

### 3.5 Por que funciona apesar do número ser "inventado"

Resultado importante de **Tian et al. (2023)** e **Kadavath et al. (2022, Anthropic)** — *"Language Models (Mostly) Know What They Know"* — mostrando que LLMs grandes têm **calibração razoável quando forçados a verbalizar**, especialmente se você pede para eles **explicarem o porquê** antes de dar o número (o que é exatamente o que o template faz: KB check → MCP check → Agreement → daí o score).

O mecanismo subjacente é **metacognição emergente**: o modelo, ao gerar a justificativa, ativa atenção sobre os próprios sinais de incerteza (presença/ausência de fontes, contradições) e isso melhora o número final. Se você só pedir "dê um score 0-1", a calibração é ruim. Se forçar o ritual KB+MCP+modifiers, melhora bastante.

### 3.6 Leituras recomendadas

- **Survey definitivo:** Geng et al. (2024) — *"A Survey of Confidence Estimation and Calibration in Large Language Models"*
- **Selective prediction em LLMs:** Yoshikawa & Okazaki (2023) — *"Selective-LAMA"*
- **Self-critique aplicado a agents:** Reflexion (Shinn 2023), CRITIC (Gou 2024)
- **Anthropic-specific:** Constitutional AI (Bai 2022) e *"Discovering Language Model Behaviors with Model-Written Evaluations"* (Perez 2022) — usa princípios parecidos para auto-avaliação

---

## 4. TL;DR

### KBs locais

- **18 domínios** organizados em `.claude/kb/<domain>/{concepts,patterns,specs}/`
- **Não há auto-loading** pelo Claude principal
- **Subagents carregam KBs** via instrução "MANDATORY: Read Before..." em seus próprios system prompts
- O `_index.yaml` é **registry declarativo**, não executável

### Confidence

- **`confidence: 0.95` no `_index.yaml`** = atestado estático de validação do concept (MCP-checked, fresh, com exemplos)
- **Confidence runtime do agent** = score calculado por tarefa, comparado contra threshold para decidir Execute / Ask / Refuse
- **Nada disso é enforcement por código** — é convenção de prompting que o subagent segue ao raciocinar
- Nome acadêmico: **"Verbalized Confidence with Selective Abstention and Multi-Source Grounding"**
- Coloquial: **"confidence-gated agent"** ou **"guardrailed agent execution"**
- Área-mãe: **Uncertainty Quantification em LLMs**, dentro de **Trustworthy AI**
