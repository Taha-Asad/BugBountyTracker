# BUSINESS REQUIREMENTS DOCUMENT (BRD)
## Project BugBountyTrack: A Multi-Tenant Vulnerability Disclosure Platform with Cryptographic Payload Isolation and Evidence-Based Remediation Traceability
**Document Release State**: Commercial Baseline & Academic Evaluation Specification (Version 3.2.0)  
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
| **Target Architecture** | Decoupled 3-Tier Web Application (Next.js 14+ App Router, Node.js 22 LTS, PostgreSQL 16 on Neon, OpenPGP.js Client Crypto, Cloudflare R2, Tailwind CSS) |
| **Target Deliverable** | Commercial Launch-Ready Micro-VDP & Evaluated FYP Specification Suite |
| **Planned Duration** | 18 Calendar Weeks (Part A: Weeks 1–12 Academic Prototype Baseline; Part B: Weeks 13–18 Commercial Launch & Pilot) |

---

## 2. Executive Summary & Problem Horizon

### 2.1 Context & Problem Statement
Vulnerability coordination is an essential component of modern software defense. When external security researchers discover flaws in software products, they require a secure, confidential mechanism to report their findings without exposing the affected organization or risking legal ambiguity.

While mature enterprises deploy dedicated security portals or contract commercial crowdsourced platforms (such as HackerOne, Bugcrowd, or Intigriti), early-stage technology startups, small software engineering teams (5–50 developers), and open-source projects face significant structural barriers:
1. **Triage Architecture & Commercial Trade-Offs**: While established platforms offer entry tiers (such as HackerOne's free Essential VDP), existing solutions typically operate on a server-managed triage model where exploit details are held unencrypted on vendor infrastructure and forwarded to external mailboxes or ticketing systems. Organizations desiring confidential triage are steered toward enterprise managed-service contracts ($15,000–$30,000+/year) where vendor staff review raw reports. Small teams who want confidential intake without delegating report access to third-party services currently lack a lightweight, privacy-preserving tool.
2. **Confidentiality & Insecure Communication**: Lacking dedicated cryptographic intake channels, small organizations receive security reports via plaintext email, public issue trackers, or social media direct messages. This unencrypted transit exposes sensitive zero-day vulnerability reproduction steps across intermediate mail servers and employee devices.
3. **The Remediation & Verification Gap**: Standard bug trackers treat vulnerability resolution as an informal status change (`Closed` or `Resolved`). There is rarely an explicit, verifiable connection between the vulnerability report, the code or configuration change intended to resolve it, and an attested retest outcome confirming the fix before closure.
4. **Legal Ambiguity & Onboarding Friction**: Early-stage engineering teams struggle to establish clear rules of engagement, RFC 9116 `security.txt` discovery policies, and safe-harbor terms without expensive legal counsel.

### 2.2 Proposed Solution & Commercial Value Proposition
BugBountyTrack is a focused B2B micro-VDP engineered specifically for small software engineering leads, CTOs, and product security owners who handle vulnerability reports manually:

> **Core Value Proposition**: *A confidential vulnerability reporting workspace that helps small software teams receive reports, coordinate fixes, and document how each issue was retested and closed.*

The platform differentiates itself through four architectural and operational pillars:
* **Client-Side Cryptographic Payload Isolation**: Sensitive exploit descriptions, reproduction steps, and proof-of-concept (PoC) attachments are encrypted directly in the browser using OpenPGP before transmission. To maximize researcher adoption and eliminate friction, researchers can submit findings without account registration using ephemeral Curve25519 keys and secret tracking URLs. To prevent sensitive title leakage in URLs, notification logs, and dashboards, titles are encrypted client-side (`title_ciphertext`) while exposing a neutral, server-readable operational category label (`operational_label` enum).
* **Evidence-Based Remediation & Attested Retest**: Decoupling the declaration of a fix from its verification, verifying commit existence and branch presence via the GitHub REST API v3, and enforcing an audited retest state machine with distinct, mutually exclusive terminal closure states (`VERIFIED_RESEARCHER`, `VERIFIED_INTERNAL`, `CLOSED_UNVERIFIED_TIMEOUT`, `RISK_ACCEPTED`, `REJECTED_SPAM`, `WITHDRAWN`).
* **Redacted Closure Evidence Exports**: Enabling engineering leads to generate customer-controlled, sanitized PDF/JSON closure evidence summaries that document the vulnerability's timeline, verified commit hash, deployment environment, and retest attestation without exposing raw exploit code. Included natively in the commercial Team plan ($49/mo).
* **Streamlined Onboarding & Disaster-Resilient Key Management**: Guiding engineering leads through domain DNS verification, browser-side cleartext-signed RFC 9116 `security.txt` generation, Disclose.io safe harbor configuration, and mandatory offline Organization Master Recovery Key export with test decryption verification in under 15 minutes.

---

## 3. Strategic Business & Academic Objectives

| Objective ID | Strategic Objective | Business & Academic Outcome | Target Evaluation Metric |
| :--- | :--- | :--- | :--- |
| **BO-1** | **Client-Side Payload Confidentiality & Curve25519 Pinning** | Protect sensitive exploit data from server-side database exposure by performing asymmetric OpenPGP encryption in the browser, pinning strictly to v4 Ed25519/X25519 keys (<50ms keygen) and Argon2 S2K key protection. | 100% of vulnerability descriptions, steps, attachments, and specific titles stored exclusively as ciphertext. 0 plaintext exploit bytes in database dumps. Keygen < 1.5s (NFR-02). |
| **BO-2** | **Standardized Discovery & Policy Publishing** | Enable small software teams to generate, cryptographically sign, and download standardized RFC 9116 `security.txt` files and Disclose.io-aligned reporting policies with verified domain ownership. | Browser-side generation of signed cleartext RFC 9116 `security.txt` and verified domain DNS TXT challenge (`_bbt-challenge.<domain>`). |
| **BO-3** | **Deterministic Severity Assessment** | Standardize vulnerability prioritization using the FIRST.org Common Vulnerability Scoring System (CVSS 3.1) Base metric specification. | 100% calculation accuracy across 45 canonical unique test vectors documented in `CVSS_TEST_FIXTURES.md` verified via `verify_cvss_engine.py`; mandatory recording of CVSS vector, score, assessor identity, and justification. |
| **BO-4** | **Remediation Traceability & Branch Membership** | Decouple fix declaration from fix verification by linking remediation claims to verifiable GitHub commit SHAs and verifying branch presence via GitHub compare API. | Verification of repository existence and target branch for 100% of code-linked remediation declarations; deployment environment and version string attestation. |
| **BO-5** | **Accountable Closure State Machine & Tamper-Evident Ledger** | Prevent premature or unverified bug closure through distinct terminal states, mandatory retest attestation records, configurable SLA timers, and a SHA-256 hash-chained audit ledger (`prev_hash`). | Every closed report shall have a recorded closure category and justification. Only successfully retested reports shall be labeled verified. Rejected, duplicate, risk-accepted, and timeout outcomes shall be reported separately. |
| **BO-6** | **Financial Viability & Merchant of Record Compliance** | Demonstrate zero-cost academic prototype viability on free cloud tiers ($0.00/mo) while defining a commercially compliant SaaS model using Lemon Squeezy as Merchant of Record (handling global tax and direct Pakistan bank payouts) with a $49/mo Team plan and free Open-Source tier. | Academic prototype operational cost bounded at $0.00/month; commercial production architecture validated within ~$61.00/month, fully covered with 2 paying customers ($98/mo gross). |

---

## 4. Stakeholder Ecosystem & User Classes

| Stakeholder Role | System Actor | Primary Responsibilities | Data Access Permissions |
| :--- | :--- | :--- | :--- |
| **Ethical Researcher** | `Hunter` / `Guest Hunter` | Discovers in-scope vulnerabilities; submits via guest intake or verified account; encrypts payloads client-side; conducts empirical retests upon notification. | Full access to own submitted reports (via session auth or secret tracking URL), encrypted communication lane with defender, public program policies. |
| **Organization Triage Lead** | `Defender` | Reviews intake; decrypts payloads in-browser using local private key; assigns CVSS scores; coordinates remediation; requests retests. | Full access to organization reports, internal triage notes, organization PGP key management, and remediation verification workflows. |
| **Organization Owner** | `Tenant Owner` | Manages tenant workspace, invites members, signs RFC 9116 policies, holds offline master recovery key, and manages subscription. | Administrative control over organization profile, domain DNS verification, member roles, billing subscription, and offline disaster recovery. |
| **Organization Member** | `Read-Only Member` | Monitors program operational health, SLA countdowns, and aggregate vulnerability counts without inspecting raw exploits. | Read-only visibility into non-sensitive report metadata (Report ID, operational category label, severity rating, current state, timestamps, SLA status). |
| **Platform Operator** | `SuperAdmin` | Provisions tenant accounts, monitors platform uptime, inspects rate-limiting logs, and manages platform abuse. | Administrative access to organization registry, domain verification challenges, and infrastructure telemetry. No access to private keys or encrypted payloads. |
| **Academic Evaluator** | `Supervisor / Faculty Panel` | Reviews project deliverables, validates state transitions, audits automated test coverage, and evaluates FYP defense. | Evaluator access to test execution logs, database migration scripts, architectural diagrams, and controlled demonstration instances. |

---

## 5. Detailed Functional Business Requirements

### BR-1: Multi-Tenant Workspace, Guided Onboarding & Access Governance
* **BR-1.1**: The system shall support multiple isolated organization workspaces hosted within a single multi-tenant database schema using tenant identifier bindings.
* **BR-1.2**: Access permissions shall be strictly enforced on the server across distinct roles: Tenant Owner (`ORG_OWNER`), Security Reviewer (`ORG_DEFENDER`), Read-Only Member (`ORG_READONLY`), and Researcher (`HUNTER`).
* **BR-1.3**: Users shall authenticate against the server using email and bcrypt/Argon2-hashed login passwords, backed by database-persisted session tokens stored in secure, HTTP-only cookies. Organization Owners and Defenders shall support Time-Based One-Time Password (TOTP) Multi-Factor Authentication. The login password is strictly separated from the local encryption passphrase.
* **BR-1.4**: Organizations shall be guided through a streamlined Onboarding Wizard covering domain DNS verification, policy definition, browser-side keypair generation, offline Organization Master Recovery Key export with test challenge, and RFC 9116 `security.txt` signing in under 15 minutes.
* **BR-1.5**: Organizations shall be able to configure public program profiles (`/programs/[slug]`) and launch private, invitation-only programs accessible via cryptographically tokenized invitation links.
* **BR-1.6**: The platform shall provide frictionless **Account-Less (Guest) Vulnerability Intake**: external researchers can submit vulnerability reports without registering an account. The client browser generates an ephemeral Curve25519 keypair, encrypts the report to the program defenders and organization recovery key, and provides the submitter with an opaque secret tracking URL (`/report/track/BBT-RPT-XXXX?token=<secret>`) to review replies and submit retests.

### BR-2: RFC 9116 Policy & Safe Harbor Generator
* **BR-2.1**: The platform shall automatically generate a compliant RFC 9116 text policy file available for download and preview at `/api/v1/programs/[slug]/security.txt`.
* **BR-2.2**: The `security.txt` content shall be signed in the browser using the organization's private signing key and exported as a standard OpenPGP cleartext signed document. The organization downloads this signed document and hosts it on their own root domain at `/.well-known/security.txt`, with the `Contact:` directive pointing back to BugBountyTrack's intake portal.
* **BR-2.3**: Verification of `security.txt` shall be performable using the organization's advertised public key.
* **BR-2.4**: The policy builder shall generate clear safe-harbor terms based on Disclose.io Core standards, explicitly stating authorized research activities, scope boundaries, and documented limitations without asserting universal third-party legal immunity.
* **BR-2.5**: Domain ownership shall be verified through automated DNS TXT record challenge verification (`_bbt-challenge.<domain>`) prior to program activation.

### BR-3: Browser-Side OpenPGP Cryptographic Intake & Neutral Labeling
* **BR-3.1**: Sensitive report fields (vulnerability title, vulnerability description, reproduction steps, impact analysis, and proof-of-concept attachments) shall be encrypted in the client browser using OpenPGP prior to network transit (`title_ciphertext`).
* **BR-3.2**: To enable operational filtering, dashboard queuing, and safe external notifications without leaking sensitive exploit details, the submitter shall select a neutral server-readable operational category label (`operational_label` enum: `AUTHENTICATION_BYPASS`, `INJECTION_VULNERABILITY`, `INFORMATION_DISCLOSURE`, `CROSS_SITE_SCRIPTING`, `ACCESS_CONTROL_ISSUE`, `DENIAL_OF_SERVICE`, `OTHER`).
* **BR-3.3**: Encryption shall utilize an OpenPGP multi-recipient envelope encrypting the payload to the program's authorized defenders (N ≤ 10), the organization's offline master recovery key, and the reporting researcher's key (or ephemeral report key).
* **BR-3.4**: The protection boundary shall strictly isolate ciphertext: application APIs and databases shall receive and persist only ciphertext for sensitive fields.
* **BR-3.5**: Private keys shall remain strictly within client-side storage, protected by local encryption passphrases derived via OpenPGP native Argon2 S2K. All keys are standardized on v4 Ed25519/X25519 Curve25519 algorithms (<50ms generation). RSA-4096 is deprecated and dropped to eliminate keygen stalls.
* **BR-3.6**: The platform documentation shall explicitly state the browser trust boundary: client-side cryptographic isolation protects against server-side database exposure, untrusted backend administrators, and compromised database dumps; it assumes a modern browser environment free of malicious DOM-modifying extensions.

### BR-4: Deterministic CVSS 3.1 Scoring Engine
* **BR-4.1**: The platform shall incorporate a pure TypeScript calculation engine strictly adhering to the FIRST.org CVSS 3.1 Base metric specification.
* **BR-4.2**: The engine shall calculate numeric scores (0.0 to 10.0) and qualitative ratings (None, Low, Medium, High, Critical) based on the eight Base metrics: Attack Vector (AV), Attack Complexity (AC), Privileges Required (PR), User Interaction (UI), Scope (S), Confidentiality (C), Integrity (I), and Availability (A).
* **BR-4.3**: The engine implementation shall be verified against the 45 canonical unique test vectors documented in `CVSS_TEST_FIXTURES.md` with 100% mathematical parity via `verify_cvss_engine.py`.
* **BR-4.4**: For every report, the schema shall decouple the researcher-suggested score (`cvss_suggested`) from the defender-assigned official score (`cvss_score`), recording assessor identity and textual justification.

### BR-5: Confidential Triage, Dual-Lane Messaging & SLA Timers
* **BR-5.1**: Authorized reviewers shall decrypt vulnerability payloads in-browser upon unlocking their local private key.
* **BR-5.2**: The platform shall provide a dual-lane discussion interface:
  * **Researcher–Organization Conversation**: Confidential threaded messages encrypted for Submitter + Program Defenders + Org Recovery Key.
  * **Internal Reviewer Notes**: Private notes encrypted exclusively for Program Defenders + Org Recovery Key, completely inaccessible to the researcher.
* **BR-5.3**: Outbound notifications (via email or Slack-compatible webhooks) shall convey operational metadata only (e.g., "New update on Report #BBT-104 [AUTHENTICATION_BYPASS]") with an authenticated link, never transmitting exploit details over external notification rails.
* **BR-5.4**: The system shall track SLA countdown timers based on severity (Critical: 48h initial triage, 14d fix; High: 72h triage, 30d fix), displaying visual alerts and dispatching automated reminders via hourly scheduled checks.
* **BR-5.5**: Duplicate management shall be reviewer-driven: reviewers may link related reports internally after authorized decryption without leaking details between unrelated researchers.

### BR-6: Automated VCS Integration & Remediation Evidence
* **BR-6.1**: When declaring a vulnerability fix, the organization shall propose remediation evidence categorized by type: code repository commit or non-code configuration change.
* **BR-6.2**: For code fixes, the platform shall query the GitHub REST API v3 to verify that the referenced commit SHA exists and confirm its inclusion on the target repository branch using the GitHub compare API across public or private repositories (with organization Personal Access Tokens encrypted at rest).
* **BR-6.3**: For non-code infrastructure remediations (e.g., WAF rules, cloud policies), the browser shall compute a cryptographic SHA-256 hash of the configuration document locally before transmission to establish an immutable evidence baseline without hosting proprietary configuration files on the platform.
* **BR-6.4**: Remediation declarations shall explicitly record the target deployment environment (Staging, Pre-Production, Production) and version string where the fix is accessible for retesting.

### BR-7: Attested Retest State Machine, Accountable Closure & Redacted Exports
* **BR-7.1**: The platform shall enforce an explicit, audited lifecycle state machine:
  `NEW → TRIAGING → ACCEPTED → FIX_PROPOSED → RETEST_PENDING → [TERMINAL STATE]`
* **BR-7.2**: Intermediary exception states shall be formally supported: `NEED_MORE_INFO` (with automated 14-day inactivity timeout), `REJECTED_SPAM` (direct closure of noise from `NEW`), `REJECTED_INVALID`, and `DUPLICATE`.
* **BR-7.3**: Reports shall transition from `RETEST_PENDING` to final closure exclusively under one of three distinct terminal states:
  * `VERIFIED_RESEARCHER`: The reporting researcher independently retested and certified that the vulnerability is mitigated on the deployment environment.
  * `VERIFIED_INTERNAL`: An authorized organization reviewer certified the fix, recording whether they authored the fix.
  * `CLOSED_UNVERIFIED_TIMEOUT`: Closed following an expired researcher grace period (≥ 14 days) **only through an explicit authorized reviewer action with recorded justification**.
* **BR-7.2**: From `RETEST_PENDING`, reports shall transition to final closure exclusively under one of three distinct terminal states:
  * `VERIFIED_RESEARCHER`: The reporting researcher independently confirmed the vulnerability is mitigated on the target deployment.
  * `VERIFIED_INTERNAL`: An authorized organization reviewer certified the fix, recording whether they authored the fix.
  * `CLOSED_UNVERIFIED_TIMEOUT`: Closed following an expired researcher grace period (≥ 14 days) **only through an explicit authorized reviewer action with recorded administrative justification**. Never counted as a verified fix.
* **BR-7.3**: Additional terminal states include:
  * `CLOSED_INCOMPLETE`: Clarification inquiry (`NEED_MORE_INFO`) expired after 14 days of researcher inactivity at intake. Distinct from `CLOSED_UNVERIFIED_TIMEOUT` (which applies only to deployed fixes awaiting retest).
  * `RISK_ACCEPTED`: Formal organization acceptance of operational risk without code modification. Requires an authorized decision-maker (`ORG_OWNER` or Lead Defender), a mandatory written business and security rationale, and a scheduled review date. Under no circumstances does `RISK_ACCEPTED` count as a passed retest or verified remediation.
  * `REJECTED_SPAM`, `REJECTED_INVALID`, `DUPLICATE`, and `WITHDRAWN`.
* **BR-7.4**: Reports in `NEED_MORE_INFO` shall automatically transition to `CLOSED_INCOMPLETE` after 14 days of researcher inactivity without clarification, preserving the audit record. Reopening is permitted if the researcher subsequently provides the required clarification.
* **BR-7.5**: If retesting reveals that the vulnerability persists, the state transition shall record a `RETEST_FAILED` audit event and return to `ACCEPTED`, preserving the failed retest evidence in the immutable audit log.
* **BR-7.6**: Reopening any closed report shall require an authorized Defender or Tenant Owner action recording an immutable justification log, transitioning the ticket back to `TRIAGING`.
* **BR-7.7**: The platform shall generate exportable Redacted Closure Evidence summaries (PDF and JSON format) capturing the operational label, report lifecycle timestamps, verified commit SHA/branch, deployment environment, retest attestations, and closing officer identity, suitable for sharing with enterprise clients and security auditors without disclosing raw exploit instructions.

### BR-8: Application Hardening, Defensive Controls & Storage Quotas
* **BR-8.1**: Decrypted Markdown content shall be sanitized prior to DOM rendering using an Abstract Syntax Tree (AST) parser (`unified` / `remark-parse` / `rehype-sanitize`) enforcing strict HTML element and attribute allowlists to neutralize Stored Cross-Site Scripting (XSS).
* **BR-8.2**: The platform shall enforce database-level Row-Level Security (RLS) in PostgreSQL, dynamically scoping connection queries to the authenticated tenant context within interactive transactions (`SET LOCAL app.current_tenant_id`).
* **BR-8.3**: Public report submission endpoints shall be protected by shared store rate limiting (Postgres / Upstash) and Cloudflare Turnstile CAPTCHA (5 submissions / hour / IP).
* **BR-8.4**: Attachments up to 25 MB shall be uploaded directly from the browser to Cloudflare R2 using presigned URLs requested from `/api/uploads/presign`, bypassing serverless function payload size ceilings. Quotas (2 GB demo, 10 GB Team) shall be validated at URL issuance time, and unconfirmed uploads shall be cleaned up by an automated orphan cleanup job.
* **BR-8.5**: The audit ledger shall enforce strict append-only constraints with a SHA-256 `prev_hash` cryptographic chain: database permissions on `audit_events` shall permit `INSERT` and `SELECT` operations only, strictly preventing `UPDATE` and `DELETE` actions by any application role.

---

## 6. Scope Boundaries & Anti-Goals

To maintain high engineering fidelity and realistic delivery boundaries, the following capabilities are explicitly declared out of scope for the initial product baseline:
1. **No Direct Banking Payout Rails in MVP**: The initial launch omits real-money banking payout rails (Stripe Connect, ACH, SEPA) and tax compliance forms (W-8BEN / W-9). If demonstration awards are shown, they shall be modeled as explicitly simulated credit/point records.
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
   * *Remediation Verification Ratio*: Every closed report shall have a recorded closure category and justification. Only successfully retested reports shall be labeled verified. Rejected, duplicate, risk-accepted, and unverified-timeout outcomes shall be reported separately.
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
When transitioning to paid commercial operations serving early B2B customers, the infrastructure shifts to commercially supported tiers with dedicated SLAs, custom domains, and hourly crons:

| Infrastructure Layer | Commercial Provider | Provisioned Commercial Tier | Purpose & Quota | Monthly Cost ($USD) |
| :--- | :--- | :--- | :--- | :---: |
| **Application & API Gateway** | Vercel Pro | Pro Team Tier ($20 / seat) | Commercial license, hourly SLA crons, zero cold starts | **$20.00** |
| **Production Database** | Neon Serverless | Launch Tier (Usage-Based) | PostgreSQL 16 (~180 CU-hrs compute reserve + 10 GB storage at $0.106/CU-hr) | **~$19.00** |
| **Encrypted Object Storage** | Cloudflare R2 | Pay-As-You-Go ($0.015/GB-mo) | Encrypted report attachments, 50 GB pooled baseline, zero egress fees | **$0.75** |
| **Transactional Email Delivery** | Resend / Postmark Pro | Essential Commercial Tier | High deliverability minimal-metadata notifications (50,000/mo) | **$20.00** |
| **Domain & DNS Registration** | Cloudflare Registrar | `.com` / `.security` TLD | Amortized domain registrar fee ($15.00/year) | **$1.25** |
| **Merchant of Record Gateway** | Lemon Squeezy | MoR Billing & Global Tax | Handles global VAT, sales tax, direct bank payouts to Pakistan (5% base + 50¢/tx + 0.5% subscription fee) | **Variable** |
| **TOTAL PRODUCTION OPERATING BASELINE** | — | — | **Commercial Production Cloud Baseline (10–25 Tenants)** | **~$61.00 / mo** |

### 8.3 Commercial SaaS Subscription Pricing Model (Validation Hypotheses)
To ensure financial viability and recover cloud operational costs, BugBountyTrack adopts a focused commercial pricing model:

| Subscription Tier | Proposed Price | Target Customer Hypothesis | Included Features & Quota Bounds |
| :--- | :---: | :--- | :--- |
| **Open Source / Community** | **$0 / mo** | Open-source libraries, solo maintainers & non-profits | 1 active public program, 1 defender seat, up to 5 simultaneously active open reports (if a 6th report is submitted while 5 remain active, intake still encrypts and accepts the payload, displaying a non-blocking quota banner to triage/resolve open tickets or upgrade, guaranteeing zero data loss for security disclosures), 2 GB encrypted storage, signed RFC 9116 generator, GitHub commit verification. |
| **Team Launch Plan** | **$49 / mo** | Small software engineering teams (5–25 devs) needing structured intake | 1 active disclosure program (public or invite-only), up to 5 defender seats (with program-scoped decryption), 10 GB encrypted storage, direct presigned R2 uploads, SLA countdown timers, Slack-compatible webhooks, GitHub commit & branch compare verification, Redacted PDF/JSON Closure Evidence exports. |

#### Financial Unit Economics & Payout Modeling
* **Gross Revenue (2 Paying Customers)**: 2 × $49.00 = **$98.00 / month**.
* **Lemon Squeezy Base Fees**: 5% base ($4.90) + $0.50/transaction ($1.00) + 0.5% recurring subscription fee ($0.49) = **$6.39 total fees**.
* **Base Net Revenue**: $98.00 − $6.39 = **$91.61 / month**.
* **International Card & Transfer Mix Modeling**:
  * *Domestic US Cards*: Net = **$91.61** (covers 150% of the ~$61.00/mo operating baseline).
  * *International Cards (+1.5% surcharge, $1.47)*: Net = **$90.14**.
  * *Bank Payout to Pakistan via Stripe Connect Rails (1% payout fee)*: Net received = **$89.24 – $90.69**.
* In all modeled payment scenarios, 2 paying customers reliably cover 100% of the commercial cloud baseline (~$61.00/mo) with a healthy operating margin. All pricing figures represent initial validation hypotheses subject to empirical testing during the commercial pilot.

---

*--- End of Business Requirements Document (BRD) ---*
