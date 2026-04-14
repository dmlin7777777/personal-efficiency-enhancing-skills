<div align="center">

# Resume Tailor

**AI-Powered Resume Tailoring — Not a Polisher, a Coach**
**AI 驱动的简历定制 — 不是润色工具，是求职教练**

[English](#english) · [中文](#中文)

</div>

---

## The Hook / 为什么不一样？

> **🪞 Not just rewriting — it coaches.** Built-in interviewer persona reviews your resume from the attacker's perspective before you send it out.
>
> **🚫 No AI fluff.** The Anti-Filler Rule forces every bullet to carry measurable outcomes. "实现智能化" and "提升效率" (without numbers) get rejected automatically.
>
> **🌍 Works everywhere.** Auto-adapts to regional hiring norms — remove your photo for North America, explain career gaps for Germany, tone down assertiveness for East Asia.

> **🪞 不只是改写，更是教练。** 内置面试官画像，在你投递前从攻击者视角审视简历的每一个漏洞。
>
> **🚫 拒绝 AI 废话。** 强制量化原则——没有数字支撑的"实现智能化"会被自动拦截。
>
> **🌍 全球通行。** 自动适配不同地区的求职潜规则——北美删照片、德国补空窗期、东亚调语调。

---

## Features / 核心能力

### 🎯 Semantic-Level Matching / 语义级匹配
Not keyword stuffing. Recognizes that "抗压能力强" aligns with "Thrives in fast-paced environments" and "数据驱动决策" maps to "Data-informed strategic thinking" — with confidence scores.
不只关键词堆砌。能识别"抗压能力强"与"Thrives in fast-paced environments"的深层语义对齐，并标注匹配置信度。

### ⚖️ Cross-Credential Alignment / 跨证书对齐
JD asks for CET-6 but you only have IELTS 7.5? It tells you they're equivalent — and keeps the stronger credential on your resume.
JD 写了英语六级，你只有雅思 7.5？它会告诉你这超过了要求，并保留更有说服力的证书。

### 🔍 Reverse Interview Audit / 反向面试审计
Generates mock interview questions targeting your resume's weak spots, so you can prepare before the interviewer challenges you.
自动生成针对你简历漏洞的面试追问，让你在被面试官挑战前先做好准备。

### 🚫 Privacy Compliance / 隐私合规
Applying to North America? Automatically flags your photo and birthday for removal. Germany? Reminds you to explain career gaps.
投递北美岗位？自动标记需要删除的照片和生日。德国岗位？提醒你补充空窗期说明。

### 📊 Anti-Filler Enforcement / 拒绝空话
Every bullet must follow: **Action + Object + Measurable Outcome**. If you can't provide numbers, it asks you targeted questions — and if you still can't, it keeps your original wording rather than inventing fake metrics.
每条经历必须满足：**动作 + 对象 + 可量化成果**。说不出数字？它会用场景化追问引导你回忆，而不是编造。

### 🌐 Cultural Tone Slider / 文化语调适配
Adjusts verb intensity and self-promotion level based on target region — assertive for North America, collaborative for East Asia, modest for Nordics.
根据目标地区自动调整动词强度和自我推销程度——北美自信果敢，东亚协同低调，北欧谦逊务实。

---

## Quick Start / 快速开始

```
"帮我针对这个 JD 调简历"
```

Provide a **JD** (URL or pasted text) and your **resume** (.docx / .pdf / .txt). That's it.

The skill handles everything:
1. **Research** — scans current hiring expectations for the role
2. **Match** — compares your resume against JD requirements with confidence levels
3. **Advise** — proposes what to keep, drop, rewrite, or quantify (you confirm or override)
4. **Deliver** — generates a tailored resume with built-in reverse audit and interview prep

```
提供一份 JD（链接或文字）和你的简历（.docx / .pdf / .txt），就这么简单。

系统会自动完成：
1. **调研** — 扫描该岗位当前的招聘偏好
2. **匹配** — 用置信度评分对比你的简历与 JD 要求
3. **建议** — 提出保留、删除、改写、量化的建议（你确认或否决）
4. **交付** — 生成定制简历，附带反向审计和面试准备
```

---

## How It Works / 工作原理

```
Stage 1 — Context & Research          了解你、了解岗位
Stage 2 — Semantic Matching           严谨匹配，标注缺口
Stage 3 — Interactive Adjustment      交互式调整（只给建议，不替你决定）
Stage 4 — Audit & Delivery            反向审计 + 面试备战 + 交付
```

| Stage | What Happens | Your Role |
|-------|-------------|-----------|
| **1. Context** | Extract JD requirements (script + LLM), research company, assess risks | Review & confirm |
| **2. Match** | Direct + implicit matching with confidence levels | Review match table |
| **3. Adjust** | Experience selection, gap filling, quantification, wording upgrade | Confirm or override each suggestion |
| **4. Audit** | Compliance check, interviewer-persona review, mock questions, generate .docx | Final review |

Every suggestion comes with a **concrete recommendation** — you confirm or override, never decide from scratch.
每个建议都附带具体方案——你只需要确认或否决，不需要从零开始做决策。

---

## Developer Reference / 开发者文档

<details>
<summary>📁 File Structure / 文件结构</summary>

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
<summary>⚙️ Script Usage / 脚本使用</summary>

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
<summary>📦 Dependencies / 依赖</summary>

```
python-docx>=0.8.11    # .docx read/write
pdfplumber>=0.9.0      # PDF reading (primary)
PyPDF2>=3.0.0          # PDF reading (fallback)
```

Optional: `pandoc` for PDF generation.

</details>

---

## Version History / 版本历史

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
