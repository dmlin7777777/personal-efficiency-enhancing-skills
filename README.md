# Personal Efficiency Enhancing Skills / 个人效率增强 Skills

A collection of AI assistant Skills designed to enhance personal workflow efficiency.
适用于 [WorkBuddy](https://www.codebuddy.cn/) / Claw 等 AI 助手平台的 Skills 合集。

---

## Skills

### Resume Tailor (`resume-tailor/`)

**Tailor your resume for any job description with one command.**
**一句话概括**：输入 JD → 自动匹配分析 → 交互式调整简历 → 生成 PDF + 版本审计。

#### Features / 核心功能

- **JD Keyword Extraction / JD 关键词提取**: Automatically parses JD text to extract hard skills, soft skills, domain keywords, and experience requirements / 自动解析 JD 文本，分类提取硬技能、软技能、行业背景、经验要求
- **Resume Matching / 简历匹配分析**: Analyzes how well your master resume matches the target JD / 对比 master 简历与 JD 关键词，输出直接匹配 / 可关联 / 缺口三类报告
- **Interactive Adjustment / 交互式调整**: 6 decision points where you can guide the tailoring process / 6 个决策介入点，你可以全程引导调整方向：
  1. Experience selection — keep, demote, or remove / 经历取舍
  2. Wording upgrades — fact-check before escalating / 措辞升级（确认后再优化）
  3. Quantification gaps — add missing numbers / 量化补充
  4. Content gaps — prompt you to recall relevant experience / 内容缺口（引导回忆）
  5. Merge/split decisions — combine or split experiences / 经历合并/拆分
  6. Final confirmation before PDF generation / 最终确认
- **Version Audit / 版本审计**: Every tailored version is logged with a full diff against the master / 每次生成保留完整 diff 记录，方便回溯
- **PDF Output / PDF 输出**: Markdown preview → confirmation → .docx → PDF

#### Installation / 安装

Compatible with WorkBuddy / Claw, Cursor, Cline, and other AI assistant platforms.
适用于 WorkBuddy / Claw、Cursor、Cline 及其他兼容平台。

**Method 1: Copy directly / 直接复制（推荐）**

Copy the `resume-tailor/` folder to your skills directory:
将 `resume-tailor/` 文件夹复制到你的 skills 目录：

| Platform / 平台 | Skills Directory / 目录路径 |
|---|---|
| **WorkBuddy / Claw** | `~/.workbuddy/skills/resume-tailor/` |
| **Cursor** | `~/.cursor/skills/resume-tailor/` |
| **Cline** | `~/.cline/skills/resume-tailor/` |
| **Generic / 通用** | `.workbuddy/skills/resume-tailor/` (project root) |

> `~` refers to your home directory. On Windows: `C:\Users\<username>\`

**Method 2: Git Clone**

```bash
git clone https://github.com/dmlin7777777/personal-efficiency-enhancing-skills.git
cp -r personal-efficiency-enhancing-skills/resume-tailor ~/.workbuddy/skills/
```

#### Usage / 使用方式

After installation, prompt your AI assistant:
安装后，在 AI 助手中输入：

```
Help me tailor my resume for this JD: [paste JD text or URL]
帮我针对这个 JD 调简历：[粘贴 JD 文本或 URL]
```

#### Dependencies / 前置依赖

| Dependency | Purpose / 用途 | Install / 安装方式 |
|---|---|---|
| `python-docx` | Read and generate .docx files / 读取和生成 .docx | `pip install python-docx` |
| `pandoc` | Convert .docx to PDF / .docx 转 PDF | [Download](https://pandoc.org/installing.html) |

#### File Structure / 文件结构

```
resume-tailor/
├── SKILL.md                              # Main skill definition / Skill 主定义
├── scripts/
│   ├── jd_parser.py                      # JD keyword extraction / JD 关键词提取
│   └── diff_audit.py                     # Resume diff audit / 新旧简历对比审计
├── references/
│   ├── interaction_checkpoints.md        # 6 interaction checkpoints / 交互介入点指引
│   └── audit_log_template.md             # Audit log template / 版本变更日志模板
└── requirements.txt                      # Python dependencies / Python 依赖
```

---

## Contributing / 贡献

Issues and PRs are welcome. If you improve these Skills, feel free to fork and submit a PR.
欢迎提交 Issue 和 PR。如果你基于这些 Skills 做了改进，欢迎 Fork 后提 PR。

## License

MIT
