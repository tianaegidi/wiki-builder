---
name: wiki-builder
title: All-in-One Wiki Page Creator, Editor & Designer
description: >-
  A portable OpenCode skill that creates, edits, and designs Confluence wiki pages
  on wiki.cfdata.org with live Jira macros, panels, status lozenges, tabs, roadmaps,
  and table filters — all in clean, editable Storage Format.
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
  - scripts/update-handbook.py
---

# All-in-One Wiki Page Creator, Editor & Designer

A portable OpenCode skill that builds, edits, and designs Confluence wiki pages on
**wiki.cfdata.org**. Creates pages with live Jira data, polished UI (gradient headers,
color-coded panels, tabs, status lozenges), and Stiltsoft macros — all in clean
**Storage Format** that stays editable (no locked editors).

> **Repo:** `github.com/tianaegidi/wiki-builder` · **Owner:** Tiana Egidi · **Status:** active

## What this skill does

| Capability | Description |
|---|---|
| **Create pages** | Build new wiki pages from scratch with any combination of macros |
| **Edit pages** | Update specific sections/tabs of existing pages without touching the rest |
| **Replicate pages** | Fetch an existing page, extract its macros/queries, rebuild it cleanly |
| **Design UI** | Apply proven layout patterns (landing pages, dashboards, handbooks, timelines) |
| **Dynamic data** | Jira count macros pull live ticket counts — no manual updates needed |

## Macros supported

- **Jira Issues Count** — live ticket counts with JQL queries
- **Panel** — colored bordered containers with optional headers
- **Status Lozange** — Green/Blue/Yellow/Red/Grey status badges
- **Info** — contextual info boxes
- **UI Button** — styled buttons linking to external pages
- **UI Tabs** — tabbed content sections
- **Style (CSS)** — custom CSS (gradient headers, etc.)
- **Section/Column** — multi-column layouts
- **Expand** — collapsible sections
- **Table Filter** (Stiltsoft) — filterable data tables
- **Roadmap Planner** (Stiltsoft) — timeline visualizations

## UI Design Patterns

The skill includes 5 battle-tested layout patterns:

| Pattern | Use for | Example |
|---|---|---|
| **Landing Page with Tabs** | Program homepages, hubs | Gradient header + welcome panel + tabs |
| **Program Health Dashboard** | Metrics at a glance | 2x2 colored panel grid with Jira counts |
| **Handbook / Reference** | How-to guides, runbooks | Roles table, workflows, escalation paths |
| **Workstreams / Tickets** | Ticket tracking | 3-column status cards + filterable table |
| **Timeline & Milestones** | Roadmaps, planning | Roadmap macro + status-tracked milestones |

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

3. **Jira access**: The skill uses the Cloudflare Jira app link (`cc100dec-3d79-305b-8fae-4caba5e44cd2`). No additional config needed.

## Usage

Once installed, the skill auto-triggers when you mention wiki.cfdata.org, Confluence,
dashboards, or ask to create/edit wiki pages.

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

### Revamp a page

```
Revamp this wiki page with tabs, panels, and live Jira data:
https://wiki.cfdata.org/spaces/INFOSEC/pages/1276292540
```

### Replicate a page

```
Recreate this page as a child page under it with the same macros and styling:
https://wiki.cfdata.org/spaces/INFOSEC/pages/1424133824
```

## Real examples built with this skill

| Page | What it demonstrates |
|---|---|
| [Ticket Handling Handbook](https://wiki.cfdata.org/spaces/INFOSEC/pages/1424133824#tab-Ticket+Handling+Handbook) | Handbook pattern: roles, workflows, escalation paths, DoD, label reference, weekly cadence |

## Key lessons

- **Storage Format = editable.** Rendered HTML = locked editor. Always use XHTML storage format.
- **Jira macros** need `jqlQuery` (not `jql`), `server` + `serverId`, and `ac:schema-version` + `ac:macro-id`.
- **UI tabs** use `title` (not `name`), need `ac:schema-version` + `ac:macro-id`.
- **UI buttons** use `color=blue`, `url` (not `link`), no `textColor`.
- **Validate XML tag balance** before creating — mismatched tags cause API errors.
- **When editing pages**, fetch the current version first — pages can change between fetches.

## Repository map

| Path | What it is |
|---|---|
| [`SKILL.md`](SKILL.md) | The skill instructions — macro reference, design patterns, workflows |
| [`references/jira-reference.md`](references/jira-reference.md) | Jira app link ID, common JQL patterns, threat model labels |
| [`references/page-template.xml`](references/page-template.xml) | Working page template with all macros properly configured |
| [`scripts/update-handbook.py`](scripts/update-handbook.py) | Example script for editing an existing page section |

*Confidential — Internal use only.*