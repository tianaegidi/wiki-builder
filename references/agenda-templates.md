# Agenda Templates

## Weekly Sync Agenda (30 min)

Standing weekly meeting to review program health, spotlight a threat model, and triage blockers.

### Structure
1. Meeting Details panel (date, time, attendees, facilitator, note taker)
2. Agenda table (timeboxed topics)
3. Dashboard Snapshot panel (live Jira counts)
4. Threat Model Spotlight (expand macro, rotating each week)
5. Blockers & Escalations table
6. Action Items table
7. Decisions Made table

### Agenda Timebox
| Time | Topic | Owner | Type |
|------|-------|-------|------|
| 0:00 | Roll call + agenda review | Facilitator | Standing |
| 0:02 | Program health dashboard review | TPM | Standing |
| 0:10 | Threat model spotlight (rotating) | Lead Assessor | Rotating |
| 0:20 | Blockers & escalations | Open floor | Standing |
| 0:25 | Action items + next week preview | Facilitator | Standing |

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

### Dashboard Snapshot JQL
- Total: `labels = ThreatFocusedControl`
- Completed: `labels = ThreatFocusedControl AND status in (Done, Closed, Cancelled)`
- In Progress: `labels = ThreatFocusedControl AND status = "In Progress"`
- Blocked: `labels = ThreatFocusedControl AND status = Blocked`
- Unassigned: `labels = ThreatFocusedControl AND assignee = null`

---

## Quarterly Review Agenda (90 min)

End-of-quarter review covering wins, misses, process retro, and next quarter planning.

### Structure
1. Review Scope panel (date, duration, attendees)
2. Agenda table
3. Quarter Metrics Summary table (start vs end of quarter)
4. Threat model deep dive (each lead presents)
5. Process retro (what worked, what didn't)
6. Next quarter planning (scope, priorities, resourcing)
7. Action items + commitments

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

### Structure
1. Review Details panel (threat model, lead, date, duration)
2. Agenda table
3. Control Coverage table (each control, status, owner, due, notes)
4. Risk gap analysis
5. Next steps + resource needs
6. Action items

### Agenda Timebox
| Time | Topic |
|------|-------|
| 0:00 | Threat model overview + scope confirmation |
| 0:10 | Control coverage review (done, in progress, missing) |
| 0:25 | Risk gap analysis — unaddressed threats |
| 0:35 | Next steps + resource needs |
| 0:40 | Action items |

### When to Use
- When a threat model is behind schedule
- When adding a new threat model (Wave 2 onboarding)
- Before quarterly review for each model
- When blockers persist for > 2 weeks

---

## Ad-Hoc Agenda Template

For unscheduled meetings (incident response, urgent scope changes, etc.)

### Structure
1. Meeting Details panel
2. Objectives list (what needs to be decided)
3. Discussion topics table
4. Decisions table
5. Action items table

### Workflow
1. Ask user: what's the meeting about, who's attending, what needs to be decided
2. Generate page with objectives clearly stated
3. After meeting, append decisions and action items
4. Log decisions to the decision log page
5. Update hub page if scope changed