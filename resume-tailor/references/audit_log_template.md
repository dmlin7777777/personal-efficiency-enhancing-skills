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

## Match Summary / 匹配度摘要

| Metric / 指标 | Value / 数值 |
|------|------|
| JD Keywords / JD 关键词总数 | X |
| Direct Match / 直接匹配 | Y (Z%) |
| Related / 可关联 | A (B%) |
| Gap / 缺口 | C (D%) |

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

| Section / 位置 | Before / 修改前 | After / 修改后 | Type / 类型 |
|------|------|--------|------|
| [Experience name] | [Before] | [After] | Wording upgrade / Quantification / Reorder |

### Reorder Changes / 排序变更

| Experience / 经历 | Before / 原排序 | After / 新排序 | Reason / 原因 |
|------|--------|--------|------|
| [Experience A] | #3 | #1 | Directly matches core JD requirement |

## Uncovered JD Requirements / 未覆盖的 JD 要求

- [ ] [Keyword 1] — No matching content, user confirmed no relevant experience / 无对应内容，用户确认无相关经历
- [ ] [Keyword 2] — User provided relevant experience (see added content) / 用户补充了相关经历（见新增内容）

## File Manifest / 文件清单

| File / 文件 | Path / 路径 |
|------|------|
| Tailored resume (Markdown) / 调整后简历 | `resume/history/YYYY-MM-DD_{company}_{role}.md` |
| Change audit / 变更审计 | `resume/history/YYYY-MM-DD_{company}_{role}_audit.md` |
| Tailored resume (PDF) / 调整后简历 | `resume/history/YYYY-MM-DD_{company}_{role}.pdf` |
```
