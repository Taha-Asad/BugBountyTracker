# BugBountyTrack — Project Executive Summary

**Project**: BugBountyTrack  
**Academic Level**: Fifth-Semester Project (Evaluated Prototype)  
**Student**: Taha Asadullah (Software Engineering Technology)  
**Sub-Field**: Application Security & Secure Software Engineering  
**Last Updated**: September 2026  

---

## 1. The Big Picture (The 30-Second Pitch)

```mermaid
flowchart LR
    A["1. Finder Discovers Bug<br/>(Reads security.txt)"] --> B["2. Submits Encrypted Report<br/>(Locked with PGP)"]
    B --> C["3. Company Fixes Code<br/>(Links Git Commit)"]
    C --> D["4. Verified Retest<br/>(Proves Bug is Dead)"]
```

* **The Problem**: Small tech startups and open-source teams cannot afford expensive enterprise bug platforms like HackerOne ($\$15\text{k}-\$30\text{k}+/\text{year}$). When ethical hackers find dangerous vulnerabilities, they report them through unencrypted emails or social media DMs. This leaks sensitive zero-days and leads to bugs being forgotten or closed without anyone verifying the fix.
* **Our Solution**: **BugBountyTrack** is a lightweight, multi-tenant web platform that gives startups an official `security.txt` beacon, an encrypted intake portal where reports are locked in the browser, and an **accountable fix tracker** that proves a bug was actually patched and retested before the ticket is closed.

---

## 2. The Three Core Pillars

### Pillar 1: The Public Door (`security.txt` & Account Portal)
* A startup hosts a standard text file (`acme.com/.well-known/security.txt`) pointing to their BugBountyTrack program page.
* Anyone can read the startup's disclosure policy, in-scope domains, and safe harbor terms.
* To prevent automated spam and abuse, researchers must register a verified account before submitting findings.

### Pillar 2: The Two-Way Lockbox (Client-Side OpenPGP)
* When a researcher submits an exploit, their browser encrypts the report with **OpenPGP** before sending it to our server.
* **The Two Keys**: The message is encrypted so that **only two people** can unlock and read it:
  1. The **Reporting Researcher**.
  2. The **Designated Company Triage Lead**.
* **What the Server Sees**: The database only stores scrambled ciphertext. Even if an attacker dumps our database, they cannot read the secret vulnerability details or PoC code.
* **Safe Display**: When the triage lead opens the report, their browser unlocks the text and renders the code safely without running any malicious scripts.

### Pillar 3: The Honest Fix Loop (Our Main Differentiator)
* Most issue trackers let developers click "Closed" with zero evidence. BugBountyTrack enforces proof.
* **Step 1 (Declaration)**: The developer links the fix by entering a Git commit hash (our backend checks GitHub's API to confirm the commit exists) or a configuration note (like an AWS S3 or firewall setting).
* **Step 2 (Retest)**: The report moves to `RETEST_PENDING`.
* **Step 3 (Proof)**: The ticket can only close under one of three transparent outcomes:
  1. `VERIFIED_RESEARCHER`: The original hacker re-tests and confirms the bug is fixed.
  2. `VERIFIED_INTERNAL`: Another team member tests and confirms the fix (our audit log records who tested it and whether they wrote the code).
  3. `CLOSED_UNVERIFIED_TIMEOUT`: If the hacker disappears, an authorized manager must click an explicit button and record a written reason. A timeout **never** counts as a passed test.

---

## 3. How the Code & Data Work (Under the Hood)

| Data Category | Who Can Read It? | Storage Format | Purpose |
| :--- | :--- | :--- | :--- |
| **Bug Status, Timestamps, Severity (CVSS)** | The Server & Both Parties | Plaintext (PostgreSQL columns) | Enables dashboard sorting, filtering, and workflow transitions. |
| **Commit Hashes & Retest Logs** | The Server & Both Parties | Plaintext (PostgreSQL columns) | Provides an unalterable audit trail of who verified the fix. |
| **Exploit Steps, PoC Code, & Screenshots** | **Only the Hunter & Triage Lead** | Scrambled PGP Ciphertext | Protects confidential zero-day details from leaks. |

### Edge Case Handling
* **What if someone loses their private key?**  
  If the researcher loses their key, they can no longer read past messages, but the company triage lead still can. There is no server-side "reset password" backdoor for private keys, preserving the cryptographic guarantee.
* **What if the hacker ghosts us?**  
  The company isn't stuck forever. After a configurable grace period, a manager can close the ticket, but it is explicitly stamped as *"Closed without verification because researcher was unresponsive."*

---

## 4. The 16-Week Implementation Roadmap

```
Weeks 1–3:   Design the blueprints, database tables, and user flows (SRS & Architecture).
Weeks 4–6:   Build the Next.js app, login system, and OpenPGP key setup.
Weeks 7–9:   Build the report forms, CVSS 3.1 calculator, and encrypted triage chat.
Weeks 10–12: Connect GitHub commit checking and the retest state machine.
Weeks 13–14: Run an exploratory study with 3–5 classmates using OWASP Juice Shop.
Weeks 15–16: Security checks, write the final report, and prep demo slides.
```

---

## 5. Why the Examination Committee & HOD Will Approve It

1. **No Fake Buzzwords**: We avoid unpredictable "AI triage" or untested claims. Everything runs on deterministic math (FIRST.org CVSS 3.1), audited libraries (`openpgp.js`), and clean database design.
2. **Solid Application Security**: Demonstrates browser-side asymmetric cryptography (OpenPGP), AST-level XSS prevention, and multi-tenant data isolation.
3. **Real Software Engineering**: Solves the actual problem of bug tracking—proving that a fix actually occurred rather than trusting an informal status drop-down.
4. **Feasible Timeline**: By cutting out real-money Stripe payments and automated exploit scanners, a solo student can comfortably build, test, and demo this evaluated prototype in one semester.

---

## 6. Project Document Index

| Document | Path | Description |
| :--- | :--- | :--- |
| **Academic Proposal** | [`requirements/HOD_PROPOSAL.md`](file:///run/media/thefoolishcrow/New%20Volume/Obsidian/TheFallenCrow/projects/BugBountyTrack/requirements/HOD_PROPOSAL.md) | Formal 2–3 page document for HOD and supervisor review. |
| **Key Architecture** | [`architecture/KEY_MANAGEMENT.md`](file:///run/media/thefoolishcrow/New%20Volume/Obsidian/TheFallenCrow/projects/BugBountyTrack/architecture/KEY_MANAGEMENT.md) | Detailed technical specifications for OpenPGP key mechanics and trust boundaries. |
| **Decision Log** | [`decisions/DECISION_LOG.md`](file:///run/media/thefoolishcrow/New%20Volume/Obsidian/TheFallenCrow/projects/BugBountyTrack/decisions/DECISION_LOG.md) | Living register of confirmed decisions, assumptions, and deferred features. |
| **Working SRS Draft** | [`requirements/SRS.md`](file:///run/media/thefoolishcrow/New%20Volume/Obsidian/TheFallenCrow/projects/BugBountyTrack/requirements/SRS.md) | Detailed requirements specification (to be updated after proposal approval). |
