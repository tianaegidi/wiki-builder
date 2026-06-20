---
name: wiki-builder
title: All-in-One Program Wiki Builder
description: >-
  A portable OpenCode skill that manages the full lifecycle of a security program's
  Confluence presence on wiki.cfdata.org. Creates, edits, and revises wiki pages with
  live Jira macros, panels, tabs, and roadmaps. Generates weekly agendas, status updates,
  and executive summaries. Maintains a program hub page that stays in sync with child pages.
  Tracks decisions and meeting notes in a decision log.
kind: skill
metadata:
  team: security-pmo
  domain: wiki
  owners:
    - tianaegidi
  status: active
references:
  - SKILL.md
  - references/jira-reference.md
  - references/page-template.xml
  - references/agenda-templates.md
  - references/status-update-templates.md
  - references/decision-log-template.md
  - references/hub-page-pattern.md
  - scripts/update-handbook.py
---

# All-in-One Program Wiki Builder

A portable OpenCode skill that manages the full lifecycle of a security program's Confluence
presence on **wiki.cfdata.org**. Handles page creation, editing, weekly agendas, status updates,
hub page sync, and decision log tracking — all in clean **Storage Format** that stays editable.

> **Repo:** `github.com/tianaegidi/wiki-builder` · **Owner:** Tiana Egidi · **Status:** active

## What this skill does

| Capability | Description |
|---|---|
| **Create pages** | Build new wiki pages from scratch with any combination of macros |
| **Edit pages** | Update specific sections/tabs of existing pages without touching the rest |
| **Revise pages** | Reorganize content, add wave separators, update tables and panels |
| **Replicate pages** | Fetch an existing page, extract its macros/queries, rebuild it cleanly |
| **Generate agendas** | Weekly sync, quarterly review, and threat model review agendas with live Jira metrics |
| **Publish status updates** | Weekly status with trend tracking, monthly executive summaries |
| **Sync hub page** | Auto-update the hub page's Latest Status panel and Quick Links when child pages change |
| **Track decisions** | Immutable decision log with status lozenges, meeting notes archive |
| **Design UI** | 8 proven layout patterns (landing pages, dashboards, handbooks, agendas, decision logs) |
| **Dynamic data** | Jira count macros pull live ticket counts — no manual updates needed |

## Macros supported

- **Jira Issues Count** — live ticket counts with JQL queries
- **Panel** — colored bordered containers with optional headers
- **Status Lozenge** — Green/Blue/Yellow/Red/Grey status badges
- **Info** — contextual info boxes
- **UI Button** — styled buttons linking to external pages
- **UI Tabs** — tabbed content sections
- **Style (CSS)** — custom CSS (gradient headers, etc.)
- **Section/Column** — multi-column layouts
- **Expand** — collapsible sections (used for meeting notes archive)
- **Table Filter** (Stiltsoft) — filterable data tables
- **Roadmap Planner** (Stiltsoft) — timeline visualizations

## UI Design Patterns

The skill includes 8 battle-tested layout patterns:

| Pattern | Use for | Example |
|---|---|---|
| **Landing Page with Tabs** | Program homepages, hubs | Gradient header + welcome panel + tabs |
| **Program Health Dashboard** | Metrics at a glance | 2x2 colored panel grid with Jira counts |
| **Handbook / Reference** | How-to guides, runbooks | Roles table, workflows, escalation paths |
| **Workstreams / Tickets** | Ticket tracking | 3-column status cards + filterable table |
| **Timeline & Milestones** | Roadmaps, planning | Roadmap macro + status-tracked milestones |
| **Agenda Page** | Weekly syncs, reviews | Meeting details + timeboxed agenda + live metrics + spotlight |
| **Status Update Page** | Weekly/monthly reporting | Status lozenge + metrics table + highlights + concerns |
| **Decision Log Page** | Decision tracking | Immutable table + meeting notes expand archive |

## Weekly Program Workflow

| Day | Action |
|-----|--------|
| **Monday** | Generate agenda → Run sync → Log decisions → Log notes → Sync hub page |
| **Wednesday** | Mid-week Jira check → Flag new blockers |
| **Friday** | Generate status update → Sync hub page → Draft next week's agenda |
| **End of Month** | Generate executive summary → Sync hub page → Review decision log |
| **End of Quarter** | Quarterly review → Update program scope → Sync hub page |

## Installation

```sh
git clone https://github.com/tianaegidi/wiki-builder ~/.agents/skills/wiki-builder
```

Every AI tool that follows the `.agents/skills/` convention (OpenCode, Claude Code, Windsurf)
will discover the skill automatically.

| Tool | Discovery path |
|---|---|
| OpenCode | `~/.agents/skills/*/ SKILL.md` |
| Claude Code | `~/.agents/skills/*/ SKILL.md` |
| Windsurf | `~/.agents/skills/*/ SKILL.md` |

## Prerequisites

1. **Script**: Download `wikigen-generic.sh` to your home directory and make it executable:
   ```sh
   chmod +x ~/wikigen-generic.sh
   ```

2. **Cloudflared token**: Generate a short-lived token for wiki.cfdata.org:
   ```sh
   cloudflared access login https://wiki.cfdata.org/
   ```

3. **Python requests**: For page updates (avoids curl path corruption):
   ```sh
   pip3 install requests
   ```

4. **Jira access**: The skill uses the Cloudflare Jira app link (`cc100dec-3d79-305b-8fae-4caba5e44cd2`). No additional config needed.

## Usage

Once installed, the skill auto-triggers when you mention wiki.cfdata.org, Confluence,
program management, weekly agenda, status update, decision log, or ask to create/edit wiki pages.

### Create a page
```
Create a program health dashboard in INFOSEC with Jira counts for ThreatFocusedControl
```

### Edit a page
```
Edit the Ticket Handling Handbook tab on this page:
https://wiki.cfdata.org/spaces/INFOSEC/pages/1424133824
Add roles, workflows, escalation paths, and a definition of done
```

### Generate a weekly agenda
```
Create a weekly sync agenda for [date] with [attendees]. Spotlight: AI Security (Sonia)
```

### Publish a status update
```
Generate a weekly status update for the Threat-Focused Defense program. Highlights: [list]. Concerns: [list]
```

### Log a decision
```
Log a decision: Added AI Security as Wave 2 threat model. Rationale: emerging risk. Decided by: Tiana, Corinne
```

### Sync the hub page
```
Sync the hub page with the latest status update and agenda
```

## Real examples built with this skill

| Page | What it demonstrates |
|---|---|
| [TFD Program Hub](https://wiki.cfdata.org/spaces/INFOSEC/pages/1424133824) | Landing page with tabs, threat models table with wave separators, handbook, dashboard |
| [Ticket Handling Handbook](https://wiki.cfdata.org/spaces/INFOSEC/pages/1424133824#tab-Ticket+Handling+Handbook) | Handbook pattern: roles, workflows, escalation paths, DoD, label reference, weekly cadence |
| [Threat-focused Defense (Revamped)](https://wiki.cfdata.org/spaces/INFOSEC/pages/1424148786) | Revamped page with tabs, 2x2 dashboard, roadmap, milestones |

## Key lessons

- **Storage Format = editable.** Rendered HTML = locked editor. Always use XHTML storage format.
- **Jira macros** need `jqlQuery` (not `jql`), `server` + `serverId`, and `ac:schema-version` + `ac:macro-id`.
- **UI tabs** use `title` (not `name`), need `ac:schema-version` + `ac:macro-id`.
- **UI buttons** use `color=blue`, `url` (not `link`), no `textColor`.
- **Validate XML tag balance** before creating — mismatched tags cause API errors.
- **When editing pages**, fetch the current version first — pages can change between fetches.
- **No nested panels** when replacing content inside an existing panel.
- **Decision log entries are immutable** — if reversed, add a new entry with SUPERSEDED status.
- **Hub page sync** after every status update, agenda, or decision log entry.
- **Tool path corruption**: use `w"iki"` in URLs, use `/Users/tianaegidi/` instead of `/tmp/`.

## Repository map

| Path | What it is |
|---|---|
| [`SKILL.md`](SKILL.md) | The skill instructions — all 6 parts: page creation, agendas, status updates, hub sync, decision log, macro reference |
| [`references/jira-reference.md`](references/jira-reference.md) | Jira app link ID, common JQL patterns, threat model labels (Wave 1 + Wave 2) |
| [`references/page-template.xml`](references/page-template.xml) | Working page template with all macros properly configured |
| [`references/agenda-templates.md`](references/agenda-templates.md) | Weekly sync, quarterly review, threat model review, ad-hoc agenda templates |
| [`references/status-update-templates.md`](references/status-update-templates.md) | Weekly status, monthly executive summary, ad-hoc status templates |
| [`references/decision-log-template.md`](references/decision-log-template.md) | Decision log page structure, immutability rules, add decision/notes workflows |
| [`references/hub-page-pattern.md`](references/hub-page-pattern.md) | Hub page structure, sync triggers, sync code patterns |
| [`scripts/update-handbook.py`](scripts/update-handbook.py) | Example script for editing an existing page section |

*Confidential — Internal use only.*