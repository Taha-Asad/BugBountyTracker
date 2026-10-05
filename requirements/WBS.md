# WORK BREAKDOWN STRUCTURE (WBS) & GOVERNANCE BASELINE
## Project BugBountyTrack — Final Year Project (FYP) Engineering Charter & Commercial Launch Plan
**Document Release State**: Commercial Baseline & Academic Evaluation Specification (Version 3.0.0)  
**Standard Compliance**: IEEE Std 830-1998 / ISO/IEC/IEEE 29148:2018  

---

## Sheet 1: Executive Overview

| Project Parameter | Engineering Specification |
| :--- | :--- |
| **Project Identifier** | `PTUT - PRJ - 089` |
| **Project Title** | BugBountyTrack: Private Bug Bounty & Vulnerability Disclosure Platform |
| **Academic Sub-Field** | 9. Cybersecurity, Privacy & LegalTech |
| **Single Accountable Author**| Taha Asadullah (Roll No: **`24-ST-013`**) |
| **Academic Institution** | Punjab Tianjin University of Technology (PTUT), Lahore |
| **Department** | Department of Software Engineering Technology |
| **Session / Batch / Section**| Session 2024–2028 / Batch 24-SET-Fall / Section SET-A |
| **Official Student Email** | `24-st-013@students.ptut.edu.pk` |
| **Project Supervisor** | Sir Umar Hayat |
| **Client Platform** | Modern Web (Next.js 14+ App Router, React 18+, TypeScript 5.x, Tailwind CSS, OpenPGP.js) |
| **Backend & API Gateway** | Unified Next.js Serverless Routes on Node.js 22 LTS (Vercel) |
| **Persistence Tier** | PostgreSQL 16 on Neon Serverless Cloud via Prisma ORM 5.x (Row-Level Security & Append-Only Audit) |
| **Planned Workload** | 264 Total Academic Hours (236h Core Engineering + 28h Explicit Contingency Buffer / 12 Weeks = 22.0 h/wk) |
| **Release State** | Commercial Baseline & Academic Evaluation Specification (Version 3.0.0) |

---

## Sheet 2: Module-Wise Work Breakdown Structure (WBS)

### Part A: Core Academic Prototype & Defense Baseline (Weeks 1–12)

| WBS Code | Req ID | Module / Area | Work Package Name | Deliverable Scope & Acceptance Criteria | Start–End Week | Est. Hours | Human Owner | Predecessor | Status |
| :--- | :---: | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **WP-1.1** | FR-1.1 | MOD-1: Foundation & Security | Monorepo Scaffolding & CI Pipeline | Next.js 14+ monorepo, ESLint, Prettier, and GitHub Actions CI workflow | W1–W2 | 8 | Taha Asadullah | — | `[DONE]` |
| **WP-1.2** | FR-8.2 | MOD-1: Foundation & Security | PostgreSQL Schema & Row-Level Security | Prisma relational schema, PostgreSQL RLS tenant context, and append-only audit grants | W1–W2 | 12 | Taha Asadullah | WP-1.1 | `[DONE]` |
| **WP-1.3** | FR-8.1 | MOD-1: Foundation & Security | Early Markdown AST Sanitization Engine | `rehype-sanitize` pipeline neutralizing OWASP XSS cheat sheet attack vectors | W1–W2 | 10 | Taha Asadullah | WP-1.1 | `[DONE]` |
| **WP-1.4** | NFR-04 | MOD-1: Foundation & Security | Design Tokens & Accessible UI Base | Tailwind CSS tokens meeting WCAG 2.2 AA (24 × 24 px touch targets) | W1–W2 | 10 | Taha Asadullah | WP-1.1 | `[DONE]` |
| **WP-2.1** | FR-1.3 | MOD-2: Identity & Multi-Tenancy | Tenant Registration Wizard & Profiles | Organization creation, slug reservation, and public program profile | W3–W4 | 8 | Taha Asadullah | WP-1.4 | `[READY]` |
| **WP-2.2** | FR-1.3 | MOD-2: Identity & Multi-Tenancy | Email / Password Auth & JWT Sessions | Bcrypt password hashing (rounds = 12) and signed HTTP-only JWT cookies | W3–W4 | 11 | Taha Asadullah | WP-2.1 | `[PLANNED]` |
| **WP-2.3** | FR-1.2 | MOD-2: Identity & Multi-Tenancy | Server-Enforced RBAC Middleware | Access control enforcing Owner, Defender, Hunter, and ReadOnly roles | W3–W4 | 11 | Taha Asadullah | WP-2.2 | `[PLANNED]` |
| **WP-2.4** | FR-8.3 | MOD-2: Identity & Multi-Tenancy | Token-Bucket Rate Limiter & Pool RLS | Token-bucket rate limiting (5 req/hr/IP) on intake + dynamic tenant RLS | W3–W4 | 10 | Taha Asadullah | WP-1.2 | `[PLANNED]` |
| **WP-3.1** | FR-2.1 | MOD-3: Policy & Cryptography Base | RFC 9116 security.txt Endpoint & Download | Compliant RFC 9116 text policy preview and download route per tenant | W5–W6 | 8 | Taha Asadullah | WP-2.1 | `[PLANNED]` |
| **WP-3.2** | FR-2.2 | MOD-3: Policy & Cryptography Base | In-Browser Cleartext PGP Signing UI | Browser workflow signing security.txt inline using private signing key | W5–W6 | 11 | Taha Asadullah | WP-3.1 | `[PLANNED]` |
| **WP-3.3** | FR-2.5 | MOD-3: Policy & Cryptography Base | DNS TXT Challenge Ownership Verifier | Node.js DNS challenge record lookup verifying domain ownership | W5–W6 | 11 | Taha Asadullah | WP-3.1 | `[PLANNED]` |
| **WP-3.4** | FR-3.1 | MOD-3: Policy & Cryptography Base | WebCrypto Keypair Generator & KeyStore | Ed25519 signing + X25519/RSA encryption subkeys in encrypted IndexedDB | W5–W6 | 10 | Taha Asadullah | WP-2.2 | `[PLANNED]` |
| **WP-4.1** | FR-3.3 | MOD-4: Cryptographic Intake & CVSS | Dual-Recipient OpenPGP Payload Encrypt | In-browser payload encryption targeting Org encryption subkey + Hunter key with neutral operational labels | W7–W8 | 11 | Taha Asadullah | WP-3.4 | `[PLANNED]` |
| **WP-4.2** | FR-3.4 | MOD-4: Cryptographic Intake & CVSS | Encrypted Attachment Upload (Cloudflare R2)| Client-side encrypted streaming binary uploads (≤ 25 MB) to R2 | W7–W8 | 7 | Taha Asadullah | WP-4.1 | `[PLANNED]` |
| **WP-4.3** | FR-4.1 | MOD-4: Cryptographic Intake & CVSS | Pure TypeScript CVSS 3.1 & 52-Vector Test | 8 Base metric scoring engine asserting 100% parity across FIRST.org suite in CVSS_TEST_FIXTURES.md | W7–W8 | 11 | Taha Asadullah | WP-1.1 | `[PLANNED]` |
| **WP-4.4** | FR-5.1 | MOD-4: Cryptographic Intake & CVSS | In-Browser Decrypt & Basic Triage State | Passphrase key unlocking, decrypted triage view, and basic state transitions (NEW->TRIAGING->ACCEPTED); Week 7 Live Working Prototype | W7–W8 | 11 | Taha Asadullah | WP-4.1 | `[PLANNED]` |
| **WP-5.1** | FR-5.2 | MOD-5: Triage & Commit Verification | Dual-Lane Threading Interface | Confidential conversation thread and private reviewer-only internal notes | W9–W10 | 10 | Taha Asadullah | WP-4.4 | `[PLANNED]` |
| **WP-5.2** | FR-5.3 | MOD-5: Triage & Commit Verification | Metadata Notifications & Duplicate Link | Resend email dispatching metadata only; reviewer-driven duplicate linking | W9–W10 | 9 | Taha Asadullah | WP-5.1 | `[PLANNED]` |
| **WP-5.3** | FR-6.2 | MOD-5: Triage & Commit Verification | GitHub REST API Commit SHA & Author Check | GitHub API v3 lookup validating commit existence, author, and branch for public and private repos | W9–W10 | 10 | Taha Asadullah | WP-5.1 | `[PLANNED]` |
| **WP-5.4** | FR-6.3 | MOD-5: Triage & Commit Verification | Infrastructure Config SHA-256 Hash Binder | Non-code remediation hash generator and deployment environment recording | W9–W10 | 9 | Taha Asadullah | WP-5.3 | `[PLANNED]` |
| **WP-6.1** | FR-7.2 | MOD-6: Attested Retest & Defense | Attested Retest State Machine & Closure | Attested retest state machine (3 distinct fan-out terminal states), failed retest loopback to ACCEPTED, and ticket reopening | W11–W12 | 10 | Taha Asadullah | WP-5.3 | `[PLANNED]` |
| **WP-6.2** | FR-8.4 | MOD-6: Attested Retest & Defense | Storage Quota Monitor & Enforcer | Quota enforcement (50 MB DB per tenant / 512 MB Neon, 2 GB R2 per tenant / 10 GB free tier; 90% warning, 100% rejection) | W11–W12 | 6 | Taha Asadullah | WP-1.2 | `[PLANNED]` |
| **ACAD-01**| EV-01 | ACAD: Evaluation & Usability | Controlled Peer Usability Study | Controlled evaluation with 3–5 peers across OWASP Juice Shop targets | W11–W12 | 8 | Taha Asadullah | WP-6.1 | `[PLANNED]` |
| **ACAD-02**| EV-02 | ACAD: Evaluation & Usability | Final Project Report & Live Demo Defense | Comprehensive academic report, presentation slides, and defense demo | W11–W12 | 14 | Taha Asadullah | ACAD-01 | `[PLANNED]` |
| **WP-BUF** | GOV-01 | GOV: Contingency & Buffer | Project Buffer & Defense Contingency | Distributed buffer for unexpected debugging, security fixes & defense trials | W1–W12 | 28 | Taha Asadullah | WP-1.1 | `[PLANNED]` |

**CORE PLANNED ENGINEERING EFFORT**: **236 Hours**  
**CONTINGENCY & REHEARSAL BUFFER**: **28 Hours**  
**TOTAL ACADEMIC WORKLOAD**: **264 Hours** (Consistent 22.0 Hours / Week across 12 Academic Weeks)

---

### Part B: Commercial Launch & Operational Extension (Weeks 13–18 Proposed)

| WBS Code | Req ID | Module / Area | Work Package Name | Deliverable Scope & Concrete Acceptance Criteria | Start–End Week | Est. Hours | Human Owner | Predecessor | Status |
| :--- | :---: | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **WP-7.1** | FR-1.3 | MOD-7: Commercial Launch | Auth Hardening & Session Revocation | TOTP MFA enrollment, password reset with immediate session revocation (JWT jti blacklisting), and MFA recovery codes | W13–W14 | 10 | Taha Asadullah | WP-2.2 | `[ROADMAP]` |
| **WP-7.2** | FR-1.4 | MOD-7: Commercial Launch | Guided Onboarding & Domain Verification | Step-by-step wizard: DNS TXT verification, PGP key generation, RFC 9116 download, and public program activation | W13–W14 | 10 | Taha Asadullah | WP-3.2 | `[ROADMAP]` |
| **WP-7.3** | FR-1.5 | MOD-7: Commercial Launch | Private Program Access & Invite Lifecycle | Cryptographic invitation tokens (`token_hash` SHA-256 storage, 72h expiry, one-time redemption, uninvited email rejection) | W13–W14 | 8 | Taha Asadullah | WP-2.1 | `[ROADMAP]` |
| **WP-7.4** | FR-3.6 | MOD-7: Commercial Launch | Multi-Defender Keying & Session Re-Wrapping | Local key export UI, program keyring versioning (`recipient_set_version`), and audited historical session-key re-wrapping | W15–W16 | 10 | Taha Asadullah | WP-3.4 | `[ROADMAP]` |
| **WP-7.5** | FR-5.4 | MOD-7: Commercial Launch | Notification Outbox Worker & Deduplication | Outbox table pattern, exponential backoff retries, idempotency keys (no duplicate alerts), and minimal-metadata email templates | W15–W16 | 10 | Taha Asadullah | WP-5.2 | `[ROADMAP]` |
| **WP-7.6** | FR-7.5 | MOD-7: Commercial Launch | Redacted Evidence Export Engine | Browser-side PDF/JSON export after local decryption. Excludes free-text exploit details by default; includes full preview before download | W15–W16 | 10 | Taha Asadullah | WP-6.1 | `[ROADMAP]` |
| **WP-7.7** | FR-8.4 | MOD-7: Commercial Launch | Production Cloud & Stripe Subscriptions | Stripe Checkout, Customer Portal, webhook idempotency, failed payment grace periods, cancellation downgrade, and seat entitlement checks | W17–W18 | 14 | Taha Asadullah | WP-1.1 | `[ROADMAP]` |
| **WP-7.8** | FR-8.5 | MOD-7: Commercial Launch | Disaster Recovery & Incident Runbooks | Automated daily PostgreSQL + R2 backup restore drill in sandbox, customer hard-deletion workflow, and incident response runbook | W17–W18 | 6 | Taha Asadullah | WP-1.2 | `[ROADMAP]` |
| **WP-7.9** | GOV-02 | GOV: Contingency & Buffer | Commercial Launch Contingency Buffer | Buffer for unexpected billing edge cases, webhook debugging, and production pilot support | W13–W18 | 10 | Taha Asadullah | WP-7.1 | `[ROADMAP]` |

**COMMERCIAL EXTENSION WORKLOAD**: **88 Hours** (Planned Engineering: 78h + Commercial Contingency: 10h)  
**TOTAL DOCUMENTED PROJECT WORKLOAD**: **352 Hours** (Academic Baseline: 264h + Commercial Extension: 88h)


---

## Sheet 3: RACI Governance Matrix

* **R (Responsible)**: Taha Asadullah (Carries out engineering implementation).
* **A (Accountable)**: Taha Asadullah (Single human individual with ultimate delivery accountability).
* **C (Consulted)**: Sir Umar Hayat (Academic Supervisor providing guidance and defense evaluation).
* **I (Informed)**: Department Faculty Panel (Academic stakeholders updated at milestone boundaries).

| Module Code | Module Name | Human Accountable (Taha) | Supervisor (Sir Umar) | Faculty Panel (PTUT) | Internal AI Advisory Squad (Crow Parliament) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **MOD-1** | Foundation, RLS & Markdown Sanitization | **A / R** | C | I | Advised by Arthur (Arch) & Cyra (Sec) |
| **MOD-2** | Multi-Tenancy, Auth & Server RBAC | **A / R** | C | I | Advised by Marcus (Forge) & Cyra (Sec) |
| **MOD-3** | RFC 9116 Policy & Browser Keygen | **A / R** | C | I | Advised by Victoria (Req) & Cyra (Sec) |
| **MOD-4** | Client Cryptography & CVSS 3.1 | **A / R** | C | I | Advised by Cyra (Sec) & Elena (QA) |
| **MOD-5** | Confidential Triage & GitHub Validation | **A / R** | C | I | Advised by Marcus (Forge) & Julian (UX) |
| **MOD-6** | Attested Retest, Peer Study & Defense | **A / R** | C | I | Advised by Elena (QA) & Alexander (PM) |

---

## Sheet 4: Sprint Milestones & Delivery Trajectory

### Phase 1: Academic Trajectory (Weeks 1–12) — 264 Hours

| Sprint ID | Academic Weeks | Target Work Packages | Key Engineering Deliverables | Prerequisite Gates & Evaluation | Planned Hours | Status |
| :--- | :---: | :--- | :--- | :--- | :---: | :---: |
| **Sprint 1** | Weeks 1–2 | WP-1.1, WP-1.2, WP-1.3, WP-1.4, Buffer (4h) | Monorepo scaffolding, PostgreSQL RLS schema, AST Markdown sanitization, design tokens, BRD, SRS, WBS | Phase Gate 1 (DoR) Certified | 44 | `[DONE]` |
| **Sprint 2** | Weeks 3–4 | WP-2.1, WP-2.2, WP-2.3, WP-2.4, Buffer (4h) | Tenant registration wizard, bcrypt auth, JWT cookies, server RBAC, token-bucket rate limiter | Phase Gate 2 (DoAC) Architecture | 44 | `[READY]` |
| **Sprint 3** | Weeks 5–6 | WP-3.1, WP-3.2, WP-3.3, WP-3.4, Buffer (4h) | Dynamic security.txt download API, browser cleartext PGP signing, DNS TXT check, WebCrypto keypairs | Phase Gate 3 (DoCC) Core Crypto | 44 | `[PLANNED]` |
| **Sprint 4** | Weeks 7–8 | WP-4.1, WP-4.2, WP-4.3, WP-4.4, Buffer (4h) | Multi-recipient payload encryption, R2 attachment upload, CVSS 3.1 engine, in-browser decryption, basic triage | **Week 7 Live Working Prototype Milestone** | 44 | `[PLANNED]` |
| **Sprint 5** | Weeks 9–10 | WP-5.1, WP-5.2, WP-5.3, WP-5.4, Buffer (6h) | Dual-lane triage threads, Resend metadata alerts, duplicate linking, GitHub REST API commit validation | Phase Gate 4 (DoQV) Triage & VCS | 44 | `[PLANNED]` |
| **Sprint 6** | Weeks 11–12| WP-6.1, WP-6.2, ACAD-01, ACAD-02, Buffer (6h)| Attested retest engine, storage quotas, peer study (3–5 peers), Final FYP Report & Defense | **Final FYP Defense & Demonstration** | 44 | `[PLANNED]` |

### Phase 2: Commercial Launch Trajectory (Weeks 13–18 Proposed) — 88 Hours

| Sprint ID | Calendar Weeks | Target Work Packages | Key Commercial Deliverables | Target Milestone & Gate | Planned Hours | Status |
| :--- | :---: | :--- | :--- | :--- | :---: | :---: |
| **Sprint 7** | Weeks 13–15 | WP-7.1, WP-7.2, WP-7.3, WP-7.4, Buffer (4h) | TOTP MFA, session revocation, guided onboarding wizard, tokenized private programs, multi-defender key management | **Milestone 3: Controlled Commercial Pilot** | 42 | `[ROADMAP]` |
| **Sprint 8** | Weeks 16–18 | WP-7.5, WP-7.6, WP-7.7, WP-7.8, Buffer (6h) | Notification outbox worker, redacted evidence export engine, Stripe subscription lifecycle, DR sandbox restore | **Milestone 4: Commercial Launch Gate (DoRG)** | 46 | `[ROADMAP]` |

---

## Sheet 5: Financial Sizing & Unit Economics

### Part A: Zero-Cost Academic Demonstration Budget ($0.00)

| Infrastructure Layer | Platform Provider | Provisioned Cloud Tier | Resource Allocations & Quotas | Monthly Cost ($USD) |
| :--- | :--- | :--- | :--- | :---: |
| **Client Web & API Gateway** | Vercel Cloud | Hobby / Free Tier | Serverless Functions, Edge CDN, Global SSL | **$0.00** |
| **Relational Database** | Neon Serverless Cloud | Free Tier | PostgreSQL 16 (512 MB Storage, Shared Compute, Dynamic RLS) | **$0.00** |
| **Encrypted Object Storage** | Cloudflare R2 | Free Tier | 10 GB Storage, Zero Egress Fees | **$0.00** |
| **Transactional Email** | Resend API | Free Developer Tier | 100 Emails / Day, 3,000 Emails / Month | **$0.00** |
| **Source Code & CI/CD** | GitHub Free Tier | Public Repository | 2,000 Action Minutes / Month, REST API v3 Integration | **$0.00** |
| **DNS Resolution** | System DNS Resolver | Free Native | Node.js `dns.promises` Resolver for Domain Validation | **$0.00** |
| **Domain & SSL** | Local / Vercel Subdomain | Free Tier | `.vercel.app` Free Subdomain with Automatic TLS Certificate | **$0.00** |
| **TOTAL DEMO BUDGET** | — | — | **100% Free Developer Tier Architecture** | **$0.00** |

### Part B: Production Cloud Sizing & Unit Economics (Proposed Validation Baseline)

| Service Layer | Provider & Tier | Allocation & Entitlement | Monthly Base Cost ($USD) | Variable Sizing & Scaling Notes |
| :--- | :--- | :--- | :---: | :--- |
| **Production Web Hosting** | Vercel Pro | Custom domain, isolated team compute | **$20.00** | Scales at $20/seat for platform developers |
| **Production Database** | Neon Serverless Launch | 10 GB Storage, automated daily backups | **$19.00** | $0.16/GB-mo for storage beyond 10 GB |
| **Encrypted Storage (R2)** | Cloudflare R2 Standard | 50 GB pooled storage baseline | **$0.75** | $0.015/GB-mo, zero egress bandwidth fees |
| **Transactional Email** | Resend Pro | 50,000 emails/mo, dedicated domain | **$20.00** | Minimal-metadata notification delivery |
| **Custom Domain & DNS** | Cloudflare Registrar | `.com` / `.security` TLD | **$1.25** | Amortized annual registrar fee ($15.00/yr) |
| **Payment Gateway** | Stripe Connect / Billing | Automated subscription invoicing | **Variable** | 2.9% + $0.30 per successful transaction |
| **TOTAL FIXED INFRASTRUCTURE** | — | **Baseline for ~10–25 Active Tenants** | **$61.00 / month** | Covered by 2 active Starter subscriptions |

### Unit Economics Hypothesis:
* **Starter Plan ($49/month)**: Gross $49.00 - $1.72 (Stripe fee) = **$47.28 net revenue**.
* **Team Plan ($149/month)**: Gross $149.00 - $4.62 (Stripe fee) = **$144.38 net revenue**.
* Two Starter subscriptions ($94.56 net) or one Team subscription ($144.38 net) comfortably exceed the $61.00/month baseline cloud infrastructure commitment. All pricing figures represent proposed hypotheses subject to validation during commercial pilot testing.

---

*--- End of Work Breakdown Structure (WBS) ---*
