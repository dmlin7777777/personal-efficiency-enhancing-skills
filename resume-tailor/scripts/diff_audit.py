"""
Diff Audit - Compare source and tailored resumes, generate change summary.

Uses heuristic signals instead of hardcoded word lists,
making it language-agnostic and role-agnostic.

Usage:
    python diff_audit.py --source <source_md_path> --tailored <tailored_md_path>

Output:
    Markdown audit log with categorized changes.
"""

import difflib
import re
import sys
import argparse
from datetime import datetime


def read_lines(path: str) -> list:
    """Read file and return list of non-empty lines."""
    with open(path, "r", encoding="utf-8") as f:
        return [line.rstrip() for line in f if line.strip()]


def has_numbers(text: str) -> bool:
    """Check if text contains any numeric value."""
    return bool(re.search(r"\d+", text))


def word_overlap_ratio(text_a: str, text_b: str) -> float:
    """Calculate how much of text_a's words appear in text_b (0.0 ~ 1.0)."""
    words_a = set(re.findall(r"\S+", text_a.lower()))
    words_b = set(re.findall(r"\S+", text_b.lower()))
    if not words_a:
        return 0.0
    return len(words_a & words_b) / len(words_a)


def is_expanded_version(shorter: str, longer: str) -> bool:
    """
    Check if 'longer' is an expanded version of 'shorter'.
    This signals a wording upgrade: same core content, but with added
    modifiers, results, or stronger verbs.
    """
    # Longer text should contain most of shorter's words
    overlap = word_overlap_ratio(shorter, longer)
    # And longer should be noticeably longer
    if len(longer) < len(shorter) * 1.2:
        return False
    return overlap >= 0.4


def classify_change(removed_text: str, added_text: str) -> str:
    """
    Classify a change pair using heuristic signals.

    No hardcoded word lists — uses structural signals that work
    across languages and industries.

    Returns one of:
        - "quantification": Numbers/metrics were added
        - "wording_upgrade": Same content, stronger expression
        - "content_change": Fundamentally different content
    """

    # Signal 1: Quantification — new numbers added where there were none
    added_has_numbers = has_numbers(added_text)
    removed_has_numbers = has_numbers(removed_text)
    if added_has_numbers and not removed_has_numbers:
        return "quantification"

    # Signal 2: Wording upgrade — added text is an expanded version of removed
    if is_expanded_version(removed_text, added_text):
        return "wording_upgrade"

    # Signal 3: Check if they share significant content (modification vs replacement)
    overlap = word_overlap_ratio(removed_text, added_text)
    if overlap >= 0.5:
        # High overlap but didn't trigger upgrade — still a modification
        return "wording_upgrade"

    # Default: fundamentally different content
    return "content_change"


def detect_language(text: str) -> str:
    """Auto-detect if text is primarily Chinese or English."""
    chinese_chars = len(re.findall(r"[\u4e00-\u9fff]", text))
    english_words = len(re.findall(r"[a-zA-Z]+", text))
    return "zh" if chinese_chars > english_words else "en"


def generate_audit(
    source_path: str,
    tailored_path: str,
    company: str = "",
    role: str = "",
    jd_source: str = "",
    source_name: str = "source resume",
    output_lang: str = "auto",
) -> str:
    """Generate a full audit log comparing source and tailored resumes."""

    source_lines = read_lines(source_path)
    tailored_lines = read_lines(tailored_path)

    # Generate unified diff
    diff = list(difflib.unified_diff(
        source_lines, tailored_lines,
        fromfile="source", tofile="tailored",
        lineterm=""
    ))

    # Auto-detect language
    if output_lang == "auto":
        full_text = "\n".join(source_lines + tailored_lines)
        output_lang = detect_language(full_text)

    # Categorize changes
    additions = []
    deletions = []
    modifications = []

    i = 0
    while i < len(diff):
        line = diff[i]
        if line.startswith("---") or line.startswith("+++") or line.startswith("@@"):
            i += 1
            continue

        if line.startswith("+"):
            # Check if next line is a deletion (modification pair)
            if i + 1 < len(diff) and diff[i + 1].startswith("-"):
                change_type = classify_change(
                    diff[i + 1].lstrip("- "),
                    line.lstrip("+ "),
                )
                modifications.append({
                    "added": line.lstrip("+ "),
                    "removed": diff[i + 1].lstrip("- "),
                    "type": change_type,
                })
                i += 2
            else:
                additions.append(line.lstrip("+ "))
                i += 1
        elif line.startswith("-"):
            deletions.append(line.lstrip("- "))
            i += 1
        else:
            i += 1

    # Build audit report
    now = datetime.now().strftime("%Y-%m-%d")
    is_zh = output_lang == "zh"

    if is_zh:
        report_lines = [
            f"# 简历变更审计 / Resume Change Audit",
            f"",
            f"- **日期 / Date**: {now}",
        ]
        if company:
            label = f"- **目标岗位 / Target**: {company}"
            if role:
                label += f" - {role}"
            report_lines.append(label)
        if jd_source:
            report_lines.append(f"- **JD 来源 / JD Source**: {jd_source}")
        report_lines.append(f"- **基于版本 / Based on**: {source_name}")

        report_lines.extend([
            f"",
            f"## 变更统计 / Change Summary",
            f"",
            f"| 类型 / Type | 数量 / Count |",
            f"|------|------|",
            f"| 新增内容 / Added | {len(additions)} |",
            f"| 删除内容 / Removed | {len(deletions)} |",
            f"| 修改内容 / Modified | {len(modifications)} |",
        ])

        type_labels = {
            "wording_upgrade": "措辞升级 / Wording Upgrade",
            "quantification": "量化补充 / Quantification",
            "content_change": "内容变更 / Content Change",
        }
    else:
        report_lines = [
            f"# Resume Change Audit",
            f"",
            f"- **Date**: {now}",
        ]
        if company:
            label = f"- **Target**: {company}"
            if role:
                label += f" - {role}"
            report_lines.append(label)
        if jd_source:
            report_lines.append(f"- **JD Source**: {jd_source}")
        report_lines.append(f"- **Based on**: {source_name}")

        report_lines.extend([
            f"",
            f"## Change Summary",
            f"",
            f"| Type | Count |",
            f"|------|------|",
            f"| Added | {len(additions)} |",
            f"| Removed | {len(deletions)} |",
            f"| Modified | {len(modifications)} |",
        ])

        type_labels = {
            "wording_upgrade": "Wording Upgrade",
            "quantification": "Quantification",
            "content_change": "Content Change",
        }

    # Type breakdown
    type_counts = {}
    for mod in modifications:
        t = mod["type"]
        type_counts[t] = type_counts.get(t, 0) + 1

    for t, count in type_counts.items():
        label = type_labels.get(t, t)
        report_lines.append(f"| ↳ {label} | {count} |")

    # Detailed changes
    if is_zh:
        if additions:
            report_lines.extend(["", "## 新增内容", ""])
            for idx, add in enumerate(additions, 1):
                report_lines.append(f"{idx}. {add}")

        if deletions:
            report_lines.extend(["", "## 删除内容", ""])
            for idx, dlt in enumerate(deletions, 1):
                report_lines.append(f"{idx}. {dlt}")

        if modifications:
            report_lines.extend(["", "## 修改内容", ""])
            for idx, mod in enumerate(modifications, 1):
                type_label = type_labels.get(mod["type"], mod["type"])
                report_lines.extend([
                    f"### {idx}. [{type_label}]",
                    f"- **删除**: {mod['removed']}",
                    f"- **新增**: {mod['added']}",
                    "",
                ])
    else:
        if additions:
            report_lines.extend(["", "## Added Content", ""])
            for idx, add in enumerate(additions, 1):
                report_lines.append(f"{idx}. {add}")

        if deletions:
            report_lines.extend(["", "## Removed Content", ""])
            for idx, dlt in enumerate(deletions, 1):
                report_lines.append(f"{idx}. {dlt}")

        if modifications:
            report_lines.extend(["", "## Modified Content", ""])
            for idx, mod in enumerate(modifications, 1):
                type_label = type_labels.get(mod["type"], mod["type"])
                report_lines.extend([
                    f"### {idx}. [{type_label}]",
                    f"- **Removed**: {mod['removed']}",
                    f"- **Added**: {mod['added']}",
                    "",
                ])

    return "\n".join(report_lines)


def main():
    parser = argparse.ArgumentParser(description="Resume Diff Audit")
    parser.add_argument("--source", help="Path to source resume (Markdown)")
    parser.add_argument("--tailored", help="Path to tailored resume (Markdown)")
    parser.add_argument("--company", default="", help="Target company name")
    parser.add_argument("--role", default="", help="Target role name")
    parser.add_argument("--jd-source", default="", help="JD URL or source description")
    parser.add_argument("--source-name", default="source resume", help="Display name of the source resume file")
    parser.add_argument("--lang", default="auto", choices=["auto", "zh", "en"], help="Output language (auto-detect by default)")
    parser.add_argument("--output", default="", help="Output file path (default: stdout)")
    args = parser.parse_args()

    report = generate_audit(
        args.source, args.tailored,
        args.company, args.role, args.jd_source, args.source_name,
        args.lang,
    )

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Audit log saved to {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
