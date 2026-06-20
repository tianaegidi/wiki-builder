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
labels = ThreatFocusedControl
labels = ThreatFocusedControl AND status in (Done, Closed, Cancelled)
labels = ThreatFocusedControl AND status = "In Progress"
labels = ThreatFocusedControl AND status in (Blocked)
labels = ThreatFocusedControl AND assignee = EMPTY
labels = ThreatFocusedControl and status not in (Done, Cancelled)
```

### Per-threat-model counts
```
labels = ThreatFocusedControl and labels in (CompromisedServer) AND status = backlog
labels = ThreatFocusedControl and labels in (CompromisedServer) AND status = "In Progress"
labels = ThreatFocusedControl and labels in (CompromisedServer) AND status = Done
labels = ThreatFocusedControl and labels in (CompromisedServer) AND status = Blocked
```

### Status update JQL (per threat model, simpler format)
```
Done:   labels = [LABEL] and status in (Done, Cancelled)
Open:   labels = [LABEL] and status not in (Done, Cancelled)
Total:  labels = [LABEL]
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

# Due this year
project = GRC and due <= 2026-12-31 and labels = ThreatFocusedControl

# Due next year
project = GRC and due <= 2027-12-31 and labels = ThreatFocusedControl

# High priority
project = GRC and priority = "Highest" and labels = ThreatFocusedControl
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