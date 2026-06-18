---
name: wiki-builder
description: Create and edit Confluence wiki pages on wiki.cfdata.org. Use this skill whenever the user asks to create a wiki page, build a dashboard, make a Confluence page, set up wiki documentation with macros (Jira issues, panels, status lozenges, tables, charts, roadmaps, table filters), edit existing pages, or replicate/copy existing wiki pages. Also use when the user mentions wiki.cfdata.org, Confluence, or wants to revamp/redesign a wiki page.
---

# Wiki Builder

Create editable, dynamic Confluence wiki pages on wiki.cfdata.org using the Confluence REST API via the `wikigen-generic.sh` script.

## Prerequisites

Before creating any page, verify these are in place:

1. **Script**: The user must have `wikigen-generic.sh` in their home directory and it must be executable
2. **Cloudflared token**: Must have a valid token in `~/.cloudflared/` for `wiki.cfdata.org`. If missing, run:
   ```bash
   cloudflared access login https://wiki.cfdata.org/
   ```
3. **Jira app link ID**: `cc100dec-3d79-305b-8fae-4caba5e44cd2` (used as `serverId` parameter)

## Critical Rule: Use Storage Format, NOT Rendered HTML

**ALWAYS use Confluence Storage Format (XHTML)** for page content. Never use rendered HTML with JavaScript, DOM IDs, or plugin-generated markup. Rendered HTML blocks the Confluence editor and makes pages uneditable.

Storage format uses `<ac:structured-macro>` tags to declare macros. Confluence renders them at view time. This keeps the editor clean and functional.

## Content File Structure

Every page content file must start with:

```xml
<ac:confluence xmlns:ac="https://jira.atlassian.com/wiki" xmlns:ri="http://atlassian.com/resource/identifier">
```

And end with `</ac:confluence>`.

Do NOT include `<?xml?>` or `<!DOCTYPE>` declarations -- the REST API rejects them.

## Macro Reference

### Jira Issues Count Macro (CRITICAL - exact format required)

The Jira macro requires ALL of these parameters and attributes to work correctly:

```xml
<ac:structured-macro ac:name="jira" ac:schema-version="1" ac:macro-id="UNIQUE-UUID-HERE">
  <ac:parameter ac:name="server">Cloudflare Jira</ac:parameter>
  <ac:parameter ac:name="serverId">cc100dec-3d79-305b-8fae-4caba5e44cd2</ac:parameter>
  <ac:parameter ac:name="jqlQuery">labels = ThreatFocusedControl AND status = Done</ac:parameter>
  <ac:parameter ac:name="count">true</ac:parameter>
</ac:structured-macro>
```

**Key details:**
- Parameter name is `jqlQuery` (NOT `jql`)
- `server` is the display name `Cloudflare Jira`
- `serverId` is the app link ID `cc100dec-3d79-305b-8fae-4caba5e44cd2`
- Each macro needs `ac:schema-version="1"` and a unique `ac:macro-id` (UUID)
- Generate a fresh UUID for each Jira macro instance

### Panel Macro

```xml
<ac:structured-macro ac:name="panel">
  <ac:parameter ac:name="borderColor">#1c5e98</ac:parameter>
  <ac:parameter ac:name="borderWidth">2</ac:parameter>
  <ac:parameter ac:name="title">Panel Title</ac:parameter>
  <ac:parameter ac:name="titleBGColor">#1c5e98</ac:parameter>
  <ac:parameter ac:name="titleColor">#FFFFFF</ac:parameter>
  <ac:rich-text-body>
    <p>Panel content here</p>
  </ac:rich-text-body>
</ac:structured-macro>
```

For panels without a header, omit the `title`, `titleBGColor`, and `titleColor` parameters.

### Status Lozange

```xml
<ac:structured-macro ac:name="status">
  <ac:parameter ac:name="colour">Green</ac:parameter>
  <ac:parameter ac:name="title">ON TRACK</ac:parameter>
</ac:structured-macro>
```
Colours: Green, Blue, Yellow, Red, Grey

### Info Macro

```xml
<ac:structured-macro ac:name="info">
  <ac:parameter ac:name="title">Info Title</ac:parameter>
  <ac:rich-text-body><p>Info content</p></ac:rich-text-body>
</ac:structured-macro>
```

### UI Button

```xml
<ac:structured-macro ac:name="ui-button" ac:schema-version="1" ac:macro-id="UNIQUE-UUID">
  <ac:parameter ac:name="color">blue</ac:parameter>
  <ac:parameter ac:name="title">Button Title</ac:parameter>
  <ac:parameter ac:name="url">https://wiki.cfdata.org/...</ac:parameter>
</ac:structured-macro>
```
Note: `color` is `blue` (not `rgb(...)`), parameter is `url` (not `link`), no `textColor` parameter.

### UI Tabs (CRITICAL - exact format required)

The tab parameter is `title` (NOT `name`), and both `ui-tabs` and `ui-tab` need `ac:schema-version` and `ac:macro-id`:

```xml
<ac:structured-macro ac:name="ui-tabs" ac:schema-version="1" ac:macro-id="UNIQUE-UUID-1">
  <ac:rich-text-body>
    <ac:structured-macro ac:name="ui-tab" ac:schema-version="1" ac:macro-id="UNIQUE-UUID-2">
      <ac:parameter ac:name="title">Tab Name</ac:parameter>
      <ac:rich-text-body>
        <p>Tab content</p>
      </ac:rich-text-body>
    </ac:structured-macro>
  </ac:rich-text-body>
</ac:structured-macro>
```

### Style Macro (CSS)

```xml
<ac:structured-macro ac:name="style">
  <ac:plain-text-body><![CDATA[
#grad1{ background: rgb(28,94,152); background: linear-gradient(145deg, rgba(28,94,152) 0%, rgba(32,109,177) 50%, rgba(40,133,215) 100%); box-sizing: border-box; padding: 1em;}
]]></ac:plain-text-body>
</ac:structured-macro>
```

### Section/Column Layout

```xml
<ac:structured-macro ac:name="section">
  <ac:rich-text-body>
    <ac:structured-macro ac:name="column">
      <ac:rich-text-body>
        <p>Column content</p>
      </ac:rich-text-body>
    </ac:structured-macro>
  </ac:rich-text-body>
</ac:structured-macro>
```

### Expand Macro (Collapsible Section)

```xml
<ac:structured-macro ac:name="expand" ac:schema-version="1" ac:macro-id="UNIQUE-UUID">
  <ac:parameter ac:name="title">Click to Expand</ac:parameter>
  <ac:rich-text-body>
    <p>Collapsible content here</p>
  </ac:rich-text-body>
</ac:structured-macro>
```

### Table Filter (Stiltsoft)

```xml
<ac:structured-macro ac:name="table-filter">
  <ac:rich-text-body>
    <table><tbody>
      <tr><th>Col1</th><th>Col2</th></tr>
      <tr><td>Data</td><td>Data</td></tr>
    </tbody></table>
  </ac:rich-text-body>
</ac:structured-macro>
```

### Roadmap Planner (Stiltsoft)

```xml
<ac:structured-macro ac:name="roadmap">
  <ac:parameter ac:name="source">manual</ac:parameter>
  <ac:parameter ac:name="title">Roadmap Title</ac:parameter>
  <ac:parameter ac:name="timeframe">month</ac:parameter>
  <ac:parameter ac:name="startDate">2025-11-01</ac:parameter>
  <ac:parameter ac:name="endDate">2026-10-31</ac:parameter>
</ac:structured-macro>
```

## UI/UX Design Patterns

When designing wiki pages, think like a UI/UX designer. Use these proven patterns:

### Pattern 1: Landing Page with Tabs
- Gradient header banner (style macro + div)
- Welcome panel with program description
- Info panel inside welcome for context/status
- UI button linking to FAQ or key resource
- "How to read this page" panel explaining tab navigation
- Team/Stakeholders table
- UI tabs organizing content by topic

### Pattern 2: Program Health Dashboard
- 2x2 colored panel grid with Jira count macros
- Green = completed/on track, Blue = in progress, Yellow = needs attention, Red = blocked/action needed
- Status lozenges under each count
- Reporting table with per-threat-model Jira counts

### Pattern 3: Handbook / Reference Tab
- "How to Use This Handbook" intro panel
- Roles & Definitions table (Role, Definition, Responsibility)
- Threat models list with descriptions
- Step-by-step workflow guides in numbered lists
- Label reference table
- Escalation paths table (Situation, Action, Channel/Contact)
- Definition of Done panel with status lozenge
- Weekly cadence table

### Pattern 4: Workstreams / Tickets
- 3-column summary cards (Backlog, In Progress, Completed) with Jira counts
- Table Filter macro for open tickets
- Color-coded panel borders matching status

### Pattern 5: Timeline & Milestones
- Roadmap Planner macro
- Milestones table with status lozenges
- Expand macro for collapsible milestone lists

## Creating a Page

Use the script with these flags:
- `-s SPACE_KEY` -- Space key (e.g., INFOSEC)
- `-t "Page Title"` -- Title
- `-i PARENT_PAGE_ID` -- Parent page ID (optional)
- `-c content.html` -- Content file path

```bash
~/wikigen-generic.sh -s INFOSEC -t "My Page" -i 1424133824 -c ~/test-page-content.html
```

## Updating an Existing Page

To edit a specific section of an existing page:

1. **Fetch the current page** storage format and version:
```bash
CF_TOKEN=$(cloudflared access login https://wiki.cfdata.org/ 2>&1 | grep -o 'eyJ[a-zA-Z0-9\._-]*' | head -1)
curl -s -k -H "cf-access-token: $CF_TOKEN" "https://wiki.cfdata.org/rest/api/content/PAGE_ID?expand=body.storage,version" > /tmp/page.json
```

2. **Find the exact section boundaries** to replace:
```python
old_start = body.find('Section Title</ac:parameter>')
next_section_start = body.find('NextSection</ac:parameter>', old_start)
region = body[old_start:next_section_start]
first_close = region.find('</ac:rich-text-body></ac:structured-macro>')
old_end = old_start + first_close + len('</ac:rich-text-body></ac:structured-macro>')
```

3. **Build replacement content** in storage format XHTML

4. **Replace and update** via curl PUT:
```bash
curl -s -k -X PUT \
  -H "Content-Type: application/json" \
  -H "cf-access-token: $CF_TOKEN" \
  -H "X-Atlassian-Token: no-check" \
  -d @/ttp/wiki-update-payload.json \
  "https://wiki.cfdata.org/rest/api/content/PAGE_ID"
```

**IMPORTANT**: Always fetch the version right before updating — pages can be edited by others between fetches.

## Workflow for Building a Page

1. **Understand what the user wants** -- what sections, macros, data sources
2. **If replicating an existing page**, fetch it first via the REST API to extract the storage format and JQL queries
3. **Design the UI** -- choose the right pattern (landing page, dashboard, handbook, etc.)
4. **Build the content file** as Confluence Storage Format XHTML
5. **Validate XML balance** -- count open/close tags for structured-macro, rich-text-body
6. **Run the script** to create the page
7. **Share the URL** with the user
8. **Ask the user to test editing** -- can they click Edit and modify content?

## When Replicating an Existing Page

Fetch the source page's storage format to get exact macro parameters:

```bash
CF_TOKEN=$(cloudflared access login https://wiki.cfdata.org/ 2>&1 | grep -o 'eyJ[a-zA-Z0-9\._-]*' | head -1)
curl -s -k -H "cf-access-token: $CF_TOKEN" "https://wiki.cfdata.org/rest/api/content/PAGE_ID?expand=body.storage"
```

Extract JQL queries from the storage format:
```python
import re
jqls = re.findall(r'ac:name="jqlQuery">([^<]+)<', body)
```

## Key Lessons Learned

- **Storage format = editable**. Rendered HTML = locked editor.
- **Jira macros**: parameter is `jqlQuery` (not `jql`), need both `server` (display name) and `serverId` (app link ID), plus `ac:schema-version` and `ac:macro-id`
- **UI tabs**: parameter is `title` (not `name`), need `ac:schema-version` and `ac:macro-id` on both `ui-tabs` and each `ui-tab`
- **UI button**: `color` is `blue` (not rgb), `url` (not `link`), no `textColor`, needs `ac:schema-version` and `ac:macro-id`
- **Stiltsoft macros** (table-filter, roadmap, table-chart) work when declared in storage format without pre-generated session IDs
- **No labels** on new pages unless the user specifically asks for them
- **Always validate XML tag balance** before creating -- mismatched tags cause API errors
- **Remove `<?xml?>` and `<!DOCTYPE>`** from content files before sending to API
- **To update a page**, fetch current version, find exact section boundaries, replace, PUT with incremented version
- **When replacing sections**, use `find()` for the first closing tag after the section start, not `rfind()` which can match parent elements
