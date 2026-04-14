<div align="center">

# Resume Tailor

**AI 驱动的简历定制 — 不是润色工具，是求职教练**

*本项目遵循"教练而非润色器"的理念。*

[English](README.md) · [简体中文](README.zh-CN.md)

</div>

---

## 为什么需要它？

大多数 AI 简历工具只会**改写**你的 bullet 让它听起来很厉害。而这个工具**引导**你让它们变得真实。

| 传统 AI 改写 | Resume Tailor |
|---|---|
| ❌ "显著提升了数据分析效率，获得团队认可" | ✅ "主导搭建自动化对账工具，将月度核算周期从 **5 天缩短至 6 小时**，覆盖 **12 条业务线**" |
| 缺少数据时就用空泛形容词填充 | 用场景化追问引导量化 — 说不出数字就保留原文 |
| 对角色盲目乐观（什么都是"主导"） | 每条声明都挑战你：*"你是最终决策者吗？"* |
| 千篇一律的输出 | 根据目标地区自动调整语调、格式、隐私规则 |

**区别**：一份被精心包装的谎言会在面试中被戳穿。一份经过教练打磨的真实经历能帮你拿到 offer。

---

## 你将得到什么

你不只得到一份定制简历。你得到一套**求职攻略包**。

### ✅ 定制简历（.docx）
针对特定 JD 和目标地区优化 — ATS 兼容、文化适配、事实准确。

### 📊 审计日志
每项修改都有据可查：
- 每个 JD 要求的匹配置信度评分
- 硬性缺口标记（缺失证书、经验门槛）
- 合规预警（按地区提示删除照片/年龄等）

### 🎙️ 面试准备包
对简历上的每一处重大修改，系统自动生成：
- **模拟追问** — 面试官可能会挑战你的问题
- **STAR 笔记** — 结构化回答要点，让你能自信地捍卫每一条经历

---

## 核心原则

这些是写入每一次运行的不可协商的硬规则：

### 🚫 拒绝空话（Anti-Filler Rule）
每条经历必须满足：**动作 + 对象 + 可量化成果**
- 说不出数字？系统用递进式追问引导回忆。
- 追问两轮仍无果？保留原文措辞——绝不编造指标。
- **铁律：空泛的结果比没有结果更差。**

### 🪞 反向审计
交付前，面试官画像从攻击者视角审视每一条经历。角色夸大、逻辑跳跃、术语堆砌在 HR 看到之前就被拦截。

### ⏳ 事实守恒
工作经历严格按**时间倒序排列**。不允许按相关性重排——只能保留或隐藏。

### 🌐 文化语调滑块
动词强度自动调整：自信果断（北美）→ 协同低调（东亚）→ 谦逊务实（北欧）。同样的内容，不同的呈现方式。

### ⚖️ 跨证书对齐
雅思 7.5 ≈ 六级 550+。系统跨地区映射证书等价关系，并保留最具说服力的那一个。

---

## 工作原理

```
Phase 1 — 背景调研与上下文     了解岗位、调研公司
Phase 2 — 语义匹配            将你的经历与 JD 要求逐一比对
Phase 3 — 交互式调整           审阅建议、确认或否决
Phase 4 — 审计交付             最终合规检查、模拟追问、输出文件
```

| 阶段 | 做什么 | 你的角色 |
|------|--------|---------|
| **1. 背景** | 提取 JD 要求（脚本 + LLM），调研公司，评估风险 | 审阅确认 |
| **2. 匹配** | 直接匹配 + 隐性匹配，标注置信度 | 审阅匹配表 |
| **3. 调整** | 经历取舍、缺口补全、量化补充、措辞升级 | 确认或否决每条建议 |
| **4. 审计** | 合规检查、面试官视角审查、模拟追问、生成 .docx | 最终审阅 |

每个建议都附带具体方案——你只需要确认或否决，不需要从零开始做决策。

---

## 快速开始

```bash
# 提供 JD 和简历
"帮我针对这个 JD 调简历"
```

就这么简单。系统会自动完成调研、匹配、调整和审计全流程。

---

## 开发者文档

<details>
<summary>📁 文件结构</summary>

```
resume-tailor/
├── SKILL.md                          # Skill 定义与工作流
├── requirements.txt                  # Python 依赖
├── scripts/
│   ├── main.py                       # CLI 入口
│   ├── engine.py                     # 流水线编排
│   ├── utils.py                      # 共享工具函数
│   ├── jd_parser.py                  # 硬性要求提取
│   ├── diff_audit.py                 # 源简历 vs 定制简历 diff
│   └── ats_checker.py                # ATS 兼容性检查
└── references/
    ├── interaction_checkpoints.md    # 交互检查点模板
    └── audit_log_template.md         # 审计日志结构模板
```

</details>

<details>
<summary>⚙️ 脚本使用</summary>

```bash
# 仅 JD
python scripts/jd_parser.py --file jd.txt --json

# JD + 简历匹配
python scripts/jd_parser.py --file jd.txt --resume resume.docx --json

# 结构化简历读取
python scripts/main.py read-structured --resume resume.docx

# Diff 对比
python scripts/main.py diff --source-docx source.docx --tailored tailored.md

# ATS 兼容性检查
python scripts/ats_checker.py --resume tailored.md --region north_america --json
```
**地区**: north_america, uk_ireland, dach, east_asia, global

</details>

<details>
<summary>📦 依赖</summary>

```
python-docx>=0.8.11    # .docx 读写
pdfplumber>=0.9.0      # PDF 读取（主要）
PyPDF2>=3.0.0          # PDF 读取（备用）
```
可选: `pandoc`（用于 PDF 生成）

</details>

---

## 版本历史

### v2.4（当前）— 结构性重构
- 4 阶段流水线，3 级路由，统一特征提取
- Anti-Filler Rule、Propose-don't-ask 原则、反向审计
- 影子副本改为按需触发

[完整更新日志 → CHANGELOG.md](CHANGELOG.md)

---

## 许可证

MIT
