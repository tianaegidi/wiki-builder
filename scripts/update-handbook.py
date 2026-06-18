import json, sys, uuid, subprocess, re, urllib.request, ssl

# Read the draft page
with open('/tmp/draft-page.json') as f:
    data = json.load(f)

body = data['body']['storage']['value']
version = data['version']['number']
title = data['title']

# Build the new Ticket Handling Handbook content
new_tab = '''Ticket Handling Handbook</ac:parameter><ac:rich-text-body>

<h2>📖 Ticket Handling Handbook</h2>

<ac:structured-macro ac:name="panel">
  <ac:parameter ac:name="title">How to Use This Handbook</ac:parameter>
  <ac:parameter ac:name="titleBGColor">#1c5e98</ac:parameter>
  <ac:parameter ac:name="titleColor">#FFFFFF</ac:parameter>
  <ac:rich-text-body>
    <p>This handbook is your single source of truth for managing the Threat-Focused Defense program. It covers roles, threat models, ticket workflows, and escalation paths. Bookmark this tab — you will reference it weekly.</p>
  </ac:rich-text-body>
</ac:structured-macro>

<p><br/></p>

<h2>👥 Roles &amp; Definitions</h2>

<ac:structured-macro ac:name="panel">
  <ac:parameter ac:name="title">Key Roles</ac:parameter>
  <ac:rich-text-body>
    <table>
      <tbody>
        <tr><th>Role</th><th>Definition</th><th>Responsibility</th></tr>
        <tr>
          <td><strong>Business Owner</strong></td>
          <td>The individual or team accountable for the successful implementation of a control. They own the outcome, not just the task.</td>
          <td>Confirm scope, set timelines, escalate blockers, sign off on completion</td>
        </tr>
        <tr>
          <td><strong>Assignee</strong></td>
          <td>The person doing the work — writing code, configuring tooling, running tests</td>
          <td>Execute the control, update ticket status, flag issues early</td>
        </tr>
        <tr>
          <td><strong>TPM / Program Lead</strong></td>
          <td>Owns the program dashboard, tracks progress, runs weekly reviews</td>
          <td>Keep Jira labels clean, run weekly health checks, escalate stale tickets</td>
        </tr>
        <tr>
          <td><strong>Security Leadership Sponsor</strong></td>
          <td>Executive sponsor who removes organizational blockers</td>
          <td>Approve scope changes, unblock cross-team dependencies</td>
        </tr>
      </tbody>
    </table>
  </ac:rich-text-body>
</ac:structured-macro>

<p><br/></p>

<h2>🧩 Threat Models</h2>

<ac:structured-macro ac:name="info">
  <ac:parameter ac:name="title">Current &amp; Planned</ac:parameter>
  <ac:rich-text-body>
    <p>We currently have <strong>5 active threat models</strong>. Three additional models are planned for Q3/Q4 rollout.</p>
  </ac:rich-text-body>
</ac:structured-macro>

<ac:structured-macro ac:name="panel">
  <ac:parameter ac:name="title">Active Threat Models (5)</ac:parameter>
  <ac:parameter ac:name="titleBGColor">#36B37E</ac:parameter>
  <ac:parameter ac:name="titleColor">#FFFFFF</ac:parameter>
  <ac:rich-text-body>
    <ol>
      <li><strong>Compromise of Core/Edge Infrastructure</strong> — Edge server boot validation, runtime integrity, anomalous behaviour detection</li>
      <li><strong>Malicious Insider Risk</strong> — Access control reviews, privilege escalation detection, data loss prevention</li>
      <li><strong>Compromise or Physical Tampering of Hardware</strong> — Colo rack integrity, tamper-evident seals, supply chain hardware validation</li>
      <li><strong>B2B SaaS Integration &amp; Supply Chain Exploitation</strong> — Vendor access reviews, SaaS integration controls, supply chain risk assessment</li>
      <li><strong>Software Supply Chain</strong> — Software dependency validation, build pipeline integrity, artifact signing</li>
    </ol>
  </ac:rich-text-body>
</ac:structured-macro>

<ac:structured-macro ac:name="panel">
  <ac:parameter ac:name="title">Planned Threat Models (3 — Placeholder)</ac:parameter>
  <ac:parameter ac:name="titleBGColor">#6554C0</ac:parameter>
  <ac:parameter ac:name="titleColor">#FFFFFF</ac:parameter>
  <ac:rich-text-body>
    <ol start="6">
      <li><strong>[TBD — Placeholder]</strong> — Scope and deliverables to be defined in Q3 planning</li>
      <li><strong>[TBD — Placeholder]</strong> — Scope and deliverables to be defined in Q3 planning</li>
      <li><strong>[TBD — Placeholder]</strong> — Scope and deliverables to be defined in Q4 planning</li>
    </ol>
  </ac:rich-text-body>
</ac:structured-macro>

<p><br/></p>

<h2>📋 Ticket Handling Workflow</h2>

<ac:structured-macro ac:name="panel">
  <ac:parameter ac:name="title">Step-by-Step Guide</ac:parameter>
  <ac:parameter ac:name="titleBGColor">#1c5e98</ac:parameter>
  <ac:parameter ac:name="titleColor">#FFFFFF</ac:parameter>
  <ac:rich-text-body>

    <h3>How to Handle a New Threat-Focused Control Ticket</h3>
    <ol>
      <li><strong>Verify labels</strong> — Ensure the ticket has <code>ThreatFocusedControl</code> + the correct threat model label (e.g., <code>CompromisedServer</code>, <code>PhysicalTampering</code>)</li>
      <li><strong>Assign an owner</strong> — Every ticket must have an assignee within <strong>5 business days</strong> of creation</li>
      <li><strong>Set a due date</strong> — Align to the quarterly commitment timeline (Q1, Q2, Q3, Q4)</li>
      <li><strong>Contact the owner</strong> — Confirm scope, timeline, and any dependencies. Log the contact in the Owner Contact Log</li>
      <li><strong>Update the ticket</strong> — Move from Backlog → In Progress once work begins</li>
      <li><strong>Track weekly</strong> — Review every Monday in the Program Health dashboard. Flag any ticket stalled &gt; 5 days</li>
    </ol>

    <h3>How to Close a Ticket</h3>
    <ol>
      <li><strong>Owner confirms implementation</strong> — The control has been implemented and validated</li>
      <li><strong>Due date is met</strong> — Or a new due date has been agreed with the TPM</li>
      <li><strong>Status = Done</strong> — Move ticket to Done status in Jira</li>
      <li><strong>Dashboard updates automatically</strong> — Jira macros on the Program Health tab will reflect the change on next page load</li>
    </ol>

    <h3>How to Handle a Blocker</h3>
    <ol>
      <li><strong>Mark ticket as Blocked</strong> in Jira</li>
      <li><strong>Add a comment</strong> explaining the blocker and what is needed to resolve it</li>
      <li><strong>Escalate if stale</strong> — If blocked &gt; 3 days, post in <code>#security-pmo</code> Slack channel</li>
      <li><strong>Escalation contacts:</strong> TPM (@tianaegidi), Manager (@corinne)</li>
    </ol>

  </ac:rich-text-body>
</ac:structured-macro>

<p><br/></p>

<h2>🏷️ Jira Label Reference</h2>

<ac:structured-macro ac:name="panel">
  <ac:parameter ac:name="title">Required Labels</ac:parameter>
  <ac:rich-text-body>
    <table>
      <tbody>
        <tr><th>Label</th><th>Purpose</th><th>Applies To</th></tr>
        <tr><td><code>ThreatFocusedControl</code></td><td>Program-level label — required on ALL tickets</td><td>Every ticket in this program</td></tr>
        <tr><td><code>CompromisedServer</code></td><td>Threat model: Core/Edge Infrastructure</td><td>Compromise of Core/Edge tickets</td></tr>
        <tr><td><code>InsiderThreat</code></td><td>Threat model: Malicious Insider</td><td>Insider risk tickets</td></tr>
        <tr><td><code>PhysicalTampering</code></td><td>Threat model: Physical Tampering</td><td>Physical/hardware tickets</td></tr>
        <tr><td><code>B2BSaaSIntegration</code></td><td>Threat model: B2B SaaS &amp; Supply Chain</td><td>B2B SaaS tickets</td></tr>
        <tr><td><code>SoftwareSupplyChain</code></td><td>Threat model: Software Supply Chain</td><td>Software supply chain tickets</td></tr>
      </tbody>
    </table>
  </ac:rich-text-body>
</ac:structured-macro>

<p><br/></p>

<h2>🚨 Escalation Paths</h2>

<table>
  <tbody>
    <tr><th>Situation</th><th>Action</th><th>Channel / Contact</th></tr>
    <tr>
      <td>Ticket unassigned &gt; 5 days</td>
      <td>Flag in weekly review, assign owner</td>
      <td>TPM (@tianaegidi)</td>
    </tr>
    <tr>
      <td>Ticket blocked &gt; 3 days</td>
      <td>Escalate immediately</td>
      <td><code>#security-pmo</code> Slack</td>
    </tr>
    <tr>
      <td>Scope change needed</td>
      <td>Discuss with TPM + Security Leadership</td>
      <td>TPM → Sponsor (@corinne)</td>
    </tr>
    <tr>
      <td>Due date at risk</td>
      <td>Notify TPM, propose new date</td>
      <td>TPM (@tianaegidi)</td>
    </tr>
    <tr>
      <td>New threat model proposed</td>
      <td>Submit for Q3/Q4 planning review</td>
      <td><code>#security-pmo</code> Slack</td>
    </tr>
  </tbody>
</table>

<p><br/></p>

<h2>✅ Definition of Done</h2>

<ac:structured-macro ac:name="panel">
  <ac:parameter ac:name="title">A ticket is Done when:</ac:parameter>
  <ac:parameter ac:name="titleBGColor">#36B37E</ac:parameter>
  <ac:parameter ac:name="titleColor">#FFFFFF</ac:parameter>
  <ac:rich-text-body>
    <ol>
      <li>Ticket status = <ac:structured-macro ac:name="status"><ac:parameter ac:name="colour">Green</ac:parameter><ac:parameter ac:name="title">DONE</ac:parameter></ac:structured-macro> in Jira</li>
      <li>Owner has confirmed implementation is complete</li>
      <li>Due date has been met (or renegotiated)</li>
      <li>Any related documentation has been updated</li>
      <li>The control appears in the "Completed" count on the Program Health dashboard</li>
    </ol>
  </ac:rich-text-body>
</ac:structured-macro>

<p><br/></p>

<h2>📅 Weekly Cadence</h2>

<table>
  <tbody>
    <tr><th>Day</th><th>Activity</th><th>Owner</th></tr>
    <tr><td>Monday</td><td>Review Program Health dashboard — check for stale tickets, unassigned, blocked</td><td>TPM</td></tr>
    <tr><td>Tuesday</td><td>Follow up with owners on any tickets needing attention</td><td>TPM</td></tr>
    <tr><td>Wednesday</td><td>Mid-week blocker triage — escalate anything blocked &gt; 3 days</td><td>TPM</td></tr>
    <tr><td>Thursday</td><td>Update Owner Contact Log with any new outreach</td><td>TPM</td></tr>
    <tr><td>Friday</td><td>Weekly summary — update dashboard metrics, flag trends</td><td>TPM</td></tr>
  </tbody>
</table>

</ac:rich-text-body></ac:structured-macro>'''

# Replace the old section
old_start = body.find('Ticket Handling Handbook</ac:parameter>')
resources_start = body.find('Resources</ac:parameter>', old_start)
search_region = body[old_start:resources_start]
last_close = search_region.rfind('</ac:rich-text-body></ac:structured-macro>')
tab_close = old_start + last_close

new_body = body[:old_start] + new_tab + body[tab_close:]

# Get cloudflared token
result = subprocess.run(['cloudflared', 'access', 'login', 'https://wiki.cfdata.org/'], capture_output=True, text=True)
token = ''
for line in (result.stdout + result.stderr).split('\n'):
    m = re.search(r'eyJ[a-zA-Z0-9\._-]+', line)
    if m:
        token = m.group(0)
        break

# Get current version via curl
result = subprocess.run([
    'curl', '-s', '-k',
    '-H', f'cf-access-token: {token}',
    'https://wiki.cfdata.org/rest/api/content/1424133824?expand=version'
], capture_output=True, text=True)
current = json.loads(result.stdout)
current_version = current['version']['number']
print(f'Current version: {current_version}')

# Build payload and update
payload = json.dumps({
    'id': '1424133824',
    'type': 'page',
    'title': current['title'],
    'space': {'key': 'INFOSEC'},
    'body': {'storage': {'value': new_body, 'representation': 'storage'}},
    'version': {'number': current_version + 1}
})

with open('/tmp/wiki-update-payload.json', 'w') as f:
    f.write(payload)

# Use curl to update
result = subprocess.run([
    'curl', '-s', '-k', '-X', 'PUT',
    '-H', 'Content-Type: application/json',
    '-H', f'cf-access-token: {token}',
    '-H', 'X-Atlassian-Token: no-check',
    '-d', '@/tmp/wiki-update-payload.json',
    'https://wiki.cfdata.org/rest/api/content/1424133824'
], capture_output=True, text=True)

resp_data = json.loads(result.stdout) if result.stdout else {}
if 'id' in resp_data:
    print(f'Updated to version {resp_data.get("version", {}).get("number", "?")}')
else:
    print(f'Error: {resp_data.get("message", result.stdout)}')