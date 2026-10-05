# Cryptographic Key Management & Data Boundary Architecture

**Project**: BugBountyTrack — Vulnerability Disclosure Platform with Remediation Tracking  
**Document**: Architecture Design Note (`ARCH-NOTE-001`)  
**Status**: Active Architecture Reference (Version 3.2.0)  
**Standard**: OpenPGP Specification (RFC 4880 / RFC 9580) & `openpgp.js` Integration  

---

## 1. Overview & Core Cryptographic Objective

BugBountyTrack incorporates client-side OpenPGP encryption to protect sensitive vulnerability reproduction steps, proof-of-concept payloads, attachments, and remediation discussions against database compromise, cloud snapshot theft, and unauthorized server-side access.

The cryptographic subsystem executes in the user's web browser using `openpgp.js`. The server functions strictly as an untrusted message routing and ciphertext persistence layer for encrypted payloads.

To ensure rapid browser performance (<50ms) and eliminate compliance friction:
1. **Algorithm Pinning**: The platform pins exclusively to **v4 Ed25519 (Signing) / X25519 (Encryption)** Curve25519 keys. Legacy RSA-4096 is deprecated and dropped because its multi-second in-browser key generation violates NFR-02 (<1.5s).
2. **Standardized Key Protection**: Private keys stored in browser `IndexedDB` are protected using OpenPGP's standardized **Argon2 S2K (String-to-Key)** derivation rather than non-standard custom AES-GCM wrappers.

---

## 2. Recipient Scope & Multi-Defender Protocol

```mermaid
flowchart TD
    subgraph Browser["Client Browser (Guest Researcher / Defender)"]
        Msg["Plaintext Payload<br/>(PoC / Remediation Note / Attachment)"]
        K_S["Ephemeral Symmetric Session Key K_S (AES-256)"]
        Msg -->|"Encrypt with K_S"| Ciphertext["Encrypted Data Packet"]
        
        K_S -->|"Wrap for Report Key"| PKESK_R["PKESK (Ephemeral Report Key)"]
        K_S -->|"Wrap for Org Recovery"| PKESK_REC["PKESK (Org Master Recovery Key)"]
        K_S -->|"Wrap for Def 1"| PKESK_D1["PKESK (Defender 1 Key)"]
        K_S -->|"Wrap for Def N"| PKESK_DN["PKESK (Defender N Key)"]
        
        Combined["OpenPGP Armored Envelope<br/>(PKESK_R + PKESK_REC + PKESK_D1..N + Ciphertext)"]
        PKESK_R --> Combined
        PKESK_REC --> Combined
        PKESK_D1 --> Combined
        PKESK_DN --> Combined
        Ciphertext --> Combined
    end
    Combined -->|"POST with recipient_set_version"| Svr[("Server & Database<br/>(Verifies version & stores ciphertext)")]
```

### 2.1 Bounded Program-Scoped Recipient Model ($N \le 10$)
To prevent combinatorial key explosion while supporting collaborative team triage:
1. **Program-Scoped Authorization**: Encryption recipients are strictly bounded to the **reporting researcher** (or ephemeral report key), the **offline organization master recovery key**, plus the **active defenders explicitly assigned to the specific program** ($N \le 10$). Defenders in the same organization who are not assigned to the program are not included.
2. **Pseudonymous Key Identifiers**: The client fetches public encryption subkeys identified strictly by their 16-character OpenPGP Key ID or 40-character fingerprint. Employee names, email addresses, and internal roles are not included in public keyrings to minimize internal organizational disclosure.

### 2.2 Account-Less (Guest) Researcher Submission Lifecycle
To prevent adoption drop-off caused by mandatory account creation, BugBountyTrack enables account-less vulnerability intake:
1. **Ephemeral Key Generation**: When a researcher opens a program's submission form (`/report/:org_slug`), the browser autonomously generates an in-memory Curve25519 keypair (`K_report_pub`, `K_report_priv`) in under 40ms.
2. **Multi-Recipient Encryption**: The report payload is encrypted to:
   - All active defenders of the target program (`K_def_1..N`).
   - The organization's offline master recovery key (`K_recovery_pub`).
   - The ephemeral report key (`K_report_pub`).
3. **Tracking Token Generation**: Upon submission, the server returns an opaque, high-entropy tracking identifier (`BBT-RPT-XXXX`) paired with a cryptographic access token.
4. **Local Keystore Persistence**: The browser stores `K_report_priv` and the tracking URL in `localStorage`. The researcher is presented with a clear action prompt: *"Bookmark this tracking link or save your recovery code to view replies and verify fixes."*
5. **Anonymous Dialogue & Retest**: The researcher accesses `/report/track/:token` to read encrypted reviewer comments and submit retest evidence without ever registering an account or managing passwords.
6. **Optional Account Binding**: If the researcher later creates a BugBountyTrack account, they can claim historical report tokens to bind findings to their public profile and reputation score.

### 2.3 Offline Organization Master Recovery Key & Mandatory Backup
To prevent total data loss in the event of defender laptop destruction or browser cache clearing:
1. **Key Generation at Onboarding**: During initial organization onboarding, the owner's browser generates an **Organization Master Recovery Keypair** (`K_rec_pub`, `K_rec_priv`).
2. **Server Storage of Public Key**: The server stores `K_rec_pub` as part of the organization profile. Every report submitted to the organization includes a PKESK packet wrapped for `K_rec_pub`.
3. **Mandatory Offline Export**: `K_rec_priv` is **never** transmitted to the server. The owner must download the ASCII-armored recovery kit (`org-recovery-key.asc` or printable emergency kit).
4. **Pre-Activation Decryption Challenge**: The onboarding wizard requires the owner to upload the exported key file and decrypt a test challenge ciphertext before the organization is activated. Programs cannot receive reports until backup verification succeeds.
5. **Disaster Recovery**: If all defenders lose their local browser keys, the organization owner can use their offline recovery key to decrypt historical report envelopes and re-wrap session keys for newly assigned defenders.

### 2.4 Key Synchronization & Concurrency Protocol (`recipient_set_version`)
To prevent race conditions when team members join or leave while reports are in transit:
1. **Keyring Versioning**: Every program maintains an integer `recipient_set_version` counter in PostgreSQL.
2. **Key Retrieval**: When opening a report form or reply box, the browser retrieves:
   ```json
   {
     "program_id": "prog_123",
     "recipient_set_version": 4,
     "public_keys": [
       { "key_id": "F7B2C109E45A12D8", "armored_public_key": "-----BEGIN PGP..." },
       { "key_id": "3A81D92C4B7E55F1", "armored_public_key": "-----BEGIN PGP..." }
     ],
     "recovery_public_key": "-----BEGIN PGP..."
   }
   ```
3. **Submission Guard**: Submissions send the payload envelope alongside `recipient_set_version`.
4. **Stale Keyring Rejection**: If the server detects that the program's `recipient_set_version` has incremented, the submission is rejected with `409 Conflict: STALE_RECIPIENT_SET`. The client fetches the updated keyring and prompts the user to re-encrypt before retrying.

### 2.5 Dual-Lane Recipient Isolation
The platform enforces strict cryptographic separation between collaborative researcher dialogue and internal security analysis:
* **Lane 1: Collaborative Triage & Retest Thread**: Encrypted with symmetric key $K_S$, wrapped for the **Researcher (or Report Key) + Program Defenders + Org Recovery Key**.
* **Lane 2: Internal Review Notes & Remediation Triage**: Encrypted with symmetric key $K_S$, wrapped **strictly for Program Defenders + Org Recovery Key**. The researcher's public key is completely excluded from the envelope, ensuring external submitters cannot decrypt internal comments even if database records are exposed.

### 2.6 Historical-Access Isolation & Audited Session Key Re-Wrapping
* **Historical-Access Isolation**: A newly onboarded defender receives access only to future submissions and replies. They do not possess past keys and cannot decrypt reports submitted prior to their assignment.
* **Audited Session Key Re-Wrapping**: When a new defender requires access to a historical report:
  1. An existing authorized defender (or org owner using the recovery key) opens the report in their browser and unlocks their private key.
  2. The browser decrypts the symmetric session key ($K_S$) in local memory.
  3. The browser re-wraps $K_S$ with the new defender's public key using standard OpenPGP PKESK packet generation (`openpgp.js`).
  4. The client transmits the new PKESK packet to the server, which appends it to the stored message envelope.
  5. The server records an immutable audit event: `HISTORICAL_ACCESS_GRANTED` (`grantor_id`, `recipient_id`, `report_id`, `timestamp`).
* **Member Offboarding**: When a defender is removed, the program's `recipient_set_version` increments. All subsequent report submissions and future replies in existing threads exclude the offboarded member's public key.

---

## 3. Data Boundary: Server-Visible Metadata vs. Client-Encrypted Fields

| Data Field | Storage Format | Visibility | System Purpose & Security Risk |
| :--- | :--- | :--- | :--- |
| **Report Reference ID** | Text (`#BBT-xxx`) | Server-Visible Plaintext | Ticket routing, audit trail correlation. Low risk. |
| **Program & Target Asset** | UUID & Text (`api.example.com`) | Server-Visible Plaintext | Program scope validation. Reveals target surface. |
| **Operational Category Enum**| Enum (`AUTHENTICATION_BYPASS`, etc.) | Server-Visible Plaintext | Queue filtering and SLA triage. Reveals vulnerability type. |
| **CVSS 3.1 Vector & Score** | Text & Decimal (`9.8 Critical`) | Server-Visible Plaintext | SLA routing and dashboard prioritization. Reveals severity. |
| **Lifecycle State** | Enum (`ACCEPTED`, `RETEST_PENDING`, etc.) | Server-Visible Plaintext | State machine enforcement. Reveals remediation status. |
| **VCS Fix Reference** | SHA-1 / SHA-256 Commit Hash | Server-Visible Plaintext | Automated commit existence and branch verification. |
| **Vulnerability Title & PoC**| Text (`pgp_armored`) | Client-Encrypted Ciphertext | Detailed exploit mechanics. Fully confidential. |
| **Reproduction Steps** | Text (`pgp_armored`) | Client-Encrypted Ciphertext | Step-by-step exploit reproduction. Fully confidential. |
| **Thread Messages & Replies**| Text (`pgp_armored`) | Client-Encrypted Ciphertext | Triage conversation and patch advice. Fully confidential. |
| **Internal Review Notes** | Text (`pgp_armored`) | Client-Encrypted Ciphertext | Defender-only notes (excludes hunter key). Fully confidential. |
| **Evidence Attachments** | Binary (`pgp_armored` in R2) | Client-Encrypted Ciphertext | PoC scripts, PCAP traces, HAR logs. Fully confidential. |

### Minimal-Metadata Notification Policy
To prevent notification emails from leaking exploit characteristics or vulnerable assets:
* External email notifications sent via transactional email (Postmark/Resend API) default strictly to:
  * **Subject**: `[BugBountyTrack] Status Update on Report #BBT-104`
  * **Body**: `A new message or state change occurred on report #BBT-104. Log in to your encrypted portal to view details: https://app.bugbountytrack.com/reports/104`
* Exploit titles, CWE categories, target domain names, and reproduction snippets are strictly excluded from automated emails.

---

## 4. Key Lifecycle & Storage Model

1. **Passphrase Separation**:
   * **Login Password**: Authenticates against the server (hashed using Argon2id / bcrypt, 12 rounds).
   * **Encryption Passphrase**: Retained strictly on client devices, never transmitted to the server. Unlocks local OpenPGP Argon2 S2K encrypted `IndexedDB` key storage.
2. **Disaster Recovery via Offline Master Key**:
   * In individual key loss scenarios, other active defenders retain access.
   * If all local devices are wiped, the organization owner applies the **Offline Master Recovery Key** to re-seed access.
   * No server-side key escrow or plaintext reset mechanism exists.
3. **Direct-to-Storage Presigned Attachment Uploads**:
   * Client-side encrypted files (up to 25 MB) are uploaded directly to Cloudflare R2 via presigned URLs, bypassing the 4.5 MB Vercel serverless request body ceiling.

---

## 5. Security Model & Explicit Trust Assumptions

1. **Delivered Code & Key Distribution Trust Assumption**:
   Client-side cryptography isolates sensitive exploit payloads from backend database compromises, cloud snapshot theft, and untrusted database administrators. However, **the platform assumes that the delivered client web application (HTML/JS) and the server's public-key distribution endpoint are untampered**. Client-side cryptography cannot protect against a malicious platform operator who alters the delivered JavaScript or substitutes public keys during retrieval.
2. **Platform Hardening**:
   To minimize the risk of client-side code modification or XSS injection, the application enforces:
   * Strict Content Security Policy (`script-src 'self'`) blocking third-party scripts.
   * Subresource Integrity (SRI) on all bundled static chunks.
   * AST-based Markdown sanitization neutralizing HTML tags and embedded scripts inside code blocks.
3. **Client-Side Rendering Safety**:
   Decrypted vulnerability payloads and proof-of-concept code are rendered exclusively inside inert syntax-highlighted code blocks using client-side AST tokenizers. The raw plaintext is never injected via `dangerouslySetInnerHTML`.
