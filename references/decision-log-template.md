# Decision Log Template

## Page Info

- **Page ID**: `1346668352`
- **URL**: [Link](https://wiki.cfdata.org/spaces/INFOSEC/pages/1346668352)
- **Status**: LIVE (converted from Notes page)
- **Parent**: Program Hub (`1276292540`)

## Page Structure

The decision log is a single Confluence page that serves as the immutable record of all program decisions.

### Layout

1. **Header**: TFD Decision Log
2. **About This Log panel**: Explains immutability rules
3. **Decision Log table**: All decisions with status lozenges
4. **Decision Log Principles section**: Guidelines for logging decisions

### Decision Log Table Columns

| Column | Description | Example |
|--------|-------------|---------|
| Date | When decided | 2026-06-20 |
| Decision | What was decided | Add AI Security as Wave 2 threat model |
| Stakeholders | Who's affected | Security Eng, AI Platform team |
| Outcome | What changes | New Jira label, new control tickets |
| Status | Active/Superseded | Green lozenge "ACTIVE" |

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
tbody_start = body.find('<tbody>', body.find('Decision Log'))
tbody_end = body.find('</tbody>', tbody_start)

# Find the last </tr> in the table
last_tr = body.rfind('</tr>', tbody_start, tbody_end)

# Build new row
new_row = f'''<tr>
  <td>{date}</td>
  <td><strong>{decision}</strong></td>
  <td>{stakeholders}</td>
  <td>{outcome}</td>
  <td><ac:structured-macro ac:name="status" ac:schema-version="1" ac:macro-id="{uuid.uuid4()}">
    <ac:parameter ac:name="subtle">true</ac:parameter>
    <ac:parameter ac:name="colour">Green</ac:parameter>
    <ac:parameter ac:name="title">ACTIVE</ac:parameter>
  </ac:structured-macro></td>
</tr>'''

# Insert after last </tr>
body = body[:last_tr + 5] + new_row + body[last_tr + 5:]
```

---

## Current Decisions (as of Jun 20, 2026)

4 historical decisions migrated from comments:
1. Program restructuring decisions
2. Wave 2 threat model additions
3. Hub page design approvals
4. Agenda format changes

(See live page for current decision log content)
