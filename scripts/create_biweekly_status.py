"""
create_biweekly_status.py — Create a bi-weekly status page for the TFD program.

Bi-weekly status meetings are status updates for the team, not agenda-driven
discussion meetings. The page is intentionally concise — 4 panels, high-level,
scannable in under 30 seconds.

Usage:
    python3 create_biweekly_status.py

    # Then edit the generated script to fill in content, or use interactively:
    from create_biweekly_status import create_biweekly_status
    page_id = create_biweekly_status(
        date="7/10/26",
        status_color="Red",
        status_title="OFF TRACK",
        status_summary="Off-Track — improving. 18 tickets updated in last 7 days.",
        progress_bullets=[
            "18 tickets updated in last 7 days",
            "Program Hub live with auto-updating dashboards",
            "Jira adopted as single source of truth",
        ],
        focus_bullets=[
            "Confirm ticket owners and start outreach",
            "Resolve 4 unassigned tickets",
            "Confirm Wave 2 start date",
        ],
        risk_bullets=[
            "1 blocked ticket (Immutable Storage / R2 limitation)",
            "Outreach pending Sonia's confirmation on contact list",
        ],
    )
"""

import requests
import urllib3
import subprocess
import re
import uuid
import json

urllib3.disable_warnings()

BASE = 'https://wiki.cfdata.org/rest/api/content'
PARENT_ID = '1424137842'
JIRA_SERVER_ID = 'cc100dec-3d79-305b-8fae-4caba5e44cd2'


def get_token():
    result = subprocess.run(
        ['cloudflared', 'access', 'login', 'https://wiki.cfdata.org/'],
        capture_output=True, text=True
    )
    for line in (result.stdout + result.stderr).split('\n'):
        m = re.search(r'eyJ[a-zA-Z0-9._-]+', line)
        if m:
            return m.group(0)
    raise RuntimeError("Could not get cloudflared token")


def panel(title, title_bg, border_color, bg_color, content):
    return (
        f'<ac:structured-macro ac:name="panel" ac:schema-version="1" ac:macro-id="{uuid.uuid4()}">'
        f'<ac:parameter ac:name="title">{title}</ac:parameter>'
        f'<ac:parameter ac:name="titleBGColor">{title_bg}</ac:parameter>'
        f'<ac:parameter ac:name="titleColor">#FFFFFF</ac:parameter>'
        f'<ac:parameter ac:name="borderColor">{border_color}</ac:parameter>'
        f'<ac:parameter ac:name="bgColor">{bg_color}</ac:parameter>'
        f'<ac:rich-text-body>{content}</ac:rich-text-body>'
        f'</ac:structured-macro>'
    )


def lozenge(color, title_text):
    return (
        f'<ac:structured-macro ac:name="status" ac:schema-version="1" ac:macro-id="{uuid.uuid4()}">'
        f'<ac:parameter ac:name="subtle">true</ac:parameter>'
        f'<ac:parameter ac:name="colour">{color}</ac:parameter>'
        f'<ac:parameter ac:name="title">{title_text}</ac:parameter>'
        f'</ac:structured-macro>'
    )


def bullets(items):
    lis = ''.join(f'<li>{item}</li>' for item in items)
    return f'<ul>{lis}</ul>'


def create_biweekly_status(
    date,
    status_color="Red",
    status_title="OFF TRACK",
    status_summary="Off-Track — improving.",
    progress_bullets=None,
    focus_bullets=None,
    risk_bullets=None,
):
    """
    Create a bi-weekly status page and return the new page ID.

    Args:
        date: Date string for title (e.g., "7/10/26")
        status_color: Lozenge color (Red, Yellow, Green)
        status_title: Lozenge title text (e.g., "OFF TRACK")
        status_summary: 1-2 sentence summary after lozenge
        progress_bullets: List of strings for Progress panel
        focus_bullets: List of strings for Focus panel
        risk_bullets: List of strings for Risks panel

    Returns:
        New page ID (string)
    """
    if progress_bullets is None:
        progress_bullets = ["[Add progress items]"]
    if focus_bullets is None:
        focus_bullets = ["[Add focus items]"]
    if risk_bullets is None:
        risk_bullets = ["[Add risks]"]

    token = get_token()
    headers = {
        'cf-access-token': token,
        'X-Atlassian-Token': 'no-check',
        'Content-Type': 'application/json',
    }

    title = f"{date} Bi-Weekly Status"

    # Build 4 panels
    parts = []

    # Panel 1: Program Status (red)
    status_content = f'<p>{lozenge(status_color, status_title)} &nbsp; {status_summary}</p>'
    parts.append(panel("Program Status", "#DE350B", "#DE350B", "#ffe6e6", status_content))
    parts.append('<p><br /></p>')

    # Panel 2: Progress Since Last Meeting (green)
    parts.append(panel("Progress Since Last Meeting", "#36B37E", "#36B37E", "#e6f7ef", bullets(progress_bullets)))
    parts.append('<p><br /></p>')

    # Panel 3: Focus for Next 2 Weeks (blue)
    parts.append(panel("Focus for Next 2 Weeks", "#0052cc", "#0052cc", "#f0f4ff", bullets(focus_bullets)))
    parts.append('<p><br /></p>')

    # Panel 4: Key Risks (orange)
    parts.append(panel("Key Risks", "#FF8B00", "#FF8B00", "#fff4e6", bullets(risk_bullets)))

    body = ''.join(parts)

    payload = {
        'type': 'page',
        'title': title,
        'space': {'key': 'INFOSEC'},
        'ancestors': [{'id': PARENT_ID}],
        'body': {'storage': {'value': body, 'representation': 'storage'}}
    }

    resp = requests.post(BASE, json=payload, headers=headers, verify=False)
    resp.raise_for_status()
    new_page = resp.json()
    page_id = new_page['id']

    print(f"Created: {title}")
    print(f"Page ID: {page_id}")
    print(f"URL: https://wiki.cfdata.org/spaces/INFOSEC/pages/{page_id}")

    # Update index page
    _update_index(headers, title, page_id)

    return page_id


def _update_index(headers, page_title, page_id):
    """Add the new bi-weekly status link to the index page's Bi-Weekly Status column."""
    resp = requests.get(
        f'{BASE}/{PARENT_ID}?expand=body.storage,version',
        headers=headers, verify=False
    )
    resp.raise_for_status()
    data = resp.json()
    body = data['body']['storage']['value']
    version = data['version']['number']

    # Parse the table to find the last row and add a link in the Bi-Weekly Status column
    # Simple approach: find the last </tr> before </tbody> and insert a new row
    new_link = f'<ac:link><ri:page ri:content-title="{page_title}" /></ac:link>'
    new_row = f'<tr><td><br /></td><td><br /></td><td>{new_link}</td></tr>'

    # Insert before </tbody>
    new_body = body.replace('</tbody>', f'{new_row}</tbody>')

    if new_body == body:
        # Fallback: append before </table>
        new_body = body.replace('</table>', f'{new_row}</tbody></table>')

    payload = {
        'id': PARENT_ID,
        'type': 'page',
        'title': data['title'],
        'body': {'storage': {'value': new_body, 'representation': 'storage'}},
        'version': {'number': version + 1}
    }

    resp = requests.put(
        f'{BASE}/{PARENT_ID}', json=payload, headers=headers,
        verify=False, params={'expand': 'version'}
    )
    resp.raise_for_status()
    print(f"Index page updated: v{resp.json()['version']['number']}")


if __name__ == '__main__':
    # Example usage — edit these values for each bi-weekly status
    page_id = create_biweekly_status(
        date="7/10/26",
        status_color="Red",
        status_title="OFF TRACK",
        status_summary="Off-Track — improving. [Update with current state.]",
        progress_bullets=[
            "[Add progress items from latest Friday send-out]",
        ],
        focus_bullets=[
            "[Add focus areas for next 2 weeks]",
        ],
        risk_bullets=[
            "[Add key risks]",
        ],
    )
