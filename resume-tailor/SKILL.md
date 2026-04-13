---
name: resume-tailor
description: This skill should be used when the user wants to tailor their resume to a specific job description (JD). It analyzes JD keywords, matches against the master resume, provides adjustment suggestions with interactive checkpoints, and generates a tailored resume in PDF format with version audit.
---

# Resume Tailor

Analyze a job description and tailor the master resume to match, with interactive checkpoints for content decisions and full version audit.

## Trigger Phrases

- "帮我针对这个 JD 调简历" / "tailor resume to this JD"
- "优化简历给这个岗位" / "optimize resume for this role"
- "这份简历匹配这个岗位吗" / "is my resume a good fit"
- Any JD text or URL provided with resume adjustment intent

## Master Resume Location

```
C:\Users\12932\WorkBuddy\Claw\resume\resume_master.docx
```

All tailored versions derive from this file. Never modify the master.

## Workflow

### Phase 1: JD Analysis (Auto)

1. **Accept JD input** — URL or plain text.
   - If URL: use `web_fetch` to extract job description content.
   - If text: use directly.
2. **Extract keywords** — Run `scripts/jd_parser.py` to categorize JD requirements:
   - Hard skills (tools, languages, frameworks)
   - Soft skills (leadership, communication, etc.)
   - Domain knowledge (industry, business area)
   - Experience requirements (years, specific backgrounds)
3. **Output**: Structured keyword list with priority (must-have vs nice-to-have).

### Phase 2: Resume Matching (Auto)

1. **Read master resume** — Extract all content from `resume_master.docx`.
2. **Match analysis** — Compare master resume content against JD keywords:
   - Direct match: skill/experience explicitly mentioned in resume
   - Implicit match: experience demonstrates the skill but not named explicitly
   - Gap: JD requirement with no corresponding resume content
3. **Generate match report** (Markdown):
   ```
   ## 匹配度分析

   ### ✅ 直接匹配 (X/Y)
   - [keyword] → [resume bullet point]

   ### 🔄 可关联 (X/Y)
   - [keyword] → [resume experience that demonstrates it]

   ### ❌ 缺口 (X/Y)
   - [keyword] → 无对应内容
   ```

### Phase 3: Interactive Adjustment (User Input Required)

**CRITICAL**: This phase requires interactive dialogue with the user. Follow the checkpoints in `references/interaction_checkpoints.md`.

For each checkpoint, present the question clearly, wait for user response, then proceed.

**Order of checkpoints**:

1. **Experience Selection** — Which experiences to keep, remove, or reorder based on match report.
2. **Content Gaps** — For each gap identified, ask the user if they have relevant experience not in master.
3. **Quantification** — For bullets lacking numbers, prompt the user to supply metrics.
4. **Wording Upgrade** — Present proposed wording changes (e.g., "参与" → "主导"), confirm with user.
5. **Experience Merge/Split** — If multiple entries can be combined or one should be split, propose and confirm.

### Phase 4: Generate Tailored Resume (Auto + Final Confirmation)

1. **Generate Markdown draft** — Based on all confirmed adjustments, create the tailored resume in Markdown format.
2. **Final confirmation** — Present the complete Markdown to the user for review.
   - User confirms: proceed to PDF generation.
   - User requests changes: apply changes and re-present.
3. **Generate .docx** — Use python-docx to create a styled .docx based on the confirmed Markdown content.
4. **Convert to PDF** — Use pandoc to convert .docx to PDF, preserving formatting.

### Phase 5: Version Audit (Auto)

1. **Save tailored Markdown** to `resume/history/YYYY-MM-DD_{company}_{role}.md`.
2. **Generate audit log** using `scripts/diff_audit.py` — compare master vs tailored version, output change summary.
3. **Save audit log** to `resume/history/YYYY-MM-DD_{company}_{role}_audit.md`.

## Output Structure

```
resume/
├── resume_master.docx          # NEVER modify
├── resume_产品.docx/.pdf       # Existing tailored versions
├── resume_数据.docx/.pdf
└── history/                    # Version-tracked tailored resumes
    ├── 2026-04-13_腾讯_广告产品运营.md
    ├── 2026-04-13_腾讯_广告产品运营_audit.md
    ├── 2026-04-13_腾讯_广告产品运营.pdf
    └── ...
```

## Error Handling

- If `resume_master.docx` is not found: ask user to confirm the path.
- If JD URL fails to fetch: ask user to paste JD text directly.
- If pandoc is not installed: install it before PDF conversion.
- If python-docx is not installed: install it before .docx generation.

## Dependencies

- `python-docx` — Read and write .docx files
- `pandas` — JD keyword parsing (in script)
- `pandoc` — .docx to PDF conversion
