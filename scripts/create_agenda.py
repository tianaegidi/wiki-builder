#!/usr/bin/env python3
"""
TFD Weekly Agenda Creator
=========================
Creates a new weekly agenda page under TFD Status Updates 2026 (1424137842).

Usage:
  python3 create_agenda.py

Fill in the AGENDA_CONFIG section below before running.
"""
import json, requests, urllib3, subprocess, re, uuid
urllib3.disable_warnings()

# ============================================================
# AGENDA CONFIG — Fill in these fields
# ============================================================

AGENDA_DATE = "7/3/26"           # M/D/YY format
AGENDA_TITLE = f"{AGENDA_DATE} TFD Weekly Agenda"
PARENT_ID = '1424137842'

# Project Status
OVERALL_STATUS_COLOR = "Yellow"   # Green, Yellow, Red
OVERALL_STATUS_TEXT = "AT RISK"   # ON TRACK, AT RISK, OFF TRACK
STATUS_NARRATIVE = "Improving — [describe current state]"
ON_TRACK_ASSESSMENT = "At Risk — [describe why]"
KEY_WINS = [
    "[Win 1]",
    "[Win 2]",
]
BLOCKERS = [
    "[Blocker 1]",
    "[Blocker 2]",
]
DOD_STATEMENT = "Right owners assigned and start dates to each ticket"
PATH_TO_GREEN = "[Describe path to green]"

# Progress Updates (one tuple per row: Update, Owner, Progress, Follow-up)
PROGRESS_UPDATES = [
    ("[Update title]", "[Owner]", "[Progress made]", "[Follow-up]"),
]

# Status by Workstream (one tuple per row: Name, Subtitle, Status color, Status text, What changed, Next milestone, Owner)
WORKSTREAMS = [
    ("Wave 1", "Top 5 threat scenarios", "Yellow", "IN PROGRESS", "[What changed]", "[Next milestone]", "[Owner]"),
    ("Wave 2", "3 new threat scenarios", "Blue", "DISCOVERY", "[What changed]", "[Next milestone]", "[Owner]"),
    ("Wave 3", "Next Q", "Grey", "BACKLOG", "Not started", "Next quarter", "TBD"),
]

# Discussion Items (one dict per item: title, question, context, decision, owner, timebox)
DISCUSSION_ITEMS = [
    {
        "title": "Item 1: [Title]",
        "question": "[Question]",
        "context": "[Context]",
        "decision": "[Decision needed]",
        "owner": "[Owner]",
        "timebox": "10 min",
    },
]

# Notes (bullet list)
NOTES = [
    "[Note 1]",
    "[Note 2]",
]

# Next Steps (one tuple per row: Action, Owner, Due, Status color, Status text)
NEXT_STEPS = [
    ("[Action item]", "[Owner]", "[Due date]", "Yellow", "IN PROGRESS"),
]

# Parking Lot (bullet list)
PARKING_LOT = [
    "[Topic 1]",
]

# ============================================================
# END CONFIG — Code below builds the page
# ============================================================

def get_token():
    result = subprocess.run(['cloudflared', 'access', 'login', 'https://wiki.cfdata.org/'],
                            capture_output=True, text=True)
    for line in (result.stdout + result.stderr).split('\n'):
        m = re.search(r'eyJ[a-zA-Z0-9._-]+', line)
        if m:
            return m.group(0)
    raise RuntimeError("Could not get cloudflared token")

def colored_header(text, color):
    return f'<table class="wrapped" style="width: 100%;"><tbody><tr><td style="background-color: {color}; color: #FFFFFF;"><strong>{text}</strong></td></tr></tbody></table>'

def th(color, text):
    return f'<th style="background-color: {color}; color: #FFFFFF;"><strong>{text}</strong></th>'

def status_lozenge(color, title_text):
    return f'<ac:structured-macro ac:name="status" ac:schema-version="1" ac:macro-id="{uuid.uuid4()}"><ac:parameter ac:name="subtle">true</ac:parameter><ac:parameter ac:name="colour">{color}</ac:parameter><ac:parameter ac:name="title">{title_text}</ac:parameter></ac:structured-macro>'

def build_agenda():
    parts = []

    # 1) PROJECT STATUS
    parts.append(colored_header('1) Project Status', '#0052cc'))
    parts.append('<p>Current state of the project.</p>')
    parts.append('<table class="wrapped"><tbody>')
    parts.append(f'<tr><th style="width: 35%;">Overall status</th><td>{status_lozenge(OVERALL_STATUS_COLOR, OVERALL_STATUS_TEXT)} {STATUS_NARRATIVE}</td></tr>')
    parts.append(f'<tr><th>On track / at risk / blocked</th><td>{ON_TRACK_ASSESSMENT}</td></tr>')
    wins_html = '<ul>' + ''.join(f'<li>{w}</li>' for w in KEY_WINS) + '</ul>'
    parts.append(f'<tr><th>Key wins since last meeting</th><td>{wins_html}</td></tr>')
    blockers_html = '<ul>' + ''.join(f'<li>{b}</li>' for b in BLOCKERS) + '</ul>'
    parts.append(f'<tr><th>Main blockers or decisions needed</th><td>{blockers_html}</td></tr>')
    parts.append(f'<tr><th>Definition of Done</th><td>{DOD_STATEMENT}</td></tr>')
    parts.append(f'<tr><th>Path to green</th><td>{PATH_TO_GREEN}</td></tr>')
    parts.append('</tbody></table>')
    parts.append('<p><br /></p>')

    # Project Artifacts
    parts.append(colored_header('Project Artifacts', '#36B37E'))
    parts.append('<ul>')
    parts.append('<li><a href="https://wiki.cfdata.org/spaces/INFOSEC/pages/1419363218">TFD Project Management Wiki</a></li>')
    parts.append('<li><a href="https://wiki.cfdata.org/spaces/INFOSEC/pages/1276292540">TFD Program Hub Wiki</a></li>')
    parts.append('<li><a href="https://wiki.cfdata.org/spaces/INFOSEC/pages/1346668352">TFD Decision Log</a></li>')
    parts.append('</ul>')
    parts.append('<p><br /></p>')

    # 2) PROGRESS UPDATES
    parts.append(colored_header('2) Progress Updates', '#6554C0'))
    parts.append('<p><em>What has happened since the last meeting.</em></p>')
    parts.append('<table class="wrapped"><tbody>')
    parts.append(f'<tr>{th("#6554C0", "Update")}{th("#6554C0", "Owner")}{th("#6554C0", "Progress made")}{th("#6554C0", "Follow-up")}</tr>')
    for update, owner, progress, followup in PROGRESS_UPDATES:
        parts.append(f'<tr><td>{update}</td><td>{owner}</td><td>{progress}</td><td>{followup}</td></tr>')
    parts.append('</tbody></table>')
    parts.append('<p><br /></p>')

    # 3) STATUS BY WORKSTREAM
    parts.append(colored_header('3) Status by Workstream', '#FF8B00'))
    parts.append('<p><em>Review each workstream one at a time.</em></p>')
    parts.append('<table class="wrapped"><tbody>')
    parts.append(f'<tr>{th("#FF8B00", "Workstream")}{th("#FF8B00", "Status")}{th("#FF8B00", "What changed")}{th("#FF8B00", "Next milestone")}{th("#FF8B00", "Owner")}</tr>')
    for name, subtitle, scolor, stext, changed, milestone, owner in WORKSTREAMS:
        parts.append(f'<tr><td><strong>{name}</strong><br /><span style="color: #6b7280;font-size: 12px;">{subtitle}</span></td><td>{status_lozenge(scolor, stext)}</td><td>{changed}</td><td>{milestone}</td><td>{owner}</td></tr>')
    parts.append('</tbody></table>')
    parts.append('<p><br /></p>')
    parts.append('<p><strong>Reference:</strong> <a href="https://wiki.cfdata.org/spaces/INFOSEC/pages/1276292540/Threat-focused+Defense#ThreatfocusedDefense-OpenTicketsbyView">Open Tickets by View</a></p>')
    parts.append('<p><br /></p>')

    # 4) DISCUSSION ITEMS
    parts.append(colored_header('4) Discussion Items', '#DE350B'))
    parts.append('<p><em>Use this section for the questions we need to solve.</em></p>')
    for item in DISCUSSION_ITEMS:
        parts.append(f'<h3>{item["title"]}</h3>')
        parts.append('<ul>')
        parts.append(f'<li><strong>Question:</strong> {item["question"]}</li>')
        parts.append(f'<li><strong>Context:</strong> {item["context"]}</li>')
        parts.append(f'<li><strong>Decision needed:</strong> {item["decision"]}</li>')
        parts.append(f'<li><strong>Owner:</strong> {item["owner"]}</li>')
        parts.append(f'<li><strong>Timebox:</strong> {item["timebox"]}</li>')
        parts.append('</ul>')
    parts.append('<p><br /></p>')

    # 5) NOTES
    parts.append(colored_header('5) Notes', '#6B778C'))
    parts.append('<p><em>Helpful context and parked tangents.</em></p>')
    parts.append('<ul>')
    for note in NOTES:
        parts.append(f'<li>{note}</li>')
    parts.append('</ul>')
    parts.append('<p><br /></p>')

    # 6) NEXT STEPS
    parts.append(colored_header('6) Next Steps', '#36B37E'))
    parts.append('<p><em>Action items before we close.</em></p>')
    parts.append('<table class="wrapped"><tbody>')
    parts.append(f'<tr>{th("#36B37E", "Action item")}{th("#36B37E", "Owner")}{th("#36B37E", "Due date")}{th("#36B37E", "Status")}</tr>')
    for action, owner, due, scolor, stext in NEXT_STEPS:
        parts.append(f'<tr><td>{action}</td><td>{owner}</td><td>{due}</td><td>{status_lozenge(scolor, stext)}</td></tr>')
    parts.append('</tbody></table>')
    parts.append('<p><br /></p>')

    # PARKING LOT
    parts.append(colored_header('Parking Lot', '#97a0af'))
    parts.append('<p><em>Topics to revisit later.</em></p>')
    parts.append('<ul>')
    for topic in PARKING_LOT:
        parts.append(f'<li>{topic}</li>')
    parts.append('</ul>')

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

def update_index(token, agenda_page_id, agenda_title):
    """Add link to the index page (1424137842)"""
    resp = requests.get('https://wiki.cfdata.org/rest/api/content/1424137842?expand=body.storage,version',
        headers={'cf-access-token': token, 'X-Atlassian-Token': 'no-check'}, verify=False)
    data = resp.json()
    body = data['body']['storage']['value']
    version = data['version']['number']

    # Add link to agendas column (first <td> in the data row)
    new_link = f'<p><a href="https://wiki.cfdata.org/spaces/INFOSEC/pages/{agenda_page_id}">{agenda_title}</a></p>'
    # Find the first <td> after the header row and insert
    td_start = body.find('<td>', body.find('</tr>')) + 4
    body = body[:td_start] + new_link + body[td_start:]

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
    body = build_agenda()
    page_id = create_page(token, AGENDA_TITLE, body, PARENT_ID)
    if page_id:
        update_index(token, page_id, AGENDA_TITLE)
        print('\nSUCCESS! Agenda created and index updated.')
