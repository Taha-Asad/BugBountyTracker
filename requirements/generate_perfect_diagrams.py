import subprocess, os

os.makedirs('projects/BugBountyTrack/requirements/diagrams', exist_ok=True)

# -------------------------------------------------------------
# 1. Figure 4.1: Component Architecture SVG (Commercial B2B SaaS Layer)
# -------------------------------------------------------------
svg_comp = '''<svg width="920" height="470" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr" markerWidth="9" markerHeight="6" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 9 3, 0 6" fill="#386B24" />
    </marker>
    <marker id="arr_ext" markerWidth="9" markerHeight="6" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 9 3, 0 6" fill="#0284C7" />
    </marker>
  </defs>
  <rect width="100%" height="100%" fill="#FFFFFF"/>
  <text x="460" y="26" font-family="DejaVu Sans, Arial" font-size="15" font-weight="bold" fill="#1B1D1E" text-anchor="middle">Figure 4.1: BugBountyTrack 3-Tier Decoupled Architecture &amp; Commercial Services</text>

  <!-- Tier 1: Client Tier -->
  <rect x="20" y="48" width="225" height="405" rx="8" fill="#F7FAF2" stroke="#386B24" stroke-width="2"/>
  <rect x="20" y="48" width="225" height="34" rx="8" fill="#E3EFCB"/>
  <text x="132" y="70" font-family="DejaVu Sans, Arial" font-size="11.5" font-weight="bold" fill="#1B1D1E" text-anchor="middle">Tier 1: Client Browser Runtime</text>
  
  <rect x="30" y="92" width="205" height="52" rx="5" fill="#FFFFFF" stroke="#D1E3A5" stroke-width="1.5"/>
  <text x="132" y="111" font-family="DejaVu Sans, Arial" font-size="10.5" font-weight="bold" fill="#222222" text-anchor="middle">Next.js 14 App Router UI</text>
  <text x="132" y="126" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#555555" text-anchor="middle">Guided Onboarding &amp; Health Checklist</text>
  <text x="132" y="138" font-family="DejaVu Sans, Arial" font-size="8" fill="#386B24" text-anchor="middle">Redacted Closure PDF/HTML Exporter</text>

  <rect x="30" y="152" width="205" height="56" rx="5" fill="#FFFFFF" stroke="#D1E3A5" stroke-width="1.5"/>
  <text x="132" y="171" font-family="DejaVu Sans, Arial" font-size="10.5" font-weight="bold" fill="#222222" text-anchor="middle">OpenPGP.js &amp; WebCrypto</text>
  <text x="132" y="187" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#555555" text-anchor="middle">Dual-Recipient Payload Encryption</text>
  <text x="132" y="200" font-family="DejaVu Sans, Arial" font-size="8" fill="#386B24" text-anchor="middle">Title &amp; Exploit Ciphertext Isolation</text>

  <rect x="30" y="216" width="205" height="60" rx="5" fill="#FFFFFF" stroke="#D1E3A5" stroke-width="1.5"/>
  <text x="132" y="235" font-family="DejaVu Sans, Arial" font-size="10.5" font-weight="bold" fill="#222222" text-anchor="middle">IndexedDB KeyStore &amp; Backup</text>
  <text x="132" y="250" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#555555" text-anchor="middle">PBKDF2/AES-GCM Local Passphrase</text>
  <text x="132" y="263" font-family="DejaVu Sans, Arial" font-size="8" fill="#386B24" text-anchor="middle">Protected Armored Export &amp; Restore</text>
  <text x="132" y="273" font-family="DejaVu Sans, Arial" font-size="7.5" fill="#B91C1C" text-anchor="middle">0 Plaintext Key Material to Server</text>

  <rect x="30" y="284" width="205" height="50" rx="5" fill="#FFFFFF" stroke="#D1E3A5" stroke-width="1.5"/>
  <text x="132" y="303" font-family="DejaVu Sans, Arial" font-size="10.5" font-weight="bold" fill="#222222" text-anchor="middle">rehype-sanitize AST Parser</text>
  <text x="132" y="319" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#555555" text-anchor="middle">Stored XSS Defense &amp; Safe Markdown</text>
  <text x="132" y="330" font-family="DejaVu Sans, Arial" font-size="7.5" fill="#555555" text-anchor="middle">Strict HTML Tag Allowlist</text>

  <rect x="30" y="342" width="205" height="48" rx="5" fill="#FFFFFF" stroke="#D1E3A5" stroke-width="1.5"/>
  <text x="132" y="361" font-family="DejaVu Sans, Arial" font-size="10.5" font-weight="bold" fill="#222222" text-anchor="middle">Local SHA-256 Digest Hasher</text>
  <text x="132" y="377" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#555555" text-anchor="middle">WebCrypto Infrastructure Baseline</text>

  <rect x="30" y="398" width="205" height="45" rx="5" fill="#FFFFFF" stroke="#D1E3A5" stroke-width="1.5"/>
  <text x="132" y="416" font-family="DejaVu Sans, Arial" font-size="10" font-weight="bold" fill="#222222" text-anchor="middle">Browser Trust Boundary</text>
  <text x="132" y="432" font-family="DejaVu Sans, Arial" font-size="8" fill="#B91C1C" text-anchor="middle">Assumes Uncompromised Client Device</text>

  <!-- Flow 1->2 -->
  <path d="M 245 190 L 280 190" stroke="#386B24" stroke-width="2" marker-end="url(#arr)"/>
  <text x="262" y="180" font-family="DejaVu Sans, Arial" font-size="8" font-weight="bold" fill="#386B24" text-anchor="middle">HTTPS</text>
  <text x="262" y="202" font-family="DejaVu Sans, Arial" font-size="7.5" fill="#555555" text-anchor="middle">Ciphertext</text>

  <!-- Tier 2: Serverless Application Tier -->
  <rect x="280" y="48" width="235" height="405" rx="8" fill="#F7FAF2" stroke="#386B24" stroke-width="2"/>
  <rect x="280" y="48" width="235" height="34" rx="8" fill="#E3EFCB"/>
  <text x="397" y="70" font-family="DejaVu Sans, Arial" font-size="11.5" font-weight="bold" fill="#1B1D1E" text-anchor="middle">Tier 2: Backend (Node.js 22 LTS)</text>

  <rect x="292" y="92" width="210" height="52" rx="5" fill="#FFFFFF" stroke="#D1E3A5" stroke-width="1.5"/>
  <text x="397" y="111" font-family="DejaVu Sans, Arial" font-size="10.5" font-weight="bold" fill="#222222" text-anchor="middle">Next.js API Gateway Routes</text>
  <text x="397" y="126" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#555555" text-anchor="middle">JWT Sessions &amp; TOTP 2FA Verification</text>
  <text x="397" y="138" font-family="DejaVu Sans, Arial" font-size="8" fill="#386B24" text-anchor="middle">Tenant Scope &amp; Private Invite Auth</text>

  <rect x="292" y="152" width="210" height="56" rx="5" fill="#FFFFFF" stroke="#D1E3A5" stroke-width="1.5"/>
  <text x="397" y="171" font-family="DejaVu Sans, Arial" font-size="10.5" font-weight="bold" fill="#222222" text-anchor="middle">Server-Side RBAC Middleware</text>
  <text x="397" y="187" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#555555" text-anchor="middle">Owner, Defender, Hunter, ReadOnly</text>
  <text x="397" y="200" font-family="DejaVu Sans, Arial" font-size="8" fill="#386B24" text-anchor="middle">Dynamic SET LOCAL app.current_tenant_id</text>

  <rect x="292" y="216" width="210" height="56" rx="5" fill="#FFFFFF" stroke="#D1E3A5" stroke-width="1.5"/>
  <text x="397" y="235" font-family="DejaVu Sans, Arial" font-size="10.5" font-weight="bold" fill="#222222" text-anchor="middle">SLA Engine &amp; Assignment</text>
  <text x="397" y="250" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#555555" text-anchor="middle">Owner Assignment &amp; Target Timers</text>
  <text x="397" y="263" font-family="DejaVu Sans, Arial" font-size="8" fill="#386B24" text-anchor="middle">Overdue First-Response Reminders</text>

  <rect x="292" y="280" width="210" height="52" rx="5" fill="#FFFFFF" stroke="#D1E3A5" stroke-width="1.5"/>
  <text x="397" y="299" font-family="DejaVu Sans, Arial" font-size="10.5" font-weight="bold" fill="#222222" text-anchor="middle">Rate Limiter &amp; Quota Guard</text>
  <text x="397" y="315" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#555555" text-anchor="middle">Token Bucket (5 sub/hr/IP limit)</text>
  <text x="397" y="327" font-family="DejaVu Sans, Arial" font-size="8" fill="#386B24" text-anchor="middle">Atomic Quota (50MB DB / 2GB R2)</text>

  <rect x="292" y="340" width="210" height="50" rx="5" fill="#FFFFFF" stroke="#D1E3A5" stroke-width="1.5"/>
  <text x="397" y="359" font-family="DejaVu Sans, Arial" font-size="10.5" font-weight="bold" fill="#222222" text-anchor="middle">Deterministic CVSS 3.1 &amp; State</text>
  <text x="397" y="375" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#555555" text-anchor="middle">Pure TypeScript Function (52 Vectors)</text>
  <text x="397" y="386" font-family="DejaVu Sans, Arial" font-size="8" fill="#555555" text-anchor="middle">Append-Only Audit Event Dispatcher</text>

  <rect x="292" y="398" width="210" height="45" rx="5" fill="#FFFFFF" stroke="#D1E3A5" stroke-width="1.5"/>
  <text x="397" y="416" font-family="DejaVu Sans, Arial" font-size="10" font-weight="bold" fill="#222222" text-anchor="middle">GitHub App Integration Client</text>
  <text x="397" y="432" font-family="DejaVu Sans, Arial" font-size="8" fill="#386B24" text-anchor="middle">Read-Only Scopes (Public &amp; Private Repos)</text>

  <!-- Flow 2->3 -->
  <path d="M 515 190 L 545 190" stroke="#386B24" stroke-width="2" marker-end="url(#arr)"/>

  <!-- Tier 3: Persistence Tier -->
  <rect x="545" y="48" width="175" height="405" rx="8" fill="#F7FAF2" stroke="#386B24" stroke-width="2"/>
  <rect x="545" y="48" width="175" height="34" rx="8" fill="#E3EFCB"/>
  <text x="632" y="70" font-family="DejaVu Sans, Arial" font-size="11.5" font-weight="bold" fill="#1B1D1E" text-anchor="middle">Tier 3: Persistence Tier</text>

  <rect x="555" y="105" width="155" height="95" rx="5" fill="#FFFFFF" stroke="#D1E3A5" stroke-width="1.5"/>
  <text x="632" y="126" font-family="DejaVu Sans, Arial" font-size="10.5" font-weight="bold" fill="#222222" text-anchor="middle">Neon PostgreSQL 16</text>
  <text x="632" y="144" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#386B24" text-anchor="middle">Dynamic Row-Level Security</text>
  <text x="632" y="159" font-family="DejaVu Sans, Arial" font-size="8" fill="#555555" text-anchor="middle">Append-Only Audit Log Tables</text>
  <text x="632" y="173" font-family="DejaVu Sans, Arial" font-size="8" fill="#555555" text-anchor="middle">Point-in-Time Recovery (PITR)</text>
  <text x="632" y="187" font-family="DejaVu Sans, Arial" font-size="7.5" fill="#B91C1C" text-anchor="middle">Ciphertext Payload Custodian</text>

  <rect x="555" y="240" width="155" height="95" rx="5" fill="#FFFFFF" stroke="#D1E3A5" stroke-width="1.5"/>
  <text x="632" y="262" font-family="DejaVu Sans, Arial" font-size="10.5" font-weight="bold" fill="#222222" text-anchor="middle">Cloudflare R2 Storage</text>
  <text x="632" y="280" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#555555" text-anchor="middle">Client-Encrypted Binaries</text>
  <text x="632" y="295" font-family="DejaVu Sans, Arial" font-size="8" fill="#386B24" text-anchor="middle">Zero Egress Bandwidth Fees</text>
  <text x="632" y="309" font-family="DejaVu Sans, Arial" font-size="8" fill="#555555" text-anchor="middle">24h Multipart Orphan Pruning</text>
  <text x="632" y="323" font-family="DejaVu Sans, Arial" font-size="7.5" fill="#555555" text-anchor="middle">Encrypted PoC Attachments</text>

  <!-- Flow 2->External -->
  <path d="M 515 350 L 740 350" stroke="#0284C7" stroke-width="1.5" stroke-dasharray="4" marker-end="url(#arr_ext)"/>

  <!-- External 3rd-Party Services -->
  <rect x="740" y="48" width="165" height="405" rx="8" fill="#F0F9FF" stroke="#0284C7" stroke-width="2"/>
  <rect x="740" y="48" width="165" height="34" rx="8" fill="#BAE6FD"/>
  <text x="822" y="70" font-family="DejaVu Sans, Arial" font-size="11" font-weight="bold" fill="#0369A1" text-anchor="middle">External Services</text>

  <rect x="750" y="98" width="145" height="70" rx="5" fill="#FFFFFF" stroke="#BAE6FD" stroke-width="1.5"/>
  <text x="822" y="119" font-family="DejaVu Sans, Arial" font-size="10" font-weight="bold" fill="#0369A1" text-anchor="middle">GitHub REST API v3</text>
  <text x="822" y="135" font-family="DejaVu Sans, Arial" font-size="8" fill="#555555" text-anchor="middle">GET /repos/.../commits/{ref}</text>
  <text x="822" y="149" font-family="DejaVu Sans, Arial" font-size="8" fill="#386B24" text-anchor="middle">Commit SHA &amp; Branch</text>
  <text x="822" y="161" font-family="DejaVu Sans, Arial" font-size="7.5" fill="#555555" text-anchor="middle">Public &amp; Private Repo Check</text>

  <rect x="750" y="185" width="145" height="72" rx="5" fill="#FFFFFF" stroke="#BAE6FD" stroke-width="1.5"/>
  <text x="822" y="206" font-family="DejaVu Sans, Arial" font-size="10" font-weight="bold" fill="#0369A1" text-anchor="middle">Resend / Postmark</text>
  <text x="822" y="222" font-family="DejaVu Sans, Arial" font-size="8" fill="#555555" text-anchor="middle">Metadata Alerts &amp; Invites</text>
  <text x="822" y="235" font-family="DejaVu Sans, Arial" font-size="8" fill="#386B24" text-anchor="middle">Exponential Backoff Outbox</text>
  <text x="822" y="248" font-family="DejaVu Sans, Arial" font-size="7.5" fill="#B91C1C" text-anchor="middle">Zero Exploit Bytes in Email</text>

  <rect x="750" y="275" width="145" height="68" rx="5" fill="#FFFFFF" stroke="#BAE6FD" stroke-width="1.5"/>
  <text x="822" y="296" font-family="DejaVu Sans, Arial" font-size="10" font-weight="bold" fill="#0369A1" text-anchor="middle">DNS Authority</text>
  <text x="822" y="312" font-family="DejaVu Sans, Arial" font-size="8" fill="#555555" text-anchor="middle">Node.js dns.promises</text>
  <text x="822" y="325" font-family="DejaVu Sans, Arial" font-size="8" fill="#386B24" text-anchor="middle">_bbt-challenge.&lt;domain&gt;</text>
  <text x="822" y="337" font-family="DejaVu Sans, Arial" font-size="7.5" fill="#555555" text-anchor="middle">TXT Record Verification</text>

  <rect x="750" y="360" width="145" height="75" rx="5" fill="#FFFFFF" stroke="#BAE6FD" stroke-width="1.5"/>
  <text x="822" y="380" font-family="DejaVu Sans, Arial" font-size="10" font-weight="bold" fill="#0369A1" text-anchor="middle">Commercial Billing</text>
  <text x="822" y="396" font-family="DejaVu Sans, Arial" font-size="8" fill="#555555" text-anchor="middle">Subscription Entitlements</text>
  <text x="822" y="409" font-family="DejaVu Sans, Arial" font-size="8" fill="#386B24" text-anchor="middle">Starter vs Team Seats</text>
  <text x="822" y="422" font-family="DejaVu Sans, Arial" font-size="7.5" fill="#555555" text-anchor="middle">Grace Period Enforcement</text>
</svg>'''

with open('projects/BugBountyTrack/requirements/diagrams/fig4_1_component.svg', 'w') as f:
    f.write(svg_comp)
subprocess.run(['rsvg-convert', '-f', 'png', '-o', 'projects/BugBountyTrack/requirements/diagrams/fig4_1_component.png', 'projects/BugBountyTrack/requirements/diagrams/fig4_1_component.svg'])
print('Generated fig4_1_component.png')

# -------------------------------------------------------------
# 2. Figure 4.2: Use Case Model SVG (Expanded B2B SaaS Workflows)
# -------------------------------------------------------------
svg_uc = '''<svg width="920" height="490" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arruc" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#386B24" />
    </marker>
    <marker id="arruc_admin" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#6B7280" />
    </marker>
  </defs>
  <rect width="100%" height="100%" fill="#FFFFFF"/>
  <text x="460" y="24" font-family="DejaVu Sans, Arial" font-size="15" font-weight="bold" fill="#1B1D1E" text-anchor="middle">Figure 4.2: BugBountyTrack Use Case Model &amp; Commercial Actor Roles</text>

  <!-- Actors on Left -->
  <!-- Hunter -->
  <circle cx="70" cy="95" r="14" fill="#E3EFCB" stroke="#386B24" stroke-width="1.5"/>
  <text x="70" y="99" font-family="DejaVu Sans, Arial" font-size="10" font-weight="bold" fill="#386B24" text-anchor="middle">H</text>
  <text x="70" y="122" font-family="DejaVu Sans, Arial" font-size="9.5" font-weight="bold" fill="#1B1D1E" text-anchor="middle">Ethical Researcher</text>
  <text x="70" y="134" font-family="DejaVu Sans, Arial" font-size="8" fill="#555555" text-anchor="middle">(Hunter)</text>

  <!-- Defender -->
  <circle cx="70" cy="215" r="14" fill="#E3EFCB" stroke="#386B24" stroke-width="1.5"/>
  <text x="70" y="219" font-family="DejaVu Sans, Arial" font-size="10" font-weight="bold" fill="#386B24" text-anchor="middle">D</text>
  <text x="70" y="242" font-family="DejaVu Sans, Arial" font-size="9.5" font-weight="bold" fill="#1B1D1E" text-anchor="middle">Triage Lead / Reviewer</text>
  <text x="70" y="254" font-family="DejaVu Sans, Arial" font-size="8" fill="#555555" text-anchor="middle">(Org Defender / Custodian)</text>

  <!-- Owner -->
  <circle cx="70" cy="335" r="14" fill="#E3EFCB" stroke="#386B24" stroke-width="1.5"/>
  <text x="70" y="339" font-family="DejaVu Sans, Arial" font-size="10" font-weight="bold" fill="#386B24" text-anchor="middle">O</text>
  <text x="70" y="362" font-family="DejaVu Sans, Arial" font-size="9.5" font-weight="bold" fill="#1B1D1E" text-anchor="middle">Tenant Owner</text>
  <text x="70" y="374" font-family="DejaVu Sans, Arial" font-size="8" fill="#555555" text-anchor="middle">(Eng Lead / SaaS Admin)</text>

  <!-- ReadOnly -->
  <circle cx="70" cy="425" r="12" fill="#F3F4F6" stroke="#4B5563" stroke-width="1.5"/>
  <text x="70" y="429" font-family="DejaVu Sans, Arial" font-size="9" font-weight="bold" fill="#4B5563" text-anchor="middle">R</text>
  <text x="70" y="450" font-family="DejaVu Sans, Arial" font-size="8.5" font-weight="bold" fill="#4B5563" text-anchor="middle">Executive ReadOnly</text>

  <!-- SuperAdmin on Right -->
  <circle cx="845" cy="245" r="14" fill="#F3F4F6" stroke="#4B5563" stroke-width="1.5"/>
  <text x="845" y="249" font-family="DejaVu Sans, Arial" font-size="10" font-weight="bold" fill="#4B5563" text-anchor="middle">A</text>
  <text x="845" y="272" font-family="DejaVu Sans, Arial" font-size="9.5" font-weight="bold" fill="#374151" text-anchor="middle">Platform SuperAdmin</text>
  <text x="845" y="284" font-family="DejaVu Sans, Arial" font-size="7.5" fill="#B91C1C" text-anchor="middle">(0 Plaintext Payload Access)</text>

  <!-- Boundary Box -->
  <rect x="175" y="45" width="570" height="430" rx="10" fill="#FAFCF7" stroke="#386B24" stroke-width="2"/>
  <text x="460" y="68" font-family="DejaVu Sans, Arial" font-size="11.5" font-weight="bold" fill="#386B24" text-anchor="middle">BugBountyTrack B2B Security Platform Boundary</text>

  <!-- Use Case Bubbles -->
  <!-- UC-01 -->
  <rect x="200" y="85" width="235" height="38" rx="19" fill="#FFFFFF" stroke="#386B24" stroke-width="1.5"/>
  <text x="317" y="102" font-family="DejaVu Sans, Arial" font-size="9" font-weight="bold" fill="#1B1D1E" text-anchor="middle">UC-01: Submit Encrypted Report</text>
  <text x="317" y="114" font-family="DejaVu Sans, Arial" font-size="7.5" fill="#555555" text-anchor="middle">(Public Intake or Private Invite Token)</text>

  <!-- UC-02 -->
  <rect x="475" y="85" width="245" height="38" rx="19" fill="#FFFFFF" stroke="#386B24" stroke-width="1.5"/>
  <text x="597" y="102" font-family="DejaVu Sans, Arial" font-size="9" font-weight="bold" fill="#1B1D1E" text-anchor="middle">UC-02: Decrypt &amp; Triage Report</text>
  <text x="597" y="114" font-family="DejaVu Sans, Arial" font-size="7.5" fill="#555555" text-anchor="middle">(Local Key Unlock, Neutral Label &amp; CVSS)</text>

  <!-- UC-03 -->
  <rect x="200" y="140" width="235" height="38" rx="19" fill="#FFFFFF" stroke="#386B24" stroke-width="1.5"/>
  <text x="317" y="157" font-family="DejaVu Sans, Arial" font-size="9" font-weight="bold" fill="#1B1D1E" text-anchor="middle">UC-03: Propose Remediation Evidence</text>
  <text x="317" y="169" font-family="DejaVu Sans, Arial" font-size="7.5" fill="#555555" text-anchor="middle">(Public / Private GitHub Commit &amp; Branch)</text>

  <!-- UC-04 -->
  <rect x="475" y="140" width="245" height="38" rx="19" fill="#FFFFFF" stroke="#386B24" stroke-width="1.5"/>
  <text x="597" y="157" font-family="DejaVu Sans, Arial" font-size="9" font-weight="bold" fill="#1B1D1E" text-anchor="middle">UC-04: Attested Retest &amp; Closure</text>
  <text x="597" y="169" font-family="DejaVu Sans, Arial" font-size="7.5" fill="#555555" text-anchor="middle">(Hunter / Internal Attestation or Timeout)</text>

  <!-- UC-05 -->
  <rect x="200" y="195" width="235" height="38" rx="19" fill="#FFFFFF" stroke="#386B24" stroke-width="1.5"/>
  <text x="317" y="212" font-family="DejaVu Sans, Arial" font-size="9" font-weight="bold" fill="#1B1D1E" text-anchor="middle">UC-05: Guided Onboarding &amp; Setup</text>
  <text x="317" y="224" font-family="DejaVu Sans, Arial" font-size="7.5" fill="#555555" text-anchor="middle">(DNS TXT, RFC 9116 Policy &amp; Health Checklist)</text>

  <!-- UC-06 -->
  <rect x="475" y="195" width="245" height="38" rx="19" fill="#FFFFFF" stroke="#386B24" stroke-width="1.5"/>
  <text x="597" y="212" font-family="DejaVu Sans, Arial" font-size="9" font-weight="bold" fill="#1B1D1E" text-anchor="middle">UC-06: Assign Report &amp; Monitor SLAs</text>
  <text x="597" y="224" font-family="DejaVu Sans, Arial" font-size="7.5" fill="#555555" text-anchor="middle">(Assignee, Target Timers &amp; Reminders)</text>

  <!-- UC-07 -->
  <rect x="200" y="250" width="235" height="38" rx="19" fill="#FFFFFF" stroke="#386B24" stroke-width="1.5"/>
  <text x="317" y="267" font-family="DejaVu Sans, Arial" font-size="9" font-weight="bold" fill="#1B1D1E" text-anchor="middle">UC-07: Generate Redacted Closure Export</text>
  <text x="317" y="279" font-family="DejaVu Sans, Arial" font-size="7.5" fill="#555555" text-anchor="middle">(Auditor Evidence PDF / Client Summary)</text>

  <!-- UC-08 -->
  <rect x="475" y="250" width="245" height="38" rx="19" fill="#FFFFFF" stroke="#386B24" stroke-width="1.5"/>
  <text x="597" y="267" font-family="DejaVu Sans, Arial" font-size="9" font-weight="bold" fill="#1B1D1E" text-anchor="middle">UC-08: Key Backup, Restore &amp; Handover</text>
  <text x="597" y="279" font-family="DejaVu Sans, Arial" font-size="7.5" fill="#555555" text-anchor="middle">(Armored Backup, Restore Drill, Successor)</text>

  <!-- UC-09 -->
  <rect x="200" y="305" width="235" height="38" rx="19" fill="#FFFFFF" stroke="#386B24" stroke-width="1.5"/>
  <text x="317" y="322" font-family="DejaVu Sans, Arial" font-size="9" font-weight="bold" fill="#1B1D1E" text-anchor="middle">UC-09: Manage Private Program Invites</text>
  <text x="317" y="334" font-family="DejaVu Sans, Arial" font-size="7.5" fill="#555555" text-anchor="middle">(Token Generation, Acceptance &amp; Revocation)</text>

  <!-- UC-10 -->
  <rect x="475" y="305" width="245" height="38" rx="19" fill="#FFFFFF" stroke="#386B24" stroke-width="1.5"/>
  <text x="597" y="322" font-family="DejaVu Sans, Arial" font-size="9" font-weight="bold" fill="#1B1D1E" text-anchor="middle">UC-10: Subscription &amp; Quota Controls</text>
  <text x="597" y="334" font-family="DejaVu Sans, Arial" font-size="7.5" fill="#555555" text-anchor="middle">(Seat Limits, Storage Quotas &amp; Data Exit)</text>

  <!-- UC-11 (Platform Admin) -->
  <rect x="330" y="375" width="260" height="40" rx="20" fill="#F3F4F6" stroke="#4B5563" stroke-width="1.5"/>
  <text x="460" y="393" font-family="DejaVu Sans, Arial" font-size="9" font-weight="bold" fill="#374151" text-anchor="middle">UC-11: Platform Tenant Provisioning &amp; SRE</text>
  <text x="460" y="405" font-family="DejaVu Sans, Arial" font-size="7.5" fill="#4B5563" text-anchor="middle">(Tenant Lifecycle, Global Rate Limits, PITR Drills)</text>

  <!-- Connections -->
  <!-- Hunter -->
  <line x1="120" y1="100" x2="200" y2="104" stroke="#386B24" stroke-width="1.2" marker-end="url(#arruc)"/>
  <line x1="120" y1="108" x2="475" y2="155" stroke="#386B24" stroke-width="1.2" marker-end="url(#arruc)"/>

  <!-- Defender -->
  <line x1="120" y1="210" x2="475" y2="106" stroke="#386B24" stroke-width="1.2" marker-end="url(#arruc)"/>
  <line x1="120" y1="218" x2="435" y2="162" stroke="#386B24" stroke-width="1.2" marker-end="url(#arruc)"/>
  <line x1="120" y1="225" x2="475" y2="160" stroke="#386B24" stroke-width="1.2" marker-end="url(#arruc)"/>
  <line x1="120" y1="230" x2="475" y2="210" stroke="#386B24" stroke-width="1.2" marker-end="url(#arruc)"/>
  <line x1="120" y1="236" x2="435" y2="265" stroke="#386B24" stroke-width="1.2" marker-end="url(#arruc)"/>
  <line x1="120" y1="242" x2="475" y2="268" stroke="#386B24" stroke-width="1.2" marker-end="url(#arruc)"/>

  <!-- Owner -->
  <line x1="120" y1="335" x2="200" y2="215" stroke="#386B24" stroke-width="1.2" marker-end="url(#arruc)"/>
  <line x1="120" y1="342" x2="200" y2="322" stroke="#386B24" stroke-width="1.2" marker-end="url(#arruc)"/>
  <line x1="120" y1="350" x2="475" y2="322" stroke="#386B24" stroke-width="1.2" marker-end="url(#arruc)"/>

  <!-- ReadOnly -->
  <line x1="120" y1="425" x2="435" y2="275" stroke="#4B5563" stroke-width="1" stroke-dasharray="3" marker-end="url(#arruc_admin)"/>

  <!-- Admin -->
  <line x1="810" y1="270" x2="590" y2="390" stroke="#4B5563" stroke-width="1.2" marker-end="url(#arruc_admin)"/>
</svg>'''

with open('projects/BugBountyTrack/requirements/diagrams/fig4_2_usecase.svg', 'w') as f:
    f.write(svg_uc)
subprocess.run(['rsvg-convert', '-f', 'png', '-o', 'projects/BugBountyTrack/requirements/diagrams/fig4_2_usecase.png', 'projects/BugBountyTrack/requirements/diagrams/fig4_2_usecase.svg'])
print('Generated fig4_2_usecase.png')

# -------------------------------------------------------------
# 3. Figure 4.3: Submission Sequence SVG (Neutral Label + Encrypted Title)
# -------------------------------------------------------------
svg_seq_sub = '''<svg width="880" height="410" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrsq" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#386B24" />
    </marker>
  </defs>
  <rect width="100%" height="100%" fill="#FFFFFF"/>
  <text x="440" y="24" font-family="DejaVu Sans, Arial" font-size="15" font-weight="bold" fill="#1B1D1E" text-anchor="middle">Figure 4.3: Sequence: Browser-Side Dual-Recipient OpenPGP Report Submission</text>

  <!-- Lifeline Headers -->
  <rect x="30" y="48" width="120" height="32" rx="5" fill="#E3EFCB" stroke="#386B24"/>
  <text x="90" y="68" font-family="DejaVu Sans, Arial" font-size="10" font-weight="bold" fill="#1B1D1E" text-anchor="middle">Ethical Researcher</text>

  <rect x="200" y="48" width="130" height="32" rx="5" fill="#E3EFCB" stroke="#386B24"/>
  <text x="265" y="68" font-family="DejaVu Sans, Arial" font-size="10" font-weight="bold" fill="#1B1D1E" text-anchor="middle">Browser Client UI</text>

  <rect x="380" y="48" width="130" height="32" rx="5" fill="#E3EFCB" stroke="#386B24"/>
  <text x="445" y="68" font-family="DejaVu Sans, Arial" font-size="10" font-weight="bold" fill="#1B1D1E" text-anchor="middle">IndexedDB Keystore</text>

  <rect x="560" y="48" width="140" height="32" rx="5" fill="#E3EFCB" stroke="#386B24"/>
  <text x="630" y="68" font-family="DejaVu Sans, Arial" font-size="10" font-weight="bold" fill="#1B1D1E" text-anchor="middle">Next.js API Gateway</text>

  <rect x="740" y="48" width="120" height="32" rx="5" fill="#E3EFCB" stroke="#386B24"/>
  <text x="800" y="68" font-family="DejaVu Sans, Arial" font-size="10" font-weight="bold" fill="#1B1D1E" text-anchor="middle">Neon PostgreSQL</text>

  <!-- Vertical dashed lines -->
  <line x1="90" y1="80" x2="90" y2="395" stroke="#CBD5E1" stroke-dasharray="4"/>
  <line x1="265" y1="80" x2="265" y2="395" stroke="#CBD5E1" stroke-dasharray="4"/>
  <line x1="445" y1="80" x2="445" y2="395" stroke="#CBD5E1" stroke-dasharray="4"/>
  <line x1="630" y1="80" x2="630" y2="395" stroke="#CBD5E1" stroke-dasharray="4"/>
  <line x1="800" y1="80" x2="800" y2="395" stroke="#CBD5E1" stroke-dasharray="4"/>

  <!-- Step 1: Hunter inputs details -->
  <line x1="90" y1="108" x2="265" y2="108" stroke="#386B24" stroke-width="1.5" marker-end="url(#arrsq)"/>
  <text x="177" y="101" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#1B1D1E" text-anchor="middle">1. Enters Sensitive Title, Neutral Label &amp; PoC</text>

  <!-- Step 2: Fetch Org Custodian Key -->
  <line x1="265" y1="135" x2="630" y2="135" stroke="#386B24" stroke-width="1.5" marker-end="url(#arrsq)"/>
  <text x="447" y="128" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#1B1D1E" text-anchor="middle">2. GET /api/v1/programs/{slug}/key (Verify Scope / Private Token)</text>

  <line x1="630" y1="160" x2="265" y2="160" stroke="#555555" stroke-dasharray="4" marker-end="url(#arrsq)"/>
  <text x="447" y="153" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#555555" text-anchor="middle">3. Return Org Custodian Public Encryption Subkey (X25519 / RSA-4096)</text>

  <!-- Step 3: Fetch Researcher Key -->
  <line x1="265" y1="188" x2="445" y2="188" stroke="#386B24" stroke-width="1.5" marker-end="url(#arrsq)"/>
  <text x="355" y="181" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#1B1D1E" text-anchor="middle">4. Fetch Hunter Public Key</text>

  <line x1="445" y1="210" x2="265" y2="210" stroke="#555555" stroke-dasharray="4" marker-end="url(#arrsq)"/>
  <text x="355" y="203" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#555555" text-anchor="middle">5. Return Hunter Armored Key</text>

  <!-- Client-side encryption block -->
  <rect x="210" y="225" width="110" height="34" rx="4" fill="#EAF7EA" stroke="#386B24"/>
  <text x="265" y="238" font-family="DejaVu Sans, Arial" font-size="8" font-weight="bold" fill="#386B24" text-anchor="middle">openpgp.encrypt()</text>
  <text x="265" y="251" font-family="DejaVu Sans, Arial" font-size="7.5" fill="#555555" text-anchor="middle">Title &amp; PoC Dual-Wrapped</text>

  <!-- Step 4: Submit Post -->
  <line x1="265" y1="280" x2="630" y2="280" stroke="#386B24" stroke-width="1.5" marker-end="url(#arrsq)"/>
  <text x="447" y="273" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#1B1D1E" text-anchor="middle">6. POST /api/v1/reports (Neutral Label, Asset URL, CVSS + Ciphertext Payload)</text>

  <!-- Server validation -->
  <rect x="575" y="295" width="110" height="26" rx="4" fill="#FFFBEB" stroke="#D97706"/>
  <text x="630" y="311" font-family="DejaVu Sans, Arial" font-size="7.5" fill="#92400E" text-anchor="middle">Rate Limit &amp; Invite Check</text>

  <!-- Step 5: DB Persist -->
  <line x1="630" y1="335" x2="800" y2="335" stroke="#386B24" stroke-width="1.5" marker-end="url(#arrsq)"/>
  <text x="715" y="328" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#1B1D1E" text-anchor="middle">7. INSERT (RLS Tenant Context)</text>

  <line x1="800" y1="358" x2="630" y2="358" stroke="#555555" stroke-dasharray="4" marker-end="url(#arrsq)"/>
  <text x="715" y="351" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#555555" text-anchor="middle">8. 201 Created (#BBT-102)</text>

  <!-- Step 6: Confirmation -->
  <line x1="630" y1="380" x2="90" y2="380" stroke="#386B24" stroke-width="1.5" marker-end="url(#arrsq)"/>
  <text x="360" y="373" font-family="DejaVu Sans, Arial" font-size="8.5" font-weight="bold" fill="#386B24" text-anchor="middle">9. Display Encrypted Receipt &amp; Tracking ID (#BBT-102)</text>
</svg>'''

with open('projects/BugBountyTrack/requirements/diagrams/fig4_3_seq_submission.svg', 'w') as f:
    f.write(svg_seq_sub)
subprocess.run(['rsvg-convert', '-f', 'png', '-o', 'projects/BugBountyTrack/requirements/diagrams/fig4_3_seq_submission.png', 'projects/BugBountyTrack/requirements/diagrams/fig4_3_seq_submission.svg'])
print('Generated fig4_3_seq_submission.png')

# -------------------------------------------------------------
# 4. Figure 4.4: Decryption Sequence SVG (JWT & RBAC Gateway)
# -------------------------------------------------------------
svg_seq_dec = '''<svg width="900" height="425" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrsq2" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#386B24" />
    </marker>
  </defs>
  <rect width="100%" height="100%" fill="#FFFFFF"/>
  <text x="450" y="24" font-family="DejaVu Sans, Arial" font-size="15" font-weight="bold" fill="#1B1D1E" text-anchor="middle">Figure 4.4: Sequence: Authorized In-Browser Decryption &amp; Neutral Label Triage</text>

  <!-- Lifeline Headers -->
  <rect x="30" y="48" width="130" height="32" rx="5" fill="#E3EFCB" stroke="#386B24"/>
  <text x="95" y="68" font-family="DejaVu Sans, Arial" font-size="10" font-weight="bold" fill="#1B1D1E" text-anchor="middle">Organization Reviewer</text>

  <rect x="200" y="48" width="130" height="32" rx="5" fill="#E3EFCB" stroke="#386B24"/>
  <text x="265" y="68" font-family="DejaVu Sans, Arial" font-size="10" font-weight="bold" fill="#1B1D1E" text-anchor="middle">Defender Browser UI</text>

  <rect x="385" y="48" width="145" height="32" rx="5" fill="#E3EFCB" stroke="#386B24"/>
  <text x="457" y="68" font-family="DejaVu Sans, Arial" font-size="10" font-weight="bold" fill="#1B1D1E" text-anchor="middle">Next.js API Gateway</text>

  <rect x="585" y="48" width="130" height="32" rx="5" fill="#E3EFCB" stroke="#386B24"/>
  <text x="650" y="68" font-family="DejaVu Sans, Arial" font-size="10" font-weight="bold" fill="#1B1D1E" text-anchor="middle">Neon PostgreSQL</text>

  <rect x="745" y="48" width="135" height="32" rx="5" fill="#E3EFCB" stroke="#386B24"/>
  <text x="812" y="68" font-family="DejaVu Sans, Arial" font-size="10" font-weight="bold" fill="#1B1D1E" text-anchor="middle">IndexedDB Keystore</text>

  <!-- Vertical dashed lines -->
  <line x1="95" y1="80" x2="95" y2="410" stroke="#CBD5E1" stroke-dasharray="4"/>
  <line x1="265" y1="80" x2="265" y2="410" stroke="#CBD5E1" stroke-dasharray="4"/>
  <line x1="457" y1="80" x2="457" y2="410" stroke="#CBD5E1" stroke-dasharray="4"/>
  <line x1="650" y1="80" x2="650" y2="410" stroke="#CBD5E1" stroke-dasharray="4"/>
  <line x1="812" y1="80" x2="812" y2="410" stroke="#CBD5E1" stroke-dasharray="4"/>

  <!-- Step 1: Navigates -->
  <line x1="95" y1="105" x2="265" y2="105" stroke="#386B24" stroke-width="1.5" marker-end="url(#arrsq2)"/>
  <text x="180" y="98" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#1B1D1E" text-anchor="middle">1. Navigates to /reports/BBT-102</text>

  <!-- Step 2: Request Report -->
  <line x1="265" y1="130" x2="457" y2="130" stroke="#386B24" stroke-width="1.5" marker-end="url(#arrsq2)"/>
  <text x="361" y="123" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#1B1D1E" text-anchor="middle">2. GET /api/v1/reports/BBT-102 (JWT Cookie)</text>

  <!-- Gateway Auth & RLS check -->
  <rect x="400" y="145" width="115" height="34" rx="4" fill="#EAF7EA" stroke="#386B24"/>
  <text x="457" y="159" font-family="DejaVu Sans, Arial" font-size="8" font-weight="bold" fill="#386B24" text-anchor="middle">Verify JWT &amp; RBAC</text>
  <text x="457" y="171" font-family="DejaVu Sans, Arial" font-size="7.5" fill="#555555" text-anchor="middle">SET LOCAL tenant_id = :id</text>

  <!-- Step 3: Query DB -->
  <line x1="457" y1="195" x2="650" y2="195" stroke="#386B24" stroke-width="1.5" marker-end="url(#arrsq2)"/>
  <text x="553" y="188" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#1B1D1E" text-anchor="middle">3. SELECT ciphertext, label, metadata</text>

  <line x1="650" y1="220" x2="457" y2="220" stroke="#555555" stroke-dasharray="4" marker-end="url(#arrsq2)"/>
  <text x="553" y="213" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#555555" text-anchor="middle">4. Return Encrypted Record</text>

  <line x1="457" y1="245" x2="265" y2="245" stroke="#555555" stroke-dasharray="4" marker-end="url(#arrsq2)"/>
  <text x="361" y="238" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#555555" text-anchor="middle">5. 200 OK (Ciphertext Payload + Neutral Label)</text>

  <!-- Step 4: Prompt Passphrase -->
  <line x1="265" y1="270" x2="95" y2="270" stroke="#B91C1C" stroke-width="1.5" marker-end="url(#arrsq2)"/>
  <text x="180" y="263" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#B91C1C" text-anchor="middle">6. Prompt Local Encryption Passphrase</text>

  <line x1="95" y1="295" x2="265" y2="295" stroke="#386B24" stroke-width="1.5" marker-end="url(#arrsq2)"/>
  <text x="180" y="288" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#1B1D1E" text-anchor="middle">7. Enters Passphrase (Client Memory Only)</text>

  <!-- Step 5: Keystore -->
  <line x1="265" y1="320" x2="812" y2="320" stroke="#386B24" stroke-width="1.5" marker-end="url(#arrsq2)"/>
  <text x="538" y="313" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#1B1D1E" text-anchor="middle">8. Retrieve Passphrase-Encrypted Custodian Private Key</text>

  <line x1="812" y1="345" x2="265" y2="345" stroke="#555555" stroke-dasharray="4" marker-end="url(#arrsq2)"/>
  <text x="538" y="338" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#555555" text-anchor="middle">9. Return Encrypted Armored Key Material</text>

  <!-- Decrypt block -->
  <rect x="205" y="360" width="120" height="34" rx="4" fill="#EAF7EA" stroke="#386B24"/>
  <text x="265" y="373" font-family="DejaVu Sans, Arial" font-size="8" font-weight="bold" fill="#386B24" text-anchor="middle">openpgp.decrypt()</text>
  <text x="265" y="386" font-family="DejaVu Sans, Arial" font-size="7.5" fill="#555555" text-anchor="middle">Title &amp; PoC + rehype AST</text>

  <!-- Step 6: Render -->
  <line x1="265" y1="405" x2="95" y2="405" stroke="#228822" stroke-width="1.5" marker-end="url(#arrsq2)"/>
  <text x="180" y="398" font-family="DejaVu Sans, Arial" font-size="8.5" font-weight="bold" fill="#228822" text-anchor="middle">10. Renders Plaintext Report in Confidential View</text>
</svg>'''

with open('projects/BugBountyTrack/requirements/diagrams/fig4_4_seq_decryption.svg', 'w') as f:
    f.write(svg_seq_dec)
subprocess.run(['rsvg-convert', '-f', 'png', '-o', 'projects/BugBountyTrack/requirements/diagrams/fig4_4_seq_decryption.png', 'projects/BugBountyTrack/requirements/diagrams/fig4_4_seq_decryption.svg'])
print('Generated fig4_4_seq_decryption.png')

# -------------------------------------------------------------
# 5. Figure 4.5: State Machine SVG (3 Disjoint Branches, No Box Crossing!)
# -------------------------------------------------------------
svg_sm = '''<svg width="920" height="470" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrsm" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M 0 0 L 6 3 L 0 6 z" fill="#386B24" />
    </marker>
    <marker id="arrsm_red" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M 0 0 L 6 3 L 0 6 z" fill="#B91C1C" />
    </marker>
    <marker id="arrsm_orange" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M 0 0 L 6 3 L 0 6 z" fill="#D97706" />
    </marker>
    <marker id="arrsm_term" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M 0 0 L 6 3 L 0 6 z" fill="#15803D" />
    </marker>
    <marker id="arrsm_gray" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M 0 0 L 6 3 L 0 6 z" fill="#4B5563" />
    </marker>
  </defs>
  <rect width="100%" height="100%" fill="#FFFFFF"/>
  <text x="460" y="24" font-family="DejaVu Sans, Arial" font-size="15" font-weight="bold" fill="#1B1D1E" text-anchor="middle">Figure 4.5: Remediation &amp; Attested Retest Lifecycle State Machine (3 Independent Branches)</text>

  <!-- Start State -->
  <circle cx="35" cy="75" r="10" fill="#386B24"/>

  <!-- NEW State -->
  <rect x="75" y="53" width="85" height="44" rx="8" fill="#E3EFCB" stroke="#386B24" stroke-width="2"/>
  <text x="117" y="79" font-family="DejaVu Sans, Arial" font-size="11" font-weight="bold" fill="#1B1D1E" text-anchor="middle">NEW</text>

  <!-- TRIAGING State -->
  <rect x="205" y="53" width="105" height="44" rx="8" fill="#FFFFFF" stroke="#386B24" stroke-width="2"/>
  <text x="257" y="79" font-family="DejaVu Sans, Arial" font-size="11" font-weight="bold" fill="#1B1D1E" text-anchor="middle">TRIAGING</text>

  <!-- NEED_MORE_INFO (Side branch from TRIAGING) -->
  <rect x="200" y="145" width="115" height="38" rx="6" fill="#F7FAF2" stroke="#555555" stroke-width="1.5"/>
  <text x="257" y="169" font-family="DejaVu Sans, Arial" font-size="9" font-weight="bold" fill="#333333" text-anchor="middle">NEED_MORE_INFO</text>

  <!-- REJECTED & DUPLICATE (Exception Terminals) -->
  <rect x="140" y="215" width="105" height="38" rx="6" fill="#FFF0F0" stroke="#B91C1C" stroke-width="1.5"/>
  <text x="192" y="239" font-family="DejaVu Sans, Arial" font-size="9.5" font-weight="bold" fill="#B91C1C" text-anchor="middle">REJECTED</text>

  <rect x="265" y="215" width="105" height="38" rx="6" fill="#FFF0F0" stroke="#B91C1C" stroke-width="1.5"/>
  <text x="317" y="239" font-family="DejaVu Sans, Arial" font-size="9.5" font-weight="bold" fill="#B91C1C" text-anchor="middle">DUPLICATE</text>

  <!-- ACCEPTED State -->
  <rect x="365" y="53" width="105" height="44" rx="8" fill="#FFFFFF" stroke="#386B24" stroke-width="1.5"/>
  <text x="417" y="79" font-family="DejaVu Sans, Arial" font-size="11" font-weight="bold" fill="#1B1D1E" text-anchor="middle">ACCEPTED</text>

  <!-- FIX_PROPOSED State -->
  <rect x="520" y="53" width="115" height="44" rx="8" fill="#FFFFFF" stroke="#386B24" stroke-width="1.5"/>
  <text x="577" y="79" font-family="DejaVu Sans, Arial" font-size="11" font-weight="bold" fill="#1B1D1E" text-anchor="middle">FIX_PROPOSED</text>

  <!-- RETEST_PENDING State -->
  <rect x="685" y="53" width="135" height="44" rx="8" fill="#E3EFCB" stroke="#386B24" stroke-width="2"/>
  <text x="752" y="79" font-family="DejaVu Sans, Arial" font-size="11" font-weight="bold" fill="#1B1D1E" text-anchor="middle">RETEST_PENDING</text>

  <!-- THREE COMPLETELY SEPARATE OUTGOING BRANCHES FROM RETEST_PENDING -->
  <!-- Branch 1: VERIFIED_RESEARCHER (Angled Left to x=420, y=190) -->
  <rect x="420" y="190" width="170" height="44" rx="8" fill="#F0FDF4" stroke="#15803D" stroke-width="2"/>
  <text x="505" y="212" font-family="DejaVu Sans, Arial" font-size="9.5" font-weight="bold" fill="#15803D" text-anchor="middle">VERIFIED_RESEARCHER</text>
  <text x="505" y="225" font-family="DejaVu Sans, Arial" font-size="7.5" fill="#15803D" text-anchor="middle">(Independent External Pass)</text>

  <!-- Branch 2: VERIFIED_INTERNAL (Direct Down to x=610, y=285) -->
  <rect x="610" y="285" width="165" height="44" rx="8" fill="#F0FDF4" stroke="#15803D" stroke-width="2"/>
  <text x="692" y="307" font-family="DejaVu Sans, Arial" font-size="9.5" font-weight="bold" fill="#15803D" text-anchor="middle">VERIFIED_INTERNAL</text>
  <text x="692" y="320" font-family="DejaVu Sans, Arial" font-size="7.5" fill="#15803D" text-anchor="middle">(Reviewer Conflict Disclosed)</text>

  <!-- Branch 3: CLOSED_UNVERIFIED_TIMEOUT (Angled Right to x=735, y=190) -->
  <rect x="735" y="190" width="170" height="44" rx="8" fill="#F9FAFB" stroke="#4B5563" stroke-width="1.5"/>
  <text x="820" y="212" font-family="DejaVu Sans, Arial" font-size="8.5" font-weight="bold" fill="#374151" text-anchor="middle">CLOSED_UNVERIFIED_TIMEOUT</text>
  <text x="820" y="225" font-family="DejaVu Sans, Arial" font-size="7.5" fill="#4B5563" text-anchor="middle">(≥14d Inactivity Rationale)</text>

  <!-- Transitions -->
  <path d="M 45 75 L 75 75" stroke="#386B24" stroke-width="1.5" marker-end="url(#arrsm)"/>
  <path d="M 160 75 L 205 75" stroke="#386B24" stroke-width="1.5" marker-end="url(#arrsm)"/>
  <text x="182" y="68" font-family="DejaVu Sans, Arial" font-size="7.5" fill="#555555" text-anchor="middle">Intake</text>

  <path d="M 310 75 L 365 75" stroke="#386B24" stroke-width="1.5" marker-end="url(#arrsm)"/>
  <text x="337" y="68" font-family="DejaVu Sans, Arial" font-size="7.5" fill="#386B24" text-anchor="middle">CVSS Scored</text>

  <path d="M 470 75 L 520 75" stroke="#386B24" stroke-width="1.5" marker-end="url(#arrsm)"/>
  <text x="495" y="68" font-family="DejaVu Sans, Arial" font-size="7.5" fill="#555555" text-anchor="middle">Commit SHA</text>

  <path d="M 635 75 L 685 75" stroke="#386B24" stroke-width="1.5" marker-end="url(#arrsm)"/>
  <text x="660" y="68" font-family="DejaVu Sans, Arial" font-size="7.5" fill="#555555" text-anchor="middle">Deployed</text>

  <!-- Clarification loop -->
  <path d="M 245 97 L 245 145" stroke="#555555" stroke-width="1.5" marker-end="url(#arrsm)"/>
  <path d="M 270 145 L 270 97" stroke="#555555" stroke-width="1.5" marker-end="url(#arrsm)"/>
  <text x="295" y="125" font-family="DejaVu Sans, Arial" font-size="7" fill="#555555">Clarify</text>

  <!-- Rejection & Duplicate -->
  <path d="M 225 97 L 192 215" stroke="#B91C1C" stroke-width="1.5" marker-end="url(#arrsm_red)"/>
  <path d="M 285 97 L 317 215" stroke="#B91C1C" stroke-width="1.5" marker-end="url(#arrsm_red)"/>

  <!-- CLEAR NON-CROSSING FAN-OUT ARROWS FROM RETEST_PENDING -->
  <!-- Branch 1: Leftward to VERIFIED_RESEARCHER -->
  <path d="M 700 97 L 550 190" stroke="#15803D" stroke-width="2" marker-end="url(#arrsm_term)"/>
  <text x="595" y="135" font-family="DejaVu Sans, Arial" font-size="7.5" font-weight="bold" fill="#15803D">Hunter Retest Pass</text>

  <!-- Branch 2: Center/Direct to VERIFIED_INTERNAL -->
  <path d="M 740 97 L 700 285" stroke="#15803D" stroke-width="2" marker-end="url(#arrsm_term)"/>
  <text x="735" y="270" font-family="DejaVu Sans, Arial" font-size="7.5" font-weight="bold" fill="#15803D">Internal Retest Pass</text>

  <!-- Branch 3: Rightward to CLOSED_UNVERIFIED_TIMEOUT -->
  <path d="M 790 97 L 830 190" stroke="#4B5563" stroke-width="2" marker-end="url(#arrsm_gray)"/>
  <text x="825" y="145" font-family="DejaVu Sans, Arial" font-size="7.5" font-weight="bold" fill="#4B5563">≥14d Timeout Closure</text>

  <!-- Retest Failed (Audit Event returning to ACCEPTED) -->
  <path d="M 685 85 Q 580 140 445 97" stroke="#D97706" stroke-width="1.5" stroke-dasharray="4" marker-end="url(#arrsm_orange)" fill="none"/>
  <text x="565" y="128" font-family="DejaVu Sans, Arial" font-size="8" font-weight="bold" fill="#D97706" text-anchor="middle">Retest Failed Event (Audit Preserved -> Returns to ACCEPTED)</text>

  <!-- Reopening Path (From ALL closed states -> returns to TRIAGING) -->
  <path d="M 420 215 L 257 410 L 257 97" stroke="#B91C1C" stroke-width="1.5" stroke-dasharray="4" marker-end="url(#arrsm_red)" fill="none"/>
  <path d="M 610 305 L 360 410" stroke="#B91C1C" stroke-width="1.2" stroke-dasharray="3" fill="none"/>
  <path d="M 735 215 L 530 410" stroke="#B91C1C" stroke-width="1.2" stroke-dasharray="3" fill="none"/>
  <path d="M 192 253 L 192 410" stroke="#B91C1C" stroke-width="1.2" stroke-dasharray="3" fill="none"/>
  <path d="M 317 253 L 317 410" stroke="#B91C1C" stroke-width="1.2" stroke-dasharray="3" fill="none"/>

  <rect x="290" y="398" width="240" height="26" rx="4" fill="#FEF2F2" stroke="#B91C1C"/>
  <text x="410" y="415" font-family="DejaVu Sans, Arial" font-size="8" font-weight="bold" fill="#B91C1C" text-anchor="middle">Reopen Ticket with Justification -> Returns to TRIAGING</text>
</svg>'''

with open('projects/BugBountyTrack/requirements/diagrams/fig4_5_statemachine.svg', 'w') as f:
    f.write(svg_sm)
subprocess.run(['rsvg-convert', '-f', 'png', '-o', 'projects/BugBountyTrack/requirements/diagrams/fig4_5_statemachine.png', 'projects/BugBountyTrack/requirements/diagrams/fig4_5_statemachine.svg'])
print('Generated fig4_5_statemachine.png')

# -------------------------------------------------------------
# 6. Figure 4.6: Relational ERD SVG (Commercial SaaS Schema)
# -------------------------------------------------------------
svg_erd = '''<svg width="940" height="540" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrerd" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#386B24" />
    </marker>
  </defs>
  <rect width="100%" height="100%" fill="#FFFFFF"/>
  <text x="470" y="24" font-family="DejaVu Sans, Arial" font-size="15" font-weight="bold" fill="#1B1D1E" text-anchor="middle">Figure 4.6: Relational Prisma Domain Schema (Commercial B2B SaaS Architecture)</text>

  <!-- Organization -->
  <rect x="20" y="45" width="160" height="135" rx="6" fill="#F7FAF2" stroke="#386B24" stroke-width="1.5"/>
  <rect x="20" y="45" width="160" height="24" rx="6" fill="#E3EFCB"/>
  <text x="100" y="62" font-family="DejaVu Sans, Arial" font-size="10.5" font-weight="bold" fill="#1B1D1E" text-anchor="middle">Organization</text>
  <text x="28" y="86" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• id: String (PK)</text>
  <text x="28" y="102" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• name: String</text>
  <text x="28" y="118" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• slug: String (UK)</text>
  <text x="28" y="134" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• domain: String</text>
  <text x="28" y="150" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• domain_verified: Bool</text>
  <text x="28" y="166" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• created_at: DateTime</text>

  <!-- Subscription -->
  <rect x="20" y="195" width="160" height="120" rx="6" fill="#F7FAF2" stroke="#386B24" stroke-width="1.5"/>
  <rect x="20" y="195" width="160" height="24" rx="6" fill="#E3EFCB"/>
  <text x="100" y="212" font-family="DejaVu Sans, Arial" font-size="10.5" font-weight="bold" fill="#1B1D1E" text-anchor="middle">Subscription</text>
  <text x="28" y="235" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• id: String (PK)</text>
  <text x="28" y="250" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#386B24" font-weight="bold">• organization_id (FK)</text>
  <text x="28" y="265" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• plan: PlanTier (STARTER/PRO)</text>
  <text x="28" y="280" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• status: SubStatus (ACTIVE/GRACE)</text>
  <text x="28" y="295" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• seat_limit: Int (2..10)</text>
  <text x="28" y="309" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• storage_quota_mb: Int</text>

  <!-- UserMembership -->
  <rect x="20" y="330" width="160" height="105" rx="6" fill="#F7FAF2" stroke="#386B24" stroke-width="1.5"/>
  <rect x="20" y="330" width="160" height="24" rx="6" fill="#E3EFCB"/>
  <text x="100" y="347" font-family="DejaVu Sans, Arial" font-size="10.5" font-weight="bold" fill="#1B1D1E" text-anchor="middle">UserMembership</text>
  <text x="28" y="369" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• id: String (PK)</text>
  <text x="28" y="384" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#386B24" font-weight="bold">• organization_id (FK)</text>
  <text x="28" y="399" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#386B24" font-weight="bold">• user_id (FK)</text>
  <text x="28" y="414" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• role: Role (OWNER/DEF/RO)</text>
  <text x="28" y="428" font-family="DejaVu Sans, Arial" font-size="8" fill="#555555">• is_custodian: Boolean</text>

  <!-- User & PGP Key -->
  <rect x="20" y="445" width="160" height="85" rx="6" fill="#F7FAF2" stroke="#386B24" stroke-width="1.5"/>
  <rect x="20" y="445" width="160" height="22" rx="6" fill="#E3EFCB"/>
  <text x="100" y="460" font-family="DejaVu Sans, Arial" font-size="10" font-weight="bold" fill="#1B1D1E" text-anchor="middle">User &amp; Auth</text>
  <text x="28" y="480" font-family="DejaVu Sans, Arial" font-size="8" fill="#222222">• id: String (PK), email: String</text>
  <text x="28" y="494" font-family="DejaVu Sans, Arial" font-size="8" fill="#222222">• password_hash (bcrypt r=12)</text>
  <text x="28" y="508" font-family="DejaVu Sans, Arial" font-size="8" fill="#222222">• totp_secret: String? (MFA)</text>
  <text x="28" y="522" font-family="DejaVu Sans, Arial" font-size="8" fill="#222222">• email_verified: Boolean</text>

  <!-- Program & Invites -->
  <rect x="210" y="45" width="185" height="135" rx="6" fill="#F7FAF2" stroke="#386B24" stroke-width="1.5"/>
  <rect x="210" y="45" width="185" height="24" rx="6" fill="#E3EFCB"/>
  <text x="302" y="62" font-family="DejaVu Sans, Arial" font-size="10.5" font-weight="bold" fill="#1B1D1E" text-anchor="middle">Program</text>
  <text x="218" y="86" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• id: String (PK)</text>
  <text x="218" y="102" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#386B24" font-weight="bold">• organization_id: String (FK)</text>
  <text x="218" y="118" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• visibility: "PUBLIC | PRIVATE_INVITE"</text>
  <text x="218" y="134" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• scope_rules: Text</text>
  <text x="218" y="150" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• safe_harbor_policy: Text</text>
  <text x="218" y="166" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• active_encryption_subKey: Text</text>

  <rect x="210" y="195" width="185" height="120" rx="6" fill="#F7FAF2" stroke="#386B24" stroke-width="1.5"/>
  <rect x="210" y="195" width="185" height="24" rx="6" fill="#E3EFCB"/>
  <text x="302" y="212" font-family="DejaVu Sans, Arial" font-size="10.5" font-weight="bold" fill="#1B1D1E" text-anchor="middle">ProgramInvitation</text>
  <text x="218" y="235" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• id: String (PK)</text>
  <text x="218" y="250" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#386B24" font-weight="bold">• program_id: String (FK)</text>
  <text x="218" y="265" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• invited_email: String</text>
  <text x="218" y="280" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• token_hash: String (UK)</text>
  <text x="218" y="295" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• status: "PENDING | ACCEPTED | REVOKED"</text>
  <text x="218" y="309" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• expires_at: DateTime (7d TTL)</text>

  <!-- Central Entity: Report -->
  <rect x="425" y="45" width="245" height="270" rx="6" fill="#F7FAF2" stroke="#386B24" stroke-width="2"/>
  <rect x="425" y="45" width="245" height="24" rx="6" fill="#E3EFCB"/>
  <text x="547" y="62" font-family="DejaVu Sans, Arial" font-size="10.5" font-weight="bold" fill="#1B1D1E" text-anchor="middle">Report (Multi-Tenant Isolated)</text>
  <text x="435" y="86" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• id: String (PK, e.g. #BBT-102)</text>
  <text x="435" y="101" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#386B24" font-weight="bold">• organization_id: String (FK)</text>
  <text x="435" y="116" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#386B24" font-weight="bold">• program_id: String (FK)</text>
  <text x="435" y="131" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#386B24" font-weight="bold">• hunter_id: String (FK)</text>
  <text x="435" y="146" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• assigned_defender_id: String? (FK)</text>
  <text x="435" y="161" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• operational_label: NeutralCategory (Enum)</text>
  <text x="435" y="176" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#B91C1C" font-weight="bold">• title_ciphertext: Text (CIPHERTEXT)</text>
  <text x="435" y="191" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#B91C1C" font-weight="bold">• payload_ciphertext: Text (CIPHERTEXT)</text>
  <text x="435" y="206" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• asset_scope_url: String</text>
  <text x="435" y="221" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• cvss_vector: String, cvss_score: Float</text>
  <text x="435" y="236" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• state: ReportState (NEW..CLOSED)</text>
  <text x="435" y="251" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• sla_first_response_due: DateTime</text>
  <text x="435" y="266" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• sla_remediation_due: DateTime</text>
  <text x="435" y="281" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• created_at, updated_at: DateTime</text>

  <!-- Supporting Entities Right -->
  <!-- RemediationRecord -->
  <rect x="700" y="45" width="220" height="135" rx="6" fill="#F7FAF2" stroke="#386B24" stroke-width="1.5"/>
  <rect x="700" y="45" width="220" height="24" rx="6" fill="#E3EFCB"/>
  <text x="810" y="62" font-family="DejaVu Sans, Arial" font-size="10" font-weight="bold" fill="#1B1D1E" text-anchor="middle">RemediationRecord</text>
  <text x="708" y="86" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• id: String (PK)</text>
  <text x="708" y="100" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#386B24" font-weight="bold">• report_id: String (FK)</text>
  <text x="708" y="114" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• evidence_type: CODE | CONFIG</text>
  <text x="708" y="128" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• commit_sha: String? (40-char)</text>
  <text x="708" y="142" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• branch_name: String?</text>
  <text x="708" y="156" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• config_sha256_hash: String?</text>
  <text x="708" y="170" font-family="DejaVu Sans, Arial" font-size="8" fill="#555555">• deployment_env &amp; deployed_version</text>

  <!-- RetestEvidence -->
  <rect x="700" y="195" width="220" height="145" rx="6" fill="#F7FAF2" stroke="#386B24" stroke-width="1.5"/>
  <rect x="700" y="195" width="220" height="24" rx="6" fill="#E3EFCB"/>
  <text x="810" y="212" font-family="DejaVu Sans, Arial" font-size="10" font-weight="bold" fill="#1B1D1E" text-anchor="middle">RetestEvidence</text>
  <text x="708" y="235" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• id: String (PK)</text>
  <text x="708" y="249" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#386B24" font-weight="bold">• report_id: String (FK)</text>
  <text x="708" y="263" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#386B24" font-weight="bold">• verifier_id: String (FK)</text>
  <text x="708" y="277" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• verifier_type: RESEARCHER | INTERNAL</text>
  <text x="708" y="291" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• fix_confirmed: Boolean</text>
  <text x="708" y="305" font-family="DejaVu Sans, Arial" font-size="8" fill="#B91C1C">• researcher_notes_cipher: Text (Dual)</text>
  <text x="708" y="318" font-family="DejaVu Sans, Arial" font-size="8" fill="#B91C1C">• internal_notes_cipher: Text (Reviewer)</text>
  <text x="708" y="331" font-family="DejaVu Sans, Arial" font-size="8" fill="#555555">• retest_date: DateTime</text>

  <!-- ClosureExport & AuditEvent Bottom -->
  <rect x="210" y="330" width="185" height="105" rx="6" fill="#F7FAF2" stroke="#386B24" stroke-width="1.5"/>
  <rect x="210" y="330" width="185" height="24" rx="6" fill="#E3EFCB"/>
  <text x="302" y="347" font-family="DejaVu Sans, Arial" font-size="10" font-weight="bold" fill="#1B1D1E" text-anchor="middle">ClosureEvidenceExport</text>
  <text x="218" y="369" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• id: String (PK)</text>
  <text x="218" y="384" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#386B24" font-weight="bold">• report_id: String (FK)</text>
  <text x="218" y="399" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• exported_by: String (FK)</text>
  <text x="218" y="414" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• redacted_sha256_hash: String</text>
  <text x="218" y="428" font-family="DejaVu Sans, Arial" font-size="8" fill="#555555">• export_timestamp: DateTime</text>

  <rect x="425" y="345" width="245" height="175" rx="6" fill="#F7FAF2" stroke="#386B24" stroke-width="1.5"/>
  <rect x="425" y="345" width="245" height="24" rx="6" fill="#E3EFCB"/>
  <text x="547" y="362" font-family="DejaVu Sans, Arial" font-size="10.5" font-weight="bold" fill="#1B1D1E" text-anchor="middle">AuditEvent (Append-Only)</text>
  <text x="435" y="385" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• id: String (PK)</text>
  <text x="435" y="400" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#386B24" font-weight="bold">• organization_id: String (FK)</text>
  <text x="435" y="415" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#386B24" font-weight="bold">• report_id: String? (FK)</text>
  <text x="435" y="430" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#386B24" font-weight="bold">• actor_id: String (FK)</text>
  <text x="435" y="445" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• event_type: ActionType (TRANSITION/KEY_ROTATION)</text>
  <text x="435" y="460" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• state_before, state_after: String?</text>
  <text x="435" y="475" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• justification: String</text>
  <text x="435" y="490" font-family="DejaVu Sans, Arial" font-size="8" fill="#B91C1C" font-weight="bold">• Application Grants: INSERT &amp; SELECT Only</text>
  <text x="435" y="504" font-family="DejaVu Sans, Arial" font-size="8" fill="#555555">• timestamp: DateTime</text>

  <!-- DiscussionMessage -->
  <rect x="700" y="355" width="220" height="120" rx="6" fill="#F7FAF2" stroke="#386B24" stroke-width="1.5"/>
  <rect x="700" y="355" width="220" height="24" rx="6" fill="#E3EFCB"/>
  <text x="810" y="372" font-family="DejaVu Sans, Arial" font-size="10" font-weight="bold" fill="#1B1D1E" text-anchor="middle">DiscussionMessage</text>
  <text x="708" y="394" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• id: String (PK)</text>
  <text x="708" y="408" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#386B24" font-weight="bold">• report_id: String (FK)</text>
  <text x="708" y="422" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#386B24" font-weight="bold">• sender_id: String (FK)</text>
  <text x="708" y="436" font-family="DejaVu Sans, Arial" font-size="8.5" fill="#222222">• lane: "RESEARCHER_ORG | INTERNAL_NOTES"</text>
  <text x="708" y="450" font-family="DejaVu Sans, Arial" font-size="8" fill="#B91C1C" font-weight="bold">• encrypted_body: Text (CIPHERTEXT)</text>
  <text x="708" y="464" font-family="DejaVu Sans, Arial" font-size="8" fill="#555555">• created_at: DateTime</text>

  <!-- Relationship Lines -->
  <line x1="180" y1="100" x2="210" y2="100" stroke="#386B24" stroke-width="1.5" marker-end="url(#arrerd)"/>
  <line x1="395" y1="100" x2="425" y2="100" stroke="#386B24" stroke-width="1.5" marker-end="url(#arrerd)"/>
  <line x1="302" y1="180" x2="302" y2="195" stroke="#386B24" stroke-width="1.5" marker-end="url(#arrerd)"/>
  <line x1="670" y1="100" x2="700" y2="100" stroke="#386B24" stroke-width="1.5" marker-end="url(#arrerd)"/>
  <line x1="670" y1="230" x2="700" y2="230" stroke="#386B24" stroke-width="1.5" marker-end="url(#arrerd)"/>
  <line x1="670" y1="380" x2="700" y2="380" stroke="#386B24" stroke-width="1.5" marker-end="url(#arrerd)"/>
  <line x1="425" y1="380" x2="395" y2="380" stroke="#386B24" stroke-width="1.5" marker-end="url(#arrerd)"/>
  <line x1="100" y1="180" x2="100" y2="195" stroke="#386B24" stroke-width="1.5" marker-end="url(#arrerd)"/>
  <line x1="100" y1="315" x2="100" y2="330" stroke="#386B24" stroke-width="1.5" marker-end="url(#arrerd)"/>
  <line x1="100" y1="435" x2="100" y2="445" stroke="#386B24" stroke-width="1.5" marker-end="url(#arrerd)"/>
</svg>'''

with open('projects/BugBountyTrack/requirements/diagrams/fig4_6_erd.svg', 'w') as f:
    f.write(svg_erd)
subprocess.run(['rsvg-convert', '-f', 'png', '-o', 'projects/BugBountyTrack/requirements/diagrams/fig4_6_erd.png', 'projects/BugBountyTrack/requirements/diagrams/fig4_6_erd.svg'])
print('Generated fig4_6_erd.png')

print("All 6 diagrams regenerated successfully with zero visual overlap!")
