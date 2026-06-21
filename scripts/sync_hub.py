#!/usr/bin/env python3
"""
TFD Hub Page Sync
=================
Updates the Program Hub page (1276292540) with latest status info.

Usage:
  python3 sync_hub.py

Updates:
- Latest Status panel (status summary, date, button URL)
- Quick Links table (latest status/agenda links)
"""
import json, requests, urllib3, subprocess, re
urllib3.disable_warnings()

HUB_PAGE_ID = '1276292540'

# ============================================================
# CONFIG — Set these fields
# ============================================================

# Latest status update info
LATEST_STATUS_URL = "https://wiki.cfdata.org/spaces/INFOSEC/pages/PAGE_ID"
LATEST_STATUS_DATE = "Jun 26, 2026"
LATEST_STATUS_SUMMARY = "Program is at risk but improving. 11 tickets completed this week."

# Latest agenda info
LATEST_AGENDA_URL = "https://wiki.cfdata.org/spaces/INFOSEC/pages/PAGE_ID"
LATEST_AGENDA_DATE = "Jun 26, 2026"

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

def sync_hub(token):
    """Fetch hub page, update status info, PUT back"""
    resp = requests.get(f'https://wiki.cfdata.org/rest/api/content/{HUB_PAGE_ID}?expand=body.storage,version',
                        headers={'cf-access-token': token, 'X-Atlassian-Token': 'no-check'}, verify=False)
    data = resp.json()
    body = data['body']['storage']['value']
    version = data['version']['number']
    title = data['title']

    print(f'Hub page: {title} v{version}')
    print(f'Body length: {len(body)}')

    # --- Update Latest Status Panel ---
    # Update "Last updated" date (look for pattern like "Last updated:</strong> DATE")
    # You'll need to find the actual old date in the body and replace it
    # Example:
    # body = body.replace('Last updated:</strong> Jun 19, 2026', f'Last updated:</strong> {LATEST_STATUS_DATE}')

    # Update status summary
    # body = body.replace(old_summary, LATEST_STATUS_SUMMARY)

    # Update button URL
    # body = body.replace('ac:name="url">OLD_URL', f'ac:name="url">{LATEST_STATUS_URL}')

    # --- Update Quick Links Table ---
    # Find the Quick Links table and update the relevant rows
    # Example:
    # old_status_row = '<tr><td>Latest Status Update</td><td><a href="OLD_URL">OLD_DATE</a></td><td>OLD_DATE</td></tr>'
    # new_status_row = f'<tr><td>Latest Status Update</td><td><a href="{LATEST_STATUS_URL}">{LATEST_STATUS_DATE}</a></td><td>{LATEST_STATUS_DATE}</td></tr>'
    # body = body.replace(old_status_row, new_status_row)

    # NOTE: The exact strings to replace depend on the current page content.
    # Print the body to find the exact strings:
    # print(body[:5000])  # Uncomment to see the beginning of the page

    print('\nNOTE: This script is a template. You need to:')
    print('1. Uncomment the replace operations above')
    print('2. Set the correct old strings to replace')
    print('3. Or print the body to find the exact strings')
    return

    # --- PUT Update (uncomment when ready) ---
    payload = {
        'id': HUB_PAGE_ID,
        'type': 'page',
        'title': title,
        'body': {'storage': {'value': body, 'representation': 'storage'}},
        'version': {'number': version + 1}
    }

    resp2 = requests.put(f'https://wiki.cfdata.org/rest/api/content/{HUB_PAGE_ID}', json=payload,
                         headers={'cf-access-token': token, 'X-Atlassian-Token': 'no-check',
                                  'Content-Type': 'application/json'},
                         verify=False)

    print(f'\nUpdate status: {resp2.status_code}')
    if resp2.status_code == 200:
        print(f'New version: {resp2.json()["version"]["number"]} - SUCCESS')
    else:
        print(f'Error: {resp2.text[:500]}')

if __name__ == '__main__':
    token = get_token()
    sync_hub(token)
