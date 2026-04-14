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

Does this make sense?
这个合并合理吗？
```

**✅ Question + recommendation / 问题 + 建议**：
```
你想调整保留哪些吗？我的建议是去掉 [X]，因为 [reason]。
Do you want to adjust which ones to keep? I recommend dropping [X] because [reason].

这个合并合理吗？我觉得合并后能突出 [capability]，但如果你觉得分开讲更清晰也可以保留。
Does this merge make sense? I think merging highlights [capability], but keeping them separate is also fine if you prefer clarity.
```

**When recommendations are not appropriate / 不适合给建议的情况**：
- Asking for factual information (dates, numbers, names) / 问事实信息时不需要建议
- The user has multiple equally valid paths / 用户面前多条路都合理时 → 给出每个选项的 tradeoff，而非单一推荐

**Rule**: The user should never feel like they're doing the LLM's job. The LLM should always show its thinking, then ask for confirmation or override.
**原则**：用户不应该觉得在帮 AI 做决策。LLM 应该先展示自己的分析和建议，再请用户确认或否决。

---

## Checkpoint 1: Experience Selection / 经历取舍

**When**: After match report is generated. / 匹配报告生成后。

**What to do**: Present ALL source resume experiences in **reverse chronological order** (most recent first), marked with match relevance. The ONLY allowed operation is INCLUSION or EXCLUSION — never reorder.
按**时间倒序**（最近的在前）列出所有经历，标注 JD 匹配度。唯一允许的操作是**取舍**，绝对不可重排。

**Format**:
```
Based on JD match, here are your experiences in reverse chronological order:
基于 JD 匹配度，以下是你的全部经历（按时间倒序）：

1. ✅ [Experience A] (2024.7-2025.6) — Direct match: [keyword]
   — 直接匹配 JD 要求的 [关键词]
2. ✅ [Experience B] (2023.10-2024.3) — Direct match: [keyword]
   — 直接匹配 JD 要求的 [关键词]
3. ⚠️ [Experience C] (2022.7-2022.10) — Weak relevance, can include or drop
   — 与 JD 关联较弱，可保留可去掉
4. ❌ [Experience D] (2021.9-2022.1) — Weak relevance, suggest dropping
   — 与 JD 关联较弱，建议去掉

Do you want to adjust which ones to keep? Any to add or remove?
你想调整保留哪些吗？有要加的或去掉的吗？
```

**Rules**:
- NEVER change the order of work/internship entries. They MUST stay in reverse chronological order. / 绝对不要改变工作/实习经历的顺序，必须保持时间倒序。
- NEVER silently remove an experience. Always present the proposal and wait for confirmation. / 绝对不要静默删除经历，必须展示方案并等待确认。
- If the user wants to keep a "weak match" experience, accept it — but calculate space budget impact (see Global Hard Rules). / 如果用户想保留弱匹配经历，接受——但计算空间预算影响。
- Personal projects / side projects CAN be ordered by relevance (not strictly chronological). / 个人项目/副业可以按相关性排序。

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

**Persona-Aware Probing / 身份感知追问**：

Adapt probing style based on the role type detected in Phase 1 Step 1c-i.

**IF Campus / Entry-Level / 校招/应届**:
```
JD requires [skill] but it's not in your resume.
JD 要求的 [技能] 在你简历中没体现。
Have you encountered it through:
你是否有以下途径接触过：
- Coursework or thesis project? / 课程作业或毕业设计中涉及过吗？
- Lab research or academic competition? / 实验室科研项目或学科竞赛中有相关经历吗？
- Self-study, personal project, or open-source contribution? / 自学、个人项目或开源贡献中做过相关的吗？
- Internship or part-time role (even if brief)? / 实习或兼职中接触过相关内容吗？（即使时间很短也可以说）

Focus: learning trajectory, project involvement, and growth potential.
侧重：学习曲线、项目参与度和成长潜力。
```

**IF Social / Experienced / 社招/经验**:
```
JD requires [skill] but it's not reflected in your resume.
JD 要求的 [技能] 没在简历中体现。
Think about your previous roles — have you encountered similar scenarios:
回想一下你之前的工作经历，有没有类似场景：
- Business scenarios where you handled this type of logic or problem? / 在业务场景中处理过类似逻辑或问题吗？
- Collaborated with someone who did this (even if you weren't the primary owner)? / 协作完成过（即使不是主要负责人）？
- Side projects, freelance work, or cross-departmental initiatives? / 副业项目、外包或跨部门协作中涉及过吗？
- Tools or processes that are conceptually similar? / 使用过概念上类似的工具或流程吗？

Focus: business impact, role scope, and deliverable ownership.
侧重：业务影响、职责范围和交付物归属。
```

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

**Multilingual Workplace Probing / 多语言办公追问**：

If the JD involves a multilingual workplace (international company, global team, or target region with multiple official languages), probe for cross-language collaboration experience:

```
This role likely involves a multilingual work environment. Beyond your language test scores, do you have experience:
这个岗位很可能涉及多语言工作环境。除了语言成绩，你是否有过以下经历：
- Serving as a language bridge between teams? / 在跨语言团队中担任沟通桥梁？
- Delivering work products (reports, presentations, documentation) in multiple languages? / 用多种语言交付过工作成果（报告、演示、文档）？
- Working with stakeholders across different countries/time zones? / 与不同国家/时区的利益相关者协作？
- Translating or adapting content for different regional audiences? / 为不同地区的受众翻译或适配过内容？

This is especially valuable for roles targeting Singapore, Dubai, Amsterdam, or global companies.
这对于申请新加坡、迪拜、阿姆斯特丹或国际化公司的岗位尤其有价值。
```

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

**⚠️ Anti-Filler Rule / 禁止空泛填充**:

When a bullet lacks a quantified outcome, NEVER fill it with vague descriptors:
当某条 bullet 缺少量化成果时，绝对不要用空泛描述填充：

**❌ FORBIDDEN — Do NOT use these as outcome substitutes / 禁止用作成果替代**:
- "实现智能化" / "achieved intelligent automation"
- "具备完整闭环经验" / "demonstrated end-to-end capability"
- "提升效率" (without specifying how much) / "improved efficiency"
- "获得认可" / "received recognition"
- "显著改善" / "significantly improved"
- Any adjective that cannot be measured or verified / 任何无法度量或验证的形容词

**✅ PRIMARY — Progressive probing for quantification / 首选：逐步追问引导量化**:

Use 2 rounds of narrowing questions to extract measurable evidence. Adapt questions to the specific bullet context.
用 2 轮递进式追问提取可量化证据，根据 bullet 语境调整问题。

```
Round 1 (volume/scope): "这个工作涉及多大的数据量/多少用户/多少业务线？"
Round 2 (comparison): "做之前是什么样的？做之后有什么变化？"

If after 2 rounds the user still cannot provide metrics:
如果追问 2 轮后仍无法提供量化数据 → 进入 FALLBACK
```

**✅ FALLBACK — If no metrics after probing / 追问无果的兜底处理**:
- Keep the original wording as-is / 保留原文措辞
- Or rewrite to remove the empty outcome clause: "主导 AI Agent 方案设计，覆盖需求定义到技术验证全流程"
- Do NOT add vague descriptors as substitutes / 绝对不要用空泛描述替代

**Rule: A vague outcome is WORSE than no outcome. / 规则：空泛的结果比没有结果更差。**

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

**Special Case: Cross-Credential Mapping / 跨证书/考试对齐处理**：

When the user's credential differs from what the JD explicitly names (e.g., JD says "CET-6" but user has IELTS 7.5), do NOT simply replace the credential name. Instead, **retain the original credential and add an equivalence note**:

**❌ Wrong — Silent replacement / 静默替换**:
```
"IELTS 7.5"
(ATS/HR searching for "CET-6" will miss this)
```

**✅ Correct — Retain + Equivalence annotation / 保留原文 + 等价标注**:
```
"IELTS 7.5 (equivalent to CET-6 high score / 达到 CET-6 高分水平)"
```

**Other examples / 其他示例**:
```
"TOEFL 105 (exceeds IELTS 7.0 requirement / 超出 IELTS 7.0 要求)"
"JLPT N1 (demonstrates advanced Japanese proficiency / 具备高级日语能力)"
"CEFR B2 (equivalent to IELTS 5.5-6.5 / 相当于 IELTS 5.5-6.5)"
```

**Rules for cross-credential mapping**:
1. NEVER fabricate a credential the user doesn't have. / 绝对不要编造用户没有的证书。
2. The equivalence annotation should be brief and factual. / 等价标注应简短、基于事实。
3. Place the user's actual credential FIRST, the JD's credential as context. / 用户实际持有的证书放在前面，JD 要求的作为补充说明。
4. If the user's credential is clearly BELOW the JD requirement (e.g., IELTS 5.0 vs JD's CET-6), do NOT add an equivalence note — flag it as a gap instead. / 如果用户证书明显低于 JD 要求，不要加等价标注——标记为缺口。

**Cultural Tone Slider / 文化语调滑块**：

The LLM should adjust the "assertiveness level" of wording suggestions based on the target region detected in Phase 1.

| Target Region / 目标区域 | Tone / 语调 | Verb Preference / 动词偏好 | Example Pattern / 示例风格 |
|---|---|---|---|
| **North America (US/CA)** | Assertive, achievement-first / 自信，成果先行 | Led, Drove, Built, Achieved, Owned | "Drove 40% revenue growth by..." / "主导了 40% 的收入增长..." |
| **UK/Ireland** | Professional, understated / 专业，克制 | Delivered, Managed, Contributed, Supported | "Contributed to a team that achieved..." / "所在团队实现了..." |
| **DACH (DE/AT/CH)** | Thorough, process-focused / 严谨，过程导向 | Developed, Implemented, Optimized, Ensured | "Implemented a process that resulted in..." / "实施了一套流程，带来..." |
| **East Asia (CN/JP/KR)** | Collaborative, team-oriented / 协作，团队导向 | 协同, 推动, 参与, 负责落实 | "协同多部门推动...实现..." / "Coordinated cross-functional efforts to..." |
| **Middle East** | Respectful, authority-aware / 尊重权威 | Managed, Supported, Facilitated, Achieved | Balance between achievement and hierarchy awareness |
| **Nordic** | Humble, impact-focused / 谦逊，重影响 | Contributed, Improved, Enabled, Facilitated | "Enabled the team to improve..." / "帮助团队提升了..." |

**Rules**:
- Default to the target region detected in Phase 1. If not detected, follow the resume's language/culture.
- The slider is advisory, not mandatory. The user's actual experience should dictate the verbs, not the region.
- If the user's resume is in Chinese but the JD is in English (or vice versa), default to the JD's target region norms.

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

---

## Special: Visa & Relocation Narrative / 签证与搬迁叙事

**When**: When `jd_parser.py` detects a `work_authorization` or `citizenship_requirement` in the JD, OR when the user's profile suggests cross-border job seeking.
当脚本检测到 JD 中有工作许可/国籍要求，或用户的背景暗示跨地域求职时。

**Philosophy**: Visa and relocation status should be addressed proactively and strategically, not hidden or awkwardly mentioned. / 签证和搬迁状态应主动、策略性地处理，而不是隐藏或尴尬地提及。

### Strategy A: Already Authorized / 已具备许可

If the user already has the right to work in the target country:
```
Suggested addition to resume (near the top, in contact info or summary section):
建议在简历顶部（联系方式或摘要栏）添加：

"Eligible to work in [Country] without sponsorship"
"具备 [国家] 工作许可，无需雇主担保"

Or more detailed:
或更详细：
"[Visa type] — valid until [date], eligible to work for any employer"
"[签证类型] — 有效期至 [日期]，可自由受雇"
```

### Strategy B: Needs Sponsorship / 需要担保

If the user needs visa sponsorship:
```
Do NOT mention sponsorship needs in the resume itself. Instead:
不要在简历中直接提签证担保需求。建议：

1. In cover letter or application note:
   在求职信或申请备注中：
   "Open to relocation and willing to navigate visa sponsorship for the right opportunity."

2. In resume summary (subtle approach):
   在简历摘要中（含蓄方式）：
   "Globally mobile professional with [X] years of [industry] experience, based in [Current City], open to relocation."
   "具有 [X] 年 [行业] 经验的全球化专业人士，常驻 [当前城市]，对搬迁持开放态度。"

3. Highlight transferable value to justify sponsorship:
   强调迁移价值以证明担保的合理性：
   - Unique cross-market expertise / 独特的跨市场经验
   - Language skills that bridge markets / 连接市场的语言能力
   - Willingness to relocate at own expense / 自费搬迁意愿
```

### Strategy C: Actively Relocating / 正在搬迁

If the user is already planning to move or has recently moved:
```
Suggested phrasing for resume summary:
建议在简历摘要中这样表述：

"Actively relocating to [City/Country], bringing [X] years of global expertise in [field]"
"正在搬迁至 [城市/国家]，拥有 [X] 年 [领域] 的全球化经验"

"Based in [New City] as of [date], with [X] years of experience serving [region] markets"
"[日期] 起常驻 [新城市]，有 [X] 年服务 [地区] 市场的经验"
```

### Rules
- NEVER fabricate work authorization. / 绝对不要编造工作许可状态。
- If the user is uncertain about their visa status, advise them to verify before including it. / 如果用户不确定签证状态，建议先核实再加。
- Visa strategy should be discussed in Phase 3, BEFORE the final resume draft. / 签证策略应在 Phase 3 讨论，在最终草稿之前。
