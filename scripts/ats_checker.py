"""
ATS Checker - Validate resume ATS compatibility with regional profiles.

Checks resume for ATS parsing risks and provides actionable fix suggestions.
Supports regional profiles with different ATS system expectations and PII rules.

Checks:
- Format: tables, images, special characters
- Structure: standard sections, contact info, bullet length
- Content: date consistency, keyword coverage
- Regional PII: privacy compliance based on target region

Usage:
    # Basic check (auto-detect region from language)
    python ats_checker.py --resume <resume_md>

    # With JD keywords
    python ats_checker.py --resume <resume_md> --keywords "Python,SQL,AWS"

    # With region profile
    python ats_checker.py --resume <resume_md> --region north_america --json

    # Full pipeline
    python ats_checker.py --resume <resume_md> --keywords-file <keywords.json>
        --region uk_ireland --json --output audit_ats.json

Output:
    JSON (for LLM pipeline) or Markdown report (for user review).
"""

import re
import sys
import argparse
import json
from datetime import datetime

from utils import detect_language, PII_PATTERNS, DATE_FORMAT_PATTERNS

REGIONAL_PROFILES = {
    "north_america": {
        "label": "North America (US/Canada)",
        "label_zh": "北美（美国/加拿大）",
        "ats_systems": ["Workday", "Greenhouse", "Lever", "iCIMS", "Jobvite"],
        "expected_sections": ["Experience", "Education", "Skills"],
        "max_pages": 2,
        "forbidden_pii": [
            "photo", "age", "gender", "marital_status", "religion",
            "nationality", "salary_history", "full_address",
        ],
        "strict_format": True,
    },
    "uk_ireland": {
        "label": "UK / Ireland",
        "label_zh": "英国/爱尔兰",
        "ats_systems": ["Workday", "Greenhouse", "Hireserve"],
        "expected_sections": ["Experience", "Education", "Skills"],
        "max_pages": 2,
        "forbidden_pii": [
            "photo", "age", "gender", "marital_status", "religion",
            "national_insurance",
        ],
        "strict_format": True,
    },
    "dach": {
        "label": "DACH (Germany/Austria/Switzerland)",
        "label_zh": "德语区（德国/奥地利/瑞士）",
        "ats_systems": ["SAP SuccessFactors", "Personio", "Checkin"],
        "expected_sections": ["Experience", "Education", "Skills"],
        "max_pages": 3,
        "forbidden_pii": ["religion", "political_affiliation"],
        "strict_format": False,
    },
    "east_asia": {
        "label": "East Asia (CN/JP/KR/SG)",
        "label_zh": "东亚（中日韩新）",
        "ats_systems": ["Moka HR", "Beisen", "51job", "BizReach"],
        "expected_sections": ["Experience", "Education"],
        "max_pages": 2,
        "forbidden_pii": [],
        "strict_format": False,
    },
    "global": {
        "label": "Global / Remote",
        "label_zh": "全球/远程",
        "ats_systems": ["Workday", "Greenhouse", "Lever"],
        "expected_sections": ["Experience", "Education", "Skills"],
        "max_pages": 2,
        "forbidden_pii": [
            "photo", "age", "gender", "marital_status", "religion",
            "nationality", "salary_history",
        ],
        "strict_format": True,
    },
}


# ---------------------------------------------------------------------------
# Check functions
# ---------------------------------------------------------------------------

def check_tables(text: str) -> list:
    """Detect markdown/HTML tables in resume."""
    issues = []
    # Markdown tables
    md_tables = re.findall(r"^\|.+\|$", text, re.MULTILINE)
    if md_tables:
        # Count unique tables (consecutive table rows = 1 table)
        table_count = 0
        in_table = False
        for line in text.split("\n"):
            if re.match(r"^\|.+\|$", line.strip()):
                if not in_table:
                    table_count += 1
                    in_table = True
            else:
                in_table = False

        issues.append({
            "check": "tables",
            "severity": "high" if md_tables else "low",
            "detail_en": f"Found {table_count} markdown table(s). ATS systems may not parse table content correctly.",
            "detail_zh": f"发现 {table_count} 个 Markdown 表格。ATS 系统可能无法正确解析表格内容。",
            "suggestion_en": "Convert tables to bullet lists. Example: '- Python, SQL, Power BI' instead of a skills table.",
            "suggestion_zh": "将表格转换为列表。例如：用 '- Python, SQL, Power BI' 替代技能表格。",
            "evidence": md_tables[:3],  # cap at 3 examples
        })

    # HTML tables
    html_tables = re.findall(r"<table\b", text, re.IGNORECASE)
    if html_tables:
        issues.append({
            "check": "tables_html",
            "severity": "high",
            "detail_en": f"Found {len(html_tables)} HTML table(s). ATS will not parse HTML markup.",
            "detail_zh": f"发现 {len(html_tables)} 个 HTML 表格。ATS 不会解析 HTML 标记。",
            "suggestion_en": "Remove HTML markup. Use plain text with bullet lists.",
            "suggestion_zh": "移除 HTML 标记，使用纯文本加列表。",
            "evidence": [f"<table> (x{len(html_tables)})"],
        })

    return issues


def check_images(text: str) -> list:
    """Detect image references in resume."""
    issues = []

    # Markdown images
    md_images = re.findall(r"!\[[^\]]*\]\([^)]+\)", text)
    if md_images:
        issues.append({
            "check": "images",
            "severity": "high",
            "detail_en": f"Found {len(md_images)} image reference(s). ATS cannot read images.",
            "detail_zh": f"发现 {len(md_images)} 个图片引用。ATS 无法读取图片。",
            "suggestion_en": "Remove all image references. ATS may misparse surrounding text when it encounters image syntax.",
            "suggestion_zh": "移除所有图片引用。ATS 遇到图片语法时可能错误解析周围文本。",
            "evidence": md_images[:3],
        })

    # HTML images
    html_images = re.findall(r"<img\b[^>]+>", text, re.IGNORECASE)
    if html_images:
        issues.append({
            "check": "images_html",
            "severity": "high",
            "detail_en": f"Found {len(html_images)} HTML image tag(s).",
            "detail_zh": f"发现 {len(html_images)} 个 HTML 图片标签。",
            "suggestion_en": "Remove HTML image tags.",
            "suggestion_zh": "移除 HTML 图片标签。",
            "evidence": html_images[:3],
        })

    return issues


def check_special_chars(text: str) -> list:
    """Detect emojis, icons, and non-standard unicode symbols."""
    issues = []

    # Common emoji ranges
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001F900-\U0001F9FF"  # supplemental symbols
        "\U0001FA00-\U0001FA6F"  # chess symbols
        "\U0001FA70-\U0001FAFF"  # symbols extended
        "]+"
    )

    emojis = emoji_pattern.findall(text)
    if emojis:
        issues.append({
            "check": "emojis",
            "severity": "medium",
            "detail_en": f"Found {len(emojis)} emoji(s). ATS may corrupt or ignore emoji characters.",
            "detail_zh": f"发现 {len(emojis)} 个表情符号。ATS 可能会破坏或忽略表情符号。",
            "suggestion_en": "Replace emojis with standard bullet points (- or *) or plain text markers.",
            "suggestion_zh": "将表情符号替换为标准列表符号（- 或 *）或纯文本标记。",
            "evidence": list(set(emojis))[:5],
        })

    # Non-standard bullet characters
    special_bullets = re.findall(r"^[^\s\-\*\+•►❯✔✓✗✘▸→◆◇●○■□▪▫★☆]\s", text, re.MULTILINE)
    # Actually, let me detect bullets that are NOT standard
    nonstandard_lines = []
    for line in text.split("\n"):
        stripped = line.lstrip()
        if stripped and not re.match(r"^[-\*\+\d+\.\)]\s", stripped) and re.match(r"^[^\w#|`\s]", stripped):
            first_char = stripped[0]
            if first_char not in "-*+•►❯✔✓✗✘▸→◆◇●○■□▪▫★☆":  # allow common unicode bullets
                nonstandard_lines.append(line.strip()[:60])
    if nonstandard_lines:
        issues.append({
            "check": "nonstandard_bullets",
            "severity": "medium",
            "detail_en": f"Found {len(nonstandard_lines)} line(s) starting with non-standard characters.",
            "detail_zh": f"发现 {len(nonstandard_lines)} 行以非标准字符开头。",
            "suggestion_en": "Use standard markdown bullets (- or *) for list items.",
            "suggestion_zh": "使用标准 Markdown 列表符号（- 或 *）。",
            "evidence": nonstandard_lines[:3],
        })

    # Unicode decorative characters in section headers
    header_decorations = re.findall(r"^[#]+\s.*[─━│┃┄┅┆┇┈┉┊┋╌╍╎╗╔╚╝║═╠╣╦╩╬┌┐└┘├┤┬┴┼]", text, re.MULTILINE)
    if header_decorations:
        issues.append({
            "check": "decorative_chars",
            "severity": "low",
            "detail_en": "Found decorative unicode characters in headers. These may render incorrectly in ATS.",
            "detail_zh": "标题中发现装饰性 Unicode 字符。在 ATS 中可能显示异常。",
            "suggestion_en": "Use plain text or standard markdown headers (# ## ###) for section titles.",
            "suggestion_zh": "使用纯文本或标准 Markdown 标题（# ## ###）作为章节标题。",
            "evidence": [d.strip()[:60] for d in header_decorations[:3]],
        })

    return issues


def check_sections(text: str, profile: dict) -> list:
    """Check for standard resume sections expected by ATS."""
    issues = []

    # Extract section headers (markdown headers or all-caps lines)
    headers = set()
    for line in text.split("\n"):
        stripped = line.strip()
        # Markdown headers
        md_match = re.match(r"^#{1,4}\s+(.+)$", stripped)
        if md_match:
            headers.add(md_match.group(1).lower().strip())
        # All-caps section headers (common in plain text resumes)
        elif re.match(r"^[A-Z][A-Z\s&/]+$", stripped) and len(stripped) > 2:
            headers.add(stripped.lower().strip())

    expected = profile.get("expected_sections", ["Experience", "Education", "Skills"])
    # Aliases mapping
    section_aliases = {
        "experience": ["experience", "work experience", "professional experience",
                       "employment", "work history", "career history",
                       "工作经历", "工作经验", "职业经历", "工作背景"],
        "education": ["education", "academic", "academic background",
                      "qualifications", "教育背景", "学历", "教育经历"],
        "skills": ["skills", "technical skills", "core competencies",
                   "proficiencies", "技能", "专业技能", "核心能力", "技术栈"],
    }

    for section in expected:
        aliases = section_aliases.get(section.lower(), [section.lower()])
        found = any(alias in headers for alias in aliases)
        if not found:
            issues.append({
                "check": f"missing_section_{section.lower()}",
                "severity": "high",
                "detail_en": f"Missing standard '{section}' section. ATS uses section headers to categorize content.",
                "detail_zh": f"缺少标准的 '{section}' 章节。ATS 使用章节标题对内容进行分类。",
                "suggestion_en": f"Add a '{section}' section header. ATS systems expect standard section names for proper parsing.",
                "suggestion_zh": f"添加 '{section}' 章节标题。ATS 系统需要标准章节名才能正确解析。",
                "evidence": [f"Expected sections found: {list(headers)[:5]}"],
            })

    return issues


def check_contact_info(text: str) -> list:
    """Check for contact information (email, phone)."""
    issues = []

    has_email = bool(re.search(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", text))
    has_phone = bool(re.search(
        r"(?:\+?\d{1,3}[\s\-.]?)?\(?\d{2,4}\)?[\s\-.]?\d{3,4}[\s\-.]?\d{3,4}",
        text
    ))

    if not has_email:
        issues.append({
            "check": "missing_email",
            "severity": "high",
            "detail_en": "No email address found. ATS needs an email to link your application to your profile.",
            "detail_zh": "未找到邮箱地址。ATS 需要邮箱来关联你的申请和档案。",
            "suggestion_en": "Add your email address in the contact section at the top of the resume.",
            "suggestion_zh": "在简历顶部联系方式栏添加你的邮箱地址。",
            "evidence": [],
        })

    if not has_phone:
        issues.append({
            "check": "missing_phone",
            "severity": "medium",
            "detail_en": "No phone number found. While email is primary, some ATS systems also parse phone numbers.",
            "detail_zh": "未找到电话号码。虽然邮箱是主要的，但部分 ATS 也会解析电话。",
            "suggestion_en": "Consider adding a phone number in the contact section.",
            "suggestion_zh": "考虑在联系方式栏添加电话号码。",
            "evidence": [],
        })

    return issues


def check_date_consistency(text: str) -> list:
    """Detect inconsistent date formats across the resume."""
    issues = []

    # Detect date format patterns (from shared utils)
    used_formats = {}
    for fmt_name, pattern in DATE_FORMAT_PATTERNS.items():
        matches = re.findall(pattern, text)
        if matches:
            used_formats[fmt_name] = matches

    # Also check for "present/至今" markers
    ongoing_markers = re.findall(
        r"\b(?:Present|present|Current|current|至今|现在)\b", text
    )
    if ongoing_markers:
        used_formats["ongoing_marker"] = ongoing_markers

    if len(used_formats) > 2:
        format_names = ", ".join(used_formats.keys())
        # Collect examples
        examples = []
        for fmt, matches in used_formats.items():
            examples.extend(matches[:2])

        issues.append({
            "check": "date_inconsistency",
            "severity": "medium",
            "detail_en": f"Mixed date formats detected: {format_names}. Consistent formatting helps ATS parse dates correctly.",
            "detail_zh": f"检测到混合日期格式：{format_names}。统一格式有助于 ATS 正确解析日期。",
            "suggestion_en": "Standardize all dates to one format (e.g., 'MMM YYYY' or 'YYYY-MM').",
            "suggestion_zh": "将所有日期统一为一种格式（例如 'MMM YYYY' 或 'YYYY-MM'）。",
            "evidence": examples[:6],
        })

    return issues


def check_bullet_length(text: str) -> list:
    """Check if bullets exceed reasonable length for ATS parsing."""
    issues = []

    lines = text.split("\n")
    long_bullets = []

    for line in lines:
        stripped = line.strip()
        # Only check bullet lines
        if re.match(r"^[-\*\+•▸►→◆●]\s", stripped):
            char_count = len(stripped)
            # Rough estimate: > 250 chars ≈ 2+ lines in standard resume formatting
            if char_count > 250:
                long_bullets.append({
                    "text": stripped[:80] + "...",
                    "length": char_count,
                })

    if long_bullets:
        issues.append({
            "check": "long_bullets",
            "severity": "medium",
            "detail_en": f"Found {len(long_bullets)} bullet(s) exceeding ~250 characters. ATS may truncate long bullets.",
            "detail_zh": f"发现 {len(long_bullets)} 条超过 ~250 字符的 bullet。ATS 可能会截断过长的内容。",
            "suggestion_en": "Shorten long bullets. Each bullet should convey one key achievement in 1-2 lines.",
            "suggestion_zh": "缩短过长的 bullet。每条 bullet 应在 1-2 行内传达一个核心成果。",
            "evidence": [f"[{b['length']} chars] {b['text']}" for b in long_bullets[:3]],
        })

    return issues


def check_keywords(text: str, keywords: list) -> list:
    """Check if JD keywords appear in the resume text."""
    issues = []

    if not keywords:
        return issues

    text_lower = text.lower()
    missing_keywords = []

    for kw in keywords:
        kw_stripped = kw.strip()
        if not kw_stripped:
            continue
        # Check both exact match and word-boundary match
        kw_lower = kw_stripped.lower()
        if kw_lower not in text_lower:
            # Try word boundary match for multi-word keywords
            pattern = r"\b" + re.escape(kw_lower) + r"\b"
            if not re.search(pattern, text_lower):
                missing_keywords.append(kw_stripped)

    if missing_keywords:
        # Classify severity based on proportion missing
        missing_ratio = len(missing_keywords) / len(keywords)
        severity = "high" if missing_ratio > 0.5 else "medium"

        issues.append({
            "check": "missing_keywords",
            "severity": severity,
            "detail_en": f"{len(missing_keywords)}/{len(keywords)} JD keyword(s) not found in resume.",
            "detail_zh": f"简历中未找到 {len(missing_keywords)}/{len(keywords)} 个 JD 关键词。",
            "suggestion_en": (
                f"Consider naturally incorporating these keywords: {', '.join(missing_keywords[:5])}"
                + (f" and {len(missing_keywords) - 5} more" if len(missing_keywords) > 5 else "")
                + ". Place keywords in relevant context — do not simply list them."
            ),
            "suggestion_zh": (
                f"考虑自然地融入以下关键词：{', '.join(missing_keywords[:5])}"
                + (f" 等 {len(missing_keywords)} 个" if len(missing_keywords) > 5 else "")
                + "。将关键词放在相关上下文中，不要简单罗列。"
            ),
            "evidence": missing_keywords[:10],
        })

    return issues


def check_pii(text: str, profile: dict) -> list:
    """Check for region-specific forbidden PII."""
    issues = []
    forbidden = profile.get("forbidden_pii", [])

    if not forbidden:
        return issues

    for pii_type in forbidden:
        pii_info = PII_PATTERNS.get(pii_type)
        if not pii_info:
            continue

        matches = []
        for pattern in pii_info["patterns"]:
            found = re.findall(pattern, text, re.IGNORECASE)
            matches.extend(found)

        if matches:
            severity = "high" if profile.get("strict_format", False) else "medium"
            issues.append({
                "check": f"pii_{pii_type}",
                "severity": severity,
                "detail_en": f"Detected {pii_info['label']} information. This region's ATS/employers may flag or discriminate based on this.",
                "detail_zh": f"检测到{pii_info['label']}信息。该地区的 ATS/雇主可能会据此标记或歧视。",
                "suggestion_en": f"Remove {pii_info['label'].split('/')[0].strip()} information before submission.",
                "suggestion_zh": f"提交前移除{pii_info['label'].split('/')[1].strip() if '/' in pii_info['label'] else pii_info['label']}信息。",
                "evidence": list(set(matches))[:3],
            })

    return issues


def estimate_page_count(text: str) -> int:
    """Rough page count estimate based on character count."""
    # Average: ~3000 chars per page for a standard resume
    chars = len(text)
    return max(1, round(chars / 3000))


def check_page_length(text: str, profile: dict) -> list:
    """Check if resume exceeds region-specific page limit."""
    issues = []
    max_pages = profile.get("max_pages", 2)
    estimated = estimate_page_count(text)

    if estimated > max_pages:
        issues.append({
            "check": "page_length",
            "severity": "medium",
            "detail_en": (
                f"Resume is approximately {estimated} pages. "
                f"The target region recommends max {max_pages} page(s)."
            ),
            "detail_zh": (
                f"简历约 {estimated} 页。"
                f"目标地区建议不超过 {max_pages} 页。"
            ),
            "suggestion_en": f"Condense content to fit within {max_pages} page(s). Remove less relevant details.",
            "suggestion_zh": f"将内容精简至 {max_pages} 页以内。移除关联性较低的内容。",
            "evidence": [f"Estimated: {estimated} pages (based on {len(text)} characters)"],
        })

    return issues


# ---------------------------------------------------------------------------
# Main check runner
# ---------------------------------------------------------------------------

def run_checks(
    text: str,
    keywords: list = None,
    region: str = "global",
) -> dict:
    """
    Run all ATS checks on the resume text.
    Returns structured result dict.
    """
    profile = REGIONAL_PROFILES.get(region, REGIONAL_PROFILES["global"])

    all_issues = []

    # Run all checks
    all_issues.extend(check_tables(text))
    all_issues.extend(check_images(text))
    all_issues.extend(check_special_chars(text))
    all_issues.extend(check_sections(text, profile))
    all_issues.extend(check_contact_info(text))
    all_issues.extend(check_date_consistency(text))
    all_issues.extend(check_bullet_length(text))
    all_issues.extend(check_keywords(text, keywords or []))
    all_issues.extend(check_pii(text, profile))
    all_issues.extend(check_page_length(text, profile))

    # Calculate score
    total = len(all_issues)
    high_count = sum(1 for i in all_issues if i["severity"] == "high")
    med_count = sum(1 for i in all_issues if i["severity"] == "medium")
    low_count = sum(1 for i in all_issues if i["severity"] == "low")

    # Score: 100 - (high*10 + med*3 + low*1), floored at 0
    raw_score = 100 - (high_count * 10 + med_count * 3 + low_count * 1)
    score = max(0, min(100, raw_score))

    return {
        "score": score,
        "region": region,
        "region_profile": {
            "label": profile["label"],
            "label_zh": profile["label_zh"],
            "ats_systems": profile["ats_systems"],
            "max_pages": profile["max_pages"],
            "strict_format": profile["strict_format"],
        },
        "summary": {
            "total_issues": total,
            "high": high_count,
            "medium": med_count,
            "low": low_count,
        },
        "issues": all_issues,
    }


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

def format_markdown(result: dict, lang: str = "auto") -> str:
    """Format check results as a Markdown report."""
    is_zh = lang == "zh" or (lang == "auto" and detect_language(json.dumps(result)))

    score = result["score"]
    summary = result["summary"]
    region = result["region_profile"]
    issues = result["issues"]

    # Score badge
    if score >= 90:
        badge = "✅" if not is_zh else "✅"
    elif score >= 70:
        badge = "🟡" if not is_zh else "🟡"
    else:
        badge = "🔴" if not is_zh else "🔴"

    if is_zh:
        lines = [
            "# ATS 兼容性检查报告",
            "",
            f"**综合评分**: {badge} {score}/100",
            f"**目标地区**: {region['label_zh']}",
            f"**常见 ATS 系统**: {', '.join(region['ats_systems'])}",
            "",
            "## 问题汇总",
            "",
            "| 严重程度 | 数量 |",
            "|---------|------|",
            f"| 🔴 高风险 | {summary['high']} |",
            f"| 🟡 中风险 | {summary['medium']} |",
            f"| 🟢 低风险 | {summary['low']} |",
            f"| **合计** | **{summary['total_issues']}** |",
        ]
    else:
        lines = [
            "# ATS Compatibility Report",
            "",
            f"**Overall Score**: {badge} {score}/100",
            f"**Target Region**: {region['label']}",
            f"**Common ATS Systems**: {', '.join(region['ats_systems'])}",
            "",
            "## Issue Summary",
            "",
            "| Severity | Count |",
            "|----------|-------|",
            f"| 🔴 High | {summary['high']} |",
            f"| 🟡 Medium | {summary['medium']} |",
            f"| 🟢 Low | {summary['low']} |",
            f"| **Total** | **{summary['total_issues']}** |",
        ]

    # Detailed issues grouped by severity
    severity_order = ["high", "medium", "low"]
    severity_labels_zh = {"high": "🔴 高风险问题", "medium": "🟡 中风险问题", "low": "🟢 低风险问题"}
    severity_labels_en = {"high": "🔴 High Severity", "medium": "🟡 Medium Severity", "low": "🟢 Low Severity"}

    for severity in severity_order:
        severity_issues = [i for i in issues if i["severity"] == severity]
        if not severity_issues:
            continue

        if is_zh:
            lines.extend(["", f"## {severity_labels_zh[severity]}", ""])
        else:
            lines.extend(["", f"## {severity_labels_en[severity]}", ""])

        for idx, issue in enumerate(severity_issues, 1):
            detail = issue.get("detail_zh" if is_zh else "detail_en", "")
            suggestion = issue.get("suggestion_zh" if is_zh else "suggestion_en", "")

            lines.extend([
                f"### {idx}. {issue['check'].replace('_', ' ').title()}",
                "",
                f"- **问题**: {detail}" if is_zh else f"- **Issue**: {detail}",
                f"- **建议**: {suggestion}" if is_zh else f"- **Suggestion**: {suggestion}",
            ])

            if issue.get("evidence"):
                evidence_text = "\n".join(f"  - `{e}`" for e in issue["evidence"])
                lines.extend(["", "- **证据**:" if is_zh else "- **Evidence**:", evidence_text])

            lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="ATS Compatibility Checker")
    parser.add_argument("--resume", required=True, help="Path to resume file (Markdown or text)")
    parser.add_argument("--keywords", default="", help="Comma-separated JD keywords to check")
    parser.add_argument("--keywords-file", default="", help="Path to JSON file with keywords array")
    parser.add_argument("--region", default="global",
                        choices=list(REGIONAL_PROFILES.keys()),
                        help="Target region profile (default: global)")
    parser.add_argument("--lang", default="auto", choices=["auto", "zh", "en"],
                        help="Output language")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--output", default="", help="Output file path (default: stdout)")
    args = parser.parse_args()

    # Read resume
    try:
        with open(args.resume, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: Resume file not found: {args.resume}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

    # Parse keywords
    keywords = []
    if args.keywords:
        keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]
    elif args.keywords_file:
        try:
            with open(args.keywords_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    keywords = data
                elif isinstance(data, dict) and "keywords" in data:
                    keywords = data["keywords"]
        except Exception as e:
            print(f"Warning: Could not read keywords file: {e}", file=sys.stderr)

    # Run checks
    result = run_checks(text=text, keywords=keywords, region=args.region)

    # Output
    if args.json:
        output = json.dumps(result, ensure_ascii=False, indent=2)
    else:
        output = format_markdown(result, lang=args.lang)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"ATS report saved to {args.output}")
    else:
        try:
            print(output)
        except UnicodeEncodeError:
            print(output.encode("utf-8", errors="replace").decode("utf-8"))


if __name__ == "__main__":
    main()
