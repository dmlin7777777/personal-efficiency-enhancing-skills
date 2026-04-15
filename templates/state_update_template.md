# STATE_UPDATE Output Template

## Purpose

Every expert node **MUST** append this block at the end of its output. `engine.py` parses this block to update `context_snapshot.json`.

If this block is missing or malformed, the output is rejected and a reformat request is triggered.

---

## Format

```
<!-- STATE_UPDATE -->
{
  "node": "<scout|architect_writer|architect_quantify|architect_wording|auditor_sincerity|auditor_compliance|auditor_interview|renderer>",
  "status": "<next_status_token>",
  "delta": {
    ... (only fields that changed)
  },
  "flags": [],
  "message": "<optional human-readable summary of what changed>"
}
<!-- /STATE_UPDATE -->
```

---

## Rules

1. **Must be the LAST content** in your response, after all user-facing output.
2. **Only include fields that actually changed** in `delta`. Do NOT echo unchanged fields.
3. **`status` determines next step** — must be a valid status token from `_meta.status` enum.
4. **`flags` array triggers engine actions**:
   - `["ROLLBACK"]` → engine sets `rollback_from`, reverts to specified phase
   - `["USER_INPUT_NEEDED"]` → engine pauses and waits for user response before next node
   - `["SKIP"]` → skip current sub-node (use sparingly, only with justification)
5. If you need to update nested objects (like `user_decisions.confirmed_quantifications`), include the full path in delta.

---

## Per-Node Delta Examples

### Context Scout (scout)

```json
{
  "node": "scout",
  "status": "match_review",
  "delta": {
    "jd_facts": {
      "capability_clusters": ["Data Engineering", "Cloud Architecture", "Stakeholder Management"],
      "market_notes": "Company focuses on AI-driven analytics platform. Values cross-functional collaboration."
    },
    "expert_outputs": {
      "scout_report": {
        "summary": "Mid-senior data role at a B2B SaaS company. Strong emphasis on end-to-end ownership.",
        "key_findings": [
          "Role values both technical depth and business communication",
          "No hard certification requirement but cloud experience preferred",
          "Cultural fit emphasis on 'scrappy' and 'fast-paced' language"
        ],
        "risk_flags": []
      }
    }
  },
  "flags": [],
  "message": "Scout phase complete. JD parsed, market research done. Ready for match review."
}
```

### Architect — Experience Selection (architect_writer)

```json
{
  "node": "architect_writer",
  "status": "phase_3_adjustment",
  "delta": {
    "user_decisions": {
      "kept_experiences": [
        {"id": "pwc", "label": "PwC Singapore — Data Analysis Intern", "position_order": 0},
        {"id": "valores", "label": "Valores Green Solutions — Data & Operations Specialist", "position_order": 1},
        {"id": "jiuqi", "label": "Jiuqi Software — Project Manager", "position_order": 2},
        {"id": "didi", "label": "DiDi Finance — Strategy Intern", "position_order": 3}
      ],
      "removed_experiences": ["tianzhi", "strowin"],
      "experience_metadata": {
        "pwc": {
          "company_name": "PwC Singapore",
          "job_title": "Data Analysis Intern",
          "department": "Financial Data & Systems",
          "date_range": "Mar 2026 – Present",
          "location": "Singapore (Hybrid)"
        },
        "valores": {
          "company_name": "Valores Green Solutions Pte Ltd",
          "job_title": "Data & Operations Specialist",
          "department": "Data & Operations",
          "date_range": "Oct 2025 – Mar 2026",
          "location": "Singapore"
        }
      }
    }
  },
  "metadata_completeness": {
    "complete": false,
    "missing_fields": [
      {"experience_id": "didi", "fields": ["department"]},
      {"experience_id": "jiuqi", "fields": ["department"]}
    ]
  },
  "flags": ["USER_INPUT_NEEDED"],
  "message": "Experience selection confirmed. Metadata collected for pwc and valores. Missing department info for didi + jiuqi — prompting user."
}
```

### Architect — Quantification (architect_quantify)

```json
{
  "node": "architect_quantify",
  "status": "phase_3_adjustment",
  "delta": {
    "user_decisions": {
      "confirmed_quantifications": {
        "jiuqi_b3": "Reduced monthly close cycle from 5 days to 6 hours across 12 business lines",
        "didi_b1": "Analyzed 50+ funding scenarios, identified 3 optimization opportunities reducing cost of capital by ~15 bps"
      }
    }
  },
  "flags": ["USER_INPUT_NEEDED"],
  "message": "2 bullets quantified after progressive probing. User unable to quantify 1 bullet — kept original per Anti-Filler Rule."
}
```

### Auditor — Sincerity Check (auditor_sincerity)

```json
{
  "node": "auditor_sincerity",
  "status": "audit_in_progress",
  "delta": {
    "expert_outputs": {
      "audit_report": {
        "overall_risk_level": "MEDIUM",
        "major_issues": [
          {
            "severity": "🔴 MAJOR",
            "category": "scope_inflation",
            "description": "Bullet '主导 AI Agent 方案设计' may overstate role for an intern-level position. Interviewer likely to probe actual decision authority.",
            "bullet_ref": "valores_b1",
            "suggested_fix": "Consider '参与 AI Agent 方案设计，负责需求分析与原型验证'"
          }
        ],
        "minor_issues": [
          {
            "severity": "🟡 MINOR",
            "category": "ai_trace",
            "description": "'实现智能化' vague phrasing detected in one removed bullet (not in final draft). No action needed.",
            "bullet_ref": null
          }
        ]
      }
    }
  },
  "flags": ["ROLLBACK"],
  "message": "🔴 MAJOR issue found: scope inflation in Valores bullet. Rolling back to Phase 3 for user correction."
}
```

### Renderer (renderer)

```json
{
  "node": "renderer",
  "status": "complete",
  "delta": {
    "expert_outputs": {
      "delivery_package": {
        "resume_docx": "history/2026-04-15_pwc_da.docx",
        "resume_pdf": "history/2026-04-15_pwc_da.pdf",
        "resume_md": "history/2026-04-15_pwc_da.md",
        "audit_log": "history/2026-04-15_pwc_da_audit.md"
      }
    }
  },
  "flags": [],
  "message": "All deliverables generated. Session ready for archive."
}
```

---

## Error Handling

### If JSON parse fails:

engine.py will detect the error and inject this prompt fragment for self-correction:

> Your previous response did not contain a valid STATE_UPDATE JSON block.
> Please re-output ONLY the STATE_UPDATE block with correct JSON syntax.
> Keep all delta values identical to what you intended in your previous response.

### If required field missing:

Same mechanism — engine returns the specific validation error message.

### If status transition is invalid:

Engine logs warning, keeps previous status, but still applies the delta changes.
