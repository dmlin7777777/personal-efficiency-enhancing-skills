# Interaction Checkpoints / 交互介入点指引

Detailed guidance for each interactive checkpoint in Phase 3.
每个交互介入点的详细执行指引。

---

## Checkpoint 1: Experience Selection / 经历取舍

**When**: After match report is generated. / 匹配报告生成后。

**What to do**: Present a prioritized list of all source resume experiences, marked with match relevance.
按 JD 匹配度排列所有经历，标注相关性等级。

**Format**:
```
Based on JD match, suggested experience priority:
基于 JD 匹配度，建议的经历排序：

1. ✅ [Experience A] — Direct match: [keyword]
   — 直接匹配 JD 要求的 [关键词]
2. ✅ [Experience B] — Direct match: [keyword]
   — 直接匹配 JD 要求的 [关键词]
3. 🔄 [Experience C] — Relatable to [keyword] (suggest rephrasing)
   — 可关联到 JD 要求的 [关键词]（建议调整措辞）
4. ⚪ [Experience D] — Weak relevance, suggest demote or remove
   — 与 JD 关联较弱，建议弱化或移除

Do you agree with this order? / 你同意这个排序吗？Any adjustments?
有没有想调整的？
```

**Rules**:
- Never silently remove an experience. Always present the proposal and wait for confirmation. / 绝对不要静默删除经历，必须展示方案并等待确认。
- If the user wants to keep a "weak match" experience, ask why — it may reveal hidden relevance. / 如果用户想保留弱匹配经历，追问原因——可能存在隐性关联。

---

## Checkpoint 2: Content Gaps / 内容缺口

**When**: After experience selection is confirmed, for each gap identified in the match report.
经历取舍确认后，针对匹配报告中的每个缺口。

**What to do**: For each JD requirement with no matching resume content, ask the user if they have relevant experience.
对简历中没有覆盖的 JD 要求，引导用户回忆是否有相关经历。

**Prompt Formula / 提问公式**：
```
[Requirement] is mentioned in the JD but not reflected in your resume.
JD 要求的 [能力/经验] 在简历中没有体现。
Do you have relevant experience? / 你有相关的经历吗？
Hint: [Provide a scenario-based prompt to help recall]
提示方向：[根据 JD 上下文给出一个具体的回忆引导]
```

**Prompt Technique / 提问技巧**：
- Don't ask closed-ended "Have you done X?" questions. Provide **scenario-based prompts** to help recall. / 不要问"你做过 X 吗"这种封闭问题，给一个**场景化的提示**帮助用户回忆。
- Hints should be specific but not leading. / 提示应该足够具体但不暗示答案。

**❌ Weak Prompt / 弱提问**：
```
JD requires project management experience. Have you done project management?
JD 要求项目管理经验，你做过项目管理吗？
```

**✅ Strong Prompt / 强提问**：
```
JD requires project management experience. In your previous roles, have you encountered scenarios like:
JD 要求项目管理经验。你在之前的工作中，有没有过这样的场景：
- Coordinating multiple tasks or team members simultaneously? / 同时协调多个任务或多个团队成员？
- Creating project plans and tracking execution progress? / 制定项目计划并跟进执行进度？
- Handling unexpected issues or resource conflicts? / 处理过项目中的突发问题或资源冲突？
If so, could you briefly describe the situation? / 如果有，可以简单说说当时的具体情况。
```

**Rules**:
- If confirmed, ask for details (what did you do? what was the result? any numbers?). / 如果用户确认有相关经历，追问细节（做了什么？结果如何？有数字吗？）。
- If no, mark as "unaddressed" and move on. Do NOT fabricate content. / 如果用户说没有，标记为"未覆盖"并跳过。绝对不要编造内容。

---

## Checkpoint 3: Quantification / 量化补充

**When**: When reviewing bullets that lack specific metrics or numbers.
审查缺少具体指标或数字的 bullet point 时。

**What to do**: Identify bullets where adding numbers would strengthen the match with JD.
识别哪些 bullet 补充数字后能增强与 JD 的匹配度。

**Core Formula / 核心公式**：
```
Action + Object + Measurable Business Outcome
动作 + 对象 + 可量化的业务成果
```

**❌ Weak — Describes responsibility only, no result / 只有职责，没有结果**：
```
"Responsible for daily system maintenance" / "负责数据系统的日常运维"
"Assisted team with data analysis" / "协助团队完成数据分析工作"
"Participated in new feature launch" / "参与了新功能的上线"
"Handled client communication" / "负责客户沟通"
```

**✅ Strong — Has action, object, and business outcome / 有动作、有对象、有业务成果**：
```
"Built a customer churn prediction model, improving prediction accuracy from 65% to 89%"
"搭建客户流失预警模型，将流失预测准确率从 65% 提升至 89%"

"Streamlined the procurement approval process, reducing average cycle time from 5 days to 1 day"
"优化采购审批流程，将平均审批周期从 5 天缩短至 1 天"

"Led end-to-end launch of a new product, acquiring 10,000+ registered users in the first month"
"主导新产品从 0 到 1 上线，首月获取 10,000+ 注册用户"

"Managed key client relationships, maintaining a 95%+ renewal rate, contributing 40% of annual revenue"
"维护关键客户关系，续约率保持在 95% 以上，贡献年度收入的 40%"
```

**Guidance Prompt Format / 引导提问格式**：
```
The following bullet would benefit from quantification:
以下 bullet 建议补充量化数据：

Original: "[current text]" / 原文："[当前文案]"

Suggestion: This describes your responsibility but lacks results. Do you recall:
建议方向：这句话描述了你的职责，但缺少结果。你还记得：
- How many people or business units were affected? / 这个工作影响了多少人/多少业务量？
- What changed in efficiency, accuracy, or revenue after? / 做完之后，效率/准确率/收入等指标有什么变化？
- By how much did it improve compared to before? / 和做之前相比，改善了多少？

Approximate numbers are fine. / 你可以给个大概数字也行。
```

**Rules**:
- Only suggest quantification for bullets being kept. / 只对保留的 bullet 建议量化。
- If the user doesn't remember exact numbers, suggest approximate ranges. / 如果记不清确切数字，建议用大概范围。
- Never invent numbers. If none available, leave as-is. / 绝对不要编造数字。如果无法提供，保持原样。

---

## Checkpoint 4: Wording Upgrade / 措辞升级

**When**: After content is finalized, before generating the draft.
内容确认后、生成草稿前。

**What to do**: Present proposed wording changes with before/after comparison.
以 before/after 对比的形式展示建议的措辞调整。

**Core Formula / 核心公式**：
```
Weak verb → Strong verb + Business impact
弱动词 → 强动词 + 业务影响
```

**Common Weak → Strong Verb Patterns / 常见弱动词 → 强动词对照**：

| Weak Verb / 弱动词 | Issue / 问题 | Upgrade Direction / 升级方向 |
|---|---|---|
| Participated / 参与 | Vague role / 模糊角色 | → Led / Drove / Owned（需确认实际角色 / confirm actual role） |
| Assisted / 协助 | Marginalized / 边缘化 | → Independently completed / As core member / 独立完成 / 作为核心成员 |
| Used / 使用 | Describes tool only / 只描述工具 | → Built / Designed / Architected / 搭建 / 设计 / 从零构建 |
| Responsible for / 负责 | No result / 缺乏结果 | → Led [specific object], achieving [outcome] / 负责 [具体对象]，实现 [业务成果] |
| Familiar with / 了解 | Unverifiable / 无法证明能力 | → Proficient in / X years hands-on experience / 熟练掌握 / 有 X 年实战经验 |

**❌ Weak Upgrade — Changed verb only, no business outcome / 只换了动词，没有业务成果**：
```
"Participated in data analysis project" → "Led data analysis project"
"参与了数据分析项目" → "主导了数据分析项目"
```

**✅ Strong Upgrade — Verb upgrade + business outcome / 动词升级 + 补充业务成果**：
```
"Participated in user behavior analysis" → "Independently completed user behavior analysis, delivered strategy recommendations, drove 15% conversion rate improvement"
"参与用户行为分析" → "独立完成用户行为分析，输出策略建议，推动转化率提升 15%"
```

**⚠️ Safety Rule — Every upgrade must be confirmed by user / 每个升级都必须向用户确认**：

```
Proposed wording changes:
建议的措辞调整：

1. "[original]" → "[revised]"
   "[原文]" → "[改后]"
   Reason: [why this change] / 理由：[为什么这样改]
   ⚠️ Confirm: [any role/outcome claim must be verified] / 确认：[涉及角色/成果的地方，必须让用户确认真实性]

2. "[original]" → "[revised]"
   Reason: [why this change]
   Confirm: Is this accurate? / 确认：这个调整准确吗？

Please review each item. Let me know if anything is inaccurate.
请逐条确认，有任何不准确的地方告诉我。
```

**Rules**:
- Always flag potential over-claims with ⚠️. / 始终用 ⚠️ 标记可能过度包装的改动。
- Present all changes at once for batch confirmation. / 所有改动一次性展示，批量确认。
- If the user rejects a change, revert immediately. / 用户拒绝则立即回退，不要追问。

---

## Checkpoint 5: Experience Merge/Split / 经历合并/拆分

**When**: When multiple short experiences could be combined, or one long experience should be split.
当多段短经历可以合并，或一段长经历需要拆分时。

**Merge Formula / 合并公式**：
```
[Core contribution of A] + [Core contribution of B] = One stronger, more complete bullet
[经历A的核心贡献] + [经历B的核心贡献] = 一条更强、更完整的 bullet
```

**When to Merge / 什么时候建议合并**：
- Multiple experiences reflect different facets of the same capability (technical + business / execution + management). / 多段经历体现了同一种能力的不同侧面（技术 + 业务 / 执行 + 管理）。
- Single experience is too thin to stand alone. / 单条经历太短，单独放显得单薄。
- Combined, they form a complete "identify → solve" narrative. / 合并后能形成"从发现到解决"的完整故事。

**When to Split / 什么时候建议拆分**：
- One experience contains two distinct value props serving different JD requirements. / 一条经历包含两个差异很大的价值点，分别匹配 JD 的不同要求。
- Splitting allows emphasizing different keywords separately. / 拆分后能分别强调不同的关键词。

**❌ Weak Merge — Addition without value-add / 做了加法但没有增值**：
```
"Worked on Project A, also worked on Project B"
"做过 A 项目，也做过 B 项目"
```

**✅ Strong Merge — Extract commonality, highlight综合能力 / 提炼共性，突出综合能力**：
```
"Combined data analysis expertise with technical execution — identified core issues through quantitative analysis, then drove systematic solution delivery, ultimately achieving [business outcome]"
"结合数据分析与技术落地能力，先通过定量分析识别核心问题，再主导系统化方案落地，最终实现 [业务成果]"
```

**Prompt Format / 提问格式**：
```
Found mergeable experiences:
发现可以合并的经历：

[A] and [B] both demonstrate [capability]. Suggest merging:
[A经历] 和 [B经历] 都体现了 [某方面能力]，建议合并：

Merged: "[merged text]" / 合并后："[合并文案]"

Does this make sense? Or would you prefer to keep them separate?
你觉得这样合并合理吗？还是更想分开讲？
```

**Rules**:
- Only propose merges when it genuinely strengthens the narrative. / 只在确实能强化叙事时才建议合并。
- If the user prefers to keep them separate, respect that. / 用户想分开就分开，不要强推。

---

## Checkpoint 6: Final Confirmation / 最终确认

**When**: After Markdown draft is generated. / Markdown 草稿生成后。

**What to do**: Present the complete tailored resume and ask for final approval.
展示完整的调整后简历，请用户做最终确认。

**Format**:
```
Resume tailoring complete. Please review:
简历调整完成，请 review：

[Full Markdown content / 完整 Markdown 内容]

Once confirmed, I will generate the PDF. Let me know if any changes are needed.
确认无误后我将生成 PDF。有任何需要修改的地方请告诉我。
```

**Rules**:
- This is the last checkpoint. After confirmation, proceed directly to PDF generation. / 这是最后一个介入点。确认后直接生成 PDF。
- If the user requests changes, re-present the full draft (not just changed parts). / 用户要求修改后，重新展示完整草稿（不只是改动部分）。
