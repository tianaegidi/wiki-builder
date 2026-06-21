# Status Update Templates

## Weekly Status Update

Published every Friday. Summarizes the week's progress, metrics, and outlook.

### Design Rules

- Uses `ac:layout` with `two_right_sidebar` (status reports are NOT edited live, so layout macros are OK)
- Main column: Overall Program Status panel, Executive Summary, metrics, per-threat-model views
- Sidebar: Quick links and metrics
- All Jira counts are live JQL macros (not hardcoded numbers)

### Structure

1. **Overall Program Status panel** — date, status lozenge (Red/Yellow/Green)
2. **Two-column layout** (`two_right_sidebar`):
   - Main column:
     - Executive Summary panel (2-3 sentence narrative)
     - Metrics table (Total/Open/Completed with live Jira count macros)
     - High Level Overview panel
     - Major Wins panel (bullet list)
     - Attention Required panel (bullet list)
     - Project Workstreams table (per-threat-model with Done/Open/Total Jira macros)
   - Sidebar:
     - Quick Links (Program Hub, PM Plan, Decision Log)

### Jira Count Macro

```python
def jira_count(jql):
    return f'''<ac:structured-macro ac:name="jira" ac:schema-version="1" ac:macro-id="{uuid.uuid4()}">
  <ac:parameter ac:name="server">Cloudflare Jira</ac:parameter>
  <ac:parameter ac:name="serverId">cc100dec-3d79-305b-8fae-4caba5e44cd2</ac:parameter>
  <ac:parameter ac:name="jqlQuery">{jql}</ac:parameter>
  <ac:parameter ac:name="count">true</ac:parameter>
</ac:structured-macro>'''
```

### Program-Level Metrics JQL

| Metric | JQL |
|--------|-----|
| Total | `labels = ThreatFocusedControl` |
| Completed | `labels = ThreatFocusedControl and status in (Done, Closed, Cancelled)` |
| In Progress | `labels = ThreatFocusedControl and status = "In Progress"` |
| Blocked | `labels = ThreatFocusedControl and status in (Blocked)` |
| Unassigned | `project = GRC AND labels = ThreatFocusedControl AND status NOT IN (Done, Cancelled) AND assignee = EMPTY` |

### Per-Threat-Model JQL

For each threat model in the workstream table:

```
Done:   labels = ThreatFocusedControl and labels in (LABEL) and status in (Done, Cancelled)
Open:   labels = ThreatFocusedControl and labels in (LABEL) and status not in (Done, Cancelled)
Total:  labels = ThreatFocusedControl and labels in (LABEL)
```

### Status Lozenge Logic

| Completion Rate | Blocked > 3 days | Unassigned > 5 | Lozenge |
|----------------|-------------------|-----------------|---------|
| >= 70% | No | No | Green (ON TRACK) |
| 40-69% | Yes | Yes | Yellow (AT RISK) |
| < 40% | Yes | Yes | Red (OFF TRACK) |

### Completion Rate Calculation

```
completion_rate = (done_count / total_count) * 100
```

Where done_count = Jira count for `status in (Done, Closed, Cancelled)`

### Full Template Code

See `scripts/create_status_update.py` for a complete working script template.

### Workflow

1. Ask user for: date, executive summary narrative, wins, concerns, overall status color
2. Fetch live Jira counts for all 8 threat models (or use Jira macros for live counts)
3. Create child page under `1424137842` (POST to API)
4. Add link to index table on `1424137842` — Friday Status Send-Out column
5. Update hub page `1276292540` if needed

---

## Monthly Executive Summary

Published at the end of each month. Higher-level than weekly updates, aimed at leadership.

### Structure
1. Executive Summary panel (2-3 sentence narrative + indicator table)
2. Wins This Month (bullet list)
3. Key Risks table (risk, impact, mitigation, owner)
4. Threat Model Progress table (model, wave, lead, completion %, status, key update)
5. Decisions This Month table (date, decision, rationale, decided by)
6. Focus Areas Next Month (numbered list)

### Indicator Table
| Indicator | Status Lozenge | Detail |
|-----------|---------------|--------|
| Overall Program Health | Green/Yellow/Red | Brief narrative |
| Controls Completion Rate | Green/Yellow/Red | [N%] ([Done]/[Total]) |
| Blocked Items | Green/Yellow/Red | [N] blocked, [N] > 3 days |
| Unassigned Tickets | Green/Yellow/Red | [N] tickets |

### Monthly Narrative Template
"[Month] closed with [N]% of controls completed ([done]/[total]). [Key win]. [Key risk or concern]. Next month focuses on [priority]."

---

## Slack Format (Alternative)

For Slack posts, use this format instead of a wiki page:

```
*Weekly Status — [Date]*

*Overall:* [emoji] [ON TRACK / AT RISK / OFF TRACK]

*Metrics:*
• Completed: [N]/[N] ([N%])
• In Progress: [N]
• Blocked: [N]
• Unassigned: [N]

*Highlights:*
• [Item 1]
• [Item 2]

*Concerns:*
• [Item 1]

*Next Week:*
• [Priority 1]

*Links:* [Dashboard] | [Latest Agenda] | [Decision Log]
```
