# Resume Tailor v2

An AI-powered resume tailoring skill built on five core principles: hybrid analysis, fact conservation, semantic equivalence, closed-loop quantification, and reverse audit.
基于 AI 的简历定制技能：混合分析、事实守恒、语义等价、闭环量化、反向审计。

## Quick Start / 快速使用

```
"帮我针对这个 JD 调简历" / "tailor resume to this JD"
```

Provide a JD (URL or text) and a resume file (.docx / .pdf / .txt). The skill will:

1. Research market expectations for the role
2. Extract hard requirements (script) + semantic keywords (LLM) in one pass
3. Match resume against JD with confidence levels
4. Guide you through interactive adjustments (with AI-proposed recommendations)
5. Generate a tailored resume with reverse audit and interview prep

## Architecture / 架构

### Five Core Principles / 五大核心原则

1. **Hybrid Analysis / 混合分析** — Script extracts hard features; LLM handles semantics. Both cross-validate.
2. **Fact Conservation / 事实守恒** — Strict reverse chronological order; structure recovery requires human confirmation.
3. **Semantic Equivalence / 语义等价** — Cross-credential mapping + cultural tone slider (6 regions).
4. **Closed-loop Quantification / 闭环量化** — Anti-Filler Rule: progressive probing → fallback to original. Vague outcomes are forbidden.
5. **Reverse Audit / 反向审计** — Interviewer persona review + mock questions + STAR prep sheets.

### 4-Phase Pipeline / 四阶段流水线

```
Phase 1: Contextual Intelligence / 需求与背景深度挖掘
├── Accept JD + collect company/role info
├── Market research (2 targeted web searches)
└── Unified Context Extraction (one consolidated table)
    ├── Script: hard requirements (years, degree, certs)
    ├── LLM: role context + keywords + skill clusters
    └── Format/ATS/portfolio/timeline risk warnings (consolidated)

Phase 2: Strict Matching / 严谨匹配与风险识别
├── Structure-aware resume reading (with fallback + human verification)
└── Semantic matching
    ├── Direct / Implicit (High/Med/Low) / Gap
    ├── Cross-credential equivalence
    └── Match score calculation

Phase 3: Dynamic Interaction / 动态交互调整
├── Three-tier routing: Fast-Track (≥90%) / Full Flow (50-89%) / Alignment Check (<50%)
├── CP1: Experience selection (reverse chronological, inclusion/exclusion only)
├── CP2: Content gaps (scenario-based probing)
├── CP3: Quantification (Anti-Filler Rule: probe 2 rounds → fallback)
└── CP4: Wording upgrade (cultural tone slider + cross-credential mapping)

Phase 4: Delivery & Reverse Audit / 交付与反向审计
├── Generate Markdown → confirm → .docx (PDF optional)
├── Compliance audit (regional PII rules)
├── Reverse audit
│   ├── Interviewer persona construction
│   ├── Persona-based review (5 dimensions: AI feel, logical gaps, scope inflation, buzzword defense, cultural tone)
│   └── Interview readiness: mock questions + STAR sheets (for 🔴 Major issues)
└── Audit log (diff_audit.py + ats_checker.py)
```

## Files / 文件结构

```
resume-tailor/
├── SKILL.md                          # Skill definition & workflow
├── requirements.txt                  # Python dependencies
├── scripts/
│   ├── main.py                       # Pure argparse CLI layer (no business logic)
│   ├── engine.py                     # Pipeline orchestrator (run_full_pipeline)
│   ├── utils.py                      # Shared utilities (language, PII, date, link detection)
│   ├── jd_parser.py                  # Hard requirement extraction + role detection + portfolio scan
│   ├── diff_audit.py                 # Source vs tailored diff + structure-aware reading
│   └── ats_checker.py                # ATS compatibility check + regional PII detection
└── references/
    ├── interaction_checkpoints.md    # Interactive checkpoint templates
    └── audit_log_template.md         # Audit log structure template
```

## Scripts / 脚本说明

### jd_parser.py — Hard Feature Extractor / 硬特征提取器

Extracts structured features from JD and optionally matches against resume.

```bash
# JD only
python scripts/jd_parser.py --file jd.txt --json

# JD + resume matching
python scripts/jd_parser.py --file jd.txt --resume resume.docx --json
```

**Extracts / 提取内容**:
- Experience years (flexible prefixes: "at least", "不少于", "minimum")
- Degree requirements (tiered: doctoral/master/bachelor/associate)
- Language tests (IELTS, TOEFL, TOEIC, JLPT, TOPIK, CET, CEFR)
- Certifications (generic capital-acronym pattern)
- GPA scores, work authorization, security clearance
- Resume date ranges, role type detection, portfolio link scanning

**Output / 输出**: JSON with `hard_requirements`, `summary`, `resume_date_ranges`, `portfolio`, `pdf_reader_used`

### main.py — CLI Entry Point / 命令行入口

```bash
# Structure-aware resume reading
python scripts/main.py read-structured --resume resume.docx

# Diff comparison (source vs tailored)
python scripts/main.py diff --source-docx source.docx --tailored tailored.md --company "Company" --role "Role" --json
```

### ats_checker.py — ATS Compatibility Checker / ATS 兼容性检查

Validates resume against ATS parsing expectations with regional profiles.

```bash
python scripts/ats_checker.py --resume tailored.md \
    --keywords "Python,SQL,AWS" --region north_america --json
```

**10 Checks**: Tables, Images, Emojis, Non-standard bullets, Missing sections, Contact info, Date inconsistency, Long bullets, Missing keywords, Regional PII

**5 Regional Profiles**:
| Region | Strict | Forbidden PII |
|--------|--------|---------------|
| north_america | ✅ | photo, age, gender, marital, religion, nationality, salary, address |
| uk_ireland | ✅ | photo, age, gender, marital, religion, NI number |
| dach | ❌ | religion, political affiliation |
| east_asia | ❌ | none |
| global | ✅ | same as north_america |

## Cross-Credential Equivalence / 跨证书等价

Scripts extract credentials; LLM maps equivalents with confidence:

| JD Asks | Resume Has | Judgment |
|---------|-----------|----------|
| CET-6 | IELTS 7.5 | ✅ Implicit (High) — exceeds requirement |
| TOEFL 100 | IELTS 7.0 | 🔄 Implicit (Med) — approximate range |
| IELTS 7.0 | CET-4 | ⚪ Gap — below equivalent |

## Dependencies / 依赖

```
python-docx>=0.8.11    # .docx read/write + style detection
pdfplumber>=0.9.0      # PDF reading (primary)
PyPDF2>=3.0.0          # PDF reading (fallback)
```

`pandoc` is optional for PDF generation. If missing, the skill outputs .docx directly.

## Version History / 版本历史

### v2.4 (Current) — Structural Refactor
- **Five Core Principles**: Explicitly anchored — hybrid analysis, fact conservation, semantic equivalence, closed-loop quantification, reverse audit
- **4-Phase structure**: Consolidated from 5 phases — Contextual Intelligence → Strict Matching → Dynamic Interaction → Delivery & Reverse Audit
- **Simplified routing**: 5-tier → 3-tier (Fast-Track ≥90% / Full Flow 50-89% / Alignment Check <50%)
- **Unified extraction**: Merged script + LLM extraction into single consolidated table with integrated risk warnings
- **Removed CP5 (Merge/Split)**: Simplified checkpoint flow to CP1-CP4
- **Shadow Resume**: Moved from default flow to on-demand (only when source ≠ target language)
- **Propose-don't-ask principle**: Every user-facing question must include a concrete recommendation

### v2.3 — Robustness & UX Hardening
- Market research step: collect company + role → web search for hiring preferences
- Experience order hard rule: strict reverse chronological, inclusion/exclusion only
- Page limit hard rule: space budget calculation with over-fill warning
- Markdown preservation: saved as deliverable for diff audit
- Anti-Filler Rule: progressive probing (2 rounds) → fallback to original wording
- Fixed `--read-structured` command path

### v2.2 — Global Perspective Enhancements
- Tech stack freshness detection, timeline gap detection
- Campus scenario library, multi-currency alignment
- Structure recovery verification, portfolio deep advice

### v2.1.1 — Architecture Cleanup
- `engine.py` pipeline orchestrator, `main.py` pure CLI layer
- Shared `utils.py` library, deduplicated ~210 lines

### v2.1 — Interaction & Depth Optimizations
- Fast-Track mode, memory pre-fill, STAR prep sheet, shadow resume
- Unified CLI with shared utils

### v2.0 — Core Rewrite
- Hybrid analysis, skill clustering, structure fallback
- Dynamic routing, cross-credential equivalence, cultural tone slider
- Regional compliance audit, interviewer persona reverse audit
- ATS checker with 5 regional profiles

### v1.0
- Basic keyword extraction and matching, interactive checkpoints, diff audit
