# Interaction Checkpoints

Detailed guidance for each interactive checkpoint in Phase 3.

---

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

**提问公式**：
```
JD 要求的 [能力/经验] 在简历中没有体现。你有相关的经历吗？
提示方向：[根据 JD 上下文给出一个具体的回忆引导]
```

**提问技巧**：
- 不要问"你做过 X 吗"这种封闭问题，给一个**场景化的提示**帮助用户回忆
- 提示应该足够具体但不暗示答案

**❌ 弱提问**：
```
JD 要求项目管理经验，你做过项目管理吗？
```

**✅ 强提问**：
```
JD 要求项目管理经验。你在之前的工作中，有没有过这样的场景：
- 同时协调多个任务或多个团队成员？
- 制定项目计划并跟进执行进度？
- 处理过项目中的突发问题或资源冲突？
如果有，可以简单说说当时的具体情况。
```

**Rules**:
- If the user confirms they have relevant experience, ask for details (what did you do? what was the result? any numbers?).
- If the user says no, mark this gap as "unaddressed" and move on. Do NOT fabricate content.

---

## Checkpoint 3: Quantification

**When**: When reviewing bullets that lack specific metrics/numbers.

**What to do**: Identify bullets where adding numbers would strengthen the match with JD.

**核心公式**：
```
动作 + 对象 + 可量化的业务成果
```

**❌ 弱写法 — 只有职责，没有结果**：
```
"负责数据系统的日常运维"
"协助团队完成数据分析工作"
"参与了新功能的上线"
"负责客户沟通"
```

**✅ 强写法 — 有动作、有对象、有业务成果**：
```
"搭建客户流失预警模型，将流失预测准确率从 65% 提升至 89%"
"优化采购审批流程，将平均审批周期从 5 天缩短至 1 天"
"主导新产品从 0 到 1 上线，首月获取 10,000+ 注册用户"
"维护关键客户关系，续约率保持在 95% 以上，贡献年度收入的 40%"
```

**引导提问格式**：
```
以下 bullet 建议补充量化数据：

原文："[当前文案]"

建议方向：这句话描述了你的职责，但缺少结果。你还记得：
- 这个工作影响了多少人/多少业务量？
- 做完之后，效率/准确率/收入等指标有什么变化？
- 和做之前相比，改善了多少？

你可以给个大概数字也行。
```

**Rules**:
- Only suggest quantification for bullets that are being kept in the tailored version.
- If the user doesn't remember exact numbers, suggest using approximate ranges (e.g., "约 X%" or "X+" ).
- Never invent numbers. If the user can't provide any, leave as-is or ask if a qualitative description is acceptable.

---

## Checkpoint 4: Wording Upgrade

**When**: After content is finalized, before generating the draft.

**What to do**: Present proposed wording changes with before/after comparison.

**核心公式**：
```
弱动词 → 强动词 + 业务影响
```

**常见弱动词 → 强动词对照**：

| 弱动词 | 问题 | 升级方向 |
|--------|------|---------|
| 参与 | 模糊角色 | → 主导 / 牵头 / 负责（需确认实际角色） |
| 协助 | 边缘化 | → 独立完成 / 作为核心成员 |
| 使用 | 只描述工具 | → 搭建 / 设计 / 从零构建 |
| 负责 | 缺乏结果 | → 负责 [具体对象]，实现 [业务成果] |
| 了解 | 无法证明能力 | → 熟练掌握 / 有 X 年实战经验 |

**❌ 弱改法 — 只换了动词，没有业务成果**：
```
"参与了数据分析项目" → "主导了数据分析项目"
```

**✅ 强改法 — 动词升级 + 补充业务成果**：
```
"参与用户行为分析" → "独立完成用户行为分析，输出策略建议，推动转化率提升 15%"
```

**⚠️ 安全规则 — 每个升级都必须向用户确认**：

```
建议的措辞调整：

1. "[原文]" → "[改后]"
   理由：[为什么这样改]
   ⚠️ 确认：[涉及角色/成果的地方，必须让用户确认真实性]

2. "[原文]" → "[改后]"
   理由：[为什么这样改]
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

**合并公式**：
```
[经历A的核心贡献] + [经历B的核心贡献] = 一条更强、更完整的 bullet
```

**什么时候建议合并**：
- 多段经历体现了同一种能力的不同侧面（技术 + 业务 / 执行 + 管理）
- 单条经历太短，单独放显得单薄
- 合并后能形成"从发现到解决"的完整故事

**什么时候建议拆分**：
- 一条经历包含两个差异很大的价值点，分别匹配 JD 的不同要求
- 拆分后能分别强调不同的关键词

**❌ 弱合并 — 做了加法但没有增值**：
```
做过 A 项目，也做过 B 项目
```

**✅ 强合并 — 提炼共性，突出综合能力**：
```
"结合数据分析与技术落地能力，先通过定量分析识别核心问题，再主导系统化方案落地，最终实现 [业务成果]"
```

**提问格式**：
```
发现可以合并的经历：

[A经历] 和 [B经历] 都体现了 [某方面能力]，建议合并：

合并后："[合并文案]"

你觉得这样合并合理吗？还是更想分开讲？
```

**Rules**:
- Only propose merges when it genuinely strengthens the narrative.
- If the user prefers to keep them separate, respect that.

---

## Checkpoint 6: Final Confirmation

**When**: After Markdown draft is generated.

**What to do**: Present the complete tailored resume and ask for final approval.

**Format**:
```
简历调整完成，请 review：

[完整 Markdown 内容]

确认无误后我将生成 PDF。有任何需要修改的地方请告诉我。
```

**Rules**:
- This is the last checkpoint. After confirmation, proceed directly to PDF generation.
- If the user requests changes, apply them and re-present the full draft (not just the changed parts).
