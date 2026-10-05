# Decision Log — BugBountyTrack

**Project**: BugBountyTrack — Vulnerability Disclosure Platform with Remediation Tracking  
**Classification**: Fifth-Semester Project Proposal (Evaluated Prototype)  
**Current Phase**: SDLC Phase 1 (Planning & Requirements Engineering)  
**Last Updated**: 2026-09-20  
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
- **DEC-002**: Technical stack baseline: Next.js (App Router, TypeScript), Node.js, PostgreSQL (Prisma ORM), OpenPGP.js (client-side cryptography), and Tailwind CSS.
- **DEC-003**: Elimination of hype: No automated AI/LLM triage and no live exploit/PoC automated scanners.
- **DEC-004**: Active mentoring posture is "Build with me", pairing Alexander Cross (`CROSS-DIR`) as orchestrator and Victoria Vance (`VANCE-REQ`) as requirements lead.
- **DEC-005**: All project artifacts must reside in `projects/BugBountyTrack/` conforming to `projects/PROJECT_SCHEMA.md`.
- **DEC-006**: **Core Objective**: Focus on structured vulnerability reporting connected to verifiable fix references, retest evidence, and accountable closure.
- **DEC-007**: **State Machine Verification Scope**: The remediation state machine is an **integration-tested finite state machine** enforced at the application and database level; it is not claimed to be mathematically formally verified.
- **DEC-008**: **VCS Linkage Scope**: Checking a Git commit SHA confirms commit existence, author, and branch metadata via API; it does **not** prove runtime fix efficacy or deployment.
- **DEC-009**: **Exploratory Evaluation**: Project evaluation is an exploratory peer study (3–5 peers with 2 containerized reference apps like OWASP Juice Shop), providing empirical qualitative/quantitative data rather than claims of industry-wide proof.
- **DEC-010**: **Document Governance**: Proposal is a working draft until approved by the university department.
- **DEC-011**: **Tenancy Architecture**: Multi-tenant SaaS architecture where multiple organizations host isolated programs on one shared platform instance.
- **DEC-012**: **Mandatory PGP Constraint & Library**: PGP encryption is a strict project requirement implemented using the maintained `openpgp.js` library.
- **DEC-013**: **MVP User & Submission Access**:
  - Program directory and policy pages are public.
  - Submissions require a verified researcher account before filing.
  - Report decryption access is scoped strictly to the submitting researcher and one designated company triage lead per report.
- **DEC-014**: **Evidence Preservation & Safe Rendering**: Original vulnerability descriptions, PoC text, and sensitive remediation notes are preserved unmodified. Safe rendering (AST-level HTML escaping, strict markdown parsing, code-block containment) is enforced on the client after decryption.
- **DEC-015**: **Remediation & Retest Verification Rules**:
  - Fix declaration is strictly decoupled from retest verification.
  - Remediation evidence supports both code commits (validated via GitHub API) and non-code fixes (e.g., infrastructure config, WAF rules, DNS updates).
  - Internal verification must be performed by an authorized user with access to the evidence; the audit record explicitly tracks whether the verifier also implemented the fix.
  - Required verification audit fields: Tested version/environment, retest steps, outcome, evidence reference, verifier identity, organizational relationship, implementer flag, and timestamp.
  - Distinct closure states: `VERIFIED_RESEARCHER`, `VERIFIED_INTERNAL`, `CLOSED_UNVERIFIED_TIMEOUT`.
  - Closing under `CLOSED_UNVERIFIED_TIMEOUT` requires an **explicit authorized user action and recorded rationale**; expiration of a grace period alone never triggers automated closure or indicates successful verification.
  - Reopening is supported with a mandatory recorded reason.
- **DEC-016**: **Assistance vs. Security Boundary**: Client-side completeness checks are advisory user assistance, not trusted server-enforced security validation.
- **DEC-017**: **Key Management Boundaries**:
  - Losing one recipient's private key removes that recipient's access to historical messages; other recipients possessing their own private keys retain decryption capability. Automated key recovery is out of scope.
  - Key rotation applies to new replies in existing threads as well as new reports. Messages record recipient key fingerprints.
  - Attachments use standard multi-recipient OpenPGP encryption.
  - Trust assumption: The client browser and platform-delivered JavaScript code are assumed trusted.

---

## 2. Proposed Decisions (`[PROPOSED]`)
*(None currently pending review.)*

---

## 3. Assumptions (`[ASSUMPTION]`)
- **ASM-001**: Academic evaluators value clear software engineering discipline, verifiable controls, and documented limitations over inflated commercial claims or unverified security absolutes.
- **ASM-002**: Development and evaluation will run in a local Dockerized Linux environment before any staging deployment.
- **ASM-003**: OpenPGP multi-recipient encryption functions reliably in client browser JavaScript via `openpgp.js`.

---

## 4. Open Questions (`[OPEN QUESTION]`)
*(All initial scoping questions resolved for the 2–3 page HOD proposal.)*

---

## 5. Deferred Decisions (`[DEFERRED]`)
- **DEF-001**: Real-money payment rails (Stripe Connect, cross-border payouts, 1099 tax reporting).
- **DEF-002**: Automated sandbox reproduction and dynamic exploit scanning.
- **DEF-003**: Integration with external bug trackers (Jira, Linear, GitLab Issue Sync) beyond direct VCS commit referencing.
- **DEF-004**: Gamification features: Researcher reputation points, levels, and badges.
- **DEF-005**: Anonymous (unauthenticated) vulnerability reporting.
- **DEF-006**: Invitation-only / private disclosure programs.
- **DEF-007**: Multi-member key escrow / automated historical key recovery.
