"""
JD Parser - Extract and categorize keywords from a job description.

Usage:
    python jd_parser.py "<jd_text>"
    python jd_parser.py --file path/to/jd.txt

Output:
    JSON with categorized keywords and priorities.
"""

import re
import json
import sys
import argparse
from collections import defaultdict


# Keyword categories with patterns
HARD_SKILLS_PATTERNS = {
    "programming": [
        "Python", "Java", "SQL",
        "JavaScript", "TypeScript",
        "Scala",
        "Spark", "Hadoop", "HDFS", "Hive",
        "TensorFlow", "PyTorch", "scikit-learn",
    ],
    "tools": [
        "Excel", "Power BI", "Tableau",
        "SAS", "SPSS", "Git", "Docker",
        "Kubernetes", "Jira", "Confluence",
        "Figma", "Axure", "Copilot Studio",
        "Power Apps", "Power Automate",
        "RPA", "Selenium",
    ],
    "databases": [
        "MySQL", "PostgreSQL", "MongoDB", "Redis",
        "Oracle", "SQL Server", "BigQuery",
    ],
    "marketing_ad": [
        "oCPX", "oCPC", "oCPM", "oCPA", "CTR", "CVR",
        "ROI", "ROAS", "GMV", "DAU", "MAU", "ARPU",
        "LTV", "CAC",
        "A/B测试", "A/B test", "A/B Testing",
        "DMP", "DSP", "SSP", "ADX",
        "SEM", "SEO", "ASM",
        "程序化广告", "信息流", "竞价", "出价", "定向", "人群包", "素材", "创意",
    ],
    "data_analysis": [
        "数据分析", "数据建模", "数据治理",
        "机器学习", "深度学习", "NLP",
        "ETL", "数据仓库", "数据湖",
        "漏斗分析", "归因分析", "用户画像",
        "埋点", "指标体系",
        "Prophet", "LightGBM", "XGBoost",
    ],
}

SOFT_SKILLS_PATTERNS = {
    "leadership": [
        "主导", r"带领?", "管理", "领导",
        r"(?<!\w)leader(?!\w)", r"(?<!\w)manage(?!\w)", r"(?<!\w)lead(?!\w)",
        "团队协作", "跨团队", "沟通能力",
        r"推动?", "协调",
        "项目管理", r"(?<!\w)PM(?!\w)",
    ],
    "problem_solving": [
        "分析", "优化", "解决问题",
        "逻辑思维", "批判性思维",
        r"analytical", r"problem.?solving",
    ],
    "communication": [
        "沟通", "表达", "汇报", "演示",
        r"presentation", r"communication",
        "客户沟通", "商务沟通",
    ],
    "initiative": [
        "主动性", "自驱", r"(?<!\w)owner(?!\w)", "主人翁",
        "主动", r"proactive", r"self.?driven",
    ],
}

DOMAIN_PATTERNS = {
    "advertising": [
        "广告", "营销", "投放", "品牌", "效果广告",
        r"advertising", r"marketing", r"campaign", r"brand",
        "媒体", "流量", "转化",
    ],
    "finance": [
        "金融", "财务", "审计", "会计", "风控", "信贷",
        r"finance", r"accounting", r"audit", r"risk",
        "资金", "结算", "合规",
    ],
    "tech_platform": [
        "互联网", "平台", "产品", "运营", "用户增长",
        r"internet", r"platform", r"product", r"operation",
        r"SaaS", r"B2B", r"B2C",
    ],
    "energy_sustainability": [
        "新能源", "碳中和", "可持续发展", "绿电",
        r"energy", r"sustainability", r"carbon",
    ],
}

EXPERIENCE_PATTERNS = [
    (r"(\d+)\s*年\s*以上?", "years"),
    (r"(\d+)\+?\s*年\s*(?:以上|经验|工作)?", "years"),
    (r"(?:硕士|博士|本科|学士|研究生|master|phd|bachelor)", "degree"),
    (r"(?:英语|CET|IELTS|TOEFL|英文)", "language"),
]


def extract_keywords(text: str) -> dict:
    """Extract and categorize keywords from JD text."""

    result = {
        "hard_skills": defaultdict(list),
        "soft_skills": defaultdict(list),
        "domain": defaultdict(list),
        "experience": [],
        "raw_keywords": [],
    }

    text_lower = text.lower()

    # Extract hard skills
    for category, patterns in HARD_SKILLS_PATTERNS.items():
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for m in matches:
                keyword = m.strip()
                if keyword and keyword not in result["hard_skills"][category]:
                    result["hard_skills"][category].append(keyword)

    # Extract soft skills
    for category, patterns in SOFT_SKILLS_PATTERNS.items():
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for m in matches:
                keyword = m.strip()
                if keyword and keyword not in result["soft_skills"][category]:
                    result["soft_skills"][category].append(keyword)

    # Extract domain keywords
    for category, patterns in DOMAIN_PATTERNS.items():
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for m in matches:
                keyword = m.strip()
                if keyword and keyword not in result["domain"][category]:
                    result["domain"][category].append(keyword)

    # Extract experience requirements
    for pattern, exp_type in EXPERIENCE_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for m in matches:
                value = m if isinstance(m, str) else m[0] if m else ""
                result["experience"].append({"type": exp_type, "value": value.strip()})

    # Deduplicate experience
    seen = set()
    deduped = []
    for exp in result["experience"]:
        key = f"{exp['type']}:{exp['value']}"
        if key not in seen:
            seen.add(key)
            deduped.append(exp)
    result["experience"] = deduped

    # Flatten all keywords for easy reference
    all_keywords = set()
    for cat in result["hard_skills"].values():
        all_keywords.update(cat)
    for cat in result["soft_skills"].values():
        all_keywords.update(cat)
    for cat in result["domain"].values():
        all_keywords.update(cat)
    result["raw_keywords"] = sorted(list(all_keywords))

    return result


def print_report(analysis: dict):
    """Print a human-readable analysis report."""

    print("=" * 60)
    print("JD 关键词分析报告")
    print("=" * 60)

    print("\n## 硬技能 (Hard Skills)")
    for category, keywords in analysis["hard_skills"].items():
        if keywords:
            print(f"  {category}: {', '.join(keywords)}")

    print("\n## 软技能 (Soft Skills)")
    for category, keywords in analysis["soft_skills"].items():
        if keywords:
            print(f"  {category}: {', '.join(keywords)}")

    print("\n## 行业领域 (Domain)")
    for category, keywords in analysis["domain"].items():
        if keywords:
            print(f"  {category}: {', '.join(keywords)}")

    print("\n## 经验要求 (Experience)")
    for exp in analysis["experience"]:
        print(f"  {exp['type']}: {exp['value']}")

    total = len(analysis["raw_keywords"])
    print(f"\n## 关键词总数: {total}")
    print(f"## 全部关键词: {', '.join(analysis['raw_keywords'])}")

    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(description="JD Keyword Parser")
    parser.add_argument("input", help="JD text or --file path")
    parser.add_argument("--file", action="store_true", help="Read from file")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    if args.file:
        with open(args.input, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = args.input

    analysis = extract_keywords(text)

    if args.json:
        # Convert defaultdict to dict for JSON serialization
        output = {
            "hard_skills": dict(analysis["hard_skills"]),
            "soft_skills": dict(analysis["soft_skills"]),
            "domain": dict(analysis["domain"]),
            "experience": analysis["experience"],
            "raw_keywords": analysis["raw_keywords"],
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print_report(analysis)


if __name__ == "__main__":
    main()
