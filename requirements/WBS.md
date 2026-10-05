# WORK BREAKDOWN STRUCTURE (WBS) & GOVERNANCE BASELINE
## Project BugBountyTrack — Final Year Project (FYP) Engineering Charter & Commercial Launch Plan
**Document Release State**: Commercial Baseline & Academic Evaluation Specification (Version 3.2.0)  
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
| **Planned Workload** | **424 Total Hours** (264h Academic Baseline across 12 Weeks + 160h Commercial Launch across 6 Weeks) |
| **Release State** | Commercial Baseline & Academic Evaluation Specification (Version 3.2.0) |

---

## Sheet 2: Module-Wise Work Breakdown Structure (WBS)

### Part A: Core Academic Prototype & Defense Baseline (Weeks 1–12)

| WBS Code | Req ID | Module / Area | Work Package Name | Deliverable Scope & Acceptance Criteria | Start–End Week | Est. Hours | Human Owner | Predecessor | Status |
| :--- | :---: | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **WP-1.1** | FR-1.1 | MOD-1: Foundation & Security | Monorepo Scaffolding & CI Pipeline | Next.js 14+ monorepo, ESLint, Prettier, and GitHub Actions CI workflow | W1–W2 | 8 | Taha Asadullah | — | `[DONE]` |
| **WP-1.2** | FR-8.2 | MOD-1: Foundation & Security | PostgreSQL Schema, Neon RLS & Hash-Chained Audit | Prisma relational schema, PostgreSQL RLS tenant context, and append-only audit ledger with SHA-256 prev_hash | W1–W2 | 12 | Taha Asadullah | WP-1.1 | `[DONE]` |
| **WP-1.3** | FR-8.1 | MOD-1: Foundation & Security | Early Markdown AST Sanitization Engine | `rehype-sanitize` pipeline neutralizing OWASP XSS cheat sheet attack vectors | W1–W2 | 10 | Taha Asadullah | WP-1.1 | `[DONE]` |
| **WP-1.4** | NFR-04 | MOD-1: Foundation & Security | Design Tokens & Accessible UI Base | Tailwind CSS tokens meeting WCAG 2.2 AA (24 × 24 px touch targets) | W1–W2 | 10 | Taha Asadullah | WP-1.1 | `[DONE]` |
| **WP-2.1** | FR-1.3 | MOD-2: Identity & Multi-Tenancy | Tenant Registration Wizard & Profiles | Organization creation, slug reservation, and public program profile | W3–W4 | 8 | Taha Asadullah | WP-1.4 | `[READY]` |
| **WP-2.2** | FR-1.3 | MOD-2: Identity & Multi-Tenancy | Email / Password Auth & Database-Backed Sessions | Bcrypt/Argon2 password hashing, database-persisted session tokens, and secure HTTP-only cookies | W3–W4 | 11 | Taha Asadullah | WP-2.1 | `[PLANNED]` |
| **WP-2.3** | FR-1.2 | MOD-2: Identity & Multi-Tenancy | Server-Enforced RBAC Middleware | Access control enforcing Owner, Defender, Hunter, and ReadOnly roles | W3–W4 | 11 | Taha Asadullah | WP-2.2 | `[PLANNED]` |
| **WP-2.4** | FR-8.3 | MOD-2: Identity & Multi-Tenancy | Shared Store Rate Limiter & Turnstile CAPTCHA | Shared store rate limiting (Postgres/Upstash) and Turnstile CAPTCHA (5 req/hr/IP) | W3–W4 | 10 | Taha Asadullah | WP-1.2 | `[PLANNED]` |
| **WP-3.1** | FR-2.1 | MOD-3: Policy & Cryptography Base | RFC 9116 security.txt Endpoint & Download | Compliant RFC 9116 text policy preview and download route per tenant | W5–W6 | 8 | Taha Asadullah | WP-2.1 | `[PLANNED]` |
| **WP-3.2** | FR-2.2 | MOD-3: Policy & Cryptography Base | In-Browser Cleartext PGP Signing UI | Browser workflow signing security.txt inline using private signing key | W5–W6 | 11 | Taha Asadullah | WP-3.1 | `[PLANNED]` |
| **WP-3.3** | FR-2.5 | MOD-3: Policy & Cryptography Base | DNS TXT Challenge Ownership Verifier | Node.js DNS challenge record lookup verifying domain ownership | W5–W6 | 11 | Taha Asadullah | WP-3.1 | `[PLANNED]` |
| **WP-3.4** | FR-3.1 | MOD-3: Policy & Cryptography Base | WebCrypto Keypair Generator & Argon2 S2K KeyStore | Ed25519 signing + X25519 encryption keys stored in IndexedDB protected by OpenPGP Argon2 S2K | W5–W6 | 10 | Taha Asadullah | WP-2.2 | `[PLANNED]` |
| **WP-4.1** | FR-3.3 | MOD-4: Cryptographic Intake & CVSS | Multi-Recipient OpenPGP Payload Encrypt | In-browser payload encryption targeting Org defenders + Hunter key with neutral operational labels | W7–W8 | 11 | Taha Asadullah | WP-3.4 | `[PLANNED]` |
| **WP-4.2** | FR-3.5 | MOD-4: Cryptographic Intake & CVSS | Direct-to-R2 Presigned Attachment Upload | Client-side encrypted streaming binary uploads (≤ 25 MB) directly to Cloudflare R2 via presigned URLs | W7–W8 | 7 | Taha Asadullah | WP-4.1 | `[PLANNED]` |
| **WP-4.3** | FR-4.1 | MOD-4: Cryptographic Intake & CVSS | Pure TypeScript CVSS 3.1 & 45-Vector Test | 8 Base metric scoring engine asserting 100% parity across FIRST.org suite in CVSS_TEST_FIXTURES.md | W7–W8 | 11 | Taha Asadullah | WP-1.1 | `[PLANNED]` |
| **WP-4.4** | FR-5.1 | MOD-4: Cryptographic Intake & CVSS | In-Browser Decrypt & Basic Triage State | Passphrase key unlocking, decrypted triage view, and basic state transitions (NEW->TRIAGING->ACCEPTED); Week 7 Live Working Prototype | W7–W8 | 11 | Taha Asadullah | WP-4.1 | `[PLANNED]` |
| **WP-5.1** | FR-5.2 | MOD-5: Triage & Commit Verification | Dual-Lane Threading Interface | Confidential conversation thread and private reviewer-only internal notes | W9–W10 | 10 | Taha Asadullah | WP-4.4 | `[PLANNED]` |
| **WP-5.2** | FR-5.3 | MOD-5: Triage & Commit Verification | Metadata Notifications & Duplicate Link | Resend email dispatching metadata only; reviewer-driven duplicate linking | W9–W10 | 9 | Taha Asadullah | WP-5.1 | `[PLANNED]` |
| **WP-5.3** | FR-6.2 | MOD-5: Triage & Commit Verification | GitHub REST API Commit SHA & Branch Check | GitHub API v3 lookup validating commit existence and branch compare inclusion across public/private repos | W9–W10 | 10 | Taha Asadullah | WP-5.1 | `[PLANNED]` |
| **WP-5.4** | FR-6.3 | MOD-5: Triage & Commit Verification | Infrastructure Config SHA-256 Hash Binder | Non-code remediation hash generator and deployment environment recording | W9–W10 | 9 | Taha Asadullah | WP-5.3 | `[PLANNED]` |
| **WP-6.1** | FR-7.2 | MOD-6: Attested Retest & Defense | Attested Retest State Machine & Closure | Attested retest state machine (3 distinct fan-out terminal states), failed retest loopback to ACCEPTED, and ticket reopening | W11–W12 | 10 | Taha Asadullah | WP-5.3 | `[PLANNED]` |
| **WP-6.2** | FR-8.4 | MOD-6: Attested Retest & Defense | Storage Quota Monitor & Enforcer | Quota enforcement (50 MB DB per tenant / 512 MB Neon, 2 GB R2 per tenant / 10 GB free tier; 90% warning, 100% rejection) | W11–W12 | 6 | Taha Asadullah | WP-1.2 | `[PLANNED]` |
| **ACAD-01**| EV-01 | ACAD: Evaluation & Usability | Controlled Peer Usability Study | Controlled evaluation with 3–5 peers across OWASP Juice Shop targets | W11–W12 | 8 | Taha Asadullah | WP-6.1 | `[PLANNED]` |
| **ACAD-02**| EV-02 | ACAD: Evaluation & Usability | Final Project Report & Live Demo Defense | Comprehensive academic report, presentation slides, and defense demo | W11–W12 | 14 | Taha Asadullah | ACAD-01 | `[PLANNED]` |
| **WP-BUF-1**| GOV-01 | GOV: Contingency & Buffer | Project Buffer & Defense Contingency | Distributed buffer for unexpected debugging, security fixes & defense trials | W1–W12 | 28 | Taha Asadullah | WP-1.1 | `[PLANNED]` |

**CORE PLANNED ENGINEERING EFFORT**: **236 Hours**  
**CONTINGENCY & REHEARSAL BUFFER**: **28 Hours**  
**TOTAL ACADEMIC WORKLOAD**: **264 Hours** (Consistent 22.0 Hours / Week across 12 Academic Weeks)

---

### Part B: Commercial Launch & Deployment Extension (Weeks 13–18)

| WBS Code | Req ID | Module / Area | Work Package Name | Deliverable Scope & Concrete Acceptance Criteria | Start–End Week | Est. Hours | Human Owner | Predecessor | Status |
| :--- | :---: | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **WP-7.1** | FR-1.3 | MOD-7: Commercial Launch | Auth Hardening, TOTP MFA & Password Reset | TOTP MFA enrollment, password reset with immediate session revocation, encrypted totp_secret at rest | W13–W14 | 14 | Taha Asadullah | WP-2.2 | `[ROADMAP]` |
| **WP-7.2** | FR-1.4 | MOD-7: Commercial Launch | Guided Onboarding & Offline Org Recovery Key | Step-by-step wizard: DNS verification, Offline Master Recovery Key generation, mandatory backup test challenge | W13–W14 | 12 | Taha Asadullah | WP-3.2 | `[ROADMAP]` |
| **WP-7.3** | FR-1.6 | MOD-7: Commercial Launch | Account-Less Guest Submission & Tracking URLs | Ephemeral Curve25519 key generation in browser, secret tracking URL issuance (`/report/track/BBT-RPT-XXXX`), anonymous retests | W13–W14 | 10 | Taha Asadullah | WP-4.1 | `[ROADMAP]` |
| **WP-7.4** | FR-8.4 | MOD-7: Commercial Launch | Direct-to-R2 Presigned Upload & Orphan Cleanup | Presigned S3/R2 direct upload route (`/api/uploads/presign`), upload quota verification at issuance, and automated orphan cleanup | W13–W14 | 10 | Taha Asadullah | WP-4.2 | `[ROADMAP]` |
| **WP-7.5** | FR-5.4 | MOD-7: Commercial Launch | SLA Countdown Engine & Slack Webhooks | Hourly scheduled SLA cron check, notification outbox worker, visual countdown alerts, and Slack-compatible webhook payloads | W15–W16 | 12 | Taha Asadullah | WP-5.2 | `[ROADMAP]` |
| **WP-7.6** | FR-7.7 | MOD-7: Commercial Launch | Redacted Evidence Export Engine (PDF & JSON) | Sanitized PDF and JSON closure summary generation documenting timeline, commit SHA/branch, deployment env, and retest attestations | W15–W16 | 10 | Taha Asadullah | WP-6.1 | `[ROADMAP]` |
| **WP-7.7** | FR-8.6 | MOD-7: Commercial Launch | Merchant of Record (Lemon Squeezy) Billing | Lemon Squeezy checkout integration ($49/mo Team & Free Tier), webhook handler, subscription downgrade, direct bank payouts to Pakistan | W15–W16 | 14 | Taha Asadullah | WP-2.1 | `[ROADMAP]` |
| **WP-7.8** | FR-2.1 | MOD-7: Commercial Launch | Landing Page, Public Docs & Legal Pack | Marketing landing page, public documentation, free RFC 9116 generator tool, Terms of Service, Privacy Policy, DPA, and subprocessor list | W15–W16 | 18 | Taha Asadullah | WP-3.1 | `[ROADMAP]` |
| **WP-7.9** | FR-8.1 | MOD-7: Commercial Launch | Application Security Hardening & Pen-Test Pass | Strict CSP, Subresource Integrity (SRI), CSRF protection on cookies, login/MFA lockout, SSRF checks on GitHub URLs, and self pen-test | W17–W18 | 16 | Taha Asadullah | WP-1.3 | `[ROADMAP]` |
| **WP-7.10**| NFR-01 | MOD-7: Commercial Launch | Observability (Sentry), Environments & Uptime | Sentry error tracking, staging and production database migrations in CI, and external uptime monitoring (BetterStack/UptimeRobot) | W17–W18 | 12 | Taha Asadullah | WP-1.1 | `[ROADMAP]` |
| **WP-7.11**| FR-1.2 | MOD-7: Commercial Launch | SuperAdmin Abuse Management & Console | Administrative dashboard to inspect tenant counts, view platform error rates, handle abuse reports, and suspend abusive tenants | W13–W14 | 8 | Taha Asadullah | WP-2.3 | `[ROADMAP]` |
| **WP-7.12**| FR-8.7 | MOD-7: Commercial Launch | Disaster Recovery & GDPR Hard Deletion | Automated daily PostgreSQL + R2 backup restore drill in sandbox, customer hard-deletion workflow, and incident response runbook | W17–W18 | 8 | Taha Asadullah | WP-1.2 | `[ROADMAP]` |
| **WP-BUF-2**| GOV-02 | GOV: Contingency & Buffer | Commercial Pilot Support & Launch Buffer | Buffer for unexpected billing edge cases, webhook debugging, and production pilot customer support | W17–W18 | 16 | Taha Asadullah | WP-7.7 | `[ROADMAP]` |

**COMMERCIAL EXTENSION WORKLOAD**: **160 Hours** (Planned Engineering: 144h + Commercial Contingency: 16h)  
**TOTAL DOCUMENTED PROJECT WORKLOAD**: **424 Hours** (Academic Baseline: 264h + Commercial Extension: 160h across 38 Work Packages)

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
| **MOD-6** | Attested Retest & Quota Management | **A / R** | C | I | Advised by Elena (QA) & Garrison (SRE) |
| **MOD-7** | Commercial Deployment, Billing & Hardening | **A / R** | C | I | Advised by Garrison (SRE) & Nadia (Release) |
| **ACAD** | Usability Study & FYP Defense | **A / R** | C | I | Advised by Alexander (Steward) & Victoria (Req) |

---

## Sheet 4: Sprint Milestones & Delivery Schedule

| Sprint ID | Academic Weeks | Target Work Packages | Key Engineering Deliverables | Prerequisite Gates & Evaluation | Planned Hours | Status |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| **Sprint 1** | Weeks 1–2 | WP-1.1, WP-1.2, WP-1.3, WP-1.4 | Monorepo scaffolding, PostgreSQL RLS schema, AST sanitization, and UI tokens | Gate 0: Foundation Review | 40 | `[DONE]` |
| **Sprint 2** | Weeks 3–4 | WP-2.1, WP-2.2, WP-2.3, WP-2.4 | Tenant registration, DB-backed sessions, server RBAC, and shared store rate limiter | Gate 1: Identity & Multi-Tenancy | 40 | `[READY]` |
| **Sprint 3** | Weeks 5–6 | WP-3.1, WP-3.2, WP-3.3, WP-3.4 | RFC 9116 download, in-browser PGP cleartext signing, DNS TXT verifier, Ed25519 keypair generator | Gate 2: Policy & Keys | 40 | `[PLANNED]` |
| **Sprint 4** | Weeks 7–8 | WP-4.1, WP-4.2, WP-4.3, WP-4.4 | Dual-recipient encryption, direct R2 presigned upload, pure TS CVSS 3.1 engine, in-browser decryption | **Gate 3: Working Prototype Demonstration** | 40 | `[PLANNED]` |
| **Sprint 5** | Weeks 9–10 | WP-5.1, WP-5.2, WP-5.3, WP-5.4 | Dual-lane triage threads, metadata email alerts, GitHub commit & branch compare validation, config SHA binder | Gate 4: Remediation Evidence | 38 | `[PLANNED]` |
| **Sprint 6** | Weeks 11–12 | WP-6.1, WP-6.2, ACAD-01, ACAD-02, WP-BUF-1 | Attested retest state machine, storage quotas, Juice Shop usability study, final thesis & demo defense | **Gate 5: Academic FYP Defense Certified** | 66 | `[PLANNED]` |
| **Sprint 7** | Weeks 13–14 | WP-7.1, WP-7.2, WP-7.3, WP-7.4, WP-7.11 | TOTP MFA, offline recovery key onboarding, account-less guest intake, direct R2 upload hardening, SuperAdmin | Gate 6: Commercial Core Intake | 54 | `[ROADMAP]` |
| **Sprint 8** | Weeks 15–16 | WP-7.5, WP-7.6, WP-7.7, WP-7.8 | SLA countdown engine & Slack webhooks, redacted PDF export, Lemon Squeezy MoR billing, landing page & legal | Gate 7: Commercial Operations Ready | 54 | `[ROADMAP]` |
| **Sprint 9** | Weeks 17–18 | WP-7.9, WP-7.10, WP-7.12, WP-BUF-2 | Security hardening & pen-test pass, Sentry observability, disaster recovery sandbox drill, launch buffer | **Gate 8: Commercial Production Release** | 52 | `[ROADMAP]` |

**TOTAL PLANNED SPRINT HOURS**: **424 Hours** across 9 Sprints (Weeks 1–18)

---

## Sheet 5: Infrastructure Budget & Financial Viability

### Part A: Academic Demonstration Budget (Zero-Cost Baseline)

| Infrastructure Layer | Platform Provider | Provisioned Cloud Tier | Resource Allocations & Quotas | Monthly Cost ($USD) |
| :--- | :--- | :--- | :--- | :---: |
| **Application & API Gateway** | Vercel Cloud | Hobby Developer Tier | Edge CDN, serverless functions, global SSL certificate | 0.00 |
| **Relational Database** | Neon Serverless | PostgreSQL Free Tier | 512 MB storage, connection pooling via PgBouncer (50 MB / tenant demo) | 0.00 |
| **Encrypted File Storage** | Cloudflare R2 | Free Tier Object Storage | 10 GB storage allowance, zero egress bandwidth fees (2 GB / tenant demo) | 0.00 |
| **Transactional Email** | Resend API | Developer Free Tier | 3,000 minimal-metadata triage notifications / month | 0.00 |
| **CI/CD Build Automation** | GitHub Actions | Standard Runner Free Tier| 2,000 automated build & test minutes / month | 0.00 |

**TOTAL DEMO INFRASTRUCTURE COST**: **$0.00 / Month** (Demonstrates full FYP feasibility with zero external cash outlay)

### Part B: Commercial Production Cloud Budget (10–25 Tenants)

| Infrastructure Layer | Commercial Provider | Provisioned Commercial Tier | Purpose & Quota Bounds | Monthly Cost ($USD) |
| :--- | :--- | :--- | :--- | :---: |
| **Application & API Gateway** | Vercel Pro | Pro Team Tier ($20 / seat) | Commercial SLA, hourly SLA crons, zero cold starts | 20.00 |
| **Production Database** | Neon Serverless | Launch Tier Baseline | PostgreSQL 16 (10 GB storage, PITR branching, autoscaling compute) | 19.00 |
| **Encrypted Object Storage** | Cloudflare R2 | Pay-As-You-Go ($0.015/GB-mo) | Encrypted report attachments, 50 GB pooled baseline, zero egress fees | 0.75 |
| **Transactional Email Delivery** | Resend / Postmark Pro | Essential Commercial Tier | High deliverability minimal-metadata notifications (50,000/mo) | 20.00 |
| **Domain & DNS Registration** | Cloudflare Registrar | `.com` / `.security` TLD | Amortized domain registrar fee ($15.00/year) | 1.25 |
| **Merchant of Record Gateway** | Lemon Squeezy | MoR Billing & Global Tax | Handles global VAT, sales tax, direct bank payouts to Pakistan (5% + 50¢/tx) | 0.00 |

**TOTAL PRODUCTION OPERATING BASELINE**: **~$61.00 / Month** (100% covered by 2 paying tenants on the $49/mo Team plan)

---

*--- End of Work Breakdown Structure (WBS) ---*
