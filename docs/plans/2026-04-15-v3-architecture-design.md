# Resume Tailor v2.5 — 系统架构设计文档

> **日期**: 2026-04-15  
> **状态**: Design Approved, Pending Implementation  
> **范围**: Pseudo Multi-Agent + Blackboard Architecture + HTML Rendering Pipeline

---

## 1. 执行摘要

Resume Tailor v2.5 从"单体 Skill + 顺序执行"升级为**伪多智能体 + 黑板架构**模式。

**核心目标**: 解决单 Agent 在长链路任务中出现的注意力漂移和指令丢失问题（特别是 Phase 4 反向审计被跳过）。

**核心手段**:
- 物理隔离 LLM 调用：Writer 和 Auditor 是两次独立的 API 请求
- 黑板协议：`context_snapshot.json` 作为唯一状态源，替代上下文窗口传递
- HTML 中间层渲染：解决 python-docx 排版质量差的问题

---

## 2. 设计哲学（五大原则）

| # | 原则 | 定义 | 强制性 |
|---|------|------|--------|
| 1 | 教练而非润色器 | 引导用户挖掘真实经历，不编造不包装 | Hard |
| 2 | 事实守恒 | 时间倒序不可重排，只保留或隐藏；禁止空泛填充 | Hard |
| 3 | 物理隔离审计 | Auditor 必须是独立 API 调用，不能与 Writer 共享上下文 | Hard |
| 4 | 最小权限工具箱 | 每个节点默认无工具，按需白名单注入 | Hard |
| 5 | 脚本守门人 | engine.py 负责快照读写、格式校验、回退判定；LLM 只负责语义推理 | Hard |

---

## 3. 系统架构

### 3.1 全景图

```
┌─────────────────────────────────────────────────────┐
│                   engine.py (编排器/守门人)            │
│                                                     │
│  1. 初始化 snapshot.json (脚本填 Layer 1)             │
│  2. 检查 sessions/ 是否有断点 → 恢复或新建             │
│  3. while status != "complete":                      │
│     ├── 读取 snapshot → 组装该阶段上下文               │
│     ├── 注入白名单工具                                │
│     ├── 调用对应专家节点 (Scout/Architect/Auditor)    │
│     ├── 解析 STATE_UPDATE JSON                        │
│     ├── deep_merge 到 snapshot                       │
│     └── 检查回退条件 (🔴 major issues?)               │
│  4. 渲染最终输出 (HTML → PDF/DOCX)                    │
│  5. 归档到 history/                                  │
└─────────────────────────────────────────────────────┘
              │               │                │
         ┌────▼───┐      ┌────▼───┐       ┌────▼───┐
         │ Scout  │      │Architect│      │Auditor │
         │调研员  │      │撰写者   │       │审计员  │
         └────────┘      └────────┘       └────────┘
              ↑               ↑              ↑
         references/     references/     references/
           scout_guide.md writer_guide.md auditor_guide.md
```

### 3.2 专家角色定义

| 角色 | 核心任务 | 白名单工具 | 交互密度 |
|------|---------|-----------|---------|
| **Context Scout** | JD 结构化解析、能力簇提取、市场偏好扫描 | `web_search`, `jd_parser.py` | 低（主要靠脚本+搜索） |
| **Resume Architect** | 经历取舍(CP1)、缺口补全(CP2)、量化补充(CP3)、措辞升级(CP4) | 无（纯对话交互） | 🔥 极高（多轮追问） |
| **Sincerity Auditor** | 反向审计、真诚度检测、面试追问预演、ATS 合规检查 | `ats_checker.py`, `diff_audit.py` | 中（输出为主，偶尔回退触发） |

---

## 4. 状态协议：context_snapshot.json

### 4.1 Schema（三层分离）

```json
{
  "_meta": {
    "schema_version": "1.0",
    "session_id": "20260415_pwc_da",
    "status": "phase_3_adjustment",
    "status_history": ["initialized", "phase_1_context", "phase_2_match", "phase_3_adjustment"],
    "current_node": "architect",
    "rollback_count": 0,
    "last_updated": "2026-04-15T19:18:00Z"
  },
  "jd_facts": {
    "source": "raw_jd_text_or_url",
    "company": "Example Corp",
    "role": "Data Analyst",
    "region": "North America",
    "role_level": "Social",
    "hard_requirements": [
      { "type": "experience", "value": "2+ years", "met": false },
      { "type": "certification", "value": "SQL", "met": true }
    ],
    "soft_requirements": ["Cloud experience preferred"],
    "capability_clusters": ["Data Engineering", "Business Analysis"]
  },
  "resume_facts": {
    "source_file": "resume_master.docx",
    "experiences_raw": ["pwc", "valores", "jiuqi", "didi", "tianzhi", "strowin"],
    "credentials": [{"name": "IELTS", "score": "7.5"}, {"name": "CET-6", "score": "550"}]
  },
  "user_decisions": {
    "kept_experiences": ["pwc", "valores", "jiuqi", "didi"],
    "removed_experiences": ["tianzhi", "strowin"],
    "added_sections": [],
    "confirmed_quantifications": {
      "jiuqi_b3": "Reduced monthly close from 5 days to 6 hours across 12 business lines"
    },
    "confirmed_wording_changes": {},
    "regional_preferences": {}
  },
  "expert_outputs": {
    "scout": {
      "market_research_summary": null,
      "match_score": null,
      "hard_gaps": []
    },
    "writer": {
      "draft_path": null,
      "applied_rules": []
    },
    "auditor": {
      "audit_report_path": null,
      "risk_level": null,
      "major_issues": [],
      "minor_issues": [],
      "mock_questions": [],
      "star_notes": []
    }
  }
}
```

### 4.2 层级规则

| 层 | Key 前缀 | 写入者 | 可覆盖? | 回退时行为 |
|----|---------|--------|---------|-----------|
| Layer 0: Meta | `_meta` | engine.py | 脚本控制 | 记录 rollback_count |
| Layer 1: Facts | `jd_facts`, `resume_facts` | engine.py (脚本初始化) | ❌ 不可篡改 | 保持不变 |
| Layer 2: Decisions | `user_decisions` | Architect (经用户确认) | ✅ 可追加/修改 | 保留已确认项 |
| Layer 3: Outputs | `expert_outputs.*` | 各专家节点 | ✅ 随时覆盖 | 清空后重新生成 |

### 4.3 快照读写流程

```
[初始化] engine.py 启动
  │
  ├── 检查 sessions/{session_id}/snapshot.json 是否存在?
  │   ├── 存在 → 读取 _meta.status → 断点恢复
  │   └── 不存在 → 创建新 session
  │
  ├── 调用 jd_parser.py → 填充 jd_facts + resume_facts (Layer 1)
  │
  [主循环] while _meta.status != "complete":
  │   │
  │   ├── 根据 _meta.status + _meta.current_node 确定调用哪个专家
  │   ├── 从 snapshot 提取该阶段需要的上下文字段
  │   ├── 注入白名单工具 (TOOL_REGISTRY[node])
  │   │
  │   ├── 调用 LLM 专家节点
  │   │   ├── 输出: 专业结果 (简历草案 / 审计报告等)
  │   │   └── 输出: <!-- STATE_UPDATE --> {...JSON...} <!-- /STATE_UPDATE -->
  │   │
  │   ├── 解析 STATE_UPDATE JSON
  │   │   ├── 解析失败 → 内部 Self-Correction 重试 (不干扰用户)
  │   │   └── 成功 → deep_merge 到对应层级
  │   │
  │   ├── 检查 guardrails:
  │   │   ├── expert_outputs.auditor.major_issues 含 🔴?
  │   │   │   └── YES → _meta.status 回退到 phase_3, ++rollback_count
  │   │   └── rollback_count > MAX_ROLLBACKS?
  │   │       └── YES → 终止, 报告给用户
  │   │
  │   └── 更新 _meta.last_updated, 持久化 snapshot.json
  │
  [完成] _meta.status = "complete"
  │
  └── 渲染输出 (HTML Pipeline, 见第 6 章)
  └── 归档: sessions/{id}/ → history/{date}_{company}_{role}_snapshot.json
```

---

## 5. 专家节点输出规范

### 5.1 STATE_UPDATE JSON 格式（强制）

每个专家节点的输出**必须**在末尾附带此块：

```markdown
<!-- STATE_UPDATE -->
{
  "node": "architect",
  "phase_completed": "3_adjustment",
  "decisions_delta": {
    "user_decisions.kept_experiences": ["pwc", "valores", "jiuqi", "didi"],
    "user_decisions.removed_experiences": ["tianzhi", "strowin"],
    "user_decisions.confirmed_quantifications": {
      "jiuqi_b3": "5 days → 6 hours, 12 lines"
    }
  },
  "outputs_delta": {
    "expert_outputs.writer.draft_path": "sessions/.../tailored_draft.md",
    "expert_outputs.writer.applied_rules": ["cp1_selection", "cp3_quantify", "cp4_wording"]
  },
  "next_status": "phase_4_delivery",
  "flags": ["has_major_content_changes"]
}
<!-- /STATE_UPDATE -->
```

**engine.py 用正则提取此块**，解析失败则要求 LLM 重新格式化。

### 5.2 各节点输出要求

| 节点 | 主要输出内容 | 必须包含的 STATE_UPDATE 字段 |
|------|-------------|--------------------------|
| Scout | 匹配评分表、Hard Gaps 列表 | `expert_outputs.scout.*`, `jd_facts.*`(补充) |
| Architect | 定制后的 Markdown 简历 | `user_decisions.*`, `expert_outputs.writer.*` |
| Auditor | 审计日志 (.md)、Mock Questions、STAR Notes | `expert_outputs.auditor.*`, 可能含 `next_status` 回退 |

---

## 6. 渲染管线（HTML 中间层）

### 6.1 为什么不用 python-docx 直接写？

- 表格列宽无法精确控制
- 行距/边距单位映射复杂（twips vs 逻辑单位）
- LLM 生成的 docx 格式代码质量不稳定

### 6.2 架构

```
LLM 输出结构化 Markdown
        │
        ▼
  [Markdown → HTML 转换]
  使用 markdown 库 + 自定义 CSS template
        │
        ▼
  styled_resume.html  ← 像素级排版控制在这里
  (CSS 定义字体/行距/表格/间距/视觉层次)
        │
   ┌────┴────┐
   ▼         ▼
PDF        DOCX
(pdfkit)  (python-docx 从 HTML 注入 或 pandoc)
```

### 6.3 CSS Template 核心样式

```css
/* Resume CSS Template — v1 */
body { font-family: "Segoe UI", "Microsoft YaHei", sans-serif; font-size: 10.5pt; line-height: 1.35; margin: 0; padding: 0.72in; }

/* Section Headers */
h2 { font-size: 13pt; border-bottom: 1pt solid #333; margin-top: 14pt; margin-bottom: 4pt; letter-spacing: 0.5pt; }

/* Experience Entries */
.entry { margin-bottom: 8pt; }
.entry-header { display: flex; justify-content: space-between; }
.entry-title { font-weight: bold; }
.entry-date { color: #555; font-size: 9.5pt; }
.entry-subtitle { font-style: italic; color: #444; margin-bottom: 2pt; }
.entry-bullets { margin-left: 16pt; margin-top: 3pt; }
.entry-bullets li { margin-bottom: 2pt; line-height: 1.3; }

/* Table for skills/certificates */
.skill-table { width: 100%; border-collapse: collapse; margin: 6pt 0; }
.skill-table td { padding: 2pt 6pt; vertical-align: top; }
.skill-table td:first-child { font-weight: bold; width: 25%; color: #333; }
```

### 6.4 渲染路由

```python
def render_output(markdown_content: str, output_format: str, session_dir: str):
    html = markdown_to_html(markdown_content, css_template="resume_template.css")
    
    if output_format == "pdf":
        return html_to_pdf(html, f"{session_dir}/tailored_resume.pdf")
    elif output_format == "docx":
        return html_to_docx(html, f"{session_dir}/tailored_resume.docx")
    else:  # html
        save(html, f"{session_dir}/tailored_resume.html")
        return html
```

### 6.5 默认输出策略

- **主输出**: PDF（通过 HTML → pdfkit，排版最佳）
- **备选输出**: DOCX（通过 HTML → python-docx 或 pandoc）
- **审计交付物**: Markdown（审计日志、Mock Questions、STAR Notes）
- 用户可在 Quick Start 时指定偏好，否则默认 PDF

---

## 7. 文件结构蓝图

```
resume-tailor/
│
├── SKILL.md                          # [改造] ~200行 路由表 + 原则
├── README.md / README.zh-CN.md       # 已完成的产品文档 (v2.4)
│
├── engine.py                         # [改造] 编排循环 + 快照读写 + 渲染路由
│
├── scripts/
│   ├── jd_parser.py                  # [已有] Layer 1 初始化器
│   ├── diff_audit.py                 # [已有] 版本变更审计
│   ├── ats_checker.py                # [已有] ATS 合规检查
│   ├── utils.py                      # [已有] 工具函数
│   └── renderer.py                   # [新增] Markdown→HTML→PDF/DOCX 渲染器
│
├── references/                       # [拆分/新增] 专家节点指令集
│   ├── scout_guide.md                # Context Scout 完整指令 (~150行)
│   ├── writer_guide.md               # Resume Architect 完整指令 (~300行)
│   ├── auditor_guide.md              # Sincerity Auditor 完整指令 (~250行)
│   ├── interaction_checkpoints.md    # [已有] CP1-CP4 交互模板
│   └── reverse_audit_guide.md        # [已有/增强] 反向审计指南
│
├── schemas/
│   └── snapshot_schema_v1.json        # [新增] JSON Schema 校验定义
│
├── templates/
│   ├── state_update_template.md      # [新增] STATE_UPDATE 输出格式模板
│   └── resume_template.css           # [新增] 简历 HTML/CSS 排版模板
│
├── sessions/                         # [新增] 运行时临时目录 (gitignore)
│   └── {session_id}/
│       ├── snapshot.json             # 运行时高频读写
│       ├── tailored_draft.md          # Architect 产出草稿
│       ├── tailored_resume.html       # 渲染后 HTML
│       └── tailored_resume.pdf/.docx  # 最终交付物
│
├── history/                          # [已有] 归档目录
│   ├── {YYYY-MM-DD}_{company}_{role}.md            # Markdown 简历
│   ├── {YYYY-MM-DD}_{company}_{role}_audit.md       # 审计日志
│   ├── {YYYY-MM-DD}_{company}_{role}.pdf/.docx      # 最终交付物
│   └── {YYYY-MM-DD}_{company}_{role}_snapshot.json  # [新增] 快照归档
│
└── requirements.txt                  # [更新] 新增依赖
```

---

## 8. 容错与 Guardrails

### 8.1 格式校验

```python
# engine.py 校验逻辑
STATE_UPDATE_PATTERN = r'<!-- STATE_UPDATE -->\n(.*?)\n<!-- /STATE_UPDATE -->'

def extract_state_update(llm_output: str) -> dict:
    match = re.search(STATE_UPDATE_PATTERN, llm_output, re.DOTALL)
    if not match:
        raise StateUpdateMissingError()
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError:
        raise StateUpdateFormatError()  # 触发内部重试
```

### 8.2 回退机制

```
Auditor 发现 🔴 Major Issues:
  1. expert_outputs.auditor.major_issues 追加问题
  2. _meta.status 设为 "phase_3_adjustment" (回退)
  3. _meta.rollback_count += 1
  4. 如果 rollback_count > MAX_ROLLBACKS (默认 2):
     → 终止循环, 向用户报告无法自动修复的问题清单
     → 让用户手动决定是否继续
```

### 8.3 断点恢复

```python
# engine.py 启动时的恢复逻辑
def get_or_create_session(session_id: str) -> dict:
    snapshot_path = f"sessions/{session_id}/snapshot.json"
    if os.path.exists(snapshot_path):
        snapshot = json.load(open(snapshot_path))
        log(f"[RESUME] Restoring from phase {snapshot['_meta']['status']}")
        return snapshot
    else:
        os.makedirs(f"sessions/{session_id}", exist_ok=True)
        return init_new_snapshot(jd_text, resume_text)
```

### 8.4 Active-to-Archive

```python
def archive_session(session_id: str, company: str, role: str):
    src = f"sessions/{session_id}"
    date = datetime.now().strftime("%Y-%m-%d")
    dst_prefix = f"history/{date}_{slugify(company)}_{slugify(role)}"
    
    shutil.copy(f"{src}/snapshot.json", f"{dst_prefix}_snapshot.json")
    if os.path.exists(f"{src}/tailored_resume.pdf"):
        shutil.copy(f"{src}/tailored_resume.pdf", f"{dst_prefix}.pdf")
    # ... 其他文件
    
    shutil.rmtree(src)  # 清理运行时目录
```

---

## 9. 工具白名单注册

```python
TOOL_REGISTRY = {
    "scout": [
        "web_search",       # 平台内置，零成本
        "jd_parser"         # 本地脚本
    ],
    "architect": [
        # 无外部工具 — Architect 靠对话交互完成全部工作
        # CP1-CP4 的引导逻辑已在 interaction_checkpoints.md 中定义
    ],
    "auditor": [
        "ats_checker",     # 本地脚本
        "diff_audit"       # 本地脚本
    ]
}

def inject_tools(node_name: str):
    """根据当前节点注入最小权限工具集"""
    return [load_tool(t) for t in TOOL_REGISTRY.get(node_name, [])]
```

---

## 10. 实施计划

### Phase A: 协议基础设施 (P0)

| 任务 | 文件 | 说明 |
|------|------|------|
| 创建 snapshot schema | `schemas/snapshot_schema_v1.json` | JSON Schema 定义 |
| 创建 STATE_UPDATE 模板 | `templates/state_update_template.md` | LLM 输出格式规范 |
| 创建 CSS 模板 | `templates/resume_template.css` | 简历排版样式 |

### Phase B: 指令拆分 (P1)

| 任务 | 文件 | 来源 |
|------|------|------|
| Writer Guide | `references/writer_guide.md` | 从 SKILL.md Phase 2-3 拆出 |
| Auditor Guide | `references/auditor_guide.md` | 从 SKILL.md Phase 4 + reverse_audit 合并 |
| Scout Guide | `references/scout_guide.md` | 从 SKILL.md Phase 1 拆出 |
| SKILL.md 瘦身 | `SKILL.md` | 改为 ~200 行路由表 |

### Phase C: 引擎改造 (P1)

| 任务 | 文件 | 说明 |
|------|------|------|
| 编排循环框架 | `engine.py` | while 循环 + 节点调度 + 快照读写 |
| STATE_UPDATE 解析器 | `engine.py` | 正则提取 + JSON 校验 + 错误重试 |
| 回退逻辑 | `engine.py` | 🔴 Major → Phase 3 + rollback_count 限制 |
| 断点恢复 | `engine.py` | sessions/ 检测 + 状态恢复 |
| Active-to-Archive | `engine.py` | 完成→归档→清理 |

### Phase D: 渲染管线 (P1)

| 任务 | 文件 | 说明 |
|------|------|------|
| Markdown→HTML 转换器 | `scripts/renderer.py` | markdown 库 + CSS 注入 |
| HTML→PDF | `scripts/renderer.py` | pdfkit / weasyprint |
| HTML→DOCX | `scripts/renderer.py` | pandoc 或 python-docx HTML 注入 |
| 渲染路由集成 | `engine.py` | 在 complete 阶段调用 renderer |

### Phase E: 集成测试 (P2)

- 端到端运行完整流程
- 验证回退机制触发
- 验证断点恢复
- 验证输出 PDF/DOCX 排版质量

---

## 11. Future (v2.6+)

以下功能已记录但不在 v2.5 范围内：

- LaTeX 渲染器（学术岗高规格 PDF）
- HTML/React 交互式网页简历
- agent-browser 集成（深度公司调研）
- image_gen 集成（个人品牌素材）
- 外部 Skill 动态挂载（如 brainstorming 作为显式 skill）
- 多 JD 批量处理
- Application Tracker 集成

---

## Appendix A: 与 v2.4 的关键差异

| 维度 | v2.4 | v2.5 |
|------|------|------|
| 架构 | 单体 Skill，顺序执行 | 伪多智能体，物理隔离 LLM 调用 |
| 状态管理 | Context window 传递 | context_snapshot.json 黑板协议 |
| 审计保障 | 同一 context 内执行（可能被跳过） | 独立 API 调用（强制执行） |
| 输出格式 | LLM 直接写 .docx（格式差） | Markdown → HTML → PDF/DOCX（CSS 控制排版） |
| SKILL.md | ~600 行完整指令 | ~200 行路由表 + references 子目录 |
| 错误处理 | 无 | 格式校验 + 回退机制 + 断点恢复 |
| 工具使用 | 无明确边界 | 最小权限白名单 |
