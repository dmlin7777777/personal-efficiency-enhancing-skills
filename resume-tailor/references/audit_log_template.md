# Audit Log Template

Template for version-tracked resume changes.

## Generated File

```
resume/history/YYYY-MM-DD_{company}_{role}_audit.md
```

## Audit Log Structure

```markdown
# 简历变更审计

- **日期**: YYYY-MM-DD
- **目标岗位**: {company} - {role}
- **JD 来源**: {URL 或 "用户粘贴"}
- **基于版本**: {source_resume_filename}

## 匹配度摘要

| 指标 | 数值 |
|------|------|
| JD 关键词总数 | X |
| 直接匹配 | Y (Z%) |
| 可关联 | A (B%) |
| 缺口 | C (D%) |

## 变更记录

### 新增内容
| 位置 | 原文 | 新增内容 | 来源 |
|------|------|---------|------|
| [经历名称] | — | [新增的 bullet point] | 用户补充 / 优化措辞 |

### 删除内容
| 位置 | 原文 | 原因 |
|------|------|------|
| [经历名称] | [被删除的 bullet point] | 与 JD 关联弱 / 用户确认删除 |

### 修改内容
| 位置 | 原文 | 修改后 | 类型 |
|------|------|--------|------|
| [经历名称] | [原文] | [修改后] | 措辞升级 / 量化补充 / 排序调整 |

### 排序变更
| 经历 | 原排序 | 新排序 | 原因 |
|------|--------|--------|------|
| [经历A] | #3 | #1 | 直接匹配 JD 核心要求 |

## 未覆盖的 JD 要求

- [ ] [关键词1] — 无对应内容，用户确认无相关经历
- [ ] [关键词2] — 用户补充了相关经历（见新增内容）

## 文件清单

| 文件 | 路径 |
|------|------|
| 调整后简历 (Markdown) | `resume/history/YYYY-MM-DD_{company}_{role}.md` |
| 变更审计 | `resume/history/YYYY-MM-DD_{company}_{role}_audit.md` |
| 调整后简历 (PDF) | `resume/history/YYYY-MM-DD_{company}_{role}.pdf` |
```
