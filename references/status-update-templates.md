# Status Update Templates

## Weekly Status Update

Published every Friday. Summarizes the week's progress, metrics, and outlook.

### Structure
1. Status panel with overall lozenge + metrics table (this week vs last week)
2. Highlights (bullet list of wins)
3. Concerns (bullet list of risks/blockers)
4. Per-Threat-Model Status table (model, status lozenge, done/total, notes)
5. Looking Ahead (next week priorities)

### Metrics to Include
| Metric | JQL |
|--------|-----|
| Total Controls | `labels = ThreatFocusedControl` |
| Completed | `labels = ThreatFocusedControl AND status in (Done, Closed, Cancelled)` |
| In Progress | `labels = ThreatFocusedControl AND status = "In Progress"` |
| Blocked | `labels = ThreatFocusedControl AND status = Blocked` |
| Unassigned | `labels = ThreatFocusedControl AND assignee = null` |

### Per-Threat-Model JQL
For each threat model, use:
- Done: `labels = ThreatFocusedControl and labels in (LABEL) AND status in (Done, Closed, Cancelled)`
- Total: `labels = ThreatFocusedControl and labels in (LABEL)`

### Status Lozenge Logic
- **Green (ON TRACK)**: Completion rate >= 70%, no blockers > 3 days
- **Yellow (AT RISK)**: Completion rate 40-69%, or blockers 3-5 days
- **Red (OFF TRACK)**: Completion rate < 40%, or blockers > 5 days, or unassigned > 5

### Slack Format (Alternative)
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

### Completion Rate Calculation
```
completion_rate = (done_count / total_count) * 100
```
Where done_count = Jira count for `status in (Done, Closed, Cancelled)`

### Monthly Narrative Template
"[Month] closed with [N]% of controls completed ([done]/[total]). [Key win]. [Key risk or concern]. Next month focuses on [priority]."

---

## Ad-Hoc Status Update

For urgent updates outside the normal cadence (incident, major milestone, scope change).

### Structure
1. Alert panel (red/yellow background based on severity)
2. What Happened (brief narrative)
3. Impact (what's affected)
4. Current Status (lozenge + metrics)
5. Next Steps (action items with owners)
6. Communication Plan (who needs to know, when)

### When to Use
- A threat model is significantly behind
- A major blocker is escalated
- Program scope changes (new threat model added/removed)
- Security incident affecting the program