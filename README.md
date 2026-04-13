# Personal Efficiency Enhancing Skills

个人效率增强 Skills 合集，适用于 [WorkBuddy](https://www.codebuddy.cn/) / Claw 等 AI 助手平台。

## Skills

### Resume Tailor (`resume-tailor/`)

**一句话概括**：输入 JD → 自动匹配分析 → 交互式调整简历 → 生成 PDF + 版本审计。

#### 核心功能

- **JD 关键词提取**：自动解析 JD 文本，分类提取硬技能、软技能、行业背景、经验要求
- **简历匹配分析**：对比 master 简历与 JD 关键词，输出直接匹配 / 可关联 / 缺口三类报告
- **交互式调整**：6 个决策介入点，你可以全程引导调整方向：
  1. 经历取舍（保留 / 弱化 / 删除）
  2. 措辞升级（确认后再优化，避免过度包装）
  3. 量化补充（提醒补上缺失的数据指标）
  4. 内容缺口（引导你回忆 JD 要求但简历没写的经历）
  5. 经历合并/拆分（多段经历组合或拆分强调）
  6. 最终确认（完整预览后再生成 PDF）
- **版本审计**：每次生成保留完整 diff 记录，方便回溯每次调整了什么
- **PDF 输出**：Markdown 预览 → 确认 → .docx → PDF

#### 安装

适用于 WorkBuddy / Claw 及兼容平台：

**方法一：直接复制（推荐）**

将 `resume-tailor/` 文件夹复制到你的 skills 目录：

| 平台 | Skills 目录路径 |
|------|----------------|
| **WorkBuddy / Claw** | `~/.workbuddy/skills/resume-tailor/` |
| **Cursor** | `~/.cursor/skills/resume-tailor/` |
| **Cline** | `~/.cline/skills/resume-tailor/` |
| **通用** | 项目根目录 `.workbuddy/skills/resume-tailor/` |

> `~` 指用户主目录，Windows 上为 `C:\Users\<你的用户名>\`

**方法二：Git Clone**

```bash
git clone https://github.com/dmlin7777777/personal-efficiency-enhancing-skills.git
cp -r personal-efficiency-enhancing-skills/resume-tailor ~/.workbuddy/skills/
```

#### 使用方式

安装后，在 AI 助手中输入：

```
帮我针对这个 JD 调简历：[粘贴 JD 文本或 URL]
```

#### 前置依赖

| 依赖 | 用途 | 安装方式 |
|------|------|---------|
| `python-docx` | 读取和生成 .docx 文件 | `pip install python-docx` |
| `pandoc` | .docx 转 PDF | [官网下载](https://pandoc.org/installing.html) |

#### 文件结构

```
resume-tailor/
├── SKILL.md                              # Skill 主定义文件（工作流 + 触发词）
├── scripts/
│   ├── jd_parser.py                      # JD 关键词提取脚本
│   └── diff_audit.py                     # 新旧简历对比审计脚本
├── references/
│   ├── interaction_checkpoints.md        # 6 个交互介入点详细指引
│   └── audit_log_template.md             # 版本变更日志模板
└── requirements.txt                      # Python 依赖
```

## 贡献

欢迎提交 Issue 和 PR。如果你基于这些 Skills 做了改进，欢迎 Fork 后提 PR。

## License

MIT
