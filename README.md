# BugBountyTrack — Private Bug Bounty & Vulnerability Disclosure Platform

> **Core Value Proposition**: *A confidential vulnerability reporting workspace that helps small software teams receive reports, coordinate fixes, and document how each issue was retested and closed.*

**Document Release State**: Commercial Baseline & Academic Evaluation Specification (Version 3.0.0)  
**Standard Compliance**: IEEE Std 830-1998 / ISO/IEC/IEEE 29148:2018  

---

## Academic & Project Control Metadata

| Parameter | Specification |
| :--- | :--- |
| **Project Identifier** | `PTUT - PRJ - 089` |
| **Academic Sub-Field** | 9. Cybersecurity, Privacy & LegalTech |
| **Student Author** | Taha Asadullah (Roll No: **`24-ST-013`**) |
| **Official Email** | `24-st-013@students.ptut.edu.pk` |
| **Academic Institution** | Punjab Tianjin University of Technology (PTUT), Lahore |
| **Department** | Department of Software Engineering Technology |
| **Session / Batch / Section** | Session 2024–2028 / Batch 24-SET-Fall / Section SET-A |
| **FYP Supervisor** | Sir Umar Hayat |
| **Primary Architecture** | Decoupled 3-Tier Web App (Next.js 14+ App Router, Node.js 22 LTS, Neon PostgreSQL 16, OpenPGP.js, Tailwind CSS) |
| **Document Suite Version** | **Version 3.0.0** (Commercial Baseline & Academic Defense Specification) |

---

## Repository Structure

```text
projects/BugBountyTrack/
├── .gitignore                      # Comprehensive Git exclusion rules (OS, Node, Python, env)
├── README.md                       # Repository overview, attribution, and build guide
├── project.json                    # Machine-readable project state and metadata
├── PROJECT_SUMMARY.md              # Executive summary and architectural baseline
├── architecture/                   # Technical architecture & key management runbooks
│   └── KEY_MANAGEMENT.md
├── decisions/                      # Architecture Decision Records (ADRs)
│   └── DECISION_LOG.md
├── evidence/                       # Verification artifacts and test logs (.gitkeep)
├── learning/                       # Engineering research notes and prototypes (.gitkeep)
├── requirements/                   # Core engineering specification suite
│   ├── BRD.md                      # Business Requirements Document (Markdown source)
│   ├── BRD.docx                    # Compiled Word BRD (styled with Lexend & shaded tables)
│   ├── SRS.md                      # Software Requirements Specification (Markdown source)
│   ├── SRS.docx                    # Compiled Word SRS (with 6 embedded high-res diagrams)
│   ├── WBS.md                      # Work Breakdown Structure (5 Sheets, 264h baseline + M3)
│   ├── WBS.xlsx                    # Compiled Excel WBS (live =SUM() formulas across sheets)
│   ├── CVSS_TEST_FIXTURES.md       # Traceable fixture suite of 52 canonical FIRST.org/NIST vectors
│   ├── HOD_PROPOSAL.md             # Formal FYP departmental proposal
│   ├── WEEK_1_DISCOVERY_REPORT.md  # Discovery and competitive landscape report
│   ├── compile_brd_docx.py         # Portable compiler: BRD.md -> BRD.docx
│   ├── compile_srs_docx.py         # Portable compiler: SRS.md + diagrams -> SRS.docx
│   ├── compile_wbs_xlsx.py         # Portable compiler: WBS.md -> WBS.xlsx
│   ├── generate_perfect_diagrams.py# SVG/PNG compiler for all 6 architecture diagrams
│   ├── verify_all_specifications.py# Automated verification suite (85 checks, 100% pass)
│   └── diagrams/                   # Architecture, sequence, state, and ERD diagrams
│       ├── fig4_1_component.png / .svg
│       ├── fig4_2_usecase.png / .svg
│       ├── fig4_3_seq_submission.png / .svg
│       ├── fig4_4_seq_decryption.png / .svg
│       ├── fig4_5_statemachine.png / .svg
│       └── fig4_6_erd.png / .svg
├── Resources/                      # Base OpenXML templates for docx and xlsx compilation
│   ├── BRD.docx
│   ├── SRS.docx
│   └── WBS.xlsx
└── tasks/                          # Sprint task tracking (.gitkeep)
```

---

## Core Differentiators & Commercial Architecture

1. **Client-Side Cryptographic Payload Isolation**:
   - Asymmetric OpenPGP dual-envelope encryption directly in the client browser.
   - Decoupled `title_ciphertext` (encrypted OpenPGP) from `operational_label` enum (`AUTHENTICATION_BYPASS`, `INJECTION_VULNERABILITY`, etc.) to prevent sensitive title leakage in notification emails and dashboards.
2. **Evidence-Based Remediation & Attested Retest**:
   - Decouples fix declaration from verification via GitHub REST API v3 (`GET /repos/{owner}/{repo}/commits/{ref}`) across public and private repositories.
   - State machine with **3 separate, non-overlapping terminal branches** from `RETEST_PENDING`:
     - `VERIFIED_RESEARCHER`: Independent empirical verification by reporting researcher.
     - `VERIFIED_INTERNAL`: Internal reviewer certification with conflict disclosure.
     - `CLOSED_UNVERIFIED_TIMEOUT`: Expired grace period ($\ge 14$ days) with recorded rationale.
   - `RETEST_FAILED` loops back to `ACCEPTED` as an audit event.
3. **Traceable CVSS 3.1 Scoring Engine**:
   - Pure TypeScript calculation engine verified against 52 canonical test vectors documented in [`CVSS_TEST_FIXTURES.md`](file:///run/media/thefoolishcrow/New%20Volume/Obsidian/TheFallenCrow/projects/BugBountyTrack/requirements/CVSS_TEST_FIXTURES.md).
4. **Redacted Closure Evidence Exports**:
   - Generates sanitized PDF/HTML summaries capturing the timeline, verified commit hash, deployment environment, and retest attestations without raw exploit instructions.
5. **Two-Tier Budget & Financial Viability**:
   - **Academic Demo Tier**: $0.00/mo operating within free cloud developer tiers (Vercel Hobby, Neon Free, Cloudflare R2 Free, Resend Free).
   - **Commercial Production Tier**: ~$60–$80/mo (Vercel Pro $20, Neon Launch $19, Cloudflare R2, Postmark/Resend Pro $20, Sentry) funded by Starter ($49/mo) and Team/Pro ($149/mo) SaaS subscriptions.

---

## Build & Verification Toolchain

All compilation and verification scripts are self-contained and can be executed from the repository root:

```bash
# 1. Run the comprehensive automated verification suite (85 checks)
python3 requirements/verify_all_specifications.py

# 2. Recompile BRD.docx from BRD.md
python3 requirements/compile_brd_docx.py

# 3. Recompile SRS.docx from SRS.md and diagrams/
python3 requirements/compile_srs_docx.py

# 4. Recompile WBS.xlsx from WBS.md
python3 requirements/compile_wbs_xlsx.py

# 5. Regenerate all 6 high-resolution SVG and PNG diagrams
python3 requirements/generate_perfect_diagrams.py
```

---

## GitHub Remote Setup

To publish this repository to GitHub and track changes with your team:

```bash
# Add your GitHub remote repository
git remote add origin https://github.com/<your-username>/BugBountyTrack.git

# Push the initial baseline commit
git push -u origin main
```
