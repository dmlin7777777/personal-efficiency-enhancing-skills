# Resume Tailor v2

An AI-powered resume tailoring skill with hybrid analysis (script + LLM), semantic matching with confidence levels, dynamic checkpoint routing, and cross-cultural adaptation.

基于 AI 的简历定制技能：混合分析（脚本 + LLM）、带置信度的语义匹配、动态路由、跨文化适配。

## Quick Start / 快速使用

```
"帮我针对这个 JD 调简历" / "tailor resume to this JD"
```

Provide a JD (URL or text) and a resume file (.docx / .pdf / .txt). The skill will:

1. Extract hard requirements via script (years, degree, certifications, etc.)
2. Extract semantic keywords via LLM (skills, soft skills, domain knowledge)
3. Match resume against JD with confidence levels
4. Guide you through interactive adjustments
5. Generate a tailored resume with full audit trail

## Architecture / 架构

### Design Principles / 设计原则

1. **Script extracts, LLM judges / 脚本提取，LLM 判断** — Scripts do feature extraction only (numbers, dates, certifications); LLM handles semantic matching and cross-credential equivalence
2. **Feature Presence ≠ Definitive Match / 存在 ≠ 匹配** — Scripts report features found; LLM decides if they meet requirements
3. **Generic, not hardcoded / 通用化** — No China/US-centric assumptions; works with any credential system, date format, or language
4. **Culture-adaptive / 文化自适应** — Different norms, tone, and PII rules per target region

### 5-Phase Pipeline / 五阶段流水线

```
Phase 1: Hybrid JD Analysis (Auto)
├── Step 1a: Accept JD input (URL/text)
├── Step 1b: Script feature extraction (jd_parser.py)
│   ├── Experience years, degree, language tests, certifications
│   ├── GPA, work authorization, security clearance
│   ├── Resume date ranges, portfolio links scan
│   └── Position weight signal (first 20% = dealbreakers)
└── Step 1c: LLM semantic extraction
    ├── 1c-i: Role context detection (level + region + doc type + work arrangement)
    ├── 1c-ii: Keyword extraction + skill clustering
    └── 1c-iii: Cross-validation with script output

Phase 2: Semantic Match Analysis (Auto)
├── Step 2a: Structure-aware resume reading
│   ├── read_docx_structured() with style detection
│   ├── Structure fallback: LLM semantic recovery if Normal > 80%
│   ├── Format risk detection + portfolio link check
│   └── Regional ATS compatibility check (ats_checker.py)
└── Step 2b: Semantic matching
    ├── Direct / Implicit (High/Med/Low) / Gap
    ├── Cross-credential equivalence mapping
    ├── Cultural soft skill translation
    ├── Skill cluster matching
    └── Match score calculation

Phase 3: Interactive Adjustment (Dynamic Routing)
├── Step 3a: Dynamic routing based on match score
│   ├── ≥90%: Skip checkpoints 2 + 5
│   ├── 70-89%: Full flow
│   ├── 50-69%: Extended probing
│   └── <50%: Alignment check first
├── Step 3b: Execute checkpoints
│   ├── CP1: Experience selection
│   ├── CP2: Content gaps (persona-aware probing)
│   ├── CP3: Quantification (industry-aware)
│   ├── CP4: Wording upgrade (cultural tone slider + risk classification)
│   └── CP5: Experience merge/split

Phase 4: Generate Tailored Resume
├── Markdown draft → User review
├── Generate .docx (python-docx)
└── Convert to PDF (pandoc)

Phase 5: Version Audit
├── Step 5a: Save tailored resume
├── Step 5b: Regional compliance audit (5 region PII rules)
├── Step 5c: Sincerity check (reverse audit)
│   ├── 5c-i: Interviewer persona construction
│   ├── 5c-ii: Persona-based review (5 dimensions)
│   └── 5c-iii: Interview question prep (for 🔴 Major issues)
└── Step 5d: Generate audit log
    ├── diff_audit.py: source vs tailored diff
    ├── ats_checker.py: ATS compatibility report
    └── Compile final audit report (audit_log_template.md)
```

## Files / 文件结构

```
resume-tailor/
├── SKILL.md                          # Skill definition & workflow
├── requirements.txt                  # Python dependencies
├── scripts/
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

### diff_audit.py — Diff & Structure Reader / 差异与结构读取

Reads .docx with style awareness and compares source vs tailored resume.

```bash
# Structure-aware read
python scripts/diff_audit.py --read-structured resume.docx

# Diff comparison
python scripts/diff_audit.py --source-docx source.docx --tailored-docx tailored.md --json
```

**Features / 功能**:
- `read_docx_structured()`: paragraph style detection (Heading/Normal/ListBullet/TableCell)
- Three-level risk classification per change
- `--json` output for pipeline integration
- `source_structure` for Phase 2 context injection

### ats_checker.py — ATS Compatibility Checker / ATS 兼容性检查

Validates resume against ATS parsing expectations with regional profiles.

```bash
python scripts/ats_checker.py --resume tailored.md \
    --keywords "Python,SQL,AWS" --region north_america --json
```

**10 Checks / 10 项检查**:
Tables, Images, Emojis, Non-standard bullets, Missing sections, Contact info, Date inconsistency, Long bullets, Missing keywords, Regional PII

**5 Regional Profiles / 5 个区域配置**:
| Region | Strict | Forbidden PII |
|--------|--------|---------------|
| north_america | ✅ | photo, age, gender, marital, religion, nationality, salary, address |
| uk_ireland | ✅ | photo, age, gender, marital, religion, NI number |
| dach | ❌ | religion, political affiliation |
| east_asia | ❌ | none |
| global | ✅ | same as north_america |

## Regional Adaptation / 区域适配

The system auto-detects target region from JD signals and adapts:

- **Phase 1**: Adjusts keyword weights (Campus vs Social vs Executive)
- **Phase 2**: Applies cultural soft skill translation, cross-credential equivalence
- **Phase 3**: Routes to region-appropriate checkpoint questioning
- **Phase 4**: Determines output language (JD language, not resume language)
- **Phase 5**: Runs region-specific compliance audit + ATS profile

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

### v2.1 (Current)
- Hybrid analysis: script extracts features, LLM does semantic matching
- Skill clustering for keyword grouping
- Structure fallback: LLM semantic recovery when styles are lost
- Dynamic routing based on match score
- Cross-credential equivalence with confidence levels
- Cultural tone slider (6 regional presets)
- Regional compliance audit (5 regions)
- Interview readiness: mock questions for 🔴 Major issues
- ATS checker with regional profiles
- Portfolio link detection (script-level)
- PDF reader tracking with degradation warnings

### v1.0
- Basic keyword extraction and matching
- Interactive checkpoints
- Diff audit
