# Empirical Target-User Discovery Interview Log (`DISCOVERY_INTERVIEW_LOG.md`)

## BugBountyTrack — Private Bug Bounty & Vulnerability Disclosure Platform

| Attribute | Details |
| :--- | :--- |
| **Institution** | Punjab Tianjin University of Technology (PTUT), Lahore |
| **Department** | Department of Software Engineering Technology |
| **Project ID** | `PTUT - PRJ - 089` |
| **Project Title** | **BugBountyTrack — Private Bug Bounty & Vulnerability Disclosure Platform** |
| **Student Author** | Taha Asadullah (Roll No: `24-ST-013`, Section: `SET-B`) |
| **Academic Supervisor** | Sir Umar Hayat (Assistant Professor, PTUT Lahore) |
| **Document Version** | `Revision 2.7` (Empirical Discovery Tracking Ledger) |
| **Current Empirical Status** | **`PENDING_LIVE_INTERVIEWS` (`0` Live Target-User Interviews Recorded to Date)** |
| **Last Updated** | October 12, 2026 |

---

## 1. Epistemic Status & Methodological Boundary Declaration

This document is the canonical repository ledger referenced by `SRS.md` (`Section 1.4.2`), `WEEK_1_DISCOVERY_REPORT.md` (`Section 3`), and `WEEK_1_PART_A_USER_PERSONAS.md` (`Section 3`) to maintain a strict boundary between **modeled requirements assumptions** and **empirical human evidence**:

1. **Secondary Research & Workflow Modeling (`COMPLETED — PROVISIONAL BASELINE`)**:
   * The four operational frictions (`FRC-01: Provider-Managed Encryption`, `FRC-02: Insecure Ad-Hoc Email Channels`, `FRC-03: Legal Ambiguity & Registration Friction`, and `FRC-04: The "Fix-and-Forget" Verification Gap`) and the two target-user personas (**Alex Rivera — "The Hunter"** and **Sarah Chen — "The Defender"**) documented in `WEEK_1_DISCOVERY_REPORT.md`, `WEEK_1_PART_A_USER_PERSONAS.md`, and `SRS.md` are **Provisional Composite Personas** derived from secondary industry research, public vulnerability disclosure post-mortems, and international standards analysis (`ISO/IEC 29147:2018`, `ISO/IEC 30111:2019`, `IETF RFC 9116`, `IETF RFC 9580`, and `FIRST.org CVSS v3.1`).
   * **Zero live human interview quotes, transcripts, or survey statistics have been fabricated or retrofitted into those documents.**
2. **Live Target-User Discovery Interviews (`TRACKED IN THIS LEDGER — PENDING EXECUTION`)**:
   * Because the original Week 1 Problem Discovery rubric specifies interviewing target users (ethical security researchers and small-team engineering leads) to validate real-world workflow pain points, this file (`requirements/DISCOVERY_INTERVIEW_LOG.md`) provides the structured interview protocol, consent boundary, and empirical recording ledger.
   * Until live human interview sessions are completed and logged in **Section 4** below, all personas in the repository remain explicitly labelled **Provisional Composite Personas**.
3. **Phase 4 Peer Usability & Accessibility Evaluation (`SCHEDULED FOR GATE 4 / WBS WP-5.3`)**:
   * Later System Usability Scale (`SUS >= 75.0`, `NFR-04`) evaluation with 3–5 computer science / cybersecurity peers tests the **implemented user interface (`SCR-01` to `SCR-12`)** and does **not** substitute for upstream target-user problem discovery interviews.

---

## 2. Target-User Sampling Criteria & Ethical Consent Protocol

### 2.1 Target Participant Cohorts

| Cohort ID | Target Archetype | Inclusion Criteria | Target Sample Size | Current Completed Count |
| :--- | :--- | :--- | :---: | :---: |
| **Cohort A (`HUNTER`)** | External Ethical Security Researcher / Bug Finder | At least 6 months of practical vulnerability research, bug bounty participation, CTF competition experience, or responsible disclosure reporting to real web/API targets. | `>= 2` Participants | `0 / 2` (`PENDING`) |
| **Cohort B (`DEFENDER`)** | Small-Team Engineering Lead / Startup CTO / AppSec Triager | Responsible for production deployment, repository governance, or security triage in a software engineering team of `5–50` developers (or university capstone/lab production infrastructure lead). | `>= 2` Participants | `0 / 2` (`PENDING`) |

### 2.2 Ethical Interview & Data Privacy Protocol

1. **Informed Consent & Anonymization**: Participants are informed before the session that their workflow observations will be recorded in an academic capstone requirements log (`PTUT - PRJ - 089`). Real company names, proprietary repository URLs, and unpatched vulnerability details are redacted; participants are identified by anonymized codes (`INT-HUNTER-01`, `INT-DEFENDER-01`, etc.) unless explicit written permission is granted to attribute by name.
2. **Strict Non-Fabrication Rule**: Only dated, verbatim or contemporaneously summarized notes from actual human conversations may be entered into **Section 4**. Hypothetical or AI-generated responses are strictly prohibited.
3. **Hypothesis Falsification Tracking**: Each interview explicitly records both **validated assumptions** (where the participant's real workflow matches `FRC-01`–`FRC-04`) and **falsified or nuanced assumptions** (where the participant's real workflow differs from the provisional model), along with any resulting updates to `SRS.md`.

---

## 3. Semi-Structured Discovery Interview Guide

### 3.1 Cohort A Interview Script — External Security Researchers ("Hunters")

1. **Current Disclosure Channel Experience (`FRC-01`, `FRC-02`)**:
   * *"Walk me through the last time you discovered a security flaw in an independent web application or SaaS product that was not on a paid enterprise bounty program. How did you locate their contact channel, and how did you send the proof-of-concept (PoC)?"*
   * *"Have you ever hesitated to send a raw exploit payload over standard email (`security@domain.com`) or a web form? What were your specific concerns regarding plaintext storage or third-party platform visibility?"*
2. **Discovery Policy & Legal Safe Harbor (`FRC-03`)**:
   * *"Before testing or reporting a flaw, do you check for `/.well-known/security.txt` (RFC 9116)? Which fields or legal assurances (such as Safe Harbor authorization and explicit `IN_SCOPE` / `OUT_OF_SCOPE` tables) determine whether you proceed or walk away?"*
3. **Account Registration vs. Account-Less Guest Reporting (`FRC-03`, `FR-1.6`)**:
   * *"When reporting a one-off vulnerability to a startup's self-hosted portal, how do you react if the portal requires full account registration before you can submit? If the portal offered an account-less submission with a downloadable encrypted recovery file (`.bbt-recovery.json`), would you use it, and what usability pitfalls would worry you?"*
4. **Triage Communication, Severity Scoring & Patch Retesting (`FRC-04`, `FR-4`, `FR-6`, `FR-7`)**:
   * *"After submitting a report, what is the most common breakdown you experience during triage and severity assessment? Have you seen a vendor close a ticket as 'Fixed' when the underlying bug was still exploitable? What evidence (e.g., CVSS 3.1 metric breakdown, Git commit SHA, deployed environment, retest prompt) would give you confidence that the fix is real?"*

### 3.2 Cohort B Interview Script — Small-Team Engineering Leads ("Defenders")

1. **Current Vulnerability Intake & Triage Workflow (`FRC-01`, `FRC-02`)**:
   * *"How does your engineering team currently receive external vulnerability reports (e.g., `security@` email alias, GitHub Security Advisories, issue tracker, or third-party VDP)? Who has access to read incoming reports?"*
   * *"If an external researcher emails a working SQL injection or authentication bypass proof-of-concept today, where does that payload end up stored (mail servers, Slack, Jira/Linear), and how do you restrict access to authorized engineers?"*
2. **Cryptographic Key Management Ergonomics (`FRC-02`, `FR-3.1`–`FR-3.8`)**:
   * *"Has your team ever published a PGP key for `security@`? If yes, what operational problems occurred with key rotation, team member onboarding/offboarding, or lost passphrases? If browser-side encryption handled multi-recipient key wrapping automatically with an offline Master Recovery Key backup, what friction would remain for your team?"*
3. **Spam Filtering, SLA Deadlines & Quota Protection (`FRC-03`, `FR-5.4`, `FR-8.3`, `FR-8.4`)**:
   * *"What proportion of external security messages you receive are low-effort scanner noise versus actionable reports? How do you track response deadlines so valid researchers are not accidentally ignored during busy sprint cycles?"*
4. **Remediation Traceability & Customer Compliance Proof (`FRC-04`, `FR-6.1`–`FR-6.3`, `FR-7.7`)**:
   * *"When a developer merges a security fix pull request, how do you verify that the commit reached the target branch/environment before telling the reporter it is resolved? Do enterprise customers or auditors ever ask for proof of how a reported vulnerability was handled without wanting to see the raw exploit?"*

---

## 4. Empirical Interview Session Ledger (`0` Completed / `4` Planned Slots)

> **Ledger Integrity Note**: All interview slots below are currently marked **`[PENDING — NO LIVE INTERVIEW RECORDED YET]`**. As live target-user interviews are conducted by the Student Author (Taha Asadullah), each completed session will be populated with the date, participant role profile, verbatim/summarized observations, and hypothesis validation mapping.

### 4.1 Slot `INT-HUNTER-01` — External Ethical Security Researcher #1

| Field | Empirical Record |
| :--- | :--- |
| **Session ID** | `INT-HUNTER-01` |
| **Status** | **`[PENDING — NO LIVE INTERVIEW RECORDED YET]`** |
| **Interview Date & Modality** | *Pending scheduling (In-person / Video call / Written structured interview)* |
| **Participant Profile (Anonymized)** | *Pending participant recruitment (Target: Independent bug bounty researcher or university CTF security practitioner)* |
| **Observed Current Disclosure Workflow** | *No empirical data recorded yet.* |
| **Hypothesis Validation (`FRC-01`..`FRC-04`)** | *Pending empirical comparison against Provisional Persona 1 (Alex Rivera).* |
| **Key Quotes / Concrete Friction Examples** | *None recorded yet.* |
| **Resulting SRS / Design Adjustments** | *None yet — baseline remains governed by secondary research in `SRS.md` (`Revision 2.7`).* |

### 4.2 Slot `INT-HUNTER-02` — External Ethical Security Researcher #2

| Field | Empirical Record |
| :--- | :--- |
| **Session ID** | `INT-HUNTER-02` |
| **Status** | **`[PENDING — NO LIVE INTERVIEW RECORDED YET]`** |
| **Interview Date & Modality** | *Pending scheduling (In-person / Video call / Written structured interview)* |
| **Participant Profile (Anonymized)** | *Pending participant recruitment (Target: External application security researcher or penetration tester)* |
| **Observed Current Disclosure Workflow** | *No empirical data recorded yet.* |
| **Hypothesis Validation (`FRC-01`..`FRC-04`)** | *Pending empirical comparison against Provisional Persona 1 (Alex Rivera).* |
| **Key Quotes / Concrete Friction Examples** | *None recorded yet.* |
| **Resulting SRS / Design Adjustments** | *None yet — baseline remains governed by secondary research in `SRS.md` (`Revision 2.7`).* |

### 4.3 Slot `INT-DEFENDER-01` — Small-Team Engineering Lead / Startup Triager #1

| Field | Empirical Record |
| :--- | :--- |
| **Session ID** | `INT-DEFENDER-01` |
| **Status** | **`[PENDING — NO LIVE INTERVIEW RECORDED YET]`** |
| **Interview Date & Modality** | *Pending scheduling (In-person / Video call / Written structured interview)* |
| **Participant Profile (Anonymized)** | *Pending participant recruitment (Target: CTO, Lead Engineer, or DevSecOps owner at a 5–50 developer software team)* |
| **Observed Current Intake & Patch Workflow** | *No empirical data recorded yet.* |
| **Hypothesis Validation (`FRC-01`..`FRC-04`)** | *Pending empirical comparison against Provisional Persona 2 (Sarah Chen).* |
| **Key Quotes / Concrete Friction Examples** | *None recorded yet.* |
| **Resulting SRS / Design Adjustments** | *None yet — baseline remains governed by secondary research in `SRS.md` (`Revision 2.7`).* |

### 4.4 Slot `INT-DEFENDER-02` — Small-Team Engineering Lead / Startup Triager #2

| Field | Empirical Record |
| :--- | :--- |
| **Session ID** | `INT-DEFENDER-02` |
| **Status** | **`[PENDING — NO LIVE INTERVIEW RECORDED YET]`** |
| **Interview Date & Modality** | *Pending scheduling (In-person / Video call / Written structured interview)* |
| **Participant Profile (Anonymized)** | *Pending participant recruitment (Target: Engineering Manager or Infrastructure/Security Lead maintaining web/API services)* |
| **Observed Current Intake & Patch Workflow** | *No empirical data recorded yet.* |
| **Hypothesis Validation (`FRC-01`..`FRC-04`)** | *Pending empirical comparison against Provisional Persona 2 (Sarah Chen).* |
| **Key Quotes / Concrete Friction Examples** | *None recorded yet.* |
| **Resulting SRS / Design Adjustments** | *None yet — baseline remains governed by secondary research in `SRS.md` (`Revision 2.7`).* |

---

## 5. Traceability to Week 1 & Week 2 Requirements Baseline

| Provisional Friction / Persona Construct | Secondary Research Source (`Completed`) | Empirical Interview Verification Slot (`Pending`) | Mapped SRS Requirements (`Revision 2.7`) |
| :--- | :--- | :--- | :--- |
| **`FRC-01` & `FRC-02`: Provider-Managed Key Control & Plaintext Email Leaks** | `ISO/IEC 29147:2018` §6.2; `IETF RFC 9580` (OpenPGP v6); public VDP architecture analysis | `INT-HUNTER-01`, `INT-HUNTER-02`, `INT-DEFENDER-01`, `INT-DEFENDER-02` (Q1, Q2) | `FR-1.2`, `FR-3.1`–`FR-3.8`, `FR-5.1`–`FR-5.3` |
| **`FRC-03`: Legal Ambiguity (`security.txt` / Safe Harbor) & Account Signup Friction** | `IETF RFC 9116`; Disclose.io Safe Harbor framework; OWASP VDP guidelines | `INT-HUNTER-01`, `INT-HUNTER-02` (Q2, Q3); `INT-DEFENDER-01`, `INT-DEFENDER-02` (Q3) | `FR-1.6a`–`FR-1.6f`, `FR-2.1`–`FR-2.5`, `FR-8.3` |
| **`FRC-04`: Subjective Severity & "Fix-and-Forget" Unverified Closures** | `ISO/IEC 30111:2019` §7.4; `FIRST.org CVSS v3.1` Specification | `INT-HUNTER-01`, `INT-HUNTER-02` (Q4); `INT-DEFENDER-01`, `INT-DEFENDER-02` (Q4) | `FR-4.1`–`FR-4.4`, `FR-6.1`–`FR-6.4`, `FR-7.1`–`FR-7.7`, `FR-8.5` |
| **Provisional Persona 1: Alex Rivera ("The Hunter")** | `WEEK_1_PART_A_USER_PERSONAS.md` §4.1 | `INT-HUNTER-01`, `INT-HUNTER-02` | `UC-01`, `UC-04`, `UC-05` |
| **Provisional Persona 2: Sarah Chen ("The Defender")** | `WEEK_1_PART_A_USER_PERSONAS.md` §4.2 | `INT-DEFENDER-01`, `INT-DEFENDER-02` | `UC-02`, `UC-03`, `UC-04`, `UC-06`, `UC-07` |
