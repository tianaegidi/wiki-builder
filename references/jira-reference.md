# Jira Integration Reference

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

## Common JQL Patterns

### Total count by label
```
labels = ThreatFocusedControl
```

### Count by status
```
labels = ThreatFocusedControl AND status = Done
labels = ThreatFocusedControl AND status = "In Progress"
labels = ThreatFocusedControl AND status = Blocked
labels = ThreatFocusedControl AND status = "Cancelled"
labels = ThreatFocusedControl AND status in ("Backlog","On Hold")
labels = ThreatFocusedControl AND status in (Done, Closed, Cancelled)
```

### Count by threat model label + status
```
labels = ThreatFocusedControl and labels in (CompromisedServer) AND status = backlog
labels = ThreatFocusedControl and labels in (CompromisedServer) AND status = "In Progress"
labels = ThreatFocusedControl and labels in (CompromisedServer) AND status = Done
labels = ThreatFocusedControl and labels in (CompromisedServer) AND status = "Blocked"
```

### Unassigned tickets
```
labels = ThreatFocusedControl AND assignee = null
```

### Open tickets (not done/cancelled)
```
labels = ThreatFocusedControl and status not in (Done, Cancelled)
```

## Threat Model Labels
- `CompromisedServer`
- `InsiderThreat`
- `PhysicalTampering`
- `B2BSaaSIntegration`
- `SoftwareSupplyChain`