# Week 2 Task & Deliverable: Software Requirements Specification (SRS)

| Attribute | Details |
| :--- | :--- |
| **Project ID** | `PTUT - PRJ - 089` |
| **Project Title** | **BugBountyTrack — Private Bug Bounty & Vulnerability Disclosure Platform** |
| **Student Author** | Taha Asadullah (Roll No: `24-ST-013`, Section: `SET-B`) |
| **Academic Supervisor** | Sir Umar Hayat (Assistant Professor, PTUT Lahore) |
| **Milestone** | **Week 2** — Software Requirements Specification (**Gate 1: DoR Part II**) |
| **Standard Compliance** | IEEE Std 830-1998 / ISO/IEC/IEEE 29148:2018 |
| **WBS Task IDs** | `WP-1.1` (8h), `WP-1.2` (12h), `WP-1.3` (10h), `WP-1.4` (10h) — **Sprint 1 Baseline** |

---

## Supporting Deliverable Document (Google Drive Link)

| Deliverable Document | Scope Covered | Google Drive Link |
| :--- | :--- | :--- |
| **Formal IEEE 830 Software Requirements Specification (`SRS.docx`)** | Complete IEEE 830 SRS, Functional Requirements (`FR-1` to `FR-8`), Formal Use Case Specifications (`UC-01` to `UC-07`), 4 UML Behavioral Diagrams, Quantifiable NFRs (`NFR-01` to `NFR-09`), and Traceability Matrix | [View IEEE 830 Software Requirements Specification (Google Drive)](PASTE_GOOGLE_DRIVE_LINK_FOR_SRS_DOCX_HERE) |

---

## Part 1: Formal IEEE 830 Software Requirements Specification (SRS) Overview & Functional Requirements

The formal **IEEE Std 830-1998 / ISO/IEC/IEEE 29148:2018 Software Requirements Specification (`SRS`)** establishes a complete, unambiguous, verifiable, and traceable engineering baseline for **BugBountyTrack**. Every functional requirement (`FR-1.1` through `FR-8.5`) maps directly to our Week 1 Problem Statement, our 2 Target User Personas (**Alex Rivera — "The Hunter"** and **Sarah Chen — "The Defender"**), and our **5 Core MVP Features**:

| SRS Module | Requirement Range | Core Functional Specification Summary |
| :--- | :---: | :--- |
| **3.1 Multi-Tenant Workspace, Identity & Access Governance** | `FR-1.1` – `FR-1.6` | Isolated `organization_id` workspaces; 4 RBAC roles (`ORG_OWNER`, `ORG_DEFENDER`, `ORG_READONLY`, `HUNTER`) plus program-level `PROGRAM_DEFENDER` key-recipient authorization; Argon2id/Bcrypt credential hashing (`cost >= 12`), TOTP MFA (`totp_secret` AES-256-GCM encrypted at rest), and immediate session revocation on password reset; Guided Onboarding Wizard with mandatory offline **Organization Master Recovery Key** (`recovery_public_key`) decryption challenge; Account-Less Guest Submission (`guest_actor_id`, `guest_token_hash`, URI fragment `#token=<secret>`, and downloadable `.bbt-recovery.json` Recovery Package); and SHA-256 hashed Private Program Invitation Tokens (`token_hash`). |
| **3.2 RFC 9116 `security.txt` Policy & Safe Harbor Engine (MVP Feature 1)** | `FR-2.1` – `FR-2.5` | Automated generation of RFC 9116 compliant `/.well-known/security.txt` manifests (`Contact`, `Encryption`, `Policy`, `Acknowledgments`, `Preferred-Languages`, `Canonical`, and `Expires` <= 365 days); **in-browser** OpenPGP cleartext signing (`-----BEGIN PGP SIGNED MESSAGE-----`) using the organization's private Ed25519 signing key without exposing private keys to the server; structured asset scope classification (`IN_SCOPE` vs. `OUT_OF_SCOPE`); Safe Harbor legal clauses; and automated DNS TXT (`_bbt-challenge.<domain>`) ownership verification. |
| **3.3 Zero-Knowledge Client-Side Cryptographic Pipeline (MVP Feature 2)** | `FR-3.1` – `FR-3.6` | Client-side RFC 9580 v6 Curve25519 (`Ed25519` signing + `X25519` encryption) keypair generation (`< 50 ms` bare keygen benchmark target) via `OpenPGP.js v6` and WebCrypto API; private keys encrypted locally via Argon2id S2K (`~200–400 ms` intentional unlock delay) in browser `IndexedDB` (zero `localStorage`); multi-recipient PKESK encryption across all active `PROGRAM_DEFENDER` subkeys, the offline `recovery_public_key`, and the reporter's key; encrypted report title (`title_ciphertext`) paired with a coarse `operational_label` enum for zero-plaintext queue sorting; `recipient_set_version` optimistic concurrency guard (`409 Conflict` on stale keyring); direct-to-Cloudflare R2 presigned encrypted attachment uploads (`<= 25 MB`); and strict post-logout memory zeroization (`Uint8Array.fill(0)`). |
| **3.4 Deterministic CVSS v3.1 Base Severity Calculator (MVP Feature 3)** | `FR-4.1` – `FR-4.4` | Pure TypeScript engine implementing all 8 FIRST.org CVSS v3.1 Base metrics (`AV`, `AC`, `PR`, `UI`, `S`, `C`, `I`, `A`), canonical vector parser/serializer (`CVSS:3.1/AV:_/AC:_/PR:_/UI:_/S:_/C:_/I:_/A:_`), official `RoundUp` ceiling function to 1 decimal place, exact exploitability coefficient `8.22`, and immutable assessment audit logging verified at 100% mathematical parity across **45 FIRST.org and NIST NVD test vectors** (`CVSS_TEST_FIXTURES.md`). |
| **3.5 Confidential Triage, Dual-Lane Threading & SLA Engine** | `FR-5.1` – `FR-5.5` | In-browser payload decryption and `rehype-sanitize` AST neutralization prior to DOM rendering; Dual-Lane Encrypted Threading separating `RESEARCHER_ORG` conversation from `REVIEWER_INTERNAL` notes; metadata-only email notifications (Resend/Postmark) that never transmit vulnerability titles or exploit details; and an hourly SLA countdown engine (`Critical: 48h triage / 14d fix`, `High: 72h / 30d`, `Medium: 7d / 90d`, `Low: 14d / 180d`). |
| **3.6 Git-Linked Remediation & Evidence Verification (MVP Feature 4)** | `FR-6.1` – `FR-6.4` | Mandatory dual-path remediation evidence before transitioning `ACCEPTED -> FIX_PROPOSED -> RETEST_PENDING`: (a) `CODE_COMMIT` verified via GitHub REST API v3 (`/repos/{owner}/{repo}/commits/{sha}` and `/compare/{base}...{head}` confirming commit existence and branch inclusion), or (b) `CONFIG_INFRASTRUCTURE` binding a 64-character SHA-256 configuration artifact hash and target deployment environment (`Staging`, `Pre-Production`, `Production`). |
| **3.7 Attested Retest State Machine & Redacted Exports (MVP Feature 5)** | `FR-7.1` – `FR-7.7` | Strict 13-state deterministic FSM (`NEW`, `TRIAGING`, `NEED_MORE_INFO`, `ACCEPTED`, `FIX_PROPOSED`, `RETEST_PENDING`, `VERIFIED_RESEARCHER`, `VERIFIED_INTERNAL`, `CLOSED_UNVERIFIED_TIMEOUT`, `CLOSED_INCOMPLETE`, `RISK_ACCEPTED`, `DUPLICATE`, `REJECTED_INVALID`, `REJECTED_SPAM`, `WITHDRAWN`); 3 distinct retest outcomes (`VERIFIED_RESEARCHER`, `VERIFIED_INTERNAL`, `CLOSED_UNVERIFIED_TIMEOUT`, plus `RETEST_FAILED` automatic loopback to `ACCEPTED`); audited regression reopening; and Redacted Closure Evidence Export (PDF & JSON). |
| **3.8 Application Hardening, Tenant RLS & Audit Ledger** | `FR-8.1` – `FR-8.5` | `rehype-sanitize` Markdown AST XSS neutralization; PostgreSQL 16 Row-Level Security (`SET LOCAL app.current_tenant_id`); shared rate limiter (`5 submissions/hr/IP`) and Cloudflare Turnstile CAPTCHA; bounded evaluation tenant storage quotas (`50 MB` PostgreSQL DB and `2 GB` Cloudflare R2; 90% warning, 100% HTTP `413` rejection); and append-only hash-chained `audit_events` ledger (`INSERT` and `SELECT` only, SHA-256 `prev_hash`). |

---

## Part 2: Formal Use Case Specifications (`UC-01` to `UC-07`) & UML Behavioral Diagrams

### 2.1 System Use Case Diagram (`Figure 4.1`)

![Figure 4.1: System Use Case Diagram](../requirements/diagrams/fig4_2_usecase.png)

### 2.2 Formal Textual Use Case Specifications

#### Use Case `UC-01`: Submit Encrypted Vulnerability Report & Generate Recovery Package
* **Primary Actor**: Ethical Security Researcher (`Hunter` or `Guest Hunter`).
* **Preconditions**: Researcher is viewing an organization's active public program page (or possesses a valid private program invitation token `token_hash`).
* **Main Success Scenario**:
  1. Researcher selects an in-scope target asset, chooses a coarse neutral category (`operational_label` enum), and inputs the specific vulnerability title, reproduction steps, and optional PoC attachment (`<= 25 MB`).
  2. Browser generates an ephemeral RFC 9580 v6 Curve25519 keypair in memory (`< 50 ms` benchmark target) and fetches the program's active `PROGRAM_DEFENDER` encryption subkeys (`recipient_set_version`) plus `recovery_public_key`.
  3. Browser generates an ephemeral AES-256 session key, encrypts both the title (`title_ciphertext`) and body payload into an OpenPGP message, and wraps the session key in PKESK packets for all active `PROGRAM_DEFENDER` subkeys, the offline `recovery_public_key`, and the reporter's key.
  4. If an attachment is included, browser requests a presigned URL from `/api/uploads/presign` and streams the encrypted binary directly to Cloudflare R2.
  5. Browser submits `operational_label`, `recipient_set_version`, `title_ciphertext`, and `encrypted_payload` to the API gateway.
  6. Server validates Cloudflare Turnstile CAPTCHA, rate limits, tenant storage quota, and `recipient_set_version`, persists the ciphertext in PostgreSQL, issues a durable `guest_actor_id` and `guest_token_hash`, displays the Secret Tracking URL (`/report/track/BBT-RPT-XXXX#token=<secret>`) scrubbed via `window.history.replaceState`, and triggers download of the `.bbt-recovery.json` Guest Recovery Package. Report enters state `NEW`.
* **Extensions**:
  * *2a. Organization public key missing or invalid*: Browser blocks submission and alerts user.
  * *5a. Stale `recipient_set_version`*: Server returns HTTP `409 Conflict`; browser refreshes recipient keyring and re-encrypts automatically.
  * *6a. Rate limit (`> 5 req/hr/IP`) or storage quota (`> 100%`) exceeded*: Server returns HTTP `429 Too Many Requests` or `413 Payload Too Large`.

#### Use Case `UC-02`: Decrypt & Triage Vulnerability Report
* **Primary Actor**: Organization Triage Lead (`Defender`).
* **Preconditions**: Authenticated with `ORG_DEFENDER` role and active `PROGRAM_DEFENDER` membership; report is in state `NEW` or `TRIAGING`.
* **Main Success Scenario**:
  1. Defender opens report view; browser fetches encrypted payload and retrieves local private key from `IndexedDB`.
  2. Defender enters local passphrase to unlock the Argon2id S2K-protected private key (`~200–400 ms` intentional delay).
  3. Browser decrypts `title_ciphertext` and body ciphertext in memory, passes Markdown through `rehype-sanitize` AST parser, and renders sanitized HTML.
  4. Defender posts encrypted messages in either the Researcher–Organization lane (`RESEARCHER_ORG`) or Reviewer Internal Notes lane (`REVIEWER_INTERNAL`), evaluates the 8 CVSS v3.1 Base metrics, and updates state to `ACCEPTED`.
  5. Server records the CVSS v3.1 vector, score, and SHA-256 hash-chained `AUDIT_EVENT`.
* **Extensions**:
  * *2a. Incorrect passphrase*: Browser displays decryption error; private key remains locked.
  * *4a. Missing reproduction details*: Defender transitions state to `NEED_MORE_INFO` (auto-transitions to `CLOSED_INCOMPLETE` after `>= 14 days` of researcher inactivity).
  * *4b. Duplicate submission*: Defender links canonical parent Report ID and transitions state to `DUPLICATE`.
  * *4c. Out of scope or invalid*: Defender cites policy rule and transitions state to `REJECTED_INVALID`.
  * *4d. Automated scanner noise*: Defender transitions state directly from `NEW` to `REJECTED_SPAM`.

#### Use Case `UC-03`: Propose Remediation Evidence
* **Primary Actor**: Organization Triage Lead (`Defender`).
* **Preconditions**: Report is in state `ACCEPTED`.
* **Main Success Scenario**:
  1. Defender selects "Propose Remediation", chooses evidence type `CODE_COMMIT` or `CONFIG_INFRASTRUCTURE`, and specifies target deployment environment (`Staging`, `Pre-Production`, `Production`).
  2. *Path A (`CODE_COMMIT`)*: Defender inputs repository URL, target remediation branch, and 40-character Git Commit SHA. Server queries GitHub REST API v3 (`/repos/{owner}/{repo}/commits/{sha}` and `/compare/{base}...{head}`) and verifies commit existence and branch inclusion.
  3. *Path B (`CONFIG_INFRASTRUCTURE`)*: Browser computes a 64-character SHA-256 hash of the configuration artifact via WebCrypto and submits it with the remediation summary.
  4. Server persists `REMEDIATION_RECORD`, transitions report state through `FIX_PROPOSED` to `RETEST_PENDING`, records a hash-chained `AUDIT_EVENT`, and dispatches a metadata-only retest invitation email to the researcher.
* **Extensions**:
  * *2a. Commit SHA not found or not on target branch*: Server returns HTTP `422 Unprocessable Entity`; state remains `ACCEPTED`.

#### Use Case `UC-04`: Execute Attested Retest & Export Closure Evidence
* **Primary Actor**: Ethical Security Researcher (`Hunter` / `Guest Hunter`) and Organization Triage Lead (`Defender`).
* **Preconditions**: Report is in state `RETEST_PENDING`.
* **Main Success Scenario**:
  1. Researcher inspects the linked remediation commit/configuration hash and re-tests the target asset.
  2. Researcher submits a signed retest attestation confirming the vulnerability is resolved.
  3. Server transitions report state to `VERIFIED_RESEARCHER` and appends an immutable `AUDIT_EVENT`.
  4. Defender generates a **Redacted Closure Evidence Export** (PDF & JSON) containing the lifecycle timeline, CVSS 3.1 vector, commit SHA/config hash, deployment environment, and cryptographic hash-chain proof—excluding all raw exploit payloads.
* **Extensions**:
  * *2a. Patch incomplete (`RETEST_FAILED`)*: Researcher submits reproduction proof; report automatically loops back to `ACCEPTED`.
  * *2b. Internal verification (`VERIFIED_INTERNAL`)*: Defender certifies the fix internally with empirical test evidence and conflict-of-interest disclosure.
  * *2c. Researcher unresponsive (`>= 14 days`)*: Defender closes report under `CLOSED_UNVERIFIED_TIMEOUT` with mandatory administrative rationale.

#### Use Case `UC-05`: Restore Guest Session via Recovery Package
* **Primary Actor**: Account-Less Ethical Security Researcher (`Guest Hunter`).
* **Preconditions**: Guest possesses a downloaded `.bbt-recovery.json` Recovery Package on a new browser or device.
* **Main Success Scenario**:
  1. Guest navigates to `/report/restore` and selects the `.bbt-recovery.json` file.
  2. Browser validates JSON schema (`version: 1`) and verifies SHA-256 `checksum` integrity in memory.
  3. Browser imports `encrypted_private_key` into local `IndexedDB` and authenticates the session using `access_token` (`guest_token_hash`) while preserving durable `guest_actor_id` attribution.
  4. Browser redirects to `/report/track/BBT-RPT-XXXX` and decrypts historical and new messages seamlessly.

#### Use Case `UC-06`: Onboard Tenant, Verify DNS & Configure RFC 9116 / Master Recovery Key
* **Primary Actor**: Organization Owner (`ORG_OWNER`).
* **Preconditions**: Authenticated user creating or configuring an organization workspace.
* **Main Success Scenario**:
  1. Owner completes the Guided Onboarding Wizard and publishes the `_bbt-challenge.<domain>` DNS TXT record verified by the server.
  2. Browser generates RFC 9580 v6 Curve25519 defender keys and the offline **Organization Master Recovery Key** (`recovery_public_key`).
  3. Owner downloads the Argon2id-protected private recovery key and passes the mandatory in-browser test decryption challenge (`Uint8Array` zeroized immediately after verification).
  4. Owner assigns authorized defenders to `PROGRAM_DEFENDER` (incrementing `recipient_set_version`) and cleartext-signs the generated RFC 9116 `security.txt` policy in-browser for publication at `/.well-known/security.txt`.

#### Use Case `UC-07`: Enforce SLA Escalation Timers & Verify Hash-Chained Audit Ledger
* **Primary Actor**: Organization Reviewer (`Defender`), Read-Only Auditor (`ORG_READONLY`), or System Cron.
* **Preconditions**: Active vulnerability reports exist within the tenant workspace.
* **Main Success Scenario**:
  1. Hourly SLA countdown engine evaluates `sla_triage_due` and `sla_remediation_due` deadlines across active reports.
  2. Approaching or breached SLA targets trigger metadata-only email and webhook alerts without exposing exploit details.
  3. Reviewers and read-only auditors inspect the append-only `audit_events` ledger (`INSERT` and `SELECT` only) and verify cryptographic `prev_hash` SHA-256 chain continuity.

### 2.3 Sequence & Lifecycle Behavioral Diagrams (`Figure 4.2` to `Figure 4.4`)

* **Figure 4.2: Sequence Diagram — Browser-Side OpenPGP Submission (`UC-01`)**:
  ![Figure 4.2: Browser-Side OpenPGP Submission](../requirements/diagrams/fig4_3_seq_submission.png)
* **Figure 4.3: Sequence Diagram — In-Browser Decryption & Confidential Triage (`UC-02`)**:
  ![Figure 4.3: In-Browser Decryption & Confidential Triage](../requirements/diagrams/fig4_4_seq_decryption.png)
* **Figure 4.4: State Machine Diagram — Remediation & Attested Retest Lifecycle (`UC-03` & `UC-04`)**:
  ![Figure 4.4: Remediation & Attested Retest Lifecycle State Machine](../requirements/diagrams/fig4_5_statemachine.png)

---

## Part 3: Quantifiable Non-Functional Requirements (`NFR-01` to `NFR-09` — Latency, Security & Uptime)

| NFR ID | Quality Pillar | Quantifiable Engineering Metric / Threshold | Verification Method |
| :---: | :--- | :--- | :--- |
| **`NFR-01`** | **Latency (Server API)** | `p95 <= 300 ms` warm (`<= 1,200 ms` cold) under 10–50 concurrent requests | Automated k6 / Supertest latency benchmark |
| **`NFR-02`** | **Latency (Client Crypto)** | `< 50 ms` Curve25519 keygen; `~200–400 ms` Argon2id S2K; `<= 1,500 ms` total encrypt | Browser WebCrypto / OpenPGP.js timing suite |
| **`NFR-03`** | **Security (Tenant RLS)** | `0` cross-tenant rows returned via `SET LOCAL app.current_tenant_id` | Multi-tenant RLS boundary integration test (`TC-SEC-01`) |
| **`NFR-04`** | **Accessibility (WCAG 2.2)** | `>= 24x24 px` touch targets (`44x44 px` mobile nav); `>= 4.5:1` contrast | Automated axe-core / Lighthouse accessibility audit |
| **`NFR-05`** | **Security (XSS & CSP)** | `100%` neutralization of OWASP XSS corpus via `rehype-sanitize` + strict CSP | OWASP XSS vector corpus unit test (`TC-SEC-02`) |
| **`NFR-06`** | **Reliability (Storage Quotas)** | `50 MB` DB / `2 GB` R2 per tenant; warn at `90%`, block with HTTP `413` at `100%` | Quota boundary rejection test (`TC-SEC-04`) |
| **`NFR-07`** | **Security (Audit Integrity)** | `INSERT` & `SELECT` only (`0` `UPDATE`/`DELETE`); SHA-256 `prev_hash` chain | PostgreSQL privilege & hash-chain verification (`TC-SEC-05`) |
| **`NFR-08`** | **Determinism & SLA Accuracy** | `100%` CVSS 3.1 parity (`45/45` vectors); hourly SLA cron (`<= 60 min` drift) | CVSS fixture suite (`TC-CVSS-01`) & SLA timer test (`TC-SLA-01`) |
| **`NFR-09`** | **Uptime & Continuity** | **`>= 99.5%` monthly uptime** (`<= 3.65h/mo` downtime); **`RPO <= 24h`**, **`RTO <= 4h`** | 5-minute `/api/v1/health` probes & backup restore drill (`TC-OPS-01`) |

---

## Document Endorsement & Milestone Sign-Off

This Week 2 Software Requirements Specification (`SRS`) is formally submitted and endorsed as the IEEE 830 / ISO/IEC/IEEE 29148 requirements baseline for **BugBountyTrack** (`PTUT - PRJ - 089`) under the Department of Software Engineering Technology, Punjab Tianjin University of Technology (PTUT), Lahore.

| Role | Name & Designation | Roll No. / Section | Signature | Date |
| :--- | :--- | :--- | :--- | :--- |
| **Student Author** | **Taha Asadullah** (B.Sc. Software Engineering Technology) | `24-ST-013` / `SET-B` | *Signed: Taha Asadullah* | October 11, 2026 |
| **Project Supervisor** | **Sir Umar Hayat** (Assistant Professor, Dept. of SET, PTUT) | Faculty Supervisor | ______________________ | ____________ |
