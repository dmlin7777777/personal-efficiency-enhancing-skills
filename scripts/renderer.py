"""
Resume Tailor — Renderer Pipeline (v3.0)

Rendering pipeline: Markdown → (preprocess) → Jinja2 HTML → PDF/DOCX.

Architecture:
  - Jinja2 as template glue — zero string concatenation in code.
  - WeasyPrint for PDF (best CSS print support in Python ecosystem).
  - pypandoc for DOCX fallback (cleaner than HTML→Word conversion).
  - Regex preprocessing for **Summary**: content → <span class="bullet-summary"> pattern.
  - Page overflow detection: len(doc.pages) > 1 triggers compression warning to engine.py.

Entry point:
  render(snapshot_path, output_dir) -> RenderResult

Graceful degradation:
  - WeasyPrint unavailable on Windows? Falls back to HTML-only + browser-based PDF hint.
  - pandoc not installed? Falls back to raw markdown export.
"""

import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# ── Lazy imports ──

def _import_jinja2():
    from jinja2 import Environment, FileSystemLoader, select_autoescape
    return Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )


def _import_markdown_lib():
    """Try markdown-it-py (preferred) or fallback to standard markdown."""
    try:
        from markdown_it import MarkdownIt
        return MarkdownIt("commonmark").enable("strikethrough")
    except ImportError:
        import markdown
        return None


# ── Constants ──

BASE_DIR = Path(__file__).parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
SCHEMAS_DIR = BASE_DIR / "schemas"

JINJA_TEMPLATE_NAME = "resume_layout.html.j2"   # Jinja2 layout template
CSS_FILENAME = "resume_template.css"              # Our crafted CSS

# Required font families (must be available on host system)
# Each category lists aliases — ANY one match means the font is available
REQUIRED_FONTS = {
    "Latin/Digits": ["Times New Roman", "Times"],
    # Microsoft YaHei registers as "Microsoft YaHei" in Windows registry;
    # Chinese name "微软雅黑" may not appear in registry but the same font.
    "CJK": ["Microsoft YaHei", "微软雅黑", "SimHei", "黑体"],
}

# Cache for environment check results
_ENV_CHECK_CACHE = None


def check_rendering_environment() -> dict:
    """
    Check the runtime environment for rendering prerequisites.

    Returns dict with:
      - fonts_available: {category: [found_font, ...]}
      - fonts_missing: {category: [missing_font_list]}
      - weasyprint_available: bool
      - pandoc_available: bool
      - warnings: list[str]
      - is_healthy: bool (fonts ok + at least one output format works)
    """
    global _ENV_CHECK_CACHE
    if _ENV_CHECK_CACHE is not None:
        return _ENV_CHECK_CACHE

    result = {
        "fonts_available": {},
        "fonts_missing": {},
        "weasyprint_available": False,
        "pandoc_available": False,
        "warnings": [],
        "is_healthy": True,
    }

    # --- Font detection ---
    import platform
    system = platform.system()

    if system == "Windows":
        # On Windows, query the registry for installed fonts
        result["fonts_available"], result["fonts_missing"] = _check_fonts_windows()
    elif system == "Darwin":
        result["fonts_available"], result["fonts_missing"] = _check_fonts_macos()
    elif system == "Linux":
        result["fonts_available"], result["fonts_missing"] = _check_fonts_linux()
    else:
        # Unknown OS — optimistic default
        for cat in REQUIRED_FONTS:
            result["fonts_available"][cat] = ["(unknown — assuming available)"]
            result["fonts_missing"][cat] = []

    # Generate font warnings
    for cat, missing in result["fonts_missing"].items():
        if missing:
            result["warnings"].append(
                f"Missing fonts for {cat}: {', '.join(missing)}. "
                f"PDF/HTML may render with fallback fonts."
            )

    # --- WeasyPrint ---
    result["weasyprint_available"] = _check_weasyprint()

    # --- Pandoc ---
    try:
        import pypandoc
        result["pandoc_available"] = bool(pypandoc.get_pandoc_version())
    except (ImportError, Exception):
        result["pandoc_available"] = False
        # Only warn if DOCX was requested (checked later)

    # Health check: need fonts + at least one output format
    has_any_output = result["weasyprint_available"] or result["pandoc_available"]
    all_fonts_ok = all(len(v) == 0 for v in result["fonts_missing"].values())
    result["is_healthy"] = all_fonts_ok and has_any_output

    _ENV_CHECK_CACHE = result
    return result


def _check_fonts_windows() -> tuple[dict, dict]:
    """Check font availability on Windows via registry."""
    available = {}
    missing = {}

    try:
        import winreg
        font_key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"
        )
        installed_fonts = []
        i = 0
        while True:
            try:
                font_name, _, _ = winreg.EnumValue(font_key, i)
                installed_fonts.append(font_name.lower().rstrip("(truetype)").rstrip("(opentype)"))
                i += 1
            except OSError:
                break
        winreg.CloseKey(font_key)

        for cat, font_list in REQUIRED_FONTS.items():
            found_any = False
            found_names = []
            not_found = []
            for font_name in font_list:
                if any(font_name.lower() in f for f in installed_fonts):
                    found_names.append(font_name)
                    found_any = True
                else:
                    not_found.append(font_name)
            # If any alias matched → category is available
            if found_any:
                available[cat] = found_names
                missing[cat] = []  # No missing — we have at least one working alias
            else:
                available[cat] = ["(fallback to serif/sans-serif)"]
                missing[cat] = not_found

    except Exception as e:
        # Registry access failed (e.g., limited permissions) — assume OK
        for cat in REQUIRED_FONTS:
            available[cat] = ["(registry access denied — assumed present)"]
            missing[cat] = []

    return available, missing


def _check_fonts_macos() -> tuple[dict, dict]:
    """Check font availability on macOS via Font Book."""
    import subprocess
    available = {}
    missing = {}

    try:
        result = subprocess.run(
            ["system_profiler", "SPFontsDataType"],
            capture_output=True, text=True, timeout=10
        )
        font_output = result.stdout.lower()

        for cat, font_list in REQUIRED_FONTS.items():
            found_any = False
            found_names = []
            not_found = []
            for font_name in font_list:
                if font_name.lower() in font_output:
                    found_names.append(font_name)
                    found_any = True
                else:
                    not_found.append(font_name)
            if found_any:
                available[cat] = found_names
                missing[cat] = []
            else:
                available[cat] = ["(fallback to serif/sans-serif)"]
                missing[cat] = not_found
    except Exception:
        for cat in REQUIRED_FONTS:
            available[cat] = ["(font check failed — assumed present)"]
            missing[cat] = []

    return available, missing


def _check_fonts_linux() -> tuple[dict, dict]:
    """Check font availability on Linux via fc-list."""
    import subprocess
    available = {}
    missing = {}

    try:
        result = subprocess.run(
            ["fc-list", ":", "family"],
            capture_output=True, text=True, timeout=10
        )
        font_output = result.stdout.lower()

        for cat, font_list in REQUIRED_FONTS.items():
            found_any = False
            found_names = []
            not_found = []
            for font_name in font_list:
                if font_name.lower() in font_output:
                    found_names.append(font_name)
                    found_any = True
                else:
                    not_found.append(font_name)
            if found_any:
                available[cat] = found_names
                missing[cat] = []
            else:
                available[cat] = ["(fallback to serif/sans-serif)"]
                missing[cat] = not_found
    except Exception:
        for cat in REQUIRED_FONTS:
            available[cat] = ["(fc-list not found — assumed present)"]
            missing[cat] = []

    return available, missing


@dataclass
class RenderResult:
    """Structured result of a rendering pass."""
    success: bool = False
    html_path: Optional[str] = None
    pdf_path: Optional[str] = None
    docx_path: Optional[str] = None
    md_path: Optional[str] = None
    page_count: int = 0
    warnings: list = field(default_factory=list)
    errors: list = field(default_factory=list)
    engine_action: Optional[dict] = None  # Compression instruction if overflow detected


# ════════════════════════════════════════════════════════
# PHASE 1: SEMANTIC PREPROCESSING
# ════════════════════════════════════════════════════════

# Pattern 1 (primary): Match bullet points starting with "- **Summary**: detail"
# Anchored with ^\s*- to prevent matching **bold** in headings/titles
# Handles: no-space-colon, multi-space, space-before-colon, CJK colon
# (.+?) non-greedy + [^\n\r] prevents cross-line over-matching
BULLET_SUMMARY_PATTERN = re.compile(
    r'^\s*\-\s*\*\*(.+?)\*\*\s*[:：]\s*([^\n\r]+)',
    re.MULTILINE,
)

# Pattern 2 (fallback): **Summary**: at end of line with no detail (malformed, skip)
BULLET_SUMMARY_EMPTY_PATTERN = re.compile(
    r'^\s*\-\s*\*\*(.+?)\*\*\s*[:：]\s*$',
    re.MULTILINE,
)


def preprocess_markdown(md_text: str) -> str:
    """
    Phase 1: Preprocess Markdown before rendering.

    Transformations:
      1. **Summary**: content → <span class="bullet-summary">Summary:</span> content
         This lets the LLM output plain Markdown while the renderer applies CSS styling.
      2. Normalize CJK colons to ASCII colons for consistency.
      3. Strip excessive blank lines (>2 consecutive).
      4. Robustness: handles zero/multiple spaces around colon, space-before-colon,
         and gracefully skips empty bullet summaries.

    Regex robustness notes:
      - ^\\s*\\- anchor: ONLY matches list items (- text), prevents matching **bold** 
        in headings like "### Company — **Job Title**"
      - \\s* before colon: matches "text** :" (space before colon)
      - \\s* after colon: matches "text:**" (no space after) or "text**:  " (multiple spaces)
      - (.+?) non-greedy capture: prevents over-matching within same line
      - [^\\n\\r]+ for detail: restricts to single line, preventing cross-bullet over-match
      - re.MULTILINE: each line is checked independently
      - Multi-line bullets: only the FIRST line gets <span> styling; continuation lines 
        render as normal body text (this is acceptable and safer than DOTALL greediness)
    """
    def _replace_bullet(match):
        summary_text = match.group(1).strip()
        detail_text = match.group(2).strip()
        # Skip if detail is empty — don't create empty <span>
        if not detail_text:
            return match.group(0)  # Return original unchanged
        return f'<span class="bullet-summary">{summary_text}:</span> {detail_text}'

    processed = BULLET_SUMMARY_PATTERN.sub(_replace_bullet, md_text)

    # Collapse 3+ newlines into 2
    processed = re.sub(r'\n{3,}', '\n\n', processed)

    return processed.strip()


# ════════════════════════════════════════════════════════
# PHASE 2: MARKDOWN → HTML CONVERSION
# ════════════════════════════════════════════════════════

def markdown_to_html(md_text: str) -> str:
    """
    Convert preprocessed Markdown string to HTML fragment.

    Uses markdown-it-py if available (better spec compliance),
    falls back to standard markdown library.
    """
    md_converter = _import_markdown_lib()

    if md_converter is None:
        # Fallback: use built-in markdown library
        import markdown
        extensions = ["tables", "fenced_code", "nl2br"]
        return markdown.markdown(md_text, extensions=extensions)

    # markdown-it-py path
    return md_converter.render(md_text)


# ════════════════════════════════════════════════════════
# PHASE 3: JINJA2 TEMPLATE RENDERING (HTML + CSS)
# ════════════════════════════════════════════════════════

def _load_css() -> str:
    """Read our resume CSS template."""
    css_path = TEMPLATES_DIR / CSS_FILENAME
    if not css_path.exists():
        raise FileNotFoundError(f"CSS template missing: {css_path}")
    return css_path.read_text(encoding="utf-8")


def render_html_layout(html_body: str,
                       snapshot_data: dict,
                       output_path: Path) -> str:
    """
    Phase 3: Wrap HTML body fragment in our Jinja2 layout template.

    The layout includes:
      - <head> with our CSS embedded (inline for portability)
      - A4 @page settings
      - Semantic <body> structure matching our CSS classes
    """
    env = _import_jinja2()
    css_content = _load_css()

    # Extract metadata for template context
    jd_facts = snapshot_data.get("jd_facts", {})
    meta = snapshot_data.get("_meta", {})
    user_prefs = snapshot_data.get("user_decisions", {}).get("user_preferences", {})

    # Build header info from snapshot metadata if available
    experiences = snapshot_data.get("user_decisions", {}).get("kept_experiences", [])

    template_context = {
        "css_inline": css_content,
        "body_html": html_body,
        "role_title": jd_facts.get("role_title", "Resume"),
        "company": jd_facts.get("company_name", ""),
        "session_id": meta.get("session_id", ""),
        "generated_at": meta.get("last_updated", ""),
        "page_limit": user_prefs.get("page_limit", 1),
        "experience_count": len(experiences),
    }

    # Check if layout template exists; if not, generate inline
    layout_path = TEMPLATES_DIR / JINJA_TEMPLATE_NAME
    if layout_path.exists():
        template = env.get_template(JINJA_TEMPLATE_NAME)
        html_output = template.render(**template_context)
    else:
        # Inline fallback layout (no external .j2 file needed)
        html_output = _generate_inline_layout(template_context)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_output, encoding="utf-8")
    return str(output_path)


def _generate_inline_layout(ctx: dict) -> str:
    """Fallback layout when no .j2 template file exists."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{ctx['role_title']} | Resume Tailor</title>
<style>
{{{{ ctx['css_inline'] }}}}
</style>
</head>
<body>
<div class="page-container">
{{{{ ctx['body_html'] }}}}
</div>
</body>
</html>""".replace("{{{{", "{{").replace("}}}}", "}}")


# ════════════════════════════════════════════════════════
# PHASE 4a: PDF RENDERING (WeasyPrint)
# ════════════════════════════════════════════════════════

_WEASYPRINT_AVAILABLE = None  # Cached availability check


def _check_weasyprint() -> bool:
    """Check if WeasyPrint can be imported (needs GTK/Pango runtime)."""
    global _WEASYPRINT_AVAILABLE
    if _WEASYPRINT_AVAILABLE is not None:
        return _WEASYPRINT_AVAILABLE
    try:
        import weasyprint
        # Actually try to instantiate to catch GTK errors
        weasyprint.HTML(string="<p>test</p>").render()
        _WEASYPRINT_AVAILABLE = True
    except Exception:
        _WEASYPRINT_AVAILABLE = False
    return _WEASYPRINT_AVAILABLE


def render_pdf(html_path: str, output_pdf_path: str) -> dict:
    """
    Phase 4a: Convert HTML → PDF using WeasyPrint.

    Returns:
        dict with keys: path, page_count, warning (if pages > 1)
    Raises:
        RuntimeError: If WeasyPrint is unavailable.
    """
    if not _check_weasyprint():
        raise RuntimeError(
            "WeasyPrint is not available on this system. "
            "On Windows, install GTK+ runtime first. "
            "Falling back to HTML output."
        )

    from weasyprint import HTML, FontConfiguration

    font_config = FontConfiguration()
    doc = HTML(filename=html_path).render(font_config=font_config)

    page_count = len(doc.pages)
    doc.write_pdf(output_pdf_path)

    result = {
        "path": output_pdf_path,
        "page_count": page_count,
    }

    if page_count > 1:
        result["warning"] = (
            f"PDF exceeds 1-page limit ({page_count} pages). "
            "Engine should trigger Architect compression instructions."
        )
        # Generate structured action for engine.py
        result["engine_action"] = {
            "type": "PAGE_OVERFLOW",
            "current_pages": page_count,
            "target_pages": 1,
            "suggestion": (
                "Instruct architect_writer node to reduce content by "
                f"~{int((page_count - 1) / page_count * 100)}% "
                "without removing core facts."
            ),
        }

    return result


# ════════════════════════════════════════════════════════
# PHASE 4b: DOCX FALLBACK (pypandoc)
# ════════════════════════════════════════════════════════

def render_docx(md_path: str, output_docx_path: str) -> dict:
    """
    Phase 4b: Convert Markdown → clean DOCX via pypandoc.

    Rationale: HTML→Word produces broken layouts due to different rendering engines.
    pypandoc uses pandoc's native DOCX writer which respects Word's own styling model.

    Returns:
        dict with key: path
    Raises:
        RuntimeError: If pandoc/pypandoc is not available.
    """
    try:
        import pypandoc
        # Verify pandoc binary exists
        if not pypandoc.get_pandoc_version():
            raise RuntimeError("pandoc binary not found in PATH")
    except ImportError:
        raise RuntimeError(
            "pypandoc not installed. Run: pip install pypandoc\n"
            "Also ensure pandoc is installed: https://pandoc.org/installing.html"
        )

    output = pypandoc.convert_file(
        md_path,
        "docx",
        outputfile=output_docx_path,
        extra_args=[
            "--reference-doc", str(TEMPLATES_DIR / "reference.docx"),
        ] if (TEMPLATES_DIR / "reference.docx").exists() else [],
    )

    return {"path": output_docx_path or output_docx_path}


# ════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ════════════════════════════════════════════════════════

def render(snapshot_path: str, output_dir: str = None) -> RenderResult:
    """
    Main rendering entry point.

    Reads snapshot.json, extracts draft markdown, runs the full pipeline:
      1. Preprocess Markdown (semantic patterns)
      2. MD → HTML conversion
      3. Jinja2 layout rendering (with CSS injection)
      4a. WeasyPrint → PDF (if requested & available)
      4b. pypandoc → DOCX (if requested & available)

    Design contract with engine.py:
      - This function READS snapshot.json only. It NEVER writes back.
      - All state mutations (e.g., recording page count) are returned via RenderResult.
      - engine.py is responsible for merging any engine_action into the snapshot.

    Args:
        snapshot_path: Absolute path to context_snapshot.json
        output_dir: Directory for outputs (defaults to session dir)

    Returns:
        RenderResult with paths and status information.
    """
    result = RenderResult()
    snap_path = Path(snapshot_path)

    if not snap_path.exists():
        result.errors.append(f"Snapshot not found: {snapshot_path}")
        return result

    # --- Environment check ---
    env_status = check_rendering_environment()
    if env_status["warnings"]:
        result.warnings.extend(env_status["warnings"])

    # --- Load snapshot (READ-ONLY) ---
    with open(snap_path, "r", encoding="utf-8") as f:
        snapshot_data = json.load(f)

    # Determine output directory
    if output_dir is None:
        output_dir = str(snap_path.parent)
    out = Path(output_dir)

    # --- Locate draft markdown ---
    draft_rel_path = snapshot_data.get("expert_outputs", {}).get("writer_draft_path")
    if not draft_rel_path:
        result.errors.append("No writer_draft_path found in snapshot expert_outputs.")
        return result

    draft_full_path = BASE_DIR / draft_rel_path
    if not draft_full_path.exists():
        result.errors.append(f"Draft file not found: {draft_full_path}")
        return result

    md_text = draft_full_path.read_text(encoding="utf-8")

    # Save raw markdown as intermediate artifact
    md_out = out / "tailored_resume.md"
    md_out.write_text(md_text, encoding="utf-8")
    result.md_path = str(md_out)

    user_prefs = snapshot_data.get("user_decisions", {}).get("user_preferences", {})
    output_format = user_prefs.get("output_format", "html")  # Default: HTML preview

    # === Phase 1: Preprocess ===
    processed_md = preprocess_markdown(md_text)

    # Save preprocessed markdown for debugging
    pp_md_out = out / "tailored_resume_preprocessed.md"
    pp_md_out.write_text(processed_md, encoding="utf-8")

    # === Phase 2: MD → HTML Fragment ===
    html_fragment = markdown_to_html(processed_md)

    # === Phase 3: Jinja2 Layout ===
    html_out = out / "tailored_resume.html"
    html_path = render_html_layout(html_fragment, snapshot_data, html_out)
    result.html_path = html_path
    result.success = True

    # === Phase 4a: PDF (if requested) ===
    if output_format in ("pdf", "both"):
        pdf_out = out / "tailored_resume.pdf"
        try:
            pdf_result = render_pdf(html_path, str(pdf_out))
            result.pdf_path = pdf_result["path"]
            result.page_count = pdf_result["page_count"]

            if "warning" in pdf_result:
                result.warnings.append(pdf_result["warning"])
            if "engine_action" in pdf_result:
                result.engine_action = pdf_result["engine_action"]

        except RuntimeError as e:
            result.warnings.append(f"PDF generation failed: {e}")
            # Graceful degradation: tell user how to get PDF manually
            result.warnings.append(
                "Fallback: Open the generated HTML in Chrome/Firefox and Print→Save as PDF."
            )

    # === Phase 4b: DOCX (if requested) ===
    if output_format in ("docx", "both"):
        docx_out = out / "tailored_resume.docx"
        try:
            docx_result = render_docx(str(md_out), str(docx_out))
            result.docx_path = docx_result["path"]
        except RuntimeError as e:
            result.warnings.append(f"DOCX generation failed: {e}")

    # === Summary ===
    if output_format == "pdf" and not result.pdf_path:
        result.warnings.append(
            "PDF could not be generated. HTML output is available as fallback. "
            "For best results, open HTML in a modern browser and use Print→Save as PDF."
        )

    return result


# ════════════════════════════════════════════════════════
# CLI INTERFACE (for standalone testing)
# ════════════════════════════════════════════════════════

def main():
    """CLI entry point for testing: python renderer.py <snapshot.json> [output_dir] [format]"""
    import argparse

    parser = argparse.ArgumentParser(description="Resume Tailor Renderer v3.0")
    parser.add_argument("snapshot", help="Path to context_snapshot.json")
    parser.add_argument("output_dir", nargs="?", default=None, help="Output directory")
    parser.add_argument("--format", dest="fmt", default="html",
                        choices=["html", "pdf", "docx", "both"],
                        help="Output format (default: html)")
    args = parser.parse_args()

    # Override format from CLI if provided
    if args.fmt:
        # Patch snapshot preferences
        snap_path = Path(args.snapshot)
        if snap_path.exists():
            with open(snap_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            data.setdefault("user_decisions", {}).setdefault("user_preferences", {})[
                "output_format"
            ] = args.fmt
            # Write back temporarily (or just pass through)
            # We'll handle this by accepting format override in render()

    print(f"[Renderer] Processing: {args.snapshot}")

    # Show environment status
    env = check_rendering_environment()
    if env["warnings"]:
        print(f"\n[Environment Check]")
        for w in env["warnings"]:
            print(f"  ⚠️  {w}")
        print()

    result = render(args.snapshot, args.output_dir)

    print(f"\n{'='*50}")
    print(f"Status: {'SUCCESS' if result.success else 'FAILED'}")
    print(f"\nOutputs:")
    print(f"  Markdown:  {result.md_path or 'N/A'}")
    print(f"  HTML:      {result.html_path or 'N/A'}")
    print(f"  PDF:       {result.pdf_path or 'N/A'} (pages: {result.page_count})")
    print(f"  DOCX:      {result.docx_path or 'N/A'}")

    if result.warnings:
        print(f"\nWarnings ({len(result.warnings)}):")
        for w in result.warnings:
            print(f"  ⚠️  {w}")

    if result.errors:
        print(f"\nErrors ({len(result.errors)}):")
        for e in result.errors:
            print(f"  ❌ {e}")

    if result.engine_action:
        print(f"\nEngine Action Required:")
        print(json.dumps(result.engine_action, indent=2, ensure_ascii=False))

    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())
