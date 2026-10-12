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
| **Document Version** | `Revision 2.8` (Empirical Discovery Tracking Ledger) |
| **Current Empirical Status** | **`PENDING_LIVE_INTERVIEWS` (`0` Live Target-User Interviews Recorded to Date; Target: `>= 4` Participants [`>= 2` Cohort A + `>= 2` Cohort B])** |
| **Last Updated** | October 12, 2026 |

---

## 1. Epistemic Status & Methodological Boundary Declaration

This document is the canonical repository ledger referenced by `SRS.md` (`Section 1.4.2`), `WEEK_1_DISCOVERY_REPORT.md` (`Section 3`), and `WEEK_1_PART_A_USER_PERSONAS.md` (`Section 3`) to maintain a strict boundary between **modeled requirements assumptions** and **empirical human evidence**:

1. **Secondary Research & Workflow Modeling (`COMPLETED — PROVISIONAL BASELINE`)**:
   * The four operational frictions (`FRC-01: Provider-Managed Encryption`, `FRC-02: Insecure Ad-Hoc Email Channels`, `FRC-03: Legal Ambiguity & Registration Friction`, and `FRC-04: The "Fix-and-Forget" Verification Gap`) and the two target-user personas (**Alex Rivera — "The Hunter"** and **Sarah Chen — "The Defender"**) documented in `WEEK_1_DISCOVERY_REPORT.md`, `WEEK_1_PART_A_USER_PERSONAS.md`, and `SRS.md` are **Provisional Composite Personas** derived from secondary industry research, public vulnerability disclosure post-mortems, and international standards analysis (`ISO/IEC 29147:2018`, `ISO/IEC 30111:2019`, `IETF RFC 9116`, `IETF RFC 9580`, and `FIRST.org CVSS v3.1`).
   * **Zero live human interview quotes, transcripts, or survey statistics have been fabricated or retrofitted into those documents.**
2. **Live Target-User Discovery Interviews (`PENDING_LIVE_INTERVIEWS` — Target `>= 4` Participants Across Cohorts A & B)**:
   * Because the original Week 1 Problem Discovery rubric specifies interviewing target users (ethical security researchers and small-team engineering leads) to validate real-world workflow pain points, this file (`requirements/DISCOVERY_INTERVIEW_LOG.md`) provides the synchronized sampling criteria (`>= 4` participants: `>= 2` Cohort A + `>= 2` Cohort B), **Evidence Tiering (`Tier 1 Primary Evidence` vs. `Tier 2 Supplementary Evidence`)**, **Two-Stage Non-Leading Interview Script** (asking about actual past workflows and problems first before probing proposed features), consent boundary, and empirical recording ledger.
   * Until live human interview sessions are completed and logged in **Section 4** below, both `SRS.md` (`Section 1.4.2`) and this ledger carry the synchronized status **`PENDING_LIVE_INTERVIEWS`** and all personas remain explicitly labelled **Provisional Composite Personas**.
3. **Phase 4 Peer Usability & Accessibility Evaluation (`SCHEDULED FOR GATE 4 / WBS WP-6.2`)**:
   * Later System Usability Scale (`SUS >= 75.0`, `NFR-04`) evaluation with 3–5 computer science / cybersecurity peers tests the **implemented user interface (`SCR-01` to `SCR-12`)** and does **not** substitute for upstream target-user problem discovery interviews.

---

## 2. Target-User Sampling Criteria, Evidence Tiering & Ethical Consent Protocol

### 2.1 Target Participant Cohorts & Evidence Tiering (`Tier 1 Primary` vs. `Tier 2 Supplementary`)

To prevent academic or competition-only experience from being conflated with production vulnerability disclosure and triage workflows, every interviewed participant is classified into one of two explicit evidence tiers (**at least one `Tier 1 Primary Evidence` participant is required in each cohort**):

* **Tier 1 — Primary Empirical Evidence (`Production Disclosure / Triage Experience`)**:
  * **Cohort A (`HUNTER` — Tier 1)**: External security researcher, penetration tester, or bug finder who has submitted at least one real-world vulnerability report or coordinated disclosure to an external organization, vendor, or public/private VDP/bounty program.
  * **Cohort B (`DEFENDER` — Tier 1)**: CTO, engineering lead, or AppSec/DevSecOps triager responsible for receiving, triaging, or shipping security patches for externally reported vulnerabilities in a production software team (`5–50` developers).
* **Tier 2 — Supplementary Empirical Evidence (`Adjacent / Academic / CTF Experience`)**:
  * **Cohort A (`HUNTER` — Tier 2)**: University cybersecurity / Capture-The-Flag (CTF) practitioner with exploit development experience who has not yet submitted a live external vulnerability report to a vendor.
  * **Cohort B (`DEFENDER` — Tier 2)**: University lab infrastructure lead or capstone team lead managing shared multi-developer repositories and deployments without prior external VDP triage history.
  * *Methodological & Undergraduate Recruitment Fallback Rule*: **Tier 2 observations are recorded strictly as supplementary usability and mental-model feedback** and may not be cited on their own as validation of production industry disclosure/triage friction without corroborating Tier 1 evidence. Because the project author is an undergraduate student without pre-existing corporate security contacts, `Tier 1` participants may be recruited asynchronously via public channels (e.g., maintainers of open-source GitHub repositories publishing `SECURITY.md` policies, public OWASP/cybersecurity community groups, or university faculty/alumni with industry software roles). If external `Tier 1` commercial practitioners cannot be reached within the academic semester timeline, the 4-participant interview log may be completed using accessible `Tier 2` university peers, provided the summary table explicitly marks the sample as **`TIER_2_ACADEMIC_PEER_SAMPLE_ONLY`** rather than claiming `Tier 1` commercial validation.

| Cohort ID | Target Archetype | Evidence Tier Requirement | Target Sample Size | Current Completed Count |
| :--- | :--- | :--- | :---: | :---: |
| **Cohort A (`HUNTER`)** | External Ethical Security Researcher / Bug Finder | **`>= 1` Tier 1 Primary** preferred (real external disclosure experience via public/alumni outreach); **Tier 2 University CTF/Security Peers** permitted if labeled `TIER_2_ACADEMIC_PEER_SAMPLE_ONLY` | `>= 2` Participants | `0 / 2` (`PENDING_LIVE_INTERVIEWS`) |
| **Cohort B (`DEFENDER`)** | Small-Team Engineering Lead / Startup CTO / AppSec Triager | **`>= 1` Tier 1 Primary** preferred (production repo/team maintainer via public/alumni outreach); **Tier 2 University Multi-Dev Repo Leads** permitted if labeled `TIER_2_ACADEMIC_PEER_SAMPLE_ONLY` | `>= 2` Participants | `0 / 2` (`PENDING_LIVE_INTERVIEWS`) |
| **Total Sample** | Combined Hunter + Defender Discovery Sample | Synchronized with `SRS.md` (`Section 1.4.2`) | **`>= 4` Participants** | **`0 / 4` (`PENDING_LIVE_INTERVIEWS`)** |

### 2.2 Ethical Interview & Data Privacy Protocol

1. **Informed Consent & Anonymization**: Participants are informed before the session that their workflow observations will be recorded in an academic capstone requirements log (`PTUT - PRJ - 089`). Real company names, proprietary repository URLs, and unpatched vulnerability details are redacted; participants are identified by anonymized codes (`INT-HUNTER-01`, `INT-DEFENDER-01`, etc.) unless explicit written permission is granted to attribute by name.
2. **Strict Non-Fabrication Rule**: Only dated, verbatim or contemporaneously summarized notes from actual human conversations may be entered into **Section 4**. Hypothetical or AI-generated responses are strictly prohibited.
3. **Hypothesis Falsification Tracking**: Each interview explicitly records both **validated assumptions** (where the participant's real workflow matches `FRC-01`–`FRC-04`) and **falsified or nuanced assumptions** (where the participant's real workflow differs from the provisional model), along with any resulting updates to `SRS.md`.

---

## 3. Two-Stage Non-Leading Discovery Interview Guide

> **Methodological Rule (Non-Leading Sequence)**: Every interview session is divided into two sequential stages. **Stage 1 must be completed in full before any proposed `BugBountyTrack` design concept is mentioned**, ensuring that participants describe their actual past behavior and pain points without being led toward the project's architecture. **Stage 2** is asked only after Stage 1 concludes, to test whether the proposed mechanisms introduce new usability friction.

### 3.1 Cohort A Interview Script — External Security Researchers ("Hunters")

#### Stage 1 — Actual Past Behavior & Unprompted Problem Discovery (Asked First, Zero Mention of Proposed Features)

1. **Past Disclosure Channel & PoC Handling (`FRC-01`, `FRC-02`)**:
   * *"Think back to the last time you found a security bug in a web application or API that was not on a major paid bug bounty platform. Walk me step-by-step through how you found out who to contact and how you sent the technical details."*
   * *"When you had to send a working proof-of-concept (PoC), screenshots, or exploit steps, what channel did you use, and did anything about how that data was transmitted or stored concern you?"*
2. **Policy Discovery & Decision to Report (`FRC-03`)**:
   * *"Before testing or reporting a flaw to an independent company, what information do you look for on their website or domain? Have you ever decided not to report a valid bug you found—and if so, what caused you to walk away?"*
3. **Identity, Accounts & Follow-Up Tracking (`FRC-03`)**:
   * *"When you report a vulnerability to a company for the first time, do you prefer using a registered account, an alias, or reporting anonymously? How have you kept track of follow-up questions on reports you submitted in the past?"*
4. **Past Triage Disputes & Fix Verification (`FRC-04`)**:
   * *"Tell me about a time when a vendor disagreed with the severity of your report or told you a bug was fixed. How did they explain their reasoning, and how did you check whether the issue was actually resolved?"*

#### Stage 2 — Proposed Feature & Usability Probe (Asked Only After Stage 1 Is Completed)

5. **Probe A1 — Account-Less Submission & `.bbt-recovery.json` Recovery File (`FR-1.6`)**:
   * *"Suppose a self-hosted disclosure portal lets you submit without creating an account by generating a passphrase-encrypted `.bbt-recovery.json` file in your browser so you can check updates later. Compared to how you track reports today, would you use that workflow, or what would annoy or worry you about managing that recovery file?"*
6. **Probe A2 — Mandatory CVSS v3.1 Explanation & Deployment-Linked Retest (`FR-4.4`, `FR-6.1`–`FR-6.3`, `FR-7.2`)**:
   * *"If a triage team scored your report using CVSS v3.1 and was required to share a written metric explanation alongside the target environment and Git commit SHA (or redacted config diff) when asking you to retest, which of those details would actually be useful to you, and which would feel unnecessary?"*

### 3.2 Cohort B Interview Script — Small-Team Engineering Leads ("Defenders")

#### Stage 1 — Actual Past Behavior & Unprompted Problem Discovery (Asked First, Zero Mention of Proposed Features)

1. **Current Intake Channels & Internal Access Control (`FRC-01`, `FRC-02`)**:
   * *"Walk me through how your team currently receives external security reports or bug reports from outside your organization. Once a report arrives, where is it stored, and who in the company can view the raw details?"*
   * *"What challenges, if any, has your team experienced with sensitive exploit details ending up in shared email inboxes, chat channels, or general issue trackers?"*
2. **Past Experience with Encryption & Key Management (`FRC-02`)**:
   * *"Has your team ever used PGP or another encryption tool for incoming security reports? If yes, what happened when team members joined, left, or changed laptops? If no, what kept you from adopting it?"*
3. **Noise, Deadlines & Triage Workflow (`FRC-03`, `FRC-04`)**:
   * *"When external security emails or reports come in, how do you separate low-value scanner noise from real issues, and how do you track whether someone on the team has replied to the reporter?"*
4. **Patch Verification & External Audit Requests (`FRC-04`)**:
   * *"Once an engineer writes a fix for a reported security issue, how do you currently confirm that the fix is deployed before closing the ticket? Have customers, partners, or auditors ever asked your team for evidence of how a vulnerability was resolved?"*

#### Stage 2 — Proposed Feature & Usability Probe (Asked Only After Stage 1 Is Completed)

5. **Probe B1 — Browser-Side Multi-Recipient OpenPGP & Offline Master Recovery Key (`FR-3.1`–`FR-3.8`)**:
   * *"We are prototyping a workflow where reports are encrypted in the browser for authorized triage engineers' keys plus an offline Organization Master Recovery Key tested during onboarding. Where do you think a small engineering team would struggle with passphrase unlock, device changes, or offboarding in that setup?"*
6. **Probe B2 — Git Commit / Config-Diff Binding & Redacted Closure Exports (`FR-6.1`–`FR-6.4`, `FR-7.7`)**:
   * *"If the triage tool verified that a proposed fix commit SHA was merged into your target branch (or captured an encrypted configuration diff) before inviting the researcher to retest, and could export a signed, redacted closure summary, how would that fit—or conflict with—your team's release process?"*

---

## 4. Empirical Interview Session Ledger (`0` Completed / `>= 4` Planned Slots — `PENDING_LIVE_INTERVIEWS`)

> **Ledger Integrity Note**: All interview slots below are currently marked **`PENDING_LIVE_INTERVIEWS`**. As live target-user interviews are conducted by the Student Author (Taha Asadullah), each completed session will be populated with the date, anonymized participant profile, **Evidence Tier (`Tier 1 Primary` vs. `Tier 2 Supplementary`)**, separate **Stage 1 (Past Behavior)** and **Stage 2 (Feature Probe)** notes, and hypothesis validation mapping.

### 4.1 Slot `INT-HUNTER-01` — External Ethical Security Researcher #1

| Field | Empirical Record |
| :--- | :--- |
| **Session ID** | `INT-HUNTER-01` |
| **Status** | **`PENDING_LIVE_INTERVIEWS` (`No live interview recorded yet`)** |
| **Target Evidence Tier** | **`Tier 1 Primary Evidence`** *(External security researcher with real vulnerability disclosure reporting experience)* |
| **Interview Date & Modality** | *Pending scheduling (In-person / Video call / Written structured interview)* |
| **Participant Profile (Anonymized)** | *Pending participant recruitment* |
| **Stage 1 Notes (Unprompted Past Workflow & Pain Points)** | *No empirical data recorded yet.* |
| **Stage 2 Notes (Proposed Feature & Usability Probe)** | *No empirical data recorded yet.* |
| **Hypothesis Validation (`FRC-01`..`FRC-04`)** | *Pending empirical comparison against Provisional Persona 1 (Alex Rivera).* |
| **Resulting SRS / Design Adjustments** | *None yet — baseline remains governed by secondary research in `SRS.md` (`Revision 2.8`).* |

### 4.2 Slot `INT-HUNTER-02` — External Ethical Security Researcher #2

| Field | Empirical Record |
| :--- | :--- |
| **Session ID** | `INT-HUNTER-02` |
| **Status** | **`PENDING_LIVE_INTERVIEWS` (`No live interview recorded yet`)** |
| **Target Evidence Tier** | **`Tier 1 Primary Evidence`** *(or `Tier 2 Supplementary Evidence` if CTF/academic researcher)* |
| **Interview Date & Modality** | *Pending scheduling (In-person / Video call / Written structured interview)* |
| **Participant Profile (Anonymized)** | *Pending participant recruitment* |
| **Stage 1 Notes (Unprompted Past Workflow & Pain Points)** | *No empirical data recorded yet.* |
| **Stage 2 Notes (Proposed Feature & Usability Probe)** | *No empirical data recorded yet.* |
| **Hypothesis Validation (`FRC-01`..`FRC-04`)** | *Pending empirical comparison against Provisional Persona 1 (Alex Rivera).* |
| **Resulting SRS / Design Adjustments** | *None yet — baseline remains governed by secondary research in `SRS.md` (`Revision 2.8`).* |

### 4.3 Slot `INT-DEFENDER-01` — Small-Team Engineering Lead / Startup Triager #1

| Field | Empirical Record |
| :--- | :--- |
| **Session ID** | `INT-DEFENDER-01` |
| **Status** | **`PENDING_LIVE_INTERVIEWS` (`No live interview recorded yet`)** |
| **Target Evidence Tier** | **`Tier 1 Primary Evidence`** *(CTO, Engineering Lead, or AppSec owner at a 5–50 developer production software team)* |
| **Interview Date & Modality** | *Pending scheduling (In-person / Video call / Written structured interview)* |
| **Participant Profile (Anonymized)** | *Pending participant recruitment* |
| **Stage 1 Notes (Unprompted Past Workflow & Pain Points)** | *No empirical data recorded yet.* |
| **Stage 2 Notes (Proposed Feature & Usability Probe)** | *No empirical data recorded yet.* |
| **Hypothesis Validation (`FRC-01`..`FRC-04`)** | *Pending empirical comparison against Provisional Persona 2 (Sarah Chen).* |
| **Resulting SRS / Design Adjustments** | *None yet — baseline remains governed by secondary research in `SRS.md` (`Revision 2.8`).* |

### 4.4 Slot `INT-DEFENDER-02` — Small-Team Engineering Lead / Startup Triager #2

| Field | Empirical Record |
| :--- | :--- |
| **Session ID** | `INT-DEFENDER-02` |
| **Status** | **`PENDING_LIVE_INTERVIEWS` (`No live interview recorded yet`)** |
| **Target Evidence Tier** | **`Tier 1 Primary Evidence`** *(or `Tier 2 Supplementary Evidence` if university/lab infrastructure lead)* |
| **Interview Date & Modality** | *Pending scheduling (In-person / Video call / Written structured interview)* |
| **Participant Profile (Anonymized)** | *Pending participant recruitment* |
| **Stage 1 Notes (Unprompted Past Workflow & Pain Points)** | *No empirical data recorded yet.* |
| **Stage 2 Notes (Proposed Feature & Usability Probe)** | *No empirical data recorded yet.* |
| **Hypothesis Validation (`FRC-01`..`FRC-04`)** | *Pending empirical comparison against Provisional Persona 2 (Sarah Chen).* |
| **Resulting SRS / Design Adjustments** | *None yet — baseline remains governed by secondary research in `SRS.md` (`Revision 2.8`).* |

---

## 5. Traceability to Week 1 & Week 2 Requirements Baseline

| Provisional Friction / Persona Construct | Secondary Research Source (`Completed`) | Empirical Interview Verification Slot (`PENDING_LIVE_INTERVIEWS`) | Mapped SRS Requirements (`Revision 2.8`) |
| :--- | :--- | :--- | :--- |
| **`FRC-01` & `FRC-02`: Provider-Managed Key Control & Plaintext Email Leaks** | `ISO/IEC 29147:2018` §6.2; `IETF RFC 9580` (OpenPGP v6); public VDP architecture analysis | `INT-HUNTER-01`, `INT-HUNTER-02`, `INT-DEFENDER-01`, `INT-DEFENDER-02` (Stage 1 Q1–Q2; Stage 2 Probes) | `FR-1.2`, `FR-3.1`–`FR-3.8`, `FR-5.1`–`FR-5.3` |
| **`FRC-03`: Legal Ambiguity (`security.txt` / Safe Harbor) & Account Signup Friction** | `IETF RFC 9116`; Disclose.io Safe Harbor framework; OWASP VDP guidelines | `INT-HUNTER-01`, `INT-HUNTER-02` (Stage 1 Q2–Q3; Probe A1); `INT-DEFENDER-01`, `INT-DEFENDER-02` (Stage 1 Q3) | `FR-1.6a`–`FR-1.6f`, `FR-2.1`–`FR-2.5`, `FR-8.3` |
| **`FRC-04`: Subjective Severity & "Fix-and-Forget" Unverified Closures** | `ISO/IEC 30111:2019` §7.4; `FIRST.org CVSS v3.1` Specification | `INT-HUNTER-01`, `INT-HUNTER-02` (Stage 1 Q4; Probe A2); `INT-DEFENDER-01`, `INT-DEFENDER-02` (Stage 1 Q4; Probe B2) | `FR-4.1`–`FR-4.4`, `FR-6.1`–`FR-6.4`, `FR-7.1`–`FR-7.7`, `FR-8.5` |
| **Provisional Persona 1: Alex Rivera ("The Hunter")** | `WEEK_1_PART_A_USER_PERSONAS.md` §4.1 | `INT-HUNTER-01`, `INT-HUNTER-02` | `UC-01`, `UC-04`, `UC-05` |
| **Provisional Persona 2: Sarah Chen ("The Defender")** | `WEEK_1_PART_A_USER_PERSONAS.md` §4.2 | `INT-DEFENDER-01`, `INT-DEFENDER-02` | `UC-02`, `UC-03`, `UC-04`, `UC-06`, `UC-07` |

