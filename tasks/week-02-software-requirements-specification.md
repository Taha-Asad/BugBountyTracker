# Week 2 Task & Deliverable: Software Requirements Specification (SRS)

| Attribute | Details |
| :--- | :--- |
| **Project ID** | `PTUT - PRJ - 089` |
| **Project Title** | **BugBountyTrack — Private Bug Bounty & Vulnerability Disclosure Platform** |
| **Student Author** | Taha Asadullah (Roll No: `24-ST-013`, Section: `SET-B`) |
| **Academic Supervisor** | Sir Umar Hayat (Assistant Professor, PTUT Lahore) |
| **Milestone** | **Week 2** — Software Requirements Specification (**Gate 1: DoR Part II**) |
| **Standard Compliance** | IEEE Std 830-1998 / ISO/IEC/IEEE 29148:2018 (`SRS v2.1.0`) |
| **WBS Task IDs** | `WP-1.1` (8h), `WP-1.2` (12h), `WP-1.3` (10h), `WP-1.4` (10h) — **Sprint 1 Baseline** |

---

## Part 1: Formal IEEE 830 Software Requirements Specification (SRS) Overview & Functional Requirements

The formal **IEEE Std 830-1998 / ISO/IEC/IEEE 29148:2018 Software Requirements Specification (`SRS v2.1.0`)** establishes a complete, unambiguous, verifiable, and traceable engineering baseline for **BugBountyTrack**. Every functional requirement (`FR-1.1` through `FR-9.2`) is mapped directly to our 5 Core MVP Features and verified via deterministic acceptance criteria:

| SRS Module | Requirement Range | Core Functional Specification Summary |
| :--- | :---: | :--- |
| **3.1 Multi-Tenant Workspace, Identity & Access Management** | `FR-1.1` – `FR-1.7` | Cryptographically isolated `ORGANIZATION` workspaces; 4 RBAC roles (`Owner`, `Defender`, `Hunter`, `ReadOnly`) plus program-level `PROGRAM_DEFENDER` key-recipient authorization; Argon2id/Bcrypt credential hashing (`cost >= 12`), TOTP MFA (`totp_secret` AES-256-GCM encrypted at rest), and immediate session revocation on password reset; Guided Onboarding Wizard with mandatory offline **Organization Master Recovery Key** (`recovery_public_key`) decryption challenge; Account-Less Guest Submission (`guest_actor_id`, `guest_token_hash`, URI fragment `#token=<secret>`, and downloadable `.bbt-recovery.json` Recovery Package); and SHA-256 hashed Private Program Invitation Tokens (`token_hash`). |
| **3.2 RFC 9116 `security.txt` Policy & Safe Harbor Engine** | `FR-2.1` – `FR-2.5` | Automated generation of RFC 9116 compliant `/.well-known/security.txt` manifests (`Contact`, `Encryption`, `Policy`, `Acknowledgments`, `Preferred-Languages`, `Canonical`, and `Expires` <= 365 days); **in-browser** OpenPGP cleartext signing (`-----BEGIN PGP SIGNED MESSAGE-----`) using the organization's private Ed25519 signing key without exposing private keys to the server; structured asset scope classification (`IN_SCOPE` vs. `OUT_OF_SCOPE`); Safe Harbor legal clauses; and automated DNS TXT (`_bugbountytrack-challenge.<domain>`) ownership verification. |
| **3.3 Zero-Knowledge Client-Side Cryptographic Engine** | `FR-3.1` – `FR-3.7` | Client-side RFC 9580 v6 Curve25519 (`Ed25519` signing + `X25519` encryption) keypair generation (<50ms bare keygen benchmark target) via `OpenPGP.js v6` and WebCrypto API; private keys encrypted locally via Argon2id S2K (~200–400ms intentional unlock delay) in browser `IndexedDB` (zero `localStorage`); multi-recipient PKESK encryption across all active `PROGRAM_DEFENDER` subkeys, the offline `recovery_public_key`, and the reporter's key; encrypted report title (`title_ciphertext`) paired with a coarse 8-value `operational_label` enum for zero-plaintext queue sorting; `recipient_set_version` optimistic concurrency guard (`409 Conflict` on stale keyring); direct-to-Cloudflare R2 presigned encrypted attachment uploads (`<= 25 MB`); and strict post-logout memory zeroization (`Uint8Array.fill(0)`). |
| **3.4 Deterministic CVSS v3.1 Severity Calculator** | `FR-4.1` – `FR-4.4` | Pure TypeScript engine implementing all 8 FIRST.org CVSS v3.1 Base metrics (`AV`, `AC`, `PR`, `UI`, `S`, `C`, `I`, `A`), canonical vector parser/serializer (`CVSS:3.1/AV:_/AC:_/PR:_/UI:_/S:_/C:_/I:_/A:_`), official `RoundUp` ceiling function to 1 decimal place, exact exploitability coefficient `8.22`, and immutable assessment audit logging (`CVSS_ASSESSMENT`) verified at 100% mathematical parity across **45 FIRST.org and NIST NVD test vectors** (`CVSS_TEST_FIXTURES.md`). |
| **3.5 Vulnerability Triage, Dual-Lane Threading & SLA Engine** | `FR-5.1` – `FR-5.4` | In-browser payload decryption and `rehype-sanitize` AST neutralization prior to DOM rendering; Dual-Lane Encrypted Threading separating `RESEARCHER_PUBLIC` conversation from `INTERNAL_REVIEWER` notes (`author_user_id` or `author_guest_id` XOR constraint); metadata-only email notifications (Resend/Postmark) that never transmit vulnerability titles or exploit details; and an hourly SLA countdown engine (`Critical: 24h triage / 7d fix`, `High: 72h / 30d`, `Medium: 7d / 90d`, `Low: 14d / 180d`) with metadata-only Slack webhook alerts. |
| **3.6 Remediation Evidence & Commit Verification** | `FR-6.1` – `FR-6.3` | Mandatory dual-path remediation evidence before transitioning `ACCEPTED -> READY_FOR_RETEST`: (a) `CODE_COMMIT` verified via GitHub REST API v3 (`/repos/{owner}/{repo}/commits/{sha}` and `/compare/{base}...{head}` asserting `status` is `ahead` or `identical`), or (b) `CONFIG_INFRASTRUCTURE` binding a 64-character SHA-256 configuration artifact hash and target deployment environment (`PRODUCTION`, `STAGING`, `CLOUD_IAM`, `WAF_EDGE`). |
| **3.7 Lifecycle State Machine & Attested Retest Workflow** | `FR-7.1` – `FR-7.7` | Strict 13-state deterministic FSM (`QUOTA_HELD`, `NEW`, `TRIAGING`, `NEED_MORE_INFO`, `ACCEPTED`, `READY_FOR_RETEST`, `RESOLVED_VERIFIED`, `RESOLVED_UNVERIFIED`, `CLOSED_UNVERIFIED_TIMEOUT`, `CLOSED_INCOMPLETE`, `DUPLICATE`, `REJECTED_INVALID`, `REJECTED_SPAM`, `WITHDRAWN`); 3 distinct retest outcomes (`RETEST_CONFIRMED_FIXED -> RESOLVED_VERIFIED`, `RETEST_FAILED -> ACCEPTED`, `RETEST_BYPASSED -> RESOLVED_UNVERIFIED`, plus 14-day timeout `-> CLOSED_UNVERIFIED_TIMEOUT`); controlled regression reopening (`RESOLVED_* / CLOSED_INCOMPLETE -> ACCEPTED`); and Redacted Closure Evidence Export (PDF & JSON). |
| **3.8 Security, Tenant Isolation, Quotas & Commercial Billing** | `FR-8.1` – `FR-8.7` | PostgreSQL 16 Row-Level Security (`SET LOCAL app.current_tenant_id`); shared rate limiter (`5 submissions/hr/IP`) and Cloudflare Turnstile CAPTCHA; bounded tenant storage quotas (`50 MB` DB, `500 MB` Community R2 / `2 GB` Academic Demo R2 / `10 GB` Team R2; 90% warning, 100% HTTP `413` rejection); append-only hash-chained `AUDIT_EVENT` ledger (`INSERT` and `SELECT` only, SHA-256 `prev_hash`); and Lemon Squeezy Merchant of Record subscription billing (`Community $0/mo` vs. `Team $49/mo`). |

---

## Part 2: Formal Use Case Specifications (`UC-01` to `UC-08`) & System Use Case Diagram

### 2.1 System Use Case Diagram (`UC-01` through `UC-08`)

![Figure 4.2: System Use Case Diagram](../requirements/diagrams/fig4_2_usecase.png)

### 2.2 Formal Textual Use Case Specifications

#### Use Case `UC-01`: Submit Encrypted Vulnerability Report & Generate Recovery Package
* **Primary Actor**: Ethical Security Researcher (`Hunter` or `Guest Hunter`).
* **Preconditions**: Researcher is on the organization's public program page (or possesses a valid private program invitation token `token_hash`).
* **Main Success Scenario**:
  1. Researcher selects an in-scope target asset, selects a coarse `operational_label` enum (`AUTH_SESSION`, `ACCESS_CONTROL_IDOR`, `INJECTION_XSS_CSRF`, `API_BUSINESS_LOGIC`, `CRYPTO_CONFIG`, `DATA_EXPOSURE`, `DEPENDENCY_SUPPLY_CHAIN`, or `OTHER`), and inputs the vulnerability title, reproduction steps, and optional PoC attachment.
  2. Browser generates an ephemeral RFC 9580 v6 Curve25519 keypair in memory (<50ms benchmark target) and fetches the program's active `PROGRAM_DEFENDER` encryption subkeys (`recipient_set_version`) plus `recovery_public_key`.
  3. Browser generates an ephemeral AES-256 session key, encrypts both the title (`title_ciphertext`) and body payload into an OpenPGP message, and wraps the session key in PKESK packets for all active `PROGRAM_DEFENDER` subkeys, the offline `recovery_public_key`, and the reporter's key.
  4. If an attachment (`<= 25 MB`) is present, browser requests a presigned URL from `/api/uploads/presign` and streams the encrypted binary directly to Cloudflare R2.
  5. Browser submits the neutral `operational_label`, `recipient_set_version`, `title_ciphertext`, and `encrypted_payload` to the API gateway.
  6. Server validates Cloudflare Turnstile CAPTCHA, rate limits, tenant quotas, and `recipient_set_version`, persists the ciphertext in PostgreSQL, issues a durable `guest_actor_id` and `guest_token_hash`, displays the Secret Tracking URL (`/report/track/BBT-RPT-XXXX#token=<secret>`) scrubbed via `window.history.replaceState`, and triggers download of the `.bbt-recovery.json` Guest Recovery Package. Report enters state `NEW`.
* **Extensions**:
  * *4a. Organization public key missing or invalid*: Browser blocks submission and alerts user.
  * *5a. Stale `recipient_set_version`*: Server returns `409 Conflict`; browser refreshes recipient keyring and re-encrypts automatically.
  * *6a. Rate limit or Community active-report quota exceeded*: Server returns `429 Too Many Requests` (or holds report `#6+` in `QUOTA_HELD`).

#### Use Case `UC-02`: Decrypt & Triage Vulnerability Report
* **Primary Actor**: Organization Triage Lead (`Defender`).
* **Preconditions**: Authenticated with `ORG_DEFENDER` role and active `PROGRAM_DEFENDER` membership; report is in state `NEW` or `TRIAGING`.
* **Main Success Scenario**:
  1. Defender opens report view; browser fetches encrypted payload and retrieves local private key from `IndexedDB`.
  2. Defender enters local passphrase to unlock the Argon2id S2K-protected private key (~200–400ms intentional delay).
  3. Browser decrypts `title_ciphertext` and body ciphertext in memory, passes Markdown through `rehype-sanitize` AST parser, and renders sanitized HTML.
  4. Defender posts encrypted messages in either the Researcher–Organization lane (`RESEARCHER_PUBLIC`) or Reviewer Internal Notes lane (`INTERNAL_REVIEWER`), evaluates the 8 CVSS v3.1 Base metrics, and updates state to `ACCEPTED`.
  5. Server records the CVSS v3.1 vector, score, and SHA-256 hash-chained `AUDIT_EVENT`.
* **Extensions**:
  * *2a. Incorrect passphrase*: Browser displays decryption error; private key remains locked.
  * *4a. Missing reproduction details*: Defender transitions state to `NEED_MORE_INFO` (auto-transitions to `CLOSED_INCOMPLETE` after `>= 14 days` of researcher inactivity).
  * *4b. Duplicate submission*: Defender links canonical `duplicate_of_id` and transitions state to `DUPLICATE`.
  * *4c. Out of scope or invalid*: Defender cites policy rule and transitions state to `REJECTED_INVALID`.
  * *4d. Automated scanner noise*: Defender transitions state directly from `NEW` to `REJECTED_SPAM`.

#### Use Case `UC-03`: Propose Remediation Evidence
* **Primary Actor**: Organization Triage Lead (`Defender`).
* **Preconditions**: Report is in state `ACCEPTED`.
* **Main Success Scenario**:
  1. Defender selects "Propose Remediation" and selects evidence type `CODE_COMMIT` or `CONFIG_INFRASTRUCTURE`.
  2. *Path A (`CODE_COMMIT`)*: Defender inputs repository URL, target remediation branch, and 40-character Git Commit SHA. Server queries GitHub REST API v3 (`/repos/{owner}/{repo}/commits/{sha}` and `/compare/{base}...{head}`) and verifies `status` is `ahead` or `identical`.
  3. *Path B (`CONFIG_INFRASTRUCTURE`)*: Defender inputs configuration diff or rule summary, selects target environment (`PRODUCTION`, `STAGING`, `CLOUD_IAM`, `WAF_EDGE`), and computes a 64-character SHA-256 configuration artifact hash.
  4. Server persists `REMEDIATION_EVIDENCE`, transitions report state to `READY_FOR_RETEST`, records a hash-chained `AUDIT_EVENT`, and dispatches a metadata-only retest invitation email to the researcher.
* **Extensions**:
  * *2a. Commit SHA not found or not ancestor of target branch*: Server returns HTTP `422 Unprocessable Entity`; state remains `ACCEPTED`.

#### Use Case `UC-04`: Execute Attested Retest & Export Closure Evidence
* **Primary Actor**: Ethical Security Researcher (`Hunter`) and Organization Triage Lead (`Defender`).
* **Preconditions**: Report is in state `READY_FOR_RETEST` with a linked `REMEDIATION_EVIDENCE` record.
* **Main Success Scenario**:
  1. Researcher inspects the linked remediation commit/configuration hash and re-tests the target asset.
  2. Researcher submits a signed retest attestation (`RETEST_CONFIRMED_FIXED`) with encrypted verification notes.
  3. Server transitions report state to `RESOLVED_VERIFIED` and appends an immutable `AUDIT_EVENT`.
  4. Defender generates a **Redacted Closure Evidence Export** (PDF & JSON) containing the lifecycle timeline, CVSS 3.1 vector, commit SHA/config hash, deployment environment, and cryptographic hash-chain proof—excluding all raw exploit payloads.
* **Extensions**:
  * *2a. Patch incomplete (`RETEST_FAILED`)*: Researcher submits reproduction proof; report automatically loops back to `ACCEPTED`.
  * *2b. Researcher unresponsive (`>= 14 days`)*: System cron transitions report to `CLOSED_UNVERIFIED_TIMEOUT`.
  * *2c. Emergency administrative bypass (`RETEST_BYPASSED`)*: Defender closes report with mandatory justification; state transitions to `RESOLVED_UNVERIFIED`.

#### Use Case `UC-05`: Restore Guest Session via Recovery Package
* **Primary Actor**: Account-Less Ethical Security Researcher (`Guest Hunter`).
* **Preconditions**: Guest possesses a downloaded `.bbt-recovery.json` Recovery Package on a new browser or device.
* **Main Success Scenario**:
  1. Guest navigates to `/report/restore` and selects the `.bbt-recovery.json` file.
  2. Browser validates JSON schema (`version: 1`) and verifies SHA-256 `checksum` integrity in memory.
  3. Browser imports `encrypted_private_key` into local `IndexedDB` and authenticates the session using `access_token` (`guest_token_hash`) while preserving durable `guest_actor_id` attribution.
  4. Browser redirects to `/report/track/BBT-RPT-XXXX` and decrypts historical and new messages seamlessly.

#### Use Case `UC-06`: Onboard Organization Tenant, Verify DNS & Configure Cryptographic Keys
* **Primary Actor**: Organization Owner (`Tenant Owner`).
* **Preconditions**: Authenticated user creating or configuring an organization workspace.
* **Main Success Scenario**:
  1. Owner completes the Guided Onboarding Wizard and adds the `_bugbountytrack-challenge.<domain>` DNS TXT record verified by the server.
  2. Browser generates RFC 9580 v6 Curve25519 defender keys and the offline **Organization Master Recovery Key** (`recovery_public_key`).
  3. Owner downloads the Argon2id-protected private recovery key and passes the mandatory in-browser test decryption challenge (`Uint8Array` zeroized immediately after verification).
  4. Owner assigns authorized defenders to `PROGRAM_DEFENDER` (incrementing `recipient_set_version`) and cleartext-signs the generated RFC 9116 `security.txt` policy in-browser for publication at `/.well-known/security.txt`.

#### Use Case `UC-07`: Enforce SLA Escalation Timers & Verify Hash-Chained Audit Ledger
* **Primary Actor**: Organization Reviewer (`Defender`), Management (`ReadOnly`), or System Cron.
* **Preconditions**: Active vulnerability reports exist within the tenant workspace.
* **Main Success Scenario**:
  1. Hourly SLA countdown engine evaluates `sla_triage_due` and `sla_remediation_due` deadlines across active reports.
  2. Approaching or breached SLA targets trigger metadata-only email and Slack webhook alerts without exposing exploit details.
  3. Reviewers and read-only auditors inspect the append-only `AUDIT_EVENT` ledger (`INSERT` and `SELECT` only) and verify cryptographic `prev_hash` SHA-256 chain continuity.

#### Use Case `UC-08`: Manage SaaS Subscription Billing & Storage Quotas
* **Primary Actor**: Organization Owner (`Tenant Owner`) and Platform SuperAdmin.
* **Preconditions**: Organization workspace is provisioned on Community (Free) or Team ($49/month) plan.
* **Main Success Scenario**:
  1. Owner upgrades or manages subscription via Lemon Squeezy Merchant of Record checkout and webhook synchronization.
  2. Quota guard monitors PostgreSQL database volume (`50 MB` demo) and Cloudflare R2 encrypted object storage (`500 MB` Community, `2 GB` demo, `10 GB` Team), issuing warnings at `90%` and rejecting new uploads with HTTP `413` at `100%`.

---

## Part 3: Quantifiable Non-Functional Requirements (`NFR-01` to `NFR-09` — Latency, Security & Uptime)

| NFR ID | Category | Quantifiable Target / Metric | Verification Method & Tooling |
| :---: | :--- | :--- | :--- |
| **`NFR-01`** | **Latency (API & UI)** | `p95 <= 300ms` (warm) / `p95 <= 1,200ms` (cold start) for metadata & state transition APIs; `FCP <= 1.5s` | k6 load script (`50 VUs` over `60s`) & Lighthouse CI audit |
| **`NFR-02`** | **Latency (Client Crypto)** | `< 50ms` bare Curve25519 keygen benchmark target; `~200–400ms` Argon2id S2K unlock; `<= 800ms` encrypt/decrypt (`1 MB` payload) | Playwright browser `performance.now()` benchmark suite (100 iterations) |
| **`NFR-03`** | **Throughput & Concurrency** | `>= 50 concurrent VUs` sustained for `60s` with `0%` HTTP `5xx` errors and `0` cross-tenant leaks | k6 concurrency stress test against staging environment |
| **`NFR-04`** | **Accessibility & Usability** | `100%` WCAG 2.2 Level AA compliance (`>= 4.5:1` contrast, `>= 24x24 CSS px` targets); `SUS >= 75.0` | `@axe-core/playwright` E2E scan & controlled peer usability study |
| **`NFR-05`** | **Security (Zero-Knowledge)** | `0 bytes` of plaintext vulnerability title, description, or PoC in PostgreSQL, R2, or logs; `TLS 1.3`; `Argon2id S2K` | SQL/R2 ciphertext inspection, HTTP header audit, and URI fragment check |
| **`NFR-06`** | **Security (XSS & CSP)** | `100%` neutralization of OWASP XSS vectors via `rehype-sanitize` AST; `0` raw `innerHTML` sinks | Vitest XSS payload corpus & Playwright CSP violation listener |
| **`NFR-07`** | **Security (Tenant Isolation)** | `0` unauthorized cross-tenant rows returned under PostgreSQL 16 RLS (`app.current_tenant_id`) | Automated cross-tenant IDOR integration test suite (Tenant A vs. Tenant B) |
| **`NFR-08`** | **Determinism & Auditability** | `100%` exact score parity (`45/45` FIRST.org & NIST NVD vectors); `100%` SHA-256 `prev_hash` audit continuity | Vitest CVSS 3.1 fixture suite & PostgreSQL `UPDATE`/`DELETE` rejection test |
| **`NFR-09`** | **System Uptime & Availability** | `>= 99.5%` monthly uptime (`<= 3.65h/mo` max unplanned downtime); `/api/health` `p95 <= 200ms`; `RPO <= 24h`, `RTO <= 4h` | BetterStack / UptimeRobot 60-second probes & sandbox backup restore drill |

---

## Document Endorsement & Milestone Sign-Off

This Week 2 Software Requirements Specification (`SRS v2.1.0`) is formally submitted and endorsed as the baseline specification for **BugBountyTrack** (`PTUT - PRJ - 089`) under the Department of Software Engineering Technology, Punjab Tianjin University of Technology (PTUT), Lahore.

| Role | Name & Designation | Identifier / Credentials | Signature & Date |
| :--- | :--- | :--- | :--- |
| **Student Author** | **Taha Asadullah**<br>B.Sc. Software Engineering Technology | Roll No: `24-ST-013`<br>Section: `SET-B` (`2024–2028`) | *Signed: Taha Asadullah*<br>Date: October 11, 2026 |
| **Project Supervisor** | **Sir Umar Hayat**<br>Assistant Professor, Dept. of SET | Faculty Supervisor<br>PTUT Lahore | ______________________<br>Date: _______________ |
