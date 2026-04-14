<div align="center">

# Resume Tailor

**AI-Powered Resume Tailoring — Not a Polisher, a Coach**

*This project follows a "Coach, not Polisher" philosophy.*

[English](README.md) · [简体中文](README.zh-CN.md)

</div>

---

## Why You Need It?

Most AI resume tools **rewrite** your bullets to sound fancy. This one **coaches** you to make them real.

| Traditional AI Rewrite | Resume Tailor |
|---|---|
| ❌ "Significantly improved data analysis efficiency, received team recognition" | ✅ "Built automated reconciliation tool, reducing monthly close cycle from **5 days to 6 hours** across **12 business lines**" |
| Fills vague adjectives when data is missing | Asks targeted questions — or keeps original wording if you can't quantify |
| Optimistic about your role ("Led" everything) | Challenges every claim: *"Were you the decision maker?"* |
| One-size-fits-all output | Adapts tone, format, and privacy rules per target region |

**The difference**: A polished lie gets rejected at the interview. A coached truth gets you hired.

---

## What You Get

You don't just get a tailored resume. You get a **job search toolkit**.

### ✅ Tailored Resume (.docx)
Optimized for the specific JD and target region — ATS-compatible, culturally calibrated, factually accurate.

### 📊 Audit Log
Every modification is tracked:
- Match score with confidence levels for each JD requirement
- Hard gaps flagged (missing certifications, experience thresholds)
- Compliance warnings (photo/age removal by region)

### 🎙️ Interview Prep Pack
For every significant change on your resume, the system generates:
- **Mock Questions** — what interviewers will likely challenge you on
- **STAR Notes** — structured talking points so you can defend each bullet confidently

---

## Core Principles

These are non-negotiable hard rules baked into every run:

### 🚫 Anti-Filler Rule
Every bullet must follow: **Action + Object + Measurable Outcome**
- No numbers? The system asks progressive probing questions.
- Still no numbers after 2 rounds? Keep original wording — never invent metrics.
- **Rule: A vague outcome is WORSE than no outcome.**

### 🪞 Reverse Audit
Before delivery, an interviewer persona reviews every bullet from the attacker's perspective. Role inflation, logical leaps, and buzzword salads get caught before HR sees them.

### ⏳ Fact Conservation
Work experiences stay in **strict reverse chronological order**. No reordering by relevance — only keep or hide.

### 🌐 Cultural Tone Slider
Verb intensity auto-adjusts: assertive (North America) → collaborative (East Asia) → modest (Nordics). Same facts, different presentation.

### ⚖️ Cross-Credential Alignment
IELTS 7.5 ≈ CET-6 550+. The system maps credentials across regions and keeps the strongest one visible.

---

## How It Works

```
Phase 1 — Context & Research     Understand the role, research the company
Phase 2 — Semantic Matching      Match your experience against JD requirements
Phase 3 — Interactive Adjustment Review suggestions, confirm or override
Phase 4 — Audit & Delivery       Final compliance check, mock questions, output
```

| Phase | What Happens | Your Role |
|-------|-------------|-----------|
| **1. Context** | Extract JD requirements (script + LLM), research company, assess risks | Review & confirm |
| **2. Match** | Direct + implicit matching with confidence levels | Review match table |
| **3. Adjust** | Experience selection, gap filling, quantification, wording upgrade | Confirm or override each suggestion |
| **4. Audit** | Compliance check, interviewer-persona review, mock questions, generate .docx | Final review |

Every suggestion comes with a **concrete recommendation** — you confirm or override, never decide from scratch.

---

## Quick Start

```bash
# Provide a JD and your resume
"Tailor my resume for this JD"
```

That's it. The skill handles research, matching, adjustment, and audit in sequence.

---

## Developer Reference

<details>
<summary>📁 File Structure</summary>

```
resume-tailor/
├── SKILL.md                          # Skill definition & workflow
├── requirements.txt                  # Python dependencies
├── scripts/
│   ├── main.py                       # CLI entry point
│   ├── engine.py                     # Pipeline orchestrator
│   ├── utils.py                      # Shared utilities
│   ├── jd_parser.py                  # Hard requirement extraction
│   ├── diff_audit.py                 # Source vs tailored diff
│   └── ats_checker.py                # ATS compatibility check
└── references/
    ├── interaction_checkpoints.md    # Interactive checkpoint templates
    └── audit_log_template.md         # Audit log structure template
```

</details>

<details>
<summary>⚙️ Script Usage</summary>

```bash
# JD only
python scripts/jd_parser.py --file jd.txt --json

# JD + resume matching
python scripts/jd_parser.py --file jd.txt --resume resume.docx --json

# Structure-aware resume reading
python scripts/main.py read-structured --resume resume.docx

# Diff comparison
python scripts/main.py diff --source-docx source.docx --tailored tailored.md

# ATS compatibility check
python scripts/ats_checker.py --resume tailored.md --region north_america --json
```
**Regions:** north_america, uk_ireland, dach, east_asia, global

</details>

<details>
<summary>📦 Dependencies</summary>

```
python-docx>=0.8.11    # .docx read/write
pdfplumber>=0.9.0      # PDF reading (primary)
PyPDF2>=3.0.0          # PDF reading (fallback)
```
Optional: `pandoc` for PDF generation.

</details>

---

## Version History

### v2.4 (Current) — Structural Refactor
- 4-stage pipeline, 3-tier routing, unified extraction
- Anti-Filler Rule, Propose-don't-ask principle, Reverse Audit
- Shadow Resume moved to on-demand

[Full changelog → CHANGELOG.md](CHANGELOG.md)

---

## License

MIT
