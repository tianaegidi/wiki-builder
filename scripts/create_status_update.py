#!/usr/bin/env python3
"""
TFD Weekly Status Update Creator
================================
Creates a new weekly status update page under TFD Status Updates 2026 (1424137842).

Usage:
  python3 create_status_update.py

Fill in the STATUS_CONFIG section below before running.
"""
import json, requests, urllib3, subprocess, re, uuid
urllib3.disable_warnings()

# ============================================================
# STATUS CONFIG — Fill in these fields
# ============================================================

STATUS_DATE = "7/3/26"              # M/D/YY format
STATUS_TITLE = f"{STATUS_DATE} Status Update"
PARENT_ID = '1424137842'

# Overall Status
STATUS_COLOR = "Yellow"             # Green, Yellow, Red
STATUS_TEXT = "AT RISK"             # ON TRACK, AT RISK, OFF TRACK

# Executive Summary (2-3 sentences)
EXEC_SUMMARY = "[2-3 sentence narrative about program status this week]"

# High Level Overview
HIGH_LEVEL_OVERVIEW = "[Overview narrative]"

# Major Wins (bullet list)
MAJOR_WINS = [
    "[Win 1]",
    "[Win 2]",
]

# Attention Required (bullet list)
ATTENTION_REQUIRED = [
    "[Concern 1]",
]

# Next Steps (bullet list)
NEXT_STEPS = [
    "[Priority 1]",
    "[Priority 2]",
]

# ============================================================
# END CONFIG — Code below builds the page
# ============================================================

JIRA_SERVER_ID = 'cc100dec-3d79-305b-8fae-4caba5e44cd2'

THREAT_MODELS = [
    ("Compromised Server", "CompromisedServer"),
    ("Insider Threat", "InsiderThreat"),
    ("Physical Tampering", "PhysicalTampering"),
    ("B2B SaaS Integration", "B2BSaaSIntegration"),
    ("Software Supply Chain", "SoftwareSupplyChain"),
    ("Unauthorized Access to Customer Data", "UnauthorizedAccessCustomerData"),
    ("Customer Zero", "CustomerZero"),
    ("AI Security", "AISecurity"),
]

def get_token():
    result = subprocess.run(['cloudflared', 'access', 'login', 'https://wiki.cfdata.org/'],
                            capture_output=True, text=True)
    for line in (result.stdout + result.stderr).split('\n'):
        m = re.search(r'eyJ[a-zA-Z0-9._-]+', line)
        if m:
            return m.group(0)
    raise RuntimeError("Could not get cloudflared token")

def jira_count(jql):
    return f'''<ac:structured-macro ac:name="jira" ac:schema-version="1" ac:macro-id="{uuid.uuid4()}">
  <ac:parameter ac:name="server">Cloudflare Jira</ac:parameter>
  <ac:parameter ac:name="serverId">{JIRA_SERVER_ID}</ac:parameter>
  <ac:parameter ac:name="jqlQuery">{jql}</ac:parameter>
  <ac:parameter ac:name="count">true</ac:parameter>
</ac:structured-macro>'''

def status_lozenge(color, title_text):
    return f'<ac:structured-macro ac:name="status" ac:schema-version="1" ac:macro-id="{uuid.uuid4()}"><ac:parameter ac:name="subtle">true</ac:parameter><ac:parameter ac:name="colour">{color}</ac:parameter><ac:parameter ac:name="title">{title_text}</ac:parameter></ac:structured-macro>'

def panel(title, bg_color, content):
    return f'''<ac:structured-macro ac:name="panel" ac:schema-version="1" ac:macro-id="{uuid.uuid4()}">
  <ac:parameter ac:name="title">{title}</ac:parameter>
  <ac:parameter ac:name="titleBGColor">{bg_color}</ac:parameter>
  <ac:parameter ac:name="titleColor">white</ac:parameter>
  <ac:rich-text-body>{content}</ac:rich-text-body>
</ac:structured-macro>'''

def build_status_update():
    parts = []

    # Overall Program Status panel
    parts.append(f'''<ac:structured-macro ac:name="panel" ac:schema-version="1" ac:macro-id="{uuid.uuid4()}">
  <ac:parameter ac:name="borderColor">#394ECE</ac:parameter>
  <ac:parameter ac:name="titleColor">white</ac:parameter>
  <ac:parameter ac:name="titleBGColor">#394ECE</ac:parameter>
  <ac:parameter ac:name="title">Overall Program Status</ac:parameter>
  <ac:rich-text-body>
    <table class="fixed-width wrapped"><tbody>
      <tr>
        <td class="highlight-grey"><p><time datetime="{STATUS_DATE}" /></p></td>
        <td><p><strong>{status_lozenge(STATUS_COLOR, STATUS_TEXT)}</strong></p></td>
      </tr>
    </tbody></table>
  </ac:rich-text-body>
</ac:structured-macro>''')

    # Two-column layout with right sidebar
    parts.append('<ac:layout><ac:layout-section ac:type="two_right_sidebar"><ac:layout-cell>')

    # Executive Summary
    parts.append(panel('Executive Summary', '#394ECE', f'<p>{EXEC_SUMMARY}</p>'))

    # Metrics table with live Jira counts
    parts.append('<table><tbody><tr>')
    parts.append(f'<td><h1>{jira_count("labels = ThreatFocusedControl")}</h1><p>Total Tickets</p></td>')
    parts.append(f'<td><h1>{jira_count("labels = ThreatFocusedControl and status not in (Done, Cancelled)")}</h1><p>Open</p></td>')
    parts.append(f'<td><h1>{jira_count("labels = ThreatFocusedControl and status in (Done, Closed, Cancelled)")}</h1><p>Completed</p></td>')
    parts.append('</tr></tbody></table>')

    # High Level Overview
    parts.append(panel('High Level Overview', '#1c5e98', f'<p>{HIGH_LEVEL_OVERVIEW}</p>'))

    # Major Wins
    wins_html = '<ul>' + ''.join(f'<li>{w}</li>' for w in MAJOR_WINS) + '</ul>'
    parts.append(panel('Major Wins This Week', '#36B37E', wins_html))

    # Attention Required
    concerns_html = '<ul>' + ''.join(f'<li>{c}</li>' for c in ATTENTION_REQUIRED) + '</ul>'
    parts.append(panel('ATTENTION REQUIRED', '#DE350B', concerns_html))

    # Next Steps
    steps_html = '<ul>' + ''.join(f'<li>{s}</li>' for s in NEXT_STEPS) + '</ul>'
    parts.append(panel('Looking Ahead', '#6554C0', steps_html))

    # Project Workstreams table
    parts.append('<h3>PROJECT WORKSTREAMS</h3>')
    parts.append('<table class="wrapped"><tbody>')
    parts.append('<tr><th>Threat Model</th><th>Done</th><th>Open</th><th>Total</th></tr>')
    for name, label in THREAT_MODELS:
        done_jql = f'labels = ThreatFocusedControl and labels in ({label}) and status in (Done, Cancelled)'
        open_jql = f'labels = ThreatFocusedControl and labels in ({label}) and status not in (Done, Cancelled)'
        total_jql = f'labels = ThreatFocusedControl and labels in ({label})'
        parts.append(f'<tr><td>{name}</td><td>{jira_count(done_jql)}</td><td>{jira_count(open_jql)}</td><td>{jira_count(total_jql)}</td></tr>')
    parts.append('</tbody></table>')

    # Close main column, start sidebar
    parts.append('</ac:layout-cell><ac:layout-cell>')

    # Sidebar: Quick Links
    parts.append('<p><strong>Quick Links</strong></p>')
    parts.append('<ul>')
    parts.append('<li><a href="https://wiki.cfdata.org/spaces/INFOSEC/pages/1276292540">Program Hub</a></li>')
    parts.append('<li><a href="https://wiki.cfdata.org/spaces/INFOSEC/pages/1419363218">PM Plan</a></li>')
    parts.append('<li><a href="https://wiki.cfdata.org/spaces/INFOSEC/pages/1346668352">Decision Log</a></li>')
    parts.append('</ul>')

    # Close layout
    parts.append('</ac:layout-cell></ac:layout-section></ac:layout>')

    return ''.join(parts)

def create_page(token, title, body, parent_id):
    payload = {
        'type': 'page',
        'title': title,
        'space': {'key': 'INFOSEC'},
        'ancestors': [{'id': parent_id}],
        'body': {'storage': {'value': body, 'representation': 'storage'}}
    }
    resp = requests.post('https://wiki.cfdata.org/rest/api/content', json=payload,
        headers={'cf-access-token': token, 'X-Atlassian-Token': 'no-check', 'Content-Type': 'application/json'},
        verify=False)
    print(f'Create status: {resp.status_code}')
    if resp.status_code == 200:
        rdata = resp.json()
        print(f'New page ID: {rdata["id"]}')
        print(f'Title: {rdata["title"]}')
        print(f'URL: https://wiki.cfdata.org/spaces/INFOSEC/pages/{rdata["id"]}')
        return rdata['id']
    else:
        print(f'Error: {resp.text[:500]}')
        return None

def update_index(token, status_page_id, status_title):
    """Add link to the index page (1424137842) in the Friday Status Send-Out column"""
    resp = requests.get('https://wiki.cfdata.org/rest/api/content/1424137842?expand=body.storage,version',
        headers={'cf-access-token': token, 'X-Atlassian-Token': 'no-check'}, verify=False)
    data = resp.json()
    body = data['body']['storage']['value']
    version = data['version']['number']

    # Add link to status column (second <td> in the data row)
    new_link = f'<p><a href="https://wiki.cfdata.org/spaces/INFOSEC/pages/{status_page_id}">{status_title}</a></p>'
    # Find the second <td> after the header row and insert
    first_td = body.find('<td>', body.find('</tr>'))
    second_td = body.find('<td>', first_td + 4) + 4
    body = body[:second_td] + new_link + body[second_td:]

    payload = {
        'id': '1424137842', 'type': 'page', 'title': data['title'],
        'body': {'storage': {'value': body, 'representation': 'storage'}},
        'version': {'number': version + 1}
    }
    resp2 = requests.put('https://wiki.cfdata.org/rest/api/content/1424137842', json=payload,
        headers={'cf-access-token': token, 'X-Atlassian-Token': 'no-check', 'Content-Type': 'application/json'},
        verify=False)
    print(f'Index update: {resp2.status_code}')

if __name__ == '__main__':
    token = get_token()
    body = build_status_update()
    page_id = create_page(token, STATUS_TITLE, body, PARENT_ID)
    if page_id:
        update_index(token, page_id, STATUS_TITLE)
        print('\nSUCCESS! Status update created and index updated.')
