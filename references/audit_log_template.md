# Audit Log Template / 审计日志模板

Template for version-tracked resume changes.
简历变更版本的追踪模板。

## Generated File / 生成文件

```
resume/history/YYYY-MM-DD_{company}_{role}_audit.md
```

## Audit Log Structure / 审计日志结构

```markdown
# Resume Change Audit / 简历变更审计

- **Date / 日期**: YYYY-MM-DD
- **Target / 目标岗位**: {company} - {role}
- **JD Source / JD 来源**: {URL or "Pasted by user / 用户粘贴"}
- **Based on / 基于版本**: {source_resume_filename}
- **Detected Context / 检测上下文**:
  - Role Level / 岗位层级: Campus / Social / Executive
  - Target Region / 目标区域: {region}
  - Document Type / 文档类型: Resume / CV
  - Work Arrangement / 工作安排: On-site / Hybrid / Remote
- **Match Score / 匹配度**: XX%
- **Structure Recovery / 结构恢复**: Used original / LLM recovered (confidence: high/medium/low)

## Match Summary / 匹配度摘要

| Metric / 指标 | Value / 数值 |
|------|------|
| JD Keywords / JD 关键词总数 | X |
| Direct Match / 直接匹配 | Y (Z%) |
| Implicit High / 隐性高置信 | A (B%) |
| Implicit Medium / 隐性中置信 | C (D%) |
| Implicit Low / 隐性低置信 | E (F%) |
| Gap / 缺口 | G (H%) |

### Skill Clusters / 能力簇匹配

| Cluster / 簇名 | JD Keywords / JD 关键词 | Resume Coverage / 简历覆盖 | Status / 状态 |
|------|------|------|------|
| Data Visualization | Tableau, Power BI | Power BI ✅ | Partial — consider adding equivalent note |
| Data Engineering | Spark, HDFS, Airflow | Spark, HDFS ✅ | Full |

### Cross-Credential Equivalence / 跨证书等价匹配

| JD Requirement / JD 要求 | Resume Credential / 简历证书 | Equivalence / 等价判定 |
|------|------|------|
| IELTS 7.0 | CET-6 550 | Implicit (Med) — CET-6 550+ ≈ IELTS 7.0 range |

## Change Record / 变更记录

### Added Content / 新增内容

| Section / 位置 | Original / 原文 | Added / 新增内容 | Source / 来源 |
|------|------|---------|------|
| [Experience name] | — | [New bullet point] | User provided / 用户补充 |

### Removed Content / 删除内容

| Section / 位置 | Content / 内容 | Reason / 原因 |
|------|------|------|
| [Experience name] | [Deleted bullet point] | Low relevance / 与 JD 关联弱 |

### Modified Content / 修改内容

| Section / 位置 | Before / 修改前 | After / 修改后 | Type / 类型 | Risk / 风险 |
|------|------|--------|------|------|
| [Experience name] | [Before] | [After] | Wording upgrade / Quantification / Reorder | 🟡 Medium / 🔴 High |

### Reorder Changes / 排序变更

| Experience / 经历 | Before / 原排序 | After / 新排序 | Reason / 原因 |
|------|--------|--------|------|
| [Experience A] | #3 | #1 | Directly matches core JD requirement |

## Sincerity Check / 真诚度检测

> Persona: {interviewer persona summary}
> 👤 {senior interviewer role title} at {company}

### AI Feel & Buzzword Defense / AI 痕迹与术语堆砌

| # | Location / 位置 | Issue / 问题 | Severity / 严重 | Suggestion / 建议 |
|------|------|------|------|------|
| 1 | [section/bullet] | Overly polished phrasing / 措辞过于精美 | 🟡 Minor | [fix suggestion] |
| 2 | [section/bullet] | Buzzword without evidence / 术语缺证据 | 🔴 Major | [fix suggestion] |

### Logical Gaps & Scope / 逻辑跳跃与范围夸大

| # | Location / 位置 | Issue / 问题 | Severity / 严重 | Suggestion / 建议 |
|------|------|------|------|------|
| 1 | [section/bullet] | "Led" but role was "participated" / 实际参与但写主导 | 🔴 Major | [fix suggestion] |

### Cultural Tone / 文化语调

| # | Location / 位置 | Issue / 问题 | Severity / 严重 | Suggestion / 建议 |
|------|------|------|------|------|
| 1 | [section] | Too humble for NA target / 目标北美但过于谦虚 | 🟡 Minor | [fix suggestion] |

## Interview Readiness / 面试准备

> 针对 🔴 Major 级别审计问题生成的面试准备材料。
> Generated for 🔴 Major issues to help you prepare before the interview.

### Mock Questions / 追问预演

| # | Resume Wording / 简历措辞 | Expected Interview Question / 预期追问 | Prep Suggestion / 准备建议 |
|------|------|------|------|
| 1 | "Led cross-functional team of 15" | "Could you walk me through the biggest resource conflict you faced leading this team and how you resolved it?" | Prepare STAR: Situation → Task → Action → Result |
| 2 | "Architected real-time data pipeline" | "What were the key trade-offs? Why this architecture over alternatives?" | Prepare: 2-3 alternatives, why rejected, measurable outcome |

### STAR Preparation / STAR 方法准备单

> 针对新增或大幅修改的 bullet point，提供结构化面试准备引导。

| # | Bullet / 简历措辞 | S/T (Background) | A (Your Action) | R (Result + Proof) | Follow-up Risk |
|------|------|------|------|------|------|
| 1 | "Led cross-functional team achieving 30% conversion improvement" | Business context? / 当时业务背景？ | Tools + your specific role / 工具 + 个人具体贡献 | How measured? Baseline? / 怎么测算？基线？ | "What would you do differently?" |
| 2 | "Built automated reconciliation tool reducing errors by 60%" | Problem context? / 问题背景？ | Python libraries? Your design? / 哪些 Python 库？你的设计？ | Error rate before vs after? / 改善前后的错误率？ | "Biggest technical challenge?" |

## Shadow Resume / 影子副本

> Only present when source and target languages differ.

| File / 文件 | Language / 语言 | Purpose / 用途 |
|------|------|------|
| `YYYY-MM-DD_{company}_{role}.md` | {target language, e.g., English} | For submission / 用于投递 |
| `YYYY-MM-DD_{company}_{role}_shadow.md` | {source language, e.g., Chinese} | For user reference only / 仅供对照查看 |

Note: The shadow copy is a direct parallel translation (not culturally adapted). DO NOT submit it.
注意：影子副本是直接平行翻译（未经文化适配）。不要提交此文件。

## ATS Compatibility / ATS 兼容性检查

> Checked with ats_checker.py — Region: {region_profile}

| Metric / 指标 | Value / 数值 |
|------|------|
| ATS Score / ATS 评分 | XX/100 |
| Region / 目标地区 | {region} |
| Common ATS Systems / 常见 ATS | {systems list} |

### ATS Issues / ATS 问题

| # | Check / 检查项 | Issue / 问题 | Severity / 严重 | Suggestion / 建议 |
|------|------|------|------|------|
| 1 | tables | Found 1 markdown table / 发现1个表格 | 🔴 High | Convert to bullet list / 转为列表 |
| 2 | pii_photo | Photo detected / 检测到照片 | 🔴 High | Remove for NA target / 北美需移除 |

### Keyword Coverage / 关键词覆盖

| JD Keyword / JD 关键词 | Found in Resume / 简历中找到 | Status / 状态 |
|------|------|------|
| Python | ✅ Yes | Direct |
| Kubernetes | ❌ No | Gap — consider adding if you have relevant experience |

## Compliance Audit / 地域合规性审计

> Target Region: {region}

| # | Item / 项目 | Status / 状态 | Region Rule / 地区规则 | Action / 操作 |
|------|------|------|------|------|
| 1 | Photo in header / 头部照片 | 🔴 Critical | US: forbidden / 美国：禁止 | Remove before submission / 提交前移除 |
| 2 | Date of birth: 1995-03 / 出生日期 | 🟡 Caution | US: bias risk / 美国：歧视风险 | Consider removing / 建议移除 |
| 3 | "Fluent in Mandarin" | ✅ OK | All regions / 所有地区 | No action / 无需操作 |

**User Acknowledgments / 用户确认**:
- [ ] User acknowledged [item] exception: "User decided to keep photo for JP target" / 用户决定保留照片（日本岗位）

## Hard Requirement Alerts / 硬指标预警

| Requirement / 要求 | JD Value / JD 要求 | Resume Status / 简历状态 | Resolution / 处理 |
|------|------|------|------|
| Work Authorization / 工作许可 | Must have US work visa | Not found / 未找到 | User confirmed: H-1B sponsored / 用户确认：H-1B 赞助 |
| Years of Experience / 经验年限 | 5+ | ~4y (from date ranges) / 约4年（按日期计算） | User provided additional internship / 用户补充实习经历 |

## Portfolio & External Links / 作品集与外部链接

| Link Type / 链接类型 | Expected for Role / 岗位期望 | Found / 找到 | Status / 状态 |
|------|------|------|------|
| GitHub | Software Engineering | ❌ Not found | 🟡 Missing — recommended for engineering roles |
| Portfolio | UX/UI Design | ✅ behance.net/xxx | ✅ OK |

## Uncovered JD Requirements / 未覆盖的 JD 要求

- [ ] [Keyword 1] — No matching content, user confirmed no relevant experience / 无对应内容，用户确认无相关经历
- [ ] [Keyword 2] — User provided relevant experience (see added content) / 用户补充了相关经历（见新增内容）

## Structure Recovery Notes / 结构恢复备注

> Only present if LLM structure recovery was triggered.

- Recovery confidence: {high/medium/low}
- Sections recovered: {list}
- If low confidence: "⚠️ Structure recovery confidence: low — manual section review recommended"
  / "⚠️ 结构恢复置信度低 — 建议人工复核章节划分"

## PDF Reader Notes / PDF 读取备注

> Only present if source was a PDF.

- Reader used: pdfplumber / PyPDF2 / pdftotext (CLI)
- If fell back to PyPDF2 or pdftotext: "⚠️ PDF read via {reader}. Table content and complex layouts may not be fully captured. Manual review recommended."
  / "⚠️ 通过 {reader} 读取 PDF。表格内容和复杂布局可能未完全捕获，建议人工复核。"

## File Manifest / 文件清单

| File / 文件 | Path / 路径 |
|------|------|
| Tailored resume (Markdown) / 调整后简历 | `resume/history/YYYY-MM-DD_{company}_{role}.md` |
| Shadow resume (Markdown) / 影子副本 | `resume/history/YYYY-MM-DD_{company}_{role}_shadow.md` *(conditional)* |
| Change audit / 变更审计 | `resume/history/YYYY-MM-DD_{company}_{role}_audit.md` |
| Tailored resume (PDF) / 调整后简历 | `resume/history/YYYY-MM-DD_{company}_{role}.pdf` |
```

## Conditional Sections / 条件章节

Not all sections appear in every audit log. Include only when applicable:

| Section / 章节 | Condition / 出现条件 |
|------|------|
| Skill Clusters / 能力簇 | Always (if LLM extracted clusters) / 始终（如果 LLM 提取了簇） |
| Cross-Credential Equivalence / 跨证书 | When equivalent credentials detected / 检测到等价证书时 |
| Interview Readiness / 面试追问 | When 🔴 Major issues exist in Sincerity Check / 真诚度检测有 🔴 Major 时 |
| ATS Compatibility / ATS 检查 | Always / 始终 |
| Compliance Audit / 合规审计 | Always / 始终 |
| Structure Recovery Notes / 结构恢复 | When LLM structure recovery was triggered / 触发 LLM 结构恢复时 |
| PDF Reader Notes / PDF 读取 | When source was a PDF / 源文件为 PDF 时 |
| Portfolio & Links / 作品集 | When script detected role type + missing links / 脚本检测到角色类型和缺失链接时 |
| User Acknowledgments / 用户确认 | When user overrode a 🔴 Critical compliance finding / 用户覆盖了 🔴 Critical 合规项时 |
| Shadow Resume / 影子副本 | When source and target languages differ / 源语言与目标语言不同时 |
