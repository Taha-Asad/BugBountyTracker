# Week 2 Task & Deliverable: Software Requirements Specification (SRS)

| Attribute | Details |
| :--- | :--- |
| **Project ID** | `PTUT - PRJ - 089` |
| **Project Title** | **BugBountyTrack — Private Bug Bounty & Vulnerability Disclosure Platform** |
| **Student Author** | Taha Asadullah (Roll No: `24-ST-013`, Section: `SET-B`) |
| **Academic Supervisor** | Sir Umar Hayat (Assistant Professor, PTUT Lahore) |
| **Milestone** | **Week 2** — Software Requirements Specification (**Gate 1: DoR Part II**) |
| **Standard Compliance** | IEEE Std 830-1998 / ISO/IEC/IEEE 29148:2018 (`Revision 2.2`) |
| **WBS Task IDs** | `WP-1.1` (8h), `WP-1.2` (12h), `WP-1.3` (10h), `WP-1.4` (10h) — **Sprint 1 Baseline** |

---

## Supporting Deliverable Document (Google Drive Link)

| Deliverable Document | Scope Covered | Google Drive Link |
| :--- | :--- | :--- |
| **Formal IEEE 830 Software Requirements Specification (`SRS.docx`)** | Complete IEEE 830 SRS (`Revision 2.2`), Field-Level Classification Matrix (`Class A/B/C`), Functional Requirements (`FR-1` to `FR-8`), Formal Use Case Specifications (`UC-01` to `UC-07`), 4 UML Behavioral Diagrams (`Figure 4.1` to `Figure 4.4`), Quantifiable NFRs (`NFR-01` to `NFR-09`), and 100% Bidirectional Traceability Matrix | [View IEEE 830 Software Requirements Specification (Google Drive)](PASTE_GOOGLE_DRIVE_LINK_FOR_SRS_DOCX_HERE) |

---

## Part 1: Formal IEEE 830 Software Requirements Specification (SRS) Overview & Functional Requirements

The formal **IEEE Std 830-1998 / ISO/IEC/IEEE 29148:2018 Software Requirements Specification (`SRS`, Revision 2.2)** establishes a complete, unambiguous, verifiable, and traceable engineering baseline for **BugBountyTrack**. It introduces a strict **3-tier Field-Level Cryptographic & Visibility Classification Matrix** (`Class A: Plaintext Operational Metadata`, `Class B: Encrypted Shared Content [RESEARCHER_ORG]`, `Class C: Encrypted Internal Content [REVIEWER_INTERNAL]`) and maps every functional requirement (`FR-1.1` through `FR-8.5`) directly to our Week 1 Problem Statement, our 2 Target User Personas (**Alex Rivera — "The Hunter"** and **Sarah Chen — "The Defender"** leading a 7-developer engineering team), and our **5 Core MVP Features**:

| SRS Module & Week 1 Core MVP Alignment | Requirement Range | Core Functional Specification Summary (`Revision 2.2`) |
| :--- | :---: | :--- |
| **3.1 Multi-Tenant Workspace, Identity, Role Model & Guest Recovery (MVP Feature 2)** | `FR-1.1` – `FR-1.6` | Isolated `organization_id` workspaces with composite `(organization_id, id)` foreign keys; multi-organization `USER_MEMBERSHIP` (`ORG_OWNER`, `ORG_DEFENDER`, `ORG_READONLY`) decoupled from external `HUNTER` research; report-scoped `REPORT_RECIPIENT` decryption snapshot (`ORG_OWNER` requires `REPORT_RECIPIENT` membership or audited Master Recovery Key ceremony to decrypt payloads); Argon2id authentication, password-reset session revocation, and TOTP MFA; Account-Less Guest Submission with **Argon2id + AES-256-GCM authenticated `.bbt-recovery.json` package encrypting both `access_token` and `ephemeral_private_key`** (`FR-1.6c`), local-only `FileReader` restore (`FR-1.6d`), token rotation (`FR-1.6e`), and **Ed25519 detached signature proof-of-possession (`X-Guest-Signature`)** on guest state mutations (`FR-1.6f`). |
| **3.2 RFC 9116 `security.txt` Generator & Hosted Safe Harbor Engine (MVP Feature 1)** | `FR-2.1` – `FR-2.5` | Automated generation of RFC 9116 compliant `/.well-known/security.txt` manifests (`Contact`, `Encryption`, `Policy`, `Acknowledgments`, `Preferred-Languages`, `Canonical`, and `Expires <= 365 days`); **in-browser** OpenPGP cleartext signing (`-----BEGIN PGP SIGNED MESSAGE-----`) using the organization's private Ed25519 key; structured `IN_SCOPE` vs. `OUT_OF_SCOPE` asset tables; hosted Safe Harbor legal terms (explicitly distinguished from RFC 9116 directive syntax and referenced via the `Policy:` URL); and automated DNS TXT (`_bbt-challenge.<domain>`) verification. |
| **3.3 Client-Side OpenPGP v6 Pipeline & Key Lifecycle Management (MVP Feature 2)** | `FR-3.1` – `FR-3.8` | Pinned `OpenPGP.js v6` (`openpgp.config.v6Keys = true`) generating RFC 9580 v6 Curve25519 (`Ed25519` + `X25519`) keys (`< 50 ms` target) with 64-char SHA-256 fingerprints; private keys encrypted in `IndexedDB` via Argon2id S2K (`passes = 3, parallelism = 4, memoryExponent = 16 [64 MiB]`, `~200–400 ms`); multi-recipient PKESK encryption for `REPORT_RECIPIENT` + `recovery_public_key` + submitter key; Class B `title_ciphertext` + Class A `operational_label` enum; pre-upload Turnstile CAPTCHA & 30-minute `PENDING_UPLOAD` quota reservation on `/api/uploads/presign` (`<= 25 MB` ciphertext) with separate symmetric file key `K_file` and forced `Content-Disposition: attachment` + `nosniff`; Personal Key Backup (`.bbt-user-keys.json`, `FR-3.7`); and defender offboarding, key revocation, and `HISTORICAL_ACCESS_GRANTED` session-key re-wrapping (`FR-3.8`). |
| **3.4 Deterministic CVSS 3.1 Base Scoring Engine (MVP Feature 3)** | `FR-4.1` – `FR-4.4` | Pure TypeScript engine implementing all 8 FIRST.org CVSS v3.1 Base metrics (`AV`, `AC`, `PR`, `UI`, `S`, `C`, `I`, `A`), canonical vector parser/serializer, official exploitability coefficient **`8.22`**, and FIRST.org Appendix A integer-scaled `RoundUp` ceiling function (`Math.ceil(Math.round(val * 100000) / 10000) / 10`), verified across **45 FIRST.org and NIST NVD reference fixtures** (`CVSS_TEST_FIXTURES.md`) and all **2,592 valid Base metric combinations**, with defender scoring rationale encrypted as Class C `cvss_justification_ciphertext` (`FR-4.4`). |
| **3.5 Confidential Triage, Dual-Lane Threading & SLA Timers (MVP Feature 2)** | `FR-5.1` – `FR-5.5` | In-browser payload decryption and `rehype-sanitize` AST cleansing (`FR-5.1`); Dual-Lane report-scoped encrypted threading separating Class B `RESEARCHER_ORG` conversation from Class C `REVIEWER_INTERNAL` notes encrypted strictly for `REPORT_RECIPIENT` (`FR-5.2`); strict Class A metadata-only email/webhook notifications (`FR-5.3`); hourly SLA countdown & inactivity timeout scheduler (`FR-5.4`); and privacy-preserving duplicate linking (`FR-5.5`). |
| **3.6 Git-Linked & Config-Hash Remediation Verification (MVP Feature 4)** | `FR-6.1` – `FR-6.4` | **Three-step fix-to-retest workflow (`FR-6.1`)**: Step 1 records numbered `REMEDIATION_RECORD` (`remediation_attempt_no = N`, `ACCEPTED -> FIX_PROPOSED`); Step 2 records `deployment_env`, `deployed_version`, and `deployed_at`; Step 3 transitions `FIX_PROPOSED -> RETEST_PENDING` bound to `remediation_record_id`. Verifies `CODE_COMMIT` via GitHub REST API v3 (`/commits/{sha}` existence + `commit.verification.verified` boolean, and `/compare/{commit_sha}...{target_branch}` `BASE...HEAD` ancestry requiring `status IN ('ahead', 'identical')`, `FR-6.2`), or `CONFIG_INFRASTRUCTURE` 64-hex SHA-256 `config_hash` (`FR-6.3`), with AES-256-GCM encrypted GitHub PAT lifecycle (`FR-6.4`). |
| **3.7 15-State Lifecycle FSM, Attested Retest & Closure Exports (MVP Feature 5)** | `FR-7.1` – `FR-7.7` | **Deterministic 15-state FSM (`FR-7.1`)** with atomic `state_version` optimistic concurrency (`409 Conflict` on simultaneous mutations): 6 active states (`NEW`, `TRIAGING`, `NEED_MORE_INFO`, `ACCEPTED`, `FIX_PROPOSED`, `RETEST_PENDING`), 3 remediation closures bound to `remediation_record_id` (`VERIFIED_RESEARCHER`, `VERIFIED_INTERNAL`, `CLOSED_UNVERIFIED_TIMEOUT`, plus `RETEST_FAILED` loopback to `ACCEPTED` requiring `remediation_attempt_no = N + 1`), and 6 non-remediation terminal states (`CLOSED_INCOMPLETE`, `RISK_ACCEPTED` from `TRIAGING`/`ACCEPTED` by `ORG_OWNER` only, `REJECTED_INVALID`, `DUPLICATE`, `REJECTED_SPAM` recoverable by `ORG_OWNER` only, and terminal `WITHDRAWN` from `NEW`/`TRIAGING`), plus Class A Redacted Closure Evidence Exports (PDF & JSON). |
| **3.8 Application Hardening, Forced RLS & Hash-Chained Audit Ledger (MVP Feature 5)** | `FR-8.1` – `FR-8.5` | `rehype-sanitize` neutralization of the 100-vector OWASP XSS corpus (`FR-8.1`); `bbt_app_runtime` role (`NOSUPERUSER NOBYPASSRLS`) with `FORCE ROW LEVEL SECURITY` and `SECURITY DEFINER` guest/cron functions (`FR-8.2`); pre-upload CAPTCHA & rate limits (`FR-8.3`); `50 MB` logical DB / `2 GB` R2 quotas (`<= 10` evaluation tenants) with `HeadObjectCommand` verification and 30m orphan cleanup (`FR-8.4`); and per-tenant gapless `seq_no` hash-chained `audit_events` (`SELECT ... FOR UPDATE`) using **RFC 8785 JCS canonical hashing binding `evidence_payload_sha256` and `justification_ciphertext_sha256`** plus Ed25519-signed external Audit Checkpoint Receipts (`FR-8.5`). |

---

## Part 2: Formal Use Case Specifications (`UC-01` to `UC-07`) & UML Behavioral Diagrams

### 2.1 System Use Case Diagram (`Figure 4.1`)

![Figure 4.1: System Use Case Diagram](../requirements/diagrams/fig4_2_usecase.png)

### 2.2 Formal Textual Use Case Specifications (`UC-01` to `UC-07`)

#### Use Case `UC-01`: Submit Encrypted Vulnerability Report & Generate Authenticated Recovery Package
* **Primary Actor**: Ethical Security Researcher (`Hunter` or `Guest Hunter`).
* **Preconditions**: Researcher is viewing an organization's active public program page (or holds a valid private program invitation token `token_hash`).
* **Main Success Scenario**:
  1. Researcher selects an in-scope target asset (`asset_scope`), selects a coarse Class A `operational_label` enum, enters the specific vulnerability title, reproduction steps, and optional PoC attachment (`<= 25 MB` encrypted size), and sets (or copies) a Guest Recovery Passphrase.
  2. Browser configures `OpenPGP.js v6` (`v6Keys = true`), generates an ephemeral RFC 9580 v6 Curve25519 keypair in memory (`< 50 ms` target), and fetches the program's active `PROGRAM_DEFENDER` subkeys (`recipient_set_version`) plus `recovery_public_key`.
  3. If an attachment is present: Browser completes Cloudflare Turnstile CAPTCHA and calls `POST /api/uploads/presign` with the encrypted file size. Server verifies CAPTCHA, rate limits, and tenant quota, reserves a 30-minute `PENDING_UPLOAD` slot, and returns a presigned R2 `PUT` URL. Browser encrypts the file with symmetric key `K_file` and uploads the ciphertext directly to Cloudflare R2.
  4. Browser encrypts all Class B fields (`title_ciphertext`, description, reproduction steps, impact, and `K_file` if attachment present) into a multi-recipient OpenPGP packet for the active `PROGRAM_DEFENDER` subkeys, `recovery_public_key`, and the reporter's key.
  5. Browser dispatches `POST /api/v1/reports` with `operational_label`, `recipient_set_version`, `title_ciphertext`, `encrypted_payload`, `guest_public_key`, and the R2 upload reference.
  6. Inside a single PostgreSQL transaction, the server validates Turnstile CAPTCHA, rate limits, `recipient_set_version`, and R2 object size (`HeadObjectCommand`), snapshots active `PROGRAM_DEFENDER` members into `REPORT_RECIPIENT`, inserts the `REPORT` in state `NEW` (`state_version = 1`), and appends `seq_no` to `audit_events`.
  7. For guest submitters, the server returns `report_id`, durable `guest_actor_id`, and `access_token`. Browser encrypts **both `access_token` and `ephemeral_private_key`** using Argon2id + AES-256-GCM into a downloadable `.bbt-recovery.json` package (`FR-1.6c`), stores the key in `IndexedDB`, displays the Secret Tracking URL (`/report/track/BBT-RPT-XXXX#token=<secret>`), and immediately scrubs the URI fragment via `window.history.replaceState`.
* **Extensions**:
  * *2a. Organization public key missing or invalid*: Browser blocks submission and alerts user.
  * *3a / 6a. Rate limit (`> 5/hr/IP`) or storage quota (`> 100%`) exceeded*: Server rejects at presign or submission with HTTP `429 Too Many Requests` or `413 Payload Too Large`.
  * *5a. Stale `recipient_set_version`*: Server returns HTTP `409 Conflict` with updated keyring; browser re-encrypts the text payload and `K_file` (without re-uploading the R2 attachment blob) and retries automatically.

#### Use Case `UC-02`: Decrypt, Claim for Triage & Score Vulnerability Report
* **Primary Actor**: Organization Triage Lead (`ORG_DEFENDER` in `REPORT_RECIPIENT`).
* **Preconditions**: Authenticated with `ORG_DEFENDER` role and listed in `REPORT_RECIPIENT` for the report; report is in state `NEW` or `TRIAGING`.
* **Main Success Scenario**:
  1. Defender opens `/dashboard/reports/[id]`. Browser fetches the ciphertext record (`state_version`) and retrieves the defender's encrypted private key from `IndexedDB`.
  2. Defender enters their local encryption passphrase to unlock the Argon2id S2K-protected private key (`~200–400 ms` intentional delay).
  3. Browser decrypts `title_ciphertext` and `encrypted_payload` in memory, sanitizes the Markdown AST via `rehype-sanitize`, and renders sanitized HTML.
  4. **Step 4a (Claim Intake: `NEW -> TRIAGING`)**: If the report is in `NEW`, the defender clicks "Begin Triage," atomically transitioning `NEW -> TRIAGING` (`state_version + 1`) and recording the assigned triager in `audit_events`.
  5. **Step 4b (Evaluate & Accept: `TRIAGING -> ACCEPTED`)**: Defender posts encrypted comments in either `RESEARCHER_ORG` (Class B) or `REVIEWER_INTERNAL` (Class C), selects the 8 CVSS v3.1 Base metrics, writes the encrypted scoring rationale (`cvss_justification_ciphertext`, Class C), and transitions the report from `TRIAGING` to `ACCEPTED` (`state_version + 1`).
  6. Server persists `cvss_vector`, `cvss_score`, and `cvss_justification_ciphertext` and appends a hash-chained `AUDIT_EVENT`.
* **Extensions**:
  * *2a. Passphrase incorrect*: Browser displays decryption error; private key remains locked.
  * *5a. Insufficient reproduction details*: Defender transitions `TRIAGING -> NEED_MORE_INFO` and posts a Class B clarification question (auto-transitions to `CLOSED_INCOMPLETE` after `>= 14 days` of researcher inactivity).
  * *5b. Duplicate submission*: Defender links canonical parent `duplicate_of_report_id` and transitions `TRIAGING -> DUPLICATE`.
  * *5c. Out of scope or invalid*: Defender selects Class A `rejection_code`, writes Class B `rejection_reason_ciphertext`, and transitions `TRIAGING -> REJECTED_INVALID`.
  * *5d. Automated scanner spam*: Defender transitions `NEW` or `TRIAGING -> REJECTED_SPAM` (reopenable only by `ORG_OWNER` if misclassified).
  * *5e. Operational risk acceptance*: `ORG_OWNER` transitions `TRIAGING` or `ACCEPTED -> RISK_ACCEPTED` with Class C `risk_rationale_ciphertext` and `risk_review_date`.

#### Use Case `UC-03`: Propose Remediation Evidence, Confirm Deployment & Request Retest
* **Primary Actor**: Organization Triage Lead (`ORG_DEFENDER` in `REPORT_RECIPIENT`).
* **Preconditions**: Report is in state `ACCEPTED`.
* **Main Success Scenario**:
  1. **Step 1 — Record Proposed Fix (`ACCEPTED -> FIX_PROPOSED`)**: Defender opens the Remediation Modal (`SCR-04`), selects `CODE_COMMIT` or `CONFIG_INFRASTRUCTURE`, and writes encrypted remediation notes (`remediation_notes_ciphertext`, Class B).
     - *Path A (`CODE_COMMIT`)*: Defender inputs repository, `target_branch`, and 40-char `commit_sha`. Server queries GitHub REST API v3 (`/commits/{sha}` and `/compare/{commit_sha}...{target_branch}`), verifies `status` is `ahead` or `identical`, and records `verified_branch_head_sha` and `github_signature_verified`.
     - *Path B (`CONFIG_INFRASTRUCTURE`)*: Browser computes a 64-char SHA-256 `config_hash` via WebCrypto over the configuration artifact.
     Server creates `REMEDIATION_RECORD` (`remediation_attempt_no = N`, `remediation_record_id`) and atomically transitions report state `ACCEPTED -> FIX_PROPOSED` (`state_version + 1`).
  2. **Step 2 — Confirm Target Environment Deployment**: Once the patch is deployed, the defender records the target `deployment_env` (`Staging`, `Pre-Production`, or `Production`), `deployed_version`, and `deployed_at` timestamp on `remediation_record_id`.
  3. **Step 3 — Request Retest (`FIX_PROPOSED -> RETEST_PENDING`)**: Defender triggers "Request Retest." Server verifies `deployed_at != NULL` on the active `remediation_record_id`, atomically transitions `FIX_PROPOSED -> RETEST_PENDING` (`state_version + 1`), records an `AUDIT_EVENT`, and sends a Class A metadata-only retest invitation referencing `remediation_attempt_no`.
* **Extensions**:
  * *1a. Commit SHA not found or not an ancestor of `target_branch` (`status` is `behind` or `diverged`)*: Server returns HTTP `422 Unprocessable Entity`; report remains in `ACCEPTED`.
  * *3a. Attempt to transition to `RETEST_PENDING` before recording deployment*: Server rejects with HTTP `400 Bad Request`.

#### Use Case `UC-04`: Execute Attested Retest Bound to Remediation Attempt & Export Closure Evidence
* **Primary Actor**: Ethical Security Researcher (`Hunter` / `Guest Hunter`) and Organization Triage Lead (`Defender`).
* **Preconditions**: Report is in state `RETEST_PENDING` with an active `remediation_record_id` (`remediation_attempt_no = N`).
* **Main Success Scenario**:
  1. Researcher inspects the linked `commit_sha` / `config_hash` and `deployment_env` for `remediation_attempt_no = N` and re-tests the target asset.
  2. Researcher writes encrypted verification notes (`verification_notes_ciphertext`, Class B) and submits a `VERIFIED_RESEARCHER` attestation bound to `remediation_record_id` (signed in-browser with the guest's Ed25519 report key if a guest submitter).
  3. Inside an atomic transaction checking `state == RETEST_PENDING` and `state_version`, the server persists `RETEST_EVIDENCE` (linked to `remediation_record_id`), transitions the report to `VERIFIED_RESEARCHER` (`state_version + 1`), and appends a hash-chained `AUDIT_EVENT` with a signed checkpoint receipt.
  4. Defender opens `SCR-08` and generates a **Redacted Closure Evidence Export** (PDF or JSON) containing strictly Class A metadata and the signed audit checkpoint chain.
* **Extensions**:
  * *2a. Vulnerability still exploitable (`RETEST_FAILED`)*: Researcher submits reproduction proof bound to `remediation_record_id`; server records `RETEST_EVIDENCE (fix_confirmed = false)` and atomically transitions `RETEST_PENDING -> ACCEPTED` (`state_version + 1`). Any subsequent fix requires `remediation_attempt_no = N + 1`.
  * *2b. Internal verification (`VERIFIED_INTERNAL`)*: Defender certifies the fix on `remediation_record_id` with `verification_notes_ciphertext` and `verifier_authored_fix` disclosure; state transitions to `VERIFIED_INTERNAL`.
  * *2c. Researcher unresponsive (`>= 14 days`)*: Defender submits `audit_justification_ciphertext` (Class C) and transitions `RETEST_PENDING -> CLOSED_UNVERIFIED_TIMEOUT`.
  * *2d. Simultaneous conflicting action (`409 Conflict`)*: If a researcher submits `RETEST_FAILED` while a defender simultaneously submits `CLOSED_UNVERIFIED_TIMEOUT`, the second transaction fails the `state_version` check and returns HTTP `409 Conflict`.

#### Use Case `UC-05`: Restore Guest or Registered User Keys & Rotate Compromised Guest Token
* **Primary Actor**: Account-Less Researcher (`Guest Hunter`) or Registered User (`Hunter` / `Defender` / `Owner`).
* **Preconditions**: Actor possesses an Argon2id + AES-256-GCM encrypted `.bbt-recovery.json` (guest) or `.bbt-user-keys.json` (registered user) file and its recovery passphrase.
* **Main Success Scenario**:
  1. Actor navigates to `/report/restore` (guest) or `/settings/keys` (registered user, `SCR-10`) and selects their backup JSON file.
  2. Browser reads the file strictly in local memory via `FileReader` (zero network upload), derives the 256-bit key via Argon2id S2K, and verifies the AES-256-GCM authentication tag (`gcm_auth_tag`).
  3. For guests: Browser decrypts `{ access_token, ephemeral_private_key }`, imports the private key into `IndexedDB`, and authenticates against `/report/track/BBT-RPT-XXXX` preserving durable `guest_actor_id` attribution.
  4. If the guest suspects their `access_token` was exposed, they click "Rotate Tracking Token," which signs a rotation request with their Ed25519 report key (`FR-1.6f`), invalidates the old `guest_token_hash` on the server, and downloads a new `.bbt-recovery.json` package.

#### Use Case `UC-06`: Onboard Tenant, Verify DNS, Configure Master Recovery Key & Sign `security.txt`
* **Primary Actor**: Organization Owner (`ORG_OWNER`).
* **Preconditions**: Authenticated user creating or configuring an organization workspace.
* **Main Success Scenario**:
  1. Owner completes the Guided Onboarding Wizard (`SCR-07`) and publishes the `_bbt-challenge.<domain>` DNS TXT record verified by the server (`FR-2.5`).
  2. Browser configures `openpgp.config.v6Keys = true` and generates the owner's Curve25519 keypair plus the offline **Organization Master Recovery Keypair** (`recovery_public_key`).
  3. Owner downloads the Argon2id-encrypted private Master Recovery Key file and completes the mandatory in-browser test decryption challenge (`Uint8Array` buffers zeroized immediately after verification).
  4. Owner assigns authorized defenders to `PROGRAM_DEFENDER` (incrementing `recipient_set_version`) and cleartext-signs the generated RFC 9116 `security.txt` manifest in-browser for publication at `/.well-known/security.txt`.

#### Use Case `UC-07`: Enforce Scheduled SLA / Inactivity Timers & Verify Hash-Chained Audit Ledger
* **Primary Actor**: Organization Reviewer (`ORG_DEFENDER`), Read-Only Auditor (`ORG_READONLY`), or Hourly System Cron.
* **Preconditions**: Active vulnerability reports exist within the tenant workspace.
* **Main Success Scenario**:
  1. Hourly lifecycle cron job (`/api/cron/lifecycle-evaluate`) evaluates Class A `sla_triage_due` and `sla_remediation_due` deadlines, transitions `NEED_MORE_INFO` reports inactive for `>= 14 days` to `CLOSED_INCOMPLETE`, and purges expired `PENDING_UPLOAD` reservations older than 30 minutes.
  2. Approaching or breached SLA targets trigger Class A metadata-only email and webhook alerts containing a signed Audit Checkpoint Receipt.
  3. Defenders and `ORG_READONLY` auditors inspect `/dashboard/audit` (`SCR-12`) to verify gapless `seq_no` ordering, RFC 8785 JCS `row_hash` continuity, and external checkpoint signatures.

### 2.3 Sequence & Lifecycle Behavioral Diagrams (`Figure 4.2` to `Figure 4.4`)

* **Figure 4.2: Sequence Diagram — Browser-Side OpenPGP Submission & Presigned Upload (`UC-01`)**:
  ![Figure 4.2: Browser-Side OpenPGP Submission](../requirements/diagrams/fig4_3_seq_submission.png)
* **Figure 4.3: Sequence Diagram — In-Browser Decryption, Triage & CVSS Assessment (`UC-02`)**:
  ![Figure 4.3: In-Browser Decryption & Confidential Triage](../requirements/diagrams/fig4_4_seq_decryption.png)
* **Figure 4.4: State Machine Diagram — 15-State Remediation & Attested Retest Lifecycle (`UC-03` & `UC-04`)**:
  ![Figure 4.4: 15-State Remediation & Attested Retest Lifecycle State Machine](../requirements/diagrams/fig4_5_statemachine.png)

---

## Part 3: Quantifiable Non-Functional Requirements (`NFR-01` to `NFR-09` — Latency, Security & Uptime)

| NFR ID | Quality Pillar | Provisional Acceptance Target | Reference Measurement Condition & Verification Method |
| :---: | :--- | :--- | :--- |
| **`NFR-01`** | **Latency (Server API)** | `p95 <= 300 ms` warm / `<= 1,200 ms` cold | k6 (`20 VUs`, `60s`, 500-report DB, Node.js 22 + Neon PgBouncer) |
| **`NFR-02`** | **Latency (Client Crypto)** | `< 50 ms` keygen; `~200–400 ms` Argon2id; `<= 1,500 ms` encrypt | Playwright (`100 KB` payload, `5` recipients, Chromium 120+, 50 runs) |
| **`NFR-03`** | **Security (Forced RLS)** | `0` cross-tenant rows (`bbt_app_runtime` `NOBYPASSRLS`) | Interleaved Tenant A / Tenant B pooled RLS test (`TC-SEC-01`) |
| **`NFR-04`** | **Accessibility & Usability** | `0` axe-core AA errors + manual keyboard/SR pass; `SUS >= 75.0` | `@axe-core/playwright` + manual audit across `SCR-01..12` + 3–5 peer study |
| **`NFR-05`** | **Security (XSS Corpus & CSP)** | `100%` neutralization of 100-vector OWASP XSS corpus | Vitest `rehype-sanitize` corpus test (`TC-SEC-02`) + Playwright CSP check |
| **`NFR-06`** | **Reliability (Quotas)** | `50 MB` logical DB / `2 GB` R2 (`<= 10` tenants); warn `90%`, block `100%` | Pre-upload reservation, `HeadObject` & HTTP `413` test (`TC-SEC-04`) |
| **`NFR-07`** | **Security (Audit Chain)** | `0` `UPDATE`/`DELETE` grants; RFC 8785 JCS hash + checkpoint receipt | Privilege denial & tamper-detection integration test (`TC-SEC-05`) |
| **`NFR-08`** | **Determinism (CVSS 3.1)** | `100%` parity on 45 NVD fixtures + all `2,592` Base combinations | `verify_cvss_engine.py` & Vitest exhaustive 2,592-vector suite (`TC-CVSS-01`) |
| **`NFR-09`** | **Uptime & Continuity** | `>= 99.5%` uptime (`<= 3.65h/mo`); `RPO <= 24h`, `RTO <= 4h` (ciphertext+meta) | `/api/v1/health` 5-min probe & sandbox DB/R2 + Master Key restore drill (`TC-OPS-01`) |

---

## Document Submission & Milestone Sign-Off

This Week 2 Software Requirements Specification (`SRS`, Revision 2.2) is submitted for academic supervisor review and milestone endorsement as the IEEE 830 / ISO/IEC/IEEE 29148 requirements baseline for **BugBountyTrack** (`PTUT - PRJ - 089`) under the Department of Software Engineering Technology, Punjab Tianjin University of Technology (PTUT), Lahore.

| Role | Name & Designation | Roll No. / Section | Signature | Date |
| :--- | :--- | :--- | :--- | :--- |
| **Student Author** | **Taha Asadullah** (B.Sc. Software Engineering Technology) | `24-ST-013` / `SET-B` | *Signed: Taha Asadullah* | October 11, 2026 |
| **Project Supervisor** | **Sir Umar Hayat** (Assistant Professor, Dept. of SET, PTUT) | Faculty Supervisor | ______________________ | ____________ |
