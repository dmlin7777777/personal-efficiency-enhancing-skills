# Changelog

All notable changes to this project will be documented in this file.

## [3.0.0] - 2026-04-15

### Added
- **Pseudo-Multi-Agent Architecture**: Isolated expert nodes (Scout / Architect / Auditor) with blackboard state management via `context_snapshot.json`
- **4-Layer Snapshot Schema (v1.1)**: `_meta` / `facts` / `user_decisions` / `outputs` with JSON Schema validation
- **HTML Rendering Pipeline** (`scripts/renderer.py`):
  - Phase 1: Regex preprocessing for bullet summary pattern (`**Summary**: detail` → `<span class="bullet-summary">`)
  - Phase 2: Markdown → HTML conversion via markdown-it-py (with markdown fallback)
  - Phase 3: Jinja2 template layout with CSS inlining
  - Phase 4a: WeasyPrint PDF output with `len(doc.pages)` overflow detection → triggers Architect compression
  - Phase 4b: pypandoc DOCX output (clean MD→Word, avoids HTML→Word formatting chaos)
- **Jinja2 Layout Template** (`templates/resume_layout.html.j2`): HTML skeleton with inline CSS injection and hidden render metadata
- **CSS Template v3.0** (`templates/resume_template.css`): Tech Style, single-column flow layout:
  - Dual font stack: Times New Roman (Latin/Digits) + Microsoft YaHei (CJK)
  - Flexible 2-row experience header: Company · **Title** \| Date + *Department* \| Location
  - `.bullet-summary` bold prefix styling for structured bullets
  - Compact spacing with dynamic content adjustment (target ≤1 page)
  - Print optimization (`@page`, `break-inside: avoid`, color-adjust)
- **Nuance Buffer**: Layer 2 field for caching unstructured but important context between nodes
- **Conversation History Compression**: Last 3 turns auto-injected into node prompts for continuity
- **Mandatory Experience Metadata Enforcement**: Writer Guide CP1 now enforces 5-field completeness (Company, Title, Department, Date, Location)
- **Environment Check Function**: `check_rendering_environment()` detects fonts (Windows/macOS/Linux), WeasyPrint availability, pandoc installation
- **Writer Guide CP5 Section**: Complete draft finalization guide with rendering-aware Markdown rules, allowed/disallowed syntax tables, self-check checklist
- **Architecture Design Document**: `docs/plans/2026-04-15-v3-architecture-design.md` (full system design)

### Changed
- **SKILL.md**: Streamlined from monolithic instructions to ~220-line routing table (delegates detail work to reference guides)
- **engine.py**: Replaced placeholder `render_deliverables()` with actual renderer.py integration; added `record_turn()`, `add_nuance()`, `get_context_for_node()` methods
- **STATE_UPDATE Template**: New example showing `metadata_completeness` tracking and `experience_metadata` structure
- **README.md / README.zh-CN.md**: Fully rewritten for v3.0 architecture

### Fixed
- **Regex Bug**: Bullet summary pattern changed from `re.DOTALL` to `re.MULTILINE` with line anchoring — previous greedy matching would consume entire document content
- **Font Detection False Positive**: CJK font check now uses alias-based matching — "Microsoft YaHei" registry entry correctly satisfies both English and Chinese name requirements
- **Duplicate Functions**: Removed redundant `_check_fonts_macos()` and `_check_fonts_linux()` definitions from renderer.py

### Technical Decisions
- Jinja2 chosen over string concatenation for all HTML generation
- WeasyPrint chosen over pdfkit for proper Flexbox/Grid/CSS print support
- pypandoc chosen for DOCX to avoid cross-engine formatting issues
- Renderer follows READ-ONLY contract on snapshot files (returns actions, never writes back)

---

## [2.5] - 2026-04-15

### Added
- Architecture design exploration: pseudo-multi-agent + blackboard pattern
- Design document: v2.5 architecture plan (512 lines)

---

## [2.4] - 2026-04-14

### Added
- 4-stage pipeline (Contextual Intelligence → Strict Matching → Dynamic Interaction → Delivery & Reverse Audit)
- 3-tier routing system (job type / user intent / edge cases)
- Unified feature extraction across all resume formats
- Anti-Filler Rule: every bullet must have Action + Object + Measurable Outcome
- Propose-don't-ask principle: always give concrete recommendations first
- Reverse Audit: physically isolated auditor persona review
- Shadow Resume moved from automatic to on-demand trigger
- README product rewrite with bilingual support (EN/ZH-CN)

---

## [2.3] - Earlier

- Initial skill implementation
- Basic JD parsing and resume matching
