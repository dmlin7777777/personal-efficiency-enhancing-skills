---
name: resume-tailor
description: This skill should be used when the user wants to tailor their resume to a specific job description (JD). It analyzes JD keywords, matches against the source resume, provides adjustment suggestions with interactive checkpoints, and generates a tailored resume in PDF format with version audit.
---

# Resume Tailor

Analyze a job description and tailor the source resume to match, with interactive checkpoints for content decisions and full version audit.

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

## Workflow

### Phase 1: Hybrid JD Analysis (Auto)

**Philosophy / 理念**: Script extracts structured "features" (numbers, certifications, dates). LLM extracts semantic meaning (capabilities, priorities). Both outputs cross-validate.

#### Step 1a: Accept JD Input / 接收 JD

1. **Accept JD input** — URL or plain text.
   - If URL: use `web_fetch` to extract job description content.
   - If text: use directly.

#### Step 1b: Script Feature Extraction / 脚本特征提取

Run the script to extract hard requirements:
```
python scripts/jd_parser.py --file <jd_path> --json [--resume <resume_path>]
```

**What the script extracts / 脚本提取内容**:
- Experience years (with flexible prefixes: "at least", "不少于", "minimum")
- Degree requirements (grouped by level: doctoral/master/bachelor/associate)
- Language tests (IELTS, TOEFL, TOEIC, JLPT, TOPIK, CET, CEFR — with scores)
- Certifications (generic pattern: capital acronyms + cert keywords, any industry)
- GPA scores (any scale — LLM handles cross-scale comparison)
- Degree honors (First class, 2:1, 一等)
- Work authorization / citizenship / security clearance
- Date ranges from resume (for LLM to estimate total experience)

**What the script does NOT extract / 脚本不提取**:
- Soft skills, domain knowledge, business capabilities → Step 1c (LLM)
- Industry-specific terminology → Step 1c (LLM)
- Whether a number "meets" a requirement → LLM decides

**Validate JSON output / JSON 校验**:
- Check the output is valid JSON (all required fields present)
- If parse fails: retry once, then degrade to raw text, log warning, do NOT abort

**Position weight signal / 位置权重信号**:
- The script records `position` (character offset) for each extracted requirement
- Requirements appearing in the **first 20%** of the JD are likely **Dealbreakers** (must-have)
- Requirements in the **last 20%** are likely **Nice-to-have**
- Communicate this signal to Step 1c

#### Step 1c: LLM Semantic Extraction / LLM 语义提取

Read the full JD text and the script's JSON output. Extract semantic keywords:

**Step 1c-i: Role Context Detection / 岗位上下文检测** (always run first):

Based on JD signals, detect three contextual dimensions that influence ALL subsequent phases.

```
1. Role Level / 岗位层级:
   Signals: "fresh grad"/"应届"/"intern" → Campus
            "3+ years"/"experienced"/"manager" → Social
            "VP"/"Director"/"总监"/"C-suite" → Executive
   Default: Social if ambiguous

2. Target Region / 目标区域:
   Detect from JD location, company HQ, or language:
   - North America (US/Canada): Achievement-oriented, no PII, 1-2 page resume
   - UK/Ireland: UK CV norms, 2 pages acceptable, references section
   - DACH (DE/AT/CH): Detailed CV, photo sometimes acceptable
   - East Asia (CN/JP/KR/SG): Structured format, photo common in JP/KR
   - Middle East (UAE/SA): International format, nationality sometimes relevant
   - Global/Remote: Default to US norms unless company HQ suggests otherwise

3. Document Type / 文档类型:
   CV (Academic/Research/UK/EU) vs Resume (Industry/US/Canada)
   Signals: "curriculum vitae", "publications", "references", academic institution + "CV"

4. Work Arrangement / 工作安排:
   Detect remote/hybrid/on-site requirements and timezone constraints:
   - "Remote" / "远程" / "Work from anywhere" → Fully remote
   - "Hybrid" / "混合" / "X days on-site" → Hybrid
   - "Must reside in" / "必须位于" + location → Location-restricted
   - "GMT+X" / "UTC+X" / "specific timezone overlap" → Timezone requirement
   - "On-site" / "onsite" / "坐班" / "到岗" → Fully on-site

   If timezone/location constraint detected:
   → Compare against user's current location (ask if not known)
   → If mismatch: flag as ⚠️ Work Context Alert in Phase 3
   → Example: "JD requires GMT+8 residency; your profile suggests [Current Location]. Please confirm your ability to meet this requirement."
```

**How these signals influence downstream / 下游影响**:

| Signal | Phase 1 (Weight) | Phase 2 (Matching) | Phase 3 (Checkpoints) | Phase 5 (Audit) |
|--------|-----------------|-------------------|----------------------|-----------------|
| **Campus** | Education/GPA → High | Accept learning outcomes as matches | CP2: coursework/projects; CP3: allow project metrics | Focus on potential |
| **Social** | Experience/Domain → High | Require business outcomes | CP2: business scenarios; CP3: enforce business metrics | Focus on track record |
| **Executive** | Leadership/Strategy → High | Match C-suite patterns | CP4: executive tone, board-level impact | Board/VP perspective audit |
| **North America** | Leadership/ownership → High | Match "achievement" patterns | CP4: strong action verbs, first-person | No photo, no PII |
| **East Asia** | Team/process → High | Match "contribution" patterns | CP4: balanced tone, team-first language | Regional format norms |
| **CV type** | Publications/research → Core | Include academic categories | CP1: raise academic entries priority | Allow longer format |
| **Resume type** | Industry skills → Core | Industry outcomes priority | CP1: enforce 1-2 page limit | Strict brevity |
| **Remote/Timezone** | Location/timezone → check | Flag if location mismatch | Warn user before proceeding | Note flexibility requirement |

**Output**: Announce detected context: "Detected: Social role, North America target, Resume format." / "检测结果：社招岗位、北美地区、Resume 格式。"

**Step 1c-ii: Keyword Extraction / 关键词提取**:

**Categories / 分类**:
| Category | Description | Weight Signal |
|----------|-------------|---------------|
| Hard Skills | Tools, technologies, platforms, methodologies | 🔴 Core / 🟡 Nice-to-have |
| Soft Skills | Communication, leadership, analytical thinking | 🟡 Nice-to-have |
| Domain Knowledge | Industry terminology, regulatory context, business domain | 🔴 Core / 🟡 |
| Experience Context | Role scope, team size, stakeholder level, business impact | 🔴 Core / 🟡 |

**Weight assignment rules / 权重判定规则**:
1. **Position**: Keywords in the JD title or first paragraph → Core
2. **Frequency**: Mentioned 2+ times → Core; once → likely Nice-to-have
3. **Explicit markers**: "must", "required", "必须", "要求" → Core; "preferred", "nice-to-have", "加分", "优先" → Nice-to-have
4. **Script cross-validation**: If the script flagged a hard requirement gap, ensure the corresponding keyword is marked Core

**Auto-supplement / 自动补充**:
- If the script extracted a hard requirement that LLM missed → auto-add it, tagged "auto-added from script validation"
- If the script found `hard_gaps` → flag them prominently for Phase 3

**Date range handling / 日期范围处理**:
- If the script returned `resume_date_ranges` but `resume_match: false` for years → the LLM MUST calculate total experience span from the date ranges
- Formula: sum of all (end - start) periods; for ongoing entries (is_ongoing: true), use today's date
- Compare calculated total against JD's `jd_number` to determine if the requirement is met

**Output format / 输出格式**:
Present as a table for user review. Example:

| # | Keyword / 关键词 | Category | Weight | Evidence (JD quote) / 证据 | Script Cross-ref |
|---|---|---|---|---|---|
| 1 | Python | Hard Skill | 🔴 Core | "Proficient in Python for data analysis" | — |
| 2 | Cross-functional leadership | Soft Skill | 🟡 Nice-to-have | "Ability to work across teams" | — |
| 3 | 5+ years experience | Experience | 🔴 Core | "Requires at least 5 years" | ⚠️ Gap: resume date ranges suggest ~4y (LLM calculated) |
| 4 | IELTS 7.0 | Experience | 🔴 Core | "IELTS 7.0 or above" | ✅ Match: resume shows IELTS (score TBD) |
| 5 | CPA certification | Hard Skill | 🟡 Nice-to-have | "CPA preferred" | ❌ Gap: not found in resume |

**Language adaptation / 语言适配**:
- Detect JD language (EN/CN/mixed). Extract keywords in the SAME language as the JD.
- If JD is in English, all output columns use English. If Chinese, use Chinese. If mixed, follow the JD's primary language.

**Skill Clustering / 能力簇聚类**:

After extracting all keywords, group them into **capability clusters**. This strengthens implicit matching by providing structural logic rather than vague similarity claims.

```
Clustering rules:
- Group keywords that belong to the same functional capability
- Each cluster needs a clear "cluster label" describing the underlying capability
- Include JD keywords AND their resume equivalents in the same cluster

Output format:
| Cluster / 能力簇 | JD Keywords | Resume Evidence | Match Status |
|---|---|---|---|
| Data Visualization / 数据可视化 | Tableau, Looker, data dashboard | Power BI, Excel charts | 🔄 Implicit (High) |
| Programming / 编程能力 | Python, SQL, R | Python, SQL | ✅ Direct |
| Cloud & DevOps | AWS, Docker, Kubernetes | — | ⚪ Gap |
```

**How clusters strengthen implicit matching / 能力簇如何增强隐性匹配**:

Without clustering: "Resume has Power BI, JD asks for Tableau" → vague implicit match
With clustering: Both are in "Data Visualization" cluster → structured implicit match with clear reasoning

When a cluster shows a partial match (some tools overlap but not all):
- ✅ If cluster is fully covered → treat all keywords in that cluster as Direct match
- 🔄 If cluster is partially covered → treat missing keywords as Implicit (High/Medium based on overlap ratio)
  - Report: "Power BI and Tableau belong to the same data visualization capability cluster. Candidate demonstrates equivalent proficiency via Power BI."
  - Suggest: "Consider adding 'experienced with equivalent BI tools (e.g., Tableau)' or 'proficient in data visualization tools' to make the bridge explicit"
- ⚪ If no keywords in the cluster are covered → Gap

**Cluster naming guidelines**:
- Use functional capability names, NOT tool names: "Data Visualization" not "Tableau cluster"
- If unsure about cluster grouping, place keywords as standalone items (unclustered)
- Maximum 3-4 keywords per cluster to avoid over-generalization
```

### Phase 2: Semantic Match Analysis (Auto)

**Philosophy / 理念**: Go beyond literal keyword matching. Use semantic understanding to identify implicit matches, while grading confidence to prevent over-interpretation.

#### Step 2a: Read Resume with Structure Awareness / 结构感知读取

If the source resume is .docx, use the structured reader from `diff_audit.py` to extract content with style metadata:
```
python scripts/diff_audit.py --read-structured <resume_path>
```

This returns content with `style` information (Heading, ListBullet, TableCell, Normal, Header, etc.), plus a structure summary (`source_structure`).

**Structure Fallback / 结构降级兜底**:

Check `source_structure` style distribution. If `Normal` style accounts for > 80% of total paragraphs, the document lacks reliable style markup (e.g., PDF conversion loss, unstyled .docx, or .txt input).

In this case, launch **LLM Semantic Structure Recovery**:
```
Structure Recovery Prompt:
"The following resume text was read without reliable style information
(all paragraphs returned as 'Normal' style). Re-segment the content into
logical resume sections.

Input text:
[paste full resume text]

Output a JSON structure:
{
  \"sections\": [
    {
      \"title\": \"section name (e.g., Education, Experience, Skills)\",
      \"content\": \"full text of this section\",
      \"entry_count\": 3
    }
  ],
  \"confidence\": \"high | medium | low\"
}

Rules:
- Preserve ALL original text — do not summarize or omit content
- Infer section boundaries from context (dates, role titles, skill clusters, section headers)
- If the resume uses non-standard section names, map them to conventional ones
- If structure is ambiguous, set confidence to 'low' and note assumptions"
```

- Replace `source_structure` with the LLM-recovered section structure for all downstream phases
- If `confidence` is `"low"`, log in audit: `"⚠️ Structure recovery confidence: low — manual section review recommended"`
- If `Normal` ≤ 80%: skip recovery, use the original structure data directly

**Inject structure context into matching / 注入结构上下文**:
- Skills listed in `ListBullet` or `TableCell` style → higher match weight
- Content in `Header`/`Footer` style → likely metadata (name, contact) → exclude from keyword matching
- Content in `Heading 1` style → section headers → useful for understanding context but not for direct matching

**Format Risk Detection / 格式风险检测**:

After reading the structured resume, assess whether the format is ATS-compatible:

```
Format Risk Indicators / 格式风险信号:
- High proportion of "Normal" style paragraphs with no section headings → likely a plain text paste, low risk
- Multiple "TableCell" entries (especially many short cells) → likely a table-heavy layout → ⚠️ ATS risk
- Content appears significantly shorter than expected for a typical resume → may indicate failed parsing (e.g., from a graphic-heavy PDF) → 🔴 High ATS risk
- No clear "Heading 1" or "Heading 2" entries → no section structure → ⚠️ ATS may misparse

If High ATS risk detected (especially for North America or UK targets):
  "⚠️ Format Risk Warning / 格式风险提示:
   Your resume format may cause ATS parsing failures, particularly in North America.
   你的简历格式可能导致 ATS 解析失败，尤其是在北美地区。

   Detection reason: [specific signal, e.g., 'table-heavy layout detected' or 'content appears fragmented — possibly from a graphic PDF']

   Recommendation / 建议:
   - Convert to a single-column Markdown or .docx structure / 转为单栏 Markdown 或 .docx 结构
   - Avoid tables for skill lists — use bullet points instead / 技能清单不要用表格，改用列表
   - Avoid images, icons, and multi-column layouts / 避免图片、图标和多栏布局
   - If the source is a Canva/graphic PDF, consider recreating it as a plain .docx / 如果源文件是 Canva/图形化 PDF，建议重建为纯 .docx"

**Portfolio & External Links Check / 作品集与外部链接检查**:

For certain role types, external portfolios or profiles are strong signals. The script layer (`jd_parser.py`) automatically scans the resume for URLs and detects role type from the JD. Check the `portfolio` field in the script's JSON output:

```
summary.portfolio = {
  role_types_detected: ["software_engineering"],
  links_found: [{type: "linkedin", url: "..."}],
  missing_critical: true,
  missing_links: [
    {role: "software_engineering", role_label: "Software Engineering", missing_link_type: "github"}
  ]
}
```

**Script-detected role types and expected links / 脚本检测的角色类型与期望链接**:

| Role Type / 角色类型 | Expected Links / 期望链接 |
|---|---|
| Software Engineering / 软件工程 | GitHub, GitLab |
| Design / 设计 | Behance, Dribbble, Figma |
| Data Science & Analytics / 数据科学 | GitHub, Kaggle, Tableau Public |
| Academic / Research / 学术研究 | Google Scholar, ORCID |
| Product Management / 产品管理 | Medium, Personal Site |

| Role Type | Expected Links | Missing Link Action |
|---|---|---|
| Software Engineering / 前后端开发 | GitHub, GitLab, personal site | 🟡 Caution: "No GitHub profile found. For engineering roles, a GitHub link demonstrating code quality is strongly recommended." |
| UX/UI Design / 设计 | Behance, Dribbble, Figma portfolio | 🟡 Caution: "No design portfolio link found. For design roles, a Behance/Dribbble link showcasing visual work is expected." |
| Data Science / Analytics / 数据分析 | GitHub (notebooks), Kaggle, Tableau Public | 🟡 Caution: "No data portfolio found. Consider adding a Kaggle profile or GitHub notebooks to demonstrate analytical skills." |
| Academic / Research / 学术研究 | Google Scholar, ORCID, ResearchGate | 🟡 Caution: "No academic profile found. For research roles, a Google Scholar or ORCID link is recommended." |
| Product Management / 产品管理 | Personal blog, Medium, case study portfolio | 💡 Optional: "Consider adding a blog or case study portfolio to demonstrate product thinking." |
| Marketing / Content / 市场营销 | LinkedIn publications, Medium, campaign portfolio | 💡 Optional: "Consider adding published work or campaign case studies." |

**How to detect / 检测方式**:
- Search resume text for URL patterns containing: github.com, behance.net, dribbble.com, kaggle.com, scholar.google.com, linkedin.com/in/, medium.com, figma.com
- If the resume is a .docx with hyperlinks, check for clickable URLs in the document

**Rules**:
- Only flag if the role type clearly maps to the link category. / 仅在岗位类型明确对应时提示。
- This is a 🟡 Caution (not 🔴 Critical) — the absence of a link doesn't block tailoring. / 这是建议项，不阻断流程。
- If the user confirms they don't have a portfolio, suggest creating one before applying. / 用户确认没有作品集时，建议申请前准备。
```

#### Step 2b: Semantic Matching / 语义匹配

Compare Phase 1 keyword table against the resume content (with structure context).

**Match levels / 匹配等级**:

| Level | Definition / 定义 | Default Confidence |
|-------|------------------|--------------------|
| ✅ Direct | Keyword appears verbatim in resume / 关键词在简历中字面出现 | High |
| 🔄 Implicit | Different wording, same underlying capability / 措辞不同但语义等价 | High / Medium / Low (LLM decides) |
| ⚪ Gap | No related content found in resume / 简历中完全没有相关内容 | — |

**Implicit match rules / 隐性匹配规则**:
- MUST provide "Match Reason" column explaining WHY the LLM believes they are equivalent
- MUST assign a confidence level: **High** (clearly equivalent), **Medium** (likely but debatable), **Low** (stretch interpretation)
- For **Low confidence** implicit matches: flag them separately for Checkpoint 4 user verification
- **Anti-hallucination**: Do NOT claim an implicit match just to inflate the score. If unsure, mark as Gap.

**Equivalence & Proxy Matching / 等价与替代匹配**:

When matching requirements involving certifications, tests, or credentials, the LLM MUST consider cross-credential equivalence:

| Scenario / 场景 | Rule / 规则 | Example |
|---|---|---|
| JD asks for lower-level test, resume has higher-level equivalent | ✅ Implicit (High) — clearly exceeds requirement | JD: CET-6 / Resume: IELTS 7.5 → "IELTS 7.5 exceeds CET-6 proficiency level" |
| JD asks for test A, resume has equivalent test B (same level) | 🔄 Implicit (High/Med) — depends on score comparison | JD: TOEFL 100 / Resume: IELTS 7.0 → "IELTS 7.0 ≈ TOEFL 95-100 range (Medium)" |
| JD asks for test A, resume has lower-level test B | ⚪ Gap or 🔄 Implicit (Low) | JD: IELTS 7.0 / Resume: CET-4 → Gap — CET-4 is below IELTS 7.0 equivalent |
| Both have the same test but different scores | Compare numerically; flag if resume score < JD score | JD: IELTS 7.0 / Resume: IELTS 6.5 → Gap — score below threshold |

**Cross-test mapping reference / 跨考试映射参考** (LLM should use its training knowledge, not a hardcoded table):
- IELTS 7.0 ≈ TOEFL 95-100 ≈ CET-6 550+
- IELTS 6.5 ≈ TOEFL 85-90 ≈ CET-6 500+
- CEFR B2 ≈ IELTS 5.5-6.5 ≈ TOEFL 72-94
- JLPT N1 ≈ CEFR B2-C1
- TOPIK Level 5 ≈ CEFR B2

⚠️ These are approximate equivalents. The LLM should use them as guidance but mark as Implicit (Medium) when crossing test types, never as Direct.

**Cultural Translation of Soft Skills / 软技能跨文化翻译**:

When detecting implicit matches for soft skills, the LLM should account for cultural expression differences. The same capability is often described with completely different vocabulary across cultures.

| Source Culture Expression / 源文化表达 | Target Culture Expression / 目标文化表达 | Match Type |
|---|---|---|
| "抗压能力强" (CN) | "Thrives in fast-paced environments" / "Resilience under pressure" (US) | 🔄 Implicit (High) |
| "吃苦耐劳" (CN) | "Strong work ethic, demonstrated commitment to deliverables" (US) | 🔄 Implicit (Med) |
| "善于沟通" (CN) | "Cross-functional stakeholder management" (US) / "Effective communicator across teams" (UK) | 🔄 Implicit (High) |
| "团队合作精神" (CN) | "Collaborative team player with proven ability to align diverse stakeholders" (US) | 🔄 Implicit (High) |
| "虚心学习" (CN) | "Growth mindset, continuously seeking feedback and professional development" (US) | 🔄 Implicit (Med) |
| "责任心强" (CN) | "Strong sense of ownership, accountable for end-to-end delivery" (US) | 🔄 Implicit (High) |

**Rules / 规则**:
- Do NOT translate word-for-word. Translate the **underlying capability** into the target region's workplace idiom.
- The LLM should use its training knowledge of cultural workplace norms, not a hardcoded mapping table.
- When the target region is detected as North America, lean toward **assertive, achievement-oriented** language.
- When the target region is East Asia or Europe, lean toward **collaborative, process-oriented** language.
- These translations should be offered as **suggestions in Checkpoint 4 (Wording Upgrade)**, not auto-applied.

**Match Score calculation / 匹配评分**:
```
Match Score = (Direct×1.0 + Implicit_High×0.8 + Implicit_Med×0.5 + Implicit_Low×0.2 + Gap×0) / Total × 100%
```
- Low confidence implicit matches are included in the score formula but flagged for user review
- If the user rejects a Low confidence match in Checkpoint 4 → recalculate as Gap (0)

**Output format / 输出格式**:
```
## Match Analysis / 匹配度分析

### Summary / 概览
Match Score: XX%  (Direct: X | Implicit High: X | Implicit Med: X | Implicit Low: X | Gap: X)

### ✅ Direct Matches (X)
| JD Keyword | Resume Evidence | Section |
|---|---|---|

### 🔄 Implicit Matches (X)
| JD Keyword | Match Reason | Confidence | Resume Evidence |
|---|---|---|---|
| Team management | Resume mentions "coordinated X team members across Y departments" | High | [section] |
| Data-driven thinking | Resume shows analytical process but doesn't name the skill | Medium | [section] |
⚠️ Low confidence matches forwarded to Checkpoint 4 for verification.

### ⚪ Gaps (X)
| JD Keyword | Weight | Notes |
|---|---|---|

### ⚠️ Hard Requirement Alerts (from script)
| Requirement | JD Value | Resume Status | Action |
|---|---|---|---|
| Years | 5+ | ~4y (from date ranges) | LLM to discuss with user |
| Certification | CPA | Not found | May need user input |
```

**Language / 语言**:
- **Output language priority / 输出语言优先级**:
  The tailored resume language is determined by the JD language, NOT the source resume language.
  定制简历的语言由 JD 语言决定，而非源简历语言。

  | JD Language | Source Resume Language | Tailored Resume Language | Action |
  |---|---|---|---|
  | English | English | English | No change / 不变 |
  | English | Chinese | **English** | Translate + culturally adapt / 翻译 + 文化适配 |
  | Chinese | English | **Chinese** | Translate + culturally adapt / 翻译 + 文化适配 |
  | Chinese | Chinese | Chinese | No change / 不变 |

  **Translation rules / 翻译规则**:
  - When translating, apply cultural tone adjustment (see Checkpoint 4) for the target language's workplace norms.
  - Do NOT provide a bilingual resume — choose ONE language based on the JD.
  - Translate company names, role titles, and institutional names accurately. Keep well-known brand names in their original form (e.g., "PwC" not "普华永道" in an English resume, unless the user prefers otherwise).
  - If the user is unsure about translation quality, flag the specific sections for user review.

### Phase 3: Interactive Adjustment (Dynamic Routing)

**Philosophy / 理念**: Not all resumes need the same level of adjustment. High-match resumes skip unnecessary questions. Low-match resumes get an alignment check first.

#### Step 3a: Dynamic Routing / 动态路由

Before entering checkpoints, evaluate the match score and hard requirement gaps to determine the flow.

**Hard Requirement Pre-check / 硬指标前置检查**:
```
if script hard_gaps contain "dealbreaker" items (e.g., work authorization, security clearance):
  → Alert user immediately:
    "⚠️ Hard Requirement Alert: JD requires [X] which was not found in your resume.
     This is typically a non-negotiable requirement. Do you want to continue?
     - If yes: proceed (gap will be flagged in audit log)
     - If no: stop here"
```

**Match Score Routing / 匹配度路由**:

| Score Range | Flow | Rationale |
|---|---|---|
| **≥ 92% + no hard_gaps** | **Fast-Track** (see below) | 简历几乎完美匹配，跳过全部 Checkpoint，直接生成 |
| **≥ 90%** | Skip Checkpoint 2 + 5 → Execute 1 → 3 → 4 (including Low-confidence implicit) → 6 | 简历高度匹配，跳过内容补充和结构调整 |
| **70%–89%** | Full flow: 1 → 2 → 3 → 4 → 5 → 6 | 标准流程 |
| **50%–69%** | Full flow + extended Checkpoint 2 (deeper probing for hidden experience) | 匹配度偏低，需要更多挖掘 |
| **< 50%** | **Alignment Check first** (see below) | 简历方向与 JD 差距大，先确认意向 |

**Fast-Track Mode (≥ 92% + no hard_gaps) / 极速定制模式**:

When the resume is an exceptionally good fit, skip all checkpoints and generate immediately:
```
1. Generate a "Recommended Adjustments" table (not a conversation):
   | # | Suggestion / 建议 | Type / 类型 | Auto-Applied? |
   |---|---|---|---|
   | 1 | Reorder experience: move [Job A] to top / 经历重排 | Reorder | ✅ Yes |
   | 2 | Add "Power BI" to skills section / 技能补充 | Content | ✅ Yes |
   | 3 | Rephrase: "参与" → "contributed to" / 措辞微调 | Wording | ⏳ Review |

2. Generate Markdown draft with auto-applied suggestions already included.
3. Present table + draft in ONE message.
4. User reviews and either:
   - Confirms → proceed directly to Phase 4 (generate .docx/PDF)
   - Requests changes → apply and re-present
   - Switches to Full Mode → enter normal checkpoint flow
```

**Memory Pre-fill / 记忆预填**:

Before executing any checkpoint, check if the user has previously provided relevant information:
```
1. On session start (after resume path is known), look for:
   {resume_dir}/history/user_profile_cache.json

2. Cache schema:
   {
     "version": 2,
     "entries": [
       {
         "checkpoint": "quantification",
         "context": "PwC | data analysis internship",
         "data": {"metric": "50+ audit reports", "detail": "..."},
         "timestamp": "2026-04-13"
       },
       {
         "checkpoint": "content_gap",
         "context": "Python | automation",
         "data": {"experience": "Built RPA tool for reconciliation"},
         "timestamp": "2026-04-12"
       }
     ]
   }

3. When a new JD triggers a checkpoint question that matches a cached entry
   (keyword overlap between JD requirement and cached context):
   → Pre-fill the suggestion: "上次你提到在 PwC 处理了 50+ 份审计报告，
     是否沿用此数据？(Yes / No / Edit)"

4. After each checkpoint answer, save to cache (append, not overwrite).
   Cache is user-specific (tied to resume directory).
```

**Alignment Check (< 50% match) / 方向对齐检查**:
```
"Match Score: [X]%. The resume and JD show significant divergence.
简历与 JD 匹配度较低。

Before proceeding, please clarify / 请先确认：
1. Are you genuinely interested in this role direction? / 你确实想投这个方向的岗位吗？
2. Is there relevant experience not captured in the resume? / 有没有简历里没写的相关经历？
3. Is this JD a reference for a similar role? / 这个 JD 是参考，实际上投的是类似岗位？

Based on your response, I will adjust the tailoring strategy accordingly."
```

#### Step 3b: Execute Checkpoints / 执行介入点

**CRITICAL**: This phase requires interactive dialogue with the user. Follow the checkpoints in `references/interaction_checkpoints.md`.

**Checkpoint execution order / 介入点执行顺序**:

1. **Experience Selection / 经历取舍** — Always execute. Present prioritized list based on match relevance.
2. **Content Gaps / 内容缺口** — Execute unless skipped by routing. For each gap, use scenario-based prompts (see interaction_checkpoints.md Checkpoint 2).
3. **Quantification / 量化补充** — Always execute. LLM identifies role-specific quantification opportunities (see interaction_checkpoints.md Checkpoint 3 — industry-aware).
4. **Wording Upgrade / 措辞升级** — Always execute. Includes **Low-confidence implicit matches** from Phase 2 that need user verification. Risk classification applies (see interaction_checkpoints.md Checkpoint 4).
5. **Experience Merge/Split / 经历合并拆分** — Execute unless skipped by routing. Only when merging genuinely strengthens the narrative.

**For each checkpoint**: present the question clearly, wait for user response, then proceed.

### Phase 4: Generate Tailored Resume (Auto + Final Confirmation)

1. **Generate Markdown draft** — Based on all confirmed adjustments, create the tailored resume in Markdown format.
2. **Final confirmation** — Present the complete Markdown to the user for review.
   - User confirms: proceed to PDF generation.
   - User requests changes: apply changes and re-present.
3. **Generate .docx** — Use python-docx to create a styled .docx based on the confirmed Markdown content.
4. **Convert to PDF** — Use pandoc to convert .docx to PDF, preserving formatting.

**Shadow Resume Option / 影子副本**:

If the JD language differs from the source resume language (e.g., JD is English, resume is Chinese), after generating the target-language tailored draft, offer the user a **shadow copy**:
```
"Your tailored resume is ready in [JD language].
你的定制简历已用 [JD 语言] 生成。

💡 Would you like me to also generate a shadow copy in [source resume language]?
   是否需要生成一份 [源简历语言] 的对照副本？

The shadow copy is an exact parallel translation — same structure, same content —
so you can cross-reference what was changed, especially for technical terminology.
影子副本是完全对应的平行翻译（相同结构、相同内容），
方便你对照查看 AI 修改了什么，特别是专业术语部分。"

If user accepts:
  → Generate a second Markdown file: `{date}_{company}_{role}_shadow.md`
  → Same section structure as the tailored version
  → Direct parallel translation (not culturally adapted — the target version is)
  → Save alongside the tailored version in history/
  → DO NOT submit the shadow copy — it is for user reference only
```

### Phase 5: Version Audit (Auto)

#### Step 5a: Save Tailored Resume

1. **Save tailored Markdown** to a `history/` subdirectory relative to the source resume (e.g., `resume/history/YYYY-MM-DD_{company}_{role}.md`).

#### Step 5b: Compliance Audit / 地域合规性审计

Based on the Target Region detected in Phase 1 Step 1c-i, check the tailored resume for regional compliance violations.

```
IF Target Region = North America (US/Canada):
  ❌ FORBIDDEN — Critical violations (remove before submission):
    - Photo / 头像照片
    - Age / date of birth / 出生日期
    - Gender / sex / 性别
    - Marital status / 婚姻状况
    - Religion / 宗教信仰
    - Nationality (unless EEO self-identification) / 国籍
    - Salary history / 薪资历史
  ⚠️ CAUTION — May trigger bias:
    - Home address (use city/state only) / 详细住址（只写城市/州）
    - Graduation year (age discrimination risk) / 毕业年份（年龄歧视风险）

IF Target Region = UK/Ireland:
  ❌ FORBIDDEN:
    - Photo / 头像照片
    - Age / marital status / gender (Equality Act 2010)
    - National Insurance number / 国民保险号
  ⚠️ OPTIONAL but not recommended:
    - Salary history

IF Target Region = DACH (Germany/Austria/Switzerland):
  ✅ ACCEPTABLE (but changing norms):
    - Photo — common but increasingly optional / 照片常见但正变得越来越可选
    - Date of birth / 出生日期
    - Marital status / 婚姻状况
  ❌ STILL FORBIDDEN:
    - Religion / 宗教信仰
    - Political affiliation / 政治倾向
  ⚠️ NOTE:
    - If applying to an international company based in DACH, lean toward US norms (no photo, no PII)
    - If applying to a traditional local company, DACH norms are expected

IF Target Region = East Asia (CN/JP/KR):
  Photo expectations vary by country:
  - China: Photo increasingly optional in tech/internet companies / 科技互联网公司照片越来越可选
  - Japan: Photo still expected in most cases / 大多数情况下仍期望有照片
  - South Korea: Photo expected, often with specific formatting / 期望有照片，通常有特定格式要求
  - Singapore: Photo optional, align with international norms / 照片可选，遵循国际规范
  - Gender, age: Commonly included / 性别、年龄通常可包含

IF Target Region = Global/Remote or unspecified:
  Default to North America norms (most restrictive) as a safe baseline.
  默认采用北美标准（最严格），作为安全基线。

Output format / 输出格式:
| # | Item | Status | Region Rule | Action |
|---|------|--------|-------------|--------|
| 1 | Photo found in header | 🔴 Critical | US/UK: forbidden | Remove before submission |
| 2 | Date of birth: 1995-03 | 🟡 Caution | US: bias risk | Consider removing |
| 3 | "Fluent in Mandarin" | ✅ OK | All regions | No action |
```

**Rules**:
- This audit runs AFTER the tailored resume is generated but BEFORE final save.
- Critical violations (🔴) MUST be flagged to the user and require explicit acknowledgment before saving.
- If the user decides to keep a flagged item (e.g., they intentionally include a photo for a Japanese JD), add a note to the audit log: "User acknowledged regional norm exception."

#### Step 5c: Sincerity Check (Reverse Audit / 反向审计)

**Step 5c-i — Interviewer Persona Construction / 面试官画像构建**:
```
Based on the target JD, construct a senior interviewer persona:
基于目标 JD，构建一位资深面试官画像：

- Role title: [extract from JD] / 职位：从 JD 提取
- Seniority level: [infer from JD requirements] / 资深程度：从 JD 要求推断
- Industry/domain: [extract from JD] / 行业：从 JD 提取
- Target region norms: [from Phase 1 context] / 目标区域规范：来自 Phase 1

Likely evaluation priorities / 可能的评估重点 (based on role type — LLM infers):
- Finance director → numbers accuracy, risk awareness, regulatory knowledge
- Tech architect → technical 'why', trade-off decisions, system design rationale
- Product director → user growth attribution, cross-functional leadership, data-driven decisions
- Sales VP → revenue breakdown, deal cycle, quota attainment, client retention
- Junior role → learning trajectory, potential, cultural fit
- Academic/Research → publication quality, methodology rigor, research independence

Output: 👤 [Persona summary in 1-2 sentences] / 👤 [画像摘要 1-2 句话]
```

**Step 5c-ii — Persona-Based Review / 画像驱动审视**:
```
Through this persona's eyes, review the tailored resume and flag:

1. 🤖 AI-generated feel / AI 化痕迹
   - Overly polished or formulaic phrasing / 措辞过于精美或公式化
   - Buzzword stacking without substance / 堆砌流行词但缺乏实质
   - Unusually consistent bullet structure across different roles / 不同角色下的 bullet 结构过于一致

2. 🕳️ Logical gaps / 逻辑跳跃
   - Claiming outcomes without showing process / 有结果但缺过程
   - Unexplained career transitions / 未解释的职业转型
   - Timeline inconsistencies / 时间线不一致

3. 📏 Scope inflation / 角色范围夸大
   - "Led" when the actual role was "participated" / 实际是参与但写成了主导
   - Team size or budget claims that seem exaggerated / 团队规模或预算数字似乎夸大
   - Taking credit for team outcomes / 将团队成果归为个人

4. 🎯 Buzzword defense risk / 术语自圆其说风险
   - Technical terms or frameworks the candidate might not explain in an interview / 面试中可能解释不了的技术术语或框架
   - Methodologies named but no evidence of application / 提到方法论但没有应用证据

5. 🌍 Cultural tone mismatch / 文化语调不匹配
   - If targeting North America: overly humble or self-deprecating language / 目标北美但语言过于谦虚
   - If targeting East Asia: overly aggressive or self-promotional language / 目标东亚但语言过于张扬
   - Mixed cultural signals (e.g., US-style claims with CN-style modesty disclaimers) / 混杂的文化信号

Output table:

| # | Location | Issue | Severity | Suggestion |
|---|----------|-------|----------|-----------|
| 1 | [section/bullet] | [description] | 🟡/🔴 | [how to fix] |

Severity:
- 🟡 Minor: Could be tightened but not a dealbreaker / 可以改进但不是致命问题
- 🔴 Major: Would likely trigger follow-up questions or skepticism / 可能引发追问或怀疑
```

**Step 5c-iii — Interview Readiness / 面试准备**:

For every 🔴 Major issue flagged in Step 5c-ii, generate interview preparation materials.

**Part A: Mock Interview Questions / 面试追问预演**:
```
For each 🔴 Major issue:

1. 🤖 AI feel / AI 化痕迹:
   → "能具体讲讲这个项目的选型过程吗？为什么选 A 而不是 B？"

2. 🕳️ Logical gaps / 逻辑跳跃:
   → "你提到实现了 X% 的提升，能 walk me through 你是如何量化这个 baseline 的吗？"

3. 📏 Scope inflation / 角色范围夸大:
   → "请详细描述你主导此项目时遇到的最大资源冲突及解决方法。"

4. 🎯 Buzzword defense / 术语自圆其说:
   → "你说你用了 A/B Testing，能说说 control group 怎么分的、sample size 多少吗？"

5. 🌍 Cultural tone mismatch / 文化语调不匹配:
   → (No mock question — wording issue, not a factual claim)
   → 准备 2-3 个 "we" 开头的协作案例来平衡 "I" 开头的个人成就。
```

**Part B: STAR Preparation Sheet / STAR 方法准备单**:

For each 🔴 Major bullet that was **added or significantly modified** during tailoring, generate a structured STAR guide:
```
| Bullet / 简历措辞 | STAR Guide / STAR 引导 |
|---|---|
| "Led cross-functional team achieving 30% conversion improvement" | See STAR template below |

📌 STAR Preparation: "[exact bullet text from tailored resume]"

**S — Situation / 背景**:
  What was the business context? Which team/product/period?
  当时业务背景？涉及哪个团队/产品/时间段？
  [LLM pre-fills based on resume context, e.g., "Based on your PwC Data Analytics internship..."]

**T — Task / 任务**:
  What specific problem were you solving? What was the goal or KPI?
  具体解决什么问题？目标或 KPI 是什么？

**A — Action / 行动**:
  What tools/methods did you use? What was YOUR personal contribution (vs team)?
  用了什么工具/方法？你个人的具体贡献（区别于团队）？
  [LLM suggests based on JD context: e.g., "JD emphasizes Python and data analysis — consider mentioning specific libraries or frameworks"]

**R — Result / 结果**:
  How was the metric measured? What was the baseline? Time period?
  这个指标怎么测算的？基线是什么？时间跨度？
  ⚠️ Be ready to explain the calculation methodology.

**Follow-up Risk / 追问风险**:
  - "What would you do differently?" / "如果重来一次你会怎么改？"
  - "What was the biggest challenge?" / "最大挑战是什么？"
  - "How did you handle disagreement?" / "遇到分歧怎么处理的？"
```

**Output table** (appended to Step 5c-ii or as separate section):
```
## Interview Readiness / 面试准备

### Mock Questions / 追问预演
| # | Resume Wording | Expected Question | Prep Suggestion |
|---|---|---|---|

### STAR Preparation / STAR 准备单
| # | Bullet Point | S/T (Background) | A (Your Action) | R (Result + Proof) |
|---|---|---|---|---|
```

**Rules**:
- Only generate for 🔴 Major issues — 🟡 Minor issues don't need interview prep
- Questions should be **specific and challenging**, not generic
- The language of the questions should match the JD language (EN JD → EN questions)
- STAR guides should reference actual resume content, not generic templates
- This output is SAVED in the audit log alongside the tailored resume

#### Step 5d: Generate Audit Log

1. **Generate audit log** using `scripts/diff_audit.py` — compare source vs tailored version, output change summary.
2. **Run ATS compatibility check** using `scripts/ats_checker.py`:
   ```
   python scripts/ats_checker.py --resume <tailored_md> \
       --keywords <comma_separated_jd_keywords> \
       --region <target_region> --json
   ```
   - `--region` uses the Target Region from Phase 1 Step 1c-i (north_america / uk_ireland / dach / east_asia / global)
   - `--keywords` passes JD keywords from Phase 2 for coverage checking
   - Checks: format (tables/images/special chars), structure (sections/contact), content (dates/bullets), keyword coverage, regional PII compliance
   - Outputs JSON with per-issue severity (high/medium/low) and actionable suggestions
   - Scoring: 100 - (high×10 + medium×3 + low×1)
3. **Compile final audit report** combining:
   - Change summary (from diff_audit.py)
   - Risk classification (from Phase 3 Checkpoint 4)
   - Compliance audit (from Step 5b)
   - Sincerity check (from Step 5c)
   - ATS check results (from ats_checker.py)
4. **Save audit log** alongside the tailored version.

## Output Structure (Example)

```
{resume_directory}/
├── resume_source.docx          # User's original — NEVER modify
├── resume_产品.pdf              # Existing tailored versions (optional)
└── history/                     # Version-tracked tailored resumes
    ├── 2026-04-13_腾讯_广告产品运营.md
    ├── 2026-04-13_腾讯_广告产品运营_audit.md
    ├── 2026-04-13_腾讯_广告产品运营.pdf
    └── ...
```

## Error Handling

- If no resume file is found: ask user to provide the path.
- If JD URL fails to fetch: ask user to paste JD text directly.
- If pandoc is not installed: install it before PDF conversion.
- If python-docx is not installed: install it before .docx generation.
- **If pdfplumber is not installed**: the PDF reader falls back to PyPDF2 or pdftotext CLI.
  - PyPDF2 may produce lower-quality text (merged lines, missing table content).
  - pdftotext CLI requires system installation.
  - If ALL PDF readers fail, a raw binary fallback is used.
  - **In any fallback case**: warn the user:
    ```
    "⚠️ PDF Reading Fallback / PDF 读取降级:
     pdfplumber is not installed. Your PDF was read using [fallback name].
     This may cause: line order issues, missing table content, or garbled characters.
     你的 PDF 使用了 [降级方式] 读取，可能出现行序错乱、表格内容丢失或乱码。
     Recommendation: pip install pdfplumber for best results.
     建议：安装 pdfplumber 以获得最佳读取效果。"
    ```
  - The script reports which reader was used in its output (field: `pdf_reader_used`)
- **If JSON validation fails** (jd_parser.py output): retry once, then degrade to raw text with warning. Do NOT abort.

## Dependencies

- `python-docx` — Read and write .docx files
- `pdfplumber` — Read PDF files (with PyPDF2 and pdftotext as fallbacks)
- `pandoc` — .docx to PDF conversion (optional — can also output .docx directly)
