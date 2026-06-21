# Agenda Templates

## Weekly Sync Agenda (30 min)

Standing weekly meeting to review program health, spotlight a threat model, and triage blockers.

### Design Rules (CRITICAL)

- **NO `ac:layout` macros** — they lock the Confluence editor, making real-time note-taking impossible
- **NO expand macros for discussion items** — use bullet lists for live note-taking
- **NO panel macros for section headers** — use colored table cells instead
- Colored section headers use single-cell tables with inline `style="background-color: #color; color: #FFFFFF;"` (NOT `highlight-#color` class — doesn't render reliably)

### Helper Functions

```python
def colored_header(text, color):
    return f'<table class="wrapped" style="width: 100%;"><tbody><tr><td style="background-color: {color}; color: #FFFFFF;"><strong>{text}</strong></td></tr></tbody></table>'

def th(color, text):
    return f'<th style="background-color: {color}; color: #FFFFFF;"><strong>{text}</strong></th>'

def status_lozenge(color, title_text):
    return f'<ac:structured-macro ac:name="status" ac:schema-version="1" ac:macro-id="{uuid.uuid4()}"><ac:parameter ac:name="subtle">true</ac:parameter><ac:parameter ac:name="colour">{color}</ac:parameter><ac:parameter ac:name="title">{title_text}</ac:parameter></ac:structured-macro>'
```

### Structure (6 Sections + Parking Lot)

```
1) Project Status          (blue header #0052cc)
2) Progress Updates         (purple header #6554C0)
3) Status by Workstream     (orange header #FF8B00)
4) Discussion Items         (red header #DE350B)
5) Notes                    (grey header #6B778C)
6) Next Steps               (green header #36B37E)
Parking Lot                 (light grey header #97a0af)
```

### Section Details

**1) Project Status** — Overall status lozenge, on track/at risk/blocked, key wins, blockers, DoD, path to green. Followed by Project Artifacts sub-section (links to PM Plan, Hub, Decision Log, Email Template).

**2) Progress Updates** — 4-column table (Update, Owner, Progress made, Follow-up). One row per update item since last meeting.

**3) Status by Workstream** — 5-column table (Workstream, Status, What changed, Next milestone, Owner). Rows for Wave 1, Wave 2, Wave 3 with status lozenges.

**4) Discussion Items** — Each item as `<h3>` + bullet list (NOT expand macros). Bullets: Question, Context, Decision needed, Owner, Timebox.

**5) Notes** — Simple bullet list of helpful context and parked tangents.

**6) Next Steps** — 4-column table (Action item, Owner, Due date, Status) with status lozenges.

**Parking Lot** — Simple bullet list of topics to revisit later.

### Full Template Code

See `scripts/create_agenda.py` for a complete working script template.

### Threat Model Spotlight Rotation

Cycle through all threat models in order:
1. Compromise of Core/Edge Infrastructure
2. Malicious Insider Risk
3. Compromise or Physical Tampering of Hardware
4. B2B SaaS Integration & Supply Chain Exploitation
5. Software Supply Chain
6. Unauthorized Access to Customer Data
7. Customer Zero Threats
8. AI Security

Each spotlight covers: current status, progress this week, next steps, risks/blockers.

### Dashboard Snapshot JQL (for reference in agenda)

- Total: `labels = ThreatFocusedControl`
- Completed: `labels = ThreatFocusedControl AND status in (Done, Closed, Cancelled)`
- In Progress: `labels = ThreatFocusedControl AND status = "In Progress"`
- Blocked: `labels = ThreatFocusedControl AND status = Blocked`
- Unassigned: `project = GRC AND labels = ThreatFocusedControl AND status NOT IN (Done, Cancelled) AND assignee = EMPTY`

---

## Quarterly Review Agenda (90 min)

End-of-quarter review covering wins, misses, process retro, and next quarter planning.

### Agenda Timebox
| Time | Topic | Owner |
|------|-------|-------|
| 0:00 | Quarter recap — wins, misses, metrics | TPM |
| 0:15 | Threat model deep dive (each lead presents) | Lead Assessors |
| 0:45 | Process retro — what worked, what didn't | Open floor |
| 0:60 | Next quarter planning — scope, priorities, resourcing | TPM + Sponsors |
| 0:80 | Action items + commitments | Facilitator |

### Quarter Metrics to Track
- Total Controls (start vs end)
- Completed (start vs end)
- Blocked average (start vs end)
- Completion rate percentage

---

## Threat Model Review Agenda (45 min)

Deep dive on a single threat model to assess control coverage and identify gaps.

### When to Use
- When a threat model is behind schedule
- When adding a new threat model (Wave 2 onboarding)
- Before quarterly review for each model
- When blockers persist for > 2 weeks
