"""
Resume Tailor — Pipeline Engine (v2.1)

Orchestrates the full analysis pipeline:
  1. Parse JD (structural feature extraction)
  2. Read resume structure (if .docx)
  3. ATS compatibility check

This module contains the business logic. main.py is purely an argparse layer.
"""

import json
import os

# Ensure scripts/ directory is in path for imports
sys_path = os.path.dirname(os.path.abspath(__file__))
if sys_path not in __import__("sys").path:
    __import__("sys").path.insert(0, sys_path)

from jd_parser import parse_jd, read_resume_text, print_report
from diff_audit import read_docx_structured
from ats_checker import run_checks, format_markdown


def run_full_pipeline(
    jd_path: str,
    resume_path: str = None,
    keywords: list = None,
    region: str = "global",
    json_output: bool = False,
) -> dict | str:
    """
    Execute the full pipeline: parse JD → read resume structure → ATS check.

    Args:
        jd_path: Path to JD file (text/markdown).
        resume_path: Path to resume file (.docx/.pdf/.txt/.md). Optional.
        keywords: Explicit keyword list. Falls back to empty if not provided.
        region: ATS region profile key (default: "global").
        json_output: If True, returns JSON string. Otherwise returns formatted text.

    Returns:
        dict if json_output=True, else formatted string.
    """
    # ── Step 1: Parse JD ──
    with open(jd_path, "r", encoding="utf-8") as f:
        jd_text = f.read()

    resume_text = read_resume_text(resume_path) if resume_path else None
    jd_result = parse_jd(jd_text, resume_text)

    # ── Step 2: Read resume structure (if .docx) ──
    structure = None
    if resume_path and resume_path.lower().endswith(".docx"):
        try:
            structure = read_docx_structured(resume_path)
        except Exception:
            pass

    # ── Step 3: ATS check ──
    ats_result = None
    if resume_text:
        ats_result = run_checks(resume_text, keywords=keywords or [], region=region)

    # ── Compile result ──
    output = {
        "jd_analysis": jd_result,
        "resume_structure": structure,
        "ats_check": ats_result,
    }

    if json_output:
        return output

    # Human-readable output
    lines = []
    # JD report
    import io
    from contextlib import redirect_stdout

    buf = io.StringIO()
    with redirect_stdout(buf):
        print_report(jd_result)
    lines.append(buf.getvalue())

    # ATS report
    if ats_result:
        lines.append("\n" + format_markdown(ats_result))

    return "\n".join(lines)
