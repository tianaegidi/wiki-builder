---
name: wiki-builder
description: All-in-one program management skill for the Threat-Focused Defense (TFD) program on wiki.cfdata.org. Manages 5 specific wiki pages — the program hub, Q1 update, project management plan, status updates, and notes/decision log. Creates and edits pages, generates weekly agendas and status updates, maintains the hub page, and tracks decisions. Use when the user mentions TFD, Threat-Focused Defense, wiki.cfdata.org TFD pages, weekly agenda, status update, decision log, or any of the 5 program pages.
---

# TFD Program Wiki Builder

Reliable tool for managing the **Threat-Focused Defense (TFD)** program's Confluence presence on wiki.cfdata.org. Built for any program manager to pick up and use.

## What This Skill Does

Four core tasks:

1. **Keep the Program Hub updated** — page ID `1276292540`
2. **Keep the Status Updates index updated** — page ID `1424137842`
3. **Create weekly agendas** — child pages under the index
4. **Create weekly status reports** — child pages under the index

## Prerequisites

1. **Cloudflared token**: Run `cloudflared access login https://wiki.cfdata.org/` (and separately for `https://jira.cfdata.org/`)
2. **Python requests**: `pip3 install requests`
3. **wikigen-generic.sh**: `~/wikigen-generic.sh` must exist and be executable (alternative page creation method)

### Optional: Google Drive Integration

If the Google Workspace MCP server is enabled (via opencode portal), this skill can automatically search and read Gemini meeting notes from Google Drive. This is **optional** — the user can choose to use it or provide notes manually.

**When to use Google Drive integration:**
- User says "pull from my Gemini notes" or "check my Drive"
- User wants the agenda/status update auto-populated from meeting notes
- User references meeting notes without pasting content

**When NOT to use (user provides input manually):**
- User pastes notes directly in chat
- User shares a Google Doc URL
- User dictates what to include
- Google Workspace MCP server is not available

**How it works:**
1. Search Google Drive for recent "Notes by Gemini" docs (filtered by date range and TFD-relevant keywords)
2. Read each doc's content (converted to markdown)
3. Parse out: decisions, action items, discussion topics, blockers, wins
4. Filter out irrelevant content (transcript filler, Gemini boilerplate, non-TFD meetings)
5. Combine with previous week's Confluence agenda for continuity
6. Use extracted info to populate the new agenda or status update

**Drive search patterns:**
```
"name contains 'Notes by Gemini'"           — all Gemini notes
"name contains 'threat focused defense'"    — TFD-specific meetings
"name contains 'TFD'"                       — TFD-tagged docs
"name contains 'status'"                    — status review docs
```

**Parsing rules:**
- Extract from Gemini "Summary", "Decisions", "Next steps", and "Details" sections
- Ignore transcript section (too verbose, mostly filler)
- Ignore Gemini boilerplate (surveys, "review notes" disclaimers)
- Map action items to agenda "Next Steps" section
- Map decisions to Decision Log entries
- Map discussion topics to agenda "Discussion Items" section

## Tool Bug Workarounds

- `wiki` → `iki` in bash — use `w"iki"` in URLs or use Python `requests` instead
- `tmp` → `ttp` in bash — use `/Users/tianaegidi/` for temp files
- `issues` → `isses` — always verify Jira URLs in generated content

---

## Page Inventory

All pages under: `INFOSEC > Security Team Home > Security Programs > GRC Program > Threat-focused Defense`

| Page | ID | URL | Role |
|------|-----|-----|------|
| **Program Hub** | `1276292540` | [Link](https://wiki.cfdata.org/spaces/INFOSEC/pages/1276292540) | Main landing page with 8 tabs |
| **Status Updates 2026** | `1424137842` | [Link](https://wiki.cfdata.org/spaces/INFOSEC/pages/1424137842) | Index page linking to weekly agendas + status reports |
| **Decision Log** | `1346668352` | [Link](https://wiki.cfdata.org/spaces/INFOSEC/pages/1346668352) | Immutable decision log & meeting notes |
| **Q1 Update** | `1346668357` | [Link](https://wiki.cfdata.org/spaces/INFOSEC/pages/1346668357) | Quarterly briefing (orange theme) |
| **PM Plan** | `1419363218` | [Link](https://wiki.cfdata.org/spaces/INFOSEC/pages/1419363218) | TPM tracker (two-column w/ sidebar) |

### Hierarchy

```
Threat-focused Defense (1276292540) ← Program Hub (LIVE)
├── Notes / Decision Log (1346668352)
│   └── Q1 Update (1346668357)
├── Project Management Plan (1419363218)
├── TFD Status Updates 2026 (1424137842) ← Index page
│   ├── 6/17/26 TFD Weekly Agenda (1424137886)
│   ├── 6/19/26 Status Update (1424152018)
│   └── 6/26/26 TFD Weekly Agenda (1424156221)
└── TFD Program [draft] (1424133824) ← OLD DRAFT, content moved to hub
```

### Old Draft Page (1424133824)

Content from this page was copied to the live hub (1276292540). The draft still exists as a child page but is no longer maintained. Can be deleted/archived.

---

## Threat Models

### Wave 1 — Initial Five (Q1–Q2)
| # | Threat Model | Jira Label | Lead |
|---|---|---|---|
| 1 | Compromise of Core/Edge Infrastructure | `CompromisedServer` | TBD |
| 2 | Malicious Insider Risk | `InsiderThreat` | TBD |
| 3 | Compromise or Physical Tampering of Hardware | `PhysicalTampering` | TBD |
| 4 | B2B SaaS Integration & Supply Chain Exploitation | `B2BSaaSIntegration` | TBD |
| 5 | Software Supply Chain | `SoftwareSupplyChain` | TBD |

### Wave 2 — Expansion (Q3–Q4)
| # | Threat Model | Jira Label | Lead |
|---|---|---|---|
| 6 | Unauthorized Access to Customer Data | `UnauthorizedAccessCustomerData` | Evan |
| 7 | Customer Zero Threats | `CustomerZero` | Sahil |
| 8 | AI Security | `AISecurity` | Sonia |

### Other Jira Labels
- `ThreatFocusedControl` — required on ALL program tickets
- `needs-discussion` — flagged for discussion
- `Q1'26`, `Q2'26`, `Q3'26`, `Q4'26` — quarterly commitment labels

---

## API Patterns

### Authentication

```python
import json, requests, urllib3, subprocess, re, uuid
urllib3.disable_warnings()

# Get cloudflared token
result = subprocess.run(['cloudflared', 'access', 'login', 'https://wiki.cfdata.org/'],
                        capture_output=True, text=True)
token = None
for line in (result.stdout + result.stderr).split('\n'):
    m = re.search(r'eyJ[a-zA-Z0-9._-]+', line)
    if m:
        token = m.group(0)
        break

HEADERS = {'cf-access-token': token, 'X-Atlassian-Token': 'no-check'}
BASE = 'https://wiki.cfdata.org/rest/api/content'
```

### Fetch Page

```python
page_id = 'PAGE_ID'
resp = requests.get(f'{BASE}/{page_id}?expand=body.storage,version',
                    headers=HEADERS, verify=False)
data = resp.json()
body = data['body']['storage']['value']
version = data['version']['number']
title = data['title']
```

### Update Page (PUT)

**ALWAYS fetch current version right before updating.**

```python
payload = {
    'id': page_id,
    'type': 'page',
    'title': title,
    'body': {'storage': {'value': new_body, 'representation': 'storage'}},
    'version': {'number': version + 1}
}
resp = requests.put(f'{BASE}/{page_id}', json=payload,
                    headers={**HEADERS, 'Content-Type': 'application/json'},
                    verify=False)
```

### Create Page (POST)

```python
payload = {
    'type': 'page',
    'title': 'Page Title',
    'space': {'key': 'INFOSEC'},
    'ancestors': [{'id': PARENT_ID}],
    'body': {'storage': {'value': body_html, 'representation': 'storage'}}
}
resp = requests.post(BASE, json=payload,
                     headers={**HEADERS, 'Content-Type': 'application/json'},
                     verify=False)
new_page_id = resp.json()['id']
```

### Critical Rules
- **Storage Format Only** — never use rendered HTML (locks the editor)
- **Always fetch version right before PUT** — pages change between fetches
- **Validate XML tag balance** before creating — mismatched tags cause API errors

---

## Editing Approach: Choose Before You Start

Confluence's REST API only supports full-body PUT — there is no "update this section" endpoint. So the workflow is always: **GET body → modify → PUT body**. The question is *how* to modify. Always ask the user which approach they prefer:

### Option A: Full Rewrite

Rewrite the entire page body from scratch as a single XHTML string, then PUT it.

```
User says: "rebuild the agenda" or "restructure the page"
→ Fetch page (for version number only)
→ Build new body string from template
→ PUT with version + 1
```

**Best for:** Initial page creation, major restructuring, adding/removing entire sections, when the page is small or freshly created.

**Pros:**
- Full control over output — clean, predictable structure
- Can restructure anything (move sections, change table columns, swap layouts)
- Simple to reason about — you see the entire result

**Cons:**
- Fragile — one typo in a 15KB+ string can break the whole page
- Loses existing macro IDs, inline edits, and formatting nuances others may have made
- Not idempotent — re-running the same update produces different macro IDs
- Hard to diff — you can't easily see what actually changed vs. what was rewritten
- Risky if someone else edited the page since you last fetched it

### Option B: Targeted Edit (In-Place)

Fetch the existing body, parse it as XML, find the specific element(s) to modify, update just those nodes, serialize back, and PUT.

```
User says: "update the status to green" or "add a row to the next steps table"
→ Fetch page (for body + version)
→ Parse body as XML tree
→ Find target element (by text content, position, or structure)
→ Modify/insert/replace just that element
→ Serialize back to string
→ PUT with version + 1
```

**Best for:** Updating a few cells, changing status lozenges, adding table rows, updating text content, fixing typos, when others may have edited the page.

**Pros:**
- Preserves all existing content, macro IDs, formatting, and others' edits
- Safe for small changes — you only touch what you need
- Easy to diff — only the targeted element changed
- Re-runnable without side effects

**Cons:**
- More complex code — need to parse and navigate XML tree
- Requires understanding the existing page structure
- Harder for major restructuring (moving sections, changing table columns)

### When to Use Which

| Scenario | Approach |
|----------|----------|
| Creating a new page | A (Full Rewrite) — no existing body to preserve |
| Restructuring a page (new sections, new table columns) | A (Full Rewrite) |
| Updating status lozenges or text in specific cells | B (Targeted Edit) |
| Adding a row to an existing table | B (Targeted Edit) |
| Fixing a typo or updating a date | B (Targeted Edit) |
| Rebuilding a corrupted page | A (Full Rewrite) |
| Updating the Progress Panel percentages | B (Targeted Edit) — preserve the finalized design |
| Adding/removing discussion items from an agenda | B (Targeted Edit) — preserve meeting notes already added |

### Targeted Edit Helper Script

A reusable helper (`scripts/confluence_edit.py`) provides functions for common in-place edits:

```python
from confluence_edit import ConfluencePage

page = ConfluencePage('1424156221')  # fetches body + version

# Update a table cell by matching row header text
page.update_cell(row_header="Overall status", new_content="GREEN — on track")

# Add a row to a table (by matching a header cell)
page.add_table_row(after_header="Action item", cells=["New item", "Tiana", "Jul 1", lozenge])

# Replace text anywhere in the body
page.replace_text("old text", "new text")

# Update a status lozenge by its current title
page.update_lozenge(old_title="AT RISK", new_color="Green", new_title="ON TRACK")

# Add a bullet to a list after a specific item
page.add_bullet_after(match_text="Existing item", new_item="New item")

# Push changes
page.save()
```

See `scripts/confluence_edit.py` for the full implementation.

---

## Task 1: Program Hub Maintenance

**Page**: `1276292540` | **Design**: Blue gradient header (`#1c5e98 → #206db1 → #2885d7`)

### Hub Page Tabs

| Tab | Content | JQL Count |
|-----|---------|-----------|
| Program Overview | Threat models table with Wave 1 (5 models) + Wave 2 (3 models) separators | 0 (links only) |
| Program Health | 2x2 Progress Panel dashboard + threat model breakdown table | ~20 |
| Timeline & Milestones | Stiltsoft Roadmap Planner + milestones table with status lozenges | 0 |
| Now \| Next \| Later | 3 sub-tabs with workstream tables, Jira count macros, status lozenges | ~15 |
| Status Distribution | KPI cards (Total/In Progress/Blocked), threat model breakdown, priority distribution, assignment overview | ~25 |
| Workstreams | Open/closed tickets with table filters | ~10 |
| Ticket Handling Handbook | Roles, workflows, escalation, DoD, labels, cadence | 0 |
| Resources | Links to all program resources | 0 |

### Progress Panel Design (DO NOT CHANGE)

The 2x2 grid in the Progress Panel is finalized. When editing these boxes:

| Position | Border | BG | Text Color | Metric |
|----------|--------|----|------------|--------|
| Top-left | `#008000` | `#F0FFF0` | `#008000` | Completion Rate |
| Top-right | `#87CEFA` | `#F0F8FF` | `#1c5e98` | P1 Uncompleted |
| Bottom-left | `#FFC000` | `#FFFDE7` | `#B8860B` | Unassigned |
| Bottom-right | `#FF0000` | `#FFF0F0` | `#CC0000` | Blocked |

**Keep exact**: panel structure, border colors, border widths (3), bg colors, spacing (`padding-top: 15px` on lozenge, `margin-top: 30px; margin-bottom: 30px` on percentage, `margin-bottom: 20px` on counts, `margin-bottom: 15px` on target), font sizes (48px percentage, 14px counts, 10px last-calculated), layout order (status lozenge → big percentage → counts text → target → last calculated).

Only update: percentage value, JQL queries, and last-calculated date.

### Hub Page Sync Triggers

| Trigger | What to Update |
|---------|---------------|
| New status update published | Update any "latest status" references, add link to Resources tab |
| New agenda created | Add link to Resources tab |
| New threat model added | Update Program Overview tab table |
| Threat model lead changes | Update Program Overview tab + Handbook tab |
| Milestone completed | Update Timeline & Milestones tab status lozenges |
| Quarterly review done | Update Program Overview, Health, and Timeline tabs |

### Roadmap Colors
- Wave 1 = orange (`#e8741e` / `#f5a623`)
- Wave 2 = yellow (`#f5c842` / `#fce596`)

---

## Task 2: Status Updates Index Maintenance

**Page**: `1424137842`

### Index Table Structure

The index page has a 2-column table:

| Weekly Meeting Agendas | Friday Status Send-Outs |
|----------------------|----------------------|
| [Links to agenda pages] | [Links to status pages] |

### Adding a Row

When a new agenda or status update is created, add a link to the appropriate column:

```python
# Fetch the index page
resp = requests.get(f'{BASE}/1424137842?expand=body.storage,version',
                    headers=HEADERS, verify=False)
data = resp.json()
body = data['body']['storage']['value']
version = data['version']['number']

# Add link to the appropriate column
# For agendas: add <p><a href="URL">Title</a></p> inside the first <td>
# For status updates: add <p><a href="URL">Title</a></p> inside the second <td>

# PUT update with version + 1
```

### Full Index Rebuild Pattern

If the table gets corrupted or needs a full rebuild:

```python
new_body = '<table class="wrapped"><colgroup><col /><col /></colgroup><tbody>'
new_body += '<tr><th scope="col">Weekly Meeting Agendas</th><th scope="col">Friday Status Send-Outs</th></tr>'
new_body += '<tr>'
new_body += '<td>'
new_body += '<p><a href="https://wiki.cfdata.org/spaces/INFOSEC/pages/1424137886">6/17/26 TFD Weekly Agenda</a></p>'
new_body += '<p><a href="https://wiki.cfdata.org/spaces/INFOSEC/pages/1424156221">6/26/26 TFD Weekly Agenda</a></p>'
new_body += '</td>'
new_body += '<td>'
new_body += '<p><ac:link><ri:page ri:content-title="6/19/26 Status Update" /></ac:link></p>'
new_body += '</td>'
new_body += '</tr></tbody></table><p><br /></p>'
```

---

## Task 3: Weekly Agenda Creation

### Naming Convention
`[M/D/YY] TFD Weekly Agenda` (e.g., "6/26/26 TFD Weekly Agenda")

### Parent Page
`1424137842` (TFD Status Updates 2026)

### Design Rules (CRITICAL)

- **NO `ac:layout` macros** — they lock the Confluence editor, making real-time note-taking impossible during meetings
- **NO expand macros for discussion items** — use bullet lists for live note-taking
- **NO panel macros for section headers** — use colored table cells instead
- Colored section headers use single-cell tables with inline `style="background-color: #color; color: #FFFFFF;"` (NOT `highlight-#color` class — doesn't render reliably)

### Agenda Structure (6 Sections + Parking Lot)

```
1) Project Status          (blue header #0052cc)
2) Progress Updates         (purple header #6554C0)
3) Status by Workstream     (orange header #FF8B00)
4) Discussion Items         (red header #DE350B)
5) Notes                    (grey header #6B778C)
6) Next Steps               (green header #36B37E)
Parking Lot                 (light grey header #97a0af)
```

### Helper Functions

```python
def colored_header(text, color):
    return f'<table class="wrapped" style="width: 100%;"><tbody><tr><td style="background-color: {color}; color: #FFFFFF;"><strong>{text}</strong></td></tr></tbody></table>'

def th(color, text):
    return f'<th style="background-color: {color}; color: #FFFFFF;"><strong>{text}</strong></th>'

def status_lozenge(color, title_text):
    return f'<ac:structured-macro ac:name="status" ac:schema-version="1" ac:macro-id="{uuid.uuid4()}"><ac:parameter ac:name="subtle">true</ac:parameter><ac:parameter ac:name="colour">{color}</ac:parameter><ac:parameter ac:name="title">{title_text}</ac:parameter></ac:structured-macro>'
```

### Section 1: Project Status

```python
parts.append(colored_header('1) Project Status', '#0052cc'))
parts.append('<p>Current state of the project.</p>')
parts.append('<table class="wrapped"><tbody>')
parts.append(f'<tr><th style="width: 35%;">Overall status</th><td>{status_lozenge("Yellow", "AT RISK")} [narrative]</td></tr>')
parts.append('<tr><th>On track / at risk / blocked</th><td>[assessment]</td></tr>')
parts.append('<tr><th>Key wins since last meeting</th><td><ul><li>[win 1]</li><li>[win 2]</li></ul></td></tr>')
parts.append('<tr><th>Main blockers or decisions needed</th><td><ul><li>[blocker 1]</li></ul></td></tr>')
parts.append('<tr><th>Definition of Done</th><td>[DoD statement]</td></tr>')
parts.append('<tr><th>Path to green</th><td>[path to green]</td></tr>')
parts.append('</tbody></table>')
parts.append('<p><br /></p>')

# Project Artifacts sub-section
parts.append(colored_header('Project Artifacts', '#36B37E'))
parts.append('<ul>')
parts.append('<li><a href="https://wiki.cfdata.org/spaces/INFOSEC/pages/1419363218">TFD Project Management Wiki</a></li>')
parts.append('<li><a href="https://wiki.cfdata.org/spaces/INFOSEC/pages/1276292540">TFD Program Hub Wiki</a></li>')
parts.append('<li><a href="https://wiki.cfdata.org/spaces/INFOSEC/pages/1346668352">TFD Decision Log</a></li>')
parts.append('</ul>')
```

### Section 2: Progress Updates

```python
parts.append(colored_header('2) Progress Updates', '#6554C0'))
parts.append('<p><em>What has happened since the last meeting.</em></p>')
parts.append('<table class="wrapped"><tbody>')
parts.append(f'<tr>{th("#6554C0", "Update")}{th("#6554C0", "Owner")}{th("#6554C0", "Progress made")}{th("#6554C0", "Follow-up")}</tr>')
# One row per update item
parts.append('</tbody></table>')
```

### Section 3: Status by Workstream

```python
parts.append(colored_header('3) Status by Workstream', '#FF8B00'))
parts.append('<p><em>Review each workstream one at a time.</em></p>')
parts.append('<table class="wrapped"><tbody>')
parts.append(f'<tr>{th("#FF8B00", "Workstream")}{th("#FF8B00", "Status")}{th("#FF8B00", "What changed")}{th("#FF8B00", "Next milestone")}{th("#FF8B00", "Owner")}</tr>')
# Wave 1, Wave 2, Wave 3 rows
parts.append('</tbody></table>')
```

### Section 4: Discussion Items

```python
parts.append(colored_header('4) Discussion Items', '#DE350B'))
parts.append('<p><em>Use this section for the questions we need to solve.</em></p>')
# Each item as h3 + bullet list (NOT expand macros)
parts.append('<h3>Item 1: [Title]</h3>')
parts.append('<ul>')
parts.append('<li><strong>Question:</strong> [question]</li>')
parts.append('<li><strong>Context:</strong> [context]</li>')
parts.append('<li><strong>Decision needed:</strong> [decision]</li>')
parts.append('<li><strong>Owner:</strong> [owner]</li>')
parts.append('<li><strong>Timebox:</strong> [time]</li>')
parts.append('</ul>')
```

### Section 5: Notes

```python
parts.append(colored_header('5) Notes', '#6B778C'))
parts.append('<p><em>Helpful context and parked tangents.</em></p>')
parts.append('<ul>')
# Bullet list of notes
parts.append('</ul>')
```

### Section 6: Next Steps

```python
parts.append(colored_header('6) Next Steps', '#36B37E'))
parts.append('<p><em>Action items before we close.</em></p>')
parts.append('<table class="wrapped"><tbody>')
parts.append(f'<tr>{th("#36B37E", "Action item")}{th("#36B37E", "Owner")}{th("#36B37E", "Due date")}{th("#36B37E", "Status")}</tr>')
# One row per action item with status lozenge
parts.append('</tbody></table>')
```

### Parking Lot

```python
parts.append(colored_header('Parking Lot', '#97a0af'))
parts.append('<p><em>Topics to revisit later.</em></p>')
parts.append('<ul>')
# Bullet list of parked topics
parts.append('</ul>')
```

### Agenda Workflow

**Option A — With Google Drive integration (automatic):**
1. User says "draft this week's agenda" (optionally: "pull from my Gemini notes")
2. Search Google Drive for recent Gemini notes since last meeting
3. Fetch last week's agenda from Confluence for continuity
4. Parse Gemini notes: extract decisions, action items, discussion topics, blockers, wins
5. Build page body using the 6-section template, auto-populated with extracted info
6. Create child page under `1424137842` (POST to API)
7. Add link to index table on `1424137842` (Task 2)
8. Present draft to user for review/editing before finalizing

**Option B — Manual input (user provides content):**
1. Ask user for: date, attendees, discussion items, wins, blockers, action items
2. Build page body using the 6-section template above
3. Create child page under `1424137842` (POST to API)
4. Add link to index table on `1424137842` (Task 2)
5. Log any decisions to Decision Log page `1346668352`

**Option C — Hybrid (user provides some, skill pulls rest):**
1. User provides partial info (e.g., "here are my discussion items: ...")
2. Skill fetches last week's agenda + searches Drive for additional context
3. Combines user input with auto-extracted info
4. Creates the agenda page
5. User reviews and edits

---

## Task 4: Weekly Status Report Creation

### Naming Convention
`[M/D/YY] Status Update` (e.g., "6/19/26 Status Update")

### Parent Page
`1424137842` (TFD Status Updates 2026)

### Design Rules

- Uses `ac:layout` with `two_right_sidebar` (status reports are NOT edited live, so layout macros are OK)
- Main column: Overall Program Status panel, Executive Summary, metrics, per-threat-model views
- Sidebar: Quick links and metrics
- All Jira counts are live JQL macros (not hardcoded numbers)

### Status Report Structure

```python
parts = []

# Overall Program Status panel
parts.append('<ac:structured-macro ac:name="panel" ac:schema-version="1" ac:macro-id="UUID">')
parts.append('<ac:parameter ac:name="borderColor">#394ECE</ac:parameter>')
parts.append('<ac:parameter ac:name="titleColor">white</ac:parameter>')
parts.append('<ac:parameter ac:name="titleBGColor">#394ECE</ac:parameter>')
parts.append('<ac:parameter ac:name="title">Overall Program Status</ac:parameter>')
parts.append('<ac:rich-text-body>')
parts.append(f'<table class="fixed-width wrapped"><tbody>')
parts.append(f'<tr><td class="highlight-grey"><p><time datetime="{date}" /></p></td>')
parts.append(f'<td><p><strong>{status_lozenge(color, title)}</strong></p></td></tr>')
parts.append('</tbody></table>')
parts.append('</ac:rich-text-body></ac:structured-macro>')

# Two-column layout with right sidebar
parts.append('<ac:layout><ac:layout-section ac:type="two_right_sidebar"><ac:layout-cell>')

# Executive Summary panel
# High Level Overview panel
# Major Wins panel
# Attention Required panel
# Project Workstreams table (per-threat-model with Jira macros)

parts.append('</ac:layout-cell><ac:layout-cell>')
# Sidebar: Quick Links, metrics
parts.append('</ac:layout-cell></ac:layout-section></ac:layout>')
```

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

### Per-Threat-Model JQL Patterns

For each threat model, use these JQL patterns in the workstream table:

```
Done:   labels = ThreatFocusedControl and labels in (LABEL) and status in (Done, Cancelled)
Open:   labels = ThreatFocusedControl and labels in (LABEL) and status not in (Done, Cancelled)
Total:  labels = ThreatFocusedControl and labels in (LABEL)
```

### Program-Level Metrics JQL

```
Total:       labels = ThreatFocusedControl
Completed:   labels = ThreatFocusedControl and status in (Done, Closed, Cancelled)
In Progress: labels = ThreatFocusedControl and status = "In Progress"
Blocked:     labels = ThreatFocusedControl and status in (Blocked)
Unassigned:  project = GRC AND labels = ThreatFocusedControl AND status NOT IN (Done, Cancelled) AND assignee = EMPTY
```

### Status Lozenge Logic

| Completion Rate | Blocked > 3 days | Unassigned > 5 | Lozenge |
|----------------|-------------------|-----------------|---------|
| >= 70% | No | No | Green (ON TRACK) |
| 40-69% | Yes | Yes | Yellow (AT RISK) |
| < 40% | Yes | Yes | Red (OFF TRACK) |

### Status Report Workflow

**Option A — With Google Drive integration (automatic):**
1. User says "create status update" (optionally: "pull from my Gemini notes")
2. Fetch this week's filled-out agenda from Confluence (post-meeting notes)
3. Search Google Drive for any new Gemini notes from the week
4. Parse agenda + Gemini notes: extract wins, concerns, progress, metrics
5. Fetch live Jira counts for all 8 threat models (or use Jira macros for live counts)
6. Create child page under `1424137842` (POST to API)
7. Add link to index table on `1424137842` — Friday Status Send-Out column (Task 2)
8. Update hub page `1276292540` if needed (Task 1)
9. Present draft to user for review before finalizing

**Option B — Manual input (user provides content):**
1. Ask user for: date, executive summary narrative, wins, concerns, overall status color
2. Fetch live Jira counts for all 8 threat models (or use Jira macros for live counts)
3. Create child page under `1424137842` (POST to API)
4. Add link to index table on `1424137842` — Friday Status Send-Out column (Task 2)
5. Update hub page `1276292540` if needed (Task 1)

---

## Full Weekly Workflow

### Monday — Draft Agenda

**With Google Drive:**
1. Search Drive for recent Gemini notes since last meeting
2. Fetch last week's agenda from Confluence for continuity
3. Auto-populate agenda draft from parsed notes (decisions, actions, discussion items)
4. Create agenda page under `1424137842`
5. Add row to index table (Weekly Meeting Agendas column)

**Without Google Drive:**
1. Ask user for discussion items, wins, blockers, action items
2. Create agenda page under `1424137842`
3. Add row to index table (Weekly Meeting Agendas column)

### Wednesday — Mid-Week Check

1. Fetch live Jira counts — flag new blockers or status changes
2. Update PM Plan `1419363218` if new action items or people changes
3. Optionally: search Drive for any new meeting notes since Monday

### Thursday — Finalize Agenda

1. User reviews draft agenda and adds/edits content
2. Update agenda page with any changes
3. Optionally: pull any new Gemini notes from Wednesday/Thursday meetings

### Friday — Status Update (Post-Meeting)

**With Google Drive:**
1. Fetch this week's filled-out agenda from Confluence (post-meeting notes)
2. Search Drive for any new Gemini notes from the week
3. Auto-extract wins, concerns, progress from agenda + notes
4. Create status update page under `1424137842`
5. Add row to index table (Friday Status Send-Outs column)
6. Update hub page `1276292540` if needed
7. Draft next week's agenda shell

**Without Google Drive:**
1. Ask user for executive summary, wins, concerns, status color
2. Create status update page under `1424137842`
3. Add row to index table (Friday Status Send-Outs column)
4. Update hub page `1276292540` if needed
5. Draft next week's agenda shell

### End of Month
1. Generate executive summary (can be a tab on the status update)
2. Review decision log — mark any superseded decisions
3. Update PM Plan `1419363218` with monthly metrics

### End of Quarter
1. Update Q1 Update page `1346668357` (or create Q2/Q3/Q4 equivalent)
2. Run quarterly review using quarterly review agenda template
3. Update program scope — add/remove threat models in hub page Program Overview tab
4. Update all pages with new quarter info

---

## Macro Reference

### Jira Issues Count Macro
```xml
<ac:structured-macro ac:name="jira" ac:schema-version="1" ac:macro-id="UNIQUE-UUID">
  <ac:parameter ac:name="server">Cloudflare Jira</ac:parameter>
  <ac:parameter ac:name="serverId">cc100dec-3d79-305b-8fae-4caba5e44cd2</ac:parameter>
  <ac:parameter ac:name="jqlQuery">YOUR JQL HERE</ac:parameter>
  <ac:parameter ac:name="count">true</ac:parameter>
</ac:structured-macro>
```
- Parameter is `jqlQuery` (NOT `jql`)
- Each macro needs unique `ac:macro-id` (UUID)

### Status Lozenge
```xml
<ac:structured-macro ac:name="status" ac:schema-version="1" ac:macro-id="UUID">
  <ac:parameter ac:name="subtle">true</ac:parameter>
  <ac:parameter ac:name="colour">Green</ac:parameter>
  <ac:parameter ac:name="title">ON TRACK</ac:parameter>
</ac:structured-macro>
```
Colours: Green, Blue, Yellow, Red, Grey. Use `subtle=true` for softer look.

### Panel Macro
```xml
<ac:structured-macro ac:name="panel" ac:schema-version="1" ac:macro-id="UUID">
  <ac:parameter ac:name="title">Title</ac:parameter>
  <ac:parameter ac:name="titleBGColor">#1c5e98</ac:parameter>
  <ac:parameter ac:name="titleColor">#FFFFFF</ac:parameter>
  <ac:rich-text-body><p>Content</p></ac:rich-text-body>
</ac:structured-macro>
```

### UI Tabs
```xml
<ac:structured-macro ac:name="ui-tabs" ac:schema-version="1" ac:macro-id="UUID-1">
  <ac:rich-text-body>
    <ac:structured-macro ac:name="ui-tab" ac:schema-version="1" ac:macro-id="UUID-2">
      <ac:parameter ac:name="title">Tab Name</ac:parameter>
      <ac:rich-text-body><p>Content</p></ac:rich-text-body>
    </ac:structured-macro>
  </ac:rich-text-body>
</ac:structured-macro>
```
Parameter is `title` (NOT `name`).

### Layout (Two-Column with Sidebar)
```xml
<ac:layout>
  <ac:layout-section ac:type="two_right_sidebar">
    <ac:layout-cell><!-- Main content --></ac:layout-cell>
    <ac:layout-cell><!-- Sidebar --></ac:layout-cell>
  </ac:layout-section>
</ac:layout>
```
Types: `single`, `two_equal`, `two_right_sidebar`, `two_left_sidebar`, `three_equal`

### Colored Table Cell Header (for agendas)
```xml
<table class="wrapped" style="width: 100%;">
  <tbody><tr><td style="background-color: #0052cc; color: #FFFFFF;">
    <strong>Section Title</strong>
  </td></tr></tbody>
</table>
```

### UI Button
```xml
<ac:structured-macro ac:name="ui-button" ac:schema-version="1" ac:macro-id="UUID">
  <ac:parameter ac:name="color">blue</ac:parameter>
  <ac:parameter ac:name="title">Button Title</ac:parameter>
  <ac:parameter ac:name="url">https://wiki.cfdata.org/...</ac:parameter>
</ac:structured-macro>
```

### Roadmap Planner (Stiltsoft)
```xml
<ac:structured-macro ac:name="roadmap">
  <ac:parameter ac:name="source">manual</ac:parameter>
  <ac:parameter ac:name="title">Roadmap Title</ac:parameter>
  <ac:parameter ac:name="timeframe">month</ac:parameter>
  <ac:parameter ac:name="startDate">2025-11-01</ac:parameter>
  <ac:parameter ac:name="endDate">2026-10-31</ac:parameter>
</ac:structured-macro>
```

### Style Macro (CSS)
```xml
<ac:structured-macro ac:name="style" ac:schema-version="1" ac:macro-id="UUID">
  <ac:plain-text-body><![CDATA[
    #grad1 { background: linear-gradient(145deg, #1c5e98, #206db1, #2885d7); padding: 1em; }
  ]]></ac:plain-text-body>
</ac:structured-macro>
```

---

## Key Lessons Learned

- **Storage format = editable**. Rendered HTML = locked editor.
- **Jira macros**: parameter is `jqlQuery` (not `jql`), need both `server` and `serverId`, plus `ac:schema-version` and `ac:macro-id`
- **UI tabs**: parameter is `title` (not `name`)
- **UI button**: `color` is `blue` (not rgb), `url` (not `link`), no `textColor`
- **Always fetch current version right before PUT** — pages change between fetches
- **When replacing sections**, use `find()` for the first closing tag, not `rfind()`
- **No nested panels** when replacing content inside an existing panel
- **Agenda pages**: NO `ac:layout` macros (locks editor), NO panel macros for headers, NO expand macros for discussion items
- **Agenda colored headers**: use inline `style="background-color"` NOT `highlight-#color` class
- **Status report pages**: `ac:layout` with `two_right_sidebar` is OK (not edited live)
- **Stiltsoft Table Chart** does NOT work with Jira macros in cells — don't use it
- **Confluence `position` parameter** does NOT reliably reorder child pages — must drag in UI
- **Tool path corruption**: use Python `requests` instead of curl, use `/Users/tianaegidi/` instead of `/tmp/`
- **Verify Jira URLs** — `issues` can lose the `u` becoming `isses`
- **Decision log entries are immutable** — if reversed, add a new entry with SUPERSEDED status
- **Hub page sync** after every status update, agenda, or decision log entry
- **Q1 Update page** uses orange gradient; hub page uses blue gradient — don't mix them up
- **Percentages are hardcoded** with "Last calculated" date since Confluence Jira macros can't do math
