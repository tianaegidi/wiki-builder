# Hub Page Pattern & Sync Workflow

## Purpose

The hub page (`1276292540`) is the program's single landing page. It provides:
- At-a-glance program status
- Quick links to all child pages (status updates, agendas, decision log)
- Team & stakeholder directory
- Main content organized in 8 tabs

The hub page must be updated whenever child pages change to stay in sync.

---

## Hub Page Sections

1. **Gradient Header Banner** — program name with blue branded styling (`#1c5e98 → #206db1 → #2885d7`)
2. **Welcome Panel** — program description and mission
3. **Latest Status Panel** — auto-synced, shows current metrics + link to latest update
4. **Quick Links Panel** — table of all key resources with last-updated dates
5. **Team & Stakeholders Panel** — who's who
6. **UI Tabs** — main content (8 tabs)

---

## Hub Page Tabs

| Tab | Content | JQL Count |
|-----|---------|-----------|
| Program Overview | Threat models table with Wave 1 + Wave 2 separators | 0 (links only) |
| Program Health | 2x2 Progress Panel dashboard + threat model breakdown table | ~20 |
| Timeline & Milestones | Stiltsoft Roadmap Planner + milestones table | 0 |
| Now \| Next \| Later | 3 sub-tabs with workstream tables, Jira count macros, status lozenges | ~15 |
| Status Distribution | KPI cards, threat model breakdown, priority distribution, assignment overview | ~25 |
| Workstreams | Open/closed tickets with table filters | ~10 |
| Ticket Handling Handbook | Roles, workflows, escalation, DoD, labels, cadence | 0 |
| Resources | Links to all program resources | 0 |

---

## Progress Panel Design (DO NOT CHANGE)

The 2x2 grid in the Progress Panel is finalized. When editing these boxes:
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

### Roadmap Colors
- Wave 1 = orange (`#e8741e` / `#f5a623`)
- Wave 2 = yellow (`#f5c842` / `#fce596`)

---

## Latest Status Panel (Auto-Synced)

This panel is updated every time a status update or agenda is published.

### What Gets Updated
- Status lozenge (Green/Yellow/Red based on metrics)
- "Last updated" date
- 1-2 sentence status summary
- Metrics table (Completed, In Progress, Blocked, Unassigned) with live Jira macros
- "View Latest Status Update" button URL

### Sync Trigger
After creating a status update or weekly agenda:
1. Fetch the hub page (`1276292540`)
2. Replace the status summary text
3. Update the "Last updated" date
4. Update the button URL to point to the new status/agenda page
5. PUT the update

---

## Quick Links Panel (Auto-Synced)

| Resource | Link | Last Updated |
|----------|------|-------------|
| Latest Status Update | [URL] | [Date] |
| Latest Agenda | [URL] | [Date] |
| Decision Log | [URL] | [Date] |
| Program Dashboard | [URL] | Live |
| Ticket Handling Handbook | [URL] | [Date] |

### Sync Trigger
After creating any child page (status, agenda, decision log entry):
1. Fetch the hub page
2. Find the Quick Links table
3. Update the relevant row's URL and "Last Updated" date
4. PUT the update

---

## Hub Page Sync Code Pattern

```python
import json, requests, urllib3, subprocess, re
urllib3.disable_warnings()

# Auth
result = subprocess.run(['cloudflared', 'access', 'login', 'https://wiki.cfdata.org/'],
                        capture_output=True, text=True)
token = None
for line in (result.stdout + result.stderr).split('\n'):
    m = re.search(r'eyJ[a-zA-Z0-9._-]+', line)
    if m:
        token = m.group(0)
        break

HEADERS = {'cf-access-token': token, 'X-Atlassian-Token': 'no-check'}
hub_page_id = '1276292540'

# Fetch hub page
resp = requests.get(f'https://wiki.cfdata.org/rest/api/content/{hub_page_id}?expand=body.storage,version',
                    headers=HEADERS, verify=False)
data = resp.json()
body = data['body']['storage']['value']
version = data['version']['number']

# --- Update Latest Status Panel ---

# Update "Last updated" date
body = body.replace(
    'Last updated:</strong> [OLD_DATE]',
    f'Last updated:</strong> {new_date}'
)

# Update status summary
body = body.replace(old_summary, new_summary)

# Update button URL
body = body.replace(
    'ac:name="url">[OLD_URL]',
    f'ac:name="url">{new_status_page_url}'
)

# --- Update Quick Links Table ---
old_row = '<tr><td>Latest Status Update</td><td><a href="[OLD_URL]">[OLD_DATE]</a></td><td>[OLD_DATE]</td></tr>'
new_row = f'<tr><td>Latest Status Update</td><td><a href="{new_url}">{new_date}</a></td><td>{new_date}</td></tr>'
body = body.replace(old_row, new_row)

# --- PUT Update ---
payload = {
    'id': hub_page_id,
    'type': 'page',
    'title': data['title'],
    'body': {'storage': {'value': body, 'representation': 'storage'}},
    'version': {'number': version + 1}
}

resp2 = requests.put(f'https://wiki.cfdata.org/rest/api/content/{hub_page_id}',
                     json=payload,
                     headers={**HEADERS, 'Content-Type': 'application/json'},
                     verify=False)
```

---

## When to Sync the Hub Page

| Trigger | What to Update |
|---------|---------------|
| New status update published | Latest Status panel + Quick Links (status row) |
| New agenda created | Quick Links (agenda row) |
| New decision logged | Quick Links (decision log row date) |
| New threat model added | Program Overview tab table |
| Threat model status changes | Program Overview tab + Latest Status panel |
| Team member added/removed | Team & Stakeholders panel |
| Quarterly review completed | Program Overview tab + Latest Status panel + Quick Links |
