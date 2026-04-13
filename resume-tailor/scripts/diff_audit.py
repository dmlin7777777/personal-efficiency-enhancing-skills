"""
Diff Audit - Compare source and tailored resumes, generate change summary.

Usage:
    python diff_audit.py --master <source_md_path> --tailored <tailored_md_path>

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


def classify_change(diff_line: str) -> str:
    """Classify a diff line into a change type."""
    text = diff_line.lstrip("+-").strip()
    
    # Check for quantification (numbers added)
    if re.search(r"\d+", text) and diff_line.startswith("+"):
        if re.search(r"\d+[%号万元人]", text):
            return "quantification"
    
    # Check for wording upgrade
    upgrade_patterns = [
        (r"参与", "主导"), (r"协助", "负责"), (r"使用", "独立搭建"),
        (r"学习", "掌握"), (r"了解", "精通"), (r"负责", "主导"),
    ]
    for old_word, new_word in upgrade_patterns:
        if new_word in text and diff_line.startswith("+"):
            return "wording_upgrade"
    
    return "content_change"


def generate_audit(master_path: str, tailored_path: str, company: str = "", role: str = "", jd_source: str = "", source_name: str = "source resume") -> str:
    """Generate a full audit log comparing source and tailored resumes."""

    source_lines = read_lines(master_path)
    tailored_lines = read_lines(tailored_path)

    # Generate unified diff
    diff = list(difflib.unified_diff(
        source_lines, tailored_lines,
        fromfile="source", tofile="tailored",
        lineterm=""
    ))

    # Categorize changes
    additions = []
    deletions = []
    modifications = []

    i = 0
    while i < len(diff):
        line = diff[i]
        if line.startswith("---") or line.startswith("+++"):
            i += 1
            continue
        if line.startswith("@@"):
            i += 1
            continue

        if line.startswith("+"):
            # Check if next line is a deletion (modification pair)
            if i + 1 < len(diff) and diff[i + 1].startswith("-"):
                change_type = classify_change(line)
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

    # Count keywords for match summary (placeholder - would need JD parser output)
    # This is a simplified version; in practice, combine with jd_parser.py output

    # Build audit report
    now = datetime.now().strftime("%Y-%m-%d")
    report_lines = [
        f"# 简历变更审计",
        f"",
        f"- **日期**: {now}",
    ]
    
    if company:
        report_lines.append(f"- **目标岗位**: {company}" + (f" - {role}" if role else ""))
    if jd_source:
        report_lines.append(f"- **JD 来源**: {jd_source}")
    
    report_lines.extend([
        f"- **基于版本**: {source_name}",
        f"",
        f"## 变更统计",
        f"",
        f"| 类型 | 数量 |",
        f"|------|------|",
        f"| 新增内容 | {len(addments)} |",
        f"| 删除内容 | {len(deletions)} |",
        f"| 修改内容 | {len(modifications)} |",
    ])

    # Type breakdown for modifications
    type_counts = {}
    for mod in modifications:
        t = mod["type"]
        type_counts[t] = type_counts.get(t, 0) + 1

    type_labels = {
        "wording_upgrade": "措辞升级",
        "quantification": "量化补充",
        "content_change": "内容变更",
    }
    for t, count in type_counts.items():
        label = type_labels.get(t, t)
        report_lines.append(f"| ↳ {label} | {count} |")

    # Detailed changes
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
                ""
            ])

    return "\n".join(report_lines)


def main():
    parser = argparse.ArgumentParser(description="Resume Diff Audit")
    parser.add_argument("--master", help="Path to source resume (Markdown)")
    parser.add_argument("--tailored", help="Path to tailored resume (Markdown)")
    parser.add_argument("--company", default="", help="Target company name")
    parser.add_argument("--role", default="", help="Target role name")
    parser.add_argument("--jd-source", default="", help="JD URL or source description")
    parser.add_argument("--source-name", default="source resume", help="Display name of the source resume file")
    parser.add_argument("--output", default="", help="Output file path (default: stdout)")
    args = parser.parse_args()

    report = generate_audit(args.master, args.tailored, args.company, args.role, args.jd_source, args.source_name)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Audit log saved to {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
