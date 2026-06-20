# Decision Log Template

## Page Structure

The decision log is a single Confluence page that serves as the immutable record of all program decisions and meeting notes.

### Page Hierarchy
```
Program Hub Page
├── Decision Log & Meeting Notes  ← this page
├── Status Updates (child pages or tab)
├── Agendas (child pages or tab)
└── Program Dashboard (tab on hub)
```

### Page Layout

1. **Header**: `📝 Decision Log — [Program Name]`
2. **About This Log panel**: Explains immutability rules
3. **Decision Log table**: All decisions with status lozenges
4. **Meeting Notes Archive**: Expand macros per meeting

---

## Decision Log Table Columns

| Column | Description | Example |
|--------|-------------|---------|
| # | Sequential number | 1 |
| Date | When decided | 2026-06-20 |
| Decision | What was decided | Add AI Security as Wave 2 threat model |
| Rationale | Why | Emerging risk from agentic AI adoption |
| Decided By | Who made the call | Tiana, Corinne |
| Stakeholders | Who's affected | Security Eng, AI Platform team |
| Impact | What changes | New Jira label, new control tickets |
| Status | Active/Superseded | Green lozenge "ACTIVE" |
| Supersedes | Entry # if replacing | — or #3 |

---

## Decision Status Lozenges

- **Green "ACTIVE"** — Decision is in effect
- **Grey "SUPERSEDED"** — Replaced by a newer decision (reference the new #)
- **Yellow "UNDER REVIEW"** — Being reconsidered but still in effect
- **Red "REVERSED"** — Decision was reversed without replacement

---

## Immutability Rules

1. **Never edit or delete a decision row** once logged
2. If a decision is reversed, add a NEW row with status "REVERSED" or "SUPERSEDED"
3. The new row should reference the original in the "Supersedes" column
4. The original row's status changes to "SUPERSEDED" with a reference to the new #
5. Meeting notes in expand macros are also immutable — add corrections as new entries

---

## Meeting Notes Format

Each meeting gets an expand macro with:
- Title: `📅 [Date] — [Meeting Type]`
- Attendees list
- Discussion summary (bullet points)
- Decisions made (bullet points, cross-referenced to decision log entries)
- Action items table (#, Action, Owner, Due)

### Meeting Types
- Weekly Sync
- Quarterly Review
- Threat Model Review
- Ad-Hoc / Emergency

---

## Adding a Decision (Workflow)

1. User provides: decision text, rationale, who decided, stakeholders, impact
2. Fetch the decision log page (storage format + version)
3. Find the last `</tr>` before `</tbody>` in the decisions table
4. Insert a new `<tr>` with the decision details
5. Auto-increment the decision number
6. PUT the update with version + 1
7. If the decision supersedes an earlier one, also update that row's status to "SUPERSEDED"

### Code Pattern

```python
# Find the decisions table tbody
tbody_start = body.find('<tbody>', body.find('All Decisions'))
tbody_end = body.find('</tbody>', tbody_start)

# Find the last </tr> in the table
last_tr = body.rfind('</tr>', tbody_start, tbody_end)

# Build new row
new_row = f'''<tr>
  <td>{next_number}</td>
  <td>{date}</td>
  <td><strong>{decision}</strong></td>
  <td>{rationale}</td>
  <td>{decided_by}</td>
  <td>{stakeholders}</td>
  <td>{impact}</td>
  <td><ac:structured-macro ac:name="status"><ac:parameter ac:name="colour">Green</ac:parameter><ac:parameter ac:name="title">ACTIVE</ac:parameter></ac:structured-macro></td>
  <td>—</td>
</tr>'''

# Insert after last </tr>
body = body[:last_tr + 5] + new_row + body[last_tr + 5:]
```

---

## Adding Meeting Notes (Workflow)

1. User provides: date, meeting type, attendees, discussion points, decisions, action items
2. Fetch the decision log page
3. Find the last expand macro before `</ac:confluence>`
4. Insert a new expand macro with the meeting notes
5. PUT the update with version + 1
6. Cross-reference any decisions to the decision log table

### Code Pattern

```python
# Find insertion point (before </ac:confluence>)
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
</ac:structured-macro>
'''

body = body[:confluence_close] + new_notes + body[confluence_close:]
```