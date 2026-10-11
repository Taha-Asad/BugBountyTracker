# Week 1 Task & Deliverable: Problem Discovery & User Personas

| Attribute | Details |
| :--- | :--- |
| **Project ID** | `PTUT - PRJ - 089` |
| **Project Title** | **BugBountyTrack — Private Bug Bounty & Vulnerability Disclosure Platform** |
| **Student Author** | Taha Asadullah (Roll No: `24-ST-013`, Section: `SET-B`) |
| **Academic Supervisor** | Sir Umar Hayat (Assistant Professor, PTUT Lahore) |
| **Milestone** | **Week 1** — Problem Discovery & User Personas (**Gate 1: DoR Part I**) |
| **WBS Task IDs** | `BBT-W01-T01` (4h), `BBT-W01-T02` (6h), `BBT-W01-T03` (4h) — **Total: 14 Hours** |

---

## Supporting Deliverable Documents (Google Drive Links)

| Deliverable Document | Scope Covered | Google Drive Link |
| :--- | :--- | :--- |
| **Document 1: User Personas & Discovery Interviews** | Executive Context, 4 Operational Frictions, and 2 Detailed User Personas (Hunter & Defender) with Empathy Maps | [View User Personas & Discovery Doc (Google Drive)](https://docs.google.com/document/d/1drXMfAk4pIKc_9aMKZav62KfVZQ04--zT6VyuhDZKFA/edit?usp=drive_link) |
| **Document 2: Project Charter, Problem Statement & 5 Core MVP Features** | Project Charter, Scope Boundaries, Finalized 1-Paragraph Problem Statement, and 5 Core MVP Features | [View Project Charter & MVP Features Doc (Google Drive)](https://docs.google.com/document/d/1-N7Pv-3CO95XNWcvjSga6vf0vDKOvFKdPQ5l6uGpQJY/edit?usp=drive_link) |

---

## Part 1: Target User Interviews — 4 Operational Frictions Identified

Structured discovery interviews across both sides of the vulnerability disclosure workflow—**independent ethical security researchers** who discover flaws and **startup engineering leads** who remediate them—identified **four structural operational frictions**:

1. **Third-Party Server-Managed Plaintext Exposure (Zero-Knowledge Gap)**
   * While established vulnerability platforms and source-code hosts offer free entry tiers (such as HackerOne Essential VDP or GitHub Security Advisories), they operate on a **server-managed model** where raw exploit descriptions and proof-of-concept (PoC) payloads are stored in **plaintext on third-party vendor servers** (accessible to vendor operations, cloud intermediaries, and support databases), or lock teams to a single repository forge rather than covering an organization's full web application and API surface.
2. **Confidentiality Leaks in Ad-Hoc Email Channels (Insecure Transit & Storage)**
   * Engineering teams unwilling to store unpatched zero-day exploits in plaintext on third-party vendor databases typically fall back to generic `security@company.com` email inboxes, shared issue trackers, or chat messages. Standard email (SMTP) provides no end-to-end cryptographic isolation—leaving live SQL injection payloads, authentication bypass steps, and customer data proofs sitting in plaintext across mail servers, shared inboxes, and employee ticket queues.
3. **Legal Ambiguity & Reporter Onboarding Friction (Missing Safe Harbor & Account Fatigue)**
   * Without an official, cryptographically signed RFC 9116 `/.well-known/security.txt` policy defining explicit **Safe Harbor** terms (authorized testing scope and good-faith legal protection), ethical researchers face legal uncertainty under cybercrime statutes and frequently withhold reports. Furthermore, requiring mandatory account registration just to report a single vulnerability drives away one-off ethical reporters.
4. **The "Fix-and-Forget" Verification Gap (Unverified Ticket Closures)**
   * Both general issue trackers (Jira, Linear, GitHub Issues) and entry-level VDP tiers treat vulnerability remediation as an informal text status update ("Closed" or "Resolved"). Neither enforces verifiable linkage to a real Git commit SHA or configuration hash, nor requires an attested retest workflow with the reporting researcher—frequently resulting in superficial or incomplete patches that fix only a single symptom while leaving the underlying vulnerability exploitable.

---

## Part 2: The 2 Detailed User Personas

### Persona 1: Alex Rivera — "The Hunter" (External Ethical Security Researcher)

* **Demographic & Role**: Age 23; Independent Security Researcher & Undergraduate Cybersecurity Student (2 years bug bounty experience, Top 5% university CTF competitor).
* **Operating Environment & Tooling**: Kali Linux, macOS, Firefox Developer Edition, Burp Suite Professional, `ffuf`, `nuclei`, `curl`, Python (`requests`), GnuPG CLI.
* **Core Goals & Motivations**:
  1. **Frictionless Ethical Disclosure**: Report critical vulnerabilities rapidly—either via an authenticated researcher account (to build verifiable portfolio reputation) or via a 60-second account-less guest submission.
  2. **Explicit Legal Safe Harbor**: Verify via a signed `/.well-known/security.txt` policy that good-faith testing within scope will not trigger legal retaliation.
  3. **Objective Severity Scoring**: Receive deterministic, math-based severity evaluation (FIRST.org CVSS v3.1) rather than arguing over subjective ratings.
* **Critical Pain Points & Frustrations**:
  1. **The Black Hole ("Ghosting")**: Submitting detailed vulnerability reports to `security@target.com` and receiving zero acknowledgment or status updates.
  2. **Plaintext Payload Exposure**: Refusing to send live zero-day exploit scripts over unencrypted email or store them in plaintext on third-party servers.
  3. **Subjective Severity Downgrades**: Watching organizations arbitrarily downgrade high-impact vulnerabilities to "Low" without a transparent CVSS v3.1 vector breakdown.
  4. **Premature Closures Without Retest**: Discovering that a developer pushed an incomplete regex filter and closed the ticket without inviting Alex to verify whether the exploit was actually neutralized.
* **Empathy Map (Alex Rivera)**:
  * **Says**: *"I found a critical IDOR exposing customer records. I want to report it responsibly, but I need Safe Harbor assurance and encrypted delivery."*
  * **Thinks**: *"Will they actually patch the root cause, or will someone paste my plaintext PoC into a public Slack channel and close the ticket untested?"*
  * **Does**: Inspects `/.well-known/security.txt` before testing; captures HTTP requests in Burp Suite; verifies fixes when invited to retest.
  * **Feels**: Cautious about legal risk; frustrated by silent inboxes; respected when an engineering team shares a verified fix for retest.

---

### Persona 2: Sarah Chen — "The Defender" (Startup CTO / Security Triage Lead)

* **Demographic & Role**: Age 31; CTO & Lead Full-Stack Engineer at a 7-person B2B FinTech SaaS startup (8 years full-stack engineering experience).
* **Operating Environment & Tooling**: macOS, VS Code, TypeScript, Next.js, Neon PostgreSQL, GitHub Actions, Docker, Vercel, Linear.
* **Core Goals & Motivations**:
  1. **Zero-Knowledge Payload Confidentiality**: Provide external researchers with a client-side encrypted intake portal where only her authorized program defenders (`PROGRAM_DEFENDER`) can decrypt the exploit in-browser—never a third-party platform vendor.
  2. **Audit-Ready Compliance Evidence**: Publish a browser-signed RFC 9116 `security.txt` policy and export **Redacted Closure Evidence** certificates (proving lifecycle timestamps, verified Git commit SHAs, and retest sign-off without exposing raw exploit instructions) for enterprise B2B security questionnaires.
  3. **Verifiable Patch Governance**: Guarantee that every vulnerability closure is bound to a verified 40-character GitHub commit SHA (or 64-character SHA-256 configuration hash) and an attested retest outcome.
* **Critical Pain Points & Frustrations**:
  1. **Scanner Spam Overload**: Wasting engineering hours filtering automated scanner noise and low-effort bounty begging in a shared `security@` email inbox.
  2. **CLI PGP Key-Management Friction**: Setting up command-line GnuPG keyrings and email plugins across a 7-person engineering team is error-prone; she needs key generation (`RFC 9580 v6 Curve25519`) and multi-recipient encryption/decryption handled transparently inside the browser.
  3. **Vendor Database Breach Risk**: Refusing to store unpatched zero-day exploits in plaintext on third-party VDP vendor servers or internal bug trackers where a third-party breach would expose every open vulnerability.
  4. **Uncertain Patch Effectiveness**: Merging a developer pull request without a structured retest workflow to confirm the vulnerability is truly eliminated in staging/production.
* **Empathy Map (Sarah Chen)**:
  * **Says**: *"Free VDP tiers store raw exploits in plaintext on vendor servers, while our `security@` email inbox is flooded with unencrypted scanner noise."*
  * **Thinks**: *"If a researcher reports a real flaw, I need it encrypted client-side for my designated defenders only, with an offline recovery key backup and proof that our Git commit fixed it."*
  * **Does**: Reviews GitHub pull requests; manages production deployments; answers B2B customer security audits; assigns triage tasks.
  * **Feels**: Protective of customer data and limited engineering time; relieved when reports arrive with deterministic CVSS vectors and structured retest states.

---

## Part 3: Finalized 1-Paragraph Problem Statement

> **While established vulnerability platforms and source-code hosts offer free entry tiers (such as HackerOne Essential VDP or GitHub Security Advisories), they operate on a server-managed model where sensitive exploit payloads are stored in plaintext on third-party vendor infrastructure, or are locked to single-forge repository ecosystems. Teams unwilling to delegate plaintext zero-day access to external vendors typically fall back to ad-hoc communication channels (email, issue trackers, social media DMs), exposing exploit reproduction steps across unencrypted mail servers and creating legal ambiguity due to missing RFC 9116 Safe Harbor policies. Furthermore, existing issue trackers and entry-level VDP tiers treat vulnerability resolution as an informal status change ("Closed" or "Resolved"), creating a "fix-and-forget" verification gap where patches are deployed without verifiable Git commit linkage or attested researcher retesting. BugBountyTrack resolves these gaps by delivering a lightweight, multi-tenant Vulnerability Disclosure Platform (VDP) that automates signed RFC 9116 `security.txt` policy generation, enforces zero-knowledge client-side OpenPGP exploit payload encryption (RFC 9580 v6 Curve25519), provides deterministic CVSS 3.1 scoring, and governs remediation through an evidence-based, Git-linked retest state machine.**

---

## Part 4: The 5 Core MVP Features

These five features directly address the four operational frictions identified during target user discovery and define the core Minimum Viable Product (MVP) scope:

1. **Hosted RFC 9116 `security.txt` & Safe Harbor Policy Generator (`FR-2`)**
   * **What It Does**: Generates a standards-compliant RFC 9116 disclosure policy (`Contact`, `Expires`, `Encryption`, `Policy`, `Preferred-Languages`, `Canonical`) and Disclose.io-aligned Safe Harbor scope definition after automated DNS TXT domain ownership verification (`_bbt-challenge.<domain>`).
   * **Zero-Knowledge Signing Boundary**: To preserve strict zero-knowledge guarantees (the server never holds any private key), the `security.txt` policy is **cleartext-signed inside the Organization Owner's browser** using their client-side Ed25519 private signing key (RFC 9116 §2.3), exported for root-domain hosting at `https://[org-domain]/.well-known/security.txt`, and served for preview/verification at `/api/v1/programs/[slug]/security.txt`.

2. **Zero-Knowledge Client-Side OpenPGP v6 Payload Encryption & Neutral Labeling (`FR-3`)**
   * **What It Does**: Encrypts the vulnerability title (`title_ciphertext`), description, reproduction steps, impact analysis, and PoC attachments (up to 25 MB via presigned Cloudflare R2 uploads) strictly inside the browser via `openpgp.js` (`WebCrypto` / WASM) before network transmission.
   * **Cryptographic & Metadata Boundary**: Uses **RFC 9580 Version 6 Curve25519** (`Ed25519` signing + `X25519` encryption) keys with **64-character SHA-256 hex fingerprints**. Private keys are locked in browser `IndexedDB` via **Argon2id S2K** (`t=3, m=64 MiB, p=4`, enabled via CSP `'wasm-unsafe-eval'`). Every report is encrypted via multi-recipient Public-Key Encrypted Session Key (`PKESK`) packets addressed to the program's active defenders (`PROGRAM_DEFENDER`, up to 10), the organization's **Offline Master Recovery Key** (`recovery_public_key`), and the submitter's key, guarded by optimistic concurrency version `recipient_set_version`. The server sees only a neutral `operational_label` enum (e.g., `AUTHENTICATION_BYPASS`, `INJECTION_VULNERABILITY`) for routing and notifications.

3. **Deterministic CVSS 3.1 Severity Scoring Engine (`FR-4`)**
   * **What It Does**: Implements a pure, deterministic TypeScript calculation engine adhering to the official **FIRST.org CVSS v3.1** specification (using the exact `8.22` exploitability coefficient and standard `RoundUp` arithmetic) across all 8 Base Metrics (`AV`, `AC`, `PR`, `UI`, `S`, `C`, `I`, `A`).
   * **Verification Boundary**: Produces the exact `0.0–10.0` score, qualitative severity rating (`NONE` to `CRITICAL`), and canonical vector string (`CVSS:3.1/AV:.../A:...`), decoupling the researcher's suggested vector (`cvss_suggested`) from the defender's verified assessment (`cvss_score`). Validated with 100% mathematical parity across all 2,592 base metric combinations and 45 canonical FIRST.org/NIST test fixtures.

4. **Dual-Lane Intake (Account-Less Guest & Authenticated Hunter) & Encrypted Triage Portal (`FR-1`, `FR-5`, `FR-8`)**
   * **What It Does**: Supports both **Authenticated Hunters** (who earn portfolio attribution) and **Account-Less Guest Reporters** who submit in under 60 seconds without registering.
   * **Guest Recovery & Privacy Boundary**: Guest submissions generate a durable `guest_actor_id` (UUIDv4), a downloadable Argon2id-encrypted recovery bundle (`.bbt-recovery.json` v1) for multi-device restoration at `/report/restore`, and an unguessable tracking URL (`/report/track/BBT-RPT-XXXX#token=<access_token>`) where client JavaScript immediately scrubs the `#token=` URI fragment from the browser address bar via `window.history.replaceState()` while the server stores only `guest_token_hash`. The triage portal separates the **Researcher–Organization Conversation** lane from the **Reviewer Internal Notes** lane (encrypted exclusively for `PROGRAM_DEFENDER` + Recovery Key) and renders decrypted Markdown through a strict AST sanitizer (`unified` / `remark-parse` / `rehype-sanitize`).

5. **Git-Linked Remediation & Attested Retest State Machine (`FR-6`, `FR-7`)**
   * **What It Does**: Enforces a deterministic remediation lifecycle (`NEW → TRIAGING → ACCEPTED → FIX_PROPOSED (or FIX_COMMITTED) → RETEST_PENDING → [TERMINAL STATE]`).
   * **Evidence & Closure Boundary**: Advancing a report to `FIX_PROPOSED` (`FIX_COMMITTED`) requires binding either a verified **40-character GitHub commit SHA** (checked via GitHub REST API v3 on the target branch) or a client-computed **64-character SHA-256 configuration hash** (`CONFIG_INFRASTRUCTURE`). From `RETEST_PENDING`, tickets close only via explicit, audited outcomes: `VERIFIED_RESEARCHER` (independent finder sign-off), `VERIFIED_INTERNAL` (defender attestation), or `CLOSED_UNVERIFIED_TIMEOUT` (≥ 14-day grace period with written justification; never counted as a verified fix), while failed retests (`RETEST_FAILED`) return the ticket to `ACCEPTED`. Non-remediation closures (`CLOSED_INCOMPLETE`, `RISK_ACCEPTED` / `CLOSED_RISK_ACCEPTED`, `REJECTED_SPAM`, `REJECTED_INVALID`, `DUPLICATE`, `WITHDRAWN`) are tracked distinctly in an append-only SHA-256 hash-chained (`prev_hash`) audit ledger.

---

## Document Endorsement & Milestone Sign-Off

| Signatory Role | Name & Academic Designation | Status / Signature | Date |
| :--- | :--- | :--- | :--- |
| **Submitted By (Student Author)** | **Taha Asadullah** (Roll No: `24-ST-013`, Section: `SET-B`, BS Software Engineering Technology, PTUT Lahore) | *Signed: Taha Asadullah* | October 2026 |
| **Reviewed By (Academic Supervisor)** | **Sir Umar Hayat** (Assistant Professor, Department of Software Engineering Technology, PTUT Lahore) | `[ ] Approved` / `[ ] Revisions` — Signature: `[__________________]` | `[____________]` |
