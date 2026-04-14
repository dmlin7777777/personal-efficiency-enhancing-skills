<div align="center">

# Resume Tailor

**AI-Powered Resume Tailoring — Not a Polisher, a Coach**

</div>

---

## Why Different?

> **🪞 Not just rewriting — it coaches.** Built-in interviewer persona reviews your resume from the attacker's perspective before you send it out.
>
> **🚫 No AI fluff.** The Anti-Filler Rule forces every bullet to carry measurable outcomes. Vague phrases like "achieved intelligent automation" get rejected automatically.
>
> **🌍 Works everywhere.** Auto-adapts to regional hiring norms — remove your photo for North America, explain career gaps for Germany, tone down assertiveness for East Asia.

---

## Features

### 🎯 Semantic-Level Matching
Not keyword stuffing. Recognizes that "抗压能力强" aligns with "Thrives in fast-paced environments" and "数据驱动决策" maps to "Data-informed strategic thinking" — with confidence scores.

### ⚖️ Cross-Credential Alignment
JD asks for CET-6 but you only have IELTS 7.5? It tells you they're equivalent — and keeps the stronger credential on your resume.

### 🔍 Reverse Interview Audit
Generates mock interview questions targeting your resume's weak spots, so you can prepare before the interviewer challenges you.

### 🚫 Privacy Compliance
Applying to North America? Automatically flags your photo and birthday for removal. Germany? Reminds you to explain career gaps.

### 📊 Anti-Filler Enforcement
Every bullet must follow: **Action + Object + Measurable Outcome**. If you can't provide numbers, it asks you targeted questions — and if you still can't, it keeps your original wording rather than inventing fake metrics.

### 🌐 Cultural Tone Slider
Adjusts verb intensity and self-promotion level based on target region — assertive for North America, collaborative for East Asia, modest for Nordics.

---

## Quick Start

```
"Tailor my resume for this JD"
```

Provide a **JD** (URL or pasted text) and your **resume** (.docx / .pdf / .txt). That's it.

The skill handles everything:
1. **Research** — scans current hiring expectations for the role
2. **Match** — compares your resume against JD requirements with confidence levels
3. **Advise** — proposes what to keep, drop, rewrite, or quantify (you confirm or override)
4. **Deliver** — generates a tailored resume with built-in reverse audit and interview prep

---

## How It Works

| Stage | What Happens | Your Role |
|-------|-------------|-----------|
| **1. Context** | Extract JD requirements (script + LLM), research company, assess risks | Review & confirm |
| **2. Match** | Direct + implicit matching with confidence levels | Review match table |
| **3. Adjust** | Experience selection, gap filling, quantification, wording upgrade | Confirm or override each suggestion |
| **4. Audit** | Compliance check, interviewer-persona review, mock questions, generate .docx | Final review |

Every suggestion comes with a **concrete recommendation** — you confirm or override, never decide from scratch.

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

### jd_parser.py — Extract structured features from JD
```bash
# JD only
python scripts/jd_parser.py --file jd.txt --json

# JD + resume matching
python scripts/jd_parser.py --file jd.txt --resume resume.docx --json
```

### main.py — CLI entry point
```bash
# Structure-aware resume reading
python scripts/main.py read-structured --resume resume.docx

# Diff comparison (source vs tailored)
python scripts/main.py diff --source-docx source.docx --tailored tailored.md --company "Company" --role "Role" --json
```

### ats_checker.py — ATS compatibility check
```bash
python scripts/ats_checker.py --resume tailored.md --keywords "Python,SQL,AWS" --region north_america --json
```

**Regional profiles**: north_america, uk_ireland, dach, east_asia, global

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
- 4-stage pipeline (consolidated from 5), 3-tier routing, unified extraction
- Anti-Filler Rule, Propose-don't-ask principle, Reverse Audit
- Shadow Resume moved to on-demand

### v2.3 — Robustness & UX Hardening
- Market research, experience order hard rule, page limit, Anti-Filler Rule

[Full changelog → CHANGELOG.md](CHANGELOG.md)

---

## License

MIT
