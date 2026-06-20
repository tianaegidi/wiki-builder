---
name: wiki-builder
description: All-in-one program management skill for Confluence wiki pages on wiki.cfdata.org. Create, edit, and revise wiki pages with dynamic Jira macros, panels, tabs, tables, and roadmaps. Generate weekly agendas, status updates, and executive summaries. Maintain a program hub page that stays in sync with child pages. Track decisions and meeting notes in a decision log. Use when the user mentions wiki.cfdata.org, Confluence, program management, weekly agenda, status update, decision log, hub page, or wants to build/edit/revamp wiki pages.
---

# Program Wiki Builder

All-in-one skill for managing a security program's Confluence presence on wiki.cfdata.org. Handles the full lifecycle: page creation, editing, revision, weekly agendas, status updates, hub page sync, and decision log tracking.

## Prerequisites

1. **Script**: `~/wikigen-generic.sh` must exist and be executable
2. **Cloudflared token**: Valid token in `~/.cloudflared/` for `wiki.cfdata.org`. If missing:
   ```bash
   cloudflared access login https://wiki.cfdata.org/
   ```
3. **Jira app link ID**: `cc100dec-3d79-305b-8fae-4caba5e44cd2`
4. **Python requests**: `pip3 install requests` (used for page updates)

## Critical Rule: Use Storage Format, NOT Rendered HTML

**ALWAYS use Confluence Storage Format (XHTML)** for page content. Never use rendered HTML with JavaScript, DOM IDs, or plugin-generated markup. Rendered HTML blocks the Confluence editor and makes pages uneditable.

## Tool Bug Workarounds

When using bash/curl with wiki URLs, the tool corrupts paths:
- `wiki` becomes `iki` — workaround: use `w"iki"` in URLs
- `tmp` becomes `ttp` — workaround: use `/Users/tianaegidi/` for temp files instead of `/tmp/`
- `issues` can lose the `u` becoming `isses` — always verify URLs in generated content

## Content File Structure

Every page content file must start with:
```xml
<ac:confluence xmlns:ac="https://jira.atlassian.com/wiki" xmlns:ri="http://atlassian.com/resource/identifier">
```
And end with `</ac:confluence>`. Do NOT include `<?xml?>` or `<!DOCTYPE>` declarations.

---

## Part 1: Page Creation & Editing

### Creating a Page

```bash
~/wikigen-generic.sh -s INFOSEC -t "Page Title" -i PARENT_PAGE_ID -c ~/content.html
```

Flags: `-s SPACE_KEY`, `-t "Title"`, `-i PARENT_ID` (optional), `-c content.html`

### Updating an Existing Page

Use Python with `requests` for reliability (avoids curl path corruption):

```python
import json, requests, urllib3
urllib3.disable_warnings()

token = '$CF_TOKEN'
url = 'https://wiki.cfdata.org/rest/api/content/PAGE_ID?expand=body.storage,version'
resp = requests.get(url, headers={'cf-access-token': token, 'X-Atlassian-Token': 'no-check'}, verify=False)
data = resp.json()
body = data['body']['storage']['value']
version = data['version']['number']

# Modify body here
new_body = body[:start] + new_content + body[end:]

payload = {
    'id': 'PAGE_ID', 'type': 'page', 'title': data['title'],
    'body': {'storage': {'value': new_body, 'representation': 'storage'}},
    'version': {'number': version + 1}
}

resp2 = requests.put('https://wiki.cfdata.org/rest/api/content/PAGE_ID', json=payload,
    headers={'cf-access-token': token, 'X-Atlassian-Token': 'no-check', 'Content-Type': 'application/json'},
    verify=False)
```

**IMPORTANT**: Always fetch the version right before updating — pages can be edited by others between fetches.

### Finding Section Boundaries for Replacement

```python
# Find the panel/macro by title
idx = body.find('ac:name="panel"')
# Find the rich-text-body opening
content_start = body.find('<ac:rich-text-body>', idx)
content_start = body.find('>', content_start) + 1
# Find the closing tags
panel_close = body.find('</ac:rich-text-body></ac:structured-macro>', content_start)
old_end = panel_close + len('</ac:rich-text-body></ac:structured-macro>')
# Replace body[content_start:old_end]
```

Use `find()` for the first closing tag after the section start, NOT `rfind()` which can match parent elements.

### Simple String Replacement

For small changes (text swaps, title updates):
```python
body = body.replace('old text', 'new text')
```

---

## Part 2: Weekly Agenda Generation

When the user asks for a weekly agenda, generate a Confluence page or append to an existing agenda page.

### Weekly Sync Agenda Template

Structure: 30-minute standing meeting, same day each week.

```xml
<h2>📅 Weekly Sync — [Date]</h2>

<ac:structured-macro ac:name="panel">
  <ac:parameter ac:name="title">Meeting Details</ac:parameter>
  <ac:parameter ac:name="titleBGColor">#1c5e98</ac:parameter>
  <ac:parameter ac:name="titleColor">#FFFFFF</ac:parameter>
  <ac:rich-text-body>
    <table>
      <tbody>
        <tr><td><strong>Date</strong></td><td>[Date]</td></tr>
        <tr><td><strong>Time</strong></td><td>[Time + Timezone]</td></tr>
        <tr><td><strong>Attendees</strong></td><td>[List names]</td></tr>
        <tr><td><strong>Facilitator</strong></td><td>[Name]</td></tr>
        <tr><td><strong>Notes</strong></td><td>[Note taker name]</td></tr>
      </tbody>
    </table>
  </ac:rich-text-body>
</ac:structured-macro>

<h3>Agenda</h3>
<table>
  <tbody>
    <tr><th>Time</th><th>Topic</th><th>Owner</th><th>Type</th></tr>
    <tr><td>0:00</td><td>Roll call + agenda review</td><td>Facilitator</td><td>Standing</td></tr>
    <tr><td>0:02</td><td>Program health dashboard review</td><td>TPM</td><td>Standing</td></tr>
    <tr><td>0:10</td><td>Threat model spotlight (rotating)</td><td>[Lead Assessor]</td><td>Rotating</td></tr>
    <tr><td>0:20</td><td>Blockers &amp; escalations</td><td>Open floor</td><td>Standing</td></tr>
    <tr><td>0:25</td><td>Action items + next week preview</td><td>Facilitator</td><td>Standing</td></tr>
  </tbody>
</table>

<h3>Dashboard Snapshot</h3>
<ac:structured-macro ac:name="panel">
  <ac:parameter ac:name="title">Live Metrics</ac:parameter>
  <ac:rich-text-body>
    <table>
      <tbody>
        <tr><th>Metric</th><th>Current</th><th>Trend</th></tr>
        <tr><td>Total Controls</td><td>[Jira count macro]</td><td>[+/- from last week]</td></tr>
        <tr><td>Completed</td><td>[Jira count macro]</td><td>[+/-]</td></tr>
        <tr><td>In Progress</td><td>[Jira count macro]</td><td>[+/-]</td></tr>
        <tr><td>Blocked</td><td>[Jira count macro]</td><td>[+/-]</td></tr>
        <tr><td>Unassigned</td><td>[Jira count macro]</td><td>[+/-]</td></tr>
      </tbody>
    </table>
  </ac:rich-text-body>
</ac:structured-macro>

<h3>Threat Model Spotlight: [Model Name]</h3>
<ac:structured-macro ac:name="expand" ac:schema-version="1" ac:macro-id="UUID">
  <ac:parameter ac:name="title">Click to expand spotlight details</ac:parameter>
  <ac:rich-text-body>
    <p><strong>Lead:</strong> [Name]</p>
    <p><strong>Current status:</strong> [Status lozenge]</p>
    <p><strong>Progress this week:</strong></p>
    <ul><li>[Item 1]</li><li>[Item 2]</li></ul>
    <p><strong>Next steps:</strong></p>
    <ul><li>[Item 1]</li><li>[Item 2]</li></ul>
    <p><strong>Risks/Blockers:</strong></p>
    <ul><li>[Item 1]</li></ul>
  </ac:rich-text-body>
</ac:structured-macro>

<h3>Blockers &amp; Escalations</h3>
<table>
  <tbody>
    <tr><th>Blocker</th><th>Owner</th><th>Days Blocked</th><th>Action</th><th>Escalation</th></tr>
    <tr><td>[Description]</td><td>[Name]</td><td>[N]</td><td>[Action]</td><td>[Contact]</td></tr>
  </tbody>
</table>

<h3>Action Items</h3>
<table>
  <tbody>
    <tr><th>#</th><th>Action</th><th>Owner</th><th>Due</th><th>Status</th></tr>
    <tr><td>1</td><td>[Action]</td><td>[Name]</td><td>[Date]</td><td>[Lozenge]</td></tr>
  </tbody>
</table>

<h3>Decisions Made</h3>
<table>
  <tbody>
    <tr><th>Decision</th><th>Rationale</th><th>Decided By</th></tr>
    <tr><td>[Decision]</td><td>[Why]</td><td>[Names]</td></tr>
  </tbody>
</table>
```

### Quarterly Review Agenda Template

```xml
<h2>🗓️ Quarterly Review — [Quarter] [Year]</h2>

<ac:structured-macro ac:name="panel">
  <ac:parameter ac:name="title">Review Scope</ac:parameter>
  <ac:parameter ac:name="titleBGColor">#6554C0</ac:parameter>
  <ac:parameter ac:name="titleColor">#FFFFFF</ac:parameter>
  <ac:rich-text-body>
    <table>
      <tbody>
        <tr><td><strong>Date</strong></td><td>[Date]</td></tr>
        <tr><td><strong>Duration</strong></td><td>90 minutes</td></tr>
        <tr><td><strong>Attendees</strong></td><td>[List]</td></tr>
      </tbody>
    </table>
  </ac:rich-text-body>
</ac:structured-macro>

<h3>Agenda</h3>
<table>
  <tbody>
    <tr><th>Time</th><th>Topic</th><th>Owner</th></tr>
    <tr><td>0:00</td><td>Quarter recap — wins, misses, metrics</td><td>TPM</td></tr>
    <tr><td>0:15</td><td>Threat model deep dive (each model lead presents)</td><td>Lead Assessors</td></tr>
    <tr><td>0:45</td><td>Process retro — what worked, what didn't</td><td>Open floor</td></tr>
    <tr><td>0:60</td><td>Next quarter planning — scope, priorities, resourcing</td><td>TPM + Sponsors</td></tr>
    <tr><td>0:80</td><td>Action items + commitments</td><td>Facilitator</td></tr>
  </tbody>
</table>

<h3>Quarter Metrics Summary</h3>
<table>
  <tbody>
    <tr><th>Metric</th><th>Start of Quarter</th><th>End of Quarter</th><th>Delta</th></tr>
    <tr><td>Total Controls</td><td>[N]</td><td>[N]</td><td>[+/-]</td></tr>
    <tr><td>Completed</td><td>[N]</td><td>[N]</td><td>[+/-]</td></tr>
    <tr><td>Blocked (avg)</td><td>[N]</td><td>[N]</td><td>[+/-]</td></tr>
  </tbody>
</table>
```

### Threat Model Review Agenda Template

```xml
<h2>🔍 Threat Model Review — [Model Name]</h2>

<ac:structured-macro ac:name="panel">
  <ac:parameter ac:name="title">Review Details</ac:parameter>
  <ac:parameter ac:name="titleBGColor">#FF5630</ac:parameter>
  <ac:parameter ac:name="titleColor">#FFFFFF</ac:parameter>
  <ac:rich-text-body>
    <table>
      <tbody>
        <tr><td><strong>Threat Model</strong></td><td>[Name]</td></tr>
        <tr><td><strong>Lead Assessor</strong></td><td>[Name]</td></tr>
        <tr><td><strong>Date</strong></td><td>[Date]</td></tr>
        <tr><td><strong>Duration</strong></td><td>45 minutes</td></tr>
      </tbody>
    </table>
  </ac:rich-text-body>
</ac:structured-macro>

<h3>Agenda</h3>
<table>
  <tbody>
    <tr><th>Time</th><th>Topic</th></tr>
    <tr><td>0:00</td><td>Threat model overview + scope confirmation</td></tr>
    <tr><td>0:10</td><td>Control coverage review (what's done, in progress, missing)</td></tr>
    <tr><td>0:25</td><td>Risk gap analysis — unaddressed threats</td></tr>
    <tr><td>0:35</td><td>Next steps + resource needs</td></tr>
    <tr><td>0:40</td><td>Action items</td></tr>
  </tbody>
</table>

<h3>Control Coverage</h3>
<table>
  <tbody>
    <tr><th>Control</th><th>Status</th><th>Owner</th><th>Due</th><th>Notes</th></tr>
    <tr><td>[Control name]</td><td>[Lozenge]</td><td>[Name]</td><td>[Date]</td><td>[Notes]</td></tr>
  </tbody>
</table>
```

### Agenda Workflow

1. Ask the user for: date, attendees, which threat model is in the spotlight (if rotating)
2. Fetch live Jira counts for the dashboard snapshot
3. Generate the page as a child of the program hub page
4. Append to an "Agendas" tab or create a standalone page
5. Share the URL

---

## Part 3: Status Updates

### Weekly Status Update (Wiki Section or Slack)

```xml
<h2>📊 Weekly Status — Week of [Date]</h2>

<ac:structured-macro ac:name="panel">
  <ac:parameter ac:name="title">Program Status</ac:parameter>
  <ac:parameter ac:name="titleBGColor">#1c5e98</ac:parameter>
  <ac:parameter ac:name="titleColor">#FFFFFF</ac:parameter>
  <ac:rich-text-body>
    <p><ac:structured-macro ac:name="status"><ac:parameter ac:name="colour">Green</ac:parameter><ac:parameter ac:name="title">ON TRACK</ac:parameter></ac:structured-macro></p>
    <table>
      <tbody>
        <tr><th>Metric</th><th>This Week</th><th>Last Week</th><th>Trend</th></tr>
        <tr><td>Total Controls</td><td>[Jira macro]</td><td>[N]</td><td>[+/-]</td></tr>
        <tr><td>Completed</td><td>[Jira macro]</td><td>[N]</td><td>[+/-]</td></tr>
        <tr><td>In Progress</td><td>[Jira macro]</td><td>[N]</td><td>[+/-]</td></tr>
        <tr><td>Blocked</td><td>[Jira macro]</td><td>[N]</td><td>[+/-]</td></tr>
        <tr><td>Unassigned</td><td>[Jira macro]</td><td>[N]</td><td>[+/-]</td></tr>
      </tbody>
    </table>
  </ac:rich-text-body>
</ac:structured-macro>

<h3>Highlights</h3>
<ul>
  <li>[Key accomplishment 1]</li>
  <li>[Key accomplishment 2]</li>
</ul>

<h3>Concerns</h3>
<ul>
  <li>[Risk or blocker 1]</li>
</ul>

<h3>Per-Threat-Model Status</h3>
<table>
  <tbody>
    <tr><th>Threat Model</th><th>Status</th><th>Done / Total</th><th>Notes</th></tr>
    <tr><td>Compromise of Core/Edge</td><td>[Lozenge]</td><td>[Jira macro] / [Jira macro]</td><td>[Notes]</td></tr>
    <tr><td>Malicious Insider Risk</td><td>[Lozenge]</td><td>[Jira macro] / [Jira macro]</td><td>[Notes]</td></tr>
    <!-- ... repeat for each threat model ... -->
  </tbody>
</table>

<h3>Looking Ahead</h3>
<ul>
  <li>[Next week priority 1]</li>
  <li>[Upcoming milestone]</li>
</ul>
```

### Monthly Executive Summary

```xml
<h2>📋 Monthly Executive Summary — [Month] [Year]</h2>

<ac:structured-macro ac:name="panel">
  <ac:parameter ac:name="title">Executive Summary</ac:parameter>
  <ac:parameter ac:name="titleBGColor">#1c5e98</ac:parameter>
  <ac:parameter ac:name="titleColor">#FFFFFF</ac:parameter>
  <ac:rich-text-body>
    <p>[2-3 sentence narrative of program health, major wins, and key risks]</p>
    
    <table>
      <tbody>
        <tr><th>Indicator</th><th>Status</th><th>Detail</th></tr>
        <tr><td>Overall Program Health</td><td>[Lozenge]</td><td>[Brief]</td></tr>
        <tr><td>Controls Completion Rate</td><td>[Lozenge]</td><td>[N%] ([Done]/[Total])</td></tr>
        <tr><td>Blocked Items</td><td>[Lozenge]</td><td>[N] blocked, [N] &gt; 3 days</td></tr>
        <tr><td>Unassigned Tickets</td><td>[Lozenge]</td><td>[N] tickets</td></tr>
      </tbody>
    </table>
  </ac:rich-text-body>
</ac:structured-macro>

<h3>Wins This Month</h3>
<ul><li>[Win 1]</li><li>[Win 2]</li></ul>

<h3>Key Risks</h3>
<table>
  <tbody>
    <tr><th>Risk</th><th>Impact</th><th>Mitigation</th><th>Owner</th></tr>
    <tr><td>[Risk]</td><td>[High/Med/Low]</td><td>[Action]</td><td>[Name]</td></tr>
  </tbody>
</table>

<h3>Threat Model Progress</h3>
<table>
  <tbody>
    <tr><th>Threat Model</th><th>Wave</th><th>Lead</th><th>Completion</th><th>Status</th><th>Key Update</th></tr>
    <tr><td>[Model]</td><td>[1/2]</td><td>[Name]</td><td>[N%]</td><td>[Lozenge]</td><td>[Summary]</td></tr>
  </tbody>
</table>

<h3>Decisions This Month</h3>
<table>
  <tbody>
    <tr><th>Date</th><th>Decision</th><th>Rationale</th><th>Decided By</th></tr>
    <tr><td>[Date]</td><td>[Decision]</td><td>[Why]</td><td>[Who]</td></tr>
  </tbody>
</table>

<h3>Focus Areas Next Month</h3>
<ol><li>[Priority 1]</li><li>[Priority 2]</li></ol>
```

### Status Update Workflow

1. Fetch live Jira counts for all metrics
2. Ask user for highlights, concerns, and narrative
3. Compare with last week's numbers (fetch previous status page or ask user)
4. Generate the content
5. Either: create a new child page, append to a "Status Updates" tab, or format as Slack message
6. Update the hub page's "Latest Status" section to point to the new update

---

## Part 4: Hub Page Management

The hub page is the program's landing page. It must stay in sync with child pages and reflect the latest status.

### Hub Page Structure

```xml
<!-- Gradient header banner -->
<ac:structured-macro ac:name="style">
  <ac:plain-text-body><![CDATA[
    #grad1 { background: linear-gradient(145deg, #1c5e98, #206db1, #2885d7); padding: 1em; }
  ]]></ac:plain-text-body>
</ac:structured-macro>
<div id="grad1"><h1><span style="color:#ffffff;">[Program Name]</span></h1></div>

<!-- Welcome panel -->
<ac:structured-macro ac:name="panel">
  <ac:parameter ac:name="title">Welcome</ac:parameter>
  <ac:parameter ac:name="titleBGColor">#1c5e98</ac:parameter>
  <ac:parameter ac:name="titleColor">#FFFFFF</ac:parameter>
  <ac:rich-text-body>
    <p>[Program description]</p>
  </ac:rich-text-body>
</ac:structured-macro>

<!-- Latest Status panel (auto-updated) -->
<ac:structured-macro ac:name="panel">
  <ac:parameter ac:name="title">Latest Status</ac:parameter>
  <ac:parameter ac:name="titleBGColor">#36B37E</ac:parameter>
  <ac:parameter ac:name="titleColor">#FFFFFF</ac:parameter>
  <ac:rich-text-body>
    <p><ac:structured-macro ac:name="status"><ac:parameter ac:name="colour">Green</ac:parameter><ac:parameter ac:name="title">ON TRACK</ac:parameter></ac:structured-macro></p>
    <p><strong>Last updated:</strong> [Date]</p>
    <p>[1-2 sentence status summary]</p>
    <table>
      <tbody>
        <tr><th>Completed</th><th>In Progress</th><th>Blocked</th><th>Unassigned</th></tr>
        <tr><td>[Jira macro]</td><td>[Jira macro]</td><td>[Jira macro]</td><td>[Jira macro]</td></tr>
      </tbody>
    </table>
    <p><ac:structured-macro ac:name="ui-button" ac:schema-version="1" ac:macro-id="UUID">
      <ac:parameter ac:name="color">blue</ac:parameter>
      <ac:parameter ac:name="title">View Latest Status Update</ac:parameter>
      <ac:parameter ac:name="url">[Link to latest status page]</ac:parameter>
    </ac:structured-macro></p>
  </ac:rich-text-body>
</ac:structured-macro>

<!-- Quick Links panel -->
<ac:structured-macro ac:name="panel">
  <ac:parameter ac:name="title">Quick Links</ac:parameter>
  <ac:rich-text-body>
    <table>
      <tbody>
        <tr><th>Resource</th><th>Link</th><th>Last Updated</th></tr>
        <tr><td>Latest Status Update</td><td><a href="[URL]">[Date]</a></td><td>[Date]</td></tr>
        <tr><td>Latest Agenda</td><td><a href="[URL]">[Date]</a></td><td>[Date]</td></tr>
        <tr><td>Decision Log</td><td><a href="[URL]">View</a></td><td>[Date]</td></tr>
        <tr><td>Program Dashboard</td><td><a href="[URL]">View</a></td><td>Live</td></tr>
        <tr><td>Ticket Handling Handbook</td><td><a href="[URL]">View</a></td><td>[Date]</td></tr>
      </tbody>
    </table>
  </ac:rich-text-body>
</ac:structured-macro>

<!-- Team & Stakeholders -->
<ac:structured-macro ac:name="panel">
  <ac:parameter ac:name="title">Team &amp; Stakeholders</ac:parameter>
  <ac:rich-text-body>
    <table>
      <tbody>
        <tr><th>Name</th><th>Role</th><th>Threat Model</th><th>Slack</th></tr>
        <tr><td>[Name]</td><td>[Role]</td><td>[Model]</td><td>@[handle]</td></tr>
      </tbody>
    </table>
  </ac:rich-text-body>
</ac:structured-macro>

<!-- Main content tabs -->
<ac:structured-macro ac:name="ui-tabs" ac:schema-version="1" ac:macro-id="UUID">
  <ac:rich-text-body>
    <ac:structured-macro ac:name="ui-tab" ac:schema-version="1" ac:macro-id="UUID">
      <ac:parameter ac:name="title">Program Overview</ac:parameter>
      <ac:rich-text-body>[Threat models table with waves]</ac:rich-text-body>
    </ac:structured-macro>
    <ac:structured-macro ac:name="ui-tab" ac:schema-version="1" ac:macro-id="UUID">
      <ac:parameter ac:name="title">Program Health</ac:parameter>
      <ac:rich-text-body>[Dashboard with Jira macros]</ac:rich-text-body>
    </ac:structured-macro>
    <ac:structured-macro ac:name="ui-tab" ac:schema-version="1" ac:macro-id="UUID">
      <ac:parameter ac:name="title">Ticket Handling Handbook</ac:parameter>
      <ac:rich-text-body>[Handbook content]</ac:rich-text-body>
    </ac:structured-macro>
    <ac:structured-macro ac:name="ui-tab" ac:schema-version="1" ac:macro-id="UUID">
      <ac:parameter ac:name="title">Timeline &amp; Milestones</ac:parameter>
      <ac:rich-text-body>[Roadmap + milestones table]</ac:rich-text-body>
    </ac:structured-macro>
    <ac:structured-macro ac:name="ui-tab" ac:schema-version="1" ac:macro-id="UUID">
      <ac:parameter ac:name="title">Resources</ac:parameter>
      <ac:rich-text-body>[Resource links]</ac:rich-text-body>
    </ac:structured-macro>
  </ac:rich-text-body>
</ac:structured-macro>
```

### Hub Page Sync Workflow

When a new status update, agenda, or decision log entry is created, update the hub page:

1. **Fetch the hub page** storage format and version
2. **Update the "Latest Status" panel**:
   - Replace the status summary text
   - Update the "Last updated" date
   - Update the "View Latest Status Update" button URL
3. **Update the "Quick Links" table**:
   - Add/update the row for the latest status update
   - Add/update the row for the latest agenda
   - Update "Last Updated" dates
4. **PUT the update** with incremented version

```python
# Example: update Latest Status panel on hub page
hub_page_id = '1424133824'

# Fetch hub page
resp = requests.get(f'https://wiki.cfdata.org/rest/api/content/{hub_page_id}?expand=body.storage,version', ...)
body = resp.json()['body']['storage']['value']
version = resp.json()['version']['number']

# Update last updated date
body = body.replace('Last updated:</strong> [old date]', f'Last updated:</strong> {new_date}')

# Update status summary
old_summary_start = body.find('<p>[old summary]</p>')
# ... find and replace ...

# Update button URL
body = body.replace('ac:name="url">[old url]', f'ac:name="url">{new_url}')

# PUT update
```

---

## Part 5: Decision Log & Meeting Notes

### Decision Log Page Structure

Create a dedicated decision log page as a child of the hub page:

```xml
<ac:confluence xmlns:ac="https://jira.atlassian.com/wiki" xmlns:ri="http://atlassian.com/resource/identifier">

<h1>📝 Decision Log — [Program Name]</h1>

<ac:structured-macro ac:name="panel">
  <ac:parameter ac:name="title">About This Log</ac:parameter>
  <ac:parameter ac:name="titleBGColor">#1c5e98</ac:parameter>
  <ac:parameter ac:name="titleColor">#FFFFFF</ac:parameter>
  <ac:rich-text-body>
    <p>This page tracks all decisions made in the [Program Name]. Each entry includes the decision, rationale, date, and stakeholders. Decisions are immutable once logged — if a decision is reversed, add a new entry referencing the original.</p>
  </ac:rich-text-body>
</ac:structured-macro>

<h2>Decision Log</h2>

<ac:structured-macro ac:name="panel">
  <ac:parameter ac:name="title">All Decisions</ac:parameter>
  <ac:rich-text-body>
    <table>
      <tbody>
        <tr>
          <th>#</th>
          <th>Date</th>
          <th>Decision</th>
          <th>Rationale</th>
          <th>Decided By</th>
          <th>Stakeholders</th>
          <th>Impact</th>
          <th>Status</th>
          <th>Supersedes</th>
        </tr>
        <tr>
          <td>1</td>
          <td>[Date]</td>
          <td><strong>[Decision text]</strong></td>
          <td>[Why this decision was made]</td>
          <td>[Name(s)]</td>
          <td>[Affected teams/people]</td>
          <td>[What changes because of this]</td>
          <td><ac:structured-macro ac:name="status"><ac:parameter ac:name="colour">Green</ac:parameter><ac:parameter ac:name="title">ACTIVE</ac:parameter></ac:structured-macro></td>
          <td>—</td>
        </tr>
        <tr>
          <td>2</td>
          <td>[Date]</td>
          <td><strong>[Decision text]</strong></td>
          <td>[Why]</td>
          <td>[Name(s)]</td>
          <td>[Stakeholders]</td>
          <td>[Impact]</td>
          <td><ac:structured-macro ac:name="status"><ac:parameter ac:name="colour">Grey</ac:parameter><ac:parameter ac:name="title">SUPERSEDED</ac:parameter></ac:structured-macro></td>
          <td>—</td>
        </tr>
      </tbody>
    </table>
  </ac:rich-text-body>
</ac:structured-macro>

<h2>Meeting Notes Archive</h2>

<ac:structured-macro ac:name="expand" ac:schema-version="1" ac:macro-id="UUID-1">
  <ac:parameter ac:name="title">📅 [Date] — Weekly Sync</ac:parameter>
  <ac:rich-text-body>
    <p><strong>Attendees:</strong> [Names]</p>
    <p><strong>Facilitator:</strong> [Name]</p>
    <h3>Discussion</h3>
    <ul><li>[Topic 1: summary]</li><li>[Topic 2: summary]</li></ul>
    <h3>Decisions</h3>
    <ul><li>[Decision 1]</li></ul>
    <h3>Action Items</h3>
    <table>
      <tbody>
        <tr><th>#</th><th>Action</th><th>Owner</th><th>Due</th></tr>
        <tr><td>1</td><td>[Action]</td><td>[Name]</td><td>[Date]</td></tr>
      </tbody>
    </table>
  </ac:rich-text-body>
</ac:structured-macro>

<ac:structured-macro ac:name="expand" ac:schema-version="1" ac:macro-id="UUID-2">
  <ac:parameter ac:name="title">📅 [Date] — Quarterly Review</ac:parameter>
  <ac:rich-text-body>
    <p>[Meeting notes content]</p>
  </ac:rich-text-body>
</ac:structured-macro>

</ac:confluence>
```

### Adding a Decision to the Log

To append a new decision to the decision log page:

```python
# Fetch decision log page
resp = requests.get(f'https://wiki.cfdata.org/rest/api/content/{decision_log_page_id}?expand=body.storage,version', ...)
body = resp.json()['body']['storage']['value']
version = resp.json()['version']['number']

# Find the last row in the decisions table (before </tbody>)
tbody_close = body.find('</tbody>', body.find('All Decisions'))
new_row = f'''<tr>
  <td>{decision_number}</td>
  <td>{date}</td>
  <td><strong>{decision}</strong></td>
  <td>{rationale}</td>
  <td>{decided_by}</td>
  <td>{stakeholders}</td>
  <td>{impact}</td>
  <td><ac:structured-macro ac:name="status"><ac:parameter ac:name="colour">Green</ac:parameter><ac:parameter ac:name="title">ACTIVE</ac:parameter></ac:structured-macro></td>
  <td>—</td>
</tr>'''

body = body[:tbody_close] + new_row + body[tbody_close:]

# PUT update with version + 1
```

### Adding Meeting Notes

To append meeting notes as a new expand section:

```python
# Find the last expand macro before </ac:confluence>
confluence_close = body.rfind('</ac:confluence>')
new_notes = f'''<ac:structured-macro ac:name="expand" ac:schema-version="1" ac:macro-id="{uuid4()}">
  <ac:parameter ac:name="title">📅 {date} — {meeting_type}</ac:parameter>
  <ac:rich-text-body>
    <p><strong>Attendees:</strong> {attendees}</p>
    <h3>Discussion</h3>
    <ul>{discussion_items}</ul>
    <h3>Decisions</h3>
    <ul>{decisions}</ul>
    <h3>Action Items</h3>
    <table><tbody>
      <tr><th>#</th><th>Action</th><th>Owner</th><th>Due</th></tr>
      {action_rows}
    </tbody></table>
  </ac:rich-text-body>
</ac:structured-macro>'''

body = body[:confluence_close] + new_notes + body[confluence_close:]
```

### Decision Log Workflow

1. When a decision is made (in a meeting, via email, or in Slack), the user asks to log it
2. Ask for: decision text, rationale, who decided, stakeholders, impact
3. Fetch the decision log page
4. Append a new row to the decisions table
5. If meeting notes are also being added, append an expand section
6. Update the hub page's Quick Links to reflect the latest decision date
7. If the decision affects the program scope (e.g., adding a threat model), also update the Program Overview tab

---

## Part 6: Full Program Workflow

Here's how all the pieces fit together in a weekly cycle:

### Monday
1. **Generate weekly agenda** — create agenda page with live Jira metrics
2. **Run the sync** — use the agenda to run the meeting
3. **Log decisions** — add any decisions to the decision log
4. **Log meeting notes** — append notes to the decision log page
5. **Update hub page** — sync Latest Status panel + Quick Links

### Wednesday
1. **Mid-week check** — fetch Jira counts, flag any new blockers
2. **Update status** if significant changes

### Friday
1. **Generate weekly status update** — with metrics, highlights, concerns
2. **Update hub page** — point to new status update
3. **Prepare next week's agenda** — draft agenda with spotlight topic

### End of Month
1. **Generate monthly executive summary**
2. **Update hub page** with executive summary link
3. **Review decision log** — mark any superseded decisions

### End of Quarter
1. **Generate quarterly review agenda**
2. **Run quarterly review**
3. **Log all decisions**
4. **Update program scope** — add/remove threat models in Program Overview table
5. **Update hub page** with new quarter info

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
- `server` = display name "Cloudflare Jira"
- `serverId` = `cc100dec-3d79-305b-8fae-4caba5e44cd2`
- Each macro needs unique `ac:macro-id` (UUID)

### Panel Macro
```xml
<ac:structured-macro ac:name="panel">
  <ac:parameter ac:name="title">Title</ac:parameter>
  <ac:parameter ac:name="titleBGColor">#1c5e98</ac:parameter>
  <ac:parameter ac:name="titleColor">#FFFFFF</ac:parameter>
  <ac:rich-text-body><p>Content</p></ac:rich-text-body>
</ac:structured-macro>
```

### Status Lozenge
```xml
<ac:structured-macro ac:name="status">
  <ac:parameter ac:name="colour">Green</ac:parameter>
  <ac:parameter ac:name="title">ON TRACK</ac:parameter>
</ac:structured-macro>
```
Colours: Green, Blue, Yellow, Red, Grey

### Info Macro
```xml
<ac:structured-macro ac:name="info">
  <ac:parameter ac:name="title">Title</ac:parameter>
  <ac:rich-text-body><p>Content</p></ac:rich-text-body>
</ac:structured-macro>
```

### UI Button
```xml
<ac:structured-macro ac:name="ui-button" ac:schema-version="1" ac:macro-id="UUID">
  <ac:parameter ac:name="color">blue</ac:parameter>
  <ac:parameter ac:name="title">Button Title</ac:parameter>
  <ac:parameter ac:name="url">https://wiki.cfdata.org/...</ac:parameter>
</ac:structured-macro>
```
`color` is `blue` (not rgb), `url` (not `link`), no `textColor`.

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

### Expand Macro
```xml
<ac:structured-macro ac:name="expand" ac:schema-version="1" ac:macro-id="UUID">
  <ac:parameter ac:name="title">Click to Expand</ac:parameter>
  <ac:rich-text-body><p>Content</p></ac:rich-text-body>
</ac:structured-macro>
```

### Style Macro (CSS)
```xml
<ac:structured-macro ac:name="style">
  <ac:plain-text-body><![CDATA[
    #grad1 { background: linear-gradient(145deg, #1c5e98, #206db1, #2885d7); padding: 1em; }
  ]]></ac:plain-text-body>
</ac:structured-macro>
```

### Section/Column Layout
```xml
<ac:structured-macro ac:name="section">
  <ac:rich-text-body>
    <ac:structured-macro ac:name="column">
      <ac:rich-text-body><p>Content</p></ac:rich-text-body>
    </ac:structured-macro>
  </ac:rich-text-body>
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

---

## UI/UX Design Patterns

### Pattern 1: Landing Page with Tabs
Gradient header banner → Welcome panel → Latest Status panel → Quick Links → Team table → UI tabs

### Pattern 2: Program Health Dashboard
2x2 colored panel grid with Jira count macros. Green = done, Blue = in progress, Yellow = needs attention, Red = blocked.

### Pattern 3: Handbook / Reference Tab
Intro panel → Roles table → Threat models list → Workflow guides → Label reference → Escalation paths → Definition of Done → Weekly cadence table

### Pattern 4: Workstreams / Tickets
3-column summary cards (Backlog, In Progress, Completed) with Jira counts → Table Filter macro for open tickets

### Pattern 5: Timeline & Milestones
Roadmap Planner macro → Milestones table with status lozenges → Expand macro for details

### Pattern 6: Agenda Page
Meeting details panel → Agenda table → Dashboard snapshot with live Jira counts → Threat model spotlight (expand) → Blockers table → Action items table → Decisions table

### Pattern 7: Status Update Page
Status panel with lozenge → Metrics table (this week vs last week) → Highlights → Concerns → Per-threat-model status table → Looking ahead

### Pattern 8: Decision Log Page
About panel → Decisions table (immutable rows, status lozenges) → Meeting notes archive (expand macros per meeting)

---

## Key Lessons Learned

- **Storage format = editable**. Rendered HTML = locked editor.
- **Jira macros**: parameter is `jqlQuery` (not `jql`), need both `server` and `serverId`, plus `ac:schema-version` and `ac:macro-id`
- **UI tabs**: parameter is `title` (not `name`), need `ac:schema-version` and `ac:macro-id`
- **UI button**: `color` is `blue` (not rgb), `url` (not `link`), no `textColor`
- **Always validate XML tag balance** before creating — mismatched tags cause API errors
- **Always fetch current version right before PUT** — pages change between fetches
- **When replacing sections**, use `find()` for the first closing tag, not `rfind()`
- **No nested panels** when replacing content inside an existing panel — just replace the inner content
- **Tool path corruption**: use `w"iki"` in URLs, use `/Users/tianaegidi/` instead of `/tmp/`
- **Verify Jira URLs** in generated content — `issues` can lose the `u` becoming `isses`
- **Decision log entries are immutable** — if reversed, add a new entry with `SUPERSEDED` status referencing the original
- **Hub page sync** is critical — after every status update or agenda, update the hub page's Latest Status panel and Quick Links