# TFD Page Inventory & Hierarchy

## Controlled Pages

All pages under: `INFOSEC > Security Team Home > Security Programs > GRC Program > Threat-focused Defense`

### Page Map

| Page | ID | URL | Purpose | Status |
|------|-----|-----|---------|--------|
| **Program Hub** | `1276292540` | [Link](https://wiki.cfdata.org/spaces/INFOSEC/pages/1276292540) | Main landing page with 8 tabs | LIVE (replaced old page) |
| **Status Updates 2026** | `1424137842` | [Link](https://wiki.cfdata.org/spaces/INFOSEC/pages/1424137842) | Index for weekly agendas + status reports | LIVE |
| **Decision Log** | `1346668352` | [Link](https://wiki.cfdata.org/spaces/INFOSEC/pages/1346668352) | Decision log & meeting notes | LIVE (converted from Notes) |
| **Q1 Update** | `1346668357` | [Link](https://wiki.cfdata.org/spaces/INFOSEC/pages/1346668357) | Quarterly briefing (orange theme) | LIVE |
| **PM Plan** | `1419363218` | [Link](https://wiki.cfdata.org/spaces/INFOSEC/pages/1419363218) | TPM tracker (two-column w/ sidebar) | Under Construction |
| ~~Program Hub [draft]~~ | `1424133824` | [Link](https://wiki.cfdata.org/spaces/INFOSEC/pages/1424133824) | Old draft — content moved to live hub | OBSOLETE (can delete) |

### Hierarchy

```
Threat-focused Defense (1276292540) ← Program Hub (LIVE)
├── Notes / Decision Log (1346668352)
│   └── Q1 Update (1346668357)
├── Project Management Plan (1419363218)
├── TFD Status Updates 2026 (1424137842) ← Index page
│   ├── 6/17/26 TFD Weekly Agenda (1424137886)
│   ├── 6/19/26 Status Update (1424152018)
│   └── 6/26/26 TFD Weekly Agenda (1424156221)
└── TFD Program [draft] (1424133824) ← OLD DRAFT, content moved to hub
```

### Child Page Naming Conventions

Under TFD Status Updates 2026 (ID: `1424137842`):
- **Agendas**: `[M/D/YY] TFD Weekly Agenda` (e.g., "6/26/26 TFD Weekly Agenda")
- **Status updates**: `[M/D/YY] Status Update` (e.g., "6/19/26 Status Update")

---

## Design Themes

| Page | Gradient | Layout | Notes |
|------|----------|--------|-------|
| Program Hub | Blue (`#1c5e98 → #206db1 → #2885d7`) | Single column with 8 tabs | Live page |
| Q1 Update | Orange (`#ff6633 → #f6821f → #fbad41`) | Single column with 9 tabs | Quarterly |
| PM Plan | None | Two-column with right sidebar | Under construction |
| Status Updates Index | None | Simple 2-column table | Index page |
| Weekly Agenda | None | Single column, colored table-cell headers | NO ac:layout (locks editor) |
| Status Update | None | Two-column with right sidebar (`ac:layout` OK) | Not edited live |

---

## Program Hub Tab Inventory (ID: 1276292540)

| Tab | Content | JQL Count |
|-----|---------|-----------|
| Program Overview | Threat models table with Wave 1 (5 models) + Wave 2 (3 models) separators | 0 (links only) |
| Program Health | 2x2 Progress Panel dashboard + threat model breakdown table | ~20 |
| Timeline & Milestones | Stiltsoft Roadmap Planner + milestones table with status lozenges | 0 |
| Now \| Next \| Later | 3 sub-tabs with workstream tables, Jira count macros, status lozenges | ~15 |
| Status Distribution | KPI cards (Total/In Progress/Blocked), threat model breakdown, priority distribution, assignment overview | ~25 |
| Workstreams | Open/closed tickets with table filters | ~10 |
| Ticket Handling Handbook | Roles, workflows, escalation, DoD, labels, cadence | 0 |
| Resources | Links to all program resources | 0 |

### Progress Panel (DO NOT CHANGE SIZING)

| Position | Border | BG | Text Color | Metric |
|----------|--------|----|------------|--------|
| Top-left | `#008000` | `#F0FFF0` | `#008000` | Completion Rate |
| Top-right | `#87CEFA` | `#F0F8FF` | `#1c5e98` | P1 Uncompleted |
| Bottom-left | `#FFC000` | `#FFFDE7` | `#B8860B` | Unassigned |
| Bottom-right | `#FF0000` | `#FFF0F0` | `#CC0000` | Blocked |

### Roadmap Colors
- Wave 1 = orange (`#e8741e` / `#f5a623`)
- Wave 2 = yellow (`#f5c842` / `#fce596`)

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

---

## Existing Child Pages Under Status Updates 2026

| Page ID | Title | Type | Date |
|---------|-------|------|------|
| `1424137886` | 6/17/26 TFD Weekly Agenda | Agenda | Jun 17, 2026 |
| `1424152018` | 6/19/26 Status Update | Status Update | Jun 19, 2026 |
| `1424156221` | 6/26/26 TFD Weekly Agenda | Agenda | Jun 26, 2026 |

---

## Jira Stats (as of Jun 20, 2026)

- **Total tickets**: 145
- **Done**: 55
- **In Progress**: 25
- **Backlog**: 63
- **Blocked**: 1
- **Cancelled**: 1
- **Unassigned**: 4
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
