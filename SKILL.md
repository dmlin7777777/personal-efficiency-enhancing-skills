---
name: resume-tailor
description: This skill should be used when the user wants to tailor their resume to a specific job description (JD). It analyzes JD keywords, matches against the source resume, provides adjustment suggestions with interactive checkpoints, and generates a tailored resume in docx format with full reverse audit.
---

# Resume Tailor

Analyze a job description and tailor the source resume to match, with interactive checkpoints for content decisions and full reverse audit.

## Trigger Phrases

- "帮我针对这个 JD 调简历" / "tailor resume to this JD"
- "优化简历给这个岗位" / "optimize resume for this role"
- "这份简历匹配这个岗位吗" / "is my resume a good fit"
- Any JD text or URL provided with resume adjustment intent

## Resume Input

On first run, **ask the user to provide their resume file path** (absolute path to .docx, .pdf, or .txt). Acceptable formats:
- `.docx` — preferred, preserves formatting
- `.pdf` — readable but harder to preserve layout
- `.txt` / `.md` — plain text

Store the path in memory for the session. If the user provides a new path, update accordingly.

All tailored versions derive from this source file. **Never modify the original.**

If no path is provided and no resume file is found in the workspace, guide the user to place one.

---

## Five Core Principles / 五大核心原则

These are the non-negotiable foundations of this skill. Every phase and checkpoint must uphold them.

### 1. Hybrid Analysis / 混合分析
Script (`jd_parser.py`) extracts structured features (years, degrees, certifications). LLM extracts semantic meaning (capability clusters, business logic). Both cross-validate — script catches what LLM misses, LLM interprets what script can't.

### 2. Fact Conservation / 事实守恒
- **Strict reverse chronological order**: Work/internship entries are NEVER reordered by relevance. Only inclusion or exclusion is allowed.
- **Structure recovery confirmation**: When resume styling is lost and LLM reconstructs section boundaries, the user MUST confirm before proceeding.

### 3. Semantic Equivalence / 语义等价
- **Cross-credential mapping**: IELTS 7.0 ≈ CET-6 550+ — retain the original credential and add an equivalence note.
- **Cultural tone slider**: Adjust assertiveness level based on target region (North America: assertive; East Asia: collaborative; etc.). Applied in CP4 as suggestions, never auto-applied.

### 4. Closed-loop Quantification / 闭环量化
**Anti-Filler Rule (see interaction_checkpoints.md)**: If a bullet lacks a quantified outcome, the LLM must progressively probe (up to 2 rounds) for measurable evidence. If the user still cannot provide data, keep the original wording or remove the outcome clause. **A vague outcome ("实现智能化", "提升效率") is WORSE than no outcome.**

### 5. Reverse Audit / 反向审计
After generating the tailored resume, simulate a senior interviewer reviewing it. Flag AI-generated feel, logical gaps, scope inflation, and buzzword defense risks. For every 🔴 Major issue, generate mock interview questions and STAR preparation sheets.

---

## Workflow

### Phase 1: Contextual Intelligence / 需求与背景深度挖掘

**Philosophy / 理念**: Understand not just what the JD says, but the market context, role level, and cultural norms that shape what the hiring manager actually looks for.

#### Step 1a: Accept JD + Market Research / 接收 JD + 市场调研

1. **Accept JD input** — URL or plain text.
   - If URL: use `web_fetch` to extract job description content.
   - If text: use directly.

2. **Ask for company and role context / 收集公司+岗位信息**:

   "请问这是哪个公司的岗位？具体岗位名称是什么？"
   - If the user provides company name and role:

3. **Web search for market expectations / 岗位偏好搜索**:

Use `web_search` with 2 targeted queries:
   - Query 1: "2026 [company] [role] 招聘偏好 技能要求"
   - Query 2: "[company] [role] 面试重点 产品文化"
   - Fallback (if no company): "2026 [role] 岗位趋势 技能要求"

Present findings briefly: "🔍 市场调研: [2-3 key insights]"

These insights feed into keyword extraction and checkpoint design.

#### Step 1b: Unified Context Extraction / 统一上下文特征提取

Execute script extraction and LLM semantic analysis in one pass. Present a **single consolidated table** to the user.

**Step 1b-i: Run script for hard requirements**:
```bash
python scripts/jd_parser.py --file <jd_path> --json [--resume <resume_path>]
```

Script extracts: experience years, degree requirements, language tests, certifications, GPA, work authorization, date ranges.
Script does NOT extract: soft skills, domain knowledge, business capabilities → LLM handles these.

**Position weight signal**: Requirements in the first 20% of JD → likely Dealbreakers. Last 20% → likely Nice-to-have.

**Step 1b-ii: Role Context Detection / 岗位上下文检测**:

```
1. Role Level / 岗位层级:
   "应届"/"intern" → Campus | "3+ years"/"manager" → Social | "VP"/"总监" → Executive

2. Target Region / 目标区域:
   North America | UK/Ireland | DACH | East Asia | Middle East | Global/Remote

3. Document Type: CV (Academic/UK/EU) vs Resume (Industry/US)

4. Work Arrangement: Remote | Hybrid | On-site | Timezone-restricted
```

Output: "检测结果：Campus 岗位、东亚地区、Resume 格式、On-site。"

**Step 1b-iii: LLM Keyword Extraction + Skill Clustering / 语义关键词提取 + 能力簇聚类**:

Read full JD text + script JSON output. Extract keywords by category (Hard Skills, Soft Skills, Domain Knowledge, Experience Context), assign weights (🔴 Core / 🟡 Nice-to-have), then cluster into capability groups.

**Output — Single Consolidated Table**:

```
## 上下文特征提取 / Context Extraction

### 角色定位
- 岗位层级: [Campus/Social/Executive]
- 目标区域: [Region]
- 文档类型: [CV/Resume]
- 工作安排: [Remote/Hybrid/On-site]

### 关键词与能力簇
| # | 关键词 | 能力簇 | 权重 | JD 证据 |
|---|--------|--------|------|---------|

### 硬指标检查 (脚本)
| 指标 | JD 要求 | 简历状态 |
|------|---------|---------|

### 格式与兼容性风险
| 风险项 | 严重度 | 建议 |
|--------|--------|------|
```

**Integrated Format & Risk Warnings / 整合格式与风险提示**:

After reading the resume (Step 2a), consolidate ALL risk warnings into a single table above:
- **ATS risk**: Table-heavy layout, missing section headings, fragmented content from graphic PDF
- **PDF reading fallback**: If pdfplumber unavailable, note degraded quality
- **Timeline gaps**: ≥3 months between entries
- **Portfolio links**: Missing GitHub/Behance/etc. for relevant role types
- **Tech stack freshness**: Legacy-only tech in a category

Do NOT scatter these warnings across multiple phases — present them once here.

---

### Phase 2: Strict Matching / 严谨匹配与风险识别

**Philosophy / 理念**: Go beyond literal keyword matching. Use semantic understanding and capability clusters to identify implicit matches, while grading confidence to prevent over-interpretation.

#### Step 2a: Read Resume with Structure Awareness / 结构感知读取

If the source resume is .docx, use the structured reader:
```bash
python scripts/main.py read-structured --resume <resume_path>
```

**Structure Fallback / 结构降级兜底**:

If `Normal` style > 80% of paragraphs → launch LLM Semantic Structure Recovery.
After recovery, **present section boundaries to user for confirmation** (see interaction_checkpoints.md — Structure Recovery section). Do NOT proceed without user confirmation.

#### Step 2b: Semantic Matching / 语义匹配

Compare Phase 1 keyword table against resume content.

**Match levels**:

| Level | Definition | Default Confidence |
|-------|-----------|--------------------|
| ✅ Direct | Keyword appears verbatim | High |
| 🔄 Implicit | Same capability, different wording | High / Medium / Low |
| ⚪ Gap | No related content found | — |

**Implicit match rules**:
- MUST provide "Match Reason" column
- MUST assign confidence: High / Medium / Low
- Low confidence → forwarded to CP4 for user verification
- **Anti-hallucination**: If unsure, mark as Gap — do NOT inflate the score

**Equivalence & Proxy Matching**:
- JD asks CET-6, resume has IELTS 7.5 → ✅ Implicit (High)
- JD asks IELTS 7.0, resume has CET-4 → ⚪ Gap
- Cross-reference: IELTS 7.0 ≈ TOEFL 95-100 ≈ CET-6 550+ (mark as Implicit Medium when crossing test types)

**Cultural Translation of Soft Skills**:
- "抗压能力强" (CN) ≈ "Thrives in fast-paced environments" (US)
- Do NOT translate word-for-word — translate the underlying capability
- Offer as CP4 suggestions, never auto-apply

**Match Score**:
```
Score = (Direct×1.0 + Implicit_High×0.8 + Implicit_Med×0.5 + Implicit_Low×0.2 + Gap×0) / Total × 100%
```

**Output format**:
```
## 匹配度分析

### 概览
Match Score: XX% (Direct: X | Implicit High: X | Implicit Med: X | Gap: X)

### ✅ Direct Matches (X)
| JD Keyword | Resume Evidence | Section |

### 🔄 Implicit Matches (X)
| JD Keyword | Match Reason | Confidence | Resume Evidence |

### ⚪ Gaps (X)
| JD Keyword | Weight | Notes |

### ⚠️ Hard Requirement Alerts
| Requirement | JD Value | Resume Status | Action |
```

**Language determination**: Tailored resume language = JD language, NOT source resume language. Translate + culturally adapt if mismatch.

---

### Phase 3: Dynamic Interaction / 动态交互调整

**Philosophy / 理念**: Not all resumes need the same level of adjustment. Route intelligently, then execute checkpoints interactively.

#### Step 3a: Three-Tier Routing / 三级路由

**Hard Requirement Pre-check**:
```
if script hard_gaps contain "dealbreaker" items (e.g., work authorization):
  → Alert: "⚠️ JD requires [X] which was not found. This is typically non-negotiable.
   Continue? (Yes/No)"
```

**Match Score Routing**:

| Tier | Score | Flow |
|------|-------|------|
| **Tier 1: Fast-Track** | ≥ 90% | Generate draft + suggestion table directly, skip CP2/CP5 |
| **Tier 2: Full Flow** | 50%–89% | Execute CP1 → CP2 → CP3 → CP4 (with CP5 optional) |
| **Tier 3: Alignment Check** | < 50% | Confirm delivery intent before proceeding |

**Fast-Track Mode (Tier 1)**:
```
1. Generate "Recommended Adjustments" table + Markdown draft in ONE message
2. User confirms → proceed to Phase 4
3. User requests changes → apply and re-present
4. User switches to Full Mode → enter Tier 2 flow
```

**Alignment Check (Tier 3)**:
```
"Match Score: [X]%. 简历与 JD 匹配度较低，请先确认：
1. 你确实想投这个方向的岗位吗？
2. 有没有简历里没写的相关经历？
3. 这个 JD 是参考还是实际投递目标？"
```

**Memory Pre-fill**: Before executing any checkpoint, check `{resume_dir}/history/user_profile_cache.json` for previously provided data. Pre-fill suggestions when keyword overlap is detected.

#### Step 3b: Execute Checkpoints / 执行介入点

**CRITICAL**: Follow the checkpoints in `references/interaction_checkpoints.md`. This file contains the Global Interaction Principle and detailed guidance for each checkpoint.

**⚠️ GLOBAL HARD RULES / 全局硬约束**:

```
1. EXPERIENCE ORDER HARD RULE:
   Work/internship entries MUST remain in REVERSE CHRONOLOGICAL ORDER.
   ONLY operation allowed: INCLUSION or EXCLUSION (取舍).
   Exception: Personal projects CAN be ordered by relevance.

2. PAGE LIMIT HARD RULE:
   Ask on first run: "简历需要控制在几页以内？(默认 1 页)"
   HARD constraint — final output MUST fit within the limit.
   If user requests more entries than budget allows → warn with specific numbers.

3. SPACE BUDGET CALCULATION:
   After CP1, estimate: Header ~2 lines, Education ~3-4 lines,
   Per work entry ~4-6 lines, Per project ~3-4 lines, Skills ~2-3 lines.
   1-page A4 budget: ~45-50 lines (11pt font).
   If total > budget → warn BEFORE generating.
```

**Checkpoint execution order**:

1. **CP1: Experience Selection / 经历取舍** — Always execute.
   Present in reverse chronological order with ✅/⚠️/❌ recommendations.
   User confirms which to keep/remove.

2. **CP2: Content Gaps / 内容缺口** — Execute in Tier 2.
   For each gap, use scenario-based prompts (not closed-ended questions).

3. **CP3: Quantification / 量化补充** — Always execute.
   Apply Anti-Filler Rule strictly: progressive probing → fallback to original wording.
   Never use vague descriptors ("实现智能化", "提升效率") as substitutes.

4. **CP4: Wording Upgrade / 措辞升级** — Always execute.
   Weak verb → Strong verb + Business impact.
   Apply cultural tone slider for target region.
   Includes Low-confidence implicit matches from Phase 2 for user verification.
   Every change must be confirmed by user (⚠️ for potential over-claims).

**Multi-Currency Value Alignment**: When resume uses CNY but JD targets another region, suggest approximate conversion with context. Use target currency as primary, original as parenthetical. Never fabricate numbers.

---

### Phase 4: Delivery & Reverse Audit / 交付与反向审计

**Philosophy / 理念**: The tailored resume is not complete until it passes the "senior interviewer" test. Every claim must be defensible in an interview.

#### Step 4a: Generate & Deliver / 生成与交付

1. **Generate Markdown draft** — Based on all confirmed adjustments.
2. **Final confirmation** — Present complete Markdown to user for review.
   - User confirms → proceed to .docx generation.
   - User requests changes → apply and re-present.
3. **Generate .docx** — Use python-docx to create a styled .docx.
4. **Optional: PDF** — Use pandoc to convert .docx to PDF (if installed).

**Save intermediate Markdown** to `history/YYYY-MM-DD_{company}_{role}.md`. This is a deliverable, not a temp file — required for Phase 4b diff audit.

**Shadow Resume (on-demand)**: If JD language differs from source resume language, offer to generate a parallel translation copy. Only generate if user explicitly requests.

#### Step 4b: Compliance Audit / 地域合规性审计

Based on Target Region from Phase 1, check for regional compliance violations:

```
IF North America:
  ❌ FORBIDDEN: Photo, age, gender, marital status, religion, nationality, salary history
  ⚠️ CAUTION: Home address (city/state only), graduation year

IF UK/Ireland:
  ❌ FORBIDDEN: Photo, age, marital status, gender, NI number

IF DACH:
  ✅ ACCEPTABLE (changing norms): Photo, DOB, marital status
  ❌ FORBIDDEN: Religion, political affiliation

IF East Asia:
  Varies by country — CN (photo optional in tech), JP (photo expected), KR (photo expected), SG (optional)

IF Global/Remote: Default to North America norms (most restrictive)
```

Output: Table with item, status, region rule, and action. 🔴 Critical violations require explicit user acknowledgment.

#### Step 4c: Reverse Audit / 反向审计

**Step 4c-i: Interviewer Persona / 面试官画像**:

Based on JD, construct a senior interviewer persona (role, seniority, industry, region). Infer evaluation priorities by role type:
- Product director → user growth attribution, cross-functional leadership, data-driven decisions
- Tech architect → technical 'why', trade-off decisions
- Finance director → numbers accuracy, risk awareness
- Junior role → learning trajectory, potential, cultural fit

Output: 👤 [Persona summary in 1-2 sentences]

**Step 4c-ii: Persona-Based Review / 画像驱动审视**:

Review the tailored resume through the interviewer's eyes. Flag:

| # | Category | What to check |
|---|----------|---------------|
| 1 | 🤖 AI feel | Overly polished phrasing, buzzword stacking, formulaic structure |
| 2 | 🕳️ Logical gaps | Outcomes without process, unexplained transitions |
| 3 | 📏 Scope inflation | "Led" when actual role was "participated", exaggerated numbers |
| 4 | 🎯 Buzzword defense | Terms candidate can't explain in interview |
| 5 | 🌍 Cultural tone | Humble language for NA, aggressive language for East Asia |

Output table with location, issue, severity (🟡/🔴), and suggestion.

**Step 4c-iii: Interview Readiness / 面试备战**:

For every 🔴 Major issue:

**Mock Questions**: Generate specific, challenging follow-up questions the interviewer might ask.

**STAR Preparation Sheets**: For each significantly modified bullet:
```
📌 "[exact bullet text]"

**S — Situation**: Business context, team/product/period
**T — Task**: Specific problem, goal or KPI
**A — Action**: Tools/methods, YOUR personal contribution
**R — Result**: How measured, baseline, time period

**Follow-up Risk**: "What would you do differently?" / "Biggest challenge?"
```

**Rules**:
- Only generate for 🔴 Major issues
- Questions must be specific, not generic
- Language matches JD language
- This output is SAVED in the audit log

#### Step 4d: Generate Audit Log / 生成审计日志

1. **Diff audit** — Compare source vs tailored:
   ```bash
   python scripts/main.py diff --source-docx <source_resume.docx> --tailored <history/YYYY-MM-DD_company_role.md> --company <company> --role <role> --json
   ```

2. **ATS compatibility check**:
   ```bash
   python scripts/ats_checker.py --resume <tailored_md> --keywords <comma_separated_jd_keywords> --region <target_region> --json
   ```

3. **Compile final audit report** combining:
   - Change summary (from diff_audit.py)
   - Risk classification (from Phase 3 CP4)
   - Compliance audit (from Step 4b)
   - Reverse audit (from Step 4c)
   - ATS check results

4. **Save audit log** alongside the tailored version.

## Output Structure

```
{resume_directory}/
├── resume_source.docx          # User's original — NEVER modify
└── history/
    ├── 2026-04-14_腾讯_产品策划.md           # Tailored Markdown
    ├── 2026-04-14_腾讯_产品策划.docx          # Final deliverable
    ├── 2026-04-14_腾讯_产品策划_audit.md       # Audit log
    └── ...
```

## Error Handling

- If no resume file is found: ask user to provide the path.
- If JD URL fails to fetch: ask user to paste JD text directly.
- If pandoc is not installed: install it before PDF conversion, or output .docx only.
- If python-docx is not installed: install it before .docx generation.
- If pdfplumber is not installed: PDF reader falls back to PyPDF2 or pdftotext. Warn user about potential quality loss. Do NOT abort.
- If JSON validation fails (jd_parser.py): retry once, then degrade to raw text with warning. Do NOT abort.

## Dependencies

- `python-docx` — Read and write .docx files
- `pdfplumber` — Read PDF files (with PyPDF2 and pdftotext as fallbacks)
- `pandoc` — .docx to PDF conversion (optional — can also output .docx directly)
