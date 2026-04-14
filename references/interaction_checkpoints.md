# Interaction Checkpoints / 交互介入点指引

Detailed guidance for each interactive checkpoint in Phase 3.
每个交互介入点的详细执行指引。

---

## Global Interaction Principle / 全局交互原则

**When the LLM needs user input or decisions, NEVER ask an open question alone — ALWAYS pair the question with a concrete recommended option.**
**当需要用户做选择时，绝对不要只抛出问题——必须同时给出具体建议方案。**

**❌ Bare question / 光提问不给建议**：
```
你想调整保留哪些吗？
Do you want to adjust which ones to keep?
```

**✅ Question + recommendation / 问题 + 建议**：
```
你想调整保留哪些吗？我的建议是去掉 [X]，因为 [reason]。
Do you want to adjust which ones to keep? I recommend dropping [X] because [reason].
```

**When recommendations are not appropriate / 不适合给建议的情况**：
- Asking for factual information (dates, numbers, names) / 问事实信息时不需要建议
- The user has multiple equally valid paths → give tradeoffs, not a single recommendation

**Rule**: The user should never feel like they're doing the LLM's job. The LLM should always show its thinking, then ask for confirmation or override.
**原则**：用户不应该觉得在帮 AI 做决策。LLM 应该先展示自己的分析和建议，再请用户确认或否决。

---

## Checkpoint 1: Experience Selection / 经历取舍

**When**: After match report is generated. / 匹配报告生成后。

**What to do**: Present ALL experiences in **reverse chronological order** (most recent first), marked with JD match relevance. The ONLY allowed operation is INCLUSION or EXCLUSION — never reorder. (See SKILL.md Global Hard Rules for the full constraint.)

**Format**:
```
基于 JD 匹配度，以下是你的全部经历（按时间倒序）：

1. ✅ [Experience A] (2024.7-2025.6) — 直接匹配: [keyword]
2. ✅ [Experience B] (2023.10-2024.3) — 直接匹配: [keyword]
3. ⚠️ [Experience C] (2022.7-2022.10) — 与 JD 关联较弱，可保留可去掉
4. ❌ [Experience D] (2021.9-2022.1) — 与 JD 关联较弱，建议去掉

我的建议是保留 1-3，去掉 4，因为 [reason]。你觉得呢？
```

**Rules**:
- NEVER silently remove an experience. Always present the proposal and wait for confirmation. / 绝对不要静默删除经历。
- If the user wants to keep a "weak match" experience, accept it — but calculate space budget impact. / 如果用户想保留弱匹配经历，接受——但计算空间预算影响。

---

## Checkpoint 2: Content Gaps / 内容缺口

**When**: After experience selection is confirmed, for each gap identified in the match report.
经历取舍确认后，针对匹配报告中的每个缺口。

**What to do**: For each JD requirement with no matching resume content, use scenario-based prompts to help the user recall relevant experience.

**Prompt Formula / 提问公式**：
```
JD 要求的 [能力/经验] 在简历中没有体现。你有相关的经历吗？
提示方向：[根据 JD 上下文给出一个具体的回忆引导]

我的判断是这个缺口比较关键，建议补充。你可以回想一下是否有过类似场景：
- [场景 1]
- [场景 2]
- [场景 3]
```

**Prompt Technique / 提问技巧**：
- Don't ask closed-ended "Have you done X?" questions. Provide **scenario-based prompts** to help recall.
- Hints should be specific but not leading.

**Persona-Aware Probing / 身份感知追问**：

**IF Campus / Entry-Level**:
```
JD 要求的 [技能] 在你简历中没体现。你是否有以下途径接触过：
- 课程作业或毕业设计中涉及过吗？
- 实验室科研项目或学科竞赛中有相关经历吗？
- 自学、个人项目或开源贡献中做过相关的吗？
- 实习或兼职中接触过相关内容吗？（即使时间很短也可以说）
```

**IF Social / Experienced**:
```
JD 要求的 [技能] 没在简历中体现。回想一下你之前的工作经历，有没有类似场景：
- 在业务场景中处理过类似逻辑或问题吗？
- 协作完成过（即使不是主要负责人）？
- 副业项目、外包或跨部门协作中涉及过吗？
```

**Rules**:
- If confirmed, ask for details (what did you do? what was the result? any numbers?). / 如果用户确认，追问细节。
- If no, mark as "unaddressed" and move on. Do NOT fabricate content. / 如果用户说没有，标记为"未覆盖"并跳过。

---

## Checkpoint 3: Quantification / 量化补充

**When**: When reviewing bullets that lack specific metrics or numbers.
审查缺少具体指标或数字的 bullet point 时。

**Core Formula / 核心公式**：
```
Action + Object + Measurable Business Outcome
动作 + 对象 + 可量化的业务成果
```

**❌ Weak — Only responsibility, no result**：
```
"负责数据系统的日常运维"
"协助团队完成数据分析工作"
```

**✅ Strong — Action + Object + Measurable outcome**：
```
"搭建客户流失预警模型，将流失预测准确率从 65% 提升至 89%"
"优化采购审批流程，将平均审批周期从 5 天缩短至 1 天"
```

**Guidance Prompt Format**:
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
- Only suggest quantification for bullets being kept. / 只对保留的 bullet 建议量化。
- Never invent numbers. / 绝对不要编造数字。

**⚠️ Anti-Filler Rule / 禁止空泛填充**:

When a bullet lacks a quantified outcome, NEVER fill it with vague descriptors:

**❌ FORBIDDEN**:
- "实现智能化" / "achieved intelligent automation"
- "具备完整闭环经验" / "demonstrated end-to-end capability"
- "提升效率" (without specifying how much)
- "获得认可" / "received recognition"
- "显著改善" / "significantly improved"
- Any adjective that cannot be measured or verified

**✅ PRIMARY — Progressive probing / 首选：逐步追问引导量化**:

Use 2 rounds of narrowing questions to extract measurable evidence:
```
Round 1 (volume/scope): "这个工作涉及多大的数据量/多少用户/多少业务线？"
Round 2 (comparison): "做之前是什么样的？做之后有什么变化？"
```

**✅ FALLBACK — If no metrics after 2 rounds**:
- Keep the original wording as-is / 保留原文措辞
- Or rewrite to remove the empty outcome clause: "主导 AI Agent 方案设计，覆盖需求定义到技术验证全流程"
- Do NOT add vague descriptors as substitutes

**Rule: A vague outcome is WORSE than no outcome. / 空泛的结果比没有结果更差。**

---

## Checkpoint 4: Wording Upgrade / 措辞升级

**When**: After content is finalized, before generating the draft.
内容确认后、生成草稿前。

**Core Formula**:
```
Weak verb → Strong verb + Business impact
弱动词 → 强动词 + 业务影响
```

**Common Weak → Strong Patterns**:

| Weak Verb | Issue | Upgrade |
|---|---|---|
| 参与 | Vague role | → 主导/推动/独立完成（需确认实际角色） |
| 协助 | Marginalized | → 独立完成/作为核心成员 |
| 使用 | Describes tool only | → 搭建/设计/从零构建 |
| 负责 | No result | → 负责[具体对象]，实现[业务成果] |
| 了解 | Unverifiable | → 熟练掌握/X 年实战经验 |

**❌ Weak Upgrade — Verb only, no outcome**:
```
"参与数据分析项目" → "主导数据分析项目"
```

**✅ Strong Upgrade — Verb + outcome**:
```
"参与用户行为分析" → "独立完成用户行为分析，输出策略建议，推动转化率提升 15%"
```

**⚠️ Safety Rule — Every upgrade must be confirmed**:
```
建议的措辞调整：

1. "[原文]" → "[改后]"
   理由：[为什么这样改]
   ⚠️ 确认：[涉及角色/成果的地方需用户确认]

请逐条确认，有任何不准确的地方告诉我。
```

**Rules**:
- Always flag potential over-claims with ⚠️. / 始终标记可能过度包装的改动。
- Present all changes at once for batch confirmation. / 批量展示，批量确认。
- If the user rejects a change, revert immediately. / 用户拒绝则立即回退。

### Special: Cross-Credential Mapping / 跨证书对齐

When user's credential differs from JD requirement, retain original + add equivalence note:
```
"IELTS 7.5 (equivalent to CET-6 high score / 达到 CET-6 高分水平)"
```

Rules:
1. NEVER fabricate a credential. / 绝对不要编造证书。
2. User's actual credential FIRST, JD's as context. / 用户实际持有的在前。
3. If user's credential is clearly BELOW JD requirement → flag as gap, NOT equivalence.

### Special: Cultural Tone Slider / 文化语调滑块

| Target Region | Tone | Verb Preference |
|---|---|---|
| North America | Assertive, achievement-first | Led, Drove, Built, Achieved |
| UK/Ireland | Professional, understated | Delivered, Managed, Contributed |
| DACH | Thorough, process-focused | Developed, Implemented, Optimized |
| East Asia | Collaborative, team-oriented | 协同, 推动, 参与, 负责落实 |
| Middle East | Respectful, authority-aware | Managed, Supported, Facilitated |
| Nordic | Humble, impact-focused | Contributed, Improved, Enabled |

Rules:
- Default to target region detected in Phase 1. The slider is advisory, not mandatory.
- User's actual experience should dictate the verbs, not the region.

---

## Special: Visa & Relocation Narrative / 签证与搬迁叙事

**When**: When script detects work authorization requirements, or user's profile suggests cross-border job seeking.

### Strategy A: Already Authorized
```
建议在简历顶部添加："Eligible to work in [Country] without sponsorship"
或："[签证类型] — 有效期至 [日期]，可自由受雇"
```

### Strategy B: Needs Sponsorship
```
不要在简历中直接提签证担保需求。建议：
1. 在求职信中说明："Open to relocation and willing to navigate visa sponsorship."
2. 在简历摘要中（含蓄）："Globally mobile professional, open to relocation."
3. 强调迁移价值：跨市场经验、多语言能力、自费搬迁意愿。
```

### Strategy C: Actively Relocating
```
"Actively relocating to [City/Country], bringing [X] years of global expertise"
或："[日期] 起常驻 [新城市]，有 [X] 年服务 [地区] 市场的经验"
```

### Rules
- NEVER fabricate work authorization. / 绝对不要编造工作许可状态。
- Visa strategy should be discussed BEFORE the final resume draft.
