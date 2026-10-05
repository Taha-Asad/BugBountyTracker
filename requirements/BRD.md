# BUSINESS REQUIREMENTS DOCUMENT (BRD)
## Project BugBountyTrack: A Multi-Tenant Vulnerability Disclosure Platform with Cryptographic Payload Isolation and Evidence-Based Remediation Traceability
**Document Release State**: Commercial Baseline & Academic Evaluation Specification (Version 3.0.0)  
**Standard Compliance**: IEEE Std 830-1998 / ISO/IEC/IEEE 29148:2018  

---

## 1. Project Control & Metadata

| Project Parameter | Engineering & Academic Specification |
| :--- | :--- |
| **Project Identifier** | `PTUT - PRJ - 089` |
| **Project Title** | BugBountyTrack: Private Bug Bounty & Vulnerability Disclosure Platform |
| **Academic Sub-Field** | 9. Cybersecurity, Privacy & LegalTech |
| **Student Author** | Taha Asadullah (Roll No: **`24-ST-013`**) |
| **Academic Institution** | Punjab Tianjin University of Technology (PTUT), Lahore |
| **Department** | Department of Software Engineering Technology |
| **Session / Batch / Section** | Session 2024–2028 / Batch 24-SET-Fall / Section SET-A |
| **Official Student Email** | `24-st-013@students.ptut.edu.pk` |
| **FYP Supervisor** | Sir Umar Hayat |
| **Target Architecture** | Decoupled 3-Tier Web Application (Next.js 14+ App Router, Node.js 22 LTS, PostgreSQL 16 on Neon, OpenPGP.js Client Crypto, Tailwind CSS) |
| **Target Deliverable** | Commercial Launch-Ready Micro-VDP & Evaluated FYP Specification Suite |
| **Planned Duration** | 16 Calendar Weeks (Milestone 1: Weeks 1–8 Core; Milestone 2: Weeks 9–12 Pilot & Defense; Milestone 3: Weeks 13–16 Commercial Launch) |

---

## 2. Executive Summary & Problem Horizon

### 2.1 Context & Problem Statement
Vulnerability coordination is an essential component of modern software defense. When external security researchers discover flaws in software products, they require a secure, confidential mechanism to report their findings without exposing the affected organization or risking legal ambiguity.

While mature enterprises deploy dedicated security portals or contract commercial crowdsourced platforms (such as HackerOne, Bugcrowd, or Intigriti), early-stage technology startups, small software engineering teams (5–50 developers), and open-source projects face significant structural barriers:
1. **Commercial Subscription Realities**: While established vendors offer entry tiers (such as HackerOne Essential VDP), existing solutions either steer organizations toward high-cost enterprise managed-triage contracts ($15,000–$30,000+/year) or route unencrypted vulnerability reproduction steps and exploit payloads into standard web queues and unencrypted corporate email inboxes.
2. **Confidentiality & Insecure Communication**: Lacking dedicated cryptographic intake channels, small organizations receive security reports via plaintext email, public issue trackers, or social media direct messages. This unencrypted transit exposes sensitive zero-day vulnerability reproduction steps across intermediate mail servers and employee devices.
3. **The Remediation & Verification Gap**: Standard bug trackers treat vulnerability resolution as an informal status change (`Closed` or `Resolved`). There is rarely an explicit, verifiable connection between the vulnerability report, the code or configuration change intended to resolve it, and an attested retest outcome confirming the fix before closure.
4. **Legal Ambiguity & Onboarding Friction**: Early-stage engineering teams struggle to establish clear rules of engagement, RFC 9116 `security.txt` discovery policies, and safe-harbor terms without expensive legal counsel.

### 2.2 Proposed Solution & Commercial Value Proposition
BugBountyTrack is a focused B2B micro-VDP engineered specifically for small software engineering leads, CTOs, and product security owners who handle vulnerability reports manually:

> **Core Value Proposition**: *A confidential vulnerability reporting workspace that helps small software teams receive reports, coordinate fixes, and document how each issue was retested and closed.*

The platform differentiates itself through four architectural and operational pillars:
* **Client-Side Cryptographic Payload Isolation**: Sensitive exploit descriptions, reproduction steps, and proof-of-concept (PoC) attachments are encrypted directly in the researcher's browser using OpenPGP before transmission. Backend databases and application APIs persist and route ciphertext only. To prevent sensitive title leakage in URLs, notification logs, and dashboards, titles are encrypted client-side while exposing a neutral, server-readable operational category label (`operational_label` enum).
* **Evidence-Based Remediation & Attested Retest**: Decoupling the declaration of a fix from its verification, verifying commit existence and branch presence via the GitHub REST API v3, and enforcing an audited retest state machine with distinct, mutually exclusive terminal closure states.
* **Redacted Closure Evidence Exports**: Enabling engineering leads to generate customer-controlled, sanitized PDF/HTML closure evidence summaries that document the vulnerability's timeline, verified commit hash, deployment environment, and retest attestation without exposing raw exploit code.
* **Streamlined Onboarding & Guided Program Setup**: Guiding engineering leads through domain DNS verification, browser-side cleartext-signed RFC 9116 `security.txt` generation, and Disclose.io-aligned safe harbor configuration in under 15 minutes.

---

## 3. Strategic Business & Academic Objectives

| Objective ID | Strategic Objective | Business & Academic Outcome | Target Evaluation Metric |
| :--- | :--- | :--- | :--- |
| **BO-1** | **Client-Side Payload Confidentiality & Neutral Labeling** | Protect sensitive exploit data from server-side database exposure by performing asymmetric OpenPGP encryption in the client browser, combining encrypted titles (`title_ciphertext`) with neutral operational labels (`operational_label`). | 100% of vulnerability descriptions, steps, attachments, and specific titles stored exclusively as ciphertext. 0 plaintext exploit bytes in database dumps. |
| **BO-2** | **Standardized Discovery & Policy Publishing** | Enable small software teams to generate, cryptographically sign, and download standardized RFC 9116 `security.txt` files and Disclose.io-aligned reporting policies with verified domain ownership. | Browser-side generation of signed cleartext RFC 9116 `security.txt` and verified domain DNS TXT challenge (`_bbt-challenge.<domain>`). |
| **BO-3** | **Deterministic Severity Assessment** | Standardize vulnerability prioritization using the FIRST.org Common Vulnerability Scoring System (CVSS 3.1) Base metric specification. | 100% calculation accuracy across 52 canonical test vectors derived from FIRST.org Appendix A and NIST NVD benchmarks; mandatory recording of CVSS vector, score, assessor identity, and justification. |
| **BO-4** | **Remediation Traceability** | Decouple fix declaration from fix verification by linking remediation claims to verifiable GitHub commit SHAs (via GitHub REST API v3 for public and private repositories) or cryptographic configuration hashes. | Verification of repository existence and target branch for 100% of code-linked remediation declarations; deployment environment and version string attestation. |
| **BO-5** | **Accountable Closure State Machine & SLA Timers** | Prevent premature or unverified bug closure through distinct, mutually exclusive terminal states, mandatory retest attestation records, and configurable SLA countdown timers. | Every closed report shall have a recorded closure category and justification. Only successfully retested reports shall be labeled verified. Rejected, duplicate, and unverified-timeout outcomes shall be reported separately. |
| **BO-6** | **Two-Tier Financial Viability & Production Cloud Budget** | Demonstrate zero-cost academic prototype viability on free cloud tiers ($0.00/mo) while defining a sustainable, commercially viable production cloud infrastructure budget (~$60–$80/mo baseline) supported by paid SaaS subscription tiers. | Academic prototype operational cost bounded at $0.00/month; commercial production architecture validated within ~$60–$80/month for up to 10 paying tenant organizations. |

---

## 4. Stakeholder Ecosystem & User Classes

| Stakeholder Role | System Actor | Primary Responsibilities | Data Access Permissions |
| :--- | :--- | :--- | :--- |
| **Ethical Researcher** | `Hunter` | Discovers in-scope vulnerabilities; encrypts sensitive payloads client-side; submits reports; conducts empirical retests upon notification. | Full access to own submitted reports, encrypted communication lane with defender, public program policies, and personal reputation record. |
| **Organization Triage Lead** | `Defender` | Reviews intake; designated active Decryption Custodian; decrypts payloads in-browser using local private key; assigns CVSS scores; coordinates remediation; requests retests. | Full access to organization reports, internal triage notes, organization PGP key management, and remediation verification workflows. |
| **Organization Owner** | `Tenant Owner` | Manages tenant workspace, invites members, signs RFC 9116 policies, manages key backups/succession, and executes authorized ticket reopening. | Administrative control over organization profile, domain DNS verification, member roles, billing subscription, and program rules. |
| **Organization Member** | `Read-Only Member` | Monitors program operational health, SLA countdowns, and aggregate vulnerability counts without inspecting raw exploits. | Read-only visibility into non-sensitive report metadata (Report ID, operational category label, severity rating, current state, timestamps, SLA status). |
| **Platform Operator** | `SuperAdmin` | Provisions tenant accounts, monitors platform uptime, inspects rate-limiting logs, and manages platform configuration. | Administrative access to organization registry, domain verification challenges, and infrastructure telemetry. No access to private keys or encrypted payloads. |
| **Academic Evaluator** | `Supervisor / Faculty Panel` | Reviews project deliverables, validates state transitions, audits automated test coverage, and evaluates FYP defense. | Evaluator access to test execution logs, database migration scripts, architectural diagrams, and controlled demonstration instances. |

---

## 5. Detailed Functional Business Requirements

### BR-1: Multi-Tenant Workspace, Guided Onboarding & Access Governance
* **BR-1.1**: The system shall support multiple isolated organization workspaces hosted within a single multi-tenant database schema using tenant identifier bindings.
* **BR-1.2**: Access permissions shall be strictly enforced on the server across four distinct roles: Tenant Owner (`ORG_OWNER`), Security Reviewer (`ORG_DEFENDER`), Read-Only Member (`ORG_READONLY`), and External Researcher (`HUNTER`).
* **BR-1.3**: Users shall authenticate against the server using email and bcrypt-hashed (rounds = 12) **login passwords** transmitted over TLS, receiving signed, HTTP-only JWT session cookies. Organization Owners and Defenders shall support Time-Based One-Time Password (TOTP) Multi-Factor Authentication. The login password is strictly separated from the local encryption passphrase.
* **BR-1.4**: Organizations shall be guided through a streamlined Onboarding Wizard covering domain DNS verification, policy definition, browser-side keypair generation, and RFC 9116 `security.txt` signing in under 15 minutes.
* **BR-1.5**: Organizations shall be able to configure public program profiles (`/programs/[slug]`) and launch private, invitation-only programs accessible via cryptographically tokenized invitation links.

### BR-2: RFC 9116 Policy & Safe Harbor Generator
* **BR-2.1**: The platform shall automatically generate a compliant RFC 9116 text policy file available for download and preview at `/api/v1/programs/[slug]/security.txt`.
* **BR-2.2**: The `security.txt` content shall be signed in the browser using the organization's private signing key and exported as a standard OpenPGP cleartext signed document. The organization downloads this signed document and hosts it on their own root domain at `/.well-known/security.txt`, with the `Contact:` directive pointing back to BugBountyTrack's intake portal (`https://bugbountytrack.com/programs/[slug]/submit`).
* **BR-2.3**: Verification of `security.txt` shall be performable using the organization's advertised public key.
* **BR-2.4**: The policy builder shall generate clear safe-harbor terms based on Disclose.io Core standards, explicitly stating authorized research activities, scope boundaries, and documented limitations without asserting universal third-party legal immunity.
* **BR-2.5**: Domain ownership shall be verified through automated DNS TXT record challenge verification (`_bbt-challenge.<domain>`) prior to program activation.

### BR-3: Browser-Side OpenPGP Cryptographic Intake & Neutral Labeling
* **BR-3.1**: Sensitive report fields (vulnerability title, vulnerability description, reproduction steps, impact analysis, and proof-of-concept attachments) shall be encrypted in the client browser using OpenPGP prior to network transit (`title_ciphertext`).
* **BR-3.2**: To enable operational filtering, dashboard queuing, and safe external notifications without leaking sensitive exploit details, the submitter shall select a neutral server-readable operational category label (`operational_label` enum: `AUTHENTICATION_BYPASS`, `INJECTION_VULNERABILITY`, `INFORMATION_DISCLOSURE`, `CROSS_SITE_SCRIPTING`, `ACCESS_CONTROL_ISSUE`, `DENIAL_OF_SERVICE`, `OTHER`).
* **BR-3.3**: Encryption shall utilize a dual-recipient OpenPGP envelope encrypting the payload to the organization's designated active Decryption Custodian encryption subkey and the reporting researcher's public key.
* **BR-3.4**: The protection boundary shall strictly isolate ciphertext: application APIs and databases shall receive and persist only ciphertext for sensitive fields.
* **BR-3.5**: Private keys shall remain strictly within client-side storage, protected by **local encryption passphrases** derived via PBKDF2 (iterations ≥ 100,000) and AES-GCM. The local encryption passphrase is completely distinct from the account login password and is never transmitted to the server. The platform provides owner-managed armored private key backup export/import workflows and retains historic private keys in the custodian's local keystore to decrypt past reports upon subkey rotation.
* **BR-3.6**: The platform documentation shall explicitly state the browser trust boundary: client-side cryptographic isolation protects against server-side database exposure, untrusted backend administrators, and compromised database dumps; it does not protect against malware executing on the client host or browser extensions possessing permissions to modify client DOM or memory.

### BR-4: Deterministic CVSS 3.1 Scoring Engine
* **BR-4.1**: The platform shall incorporate a pure TypeScript calculation engine strictly adhering to the FIRST.org CVSS 3.1 Base metric specification.
* **BR-4.2**: The engine shall calculate numeric scores (0.0 to 10.0) and qualitative ratings (None, Low, Medium, High, Critical) based on the eight Base metrics: Attack Vector (AV), Attack Complexity (AC), Privileges Required (PR), User Interaction (UI), Scope (S), Confidentiality (C), Integrity (I), and Availability (A).
* **BR-4.3**: The engine implementation shall be verified against the 52 canonical test vectors documented in `CVSS_TEST_FIXTURES.md` with 100% mathematical parity.
* **BR-4.4**: For every severity assessment, the platform shall immutably record the full vector string, calculated score, assessor identity, and a textual justification to resolve potential severity disputes.

### BR-5: Confidential Triage, Dual-Lane Messaging & SLA Timers
* **BR-5.1**: Authorized reviewers (designated Decryption Custodians) shall decrypt vulnerability payloads in-browser upon providing their local encryption passphrase.
* **BR-5.2**: The platform shall provide a dual-lane discussion interface:
  * **Researcher–Organization Conversation**: Confidential threaded messages encrypted for both Hunter and Defender.
  * **Internal Reviewer Notes**: Private notes encrypted exclusively for the organization custodian's key, completely inaccessible to the researcher.
* **BR-5.3**: Outbound notifications (via email or webhooks) shall convey operational metadata only (e.g., "New update on Report #BBT-104 [AUTHENTICATION_BYPASS]") with an authenticated link, never transmitting exploit details over external notification rails.
* **BR-5.4**: The system shall track SLA countdown timers based on severity (e.g., Critical: 48h initial triage, 14d fix; High: 72h triage, 30d fix), displaying visual alerts and dispatching automated reminder emails when deadlines approach.
* **BR-5.5**: Duplicate management shall be reviewer-driven: reviewers may link related reports internally after authorized decryption without leaking details between unrelated researchers.

### BR-6: Automated VCS Integration & Remediation Evidence
* **BR-6.1**: When declaring a vulnerability fix, the organization shall propose remediation evidence categorized by type: code repository commit or non-code configuration change.
* **BR-6.2**: For code fixes, the platform shall query the GitHub REST API v3 (`GET /repos/{owner}/{repo}/commits/{ref}`) using an organization-provided GitHub token or GitHub App installation to verify that the referenced 40-character commit SHA exists and confirm its presence on the target repository branch across public or private repositories.
* **BR-6.3**: For non-code infrastructure remediations (e.g., WAF rules, cloud policies), the browser shall compute a cryptographic SHA-256 hash of the configuration document locally before transmission to establish an immutable evidence baseline without hosting proprietary configuration files on the platform.
* **BR-6.4**: Remediation declarations shall explicitly record the target deployment environment (Staging, Pre-Production, Production) and version string where the fix is accessible for retesting.

### BR-7: Attested Retest State Machine, Accountable Closure & Redacted Exports
* **BR-7.1**: The platform shall enforce an explicit, audited lifecycle state machine:
  `NEW → TRIAGING → ACCEPTED → FIX_PROPOSED → RETEST_PENDING → [TERMINAL STATE]`
* **BR-7.2**: Intermediary exception states shall be formally supported: `NEED_MORE_INFO` (requesting researcher clarification), `REJECTED` (out-of-scope or invalid), and `DUPLICATE` (internally linked).
* **BR-7.3**: Reports shall transition from `RETEST_PENDING` to final closure exclusively under one of three distinct terminal states:
  * `VERIFIED_RESEARCHER`: The reporting researcher independently retested and certified that the vulnerability is mitigated on the deployment environment.
  * `VERIFIED_INTERNAL`: An authorized organization reviewer certified the fix, recording whether they authored the fix.
  * `CLOSED_UNVERIFIED_TIMEOUT`: Closed following an expired researcher grace period (≥ 14 days) **only through an explicit authorized reviewer action with recorded justification**.
* **BR-7.4**: If retesting reveals that the vulnerability persists, the state transition shall record a `RETEST_FAILED` audit event and return to `ACCEPTED`, preserving the failed retest evidence in the immutable audit log.
* **BR-7.5**: Reopening any closed report (`VERIFIED_RESEARCHER`, `VERIFIED_INTERNAL`, `CLOSED_UNVERIFIED_TIMEOUT`, `REJECTED`, `DUPLICATE`) shall require an authorized Defender or Tenant Owner action recording an immutable justification log, transitioning the ticket back to `TRIAGING`.
* **BR-7.6**: The platform shall generate exportable Redacted Closure Evidence summaries (PDF and JSON/HTML format) capturing the operational label, report lifecycle timestamps, verified commit SHA/branch, deployment environment, retest attestations, and closing officer identity, suitable for sharing with enterprise clients and security auditors without disclosing raw exploit instructions.

### BR-8: Application Hardening, Defensive Controls & Storage Quotas
* **BR-8.1**: Decrypted Markdown content shall be sanitized prior to DOM rendering using an Abstract Syntax Tree (AST) parser (`unified` / `remark-parse` / `rehype-sanitize`) enforcing strict HTML element and attribute allowlists to neutralize Stored Cross-Site Scripting (XSS).
* **BR-8.2**: The platform shall enforce database-level Row-Level Security (RLS) in PostgreSQL, dynamically scoping connection queries to the authenticated tenant context.
* **BR-8.3**: Public report submission endpoints shall be protected by token-bucket rate limiting (5 submissions / hour / IP) to mitigate automated denial-of-service and scanner spam.
* **BR-8.4**: The platform shall enforce storage quotas to protect shared infrastructure: in the academic demonstration baseline, quotas are configured at 50 MB database volume on PostgreSQL and 2 GB encrypted object storage on Cloudflare R2 per tenant organization (bounding total multi-tenant demo volume across 5 tenants within 250 MB database and 10 GB object storage limits). In commercial production, per-tenant quotas correspond to subscription tier entitlements (10 GB for Starter, 50 GB for Team/Pro). The platform shall issue an administrative warning when organization storage usage reaches 90% of the configured quota, and strictly reject any new upload or report allocation that would cause total storage to exceed 100% (HTTP 413 Payload Too Large).
* **BR-8.5**: The audit ledger shall enforce strict append-only constraints: database permissions on `audit_events` shall permit `INSERT` and `SELECT` operations only, strictly preventing `UPDATE` and `DELETE` actions by any application role.

---

## 6. Scope Boundaries & Anti-Goals

To maintain high engineering fidelity and realistic delivery boundaries, the following capabilities are explicitly declared out of scope for the initial product baseline:
1. **No Real-Money Financial Payout Escrow in MVP**: The initial launch omits real-money banking payout rails (Stripe Connect, ACH, SEPA) and tax compliance (W-8BEN / W-9 forms). If demonstration awards are shown, they shall be modeled as explicitly simulated credit/point records.
2. **No Automated Vulnerability Exploitation**: The platform coordinates reports and verifies evidence; it does not execute active scanner exploits against target applications.
3. **No Unverified AI / LLM Triage Assistance**: All triage workflows, severity calculations, and state transitions are deterministic and human-driven.
4. **No Server-Side Private Key Escrow**: The platform never stores or manages server-side private keys for decrypting report payloads.
5. **No Enterprise Identity Federation in MVP**: Enterprise SAML 2.0 and SCIM directory synchronization are deferred to post-launch enterprise releases.

---

## 7. Success Metrics & Evaluation Methodology

The platform shall be evaluated through a structured, reproducible experimental evaluation:
1. **Functional State Machine Verification**: Automated test suites asserting that 100% of valid and invalid state transitions adhere to the formal state transition matrix, with 0 bypasses.
2. **Controlled Peer Evaluation**: A small-cohort usability study involving 3–5 software engineering peers executing simulated disclosure workflows across containerized targets (e.g., OWASP Juice Shop).
3. **Quantitative Metrics**:
   * *Cryptographic Boundary Integrity*: 100% zero-plaintext assertion across database storage dumps for designated sensitive fields.
   * *Remediation Verification Ratio*: Every closed report shall have a recorded closure category and justification. Only successfully retested reports shall be labeled verified. Rejected, duplicate, and unverified-timeout outcomes shall be reported separately.
   * *Triage Time Efficiency*: Measured reduction in triage documentation time compared to an unencrypted email baseline across the evaluation cohort.

---

## 8. Two-Tier Cloud Budget, Financial Model & Commercial Pricing

### 8.1 Academic Demonstration Budget (Zero-Cost Baseline)
The academic prototype is engineered to operate entirely within verified zero-cost developer tiers:

| Infrastructure Tier | Provider | Service Tier & Resource Allocation | Monthly Cost |
| :--- | :--- | :--- | :---: |
| **Web Frontend & API Gateway** | Vercel Cloud | Hobby Tier (Edge CDN, Serverless Functions, Global SSL) | **$0.00** |
| **Relational Persistence** | Neon Serverless | PostgreSQL Free Tier (512 MB storage total; configured quota of 50 MB per tenant across 5 demonstration tenants = 250 MB total working volume, connection pooling via PgBouncer) | **$0.00** |
| **Encrypted Attachment Storage** | Cloudflare R2 | Free Tier Object Storage (10 GB storage total allowance; configured quota of 2 GB per tenant across 5 demonstration tenants = 10 GB total application limit, zero egress fees) | **$0.00** |
| **Transactional Email Notifications** | Resend API | Developer Free Tier (3,000 emails / month for metadata triage updates) | **$0.00** |
| **CI/CD Build Automation** | GitHub Actions | 2,000 Free Build Minutes / Month (linting, Jest, test suite) | **$0.00** |
| **TOTAL MONTHLY OPERATIONAL TCO** | — | **Academic Demonstration & FYP Evaluation Baseline** | **$0.00 / mo** |

### 8.2 Commercial Production Cloud Budget (Early Commercial Cohort: 10–25 Tenants)
When transitioning to paid commercial operations serving early B2B customers, the infrastructure shifts to commercially supported tiers with dedicated SLAs and custom domain support:

| Infrastructure Layer | Commercial Provider | Provisioned Commercial Tier | Purpose & Quota | Monthly Cost ($USD) |
| :--- | :--- | :--- | :--- | :---: |
| **Application & API Gateway** | Vercel Pro | Pro Team Tier ($20 / seat) | Commercial SLA, edge caching, zero cold starts, team collaboration | **$20.00** |
| **Production Database** | Neon Serverless | Launch Tier Baseline | PostgreSQL 16 (10 GB storage, PITR branching, autoscaling compute) | **$19.00** |
| **Encrypted Object Storage** | Cloudflare R2 | Pay-As-You-Go ($0.015/GB-mo) | Encrypted report attachments, 50 GB pooled baseline, zero egress fees | **$0.75** |
| **Transactional Email Delivery** | Resend / Postmark Pro | Essential Commercial Tier | High deliverability minimal-metadata notifications (50,000/mo) | **$20.00** |
| **Domain & DNS Registration** | Cloudflare Registrar | `.com` / `.security` TLD | Amortized domain registrar fee ($15.00/year) | **$1.25** |
| **Payment Gateway** | Stripe Billing | Automated invoicing & checkout | 2.9% + $0.30 per transaction | **Variable** |
| **TOTAL PRODUCTION OPERATING BASELINE** | — | — | **Commercial Production Cloud Baseline (10–25 Tenants)** | **~$61.00 / mo** |

### 8.3 Commercial SaaS Subscription Pricing Model (Validation Hypotheses)
To ensure financial viability and recover cloud operational costs, BugBountyTrack adopts a transparent two-tier SaaS pricing model for small software companies:

| Subscription Tier | Proposed Price | Target Customer Hypothesis | Included Features & Quota Bounds |
| :--- | :---: | :--- | :--- |
| **Starter Tier** | **$49 / mo** | Seed startups & small engineering teams (5–15 devs) needing structured intake | 1 active disclosure program, 3 defender seats (all with independent program-scoped decryption capability), 10 GB encrypted storage, browser OpenPGP crypto, RFC 9116 generator, GitHub commit verification, minimal-metadata email alerts, basic Redacted PDF/JSON Closure Evidence exports. |
| **Team / Pro Tier** | **$149 / mo** | Growing SaaS companies (15–50 devs) handling multi-product disclosure | Up to 5 programs (public & private), 10 defender seats, 50 GB encrypted storage, GitHub App integration, SLA timers & automated reminders, custom-branded closure exports, executive compliance summaries, priority support. |

*With 2 paying customers on the Starter Tier ($94.56 net after Stripe 2.9% + $0.30 processing fees), the platform covers 100% of its base commercial cloud operating expenses ($61.00/mo). All pricing figures represent initial validation hypotheses subject to empirical testing during the commercial pilot.*

---

*--- End of Business Requirements Document (BRD) ---*
