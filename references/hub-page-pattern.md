# Hub Page Pattern & Sync Workflow

## Purpose

The hub page is the program's single landing page. It provides:
- At-a-glance program status
- Quick links to all child pages (status updates, agendas, decision log)
- Team & stakeholder directory
- Main content organized in tabs

The hub page must be updated whenever child pages change to stay in sync.

---

## Hub Page Sections

1. **Gradient Header Banner** — program name with branded styling
2. **Welcome Panel** — program description and mission
3. **Latest Status Panel** — auto-synced, shows current metrics + link to latest update
4. **Quick Links Panel** — table of all key resources with last-updated dates
5. **Team & Stakeholders Panel** — who's who
6. **UI Tabs** — main content (Program Overview, Program Health, Handbook, Timeline, Resources)

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
1. Fetch the hub page
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
import json, requests, urllib3
urllib3.disable_warnings()

token = '$CF_TOKEN'
hub_page_id = 'HUB_PAGE_ID'

# Fetch hub page
resp = requests.get(
    f'https://wiki.cfdata.org/rest/api/content/{hub_page_id}?expand=body.storage,version',
    headers={'cf-access-token': token, 'X-Atlassian-Token': 'no-check'},
    verify=False
)
data = resp.json()
body = data['body']['storage']['value']
version = data['version']['number']

# --- Update Latest Status Panel ---

# Update "Last updated" date
body = body.replace(
    'Last updated:</strong> [OLD_DATE]',
    f'Last updated:</strong> {new_date}'
)

# Update status summary (find the paragraph after the status panel title)
old_summary = '<p>[OLD_SUMMARY]</p>'
new_summary = f'<p>{new_summary_text}</p>'
body = body.replace(old_summary, new_summary)

# Update button URL
body = body.replace(
    'ac:name="url">[OLD_URL]',
    f'ac:name="url">{new_status_page_url}'
)

# --- Update Quick Links Table ---

# Find the Quick Links table and update the relevant row
# Example: update "Latest Status Update" row
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

resp2 = requests.put(
    f'https://wiki.cfdata.org/rest/api/content/{hub_page_id}',
    json=payload,
    headers={
        'cf-access-token': token,
        'X-Atlassian-Token': 'no-check',
        'Content-Type': 'application/json'
    },
    verify=False
)
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

---

## Hub Page ID Tracking

Store the hub page ID and child page IDs for easy reference:

```
Hub Page:         [PAGE_ID] — Threat-Focused Defense Program
Decision Log:     [PAGE_ID] — Decision Log & Meeting Notes
Status Updates:   [PAGE_ID or tab] — Weekly Status Updates
Agendas:          [PAGE_ID or tab] — Weekly Agendas
```

These IDs should be passed to the skill when the user sets up the program. If the user doesn't know the IDs, fetch the hub page's child pages via the REST API:

```python
resp = requests.get(
    f'https://wiki.cfdata.org/rest/api/content/{hub_page_id}/child/page',
    headers={'cf-access-token': token, 'X-Atlassian-Token': 'no-check'},
    verify=False
)
for page in resp.json()['results']:
    print(f"{page['title']}: {page['id']}")
```