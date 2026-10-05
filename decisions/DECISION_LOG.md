# Decision Log — BugBountyTrack

**Project**: BugBountyTrack — Vulnerability Disclosure Platform with Remediation Tracking  
**Classification**: Fifth-Semester Project Proposal (Evaluated Prototype) & Commercial Launch Baseline  
**Current Phase**: SDLC Phase 1 (Planning & Requirements Engineering)  
**Last Updated**: 2026-10-05  
**Governing Standard**: Constitution Rule 9 & 10 (Epistemic Precision & Traceable Memory)

---

## State Taxonomy
- **`[CONFIRMED]`**: Formally agreed upon by Taha Asadullah and the engineering team.
- **`[PROPOSED]`**: Recommended by specialist agents, pending Taha's confirmation.
- **`[ASSUMPTION]`**: Working premise assumed true until empirical evidence or user input alters it.
- **`[OPEN QUESTION]`**: High-impact branch point requiring explicit decision before proceeding.
- **`[DEFERRED]`**: Valid concept explicitly postponed to post-semester or downstream release.

---

## 1. Confirmed Decisions (`[CONFIRMED]`)
- **DEC-001**: Project target is a university Fifth-Semester Project under the Application Security sub-field with an approximate 16-week execution window, delivering an **evaluated prototype**.
- **DEC-002**: Technical stack baseline: Next.js 14+ (App Router, TypeScript), Node.js 22 LTS, Neon PostgreSQL 16 (Prisma ORM), OpenPGP.js (client-side cryptography), Cloudflare R2, and Tailwind CSS.
- **DEC-003**: Elimination of hype: No automated AI/LLM triage and no live exploit/PoC automated scanners.
- **DEC-004**: Active mentoring posture is "Build with me", pairing Alexander Cross (`CROSS-DIR`) as orchestrator and Victoria Vance (`VANCE-REQ`) as requirements lead.
- **DEC-005**: All project artifacts must reside in `projects/BugBountyTrack/` conforming to `projects/PROJECT_SCHEMA.md`.
- **DEC-006**: **Core Objective**: Focus on structured vulnerability reporting connected to verifiable fix references, retest evidence, and accountable closure.
- **DEC-007**: **State Machine Verification Scope**: The remediation state machine is an **integration-tested finite state machine** enforced at the application and database level; it is not claimed to be mathematically formally verified.
- **DEC-008**: **VCS Linkage Scope**: Checking a Git commit SHA confirms commit existence via API; branch inclusion is verified via GitHub compare API; it does **not** prove runtime fix efficacy or deployment.
- **DEC-009**: **Exploratory Evaluation**: Project evaluation is an exploratory peer study (3–5 peers with 2 containerized reference apps like OWASP Juice Shop), providing empirical qualitative/quantitative data rather than claims of industry-wide proof.
- **DEC-010**: **Document Governance**: Proposal is a working draft until approved by the university department.
- **DEC-011**: **Tenancy Architecture**: Multi-tenant SaaS architecture where multiple organizations host isolated programs on one shared platform instance.
- **DEC-012**: **Mandatory PGP Constraint & Library**: PGP encryption is a strict project requirement implemented using the maintained `openpgp.js` library.
- **DEC-013**: **Program-Scoped Multi-Defender Key Management & Recipient Boundary**:
  - Program directory and public policy pages are discoverable.
  - Submissions support both frictionless account-less guest intake (DEC-020) and registered researcher accounts.
  - Report decryption access is bounded to the submitting researcher/ephemeral key, the offline organization recovery key, and active defenders explicitly assigned to that specific program (up to 10 authorized defenders).
  - Key concurrency is governed by an integer `recipient_set_version`; submissions and replies targeting stale versions are rejected with `409 Conflict`.
- **DEC-014**: **Evidence Preservation & Safe Rendering**: Original vulnerability descriptions, PoC text, and sensitive remediation notes are preserved unmodified. Safe rendering (AST-level HTML escaping, strict markdown parsing, code-block containment) is enforced on the client after decryption.
- **DEC-015**: **Remediation & Retest Verification Rules**:
  - Fix declaration is strictly decoupled from retest verification.
  - Remediation evidence supports both code commits (validated via GitHub API) and non-code fixes (e.g., infrastructure config, WAF rules, DNS updates).
  - Internal verification must be performed by an authorized user with access to the evidence; the audit record explicitly tracks whether the verifier also implemented the fix.
  - Required verification audit fields: Tested version/environment, retest steps, outcome, evidence reference, verifier identity, organizational relationship, implementer flag, and timestamp.
  - Distinct terminal states: `VERIFIED_RESEARCHER`, `VERIFIED_INTERNAL`, `CLOSED_UNVERIFIED_TIMEOUT`, `RISK_ACCEPTED`, `REJECTED_SPAM`, `REJECTED_INVALID`, `DUPLICATE`, `WITHDRAWN`.
  - Closing under `CLOSED_UNVERIFIED_TIMEOUT` requires an **explicit authorized user action and recorded rationale**; expiration of a grace period alone never triggers automated closure or indicates successful verification.
  - Reopening is supported with a mandatory recorded reason, returning status to `TRIAGING`.
- **DEC-016**: **Assistance vs. Security Boundary**: Client-side completeness checks are advisory user assistance, not trusted server-enforced security validation.
- **DEC-017**: **Key Management Boundaries & Failure Modes**:
  - Losing one recipient's private key removes that recipient's access to historical messages; other recipients possessing their own private keys retain decryption capability.
  - Key rotation applies to new replies in existing threads as well as new reports. Messages record recipient key fingerprints.
  - Attachments use direct presigned uploads to Cloudflare R2 with client-side OpenPGP multi-recipient encryption.
  - Trust assumption: The client browser and platform-delivered JavaScript code are assumed trusted.
- **DEC-018 (ADR-007)**: **Private Programs & Tokenized Invitation Lifecycle**:
  - Organizations can set program visibility to `PUBLIC` or `INVITE_ONLY`.
  - Invitations are stored exclusively as SHA-256 `token_hash` values, expire after 72 hours, are single-use, and validate against target recipient email addresses.
  - Commercial launch feature.
- **DEC-019 (ADR-008)**: **Audited Historical Session Key Re-Wrapping**:
  - Newly assigned program defenders do not possess historical keys and cannot decrypt reports filed prior to their assignment.
  - Historical access is granted via client-side re-wrapping of the symmetric session key ($K_S$) by an existing authorized defender using standard OpenPGP PKESK packets. Every re-wrap emits an immutable audit event (`HISTORICAL_ACCESS_GRANTED`).
- **DEC-020 (ADR-009)**: **Account-Less (Guest) Vulnerability Submission**:
  - Researchers do not need to register an account, set a password, or configure TOTP to submit findings.
  - The client browser generates an ephemeral Curve25519 keypair in memory.
  - Submissions are encrypted to program defenders, the offline organization recovery key, and the ephemeral report key.
  - The server issues an opaque tracking URL (`/report/track/BBT-RPT-XXXX?token=<secret>`), allowing anonymous dialogue and retest verification.
  - Registered researchers can optionally claim past report tokens to build their portfolio.
  - Supersedes `DEF-005`.
- **DEC-021 (ADR-010)**: **Offline Organization Master Recovery Key**:
  - During onboarding, an Organization Master Recovery Keypair (`K_rec_pub`, `K_rec_priv`) is generated in the browser.
  - `K_rec_pub` is saved on the server and added as a mandatory PKESK recipient on every report.
  - `K_rec_priv` is exported offline as an emergency recovery kit. Organization activation is gated on a mandatory browser test decryption challenge.
- **DEC-022 (ADR-011)**: **Merchant of Record (Lemon Squeezy) Billing Architecture**:
  - Replaces direct Stripe integration. Lemon Squeezy serves as Merchant of Record, handling global sales tax, VAT, and direct bank payouts to Pakistani founders.
  - Commercial pricing structure: **Single Paid Plan ($49/mo Team)** + **Free Open-Source Community Tier ($0/mo)**.
  - Pro tier ($149/mo), custom PDF branding, and SAML SSO deferred to v1.1.
- **DEC-023 (ADR-012)**: **Direct-to-R2 Presigned Upload Architecture**:
  - Bypasses Vercel 4.5 MB serverless function payload limit.
  - Browser requests presigned S3/R2 direct `PUT` URL from `/api/uploads/presign` after validating storage quota.
  - Automated cron job cleans up orphaned unconfirmed uploads.
- **DEC-024 (ADR-013)**: **Cryptographic Primitives Pinning & Hash-Chained Audit Ledger**:
  - Standardizes on RFC 9580 Version 6 Ed25519 / X25519 Curve25519 keys with 64-character SHA-256 fingerprints; drops legacy RSA-4096 and v4 keys to eliminate in-browser keygen freezes and target sub-50ms bare keygen.
  - Uses OpenPGP native Argon2id S2K (`t=3, m=65536, p=4`) for browser key storage protection.
  - Audit log table includes a SHA-256 `prev_hash` column forming a tamper-evident hash chain.
- **DEC-025 (ADR-014)**: **Versioned JSON Guest Recovery Package & Durable Guest Identity**:
  - Standardizes guest recovery exclusively on a single versioned `.bbt-recovery.json` bundle protected with client-side Argon2id S2K; defers 24-word mnemonic seeds to eliminate server-side lookup or seed-derivation coupling.
  - Tracking URL contains only `#token=<access_token>` in hash fragment; address bar is immediately scrubbed via `window.history.replaceState`.
  - Establishes a durable, report-scoped `guest_actor_id` (UUIDv4) decoupled from mutable bearer token hashes.
  - Enforces strict program-level authorization boundaries and atomic membership updates via `PROGRAM_DEFENDER`.

---

## 2. Proposed Decisions (`[PROPOSED]`)
*(None currently pending review.)*

---

## 3. Assumptions (`[ASSUMPTION]`)
- **ASM-001**: Academic evaluators value clear software engineering discipline, verifiable controls, and documented limitations over inflated commercial claims or unverified security absolutes.
- **ASM-002**: Development and evaluation will run in a local Dockerized Linux environment before any staging deployment.
- **ASM-003**: OpenPGP multi-recipient encryption functions reliably in client browser JavaScript via `openpgp.js` with Curve25519.
- **ASM-004**: Single $49/mo Team plan provides an accessible, credible entry point for early commercial customer validation.

---

## 4. Open Questions (`[OPEN QUESTION]`)
*(All initial scoping questions resolved for the 2–3 page HOD proposal and commercial launch baseline.)*

---

## 5. Deferred Decisions (`[DEFERRED]`)
- **DEF-001**: Direct Stripe Connect / US entity incorporation (replaced by DEC-022 Lemon Squeezy MoR).
- **DEF-002**: Automated sandbox reproduction and dynamic exploit scanning.
- **DEF-003**: Full two-way external bug tracker synchronization (Jira/Linear full bi-directional sync beyond webhook alerts).
- **DEF-004**: Gamification features: Researcher reputation points, levels, and badges.
- **DEF-005**: *[SUPERSEDED by DEC-020 / ADR-009]*: Account-less guest vulnerability reporting is now an active core feature.
- **DEF-006**: *[SUPERSEDED by DEC-018 / ADR-007]*: Private programs now included in Commercial Launch extension.
- **DEF-007**: Multi-member centralized key escrow / automated historical key recovery backdoors (rejected; replaced by DEC-019 client-side session key re-wrapping and DEC-021 offline recovery key).
- **DEF-008**: Enterprise Pro Tier features ($149/mo: custom PDF branding, executive summaries, GitHub App bot, SAML SSO) deferred to Version 1.1.
