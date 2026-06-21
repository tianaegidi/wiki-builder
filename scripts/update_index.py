#!/usr/bin/env python3
"""
TFD Index Page Updater
======================
Updates the TFD Status Updates 2026 index page (1424137842) with new child page links.

Usage:
  python3 update_index.py

Can add a link to either the Weekly Meeting Agendas column or the Friday Status Send-Outs column.
"""
import json, requests, urllib3, subprocess, re
urllib3.disable_warnings()

INDEX_PAGE_ID = '1424137842'

# ============================================================
# CONFIG — Set these fields
# ============================================================

# What type of page are we adding?
PAGE_TYPE = "agenda"  # "agenda" or "status"

# Page details
NEW_PAGE_ID = "PAGE_ID_HERE"       # ID of the new child page
NEW_PAGE_TITLE = "M/D/YY Title"    # Title of the new child page

# ============================================================
# END CONFIG
# ============================================================

def get_token():
    result = subprocess.run(['cloudflared', 'access', 'login', 'https://wiki.cfdata.org/'],
                            capture_output=True, text=True)
    for line in (result.stdout + result.stderr).split('\n'):
        m = re.search(r'eyJ[a-zA-Z0-9._-]+', line)
        if m:
            return m.group(0)
    raise RuntimeError("Could not get cloudflared token")

def update_index(token, page_id, page_title, page_type):
    """Add link to the index page in the appropriate column"""
    resp = requests.get(f'https://wiki.cfdata.org/rest/api/content/{INDEX_PAGE_ID}?expand=body.storage,version',
        headers={'cf-access-token': token, 'X-Atlassian-Token': 'no-check'}, verify=False)
    data = resp.json()
    body = data['body']['storage']['value']
    version = data['version']['number']
    title = data['title']

    new_link = f'<p><a href="https://wiki.cfdata.org/spaces/INFOSEC/pages/{page_id}">{page_title}</a></p>'

    # Find the data row (after the header row)
    header_end = body.find('</tr>')
    if header_end == -1:
        print("ERROR: Could not find header row")
        return

    if page_type == "agenda":
        # First <td> in the data row = Weekly Meeting Agendas column
        td_start = body.find('<td>', header_end) + 4
    else:
        # Second <td> in the data row = Friday Status Send-Outs column
        first_td = body.find('<td>', header_end)
        td_start = body.find('<td>', first_td + 4) + 4

    body = body[:td_start] + new_link + body[td_start:]

    payload = {
        'id': INDEX_PAGE_ID,
        'type': 'page',
        'title': title,
        'body': {'storage': {'value': body, 'representation': 'storage'}},
        'version': {'number': version + 1}
    }

    resp2 = requests.put(f'https://wiki.cfdata.org/rest/api/content/{INDEX_PAGE_ID}', json=payload,
        headers={'cf-access-token': token, 'X-Atlassian-Token': 'no-check', 'Content-Type': 'application/json'},
        verify=False)

    print(f'Index update: {resp2.status_code}')
    if resp2.status_code == 200:
        print(f'New version: {resp2.json()["version"]["number"]} - SUCCESS')
    else:
        print(f'Error: {resp2.text[:500]}')

if __name__ == '__main__':
    token = get_token()
    update_index(token, NEW_PAGE_ID, NEW_PAGE_TITLE, PAGE_TYPE)
