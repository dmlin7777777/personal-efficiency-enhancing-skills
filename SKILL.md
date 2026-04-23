---
name: resume-tailor
description: "针对岗位 JD 定制简历，或生成通用方向简历。分析 JD 关键词、匹配源简历、交互式调整建议、反向诚意审计。触发词：调简历、tailor resume、优化简历、生成简历、通用简历、简历定制、resume for this JD"
version: "3.0"
---

# Resume Tailor v3

**Pseudo Multi-Agent + Blackboard Architecture**

Analyze a job description and tailor the source resume to match, using isolated expert nodes for writing and auditing.

## Trigger Phrases

**Mode A (JD-Targeted):**
- "帮我针对这个 JD 调简历" / "tailor my resume for this JD"
- "优化简历给这个岗位" / "optimize resume for this role"
- Any JD text or URL provided with resume adjustment intent

**Mode B (General-Purpose):**
- "帮我针对产品岗位生成一个通用性的简历"
- "做个通用版简历" / "生成XX方向的简历"
- "make a general resume" / "create a role-oriented resume"
- "简历定制" / "简历优化"

## Resume Input

On first run, **ask the user to provide their resume file path** (.docx preferred, .pdf or .txt acceptable).
Store the path in memory. **Never modify the original.**

## Operating Modes

Resume Tailor has two operating modes, determined by whether a JD is provided:

### Mode A: JD-Targeted（有 JD 定制）

Full 4-phase pipeline. This is the primary mode.

**Trigger**: User provides a JD (text, URL, or file) alongside resume adjustment intent.

**Flow**: Phase 1 → Phase 2 → Phase 3 → Phase 4 (see Workflow Pipeline below)

### Mode B: General-Purpose（无 JD 通用）

Simplified pipeline when no specific JD is available. Builds a role-oriented resume using capability matching from the story library.

**Trigger**:
- User asks for a resume "for X role" without providing a JD
- "帮我针对产品岗位生成一个通用性的简历"
- "做个通用版简历" / "make a general resume"
- "生成XX方向的简历" / "create a role-oriented resume"

**Flow**:

```
Phase G1: Capability Matching (replaces Phase 1+2)
  1. Identify target role type from user's description (e.g., 产品/数据/商业分析)
  2. Read project story library (唯一事实来源) → extract all experiences
  3. Build capability matching matrix: experience × core role competencies
  4. Rank experiences by match score
  5. Present selection recommendation to user (CP1)

Phase G2: Interactive Refinement (= Phase 3, CP1-CP4)
  CP1: Experience selection (which experiences to keep/hide)
  CP2: Skipped (no JD → no gap analysis)
  CP3: Quantification audit (Anti-Filler Rule — same as Mode A)
  CP4: Wording upgrade (same as Mode A, but use general role tone)

Phase G3: Delivery & Audit (= Phase 4)
  Same physical isolation audit as Mode A.
  Additional Auditor check: "Does this bullet claim something not in the story library?"
```

**Key Differences from Mode A**:
- No JD → No `jd_facts` layer, no ATS keyword matching, no hard requirement alerts
- Story library is the **sole source of truth** — no fabrication, no speculation, no "logical inference"
- If story library lacks data for a bullet → ask user to confirm, never invent
- Simpler matching: role-type competencies instead of JD-specific keywords

**⚠️ Critical Rule for Mode B**: 
> **只做提炼，不做扩展。** Even logically reasonable inferences (e.g., "覆盖从需求定义到上线的完整周期") are FORBIDDEN unless explicitly stated in the story library. Only distill and reorganize what already exists.

## Five Core Principles

| # | Principle | One-Line Definition |
|---|-----------|---------------------|
| 1 | **Hybrid Analysis** | Script extracts hard facts (jd_parser.py), LLM extracts semantics. Cross-validate. |
| 2 | **Fact Conservation** | Strict reverse chronological order. Only inclusion/exclusion allowed. |
| 3 | **Semantic Equivalence** | Cross-credential mapping (IELTS ≈ CET-6). Cultural tone slider by region. |
| 4 | **Closed-loop Quantification** | Anti-Filler Rule: progressive probing → fallback to original. No vague outcomes. |
| 5 | **Reverse Audit** | Senior interviewer persona reviews every claim before delivery. 🔴 Major issues trigger rollback. |

## Architecture Overview

```
engine.py (Orchestrator)
├── Initialize snapshot.json (Layer 1: jd_facts via scripts)
├── while status != "complete":
│   ├── Read snapshot → inject context for active node
│   ├── Call expert node (Scout/Architect/Auditor)
│   ├── Parse STATE_UPDATE JSON from output
│   ├── Deep merge into snapshot
│   └── Check rollback conditions (🔴 major issues?)
├── Render final deliverables
└── Archive: sessions/ → history/
```

### Expert Nodes

| Node | File | Responsibility |
|------|------|---------------|
| **Context Scout** | `references/writer_guide.md` (Phase 1 section) | JD extraction, market research, role detection, capability clustering |
| **Resume Architect** | `references/writer_guide.md` (CP1-CP5) | CP1 selection, CP2 gaps, CP3 quantification, CP4 wording upgrade, CP5 draft |
| **Sincerity Auditor** | `references/auditor_guide.md` | Compliance check, sincerity review, mock interview questions, STAR prep |

### State Protocol

All nodes communicate via `context_snapshot.json` (see `schemas/snapshot_schema_v1.json`):
- **Layer 0 (`_meta`)**: Session metadata, turn history, nuance buffer
- **Layer 1 (`jd_facts`)**: Script-populated, read-only after init
- **Layer 2 (`user_decisions`)**: User-confirmed interactions, persistent
- **Layer 3 (`expert_outputs`)**: Node outputs, volatile, can be overwritten

Every node MUST append `STATE_UPDATE JSON` at end of output (see `templates/state_update_template.md`).

## Workflow Pipeline

### Phase 1: Contextual Intelligence

**Node**: Context Scout
**Reference**: `references/writer_guide.md` (Phase 1 section)
**Output**: Populated `jd_facts`, `scout_report`, capability clusters
**Tools**: `scripts/jd_parser.py` (with graceful fallback to LLM), `web_search`

1. Accept JD input (URL → fetch, or text directly)
2. Ask user: company name? target region?
3. Run market research (2 targeted web searches)
4. Execute unified context extraction (script + LLM in one pass)
5. Detect role level, region, document type
6. Output consolidated context table + risk warnings

### Phase 2: Strict Matching

**Node**: Context Scout (continuation) or Architect (if Fast-Track)
**Reference**: Integrated into Phase 1 or `references/writer_guide.md`

1. Read source resume (structured reader for .docx, fallback for .pdf)
2. Semantic matching: Direct + Implicit (with confidence) + Gaps
3. Cross-credential alignment
4. Match score calculation
5. Hard requirement alerts (dealbreakers)

### Phase 3: Dynamic Interaction

**Node**: Resume Architect
**Reference**: `references/writer_guide.md`
**Sub-nodes**: `architect_writer` → `architect_quantify` → `architect_wording`
**Checkpoint details**: `references/interaction_checkpoints.md`

#### Step 3a: Three-Tier Routing

| Tier | Score | Flow |
|------|-------|------|
| **Fast-Track** | ≥90% | Draft + suggestions in one pass, skip deep CPs |
| **Full Flow** | 50–89% | CP1→CP2→CP3→CP4 all executed |
| **Alignment Check** | <50% | Confirm intent before proceeding |

#### Step 3b: Checkpoints (Always CP1, CP3, CP4; CP2 in Full Flow)

| CP | Name | What Happens |
|----|------|-------------|
| CP1 | Experience Selection | Reverse chronological review, user picks keep/hide |
| CP2 | Content Gaps | Scenario-based gap filling (implicit matches) |
| CP3 | Quantification | Anti-Filler Rule: progressive probing, no vague filler |
| CP4 | Wording Upgrade | Verb map, cultural tone slider, before→after comparison |

**Global Interaction Principle**: Every question must include a concrete recommendation. User confirms or overrides — never decides from scratch.

### Phase 4: Delivery & Audit (Physical Isolation)

**Two separate LLM calls — this is the critical architectural guarantee.**

#### Step 4a: Writer Node — Generate Draft

**Node**: Resume Architect (`architect_writer`)
**Input**: All confirmed decisions from Phase 3
**Action**: Generate Markdown draft, save to `history/YYYY-MM-DD_{company}_{role}.md`
**Constraint**: DO NOT self-audit. Just produce the draft.

#### Step 4b: Auditor Node — Compliance Check

**Node**: Sincerity Auditor (`auditor_compliance`)
**Input**: Draft + target region rules
**Action**: Regional compliance (photo, age, PII per region)
**Output**: Compliance table with 🔴 critical violations

#### Step 4c: Auditor Node — Reverse Audit

**Node**: Sincerity Auditor (`auditor_sincerity`)
**Input**: Draft + interviewer persona + JD context
**Actions**:
1. Construct senior interviewer persona based on role type
2. Review every bullet for: AI trace, logical gap, scope inflation, buzzword defense, cultural mismatch
3. Classify severity: 🔴 MAJOR / 🟡 MINOR / 🟢 INFO
4. For each 🔴 MAJOR: generate mock interview questions + STAR prep sheets

**If 🔴 MAJOR found**: Set flag `["ROLLBACK"]` in STATE_UPDATE → engine reverts to Phase 3

#### Step 4d: Compile & Deliver

1. Run `scripts/diff_audit.py` (source vs tailored change evidence)
2. Run `scripts/ats_checker.py` (ATS compatibility score)
3. Compile final audit log combining all sources
4. Render output (see Rendering section below)
5. Archive snapshot from `sessions/` to `history/`

## Rendering Pipeline

```
Layer 3 Draft (Markdown)
    ↓ Phase 1: Regex Preprocessing
    "**Summary**: detail" → "<span class='bullet-summary'>Summary:</span> detail"
    ↓ Phase 2: MD → HTML Fragment
    markdown-it-py (preferred) / python-markdown (fallback)
    ↓ Phase 3: Jinja2 Layout
    CSS-inlined complete HTML document via templates/resume_layout.html.j2
    ↓ Phase 4a: WeasyPrint → PDF (with page overflow detection)
    ↓ Phase 4b: pypandoc → DOCX (clean conversion)
```

**Graceful degradation**:
- WeasyPrint unavailable → HTML-only output with "Print → Save as PDF" prompt
- pandoc unavailable → raw Markdown export
- markdown-it-py unavailable → python-markdown fallback

CSS template: `templates/resume_template.css` (Tech Style, single-column, A4 portrait)

## Output Structure

```
{resume_directory}/
├── resume_source.docx              # Original — NEVER modified
├── schemas/snapshot_schema_v1.json # Protocol definition
├── templates/state_update_template.md
├── references/                     # Expert node guides
│   ├── writer_guide.md
│   ├── auditor_guide.md
│   ├── interaction_checkpoints.md
│   └── audit_log_template.md
├── sessions/{session_id}/          # Runtime snapshots
│   └── snapshot.json
└── history/
    ├── {date}_{company}_{role}.md           # Tailored Markdown
    ├── {date}_{company}_{role}.docx         # Final deliverable
    ├── {date}_{company}_{role}_audit.md     # Audit log
    ├── {date}_{company}_{role}_snapshot.json# Archived state
    └── ...
```

## Error Handling

| Error | Action |
|-------|--------|
| No resume file | Ask user to provide path |
| No JD provided | Switch to Mode B (General-Purpose) — see Operating Modes |
| JD URL fetch fails | Ask user to paste text |
| Story library missing data for a claim | Ask user to confirm — NEVER fabricate or infer |
| STATE_UPDATE JSON parse fail | Inject self-correction prompt, retry once |
| 🔴 Major issues in audit | ROLLBACK flag → revert to Phase 3 |
| LLM timeout | Retry with same snapshot context |
| Script failure (jd_parser etc.) | Degrade gracefully, Scout node handles via LLM, do NOT abort |

## Dependencies

```
# v3.0 Rendering Pipeline (core)
jinja2>=3.1.0              # Template engine
markdown-it-py>=3.0.0      # Markdown → HTML (preferred)
weasyprint>=60.0           # PDF generation (optional, graceful fallback)
pypandoc>=1.17             # DOCX generation (optional, requires pandoc CLI)
pyyaml>=6.0                # Snapshot schema YAML support

# v2.x Resume I/O (still used)
python-docx>=0.8.11        # .docx read/write
pdfplumber>=0.10.0         # PDF reading (primary)

# Optional fallbacks
python-markdown>=3.5.0     # Fallback MD parser
PyPDF2>=3.0.0              # Fallback PDF reader
```
