"""
Resume Tailor — Pipeline Engine (v3.0)

Pseudo Multi-Agent Orchestrator with Blackboard Architecture.

Core responsibilities:
  1. Initialize context_snapshot.json (Layer 1 via scripts)
  2. Run orchestration loop: read snapshot → call expert → parse STATE_UPDATE → merge
  3. Handle rollback on 🔴 Major audit issues
  4. Manage Active-to-Archive lifecycle
  5. Coordinate rendering pipeline

This module is the "gatekeeper" of state. Scripts handle facts; LLMs handle semantics;
this file handles flow control.
"""

import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

# ── Path Constants ──
BASE_DIR = Path(__file__).parent.parent  # resume-tailor/
SCHEMAS_DIR = BASE_DIR / "schemas"
TEMPLATES_DIR = BASE_DIR / "templates"
REFERENCES_DIR = BASE_DIR / "references"
SESSIONS_DIR = BASE_DIR / "sessions"
HISTORY_DIR = BASE_DIR / "history"
SCRIPTS_DIR = BASE_DIR / "scripts"

# Ensure scripts/ is in path for imports
_scripts_path = str(SCRIPTS_DIR)
if _scripts_path not in sys.path:
    sys.path.insert(0, _scripts_path)

# ── Lazy imports (only when needed) ──
def _import_jd_parser():
    from jd_parser import parse_jd, read_resume_text
    return parse_jd, read_resume_text

def _import_ats_checker():
    from ats_checker import run_checks
    return run_checks

def _import_diff_audit():
    from diff_audit import read_docx_structured
    return read_docx_structured


# ════════════════════════════════════════════════════════
# SNAPSHOT MANAGEMENT
# ════════════════════════════════════════════════════════

class Snapshot:
    """Manages context_snapshot.json lifecycle."""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.session_dir = SESSIONS_DIR / session_id
        self.snapshot_path = self.session_dir / "snapshot.json"
        self._data: dict = {}
        self._schema_path = SCHEMAS_DIR / "snapshot_schema_v1.json"

    def initialize(self, jd_text: str, resume_path: str,
                    company: str = None, role: str = None) -> dict:
        """Create new snapshot with Layer 1 populated by scripts."""
        self.session_dir.mkdir(parents=True, exist_ok=True)

        # Load schema for validation
        schema = self._load_schema()

        # --- Script layer: jd_parser.py (graceful degradation) ---
        parse_jd, read_resume_text = None, None
        resume_text = None
        jd_result = {}
        try:
            parse_jd, read_resume_text = _import_jd_parser()
            resume_text = read_resume_text(resume_path) if resume_path else None
            jd_result = parse_jd(jd_text, resume_text)
        except Exception as e:
            # Degrade gracefully: let Scout node handle extraction via LLM
            import traceback
            traceback.print_exc()
            print(f"[WARNING] jd_parser.py unavailable ({e}). "
                  f"Scout node will handle extraction via LLM.")

        # Build initial snapshot structure
        now_iso = datetime.now(timezone.utc).isoformat()
        self._data = {
            "_meta": {
                "version": "1.1",
                "session_id": self.session_id,
                "status": "initialized",
                "last_updated": now_iso,
                "current_node": None,
                "rollback_from": None,
                "error_log": [],
                # Rolling summary of recent turns for continuity
                "conversation_history": [],
            },
            "jd_facts": {
                "raw_jd_text": jd_text[:5000],  # Truncate to prevent bloat
                "role_title": role or jd_result.get("role_title", ""),
                "company_name": company,
                "region": jd_result.get("region", "unknown"),
                "role_level": jd_result.get("role_level", "unknown"),
                "hard_requirements": jd_result.get("requirements", []),
                "soft_requirements": jd_result.get("soft_requirements", []),
                "capability_clusters": jd_result.get("capability_clusters", []),
                "market_notes": None,  # Filled by Scout node
                "ats_keywords": jd_result.get("ats_keywords", []),
            },
            "user_decisions": {
                "resume_source_path": resume_path or "",
                "kept_experiences": [],
                "removed_experiences": [],
                "new_entries": [],
                "confirmed_quantifications": {},
                "confirmed_wording_changes": [],
                "regional_adaptations": {
                    "photo_action": "flag_for_review",
                    "personal_info_removals": [],
                    "tone_level": 3,  # Default neutral
                },
                "user_preferences": {
                    "output_format": "docx",
                    "page_limit": 1,
                    "include_shadow_resume": False,
                },
                # Semantic buffer: unstructured context that doesn't fit structured fields
                "nuance_buffer": [],
            },
            "expert_outputs": {
                "scout_report": None,
                "match_matrix": None,
                "writer_draft_path": None,
                "audit_report": None,
                "delivery_package": None,
            },
        }

        self._save()
        return self._data

    def load(self) -> dict:
        """Load existing snapshot from disk (for crash recovery)."""
        if not self.snapshot_path.exists():
            raise FileNotFoundError(f"Snapshot not found: {self.snapshot_path}")
        with open(self.snapshot_path, "r", encoding="utf-8") as f:
            self._data = json.load(f)
        return self._data

    def save(self) -> None:
        """Persist current snapshot to disk."""
        self._data["_meta"]["last_updated"] = datetime.now(timezone.utc).isoformat()
        self.session_dir.mkdir(parents=True, exist_ok=True)
        with open(self.snapshot_path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2, ensure_ascii=False)

    def get_context_for_node(self, node_name: str) -> str:
        """
        Build context string injected into LLM prompt.
        Includes: JD facts, user decisions, relevant nuance buffer, recent history.
        """
        d = self._data
        meta = d["_meta"]
        jf = d["jd_facts"]
        ud = d["user_decisions"]
        eo = d["expert_outputs"]

        lines = [
            f"=== {node_name.upper()} NODE CONTEXT ===",
            "",
            f"[JD Facts]",
            f"Role: {jf['role_title']}",
            f"Company: {jf['company_name'] or 'N/A'}",
            f"Region: {jf['region']} | Level: {jf['role_level']}",
            f"Hard Requirements: {_fmt_reqs(jf['hard_requirements'])}",
            f"ATS Keywords: {', '.join(jf.get('ats_keywords', [])[:20]) or 'N/A'}",
            "",
            f"[User Decisions]",
            f"Kept Experiences: {_fmt_experiences(ud.get('kept_experiences', []))} ",
            f"Removed: {ud.get('removed_experiences', [])} ",
            f"Quantifications: {json.dumps(ud.get('confirmed_quantifications', {}), ensure_ascii=False) or 'None yet'}",
            "",
        ]

        # --- Nuance Buffer (filtered by target_nodes or broadcast) ---
        nb = ud.get("nuance_buffer", [])
        if nb:
            relevant_nb = [
                entry for entry in nb
                if not entry.get("target_nodes") or node_name in entry.get("target_nodes", [])
            ]
            if relevant_nb:
                lines.append("[Nuance Buffer — Context from Previous Nodes]")
                for entry in relevant_nb[-5:]:  # Last 5 entries
                    src = entry.get("source_node", "?")
                    content = entry.get("content", "")
                    tags = entry.get("tags", [])
                    tag_str = f" [{', '.join(tags)}]" if tags else ""
                    lines.append(f"  [{src}]{tag_str}: {content}")
                lines.append("")

        # --- Conversation History (last 3 turns) ---
        hist = meta.get("conversation_history", [])
        if hist:
            recent = hist[-3:]  # Last N turns (configurable)
            lines.append(f"[Recent Context — Last {len(recent)} Turns]")
            for turn in recent:
                tnum = turn.get("turn_number", "?")
                tnode = turn.get("node", "?")
                summary = turn.get("summary", "")
                outputs = turn.get("key_outputs", [])
                outputs_str = f" | Outputs: {', '.join(outputs[:3])}" if outputs else ""
                lines.append(f"  Turn #{tnum} ({tnode}): {summary}{outputs_str}")
            lines.append("")

        # --- Expert Outputs (for downstream nodes) ---
        if eo.get("scout_report"):
            lines.append("[Scout Report]")
            lines.append(json.dumps(eo["scout_report"], indent=2, ensure_ascii=False)[:800])
            lines.append("")

        if eo.get("match_matrix"):
            lines.append("[Match Matrix]")
            lines.append(json.dumps(eo["match_matrix"], indent=2, ensure_ascii=False)[:800])
            lines.append("")

        if eo.get("writer_draft_path"):
            draft_path = BASE_DIR / eo["writer_draft_path"]
            if draft_path.exists():
                draft_content = draft_path.read_text(encoding="utf-8")
                lines.append(f"[Tailored Resume Draft ({eo['writer_draft_path']})]")
                lines.append(draft_content[:4000])
                if len(draft_content) > 4000:
                    lines.append(f"\n... [truncated, full at {eo['writer_draft_path']}]")
                lines.append("")

        lines.append("=" * 50)
        return "\n".join(lines)

    def apply_delta(self, delta: dict, new_status: str = None,
                     flags: list[str] = None) -> dict:
        """
        Merge a STATE_UPDATE delta into the snapshot.
        Uses deep merge for nested dicts.
        """
        flags = flags or []

        if new_status:
            self._data["_meta"]["status"] = new_status

        if "ROLLBACK" in flags:
            self._data["_meta"]["rollback_from"] = self._data["_meta"].get("status")
            self._log_error("ROLLBACK_TRIGGERED", "system", f"Rolling back from {new_status}")

        self._deep_merge(self._data, delta)
        self.save()
        return self._data

    def set_status(self, status: str, node: str = None) -> None:
        """Update status token and optionally current node."""
        self._data["_meta"]["status"] = status
        if node:
            self._data["_meta"]["current_node"] = node
        self.save()

    def archive(self) -> Path:
        """
        Move snapshot from sessions/ to history/ for long-term storage.
        Returns the archived path.
        """
        HISTORY_DIR.mkdir(parents=True, exist_ok=True)
        # Generate archive filename aligned with deliverables
        company = self._data["jd_facts"]["company_name"] or "unknown"
        role = self._data["jd_facts"]["role_title"] or "unknown"
        date_str = datetime.now().strftime("%Y-%m-%d")
        safe_name = f"{date_str}_{slugify(company)}_{slugify(role)}"
        archive_path = HISTORY_DIR / f"{safe_name}_snapshot.json"

        shutil.copy2(self.snapshot_path, archive_path)
        self._data["_meta"]["status"] = "archived"
        self._data["_meta"]["archived_at"] = datetime.now(timezone.utc).isoformat()
        self.save()
        return archive_path

    def cleanup_session(self) -> None:
        """Remove runtime session directory after successful archive."""
        if self.session_dir.exists():
            shutil.rmtree(self.session_dir)

    # ── Private helpers ──

    def _deep_merge(self, base: dict, update: dict) -> None:
        """Recursively merge update into base."""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value

    def _load_schema(self) -> dict:
        if self._schema_path.exists():
            with open(self._schema_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _log_error(self, code: str, node: str, message: str) -> None:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "node": node,
            "code": code,
            "message": message,
        }
        self._data["_meta"]["error_log"].append(entry)

    # ── Nuance Buffer & History ──

    def record_turn(self, turn_number: int, node: str,
                     summary: str, key_outputs: list[str] = None) -> None:
        """Append a compressed summary of this conversation turn to history."""
        entry = {
            "turn_number": turn_number,
            "node": node,
            "summary": summary,
            "key_outputs": key_outputs or [],
        }
        hist = self._data["_meta"].setdefault("conversation_history", [])
        hist.append(entry)
        # Keep only last 10 turns (maxItems from schema)
        if len(hist) > 10:
            self._data["_meta"]["conversation_history"] = hist[-10:]
        self.save()

    def add_nuance(self, source_node: str, content: str,
                   tags: list[str] = None,
                   target_nodes: list[str] = None) -> None:
        """
        Write an unstructured but important note into the nuance buffer.
        Use when you discover context that matters but has no structured field.
        """
        entry = {
            "source_node": source_node,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "content": content[:500],  # Truncate very long notes
            "tags": tags or [],
            "target_nodes": target_nodes or [],  # Empty = broadcast
        }
        buf = self._data["user_decisions"].setdefault("nuance_buffer", [])
        buf.append(entry)
        self.save()


# ════════════════════════════════════════════════════════
# STATE_UPDATE PARSER
# ════════════════════════════════════════════════════════

STATE_UPDATE_PATTERN = re.compile(
    r"<!-- STATE_UPDATE -->\s*(.*?)\s*<!-- /STATE_UPDATE -->",
    re.DOTALL
)

def parse_state_update(text: str) -> Optional[dict]:
    """
    Extract and parse STATE_UPDATE JSON block from LLM output.
    Returns parsed dict if found and valid, None otherwise.
    """
    match = STATE_UPDATE_PATTERN.search(text)
    if not match:
        return None

    try:
        data = json.loads(match.group(1))
        # Validate required fields
        if "node" not in data:
            return None
        return data
    except json.JSONDecodeError:
        return None


# ════════════════════════════════════════════════════════
# ORCHESTRATION LOOP
# ════════════════════════════════════════════════════════

# Status-to-node routing table
STATUS_ROUTING = {
    "initialized": ("scout", "contextual_intelligence"),
    "scout_complete": ("architect_writer", "semantic_matching"),
    "match_review": ("architect_writer", "experience_selection"),
    "phase_3_adjustment": ("architect_quantify", "quantification"),
    "writer_draft": ("auditor_compliance", "compliance_audit"),
    "audit_in_progress": ("auditor_sincerity", "reverse_audit"),
    "complete": ("renderer", "render_and_deliver"),
}

# Terminal statuses (loop exits when reached)
TERMINAL_STATUSES = {"complete", "archived", "rollback_requested"}

# Statuses where user input is expected (orchestrator pauses)
PAUSE_STATUSES = {"match_review", "phase_3_adjustment", "writer_draft"}


def run_orchestration_loop(snapshot: Snapshot,
                          llm_call_fn,  # Callable(node_name, context) -> str (LLM response text)
                          max_iterations: int = 20,
                          ) -> dict:
    """
    Main orchestration loop.

    Args:
        snapshot: Initialized Snapshot instance.
        llm_call_fn: Function that takes (node_name, context_string) and returns LLM response text.
                     In practice, this is the LLM API call with appropriate system prompt + user context.
        max_iterations: Safety limit to prevent infinite loops.

    Returns:
        Final snapshot data dictionary.
    """
    iteration = 0

    while iteration < max_iterations:
        iteration += 1
        status = snapshot._data["_meta"]["status"]

        # Check termination
        if status in TERMINAL_STATUSES:
            print(f"[Engine] Terminating at status={status} (iteration {iteration})")
            break

        # Determine next node
        if status not in STATUS_ROUTING:
            snapshot._log_error("INVALID_STATUS", "engine",
                               f"Unknown status: {status}. Defaulting to architect_writer.")
            status = "match_review"

        target_node, phase_name = STATUS_ROUTING[status]
        snapshot.set_status(status, target_node)

        print(f"[Engine] Iteration {iteration}: status={status} → node={target_node}")

        # Build context for this node
        context = snapshot.get_context_for_node(target_node)

        # Call LLM (this is where the actual work happens)
        try:
            llm_response = llm_call_fn(target_node, context)
        except Exception as e:
            snapshot._log_error("LLM_TIMEOUT", target_node, str(e))
            continue

        # Parse STATE_UPDATE
        update = parse_state_update(llm_response)

        if update is None:
            snapshot._log_error("JSON_PARSE_FAIL", target_node,
                               "No valid STATE_UPDATE block found in LLM output.")
            # Self-correction: inject reformat prompt
            # (In practice, this triggers a follow-up LLM call with correction instructions)
            print(f"[Engine] ⚠️ No STATE_UPDATE from {target_node}, retrying...")
            continue

        # Apply delta
        new_status = update.get("status", status)
        flags = update.get("flags", [])
        delta = update.get("delta", {})

        snapshot.apply_delta(delta, new_status, flags)

        # --- Record turn in conversation history ---
        llm_summary = update.get("message", f"Node {target_node} completed.")
        key_outputs = []
        if isinstance(delta, dict):
            for layer_name, layer_data in delta.items():
                if isinstance(layer_data, dict):
                    for k, v in layer_data.items():
                        if v and k not in ("removed_experiences",):
                            key_outputs.append(f"{layer_name}.{k}")
        snapshot.record_turn(iteration, target_node, llm_summary, key_outputs)

        # --- Extract nuance from STATE_UPDATE (if LLM included any) ---
        if isinstance(update.get("nuance"), list):
            for n in update["nuance"]:
                snapshot.add_nuance(
                    source_node=target_node,
                    content=n.get("content", ""),
                    tags=n.get("tags", []),
                    target_nodes=n.get("target_nodes"),
                )

        print(f"[Engine] ✓ Node {target_node} complete → status={new_status} flags={flags}")

        # Check for rollback trigger
        if "ROLLBACK" in flags:
            print(f"[Engine] 🔄 ROLLBACK triggered! Reverting to phase_3_adjustment.")
            snapshot.set_status("phase_3_adjustment", "architect_wording")
            # Don't break — loop continues with Architect node

    return snapshot._data


# ════════════════════════════════════════════════════════
# RENDERING PIPELINE
# ════════════════════════════════════════════════════════

def render_deliverables(snapshot: Snapshot) -> dict:
    """
    Render final outputs via the v3.0 rendering pipeline (renderer.py).

    Pipeline: Markdown → preprocess → Jinja2 HTML → PDF/DOCX
      - Phase 1: Regex preprocessing (**Summary**: content → <span>)
      - Phase 2: MD → HTML fragment (markdown-it-py / markdown)
      - Phase 3: Jinja2 layout with inline CSS
      - Phase 4a: WeasyPrint → PDF (with page overflow detection)
      - Phase 4b: pypandoc → DOCX (cleaner than HTML→Word)

    Returns RenderResult dict from renderer.render().
    """
    try:
        from renderer import render as run_renderer
        result = run_renderer(str(snapshot.snapshot_path))
        return {
            "success": result.success,
            "html_path": result.html_path,
            "pdf_path": result.pdf_path,
            "docx_path": result.docx_path,
            "md_path": result.md_path,
            "page_count": result.page_count,
            "warnings": result.warnings,
            "errors": result.errors,
            "engine_action": result.engine_action,
        }
    except Exception as e:
        snapshot._log_error("RENDER_FAILURE", "renderer", str(e))
        return {
            "success": False,
            "error": str(e),
            "html_path": None,
            "pdf_path": None,
            "docx_path": None,
        }


# ════════════════════════════════════════════════════════
# LEGACY COMPATIBILITY (v2.x interface)
# ════════════════════════════════════════════════════════

def run_full_pipeline(
    jd_path: str,
    resume_path: str = None,
    keywords: list = None,
    region: str = "global",
    json_output: bool = False,
) -> dict | str:
    """
    Legacy interface for backward compatibility.
    Runs v2.x-style single-pass pipeline without orchestration loop.
    New code should use Snapshot + run_orchestration_loop instead.
    """
    with open(jd_path, "r", encoding="utf-8") as f:
        jd_text = f.read()

    parse_jd, read_resume_text = _import_jd_parser()
    resume_text = read_resume_text(resume_path) if resume_path else None
    jd_result = parse_jd(jd_text, resume_text)

    ats_result = None
    if resume_text:
        run_checks = _import_ats_checker()
        ats_result = run_checks(resume_text, keywords=keywords or [], region=region)

    output = {
        "jd_analysis": jd_result,
        "resume_structure": None,
        "ats_check": ats_result,
    }

    if json_output:
        return output

    import io
    from contextlib import redirect_stdout
    from jd_parser import print_report
    from ats_checker import format_markdown

    lines = []
    buf = io.StringIO()
    with redirect_stdout(buf):
        print_report(jd_result)
    lines.append(buf.getvalue())

    if ats_result:
        lines.append("\n" + format_markdown(ats_result))

    return "\n".join(lines)


# ════════════════════════════════════════════════════════
# UTILITIES
# ════════════════════════════════════════════════════════

def slugify(text: str) -> str:
    """Convert text to URL-safe slug."""
    return re.sub(r'[^a-z0-9_]+', '_', text.lower()).strip('_')


def _fmt_reqs(reqs: list) -> str:
    """Format requirements list compactly."""
    if not reqs:
        return "None specified"
    return ", ".join(f"{r.get('value', '?')}({r.get('met', '?')})" for r in reqs[:10])


def _fmt_experiences(exps: list) -> str:
    """Format experiences list compactly."""
    if not exps:
        return "None selected yet"
    return ", ".join(e.get("label", e.get("id", "?")) for e in exps)


# ── Session ID Generator ──

def generate_session_id(company: str, role: str) -> str:
    """Generate unique session ID: YYYYMMDD_company_role"""
    date_str = datetime.now().strftime("%Y%m%d")
    return f"{date_str}_{slugify(company)}_{slugify(role)}"
