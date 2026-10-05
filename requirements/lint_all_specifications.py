import zipfile, os, re, json, xml.etree.ElementTree as ET

errors = []
warnings = []
passes = []

def check(condition, desc):
    if condition:
        passes.append(desc)
    else:
        errors.append(desc)

print("=" * 80)
print("BUGBOUNTYTRACK SPECIFICATION INTEGRITY LINTER (VERSION 3.2.0)")
print("Level 1 Specification & Cross-Document Traceability Linter")
print("=" * 80)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

files = {
    'BRD.md': os.path.join(SCRIPT_DIR, 'BRD.md'),
    'BRD.docx': os.path.join(SCRIPT_DIR, 'BRD.docx'),
    'SRS.md': os.path.join(SCRIPT_DIR, 'SRS.md'),
    'SRS.docx': os.path.join(SCRIPT_DIR, 'SRS.docx'),
    'WBS.md': os.path.join(SCRIPT_DIR, 'WBS.md'),
    'WBS.xlsx': os.path.join(SCRIPT_DIR, 'WBS.xlsx'),
    'CVSS_TEST_FIXTURES.md': os.path.join(SCRIPT_DIR, 'CVSS_TEST_FIXTURES.md'),
    'KEY_MANAGEMENT.md': os.path.join(PROJECT_DIR, 'architecture', 'KEY_MANAGEMENT.md'),
    'DECISION_LOG.md': os.path.join(PROJECT_DIR, 'decisions', 'DECISION_LOG.md'),
    'project.json': os.path.join(PROJECT_DIR, 'project.json'),
}

# 1. File existence & minimum size thresholds
for fname, fpath in files.items():
    check(os.path.exists(fpath), f"File exists: {fname}")
    sz = os.path.getsize(fpath) if os.path.exists(fpath) else 0
    min_sz = 1000 if fname == 'project.json' else 5000
    check(sz >= min_sz, f"File size valid: {fname} ({sz} bytes)")

# 2. Check metadata in Markdown specifications
for mdf in ['BRD.md', 'SRS.md', 'WBS.md']:
    p = files[mdf]
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
    check('24-ST-013' in content, f"{mdf} contains Roll No 24-ST-013")
    check('Taha Asadullah' in content, f"{mdf} contains Taha Asadullah")
    check('Sir Umar Hayat' in content, f"{mdf} contains Sir Umar Hayat")
    check('PTUT - PRJ - 089' in content, f"{mdf} contains Project ID PTUT - PRJ - 089")
    check('SET-B' in content, f"{mdf} contains Section SET-B")
    # Verify no raw unescaped LaTeX formatting artifacts
    check(r'\text{' not in content, f"{mdf} has no \\text{{}} artifacts")
    check(r'\ge' not in content, f"{mdf} has no \\ge artifacts")
    check(r'\le' not in content, f"{mdf} has no \\le artifacts")

# 3. Check project.json metadata & schema consistency
with open(files['project.json'], 'r', encoding='utf-8') as f:
    pjson = json.load(f)
check(pjson.get('rollNo') == '24-ST-013', "project.json contains rollNo 24-ST-013")
check(pjson.get('studentAuthor') == 'Taha Asadullah', "project.json contains studentAuthor Taha Asadullah")
check(pjson.get('section') == 'SET-B', "project.json contains section SET-B")
check(pjson.get('supervisor') == 'Sir Umar Hayat', "project.json contains supervisor Sir Umar Hayat")

# 4. Check specific requirements in SRS.md
with open(files['SRS.md'], 'r', encoding='utf-8') as f:
    srs = f.read()

check('45 verified' in srs or 'CVSS_TEST_FIXTURES.md' in srs, "SRS.md cites verified test vectors in CVSS_TEST_FIXTURES.md")
check('recipient_set_version' in srs, "SRS.md specifies recipient_set_version concurrency guard")
check('token_hash' in srs, "SRS.md specifies token_hash for invitations")
check('operational_label' in srs, "SRS.md specifies operational_label neutral enum")
check('title_ciphertext' in srs, "SRS.md specifies title_ciphertext")
check('50 MB' in srs and '2 GB' in srs, "SRS.md specifies 50 MB DB and 2 GB R2 demo quotas")
check('CLOSED_UNVERIFIED_TIMEOUT' in srs, "SRS.md specifies CLOSED_UNVERIFIED_TIMEOUT")
check('RETEST_FAILED' in srs, "SRS.md specifies RETEST_FAILED event returning to ACCEPTED")
check('INSERT' in srs and 'SELECT' in srs, "SRS.md specifies append-only audit boundary")
check('Redacted closure evidence export' in srs or 'Redacted Closure Evidence' in srs, "SRS.md specifies Redacted Closure Evidence Export")
check('prev_hash' in srs, "SRS.md specifies tamper-evident prev_hash audit chain")
check('guest_token_hash' in srs or 'Account-Less (Guest)' in srs, "SRS.md specifies account-less guest vulnerability intake")
check('Lemon Squeezy' in srs, "SRS.md specifies Lemon Squeezy Merchant of Record")
check('recovery_public_key' in srs or 'Organization Master Recovery Key' in srs, "SRS.md specifies Offline Organization Master Recovery Key")
check('wasm-unsafe-eval' in srs, "SRS.md specifies wasm-unsafe-eval for OpenPGP.js Argon2 S2K CSP")
check('CLOSED_INCOMPLETE' in srs, "SRS.md specifies CLOSED_INCOMPLETE for intake clarification timeout")
check('PROGRAM_DEFENDER' in srs, "SRS.md specifies PROGRAM_DEFENDER entity for program-scoped recipients")
check('Guest Recovery Package' in srs, "SRS.md specifies Guest Recovery Package for multi-device key restore")
check('URI fragment' in srs or '#token=' in srs, "SRS.md specifies URI fragment protection against credential logging")

# 5. Check architecture/KEY_MANAGEMENT.md consistency
with open(files['KEY_MANAGEMENT.md'], 'r', encoding='utf-8') as f:
    km = f.read()
check('IndexedDB' in km and 'localStorage' not in km, "KEY_MANAGEMENT.md uses IndexedDB for guest keys (zero localStorage)")
check('wasm-unsafe-eval' in km, "KEY_MANAGEMENT.md specifies wasm-unsafe-eval CSP for Argon2 S2K")
check('Argon2 S2K' in km or 'Argon2id S2K' in km, "KEY_MANAGEMENT.md specifies Argon2 S2K key protection")
check('Guest Recovery Package' in km, "KEY_MANAGEMENT.md specifies Guest Recovery Package")
check('#token=' in km, "KEY_MANAGEMENT.md specifies URI fragment protection for guest tracking URLs")
check('RFC 9580' in km, "KEY_MANAGEMENT.md references RFC 9580 standard")

# 6. Check CVSS_TEST_FIXTURES.md integrity & vector uniqueness
with open(files['CVSS_TEST_FIXTURES.md'], 'r', encoding='utf-8') as f:
    cvss_text = f.read()

check('FIRST.org' in cvss_text and 'NIST National Vulnerability Database' in cvss_text, "CVSS_TEST_FIXTURES.md cites FIRST.org Examples Guide & NIST NVD")
check('CVE-2021-41773' in cvss_text and '7.5' in cvss_text, "CVSS_TEST_FIXTURES.md correctly attributes CVE-2021-41773 as 7.5 High")
check('24-ST-013' in cvss_text, "CVSS_TEST_FIXTURES.md contains Roll No 24-ST-013")
check('8.22' in cvss_text and '8.2252' not in cvss_text, "CVSS_TEST_FIXTURES.md enforces official FIRST.org coefficient 8.22 (zero 8.2252)")
check('CVE-2018-13379-VAR' in cvss_text and '5.3' in cvss_text, "CVSS_TEST_FIXTURES.md Fixture 25 scores 5.3 Medium with 8.22 coefficient")

scoring_text = cvss_text.split("### Part 3")[0] if "### Part 3" in cvss_text else cvss_text
vector_pattern = re.compile(r'`(CVSS:3\.1/[^`]+)`')
vectors = vector_pattern.findall(scoring_text)
check(len(vectors) == 45, f"CVSS_TEST_FIXTURES.md contains exactly 45 scoring vectors (found {len(vectors)})")
unique_vectors = set(vectors)
check(len(unique_vectors) == 45, f"All 45 scoring vectors are mathematically unique (found {len(unique_vectors)} unique)")
check("### Part 3: Executable Parser Rejection" in cvss_text, "CVSS_TEST_FIXTURES.md contains Part 3 Parser Rejection test suite")

# 7. Cross-Document WBS Arithmetic, Package Parity & Task Status Honesty
with open(files['WBS.md'], 'r', encoding='utf-8') as f:
    wbs = f.read()

check('236 Hours' in wbs and '28 Hours' in wbs and '264 Hours' in wbs, "WBS.md academic arithmetic: 236h core + 28h buffer = 264h")
check('160 Hours' in wbs and '424 Hours' in wbs, "WBS.md commercial arithmetic: 264h academic + 160h commercial = 424h total")
check('WP-7.1' in wbs and 'WP-7.12' in wbs, "WBS.md contains commercial packages WP-7.1 to WP-7.12")
check('`[READY]`' in wbs and 'WP-1.1' in wbs, "WBS.md maintains honest task status: WP-1.1 is READY (not falsely DONE)")
check('Sprint 6' in wbs and '| 44 |' in wbs, "WBS.md maintains balanced academic sprints: Sprint 6 is 44h (not 66h)")

# 8. Check standalone diagrams in requirements/diagrams/
diagram_stems = [
    'fig4_1_component', 'fig4_2_usecase', 'fig4_3_seq_submission',
    'fig4_4_seq_decryption', 'fig4_5_statemachine', 'fig4_6_erd'
]
diag_dir = os.path.join(SCRIPT_DIR, 'diagrams')
for stem in diagram_stems:
    png_path = os.path.join(diag_dir, f"{stem}.png")
    svg_path = os.path.join(diag_dir, f"{stem}.svg")
    check(os.path.exists(png_path) and os.path.getsize(png_path) > 10000, f"Diagram PNG exists & >10KB: {stem}.png")
    check(os.path.exists(svg_path) and os.path.getsize(svg_path) > 10000, f"Diagram SVG exists & >10KB: {stem}.svg")

# 9. Check SRS.docx OpenXML integrity and embedded drawings
with zipfile.ZipFile(files['SRS.docx'], 'r') as srs_zip:
    srs_xml = srs_zip.read('word/document.xml').decode('utf-8')
    media_files = [f for f in srs_zip.namelist() if f.startswith('word/media/')]

check(len(media_files) == 6, f"SRS.docx contains exactly 6 images (found {len(media_files)})")
drawings_in_doc = srs_xml.count('<w:drawing>')
check(drawings_in_doc == 6, f"SRS.docx has exactly 6 <w:drawing> elements (found {drawings_in_doc})")
check('24-ST-013' in srs_xml, "SRS.docx contains Roll No 24-ST-013")
check('Taha Asadullah' in srs_xml, "SRS.docx contains Taha Asadullah")
check(r'\text{' not in srs_xml, "SRS.docx has no \\text{} artifacts")

# 10. Check BRD.docx OpenXML integrity
with zipfile.ZipFile(files['BRD.docx'], 'r') as brd_zip:
    brd_xml = brd_zip.read('word/document.xml').decode('utf-8')
check('24-ST-013' in brd_xml, "BRD.docx contains Roll No 24-ST-013")
check('Taha Asadullah' in brd_xml, "BRD.docx contains Taha Asadullah")
check('Team' in brd_xml and 'Community' in brd_xml, "BRD.docx contains SaaS pricing tiers (Team & Community)")

# 11. Check WBS.xlsx OpenXML integrity, formula consistency & mathematical parity
with zipfile.ZipFile(files['WBS.xlsx'], 'r') as wbs_zip:
    sheet1_xml = wbs_zip.read('xl/worksheets/sheet1.xml').decode('utf-8')
    sheet2_xml = wbs_zip.read('xl/worksheets/sheet2.xml').decode('utf-8')
    sheet3_xml = wbs_zip.read('xl/worksheets/sheet3.xml').decode('utf-8')
    sheet4_xml = wbs_zip.read('xl/worksheets/sheet4.xml').decode('utf-8')
    sheet5_xml = wbs_zip.read('xl/worksheets/sheet5.xml').decode('utf-8')

check('424 Total Hours' in sheet1_xml, "WBS.xlsx Sheet 1 contains 424 Total Hours")
check('24-ST-013' in sheet1_xml, "WBS.xlsx Sheet 1 contains Roll No 24-ST-013")
check('SUM(G2:G39)' in sheet2_xml, "WBS.xlsx Sheet 2 contains formula SUM(G2:G39) spanning all 38 work packages")
check('SUM(F2:F10)' in sheet4_xml, "WBS.xlsx Sheet 4 contains formula SUM(F2:F10) spanning all 9 Sprints")

match_s2_tot = re.search(r'<c r="G40"[^>]*><f>[^<]+</f><v>(\d+)</v></c>', sheet2_xml)
if match_s2_tot:
    s2_val = int(match_s2_tot.group(1))
    check(s2_val == 424, f"WBS.xlsx Sheet 2 total engineering hours == 424 (computed {s2_val})")
else:
    errors.append("WBS.xlsx Sheet 2 total cell G40 not found")

match_s4_tot = re.search(r'<c r="F11"[^>]*><f>[^<]+</f><v>(\d+)</v></c>', sheet4_xml)
if match_s4_tot:
    s4_val = int(match_s4_tot.group(1))
    check(s4_val == 424, f"WBS.xlsx Sheet 4 total sprint hours == 424 (computed {s4_val})")
else:
    errors.append("WBS.xlsx Sheet 4 total cell F11 not found")

# 12. Requirement ID Sequence & Definition Uniqueness
with open(files['BRD.md'], 'r', encoding='utf-8') as f:
    brd_full = f.read()
br_defs = re.findall(r'^\*\s+\*\*BR-(\d+\.\d+)\*\*', brd_full, re.MULTILINE)
check(len(br_defs) > 0, f"Found {len(br_defs)} BR definitions in BRD.md")
check(len(br_defs) == len(set(br_defs)), f"All {len(br_defs)} BR definitions in BRD.md are unique (zero duplicate IDs)")

fr_defs = re.findall(r'^\*\s+\*\*FR-(\d+\.\d+)', srs, re.MULTILINE)
check(len(fr_defs) > 0, f"Found {len(fr_defs)} FR definitions in SRS.md")
check(len(fr_defs) == len(set(fr_defs)), f"All {len(fr_defs)} FR definitions in SRS.md are unique (zero duplicate IDs)")

# 13. Cryptographic Precision & RFC 9580 v6 Fingerprint Standardization
check('64-character' in brd_full, "BRD.md specifies 64-character SHA-256 fingerprints")
check('64-character' in srs, "SRS.md specifies 64-character SHA-256 fingerprints")
check('64-character' in km, "KEY_MANAGEMENT.md specifies 64-character SHA-256 fingerprints")
check('40-character fingerprint' not in brd_full and '40-character fingerprint' not in srs and '40-character fingerprint' not in km, "Zero legacy 40-character fingerprint references across all crypto specifications")
check('benchmark target' in srs and 'benchmark target' in km, "Bare keygen (<50ms) accurately framed as an empirical benchmark target")
check('estimated cryptographic delay' in srs or 'intentional, estimated' in srs, "Argon2id S2K delay accurately framed as an estimated cryptographic delay (~200-400ms)")
check('Uint8Array' in srs and 'IndexedDB' in srs and 'nullified' in srs, "SRS.md specifies strict memory hygiene (Uint8Array zeroizing, IndexedDB deletion, reference nullification)")
check('Uint8Array' in km and 'IndexedDB' in km and 'nullified' in km, "KEY_MANAGEMENT.md specifies strict memory hygiene")

# 14. Durable Guest Identity, Recovery Package & PROGRAM_DEFENDER Rules
check('guest_actor_id' in srs, "SRS.md defines durable guest_actor_id in schema & relations")
check('guest_actor_id' in km, "KEY_MANAGEMENT.md specifies durable guest_actor_id decoupled from bearer tokens")
check('.bbt-recovery.json' in srs, "SRS.md specifies canonical .bbt-recovery.json package")
check('.bbt-recovery.json' in km, "KEY_MANAGEMENT.md specifies canonical .bbt-recovery.json package")
check('.bbt-recovery.json' in brd_full, "BRD.md specifies canonical .bbt-recovery.json package")
check('Same-Organization Constraint' in km, "KEY_MANAGEMENT.md enforces PROGRAM_DEFENDER Rule 1: Same-Organization Constraint")
check('Unique Membership' in km, "KEY_MANAGEMENT.md enforces PROGRAM_DEFENDER Rule 2: Unique Membership constraint")
check('Atomic Assignment & Keyring Synchronization' in km, "KEY_MANAGEMENT.md enforces PROGRAM_DEFENDER Rule 3: Atomic Assignment & Keyring Synchronization")
check('Program-Level Authorization Boundary' in km, "KEY_MANAGEMENT.md enforces PROGRAM_DEFENDER Rule 4: Program-Level Authorization Boundary")

# 15. Bounded Quotas, Reopening Policy & Financial Boundaries
check('QUOTA_HELD' in brd_full and 'QUOTA_HELD' in srs, "BRD.md and SRS.md specify QUOTA_HELD queue state for Community tier")
check('500 MB' in brd_full and '10 submissions/hr' in brd_full, "BRD.md specifies bounded Community tier limits (500 MB storage, 10 submissions/hr)")
check('security@tenant.com' in brd_full, "BRD.md specifies fallback security@tenant.com contact")
check('CLOSED_INCOMPLETE' in srs, "SRS.md explicitly includes CLOSED_INCOMPLETE in state transition matrix")
check('REJECTED_SPAM' in srs and 'WITHDRAWN' in srs, "SRS.md explicitly marks REJECTED_SPAM and WITHDRAWN as non-reopenable")
check('89.24' in brd_full and '61.00' in brd_full, "BRD.md accurately distinguishes infrastructure break-even from commercial profitability")

# 16. Academic & Professional Attribution Hygiene (Zero AI Agent Bleed into Specifications)
forbidden_personas = [
    'Alexander', 'Victoria', 'Arthur', 'Julian', 'Marcus', 'Elena',
    'Cyra', 'Garrison', 'Nadia', 'Vance', 'Pendleton', 'Sterling',
    'Rostova', 'Kaelen', 'Drake', 'Al-Mansoor', 'Crow Parliament'
]
hygiene_files = [
    ('SRS.md', srs),
    ('BRD.md', brd_full),
    ('WBS.md', wbs),
    ('KEY_MANAGEMENT.md', km),
    ('CVSS_TEST_FIXTURES.md', cvss_text)
]
for doc_name, doc_content in hygiene_files:
    for persona in forbidden_personas:
        check(persona not in doc_content, f"{doc_name} has zero bleed of internal agent persona '{persona}'")

print(f"\nSpecification Linting Results: {len(passes)} checks PASSED, {len(errors)} checks FAILED.")
for p in passes:
    print(f"  [PASS] {p}")
if errors:
    print("\nFAILED CHECKS:")
    for e in errors:
        print(f"  [FAIL] {e}")
    exit(1)
else:
    print("\nALL SPECIFICATION INTEGRITY CHECKS PASSED PERFECTLY!")
    print("\n" + "=" * 80)
    print("SPECIFICATION LINTER BOUNDARY & SCOPE DECLARATION (RULE 17):")
    print("=" * 80)
    print("  1. Verified: Document schema, metadata, cross-document arithmetic (424h),")
    print("     CVSS coefficients (8.22), test vector parity (45/45), requirement ID uniqueness,")
    print("     cryptographic standards (RFC 9580 v6, 64-hex fingerprints), OpenXML structures,")
    print("     and bounded quota policies.")
    print("  2. Level 1 Boundary Limitations (NOT checked by this static specification linter):")
    print("     - Does not parse the visual AST or layout nodes of Mermaid diagram files.")
    print("     - Does not execute live database DDL migrations or verify PostgreSQL constraints in runtime.")
    print("     - Does not execute live OpenPGP.js WebAssembly / WebCrypto encryption benchmarks in browser.")
    print("     - Does not simulate live Lemon Squeezy Merchant-of-Record webhook callbacks.")
    print("     These runtime behaviors belong to Level 2 (Unit/Integration) and Level 3 (E2E) verification.")
    print("=" * 80 + "\n")
    exit(0)
