"""
Resume Tailor — Unified CLI Entry Point (v2)

Dispatches to jd_parser.py, diff_audit.py, or ats_checker.py.

Usage:
    python main.py parse --file jd.txt --resume resume.docx --json
    python main.py read-structured --resume resume.docx
    python main.py diff --source-docx source.docx --tailored-docx tailored.md --json
    python main.py ats --resume tailored.md --keywords "Python,SQL" --region north_america --json
    python main.py full --jd jd.txt --resume resume.docx --region north_america --json
"""

import argparse
import sys
import os

# Ensure scripts/ directory is in path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def cmd_parse(args):
    """JD feature extraction."""
    from jd_parser import main as parse_main
    # Reconstruct sys.argv for jd_parser
    argv = ["jd_parser.py"]
    if args.file:
        argv.extend(["--file"])
    argv.append(args.input)
    if args.json:
        argv.append("--json")
    if args.resume:
        argv.extend(["--resume", args.resume])
    sys.argv = argv
    parse_main()


def cmd_read_structured(args):
    """Structure-aware resume reading."""
    from diff_audit import main as diff_main
    sys.argv = ["diff_audit.py", "--read-structured", args.resume]
    if args.json:
        sys.argv.append("--json")
    diff_main()


def cmd_diff(args):
    """Diff source vs tailored resume."""
    from diff_audit import main as diff_main
    sys.argv = ["diff_audit.py"]
    if args.source_docx:
        sys.argv.extend(["--source-docx", args.source_docx])
    if args.tailored_docx:
        sys.argv.extend(["--tailored-docx", args.tailored_docx])
    if args.json:
        sys.argv.append("--json")
    diff_main()


def cmd_ats(args):
    """ATS compatibility check."""
    from ats_checker import main as ats_main
    sys.argv = ["ats_checker.py", "--resume", args.resume]
    if args.keywords:
        sys.argv.extend(["--keywords", args.keywords])
    if args.keywords_file:
        sys.argv.extend(["--keywords-file", args.keywords_file])
    if args.region:
        sys.argv.extend(["--region", args.region])
    if args.lang:
        sys.argv.extend(["--lang", args.lang])
    if args.json:
        sys.argv.append("--json")
    if args.output:
        sys.argv.extend(["--output", args.output])
    ats_main()


def cmd_full(args):
    """Full pipeline: parse JD → read resume structure → ATS check."""
    import json
    from jd_parser import parse_jd, read_resume_text
    from diff_audit import read_docx_structured
    from ats_checker import run_checks

    # Step 1: Parse JD
    with open(args.jd, "r", encoding="utf-8") as f:
        jd_text = f.read()

    resume_text = read_resume_text(args.resume) if args.resume else None
    jd_result = parse_jd(jd_text, resume_text)

    # Step 2: Read resume structure (if .docx)
    structure = None
    if args.resume and args.resume.endswith(".docx"):
        try:
            structure = read_docx_structured(args.resume)
        except Exception:
            pass

    # Step 3: ATS check (keywords from JD)
    keywords = []
    if args.keywords:
        keywords = [k.strip() for k in args.keywords.split(",")]
    region = args.region or "global"

    if resume_text:
        ats_result = run_checks(resume_text, keywords=keywords, region=region)
    else:
        ats_result = None

    # Compile
    output = {
        "jd_analysis": jd_result,
        "resume_structure": structure,
        "ats_check": ats_result,
    }

    if args.json:
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        from jd_parser import print_report
        print_report(jd_result)
        if ats_result:
            from ats_checker import format_markdown
            print("\n" + format_markdown(ats_result))


def main():
    parser = argparse.ArgumentParser(
        description="Resume Tailor v2 — Unified CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # ─── parse ───
    p_parse = subparsers.add_parser("parse", help="JD feature extraction")
    p_parse.add_argument("input", help="JD text or file path")
    p_parse.add_argument("--file", action="store_true", help="Read from file")
    p_parse.add_argument("--json", action="store_true", help="JSON output")
    p_parse.add_argument("--resume", type=str, default=None, help="Resume file")
    p_parse.set_defaults(func=cmd_parse)

    # ─── read-structured ───
    p_read = subparsers.add_parser("read-structured", help="Structure-aware resume read")
    p_read.add_argument("--resume", required=True, help="Resume .docx path")
    p_read.add_argument("--json", action="store_true")
    p_read.set_defaults(func=cmd_read_structured)

    # ─── diff ───
    p_diff = subparsers.add_parser("diff", help="Diff source vs tailored")
    p_diff.add_argument("--source-docx", type=str, default=None)
    p_diff.add_argument("--tailored-docx", type=str, default=None)
    p_diff.add_argument("--json", action="store_true")
    p_diff.set_defaults(func=cmd_diff)

    # ─── ats ───
    p_ats = subparsers.add_parser("ats", help="ATS compatibility check")
    p_ats.add_argument("--resume", required=True, help="Tailored resume path")
    p_ats.add_argument("--keywords", default="", help="Comma-separated keywords")
    p_ats.add_argument("--keywords-file", default="", help="Keywords JSON file")
    p_ats.add_argument("--region", default="global", help="Target region")
    p_ats.add_argument("--lang", default="auto", choices=["auto", "zh", "en"])
    p_ats.add_argument("--json", action="store_true")
    p_ats.add_argument("--output", default="", help="Output file path")
    p_ats.set_defaults(func=cmd_ats)

    # ─── full ───
    p_full = subparsers.add_parser("full", help="Full pipeline")
    p_full.add_argument("--jd", required=True, help="JD file path")
    p_full.add_argument("--resume", default=None, help="Resume file path")
    p_full.add_argument("--keywords", default="", help="Comma-separated keywords")
    p_full.add_argument("--region", default="global", help="Target region")
    p_full.add_argument("--json", action="store_true")
    p_full.set_defaults(func=cmd_full)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
