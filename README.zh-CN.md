<div align="center">

# Resume Tailor

**AI 驱动的简历定制 — 不是润色工具，是求职教练**

[English](README.md) · [简体中文](README.zh-CN.md)

</div>

---

## 为什么不一样？

> **🪞 不只是改写，更是教练。** 内置面试官画像，在你投递前从攻击者视角审视简历的每一个漏洞。
>
> **🚫 拒绝 AI 废话。** 强制量化原则——没有数字支撑的"实现智能化"会被自动拦截。
>
> **🌍 全球通行。** 自动适配不同地区的求职潜规则——北美删照片、德国补空窗期、东亚调语调。

---

## 核心能力

### 🎯 语义级匹配
不只关键词堆砌。能识别"抗压能力强"与"Thrives in fast-paced environments"的深层语义对齐，并标注匹配置信度。

### ⚖️ 跨证书对齐
JD 写了英语六级，你只有雅思 7.5？它会告诉你这超过了要求，并保留更有说服力的证书。

### 🔍 反向面试审计
自动生成针对你简历漏洞的面试追问，让你在被面试官挑战前先做好准备。

<details>
<summary>📝 示例：会触发什么追问？</summary>

**你的 bullet：** "主导 AI Agent 方案设计，实现财务数据处理智能化。"

**系统生成的模拟追问：**

> 1. *"主导"——团队多大？你有直接下属还是跨组协调？*
> 2. *"AI Agent 方案"——用的什么平台？架构决策过程是怎样的？*
> 3. *"实现智能化"——具体提升了什么指标？处理时间？错误率？处理量？*
> 4. 如果你无法用数字回答第 3 题，Anti-Filler Rule 会介入，去掉空泛描述，重写为不含模糊结果的表述。

</details>

### 🚫 隐私合规
投递北美岗位？自动标记需要删除的照片和生日。德国岗位？提醒你补充空窗期说明。

### 📊 拒绝空话
每条经历必须满足：**动作 + 对象 + 可量化成果**。说不出数字？它会用场景化追问引导你回忆，而不是编造。

### 🌐 文化语调适配
根据目标地区自动调整动词强度和自我推销程度——北美自信果敢，东亚协同低调，北欧谦逊务实。

---

## 快速开始

```
"帮我针对这个 JD 调简历"
```

提供一份 JD（链接或文字）和你的简历（.docx / .pdf / .txt），就这么简单。

系统会自动完成：
1. **调研** — 扫描该岗位当前的招聘偏好
2. **匹配** — 用置信度评分对比你的简历与 JD 要求
3. **建议** — 提出保留、删除、改写、量化的建议（你确认或否决）
4. **交付** — 生成定制简历，附带反向审计和面试准备

---

## 工作原理

| 阶段 | 做什么 | 你的角色 |
|------|--------|---------|
| **1. 背景调研** | 提取 JD 要求（脚本 + LLM），调研公司，评估风险 | 审阅确认 |
| **2. 语义匹配** | 直接匹配 + 隐性匹配，标注置信度 | 审阅匹配表 |
| **3. 交互调整** | 经历取舍、缺口补全、量化补充、措辞升级 | 确认或否决每条建议 |
| **4. 审计交付** | 合规检查、面试官视角审查、模拟追问、生成 .docx | 最终审阅 |

每个建议都附带具体方案——你只需要确认或否决，不需要从零开始做决策。

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

### jd_parser.py — 从 JD 提取结构化特征
```bash
# 仅 JD
python scripts/jd_parser.py --file jd.txt --json

# JD + 简历匹配
python scripts/jd_parser.py --file jd.txt --resume resume.docx --json
```

### main.py — CLI 入口
```bash
# 结构化简历读取
python scripts/main.py read-structured --resume resume.docx

# Diff 对比（源简历 vs 定制简历）
python scripts/main.py diff --source-docx source.docx --tailored tailored.md --company "Company" --role "Role" --json
```

### ats_checker.py — ATS 兼容性检查
```bash
python scripts/ats_checker.py --resume tailored.md --keywords "Python,SQL,AWS" --region north_america --json
```

**地区配置**: north_america, uk_ireland, dach, east_asia, global

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

### v2.4（当前版本）— 结构性重构
- 4 阶段流水线（从 5 阶段合并），3 级路由，统一特征提取
- Anti-Filler Rule、Propose-don't-ask 原则、反向审计
- 影子副本改为按需触发

### v2.3 — 鲁棒性与体验加固
- 市场调研、经历排序硬约束、页数限制、Anti-Filler Rule

[完整更新日志 → CHANGELOG.md](CHANGELOG.md)

---

## 许可证

MIT
