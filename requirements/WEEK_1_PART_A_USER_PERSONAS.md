# Week 1 Deliverable (Part A): Target User Personas & Operational Discovery

## Project BugBountyTrack — Multi-Tenant Vulnerability Disclosure Platform

**Document Release State**: Version 3.2.0 (Gate 1 Certified — Zero-Trust Specification Standard)

**Standard Compliance**: ISO/IEC 29147, ISO/IEC 30111, RFC 9116, RFC 9580

---

## 1. Document Control & Academic Metadata

| Attribute | Specification |
| :--- | :--- |
| **Institution** | Punjab Tianjin University of Technology (PTUT), Lahore |
| **Department** | Department of Software Engineering Technology |
| **Degree Program** | BS Software Engineering Technology (5th Semester Capstone) |
| **Project ID** | `PTUT - PRJ - 089` |
| **Project Title** | **BugBountyTrack — Private Bug Bounty & Vulnerability Disclosure Platform** |
| **Category** | 9. Cybersecurity, Privacy & LegalTech |
| **Student Author** | Taha Asadullah (Roll No: `24-ST-013`, Section: `SET-B`) |
| **Academic Supervisor** | Sir Umar Hayat (Assistant Professor, PTUT Lahore) |
| **Milestone Scope** | Week 1 (Part A): Discovery Interviews, Friction Taxonomy & User Personas |

---

## 2. Executive Discovery Context & Market Reality

Vulnerability disclosure is recognized by international cybersecurity standards (ISO/IEC 29147 and ISO/IEC 30111) as a foundational discipline for modern software systems. When external ethical security researchers discover vulnerabilities in production web applications or APIs, organizations require a confidential, legally unambiguous channel to receive, triage, remediate, and verify those findings.

While established platforms and code hosts offer free entry tiers (such as HackerOne Essential VDP or GitHub Security Advisories), small engineering teams (5–50 developers) and independent B2B SaaS startups face three structural architectural gaps:

* **Server-Managed Plaintext Exposure**: Free and commercial tiers of traditional VDP platforms operate on a server-managed model where exploit descriptions and proof-of-concept (PoC) attachments are stored in plaintext on vendor infrastructure, accessible to platform operators, cloud intermediaries, and support databases.
* **Single-Forge Lock-In & Mandatory Account Friction**: Repository-bound tools (such as GitHub Security Advisories) require reporters to hold platform accounts and do not span multi-service SaaS architectures, APIs, or cloud infrastructure outside a single repository.
* **Insecure Ad-Hoc Channels & Unverified Closures**: Organizations unwilling to store unpatched zero-day exploits in plaintext on third-party vendor servers fall back to generic `security@company.com` email inboxes or standard issue trackers (Jira, Linear), exposing sensitive exploit steps over unencrypted email servers and closing security tickets via informal text status updates without Git commit verification or researcher retesting.

---

## 3. Target User Interviews & 4 Operational Frictions Identified

Structured discovery interviews representing both sides of the disclosure workflow—independent ethical security researchers ("Hunters") and startup engineering leads ("Defenders")—revealed four primary operational frictions:

| Friction ID | Friction Dimension | Observed Industry Behavior | Security & Operational Consequence | BugBountyTrack Remedy |
| :--- | :--- | :--- | :--- | :--- |
| **FRC-01** | **Third-Party Plaintext Exposure** | Existing VDP tiers store raw exploit write-ups and PoC scripts in server-readable plaintext on vendor databases. | A vendor breach or unauthorized third-party access exposes active, unpatched zero-day exploits across tenant organizations. | Zero-knowledge client-side OpenPGP v6 (`Curve25519`) encryption before transit; server stores only ciphertext and a neutral `operational_label`. |
| **FRC-02** | **Insecure Ad-Hoc Email Channels** | Teams avoiding vendor lock-in ask researchers to email vulnerability reports to `security@` or `support@` addresses. | Standard SMTP lacks end-to-end encryption; raw SQLi/RCE payloads sit in plaintext across mail relays, shared inboxes, and Slack threads. | In-browser multi-recipient `PKESK` encryption addressed strictly to `PROGRAM_DEFENDER` keys and an offline master recovery key. |
| **FRC-03** | **Legal Ambiguity & Registration Friction** | Startups lack signed `/.well-known/security.txt` Safe Harbor policies, and portals demand full account signup for one-off reports. | Researchers withhold valid reports due to fear of legal prosecution (CFAA/PECA) or abandon submissions due to registration friction. | Browser-signed RFC 9116 `security.txt` with Disclose.io Safe Harbor terms, plus 60-second Account-Less Guest Intake with `.bbt-recovery.json`. |
| **FRC-04** | **The "Fix-and-Forget" Verification Gap** | Trackers mark tickets "Closed" via a text toggle when a PR merges, without checking the branch commit or re-engaging the finder. | Superficial patches fix only a single symptom while leaving the root cause exploitable via adjacent vectors. | Git-linked remediation state machine requiring a verified 40-char commit SHA (or 64-char SHA-256 config hash) and attested retest sign-off. |

---

## 4. Detailed Target User Personas & Empathy Maps

### 4.1 Persona 1: Alex Rivera — "The Hunter" (External Ethical Security Researcher)

| Attribute | Profile Specification |
| :--- | :--- |
| **Full Name & Archetype** | Alex Rivera — "The Hunter" (External Security Researcher & Bug Finder) |
| **Age & Background** | 23 years old; Independent Security Researcher & Final-Year Cybersecurity Student |
| **Practical Experience** | 2 years part-time vulnerability research; Top 5% university CTF competitor |
| **Operating Environment** | Kali Linux, macOS, Firefox Developer Edition |
| **Core Technical Stack** | Burp Suite Professional, `ffuf`, `nuclei`, `curl`, Python (`requests`), GnuPG CLI, Wireshark |
| **Preferred Workflow** | Fast keyboard-driven submission, verifiable cryptographic privacy, objective scoring, and portfolio attribution |

#### Core Goals & Motivations (Alex Rivera)

1. **Responsible & Timely Disclosure**: Notify engineering teams of critical vulnerabilities before malicious actors exploit them—either using an authenticated Hunter account (for portfolio reputation) or via a 60-second anonymous guest submission.
2. **Explicit Legal Safe Harbor**: Confirm via a machine-readable, cryptographically signed `/.well-known/security.txt` policy that good-faith security testing within scope is authorized and protected from legal action.
3. **Deterministic Severity Evaluation**: Receive fair, reproducible severity scoring grounded in the official FIRST.org CVSS v3.1 mathematical standard rather than subjective email negotiation.
4. **Verifiable Remediation Credit**: Participate in structured patch retesting to confirm that the reported vulnerability is genuinely eliminated and earn verified attribution.

#### Critical Pain Points & Frustrations (Alex Rivera)

* **The Black Hole ("Ghosting")**: Submitting comprehensive vulnerability reproduction steps to `security@target.com` and receiving zero acknowledgment or status visibility for weeks.
* **Plaintext Exploit Leakage**: Refusing to transmit live zero-day exploit payloads over unencrypted email or upload them to third-party servers where vendor staff can inspect them in plaintext.
* **Arbitrary Severity Downgrades**: Experiencing organizations unilaterally downgrading a high-impact vulnerability to "Low" without providing a transparent CVSS v3.1 metric breakdown.
* **Premature Unverified Closures**: Discovering that an engineering team applied an incomplete client-side filter and closed the ticket without inviting the researcher to retest the fix.

#### Empathy Map (Alex Rivera — The Hunter)

| Empathy Dimension | User Expression & Behavioral Observation |
| :--- | :--- |
| **Says** | *"I found a critical IDOR exposing customer data. I want to report it responsibly, but I need Safe Harbor assurance and end-to-end encryption."* |
| **Thinks** | *"Will they actually patch the root cause on the production branch, or will someone paste my plaintext PoC into Slack and close the ticket untested?"* |
| **Does** | Checks `/.well-known/security.txt` before testing; records HTTP reproduction steps in Burp Suite; downloads `.bbt-recovery.json` when submitting as a guest; re-runs exploit payloads when invited to retest. |
| **Feels** | Cautious about legal liability; frustrated by silent email inboxes; respected and motivated when an engineering team shares a commit-linked fix for retest. |

---

### 4.2 Persona 2: Sarah Chen — "The Defender" (Startup CTO & Security Triage Lead)

| Attribute | Profile Specification |
| :--- | :--- |
| **Full Name & Archetype** | Sarah Chen — "The Defender" (Organization Owner & Triage Lead) |
| **Age & Background** | 31 years old; Co-Founder, CTO & Lead Full-Stack Engineer at a 7-person B2B FinTech SaaS startup |
| **Practical Experience** | 8 years in production full-stack software engineering, cloud infrastructure, and technical leadership |
| **Operating Environment** | macOS, VS Code, GitHub, Vercel, Neon Serverless PostgreSQL, Cloudflare R2 |
| **Core Technical Stack** | TypeScript, Next.js App Router, PostgreSQL, Prisma, Docker, GitHub Actions, Linear, Slack |
| **Preferred Workflow** | Zero-setup browser cryptography, structured triage queues, automated GitHub commit checks, and exportable compliance reports |

#### Core Goals & Motivations (Sarah Chen)

1. **Zero-Knowledge Exploit Confidentiality**: Provide external researchers with an encrypted disclosure portal where vulnerability titles, descriptions, and PoC attachments are encrypted in the browser so only authorized program defenders (`PROGRAM_DEFENDER`) can decrypt them—never a third-party vendor.
2. **Enterprise Compliance & Audit Readiness**: Publish a browser-signed RFC 9116 `security.txt` policy and export **Redacted Closure Evidence** certificates (documenting lifecycle timestamps, verified Git commit SHAs, and retest attestations without exposing raw exploit instructions) for enterprise B2B security questionnaires and SOC 2 audits.
3. **High-Signal Engineering Triage**: Separate genuine vulnerability reports from automated scanner spam and bind every engineering fix to a verified GitHub commit SHA and formal retest state.
4. **Resilient Key & Team Governance**: Maintain an offline **Organization Master Recovery Key** (`recovery_public_key`) so the startup never loses decryption access if an engineer leaves or loses their device.

#### Critical Pain Points & Frustrations (Sarah Chen)

* **Scanner Spam Overload**: Wasting valuable engineering hours sifting through automated scanner noise and low-effort bounty demands in a shared `security@` inbox.
* **CLI GnuPG Operational Complexity**: Configuring command-line GPG keyrings and email client plugins across a 7-person engineering squad is brittle and impractical; she needs key generation (`RFC 9580 v6 Curve25519`), `IndexedDB` storage (`Argon2id S2K`), and multi-recipient encryption handled automatically in the browser.
* **Third-Party Vendor Breach Risk**: Refusing to store unpatched zero-day exploits in plaintext on external VDP vendor servers where a platform breach would expose her company's vulnerabilities.
* **Uncertain Remediation Verification**: Merging a developer pull request without a deterministic state machine to verify that the commit exists on the target branch and passes researcher retesting.

#### Empathy Map (Sarah Chen — The Defender)

| Empathy Dimension | User Expression & Behavioral Observation |
| :--- | :--- |
| **Says** | *"Free VDP tiers store raw exploits in plaintext on vendor servers, while our `security@` email inbox is flooded with unencrypted scanner spam."* |
| **Thinks** | *"If an ethical hacker sends us an exploit, I need it encrypted client-side for my designated defenders only, backed by an offline master recovery key and proof that our Git commit actually fixed it."* |
| **Does** | Reviews GitHub pull requests; verifies DNS TXT challenges; assigns `PROGRAM_DEFENDER` permissions; links 40-character commit SHAs to triage tickets; exports redacted closure certificates for B2B clients. |
| **Feels** | Protective of customer financial data and limited engineering cycles; relieved and confident when vulnerability reports follow a deterministic, verifiable lifecycle. |

---

## 5. Document Endorsement & Milestone Sign-Off

| Signatory Role | Name & Academic Designation | Status / Signature | Date |
| :--- | :--- | :--- | :--- |
| **Submitted By (Student Author)** | **Taha Asadullah** (Roll No: `24-ST-013`, Section: `SET-B`, BS Software Engineering Technology, PTUT Lahore) | *Signed: Taha Asadullah* | October 2026 |
| **Reviewed By (Academic Supervisor)** | **Sir Umar Hayat** (Assistant Professor, Department of Software Engineering Technology, PTUT Lahore) | `[ ] Approved` / `[ ] Revisions` — Signature: `[__________________]` | `[____________]` |
