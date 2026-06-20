---
name: wiki-builder
description: All-in-one program management skill for the Threat-Focused Defense (TFD) program on wiki.cfdata.org. Manages 5 specific wiki pages — the program hub, Q1 update, project management plan, status updates, and notes/decision log. Creates and edits pages, generates weekly agendas and status updates, maintains the hub page, and tracks decisions. Use when the user mentions TFD, Threat-Focused Defense, wiki.cfdata.org TFD pages, weekly agenda, status update, decision log, or any of the 5 program pages.
---

# TFD Program Wiki Builder

All-in-one skill for managing the **Threat-Focused Defense (TFD)** program's Confluence presence on wiki.cfdata.org. This skill controls exactly 5 pages plus their child pages. It is NOT a generic wiki tool — it is purpose-built for TFD program management.

## Prerequisites

1. **Script**: `~/wikigen-generic.sh` must exist and be executable
2. **Cloudflared token**: `cloudflared access login https://wiki.cfdata.org/`
3. **Jira app link ID**: `cc100dec-3d79-305b-8fae-4caba5e44cd2`
4. **Python requests**: `pip3 install requests`

## Tool Bug Workarounds

- `wiki` → `iki` in bash — use `w"iki"` in URLs
- `tmp` → `ttp` in bash — use `/Users/tianaegidi/` for temp files
- `issues` → `isses` — always verify Jira URLs in generated content

---

## TFD Page Inventory

This skill controls exactly these 5 pages (all under INFOSEC > Security Team Home > Security Programs > GRC Program > Threat-focused Defense):

### Page 1: TFD Program Hub [draft]
- **ID**: `1424133824`
- **URL**: `https://wiki.cfdata.org/spaces/INFOSEC/pages/1424133824`
- **Purpose**: Main program landing page with tabs for all program content
- **Design**: Blue gradient header (`#1c5e98 → #206db1 → #2885d7`)
- **Version**: Track current via API (was 141 as of last edit)
- **Tabs**: Program Overview, Program Health, Timeline & Milestones, Now|Next|Later, Workstreams, Ticket Handling Handbook, Resources
- **JQL queries**: 38 live Jira macros
- **Key content**:
  - Threat models table with Wave 1 (5 models) and Wave 2 (3 models) separators
  - 2x2 dashboard (Done/Total, Throughput, Unassigned, Blocked)
  - Threat model breakdown table (per-model Backlog/In Progress/Done/Blocked counts)
  - Milestones table with status lozenges
  - Roadmap planner macro
  - Ticket handling handbook (roles, workflows, escalation, DoD, labels, cadence)

### Page 2: Threat-focused Defense Q1 Update
- **ID**: `1346668357`
- **URL**: `https://wiki.cfdata.org/spaces/INFOSEC/pages/1346668357`
- **Purpose**: Q1 quarterly presentation/briefing page
- **Design**: Orange gradient header (`#ff6633 → #f6821f → #fbad41`)
- **Parent**: Notes page (1346668352)
- **Tabs**: Current Progress, High Level Overview, Q1 Deliverables, 2026 & Beyond, 2026 Commitments, EDR Replacement Impact, Beyond 2026, Expanding Beyond Top 5, Resources
- **JQL queries**: 20+ (extensive per-threat-model breakdowns with due date filters)
- **Key JQL patterns**:
  - `project = GRC AND labels = ThreatFocusedControl and labels = [MODEL] and (status in (Done, Cancelled, Closed) or due <= 2026-3-31) and labels not in ("needs-discussion")`
  - `project = GRC and ((status in (Done, Closed) or due <= 2026-3-31) or labels in ("Q1'26")) and labels = ThreatFocusedControl`
  - `project = GRC and status not in (Done, Closed, Cancelled) and labels = ThreatFocusedControl and labels in ("needs-discussion")`

### Page 3: Project Management Plan
- **ID**: `1419363218`
- **URL**: `https://wiki.cfdata.org/spaces/INFOSEC/pages/1419363218`
- **Purpose**: TPM project management tracker with ticket tracking and people management
- **Design**: Two-column layout with right sidebar (`ac:layout-section ac:type="two_right_sidebar"`)
- **Sections**: Program Overview, Goal Breakdown & Success Criteria, Action Items, People (Project Leads, Business Owners), Closed/Open/Unassigned Tickets, By Assignee, By Business Owner, Assignee-Business Owner Map, High Level Timeline
- **JQL queries**: 7 (open tickets, closed tickets, unassigned)
- **Note**: Has "Under Construction" panel — still being developed

### Page 4: TFD Status Updates 2026
- **ID**: `1424137842`
- **URL**: `https://wiki.cfdata.org/spaces/INFOSEC/pages/1424137842`
- **Purpose**: Index page linking to weekly agendas and Friday status send-outs
- **Structure**: Simple 2-column table (Weekly Meeting Agenda | Friday Status Send-Out)
- **Child pages**:
  - `1424137886` — 6/17/26 TFD Weekly Agenda (two-column layout, Overall Project Status, Project Artifacts, agenda table)
  - `1424152018` — 6/19/26 Status Update (two-column with sidebar, 24 JQL queries, Executive Summary, Major Wins, Attention Required, View Tickets)
- **Workflow**: Each week, create a new child page for the agenda (Monday) and status update (Friday), then add rows to this index table

### Page 5: Notes
- **ID**: `1346668352`
- **URL**: `https://wiki.cfdata.org/spaces/INFOSEC/pages/1346668352`
- **Purpose**: Parent page for notes and decision log — currently just a children macro
- **Child page**: Q1 Update (1346668357)
- **Planned**: Convert to Decision Log & Meeting Notes page (see Part 5)

---

## Page Hierarchy

```
Threat-focused Defense (ancestor, not directly managed)
├── Notes (1346668352) ← Decision Log / Meeting Notes
│   └── Q1 Update (1346668357) ← Quarterly briefing
├── Project Management Plan (1419363218) ← TPM tracker
├── TFD Status Updates 2026 (1424137842) ← Index page
│   ├── [Date] TFD Weekly Agenda (child pages, created each week)
│   └── [Date] Status Update (child pages, created each week)
└── TFD Program [draft] (1424133824) ← Main hub page
```

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
| 7 | Customer Zero Threats (T1 Phishing, T2 Credential Stuffing, T3 Identity Spoofing) | `CustomerZero` | Sahil |
| 8 | AI Security (T1 AI without SDLC guardrails, T2 Reliance on Agentic AI) | `AISecurity` | Sonia |

### Other Jira Labels
- `ThreatFocusedControl` — required on ALL program tickets
- `needs-discussion` — flagged for discussion
- `Q1'26`, `Q2'26`, `Q3'26`, `Q4'26` — quarterly commitment labels

---

## Part 1: Page Creation & Editing

### Creating a New Page

```bash
~/wikigen-generic.sh -s INFOSEC -t "Page Title" -i PARENT_PAGE_ID -c ~/content.html
```

### Updating an Existing Page

Use Python with `requests` for reliability:

```python
import json, requests, urllib3
urllib3.disable_warnings()

token = '$CF_TOKEN'
page_id = 'PAGE_ID'

resp = requests.get(
    f'https://wiki.cfdata.org/rest/api/content/{page_id}?expand=body.storage,version',
    headers={'cf-access-token': token, 'X-Atlassian-Token': 'no-check'},
    verify=False
)
data = resp.json()
body = data['body']['storage']['value']
version = data['version']['number']

# Modify body here
new_body = body[:start] + new_content + body[end:]

payload = {
    'id': page_id, 'type': 'page', 'title': data['title'],
    'body': {'storage': {'value': new_body, 'representation': 'storage'}},
    'version': {'number': version + 1}
}

resp2 = requests.put(
    f'https://wiki.cfdata.org/rest/api/content/{page_id}',
    json=payload,
    headers={'cf-access-token': token, 'X-Atlassian-Token': 'no-check', 'Content-Type': 'application/json'},
    verify=False
)
```

**IMPORTANT**: Always fetch the version right before updating.

### Finding Section Boundaries

```python
# Find panel by title
idx = body.find('ac:name="panel"')
content_start = body.find('<ac:rich-text-body>', idx)
content_start = body.find('>', content_start) + 1
panel_close = body.find('</ac:rich-text-body></ac:structured-macro>', content_start)
old_end = panel_close + len('</ac:rich-text-body></ac:structured-macro>')
```

Use `find()` for the first closing tag, NOT `rfind()`.

### Critical Rule: Storage Format Only

**ALWAYS use Confluence Storage Format (XHTML)**. Never use rendered HTML — it locks the editor.

---

## Part 2: Weekly Agenda Generation

### Where Agendas Live
- **Parent page**: TFD Status Updates 2026 (ID: `1424137842`)
- **Naming convention**: `[M/D/YY] TFD Weekly Agenda` (e.g., "6/17/26 TFD Weekly Agenda")
- **Index**: Add a row to the parent page's table linking to the new agenda

### Agenda Page Design (matches existing 6/17/26 agenda)
- Two-column layout (`ac:type="two_equal"`)
- Left column: Overall Project Status with status lozenge + Definition of Done reminder
- Right column: Project Artifacts (links to PM Plan, Hub Wiki, Email Template)
- Full-width section: Agenda table with timeboxed topics

### Agenda Template

```xml
<ac:layout>
  <ac:layout-section ac:type="two_equal">
    <ac:layout-cell>
      <h2><strong>Overall Project Status</strong></h2>
      <table class="fixed-width wrapped">
        <colgroup><col style="width: 38.6071%;" /><col style="width: 61.3929%;" /></colgroup>
        <tbody>
          <tr>
            <td class="highlight-grey" data-highlight-colour="grey"><p><time datetime="[DATE]" /></p></td>
            <td><p><strong> <ac:structured-macro ac:name="status" ac:schema-version="1" ac:macro-id="UUID">
              <ac:parameter ac:name="subtle">true</ac:parameter>
              <ac:parameter ac:name="colour">Red</ac:parameter>
            </ac:structured-macro></strong></p></td>
          </tr>
        </tbody>
      </table>
      <p>Project is in [Red/Yellow/Green] ...</p>
      <p><strong>Definition of Done:</strong> [Current DoD statement]</p>
    </ac:layout-cell>
    <ac:layout-cell>
      <p><strong>Project Artifacts:</strong></p>
      <ul>
        <li><a href="https://wiki.cfdata.org/spaces/INFOSEC/pages/1419363218">TFD Project Management Wiki</a></li>
        <li><a href="https://wiki.cfdata.org/spaces/INFOSEC/pages/1424133824">TFD Program Hub Wiki</a></li>
      </ul>
    </ac:layout-cell>
  </ac:layout-section>
  <ac:layout-section ac:type="single">
    <ac:layout-cell>
      <h2>Agenda</h2>
      <table class="relative-table wrapped">
        <tbody>
          <tr><th>Time</th><th>Topic</th><th>Owner</th></tr>
          <tr><td>0:00</td><td>Roll call + agenda review</td><td>Facilitator</td></tr>
          <tr><td>0:02</td><td>Program health dashboard review</td><td>TPM</td></tr>
          <tr><td>0:10</td><td>Threat model spotlight (rotating)</td><td>Lead Assessor</td></tr>
          <tr><td>0:20</td><td>Blockers &amp; escalations</td><td>Open floor</td></tr>
          <tr><td>0:25</td><td>Action items + next week preview</td><td>Facilitator</td></tr>
        </tbody>
      </table>
      
      <h3>Dashboard Snapshot</h3>
      <table>
        <tbody>
          <tr><th>Metric</th><th>Current</th><th>Trend</th></tr>
          <tr><td>Total Controls</td><td>[Jira macro]</td><td>[+/-]</td></tr>
          <tr><td>Completed</td><td>[Jira macro]</td><td>[+/-]</td></tr>
          <tr><td>In Progress</td><td>[Jira macro]</td><td>[+/-]</td></tr>
          <tr><td>Blocked</td><td>[Jira macro]</td><td>[+/-]</td></tr>
          <tr><td>Unassigned</td><td>[Jira macro]</td><td>[+/-]</td></tr>
        </tbody>
      </table>
      
      <h3>Action Items</h3>
      <table>
        <tbody>
          <tr><th>#</th><th>Action</th><th>Owner</th><th>Due</th><th>Status</th></tr>
        </tbody>
      </table>
      
      <h3>Decisions Made</h3>
      <table>
        <tbody>
          <tr><th>Decision</th><th>Rationale</th><th>Decided By</th></tr>
        </tbody>
      </table>
    </ac:layout-cell>
  </ac:layout-section>
</ac:layout>
```

### Agenda Workflow
1. Ask user for: date, attendees, spotlight threat model, any specific topics
2. Create child page under TFD Status Updates 2026 (ID: `1424137842`)
3. Add row to the index table on the parent page
4. Update hub page Quick Links if applicable

---

## Part 3: Status Updates

### Where Status Updates Live
- **Parent page**: TFD Status Updates 2026 (ID: `1424137842`)
- **Naming convention**: `[M/D/YY] Status Update` (e.g., "6/19/26 Status Update")
- **Index**: Add a row to the parent page's table in the "Friday Status Send-Out" column

### Status Update Page Design (matches existing 6/19/26 status update)
- Two-column layout with right sidebar (`ac:type="two_right_sidebar"`)
- Main column: Overall Program Status panel, Executive Summary, High Level Overview, Next Steps, Major Wins, Attention Required, per-threat-model ticket views
- Sidebar: Quick metrics, links
- 24 JQL queries pulling live data per threat model

### Status Update Template

```xml
<ac:layout>
  <ac:layout-section ac:type="two_right_sidebar">
    <ac:layout-cell>
      <!-- Overall Program Status -->
      <ac:structured-macro ac:name="panel" ac:schema-version="1" ac:macro-id="UUID">
        <ac:parameter ac:name="borderColor">#394ECE</ac:parameter>
        <ac:parameter ac:name="titleColor">white</ac:parameter>
        <ac:parameter ac:name="titleBGColor">#394ECE</ac:parameter>
        <ac:parameter ac:name="title">Overall Program Status</ac:parameter>
        <ac:rich-text-body>
          <table class="fixed-width wrapped">
            <tbody>
              <tr>
                <td class="highlight-grey"><p><time datetime="[DATE]" /></p></td>
                <td><p><strong><ac:structured-macro ac:name="status" ac:schema-version="1" ac:macro-id="UUID">
                  <ac:parameter ac:name="subtle">true</ac:parameter>
                  <ac:parameter ac:name="colour">[Red/Yellow/Green]</ac:parameter>
                </ac:structured-macro></strong></p></td>
              </tr>
            </tbody>
          </table>
        </ac:rich-text-body>
      </ac:structured-macro>

      <!-- Executive Summary -->
      <ac:structured-macro ac:name="panel" ac:schema-version="1" ac:macro-id="UUID">
        <ac:parameter ac:name="title">Executive Summary</ac:parameter>
        <ac:rich-text-body>
          <p>[2-3 sentence narrative]</p>
        </ac:rich-text-body>
      </ac:structured-macro>

      <!-- Metrics table with live Jira counts -->
      <table>
        <tbody>
          <tr>
            <td><h1><a href="[Jira URL]">[Jira count macro]</a></h1><p>Total Tickets</p></td>
            <td><h1><a href="[Jira URL]">[Jira count macro]</a></h1><p>Open</p></td>
            <td><h1><a href="[Jira URL]">[Jira count macro]</a></h1><p>Completed</p></td>
          </tr>
        </tbody>
      </table>

      <!-- High Level Overview -->
      <ac:structured-macro ac:name="panel" ac:schema-version="1" ac:macro-id="UUID">
        <ac:parameter ac:name="title">High Level Overview</ac:parameter>
        <ac:rich-text-body>
          <p>[Overview narrative]</p>
        </ac:rich-text-body>
      </ac:structured-macro>

      <!-- Major Wins -->
      <ac:structured-macro ac:name="panel" ac:schema-version="1" ac:macro-id="UUID">
        <ac:parameter ac:name="title">✅ Major Wins This Week</ac:parameter>
        <ac:rich-text-body>
          <ul><li>[Win 1]</li><li>[Win 2]</li></ul>
        </ac:rich-text-body>
      </ac:structured-macro>

      <!-- Attention Required -->
      <ac:structured-macro ac:name="panel" ac:schema-version="1" ac:macro-id="UUID">
        <ac:parameter ac:name="title">⚠️ ATTENTION REQUIRED</ac:parameter>
        <ac:rich-text-body>
          <ul><li>[Concern 1]</li></ul>
        </ac:rich-text-body>
      </ac:structured-macro>

      <!-- Per-threat-model ticket views -->
      <h3>PROJECT WORKSTREAMS</h3>
      <table>
        <tbody>
          <tr><th>Threat Model</th><th>Done</th><th>Open</th><th>Total</th><th>View Tickets</th></tr>
          <tr>
            <td>Compromised Server</td>
            <td>[Jira macro]</td>
            <td>[Jira macro]</td>
            <td>[Jira macro]</td>
            <td>[Jira macro]</td>
          </tr>
          <!-- ... repeat for each threat model ... -->
        </tbody>
      </table>
    </ac:layout-cell>
    
    <ac:layout-cell>
      <!-- Sidebar: Quick links and metrics -->
      <p><strong>Quick Links</strong></p>
      <ul>
        <li><a href="https://wiki.cfdata.org/spaces/INFOSEC/pages/1424133824">Program Hub</a></li>
        <li><a href="https://wiki.cfdata.org/spaces/INFOSEC/pages/1419363218">PM Plan</a></li>
      </ul>
    </ac:layout-cell>
  </ac:layout-section>
</ac:layout>
```

### Status Update JQL Patterns (per threat model)
```
Done:   labels = [LABEL] and status in (Done, Cancelled)
Open:   labels = [LABEL] and status not in (Done, Cancelled)
Total:  labels = [LABEL]
```

### Status Update Workflow
1. Ask user for: date, executive summary narrative, wins, concerns, overall status color
2. Fetch live Jira counts for all 8 threat models
3. Create child page under TFD Status Updates 2026 (ID: `1424137842`)
4. Add row to the index table on the parent page (Friday Status Send-Out column)
5. Update hub page's Latest Status panel

---

## Part 4: Hub Page Management

The hub page (ID: `1424133824`) is the program's main landing page. It must stay in sync when other pages change.

### Hub Page Tabs
1. **Program Overview** — threat models table with wave separators
2. **Program Health** — 2x2 dashboard + threat model breakdown table
3. **Timeline & Milestones** — roadmap + milestones with status lozenges
4. **Now | Next | Later** — workstream prioritization
5. **Workstreams** — open/closed tickets with table filters
6. **Ticket Handling Handbook** — roles, workflows, escalation, DoD, labels, cadence
7. **Resources** — links to all program resources

### Progress Panel Design (DO NOT CHANGE SIZING)
The 2x2 grid in the Progress Panel has been finalized. When editing these boxes:
- **Keep the exact same panel structure** — same border colors, border widths (3), bg colors
- **Keep the exact same spacing** — `padding-top: 15px` on lozenge, `margin-top: 30px; margin-bottom: 30px` on percentage, `margin-bottom: 20px` on counts, `margin-bottom: 15px` on target
- **Keep the same font sizes** — 48px for percentage, 14px for counts, 10px for last-calculated
- **Keep the same layout** — status lozenge → big percentage → counts text → target → last calculated
- Only update the percentage value, JQL queries, and last-calculated date

| Position | Border | BG | Text Color | Metric |
|----------|--------|----|------------|--------|
| Top-left | `#008000` | `#F0FFF0` | `#008000` | Completion Rate |
| Top-right | `#87CEFA` | `#F0F8FF` | `#1c5e98` | P1 Uncompleted |
| Bottom-left | `#FFC000` | `#FFFDE7` | `#B8860B` | Unassigned |
| Bottom-right | `#FF0000` | `#FFF0F0` | `#CC0000` | Blocked |

### Hub Page Sync Triggers

| Trigger | What to Update on Hub |
|---------|----------------------|
| New status update published | Update any "latest status" references, add link to Resources tab |
| New agenda created | Add link to Resources tab |
| New threat model added | Update Program Overview tab table |
| Threat model lead changes | Update Program Overview tab + Handbook tab |
| Milestone completed | Update Timeline & Milestones tab status lozenges |
| Quarterly review done | Update Program Overview, Health, and Timeline tabs |

### Hub Page Design
- Blue gradient header: `linear-gradient(145deg, #1c5e98, #206db1, #2885d7)`
- Welcome panel with program description
- Team & Stakeholders table
- "How to read this page" panel
- UI tabs with `ac:schema-version="1"` and unique `ac:macro-id`

---

## Part 5: Decision Log & Meeting Notes

### Current State
The Notes page (ID: `1346668352`) currently just has a children macro displaying child pages. The Q1 Update page is its only child.

### Planned: Convert Notes to Decision Log
Transform the Notes page into a full decision log and meeting notes archive:

```xml
<h1>📝 TFD Decision Log &amp; Meeting Notes</h1>

<ac:structured-macro ac:name="panel">
  <ac:parameter ac:name="title">About This Log</ac:parameter>
  <ac:parameter ac:name="titleBGColor">#1c5e98</ac:parameter>
  <ac:parameter ac:name="titleColor">#FFFFFF</ac:parameter>
  <ac:rich-text-body>
    <p>Immutable record of all TFD program decisions and meeting notes. Entries are never edited — if a decision is reversed, a new entry is added with SUPERSEDED status.</p>
  </ac:rich-text-body>
</ac:structured-macro>

<h2>Decision Log</h2>
<table>
  <tbody>
    <tr><th>#</th><th>Date</th><th>Decision</th><th>Rationale</th><th>Decided By</th><th>Stakeholders</th><th>Impact</th><th>Status</th><th>Supersedes</th></tr>
    <!-- New rows appended here -->
  </tbody>
</table>

<h2>Meeting Notes Archive</h2>
<!-- Expand macros per meeting, newest first -->
```

### Adding a Decision
1. Fetch Notes page (ID: `1346668352`)
2. Find the decisions table `</tbody>`
3. Insert new `<tr>` before `</tbody>`
4. Auto-increment decision number
5. PUT update with version + 1

### Adding Meeting Notes
1. Fetch Notes page
2. Find the last expand macro before `</ac:confluence>` (or the Meeting Notes header)
3. Insert new expand macro with meeting details
4. PUT update

### Decision Status Lozenges
- **Green "ACTIVE"** — In effect
- **Grey "SUPERSEDED"** — Replaced (reference new #)
- **Yellow "UNDER REVIEW"** — Being reconsidered
- **Red "REVERSED"** — Reversed without replacement

---

## Part 6: Q1 Update Page Management

The Q1 Update page (ID: `1346668357`) is a quarterly briefing with an orange gradient design. It uses extensive JQL queries with due date filters.

### Q1 Update Design
- Orange gradient header: `linear-gradient(145deg, #ff6633, #f6821f, #fbad41)`
- 9 tabs covering current progress, deliverables, 2026 commitments, and future expansion
- 59 Jira links with complex JQL (due dates, status filters, needs-discussion exclusions)

### Key JQL Patterns (Q1 Update specific)
```
# Q1 completed (by threat model)
project = GRC AND labels = ThreatFocusedControl and labels = [MODEL] 
  and (status in (Done, Cancelled, Closed) or due <= 2026-3-31) 
  and labels not in ("needs-discussion")

# All Q1 commitments
project = GRC and ((status in (Done, Closed) or due <= 2026-3-31) 
  or labels in ("Q1'26")) and labels = ThreatFocusedControl

# Needs discussion
project = GRC and status not in (Done, Closed, Cancelled) 
  and labels = ThreatFocusedControl and labels in ("needs-discussion")

# No due date, no quarter label
project = GRC and status not in (Done, Closed, Cancelled) and due = EMPTY 
  and labels = ThreatFocusedControl 
  and labels not in ("Q1'26", "Q2'26", "Q3'26", "Q4'26") 
  and "Business Owner" != EMPTY
```

### When to Update Q1 Page
- End of quarter: Update with final Q1 metrics
- Quarterly review: Add new quarter tab
- New threat model: Add to "Expanding Beyond Top 5" tab

---

## Part 7: Project Management Plan Management

The PM Plan page (ID: `1419363218`) is the TPM's operational tracker.

### PM Plan Design
- Two-column layout with right sidebar
- Left: Program Overview, Goals, Action Items, People, Ticket Trackers, Timeline
- Right sidebar: Quick reference

### PM Plan Sections
1. **Program Overview** — currently "Under Construction"
2. **Goal Breakdown & Success Criteria** — program goals
3. **Action Items** — tracked items
4. **People** — Project Leads, Business Owners
5. **Ticket Trackers** — Closed, Open, Unassigned (with Jira macros)
6. **By Assignee** — ticket counts per assignee
7. **By Business Owner** — ticket counts per business owner
8. **Assignee-Business Owner Map** — relationship matrix
9. **High Level Timeline** — timeline for TPM projects

### PM Plan JQL Patterns
```
Open:        labels = ThreatFocusedControl and status not in (Done, Cancelled)
Closed:      labels = ThreatFocusedControl and status in (Done, Cancelled)
Unassigned:  project = GRC AND labels = ThreatFocusedControl AND status NOT IN (Done, Cancelled) AND assignee = EMPTY
```

---

## Part 8: Full Weekly Workflow

### Monday
1. **Create weekly agenda** — child page under TFD Status Updates 2026 (ID: `1424137842`)
2. **Add row to index table** on the parent page
3. **Run the sync** using the agenda
4. **Log decisions** to the Notes/Decision Log page (ID: `1346668352`)
5. **Log meeting notes** as expand macro on the Notes page

### Wednesday
1. **Mid-week Jira check** — fetch counts, flag new blockers
2. **Update PM Plan** if new action items or people changes

### Friday
1. **Create status update** — child page under TFD Status Updates 2026
2. **Add row to index table** (Friday Status Send-Out column)
3. **Update hub page** if needed (Latest Status references)
4. **Draft next week's agenda**

### End of Month
1. **Generate executive summary** (can be a tab on the status update or standalone page)
2. **Review decision log** — mark any superseded decisions
3. **Update PM Plan** with monthly metrics

### End of Quarter
1. **Update Q1 Update page** (or create Q2/Q3/Q4 equivalent)
2. **Run quarterly review** using the quarterly review agenda
3. **Update program scope** — add/remove threat models in hub page Program Overview tab
4. **Update all pages** with new quarter info

---

## Macro Reference

### Jira Issues Count Macro (CRITICAL)
```xml
<ac:structured-macro ac:name="jira" ac:schema-version="1" ac:macro-id="UNIQUE-UUID">
  <ac:parameter ac:name="server">Cloudflare Jira</ac:parameter>
  <ac:parameter ac:name="serverId">cc100dec-3d79-305b-8fae-4caba5e44cd2</ac:parameter>
  <ac:parameter ac:name="jqlQuery">labels = ThreatFocusedControl AND status = Done</ac:parameter>
  <ac:parameter ac:name="count">true</ac:parameter>
</ac:structured-macro>
```
- Parameter is `jqlQuery` (NOT `jql`)
- Each macro needs unique `ac:macro-id` (UUID)

### Panel Macro
```xml
<ac:structured-macro ac:name="panel" ac:schema-version="1" ac:macro-id="UUID">
  <ac:parameter ac:name="title">Title</ac:parameter>
  <ac:parameter ac:name="titleBGColor">#1c5e98</ac:parameter>
  <ac:parameter ac:name="titleColor">#FFFFFF</ac:parameter>
  <ac:rich-text-body><p>Content</p></ac:rich-text-body>
</ac:structured-macro>
```

### Status Lozenge
```xml
<ac:structured-macro ac:name="status" ac:schema-version="1" ac:macro-id="UUID">
  <ac:parameter ac:name="subtle">true</ac:parameter>
  <ac:parameter ac:name="colour">Green</ac:parameter>
</ac:structured-macro>
```
Colours: Green, Blue, Yellow, Red, Grey. Use `subtle=true` for a softer look.

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

### UI Button
```xml
<ac:structured-macro ac:name="ui-button" ac:schema-version="1" ac:macro-id="UUID">
  <ac:parameter ac:name="color">blue</ac:parameter>
  <ac:parameter ac:name="title">Button Title</ac:parameter>
  <ac:parameter ac:name="url">https://wiki.cfdata.org/...</ac:parameter>
</ac:structured-macro>
```

### Expand Macro
```xml
<ac:structured-macro ac:name="expand" ac:schema-version="1" ac:macro-id="UUID">
  <ac:parameter ac:name="title">Click to Expand</ac:parameter>
  <ac:rich-text-body><p>Content</p></ac:rich-text-body>
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

### Table Filter (Stiltsoft)
```xml
<ac:structured-macro ac:name="table-filter">
  <ac:rich-text-body>
    <table><tbody>
      <tr><th>Col1</th><th>Col2</th></tr>
      <tr><td>Data</td><td>Data</td></tr>
    </tbody></table>
  </ac:rich-text-body>
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

### Children Macro (used on Notes page)
```xml
<ac:structured-macro ac:name="children" ac:schema-version="2" ac:macro-id="UUID" />
```

---

## Key Lessons Learned

- **Storage format = editable**. Rendered HTML = locked editor.
- **Jira macros**: parameter is `jqlQuery` (not `jql`), need both `server` and `serverId`, plus `ac:schema-version` and `ac:macro-id`
- **UI tabs**: parameter is `title` (not `name`), need `ac:schema-version` and `ac:macro-id`
- **UI button**: `color` is `blue` (not rgb), `url` (not `link`), no `textColor`
- **Always validate XML tag balance** before creating — mismatched tags cause API errors
- **Always fetch current version right before PUT** — pages change between fetches
- **When replacing sections**, use `find()` for the first closing tag, not `rfind()`
- **No nested panels** when replacing content inside an existing panel
- **Tool path corruption**: use `w"iki"` in URLs, use `/Users/tianaegidi/` instead of `/tmp/`
- **Verify Jira URLs** — `issues` can lose the `u` becoming `isses`
- **Decision log entries are immutable** — if reversed, add a new entry with SUPERSEDED status
- **Hub page sync** after every status update, agenda, or decision log entry
- **Layout macros** (`ac:layout`) are used on all 5 pages — be careful with closing tags when editing
- **Q1 Update page** uses orange gradient; hub page uses blue gradient — don't mix them up
- **Status update pages** use `two_right_sidebar` layout; agenda pages use `two_equal` layout