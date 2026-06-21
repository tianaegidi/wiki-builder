# Jira Integration Reference — TFD Program

## Jira Macro Format (exact)

```xml
<ac:structured-macro ac:name="jira" ac:schema-version="1" ac:macro-id="UNIQUE-UUID">
  <ac:parameter ac:name="server">Cloudflare Jira</ac:parameter>
  <ac:parameter ac:name="serverId">cc100dec-3d79-305b-8fae-4caba5e44cd2</ac:parameter>
  <ac:parameter ac:name="jqlQuery">YOUR JQL HERE</ac:parameter>
  <ac:parameter ac:name="count">true</ac:parameter>
</ac:structured-macro>
```

- `server` = display name "Cloudflare Jira"
- `serverId` = app link ID "cc100dec-3d79-305b-8fae-4caba5e44cd2"
- `jqlQuery` = the JQL (NOT `jql`)
- Each macro needs a unique UUID for `ac:macro-id`

### Python Helper

```python
import uuid

def jira_count(jql):
    return f'''<ac:structured-macro ac:name="jira" ac:schema-version="1" ac:macro-id="{uuid.uuid4()}">
  <ac:parameter ac:name="server">Cloudflare Jira</ac:parameter>
  <ac:parameter ac:name="serverId">cc100dec-3d79-305b-8fae-4caba5e44cd2</ac:parameter>
  <ac:parameter ac:name="jqlQuery">{jql}</ac:parameter>
  <ac:parameter ac:name="count">true</ac:parameter>
</ac:structured-macro>'''
```

### Fetching Live Counts via REST API

```python
import requests, urllib3
urllib3.disable_warnings()

# Get Jira token (separate from wiki token)
result = subprocess.run(['cloudflared', 'access', 'login', 'https://jira.cfdata.org/'],
                        capture_output=True, text=True)
jira_token = None
for line in (result.stdout + result.stderr).split('\n'):
    m = re.search(r'eyJ[a-zA-Z0-9._-]+', line)
    if m:
        jira_token = m.group(0)
        break

JIRA_HEADERS = {'cf-access-token': jira_token}

def jira_total(jql):
    resp = requests.get(
        f'https://jira.cfdata.org/rest/api/2/search?jql={jql}&maxResults=0',
        headers=JIRA_HEADERS, verify=False
    )
    return resp.json()['total']
```

## TFD Threat Model Labels

### Wave 1 — Initial Five (Q1–Q2)
- `CompromisedServer`
- `InsiderThreat`
- `PhysicalTampering`
- `B2BSaaSIntegration`
- `SoftwareSupplyChain`

### Wave 2 — Expansion (Q3–Q4)
- `UnauthorizedAccessCustomerData`
- `CustomerZero`
- `AISecurity`

### Other Labels
- `ThreatFocusedControl` — required on ALL program tickets
- `needs-discussion` — flagged for discussion
- `Q1'26`, `Q2'26`, `Q3'26`, `Q4'26` — quarterly commitment labels

## Common JQL Patterns

### Program-level counts
```
Total:       labels = ThreatFocusedControl
Completed:   labels = ThreatFocusedControl AND status in (Done, Closed, Cancelled)
In Progress: labels = ThreatFocusedControl AND status = "In Progress"
Blocked:     labels = ThreatFocusedControl AND status in (Blocked)
Unassigned:  labels = ThreatFocusedControl AND assignee = EMPTY
Open:        labels = ThreatFocusedControl and status not in (Done, Cancelled)
```

### Per-threat-model counts
```
Backlog:     labels = ThreatFocusedControl and labels in (LABEL) AND status = backlog
In Progress: labels = ThreatFocusedControl and labels in (LABEL) AND status = "In Progress"
Done:        labels = ThreatFocusedControl and labels in (LABEL) AND status = Done
Blocked:     labels = ThreatFocusedControl and labels in (LABEL) AND status = Blocked
```

### Status update JQL (per threat model, simpler format)
```
Done:   labels = ThreatFocusedControl and labels in (LABEL) and status in (Done, Cancelled)
Open:   labels = ThreatFocusedControl and labels in (LABEL) and status not in (Done, Cancelled)
Total:  labels = ThreatFocusedControl and labels in (LABEL)
```

### Priority counts
```
P1 High:     project = GRC and priority = "High" and labels = ThreatFocusedControl
P2 Moderate: project = GRC and priority = "Moderate" and labels = ThreatFocusedControl
P3 Low:      project = GRC and priority = "Low" and labels = ThreatFocusedControl
```

### Q1 Update JQL (with due date filters)
```
# Q1 completed by threat model
project = GRC AND labels = ThreatFocusedControl and labels = [MODEL] 
  and (status in (Done, Cancelled, Closed) or due <= 2026-3-31) 
  and labels not in ("needs-discussion")

# All Q1 commitments
project = GRC and ((status in (Done, Closed) or due <= 2026-3-31) 
  or labels in ("Q1'26")) and labels = ThreatFocusedControl

# Needs discussion
project = GRC and status not in (Done, Closed, Cancelled) 
  and labels = ThreatFocusedControl and labels in ("needs-discussion")

# No due date, no quarter label, has business owner
project = GRC and status not in (Done, Closed, Cancelled) and due = EMPTY 
  and labels = ThreatFocusedControl 
  and labels not in ("Q1'26", "Q2'26", "Q3'26", "Q4'26") 
  and "Business Owner" != EMPTY
```

## Status Lozenge Logic

| Completion Rate | Blocked > 3 days | Unassigned > 5 | Lozenge |
|----------------|-------------------|-----------------|---------|
| >= 70% | No | No | Green (ON TRACK) |
| 40-69% | Yes | Yes | Yellow (AT RISK) |
| < 40% | Yes | Yes | Red (OFF TRACK) |

## Jira URL Pattern
```
https://jira.cfdata.org/issues/?jql=[URL_ENCODED_JQL]
```
Example:
```
https://jira.cfdata.org/issues/?jql=labels%20%3D%20ThreatFocusedControl%20and%20labels%20in%20(CompromisedServer)
```

**WARNING**: Always verify `issues` is spelled correctly in generated content — tool corruption can drop the `u` making it `isses`.

## Current Jira Stats (as of Jun 20, 2026)

- **Total tickets**: 145
- **Done**: 55
- **In Progress**: 25
- **Backlog**: 63
- **Blocked**: 1
- **Cancelled**: 1
- **Unassigned**: 12
- **Assigned**: 133

### By Priority
- P1 High: 60
- P2 Moderate: 72
- P3 Low: 13

### By Threat Model
- CompromisedServer: 124
- PhysicalTampering: 36
- B2BSaaSIntegration: 12
- SoftwareSupplyChain: 17
- InsiderThreat: 0
- Wave 2 models: 0
