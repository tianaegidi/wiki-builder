"""
ConfluencePage — Targeted in-place editor for Confluence wiki pages.

Usage:
    from confluence_edit import ConfluencePage

    page = ConfluencePage('1424156221')
    page.update_cell(row_header="Overall status", new_content="GREEN")
    page.add_table_row(after_header="Action item", cells=["New item", "Owner", "Jul 1"])
    page.replace_text("old text", "new text")
    page.update_lozenge(old_title="AT RISK", new_color="Green", new_title="ON TRACK")
    page.add_bullet("New bullet item")
    page.save()

Requires: requests, urllib3 (pip3 install requests urllib3)
Requires: cloudflared token for wiki.cfdata.org
"""

import requests
import urllib3
import subprocess
import re
import uuid
import xml.etree.ElementTree as ET

urllib3.disable_warnings()

# Confluence storage format namespaces
NS = {
    'ac': 'http://atlassian.com/ac',
    'ri': 'http://atlassian.com/ri',
}

# Register prefixes so ET.tostring() produces ac: and ri: (not ns0:)
for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)

# Namespace-qualified tag helpers (for find() calls)
AC = '{http://atlassian.com/ac}'
RI = '{http://atlassian.com/ri}'


def _get_token():
    """Get cloudflared access token for wiki.cfdata.org."""
    result = subprocess.run(
        ['cloudflared', 'access', 'login', 'https://wiki.cfdata.org/'],
        capture_output=True, text=True
    )
    for line in (result.stdout + result.stderr).split('\n'):
        m = re.search(r'eyJ[a-zA-Z0-9._-]+', line)
        if m:
            return m.group(0)
    raise RuntimeError("Could not get cloudflared token. Run: cloudflared access login https://wiki.cfdata.org/")


def _status_lozenge(color, title):
    """Generate a status lozenge macro string."""
    return (
        f'<ac:structured-macro ac:name="status" ac:schema-version="1" ac:macro-id="{uuid.uuid4()}">'
        f'<ac:parameter ac:name="subtle">true</ac:parameter>'
        f'<ac:parameter ac:name="colour">{color}</ac:parameter>'
        f'<ac:parameter ac:name="title">{title}</ac:parameter>'
        f'</ac:structured-macro>'
    )


def _iter_all(root, tag):
    """Iterate over elements by tag name, trying both plain and namespaced versions."""
    # Try plain tag first (for HTML elements like th, td, tr, table, ul, li)
    for elem in root.iter(tag):
        yield elem
    # Try AC-namespaced tag (for ac:structured-macro, ac:parameter, etc.)
    ac_tag = f'{AC}{tag}'
    for elem in root.iter(ac_tag):
        yield elem


def _find_all(root, tag):
    """findall that checks both plain and AC-namespaced tags."""
    results = list(root.iter(tag))
    ac_tag = f'{AC}{tag}'
    results.extend(root.iter(ac_tag))
    return results


def _get_attr(elem, name):
    """Get attribute, trying both plain and AC-namespaced versions."""
    val = elem.get(name)
    if val is not None:
        return val
    return elem.get(f'{AC}{name}')


class ConfluencePage:
    """Represents a Confluence page for targeted in-place editing."""

    BASE = 'https://wiki.cfdata.org/rest/api/content'

    def __init__(self, page_id, token=None):
        self.page_id = str(page_id)
        self.token = token or _get_token()
        self.headers = {
            'cf-access-token': self.token,
            'X-Atlassian-Token': 'no-check',
            'Content-Type': 'application/json',
        }
        self._fetch()

    def _fetch(self):
        """Fetch current page body and version."""
        resp = requests.get(
            f'{self.BASE}/{self.page_id}?expand=body.storage,version',
            headers=self.headers,
            verify=False
        )
        resp.raise_for_status()
        data = resp.json()
        self.title = data['title']
        self.version = data['version']['number']
        self.body = data['body']['storage']['value']
        self._original_body = self.body
        self._dirty = False

    # ── Text-based edits (simple, no XML parsing) ──────────────────

    def replace_text(self, old, new, count=None):
        """
        Replace text in the body.
        count=None (default) replaces all occurrences.
        count=1 replaces only the first occurrence.
        """
        if old not in self.body:
            raise ValueError(f"Text not found: {old[:80]}...")
        if count is None:
            self.body = self.body.replace(old, new)
        else:
            self.body = self.body.replace(old, new, count)
        self._dirty = True
        return self

    def replace_section(self, start_marker, end_marker, new_content):
        """Replace everything between start_marker and end_marker (inclusive of markers)."""
        start_idx = self.body.find(start_marker)
        if start_idx == -1:
            raise ValueError(f"Start marker not found: {start_marker[:80]}...")
        end_idx = self.body.find(end_marker, start_idx)
        if end_idx == -1:
            raise ValueError(f"End marker not found after start: {end_marker[:80]}...")
        end_idx += len(end_marker)
        self.body = self.body[:start_idx] + new_content + self.body[end_idx:]
        self._dirty = True
        return self

    # ── XML-based edits (structural, preserves everything else) ────

    def _parse(self):
        """Parse body as XML tree. Returns root element with namespace-aware tags."""
        wrapped = f'<__root__ xmlns:ac="{NS["ac"]}" xmlns:ri="{NS["ri"]}">{self.body}</__root__>'
        return ET.fromstring(wrapped)

    def _serialize(self, root):
        """Serialize root back to body string (strip wrapper, keep ac:/ri: prefixes)."""
        text = ET.tostring(root, encoding='unicode')
        # Remove the wrapper <__root__> tags
        text = re.sub(r'^<__root__[^>]*>', '', text)
        text = re.sub(r'</__root__>$', '', text)
        return text

    def _parse_fragment(self, html_str):
        """Parse an HTML/XML fragment with ac: and ri: namespaces declared."""
        wrapped = f'<frag xmlns:ac="{NS["ac"]}" xmlns:ri="{NS["ri"]}">{html_str}</frag>'
        return ET.fromstring(wrapped)

    def _get_text(self, elem):
        """Get all text content from an element (including children)."""
        return ''.join(elem.itertext()).strip()

    def update_cell(self, row_header, new_content):
        """
        Update a table cell by matching the row's header (th) text.
        Finds the <th> containing row_header, then updates the next <td> in the same <tr>.
        """
        root = self._parse()
        found = False
        for tr in root.iter('tr'):
            ths = tr.findall('th')
            tds = tr.findall('td')
            for th in ths:
                th_text = self._get_text(th)
                if row_header.lower() in th_text.lower():
                    if tds:
                        # Clear existing content and set new
                        for child in list(tds[0]):
                            tds[0].remove(child)
                        tds[0].text = None
                        # Parse new_content as XML fragment
                        fragment = self._parse_fragment(new_content)
                        if fragment.text:
                            tds[0].text = fragment.text
                        for child in fragment:
                            tds[0].append(child)
                        found = True
                        break
            if found:
                break
        if not found:
            raise ValueError(f"Row header not found: {row_header}")
        self.body = self._serialize(root)
        self._dirty = True
        return self

    def add_table_row(self, after_header, cells):
        """
        Add a new row to the table that contains a header cell matching after_header.
        cells is a list of strings (HTML or plain text) for each <td>.
        The row is appended to the table's tbody.
        """
        root = self._parse()
        found = False
        for table in root.iter('table'):
            for tr in table.iter('tr'):
                for th in tr.findall('th'):
                    th_text = self._get_text(th)
                    if after_header.lower() in th_text.lower():
                        # Find the tbody (create if missing)
                        tbody = table.find('tbody')
                        if tbody is None:
                            tbody = table
                        # Create new row
                        new_tr = ET.SubElement(tbody, 'tr')
                        for cell in cells:
                            new_td = ET.SubElement(new_tr, 'td')
                            # Parse cell content as XML fragment
                            fragment = self._parse_fragment(cell)
                            if fragment.text:
                                new_td.text = fragment.text
                            for child in fragment:
                                new_td.append(child)
                        found = True
                        break
                if found:
                    break
            if found:
                break
        if not found:
            raise ValueError(f"Table with header not found: {after_header}")
        self.body = self._serialize(root)
        self._dirty = True
        return self

    def update_lozenge(self, old_title, new_color=None, new_title=None):
        """
        Update a status lozenge macro by matching its current title.
        Only updates color and/or title if provided.
        """
        root = self._parse()
        found = False
        for macro in root.iter(f'{AC}structured-macro'):
            name = macro.get(f'{AC}name', '')
            if name != 'status':
                continue
            for param in macro.findall(f'{AC}parameter'):
                param_name = param.get(f'{AC}name', '')
                if param_name == 'title' and param.text and old_title.lower() in param.text.lower():
                    if new_title:
                        param.text = new_title
                    found = True
            if new_color and found:
                for param in macro.findall(f'{AC}parameter'):
                    if param.get(f'{AC}name', '') == 'colour':
                        param.text = new_color
            if found:
                break
        if not found:
            raise ValueError(f"Lozenge with title not found: {old_title}")
        self.body = self._serialize(root)
        self._dirty = True
        return self

    def add_bullet_after(self, match_text, new_item):
        """
        Add a new <li> after an existing <li> that contains match_text.
        """
        root = self._parse()
        found = False
        for ul in root.iter('ul'):
            children = list(ul)
            for i, li in enumerate(children):
                li_text = self._get_text(li)
                if match_text.lower() in li_text.lower():
                    # Create new li
                    new_li = ET.Element('li')
                    fragment = self._parse_fragment(new_item)
                    if fragment.text:
                        new_li.text = fragment.text
                    for child in fragment:
                        new_li.append(child)
                    ul.insert(i + 1, new_li)
                    found = True
                    break
            if found:
                break
        if not found:
            raise ValueError(f"Bullet not found: {match_text}")
        self.body = self._serialize(root)
        self._dirty = True
        return self

    def add_bullet(self, new_item, list_index=0):
        """
        Append a new <li> to the Nth <ul> in the page (default: first).
        """
        root = self._parse()
        uls = list(root.iter('ul'))
        if list_index >= len(uls):
            raise ValueError(f"No <ul> at index {list_index} (found {len(uls)} lists)")
        new_li = ET.SubElement(uls[list_index], 'li')
        fragment = self._parse_fragment(new_item)
        if fragment.text:
            new_li.text = fragment.text
        for child in fragment:
            new_li.append(child)
        self.body = self._serialize(root)
        self._dirty = True
        return self

    def get_section_text(self, header_text):
        """
        Extract plain text content of a section identified by its colored header.
        Returns all text between this header and the next colored header (or end of page).
        """
        root = self._parse()
        sections = []
        current_section = None
        current_text = []

        for elem in root.iter():
            # Check if this is a colored header cell (td with background-color)
            if elem.tag == 'td':
                style = elem.get('style', '')
                if 'background-color' in style:
                    elem_text = self._get_text(elem)
                    if elem_text:
                        if current_section and current_text:
                            sections.append((current_section, ' '.join(current_text)))
                        current_section = elem_text
                        current_text = []
                        continue
            if current_section:
                elem_text = self._get_text(elem)
                if elem_text and elem_text != current_section:
                    current_text.append(elem_text)

        if current_section and current_text:
            sections.append((current_section, ' '.join(current_text)))

        for section_name, text in sections:
            if header_text.lower() in section_name.lower():
                return text
        return None

    def list_tables(self):
        """
        Print a summary of all tables in the page for debugging.
        Shows table index, first row headers, and row count.
        """
        root = self._parse()
        for i, table in enumerate(root.iter('table')):
            rows = list(table.iter('tr'))
            headers = []
            if rows:
                for th in rows[0].findall('th'):
                    headers.append(self._get_text(th))
            first_row_text = self._get_text(rows[0])[:80] if rows else ''
            print(f"Table {i}: {len(rows)} rows | Headers: {headers} | First row: {first_row_text}")

    # ── Save ───────────────────────────────────────────────────────

    def save(self, comment=None):
        """Push changes to Confluence. Re-fetches version first to avoid conflicts."""
        if not self._dirty:
            print("No changes to save.")
            return self

        # Re-fetch version to avoid stale version conflicts
        resp = requests.get(
            f'{self.BASE}/{self.page_id}?expand=version',
            headers=self.headers,
            verify=False
        )
        resp.raise_for_status()
        latest_version = resp.json()['version']['number']

        if latest_version != self.version:
            print(f"WARNING: Page was edited by someone else (v{self.version} -> v{latest_version}). "
                  f"Re-fetching and retrying...")
            self._fetch()
            raise RuntimeError(
                f"Page version changed from {self.version} to {latest_version}. "
                f"Your changes were not saved. Re-fetch the page and reapply edits."
            )

        payload = {
            'id': self.page_id,
            'type': 'page',
            'title': self.title,
            'body': {'storage': {'value': self.body, 'representation': 'storage'}},
            'version': {'number': latest_version + 1},
        }
        if comment:
            payload['version']['message'] = comment

        resp = requests.put(
            f'{self.BASE}/{self.page_id}',
            json=payload,
            headers=self.headers,
            verify=False,
            params={'expand': 'version'}
        )
        resp.raise_for_status()
        data = resp.json()
        self.version = data['version']['number']
        self._original_body = self.body
        self._dirty = False
        print(f"Saved: {self.title} (v{self.version})")
        return self

    def preview(self):
        """Print the current body for review before saving."""
        print(f"Title: {self.title}")
        print(f"Version: {self.version}")
        print(f"Dirty: {self._dirty}")
        print(f"Body length: {len(self.body)} chars")
        print("---")
        print(self.body[:2000])
        if len(self.body) > 2000:
            print(f"... ({len(self.body) - 2000} more chars)")

    def diff(self):
        """Show a simple diff of changes made."""
        if not self._dirty:
            print("No changes made.")
            return
        import difflib
        old_lines = self._original_body.split('><')
        new_lines = self.body.split('><')
        diff = difflib.unified_diff(old_lines, new_lines, lineterm='')
        for line in diff:
            print(line)
