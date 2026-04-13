"""
Resume Tailor — Shared Utilities (v2)

Common functions and patterns used across jd_parser.py, ats_checker.py, and diff_audit.py.
Keeps the codebase DRY without over-abstracting.
"""

import re


# ─── Language Detection ─────────────

def detect_language(text: str) -> str:
    """
    Auto-detect if text is primarily Chinese or English.
    Returns 'zh' or 'en'.
    """
    chinese_chars = len(re.findall(r"[\u4e00-\u9fff]", text))
    english_words = len(re.findall(r"[a-zA-Z]+", text))
    return "zh" if chinese_chars > english_words else "en"


# ─── PII Detection Patterns ─────────────
# Shared between ats_checker.py (script-level) and SKILL.md Phase 5b (LLM-level reference)

PII_PATTERNS = {
    "photo": {
        "label": "Photo / 头像照片",
        "patterns": [
            r"!\[.*?\]\(.*?\.(?:png|jpe?g|gif|webp|bmp)",
            r"<img\b",
            r"(?:头像|照片|profile\s*photo|passport\s*photo)\s*[:：]?\s*\S+",
        ],
    },
    "age": {
        "label": "Age / 年龄",
        "patterns": [
            r"\b(?:age|年龄)\s*[:：]?\s*\d{1,2}\s*(?:years?\s*old|岁)?\b",
            r"\b\d{1,2}\s*(?:years?\s*old|岁)\b",
            r"\b(?:born|出生(?:日期|年月)?)\s*(?:in|on|于)\s*[\d/.\-]+\b",
            r"\bDOB\s*[:：]\s*[\d/.\-]+\b",
            r"\d{4}\s*[-/年]\s*\d{1,2}\s*[-/月]\s*\d{1,2}\s*日?",
        ],
    },
    "gender": {
        "label": "Gender / 性别",
        "patterns": [
            r"\b(?:gender|sex|性别)\s*[:：]?\s*(?:male|female|M|F|男|女|♂|♀)\b",
        ],
    },
    "marital_status": {
        "label": "Marital Status / 婚姻状况",
        "patterns": [
            r"\b(?:marital\s*status|婚姻(?:状况|状态)?)\s*[:：]?\s*\w+",
            r"\b(?:married|single|divorced|widowed|separated|已婚|未婚|离异|丧偶)\b",
        ],
    },
    "religion": {
        "label": "Religion / 宗教信仰",
        "patterns": [
            r"\b(?:religion|religious|宗教|信仰)\s*[:：]?\s*\w+",
            r"\b(?:Christian|Muslim|Buddhist|Hindu|Jewish|Sikh|Taoist|Catholic|Protestant|Orthodox)\b",
            r"\b(?:基督教|伊斯兰教|佛教|印度教|犹太教|锡克教|道教|天主教|新教|东正教)\b",
        ],
    },
    "nationality": {
        "label": "Nationality / 国籍",
        "patterns": [
            r"\b(?:nationality|国籍)\s*[:：]?\s*\w+",
        ],
    },
    "salary_history": {
        "label": "Salary History / 薪资历史",
        "patterns": [
            r"\b(?:current\s*salary|expected\s*salary|薪资?|年薪|月薪|薪酬)\s*[:：]?\s*[\d,\$¥€£]+",
            r"\b(?:salary\s*(?:history|range|expectation))\s*[:：]",
        ],
    },
    "full_address": {
        "label": "Full Address / 详细住址",
        "patterns": [
            r"\d{1,5}\s+[\w\s]+(?:Street|St|Avenue|Ave|Boulevard|Blvd|Road|Rd|Lane|Ln|Drive|Dr)\b",
            r"(?:号|弄|栋|室|单元)\s*$",
        ],
    },
    "national_insurance": {
        "label": "National Insurance Number / 国民保险号",
        "patterns": [
            r"\bNI\s*(?:number|no\.?|num)?\s*[:：]?\s*[A-Z]{2}\s*\d{6}\s*[A-Z]",
            r"\b(?:National\s*Insurance|国民保险)\s*(?:Number|No\.?|号码)?\s*[:：]",
        ],
    },
    "political_affiliation": {
        "label": "Political Affiliation / 政治倾向",
        "patterns": [
            r"\b(?:political\s*(?:affiliation|party|view)|政治(?:面貌|倾向|立场))\s*[:：]?\s*\w+",
            r"\b(?:Democrat|Republican|Labour|Conservative|Liberal|Green)\s+Party\b",
            r"\b(?:党员|团员|民主党派)\b",
        ],
    },
}


# ─── Date Format Patterns ─────────────
# Shared between jd_parser.py (date range extraction) and ats_checker.py (date consistency check)

DATE_FORMAT_PATTERNS = {
    "YYYY-MM": r"\b\d{4}[-/]\d{1,2}\b",
    "YYYY.MM": r"\b\d{4}\.\d{1,2}\b",
    "MMM YYYY": (
        r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
        r"[a-z]*\.?\s+\d{4}\b"
    ),
    "MM/YYYY": r"\b\d{1,2}/\d{4}\b",
    "YYYY年M月": r"\b\d{4}\s*年\s*\d{1,2}\s*月\b",
}


# ─── Portfolio & Link Detection ─────────────
# Used by jd_parser.py for script-level portfolio scanning

LINK_PATTERNS = {
    "github": r"(?:https?://)?(?:www\.)?github\.com/[a-zA-Z0-9\-_/]+",
    "gitlab": r"(?:https?://)?(?:www\.)?gitlab\.com/[a-zA-Z0-9\-_/]+",
    "behance": r"(?:https?://)?(?:www\.)?behance\.net/[a-zA-Z0-9\-_]+",
    "dribbble": r"(?:https?://)?(?:www\.)?dribbble\.com/[a-zA-Z0-9\-_]+",
    "kaggle": r"(?:https?://)?(?:www\.)?kaggle\.com/[a-zA-Z0-9\-_]+",
    "linkedin": r"(?:https?://)?(?:www\.)?linkedin\.com/in/[a-zA-Z0-9\-_%]+",
    "scholar": r"(?:https?://)?scholar\.google\.com/[a-zA-Z0-9\-_?=&]+",
    "orcid": r"(?:https?://)?(?:www\.)?orcid\.org/[0-9X\-]+",
    "medium": r"(?:https?://)?(?:www\.)?medium\.com/@?[a-zA-Z0-9\-_]+",
    "figma": r"(?:https?://)?(?:www\.)?figma\.com/@?[a-zA-Z0-9\-_]+",
    "tableau_public": r"(?:https?://)?public\.tableau\.com/[a-zA-Z0-9\-_/]+",
    "personal_site": r"(?:https?://)?[a-zA-Z0-9\-_]+\.(?:io|dev|me|com|co|net|org|cc)(?:/[a-zA-Z0-9\-_/]*)?",
}

ROLE_LINK_MAP = {
    "software_engineering": {
        "label": "Software Engineering / 软件工程",
        "jd_keywords": [
            r"software\s*(?:engineer|developer|architect)",
            r"(?:front|back|full)\s*[- ]?end\s*(?:developer|engineer)?",
            r"SDE|SRE|DevOps|platform\s*engineer",
            r"开发(?:工程师|人员|者)",
            r"(?:前端|后端|全栈|客户端)\s*(?:开发|工程师)",
        ],
        "expected_links": ["github", "gitlab"],
    },
    "design": {
        "label": "Design / 设计",
        "jd_keywords": [
            r"(?:UX|UI|product|graphic|visual|interaction)\s*design(?:er)?",
            r"(?:用户|交互|产品|视觉|图形)\s*设计(?:师)?",
        ],
        "expected_links": ["behance", "dribbble", "figma"],
    },
    "data_science": {
        "label": "Data Science & Analytics / 数据科学",
        "jd_keywords": [
            r"data\s*(?:scientist|analyst|engineer)",
            r"machine\s*learning\s*(?:engineer)?",
            r"(?:数据(?:科学|分析|工程)|机器学习)",
        ],
        "expected_links": ["github", "kaggle", "tableau_public"],
    },
    "academic": {
        "label": "Academic / Research / 学术研究",
        "jd_keywords": [
            r"(?:postdoc|post[\- ]?doctoral|professor|research(?:er| fellow)?)",
            r"(?:Ph\.?D|博士|研究员|博士后|教授)",
        ],
        "expected_links": ["scholar", "orcid"],
    },
    "product_management": {
        "label": "Product Management / 产品管理",
        "jd_keywords": [
            r"product\s*(?:manager|owner|director)",
            r"(?:产品经理|产品总监|产品负责人)",
        ],
        "expected_links": ["medium", "personal_site"],
    },
}


def detect_role_type(jd_text: str) -> list:
    """Detect role type(s) from JD text using structural keyword matching."""
    matched = []
    for role_key, role_info in ROLE_LINK_MAP.items():
        for pattern in role_info["jd_keywords"]:
            if re.search(pattern, jd_text, re.IGNORECASE):
                matched.append(role_key)
                break
    return matched


def scan_resume_links(resume_text: str) -> list:
    """Scan resume text for known portfolio/professional link patterns."""
    found = []
    seen_types = set()
    for link_type, pattern in LINK_PATTERNS.items():
        matches = re.findall(pattern, resume_text, re.IGNORECASE)
        if matches and link_type not in seen_types:
            found.append({"type": link_type, "url": matches[0]})
            seen_types.add(link_type)
    return found


# ─── Resume Timeline Parsing / 简历时间轴解析 ─────────────
# Used by ats_checker.py for gap detection (especially DACH region)

_MONTH_MAP = {
    "jan": 1, "january": 1, "feb": 2, "february": 2,
    "mar": 3, "march": 3, "apr": 4, "april": 4,
    "may": 5, "jun": 6, "june": 6, "jul": 7, "july": 7,
    "aug": 8, "august": 8, "sep": 9, "sept": 9, "september": 9,
    "oct": 10, "october": 10, "nov": 11, "november": 11,
    "dec": 12, "december": 12,
}

def _parse_date_part(s: str):
    """Parse a date string into (YYYY, MM) tuple or None."""
    s = s.strip().strip(".")
    # YYYY.MM / YYYY/MM / YYYY-MM
    m = re.match(r"(\d{4})[.\-/](\d{1,2})", s)
    if m:
        return (int(m.group(1)), int(m.group(2)))
    # YYYY年M月
    m = re.match(r"(\d{4})\s*年\s*(\d{1,2})\s*月?", s)
    if m:
        return (int(m.group(1)), int(m.group(2)))
    # Month YYYY (e.g., "Jan 2024")
    m = re.match(r"([A-Za-z]+)\s+(\d{4})", s)
    if m:
        month_num = _MONTH_MAP.get(m.group(1).lower())
        if month_num:
            return (int(m.group(2)), month_num)
    # YYYY only
    m = re.match(r"(\d{4})$", s.strip())
    if m:
        return (int(m.group(1)), 1)
    return None


def parse_resume_timeline(text: str) -> dict:
    """
    Parse all date ranges from resume text and detect timeline gaps.
    Returns {"entries": [...], "gaps": [...]}.

    Entries: list of {"start": (YYYY,MM), "end": (YYYY,MM)|None, "raw": str, "is_ongoing": bool}
    Gaps: list of {"start": (YYYY,MM), "end": (YYYY,MM), "months": int, "detail": str}
    """
    from datetime import datetime
    now = datetime.now()
    now_ym = (now.year, now.month)

    entries = []

    # Numeric ranges: 2021.01 - 2024.03, 2021/01 - 2024/03, 2021年1月 - 2024年3月
    for m in re.finditer(
        r"(\d{4}[.\-/年]\d{1,2}[月]?)\s*[-–—~至到]\s*(\d{4}[.\-/年]\d{1,2}[月]?)",
        text
    ):
        start = _parse_date_part(m.group(1))
        end = _parse_date_part(m.group(2))
        if start and end:
            entries.append({"start": start, "end": end, "raw": m.group(0).strip(), "is_ongoing": False})

    # Ongoing: 2021.01 - present / 至今 / 现在
    for m in re.finditer(
        r"(\d{4}[.\-/年]\d{1,2}[月]?)\s*[-–—~至到]\s*(?:present|till\s+now|current|至今|现在)",
        text, re.IGNORECASE
    ):
        start = _parse_date_part(m.group(1))
        if start:
            entries.append({"start": start, "end": now_ym, "raw": m.group(0).strip(), "is_ongoing": True})

    # Month name ranges: Jan 2020 - Dec 2024
    for m in re.finditer(
        r"([A-Za-z]{3,9})\s+(\d{4})\s*[-–—~至到]\s*([A-Za-z]{3,9})\s+(\d{4})",
        text, re.IGNORECASE
    ):
        start = _parse_date_part(f"{m.group(1)} {m.group(2)}")
        end = _parse_date_part(f"{m.group(3)} {m.group(4)}")
        if start and end:
            entries.append({"start": start, "end": end, "raw": m.group(0).strip(), "is_ongoing": False})

    # Month name ongoing: Jan 2020 - present
    for m in re.finditer(
        r"([A-Za-z]{3,9})\s+(\d{4})\s*[-–—~至到]\s*(?:present|till\s+now|current|至今|现在)",
        text, re.IGNORECASE
    ):
        start = _parse_date_part(f"{m.group(1)} {m.group(2)}")
        if start:
            entries.append({"start": start, "end": now_ym, "raw": m.group(0).strip(), "is_ongoing": True})

    # Sort by start date
    entries.sort(key=lambda e: e["start"])

    # Calculate gaps between entries
    gaps = []
    for i in range(1, len(entries)):
        prev_end = entries[i - 1]["end"]
        curr_start = entries[i]["start"]
        if prev_end and curr_start:
            gap_months = (curr_start[0] - prev_end[0]) * 12 + (curr_start[1] - prev_end[1])
            if gap_months >= 2:  # only flag gaps >= 2 months
                gap_detail = f"{prev_end[0]}.{prev_end[1]:02d} → {curr_start[0]}.{curr_start[1]:02d} ({gap_months} months)"
                gaps.append({
                    "start": prev_end,
                    "end": curr_start,
                    "months": gap_months,
                    "detail": gap_detail,
                    "after": entries[i - 1]["raw"],
                    "before": entries[i]["raw"],
                })

    # Also check gap from last entry to now (if not ongoing)
    if entries and not entries[-1]["is_ongoing"]:
        last_end = entries[-1]["end"]
        if last_end:
            gap_months = (now_ym[0] - last_end[0]) * 12 + (now_ym[1] - last_end[1])
            if gap_months >= 2:
                gap_detail = f"{last_end[0]}.{last_end[1]:02d} → {now_ym[0]}.{now_ym[1]:02d} ({gap_months} months)"
                gaps.append({
                    "start": last_end,
                    "end": now_ym,
                    "months": gap_months,
                    "detail": gap_detail,
                    "after": entries[-1]["raw"],
                    "before": "(current date)",
                })

    return {"entries": entries, "gaps": gaps}


def check_portfolio_links(jd_text: str, resume_text: str) -> dict:
    """Check if resume has portfolio links appropriate for the detected role type."""
    roles = detect_role_type(jd_text)
    links = scan_resume_links(resume_text)
    link_types_found = {l["type"] for l in links}

    missing_links = []
    missing_critical = False
    for role in roles:
        role_info = ROLE_LINK_MAP[role]
        expected = role_info["expected_links"]
        for exp_type in expected:
            if exp_type not in link_types_found:
                missing_links.append({
                    "role": role,
                    "role_label": role_info["label"],
                    "missing_link_type": exp_type,
                })
                missing_critical = True

    return {
        "role_types_detected": roles,
        "links_found": links,
        "missing_critical": missing_critical,
        "missing_links": missing_links,
    }
