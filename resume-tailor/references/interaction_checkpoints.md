# Interaction Checkpoints

Detailed guidance for each interactive checkpoint in Phase 3.

## Checkpoint 1: Experience Selection

**When**: After match report is generated.

**What to do**: Present a prioritized list of all source resume experiences, marked with match relevance.

**Format**:
```
基于 JD 匹配度，建议的经历排序：

1. ✅ [经历A] — 直接匹配 JD 要求的 [关键词]
2. ✅ [经历B] — 直接匹配 JD 要求的 [关键词]
3. 🔄 [经历C] — 可关联到 JD 要求的 [关键词]（建议调整措辞）
4. ⚪ [经历D] — 与 JD 关联较弱，建议弱化或移除

你同意这个排序吗？有没有想调整的？
```

**Rules**:
- Never silently remove an experience. Always present the proposal and wait for confirmation.
- If the user wants to keep a "weak match" experience, ask why — it may reveal hidden relevance.

---

## Checkpoint 2: Content Gaps

**When**: After experience selection is confirmed, for each gap identified in the match report.

**What to do**: For each JD requirement with no matching resume content, ask the user if they have relevant experience.

**Format**:
```
JD 要求的 [能力/经验] 在简历中没有体现。你有相关的经历吗？
比如：[给出一个具体的提示方向]
```

**Rules**:
- Provide a concrete hint to help the user recall (e.g., "比如你之前在做数据分析相关的工作时，有没有做过类似的 X 分析工作？").
- If the user confirms they have relevant experience, ask for details (what did you do? what was the result? any numbers?).
- If the user says no, mark this gap as "unaddressed" and move on. Do NOT fabricate content.

---

## Checkpoint 3: Quantification

**When**: When reviewing bullets that lack specific metrics/numbers.

**What to do**: Identify bullets where adding numbers would strengthen the match with JD.

**Format**:
```
以下 bullet point 建议补充量化数据：

原文："负责系统的日常运维"
建议改为："负责 N 个业务模块的数据系统运维，管理 M 人团队"

你还记得具体数字吗？
```

**Rules**:
- Only suggest quantification for bullets that are being kept in the tailored version.
- If the user doesn't remember exact numbers, suggest using approximate ranges (e.g., "约 X 万元").
- Never invent numbers. If the user can't provide any, leave as-is or ask if a qualitative description is acceptable.

---

## Checkpoint 4: Wording Upgrade

**When**: After content is finalized, before generating the draft.

**What to do**: Present proposed wording changes with before/after comparison.

**Format**:
```
建议的措辞调整：

1. "参与" → "主导"
   原文：参与了某系统的实施项目
   改为：主导了某系统的实施项目
   ⚠️ 确认：你确实是主要负责人吗？

2. "使用" → "独立搭建"
   原文：使用 Python 处理数据
   改为：独立搭建 Python 数据处理流程
   确认：这个调整准确吗？

请逐条确认，有任何不准确的地方告诉我。
```

**Rules**:
- Always flag potential over-claims with ⚠️.
- Present all changes at once for batch confirmation, not one-by-one (efficiency).
- If the user rejects a change, revert and do not push back.

---

## Checkpoint 5: Experience Merge/Split

**When**: When multiple short experiences could be combined into one stronger entry, or one long experience should be split to highlight different aspects.

**Format**:
```
发现可以合并的经历：

[A经历] 和 [B经历] 都体现了 [某方面能力]，建议合并为一个更强的 bullet：

合并后：
"通过 [技术手段] 和 [运营手段] 双轨驱动，实现了 [量化结果]"

你觉得这样合并合理吗？还是更想分开讲？
```

**Rules**:
- Only propose merges when it genuinely strengthens the narrative.
- If the user prefers to keep them separate, respect that.
- For splits: suggest when one experience has two distinct value props that serve different JD requirements.

---

## Checkpoint 6: Final Confirmation

**When**: After Markdown draft is generated.

**What to do**: Present the complete tailored resume and ask for final approval.

**Format**:
```
简历调整完成，请review：

[完整 Markdown 内容]

确认无误后我将生成 PDF。有任何需要修改的地方请告诉我。
```

**Rules**:
- This is the last checkpoint. After confirmation, proceed directly to PDF generation.
- If the user requests changes, apply them and re-present the full draft (not just the changed parts).
