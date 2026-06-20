---
name: wiki-builder
title: TFD Program Wiki Builder
description: >-
  All-in-one program management skill for the Threat-Focused Defense (TFD) program on
  wiki.cfdata.org. Manages 5 specific wiki pages — program hub, Q1 update, project
  management plan, status updates, and notes/decision log. Creates and edits pages,
  generates weekly agendas and status updates, maintains the hub page, and tracks
  decisions. Purpose-built for TFD — not a generic wiki tool.
kind: skill
metadata:
  team: security-pmo
  domain: wiki
  program: threat-focused-defense
  owners:
    - tianaegidi
  status: active
references:
  - SKILL.md
  - references/jira-reference.md
  - references/page-inventory.md
  - references/page-template.xml
  - references/agenda-templates.md
  - references/status-update-templates.md
  - references/decision-log-template.md
  - references/hub-page-pattern.md
  - scripts/update-handbook.py
---

# TFD Program Wiki Builder

All-in-one skill for managing the **Threat-Focused Defense (TFD)** program's Confluence
presence on wiki.cfdata.org. Controls exactly 5 wiki pages plus their child pages.
Handles page creation/editing, weekly agendas, status updates, hub page sync, and
decision log tracking.

> **Repo:** `github.com/tianaegidi/wiki-builder` · **Owner:** Tiana Egidi · **Status:** active

## Controlled Pages

| Page | ID | Purpose |
|------|-----|---------|
| TFD Program Hub [draft] | `1424133824` | Main landing page with 7 tabs (blue theme) |
| Q1 Update | `1346668357` | Quarterly briefing (orange theme, 9 tabs) |
| Project Management Plan | `1419363218` | TPM tracker (two-column w/ sidebar) |
| TFD Status Updates 2026 | `1424137842` | Index for weekly agendas + status send-outs |
| Notes | `1346668352` | Decision log & meeting notes (to be built out) |

## Capabilities

| Capability | Description |
|---|---|
| **Create pages** | Build new wiki pages (agendas, status updates) as children of the 5 controlled pages |
| **Edit pages** | Update specific sections/tabs of existing pages without touching the rest |
| **Revise pages** | Reorganize content, add wave separators, update tables and panels |
| **Generate agendas** | Weekly sync agendas with live Jira metrics, matching existing 6/17/26 format |
| **Publish status updates** | Friday status send-outs with per-threat-model metrics, matching 6/19/26 format |
| **Sync hub page** | Update hub page when status updates, agendas, or decisions are published |
| **Track decisions** | Immutable decision log on the Notes page with meeting notes archive |
| **Manage Q1 Update** | Update quarterly briefing with new metrics, tabs, and threat model data |
| **Manage PM Plan** | Update TPM tracker with action items, people, and ticket counts |

## Weekly Workflow

| Day | Action |
|-----|--------|
| **Monday** | Create agenda → Run sync → Log decisions → Log notes → Sync hub |
| **Wednesday** | Mid-week Jira check → Flag blockers → Update PM Plan if needed |
| **Friday** | Create status update → Add to index → Sync hub → Draft next week's agenda |
| **End of Month** | Executive summary → Review decision log → Update PM Plan metrics |
| **End of Quarter** | Update Q1/Q2/Q3/Q4 page → Quarterly review → Update program scope |

## Installation

```sh
git clone https://github.com/tianaegidi/wiki-builder ~/.agents/skills/wiki-builder
```

## Prerequisites

1. **Script**: `~/wikigen-generic.sh` (executable)
2. **Cloudflared token**: `cloudflared access login https://wiki.cfdata.org/`
3. **Python requests**: `pip3 install requests`
4. **Jira app link ID**: `cc100dec-3d79-305b-8fae-4caba5e44cd2`

## Usage Examples

### Create a weekly agenda
```
Create a weekly TFD sync agenda for [date]. Attendees: [list]. Spotlight: AI Security (Sonia)
```

### Publish a status update
```
Generate a TFD status update for [date]. Status: Red. Wins: [list]. Concerns: [list]
```

### Edit the hub page
```
Update the Program Overview tab on the TFD hub page — add a new threat model to Wave 2
```

### Log a decision
```
Log a decision to the TFD decision log: [decision]. Rationale: [why]. Decided by: [names]
```

### Update the PM Plan
```
Add a new action item to the PM Plan page: [action]. Owner: [name]. Due: [date]
```

## Real Pages Built with This Skill

| Page | What it demonstrates |
|---|---|
| [TFD Program Hub](https://wiki.cfdata.org/spaces/INFOSEC/pages/1424133824) | 7-tab landing page, threat models table with waves, 2x2 dashboard, handbook |
| [Q1 Update](https://wiki.cfdata.org/spaces/INFOSEC/pages/1346668357) | 9-tab quarterly briefing, 59 Jira links, orange theme |
| [PM Plan](https://wiki.cfdata.org/spaces/INFOSEC/pages/1419363218) | Two-column TPM tracker, ticket tracking, people management |
| [6/17/26 Agenda](https://wiki.cfdata.org/spaces/INFOSEC/pages/1424137886) | Two-column weekly agenda with status, artifacts, and agenda table |
| [6/19/26 Status](https://wiki.cfdata.org/spaces/INFOSEC/pages/1424152018) | Two-column status update with 24 JQL queries, exec summary, wins/concerns |

## Repository Map

| Path | What it is |
|---|---|
| [`SKILL.md`](SKILL.md) | Main skill — 8 parts: page editing, agendas, status updates, hub sync, decision log, Q1 update, PM plan, weekly workflow |
| [`references/jira-reference.md`](references/jira-reference.md) | Jira app link ID, all TFD JQL patterns, threat model labels (Wave 1 + 2) |
| [`references/page-inventory.md`](references/page-inventory.md) | All 5 page IDs, hierarchy, design themes, tab inventories |
| [`references/page-template.xml`](references/page-template.xml) | Working page template with all macros |
| [`references/agenda-templates.md`](references/agenda-templates.md) | Weekly sync, quarterly review, threat model review agenda templates |
| [`references/status-update-templates.md`](references/status-update-templates.md) | Weekly status, monthly exec summary, ad-hoc status templates |
| [`references/decision-log-template.md`](references/decision-log-template.md) | Decision log structure, immutability rules, add decision/notes workflows |
| [`references/hub-page-pattern.md`](references/hub-page-pattern.md) | Hub page sync triggers and code patterns |
| [`scripts/update-handbook.py`](scripts/update-handbook.py) | Example script for editing an existing page section |

*Confidential — Internal use only. TFD Program.*