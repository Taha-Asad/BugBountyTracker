# Week 1 Deliverable (Part B): Project Charter, Problem Statement & 5 Core MVP Features

## Project BugBountyTrack — Multi-Tenant Vulnerability Disclosure Platform

**Document Release State**: Version 3.2.0 (Gate 1 Certified — Zero-Trust Specification Standard)

**Standard Compliance**: IEEE 830-1998, ISO/IEC/IEEE 29148:2018, RFC 9116, RFC 9580, FIRST.org CVSS v3.1

---

## 1. Project Charter & Academic Control Metadata

| Attribute | Specification |
| :--- | :--- |
| **Institution** | Punjab Tianjin University of Technology (PTUT), Lahore |
| **Department** | Department of Software Engineering Technology |
| **Degree Program** | BS Software Engineering Technology (5th Semester Capstone) |
| **Project ID** | `PTUT - PRJ - 089` |
| **Project Title** | **BugBountyTrack — Private Bug Bounty & Vulnerability Disclosure Platform** |
| **Category** | 9. Cybersecurity, Privacy & LegalTech |
| **Student Author & Lead** | Taha Asadullah (Roll No: `24-ST-013`, Section: `SET-B`) |
| **Academic Supervisor** | Sir Umar Hayat (Assistant Professor, PTUT Lahore) |
| **Milestone Scope** | Week 1 (Part B): Project Charter, Problem Statement & 5 Core MVP Features |

---

## 2. Finalized 1-Paragraph Academic Problem Statement

> **While established vulnerability platforms and source-code hosts offer free entry tiers (such as HackerOne Essential VDP or GitHub Security Advisories), they operate on a server-managed model where sensitive exploit payloads are stored in plaintext on third-party vendor infrastructure, or are locked to single-forge repository ecosystems. Teams unwilling to delegate plaintext zero-day access to external vendors typically fall back to ad-hoc communication channels (email, issue trackers, social media DMs), exposing exploit reproduction steps across unencrypted mail servers and creating legal ambiguity due to missing RFC 9116 Safe Harbor policies. Furthermore, existing issue trackers and entry-level VDP tiers treat vulnerability resolution as an informal status change ("Closed" or "Resolved"), creating a "fix-and-forget" verification gap where patches are deployed without verifiable Git commit linkage or attested researcher retesting. BugBountyTrack resolves these gaps by delivering a lightweight, multi-tenant Vulnerability Disclosure Platform (VDP) that automates signed RFC 9116 `security.txt` policy generation, enforces zero-knowledge client-side OpenPGP exploit payload encryption (RFC 9580 v6 Curve25519), provides deterministic CVSS 3.1 scoring, and governs remediation through an evidence-based, Git-linked retest state machine.**

---

## 3. Project Charter: Objectives, Scope & Anti-Goals

### 3.1 Core Engineering Objectives

1. **Zero-Knowledge Payload Isolation**: Ensure the platform server never holds private decryption or signing keys and never processes plaintext vulnerability titles, descriptions, reproduction steps, or PoC attachments.
2. **Standardized Legal & Policy Discovery**: Enable organizations to generate, client-side cleartext-sign (RFC 9116 §2.3), and publish compliant `/.well-known/security.txt` policies with Disclose.io-aligned Safe Harbor terms.
3. **Frictionless Dual-Lane Intake**: Support both authenticated researchers (`HUNTER`) and 60-second account-less guest submitters equipped with portable, Argon2id-encrypted recovery packages (`.bbt-recovery.json` v1).
4. **Deterministic Severity & Remediation Governance**: Eliminate subjective severity disputes via FIRST.org CVSS v3.1 calculation and enforce a strict Git-commit-linked (`[0-9a-f]{40}`) and researcher-attested retest state machine.

### 3.2 Explicit Scope Boundaries & Anti-Goals (Savour Each Bite Doctrine)

To guarantee build-proof engineering quality within the academic evaluation timeline, the following boundaries are strictly enforced:

| Scope Category | In-Scope (Committed Deliverable) | Out-of-Scope / Deferred Anti-Goals |
| :--- | :--- | :--- |
| **Cryptography** | Browser-side `openpgp.js` v6 (`RFC 9580 Curve25519`: Ed25519 + X25519), 64-character SHA-256 hex fingerprints, `Argon2id S2K` (`IndexedDB`), multi-defender `PKESK` (N ≤ 10), offline recovery key. | Legacy RSA / OpenPGP v4 keys, server-side key escrow, hardware HSM integration, and 24-word BIP-39 mnemonic seeds. |
| **Intake & Triage** | Public & private token-gated programs, Account-Less Guest intake (`.bbt-recovery.json`), two-lane encrypted discussions, neutral `operational_label` routing. | Automated AI/LLM vulnerability triage, automated DAST/scanner execution, and open public researcher marketplaces. |
| **Remediation & Verification** | GitHub REST API v3 commit SHA verification, SHA-256 `CONFIG_INFRASTRUCTURE` hashing, attested retest state machine, Redacted Closure Evidence exports. | Multi-VCS integrations (GitLab/Bitbucket), automated CI/CD patch generation, and CVSS v4.0 MacroVectors. |
| **Commercial & Billing** | Community free tier (500 MB R2, 5 active reports + `QUOTA_HELD` queue) and Team tier (`$49/mo` via Lemon Squeezy Merchant of Record). | Real-money researcher bounty escrow/payout rails, tax form processing (W-9/W-8BEN), and enterprise SAML/SCIM SSO. |

---

## 4. The 5 Core MVP Features

The following five core features directly resolve the four operational frictions identified during target user discovery and define the Minimum Viable Product (MVP):

### Feature 1: Hosted RFC 9116 `security.txt` & Safe Harbor Policy Generator (`FR-2`)

* **Problem Solved**: Eliminates researcher legal ambiguity and provides standardized, machine-readable discovery for defensive disclosure programs.
* **Technical & Cryptographic Boundary**:
  * Generates an RFC 9116 compliant policy incorporating `Contact`, `Expires`, `Encryption` (URI to program OpenPGP v6 public key), `Policy` (URI to Safe Harbor scope), `Preferred-Languages`, and `Canonical` following automated DNS TXT domain ownership verification (`_bbt-challenge.<domain>`).
  * **Client-Side Cleartext Signing (RFC 9116 §2.3)**: Because the backend is strictly zero-knowledge and never holds private keys, the `security.txt` file is **cleartext-signed inside the Organization Owner's browser** using their local Ed25519 private signing key (`openpgp.js` v6). The organization publishes the signed file at `https://[org-domain]/.well-known/security.txt`, while BugBountyTrack serves preview and signature verification at `/api/v1/programs/[slug]/security.txt`.
  * Includes a guided Safe Harbor policy builder based on Disclose.io Core terms defining authorized testing scope and good-faith legal protection.
* **Acceptance Criteria**: Endpoint serves HTTP 200 with MIME type `text/plain; charset=utf-8`, passes automated RFC 9116 syntax validation, and verifies cryptographically against the organization's advertised public key.

---

### Feature 2: Zero-Knowledge Client-Side OpenPGP v6 Payload Encryption & Neutral Labeling (`FR-3`)

* **Problem Solved**: Prevents plaintext exploit exposure in transit and guarantees zero-day confidentiality at rest even under a total database breach.
* **Technical & Cryptographic Boundary**:
  * Executes strictly inside the client browser runtime (`openpgp.js` v6 via `WebCrypto` and WebAssembly).
  * Enforces **RFC 9580 Version 6 Curve25519** (`Ed25519` signing + `X25519` encryption) keys with **64-character hexadecimal SHA-256 fingerprints**. Private keys are encrypted at rest with **Argon2id S2K** (`t=3`, `m=64 MiB`, `p=4`, enabled via CSP `'wasm-unsafe-eval'`) and stored exclusively in browser **`IndexedDB`** (never in unencrypted browser storage or server tables).
  * Encrypts all sensitive report fields—including the vulnerability title (`title_ciphertext`), description, reproduction steps, impact assessment, and PoC attachments (up to 25 MB uploaded directly to Cloudflare R2 via presigned URLs)—using multi-recipient OpenPGP Public-Key Encrypted Session Key (`PKESK`) packets addressed to all active **Program Defenders** (`N ≤ 10` via `PROGRAM_DEFENDER`), the **Offline Organization Master Recovery Key** (`recovery_public_key`), and the **Submitter/Guest Key**, guarded by optimistic concurrency counter `recipient_set_version`.
  * Captures a server-readable neutral `operational_label` enum (`AUTHENTICATION_BYPASS`, `INJECTION_VULNERABILITY`, `INFORMATION_DISCLOSURE`, `CROSS_SITE_SCRIPTING`, `ACCESS_CONTROL_ISSUE`, `DENIAL_OF_SERVICE`, `OTHER`) so queue filtering and email/webhook notifications never leak vulnerability titles.
* **Acceptance Criteria**: Direct inspection of PostgreSQL rows and Cloudflare R2 objects confirms sensitive titles, descriptions, and attachments exist exclusively as OpenPGP ciphertext blocks (`-----BEGIN PGP MESSAGE-----`).

---

### Feature 3: Deterministic CVSS 3.1 Severity Scoring Engine (`FR-4`)

* **Problem Solved**: Eliminates subjective severity arguments between ethical researchers and organization triage leads.
* **Technical Boundary**:
  * Implemented as a standalone, deterministic pure TypeScript function adhering strictly to the **FIRST.org Common Vulnerability Scoring System v3.1** specification (using the exact `8.22` exploitability coefficient and standard integer-math `RoundUp`).
  * Evaluates all 8 Base Metrics: Attack Vector (`AV`), Attack Complexity (`AC`), Privileges Required (`PR`), User Interaction (`UI`), Scope (`S`), Confidentiality (`C`), Integrity (`I`), and Availability (`A`).
  * Computes the numerical Base Score (`0.0–10.0`), assigns the qualitative severity rating (`NONE`, `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`), generates the canonical vector string (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`), and preserves both the researcher's suggested vector (`cvss_suggested`) and the defender's verified rating (`cvss_score`).
* **Acceptance Criteria**: Automated verification confirms 100% mathematical parity across all 2,592 base metric combinations and all 45 canonical FIRST.org/NIST test fixtures.

---

### Feature 4: Dual-Lane Intake (Account-Less Guest & Authenticated Hunter) & Encrypted Triage Portal (`FR-1`, `FR-5`, `FR-8`)

* **Problem Solved**: Unifies fragmented disclosures into a role-isolated workspace while removing mandatory registration barriers for drive-by researchers.
* **Technical & Privacy Boundary**:
  * Built with Next.js App Router and PostgreSQL (enforcing Row-Level Security via `SET LOCAL app.current_tenant_id = :org_id`), supporting both **Authenticated Hunters** and **Account-Less Guest Reporters**.
  * Guest submissions generate a durable `guest_actor_id` (UUIDv4), a downloadable Argon2id-encrypted recovery package (`.bbt-recovery.json` v1) for multi-device restoration at `/report/restore`, and an unguessable tracking URL (`/report/track/BBT-RPT-XXXX#token=<access_token>`). On initial load, client JavaScript reads the `#token=` URI fragment into memory and immediately scrubs the address bar via `window.history.replaceState()`, while the server stores only `guest_token_hash`.
  * Enforces two cryptographically isolated communication lanes: (1) **Researcher–Organization Conversation** (encrypted for Submitter + Program Defenders + Org Recovery Key) and (2) **Reviewer Internal Notes** (encrypted strictly for Program Defenders + Org Recovery Key).
  * Renders decrypted Markdown safely through a strict AST sanitizer (`unified` / `remark-parse` / `rehype-sanitize`) blocking stored XSS and external beacons.
* **Acceptance Criteria**: Authorized Program Defenders and returning Reporters (via `IndexedDB` or imported `.bbt-recovery.json`) decrypt messages strictly in-browser; unauthorized cross-tenant or cross-reporter requests receive HTTP 403 Forbidden.

---

### Feature 5: Git-Linked Remediation & Attested Retest State Machine (`FR-6`, `FR-7`)

* **Problem Solved**: Eliminates the "Fix-and-Forget" verification gap by binding vulnerability closure to verifiable code/configuration artifacts and independent retesting.
* **Technical Boundary**:
  * Enforces a deterministic finite state machine governing the vulnerability lifecycle (`NEW → TRIAGING → ACCEPTED → FIX_PROPOSED (FIX_COMMITTED) → RETEST_PENDING → [TERMINAL STATE]`).
  * Advancing a report to `FIX_PROPOSED` (`FIX_COMMITTED`) requires binding either a verified **40-character GitHub commit SHA** (`[0-9a-f]{40}`, verified on the target branch via the GitHub REST API v3) or a client-computed **64-character SHA-256 configuration hash** (`CONFIG_INFRASTRUCTURE`), plus the target deployment environment (`Staging`, `Pre-Production`, `Production`).
  * From `RETEST_PENDING`, tickets transition to resolved exclusively under three audited outcomes: `VERIFIED_RESEARCHER` (independent finder confirmation), `VERIFIED_INTERNAL` (defender attestation), or `CLOSED_UNVERIFIED_TIMEOUT` (≥ 14-day grace period with written administrative justification; never counted as a verified fix), while failed retests (`RETEST_FAILED`) return the ticket to `ACCEPTED`.
  * Non-remediation closures (`CLOSED_INCOMPLETE`, `RISK_ACCEPTED` / `CLOSED_RISK_ACCEPTED`, `REJECTED_SPAM`, `REJECTED_INVALID`, `DUPLICATE`, `WITHDRAWN`) are governed by strict reopening and audit rules inside an append-only, SHA-256 hash-chained (`prev_hash`) audit ledger (`INSERT` and `SELECT` privileges only).
* **Acceptance Criteria**: State machine guards reject any closure transition lacking verified commit/hash evidence, actor attribution, and required justification metadata.

---

## 5. Document Endorsement & Milestone Sign-Off

| Signatory Role | Name & Academic Designation | Status / Signature | Date |
| :--- | :--- | :--- | :--- |
| **Submitted By (Student Author)** | **Taha Asadullah** (Roll No: `24-ST-013`, Section: `SET-B`, BS Software Engineering Technology, PTUT Lahore) | *Signed: Taha Asadullah* | October 2026 |
| **Reviewed By (Academic Supervisor)** | **Sir Umar Hayat** (Assistant Professor, Department of Software Engineering Technology, PTUT Lahore) | `[ ] Approved` / `[ ] Revisions` — Signature: `[__________________]` | `[____________]` |
