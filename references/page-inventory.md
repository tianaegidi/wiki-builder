# TFD Page Inventory & Hierarchy

## Controlled Pages

This skill controls exactly 5 pages (plus their child pages) under:
`INFOSEC > Security Team Home > Security Programs > GRC Program > Threat-focused Defense`

### Page Map

| Page | ID | URL | Purpose |
|------|-----|-----|---------|
| TFD Program Hub [draft] | `1424133824` | [Link](https://wiki.cfdata.org/spaces/INFOSEC/pages/1424133824) | Main landing page with 7 tabs |
| Q1 Update | `1346668357` | [Link](https://wiki.cfdata.org/spaces/INFOSEC/pages/1346668357) | Quarterly briefing (orange theme) |
| Project Management Plan | `1419363218` | [Link](https://wiki.cfdata.org/spaces/INFOSEC/pages/1419363218) | TPM tracker (two-column w/ sidebar) |
| TFD Status Updates 2026 | `1424137842` | [Link](https://wiki.cfdata.org/spaces/INFOSEC/pages/1424137842) | Index for weekly agendas + status updates |
| Notes | `1346668352` | [Link](https://wiki.cfdata.org/spaces/INFOSEC/pages/1346668352) | Decision log & meeting notes (to be built out) |

### Hierarchy

```
Threat-focused Defense (ancestor)
├── Notes (1346668352)
│   └── Q1 Update (1346668357)
├── Project Management Plan (1419363218)
├── TFD Status Updates 2026 (1424137842)
│   ├── 6/17/26 TFD Weekly Agenda (1424137886)
│   └── 6/19/26 Status Update (1424152018)
└── TFD Program [draft] (1424133824)
```

### Child Page Naming Conventions

Under TFD Status Updates 2026 (ID: `1424137842`):
- **Agendas**: `[M/D/YY] TFD Weekly Agenda` (e.g., "6/17/26 TFD Weekly Agenda")
- **Status updates**: `[M/D/YY] Status Update` (e.g., "6/19/26 Status Update")

### Index Table on Status Updates Page

The parent page (1424137842) has a 2-column table:

| Weekly Meeting Agenda | Friday Status Send-Out |
|----------------------|----------------------|
| [Link to agenda page] | [Link to status page] |

When creating a new agenda or status update, add a row to this table.

---

## Design Themes

| Page | Gradient | Layout |
|------|----------|--------|
| TFD Program Hub | Blue (`#1c5e98 → #206db1 → #2885d7`) | Single column with tabs |
| Q1 Update | Orange (`#ff6633 → #f6821f → #fbad41`) | Single column with tabs |
| PM Plan | None | Two-column with right sidebar |
| Status Updates | None | Simple table |
| Weekly Agenda | None | Two equal columns |
| Status Update | None | Two-column with right sidebar |

---

## Hub Page Tab Inventory (ID: 1424133824)

| Tab | Content | JQL Count |
|-----|---------|-----------|
| Program Overview | Threat models table with wave separators | 0 (links only) |
| Program Health | 2x2 dashboard + threat model breakdown | ~20 |
| Timeline & Milestones | Roadmap + milestones table | 0 |
| Now \| Next \| Later | Workstream prioritization | 0 |
| Workstreams | Open/closed tickets with table filters | ~10 |
| Ticket Handling Handbook | Roles, workflows, escalation, DoD | 0 |
| Resources | Links to all program resources | 0 |

---

## Q1 Update Tab Inventory (ID: 1346668357)

| Tab | Content |
|-----|---------|
| Top 5 Threat Scenarios: Current Progress | Per-model done/total with JQL |
| High Level Overview | Summary metrics |
| Q1 Deliverables | Deliverables with due date filters |
| Top 5 Threat Scenarios: 2026 & Beyond | Future commitments per model |
| 2026 Commitments | Annual commitments table |
| Impacted by EDR Replacement | EDR-dependent deliverables |
| Beyond 2026 | Multi-year security controls |
| Expanding beyond the Top 5 Threats | Wave 2 expansion plans |
| Resources | Links and references |