"""
JD Parser - Extract and categorize keywords from a job description.

Uses heuristic rules instead of hardcoded word lists, making it
language-agnostic and role-agnostic.

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


# ─── Universal patterns (language-agnostic) ─────────────────────

# Experience / seniority — works for both Chinese and English
EXPERIENCE_RULES = [
    # English: "3+ years", "5 years of experience", "3-5 years"
    (r"(\d+)\s*[-–~到至]\s*(\d+)\s*\+?\s*(?:years?|yrs?|年)", "years_range"),
    (r"(\d+)\s*\+?\s*(?:years?\s*(?:of\s+)?experience|年(?:以上)?(?:工作)?(?:经验)?)", "years_min"),
    (r"(?:fresh\s*grad|entry\s*level|应届|初级|入门)", "entry_level"),
    (r"(?:senior|staff|principal|高级|资深)", "senior_level"),
    (r"(?:mid[- ]?level|中级)", "mid_level"),
]

# Degree / education
DEGREE_RULES = [
    (r"(?:Ph\.?D|Doctorate|博士)", "PhD"),
    (r"(?:Master|M\.?S\.?|MSc|MBA|硕士|研究生)", "Master"),
    (r"(?:Bachelor|B\.?S\.?|BSc|BA|本科|学士)", "Bachelor"),
    (r"(?:Associate| diploma|大专|专科|副学士)", "Associate"),
]

# Language requirements
LANGUAGE_RULES = [
    (r"(?:IELTS|雅思)\s*[:：]?\s*(\d+(?:\.\d+)?)", "IELTS"),
    (r"(?:TOEFL|托福)\s*[:：]?\s*(\d+)", "TOEFL"),
    (r"(?:CET[- ]?(4|6)|英语四六级)\s*[:：]?\s*(?::?\s*(\d+)?)?", "CET"),
    (r"(?:fluent|proficient|native|business)\s+(?:in\s+)?(?:English|Chinese|Japanese|Korean|French|German|Spanish|Mandarin|Cantonese|English|中文|日语|韩语|法语|德语|西班牙语)", "language"),
    (r"(?:English|英文|英语)\s*(?:as\s+working\s+language|working\s+proficiency|流利|熟练|精通)", "language"),
]


def extract_experience(text: str) -> list:
    """Extract experience and education requirements."""
    results = []
    seen = set()

    for pattern, label in EXPERIENCE_RULES + DEGREE_RULES + LANGUAGE_RULES:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = match.group(0).strip()
            key = f"{label}:{value}"
            if key not in seen:
                seen.add(key)
                results.append({"type": label, "value": value})

    return results


def extract_tech_keywords(text: str) -> list:
    """
    Extract technical/skill keywords using heuristic signals.

    Strategy: look for known technical term patterns that are universal
    across languages and domains, rather than maintaining a hardcoded list.
    """
    keywords = []
    seen = set()

    # Pattern 1: CamelCase or PascalCase terms (e.g., Power BI, Tableau, TensorFlow)
    camel_matches = re.findall(r"\b(?:[A-Z][a-z0-9]+(?:\s+[A-Z][a-z0-9]+)*)\b", text)
    for m in camel_matches:
        m = m.strip()
        # Filter out common English words that happen to be capitalized
        common_words = {"The", "This", "That", "With", "From", "Have", "Will",
                        "Must", "Can", "Our", "You", "Your", "We", "All",
                        "Not", "But", "For", "Are", "Was", "Were", "Been",
                        "Being", "Each", "Which", "Their", "There", "These",
                        "Those", "What", "When", "Where", "Who", "How",
                        "Work", "Team", "Role", "Job", "Time", "Make",
                        "Good", "Great", "Best", "Strong", "High", "New"}
        if m not in common_words and len(m) > 2 and m not in seen:
            seen.add(m)
            keywords.append(m)

    # Pattern 2: Terms in parentheses or after colons (often skill lists)
    paren_matches = re.findall(r"[\(（]([^)）]+)[\)）]", text)
    for group in paren_matches:
        # Split by commas, slashes, or Chinese enumeration commas
        items = re.split(r"[,，、/／;；]", group)
        for item in items:
            item = item.strip()
            if 2 < len(item) < 40 and item not in seen:
                seen.add(item)
                keywords.append(item)

    # Pattern 3: Known universal abbreviation patterns (e.g., SQL, API, AI, ML, NLP)
    abbrev_matches = re.findall(r"\b(?:[A-Z]{2,6}|[A-Z][a-z]\.[A-Z]\.[a-z]?)\b", text)
    for m in abbrev_matches:
        m = m.strip()
        # Filter very common non-skill abbreviations
        skip = {"JD", "CV", "PM", "HR", "CEO", "CTO", "CFO", "COO", "VP", "FAQ",
                "DNA", "NOTE", "TBD", "ETA", "ASAP", "N/A", "TBA", "AKA",
                "VPN", "WiFi", "HTTP", "URL", "PDF", "GUI"}
        if m not in skip and m not in seen:
            seen.add(m)
            keywords.append(m)

    # Pattern 4: Quoted terms (often emphasis on specific skills/tools)
    quote_matches = re.findall(r'[""「」『』]([^""「」『』]+)[""「」『』]', text)
    for m in quote_matches:
        m = m.strip()
        if 2 < len(m) < 40 and m not in seen:
            seen.add(m)
            keywords.append(m)

    # Pattern 5: Programming languages, frameworks, and tools (common suffixes)
    # These are universal patterns that work across any tech JD
    tech_suffixes = [
        r"\b(?:JavaScript|TypeScript|Python|Java|Ruby|Go|Rust|Swift|Kotlin|C\+\+|C#|PHP|Scala|R|MATLAB|Julia)\b",
        r"\b\w+\.js\b",  # React.js, Vue.js, Node.js, etc.
        r"\b(?:TensorFlow|PyTorch|scikit-learn|Keras|OpenCV|Pandas|NumPy|Spark|Hadoop|Hive|Kafka|Flink|Airflow|Docker|Kubernetes|Jenkins|Git)\b",
    ]
    for pattern in tech_suffixes:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for m in matches:
            m = m.strip()
            if m not in seen:
                seen.add(m)
                keywords.append(m)

    return keywords


def extract_action_verbs(text: str) -> list:
    """
    Extract action verbs / responsibility indicators from JD.
    These signal what the candidate is expected to DO.
    """
    # Universal action verb patterns (work for both EN and ZH)
    action_patterns = [
        # English action verbs commonly used in JDs
        r"\b(?:design|develop|build|create|implement|deploy|manage|lead|drive|optimize|analyze|monitor|maintain|support|collaborate|coordinate|deliver|architect|configure|automate|integrate|migrate|troubleshoot|debug|test|review|evaluate|assess|improve|enhance|establish|streamline|scale)\w*\b",
        # Chinese action verbs
        r"[\u4e00-\u9fff]*(?:主导|负责|搭建|设计|开发|构建|部署|管理|带领|推动|优化|分析|监控|维护|支持|协作|协调|交付|架构|配置|自动化|集成|迁移|排查|测试|评审|评估|改进|提升|建立|简化|扩展)[\u4e00-\u9fff]*",
    ]

    verbs = []
    seen = set()
    for pattern in action_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for m in matches:
            m = m.strip()
            if m and len(m) <= 20 and m not in seen:
                seen.add(m)
                verbs.append(m)

    return verbs


def extract_metrics_keywords(text: str) -> list:
    """
    Extract business metric terms from JD (KPIs the role is measured by).
    """
    metrics = []
    seen = set()

    # Universal metric patterns
    metric_patterns = [
        # English metric abbreviations
        r"\b(?:ROI|ROAS|GMV|DAU|MAU|ARPU|LTV|CAC|CTR|CVR|CPA|CPC|CPM|NPS|CSAT|MRR|ARR|Churn|Retention|Conversion|Engagement)\b",
        # Chinese metric terms
        r"(?:转化率|点击率|留存率|复购率|满意度|活跃度|增长率|毛利率|净利率|市场份额|用户增长|收入增长)",
        # "X% improvement" patterns
        r"\d+\s*%?\s*(?:increase|decrease|improvement|reduction|growth|提升|降低|增长|减少)",
        # "by X%" patterns
        r"(?:by|达到|提升至|降低至)\s*\d+\s*%",
    ]

    for pattern in metric_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for m in matches:
            m = m.strip()
            if m and m not in seen:
                seen.add(m)
                metrics.append(m)

    return metrics


def extract_keywords(text: str) -> dict:
    """Extract and categorize keywords from JD text using heuristic rules."""

    tech = extract_tech_keywords(text)
    actions = extract_action_verbs(text)
    metrics = extract_metrics_keywords(text)
    experience = extract_experience(text)

    # Auto-detect language
    chinese_chars = len(re.findall(r"[\u4e00-\u9fff]", text))
    english_words = len(re.findall(r"[a-zA-Z]+", text))
    lang = "zh" if chinese_chars > english_words else "en"

    result = {
        "language": lang,
        "tech_keywords": tech,
        "action_verbs": actions,
        "business_metrics": metrics,
        "requirements": experience,
        "all_keywords": sorted(list(set(tech + actions + metrics + [e["value"] for e in experience]))),
    }

    return result


def print_report(analysis: dict):
    """Print a human-readable analysis report."""
    lang = analysis.get("language", "en")
    is_zh = lang == "zh"

    sep = "=" * 60
    title = "JD 关键词分析报告" if is_zh else "JD Keyword Analysis Report"
    print(sep)
    print(title)
    print(sep)

    # Tech keywords
    tech_label = "技术关键词" if is_zh else "Tech Keywords"
    print(f"\n## {tech_label}")
    print(f"  {', '.join(analysis['tech_keywords']) if analysis['tech_keywords'] else '—'}")

    # Action verbs
    action_label = "行为动词 (Action Verbs)" if is_zh else "Action Verbs"
    print(f"\n## {action_label}")
    print(f"  {', '.join(analysis['action_verbs']) if analysis['action_verbs'] else '—'}")

    # Business metrics
    metric_label = "业务指标" if is_zh else "Business Metrics"
    print(f"\n## {metric_label}")
    print(f"  {', '.join(analysis['business_metrics']) if analysis['business_metrics'] else '—'}")

    # Requirements
    req_label = "岗位要求" if is_zh else "Requirements"
    print(f"\n## {req_label}")
    for req in analysis["requirements"]:
        print(f"  [{req['type']}] {req['value']}")

    # Summary
    total_label = "关键词总数" if is_zh else "Total Keywords"
    all_label = "全部关键词" if is_zh else "All Keywords"
    print(f"\n## {total_label}: {len(analysis['all_keywords'])}")
    print(f"## {all_label}: {', '.join(analysis['all_keywords'])}")
    print(f"\n{sep}")


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
        print(json.dumps(analysis, ensure_ascii=False, indent=2))
    else:
        print_report(analysis)


if __name__ == "__main__":
    main()
