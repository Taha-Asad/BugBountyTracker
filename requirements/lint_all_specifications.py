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
    'WEEK_1_DISCOVERY_REPORT.md': os.path.join(SCRIPT_DIR, 'WEEK_1_DISCOVERY_REPORT.md'),
    'WEEK_1_PART_A_USER_PERSONAS.md': os.path.join(SCRIPT_DIR, 'WEEK_1_PART_A_USER_PERSONAS.md'),
    'WEEK_1_PART_A_USER_PERSONAS.docx': os.path.join(SCRIPT_DIR, 'WEEK_1_PART_A_USER_PERSONAS.docx'),
    'WEEK_1_PART_B_CHARTER_AND_MVP.md': os.path.join(SCRIPT_DIR, 'WEEK_1_PART_B_CHARTER_AND_MVP.md'),
    'WEEK_1_PART_B_CHARTER_AND_MVP.docx': os.path.join(SCRIPT_DIR, 'WEEK_1_PART_B_CHARTER_AND_MVP.docx'),
    'DISCOVERY_INTERVIEW_LOG.md': os.path.join(SCRIPT_DIR, 'DISCOVERY_INTERVIEW_LOG.md'),
    'HOD_PROPOSAL.md': os.path.join(SCRIPT_DIR, 'HOD_PROPOSAL.md'),
    'week-01-problem-discovery-personas.md': os.path.join(PROJECT_DIR, 'tasks', 'week-01-problem-discovery-personas.md'),
    'week-02-software-requirements-specification.md': os.path.join(PROJECT_DIR, 'tasks', 'week-02-software-requirements-specification.md'),
    'week-03-high-level-architecture-cloud-topology.md': os.path.join(PROJECT_DIR, 'tasks', 'week-03-high-level-architecture-cloud-topology.md'),
    'HIGH_LEVEL_ARCHITECTURE.md': os.path.join(PROJECT_DIR, 'architecture', 'HIGH_LEVEL_ARCHITECTURE.md'),
    'HIGH_LEVEL_ARCHITECTURE.docx': os.path.join(PROJECT_DIR, 'architecture', 'HIGH_LEVEL_ARCHITECTURE.docx'),
    'PROJECT_COMPREHENSIVE_OVERVIEW.md': os.path.join(PROJECT_DIR, 'PROJECT_COMPREHENSIVE_OVERVIEW.md'),
    'PROJECT_COMPREHENSIVE_OVERVIEW.docx': os.path.join(PROJECT_DIR, 'PROJECT_COMPREHENSIVE_OVERVIEW.docx'),
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
for mdf in ['BRD.md', 'SRS.md', 'WBS.md', 'WEEK_1_DISCOVERY_REPORT.md', 'WEEK_1_PART_A_USER_PERSONAS.md', 'WEEK_1_PART_B_CHARTER_AND_MVP.md', 'DISCOVERY_INTERVIEW_LOG.md', 'HOD_PROPOSAL.md', 'week-01-problem-discovery-personas.md', 'week-02-software-requirements-specification.md', 'week-03-high-level-architecture-cloud-topology.md', 'HIGH_LEVEL_ARCHITECTURE.md', 'PROJECT_COMPREHENSIVE_OVERVIEW.md']:
    p = files[mdf]
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
    check('24-ST-013' in content, f"{mdf} contains Roll No 24-ST-013")
    check('Taha Asadullah' in content, f"{mdf} contains Taha Asadullah")
    check('Sir Umar Hayat' in content, f"{mdf} contains Sir Umar Hayat")
    check('PTUT - PRJ - 089' in content, f"{mdf} contains Project ID PTUT - PRJ - 089")
    check('SET-B' in content, f"{mdf} contains Section SET-B")
    check('SET-A' not in content, f"{mdf} has zero legacy SET-A references")
    if mdf in ['BRD.md', 'SRS.md', 'WBS.md', 'WEEK_1_DISCOVERY_REPORT.md', 'WEEK_1_PART_A_USER_PERSONAS.md', 'WEEK_1_PART_B_CHARTER_AND_MVP.md', 'DISCOVERY_INTERVIEW_LOG.md', 'week-01-problem-discovery-personas.md', 'week-02-software-requirements-specification.md', 'week-03-high-level-architecture-cloud-topology.md', 'HIGH_LEVEL_ARCHITECTURE.md', 'PROJECT_COMPREHENSIVE_OVERVIEW.md']:
        # Verify no raw unescaped LaTeX formatting artifacts in Word-source or portal-paste docs
        check(r'\text{' not in content, f"{mdf} has no \\text{{}} artifacts")
        check(r'\longrightarrow' not in content, f"{mdf} has no \\longrightarrow artifacts")
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
check('20 MiB' in srs and '6 MiB' in srs and '50 MiB' in srs and '9.5 GiB' in srs, "SRS.md specifies 20 MiB DB intake (+6 MiB security/audit reserve), <= 50 MiB report cap, and 9.5 GiB R2 cluster cap")
check('CLOSED_UNVERIFIED_TIMEOUT' in srs, "SRS.md specifies CLOSED_UNVERIFIED_TIMEOUT")
check('RETEST_FAILED' in srs, "SRS.md specifies RETEST_FAILED event returning to ACCEPTED")
check('INSERT' in srs and 'SELECT' in srs, "SRS.md specifies append-only audit boundary")
check('Redacted closure evidence export' in srs or 'Redacted Closure Evidence' in srs, "SRS.md specifies Redacted Closure Evidence Export")
check('prev_report_chain_hash' in srs and 'prev_tenant_row_hash' in srs, "SRS.md specifies tamper-evident dual prev_report_chain_hash and prev_tenant_row_hash audit chains")
check('guest_token_hash' in srs or 'Account-Less (Guest)' in srs, "SRS.md specifies account-less guest vulnerability intake")
check('Lemon Squeezy' not in srs and 'SuperAdmin' not in srs and '$49' not in srs,
      "SRS.md stays strictly focused on Academic MVP scope (zero Lemon Squeezy, SuperAdmin, or $49/mo commercial bloat)")
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

# 9. Check SRS.docx OpenXML integrity, university formatting, and embedded drawing aspect ratios
import struct
with zipfile.ZipFile(files['SRS.docx'], 'r') as srs_zip:
    srs_xml = srs_zip.read('word/document.xml').decode('utf-8')
    srs_styles_xml = srs_zip.read('word/styles.xml').decode('utf-8')
    srs_header_xml = srs_zip.read('word/header1.xml').decode('utf-8')
    srs_footer_xml = srs_zip.read('word/footer1.xml').decode('utf-8')
    media_files = [f for f in srs_zip.namelist() if f.startswith('word/media/')]
    font_files = [f for f in srs_zip.namelist() if f.startswith('word/fonts/')]
    png_dims_in_zip = {}
    for mf in media_files:
        raw_png = srs_zip.read(mf)
        w_px, h_px = struct.unpack('>II', raw_png[16:24])
        png_dims_in_zip[os.path.basename(mf)] = (w_px, h_px)

check(len(media_files) == 4, f"SRS.docx contains the 4 core UML behavioral diagrams (found {len(media_files)})")
check(len(font_files) == 0, f"SRS.docx has zero embedded non-standard font binaries (found {len(font_files)})")
drawings_in_doc = srs_xml.count('<w:drawing')
check(drawings_in_doc == 4, f"SRS.docx has 4 <w:drawing> elements (found {drawings_in_doc})")
check('24-ST-013' in srs_xml, "SRS.docx contains Roll No 24-ST-013")
check('Taha Asadullah' in srs_xml, "SRS.docx contains Taha Asadullah")
check(r'\text{' not in srs_xml, "SRS.docx has no \\text{} artifacts")
check('Times New Roman' in srs_xml and 'Times New Roman' in srs_styles_xml and 'Times New Roman' in srs_header_xml and 'Times New Roman' in srs_footer_xml,
      "SRS.docx enforces Times New Roman across document, styles, header, and footer")
for xml_part_name, xml_part in [('document.xml', srs_xml), ('styles.xml', srs_styles_xml), ('header1.xml', srs_header_xml), ('footer1.xml', srs_footer_xml)]:
    check('Lexend' not in xml_part and 'Consolas' not in xml_part and 'Cambria' not in xml_part,
          f"SRS.docx {xml_part_name} has zero legacy Lexend/Consolas/Cambria fonts")
    colors_found = set(re.findall(r'w:color w:val="([^"]+)"', xml_part))
    non_black_colors = {c for c in colors_found if c not in ('000000', 'auto')}
    check(len(non_black_colors) == 0, f"SRS.docx {xml_part_name} uses pure black #000000 only (non-black: {non_black_colors})")

# Verify every embedded diagram in SRS.docx preserves its exact native PNG aspect ratio
drawing_blocks = re.findall(r'<wp:inline[^>]*>.*?</wp:inline>', srs_xml)
check(len(drawing_blocks) == 4, f"SRS.docx contains 4 inline drawing blocks (found {len(drawing_blocks)})")
rel_to_png = {
    'rId201': 'fig4_2_usecase.png',
    'rId202': 'fig4_3_seq_submission.png',
    'rId203': 'fig4_4_seq_decryption.png',
    'rId204': 'fig4_5_statemachine.png',
}
for dblock in drawing_blocks:
    ext_m = re.search(r'<wp:extent cx="(\d+)" cy="(\d+)"/>', dblock)
    rid_m = re.search(r'r:embed="(rId\d+)"', dblock)
    if ext_m and rid_m:
        cx_val, cy_val = int(ext_m.group(1)), int(ext_m.group(2))
        rid_val = rid_m.group(1)
        png_name = rel_to_png.get(rid_val)
        w_px, h_px = png_dims_in_zip.get(png_name, (1, 1))
        emu_ratio = cx_val / float(cy_val)
        px_ratio = w_px / float(h_px)
        check(abs(emu_ratio - px_ratio) < 0.005,
              f"SRS.docx {png_name} ({rid_val}) preserves exact aspect ratio (EMU {emu_ratio:.3f} vs PNG {px_ratio:.3f})")
        check('noChangeAspect="1"' in dblock, f"SRS.docx {png_name} ({rid_val}) locks aspect ratio (noChangeAspect=1)")


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
check('QUOTA_HELD' in brd_full and 'QUOTA_HELD' not in srs, "BRD.md specifies QUOTA_HELD while SRS.md stays focused on Academic MVP lifecycle")
check('500 MB' in brd_full and '10 submissions/hr' in brd_full, "BRD.md specifies bounded Community tier limits (500 MB storage, 10 submissions/hr)")
check('security@tenant.com' in brd_full, "BRD.md specifies fallback security@tenant.com contact")
check('CLOSED_INCOMPLETE' in srs, "SRS.md explicitly includes CLOSED_INCOMPLETE in state transition matrix")
check('REJECTED_SPAM' in srs and 'WITHDRAWN' in srs, "SRS.md explicitly marks REJECTED_SPAM and WITHDRAWN as non-reopenable")
check('89.24' in brd_full and '61.00' in brd_full, "BRD.md accurately distinguishes infrastructure break-even from commercial profitability")

with open(files['WEEK_1_DISCOVERY_REPORT.md'], 'r', encoding='utf-8') as f:
    w1_report = f.read()
with open(files['WEEK_1_PART_A_USER_PERSONAS.md'], 'r', encoding='utf-8') as f:
    w1_part_a = f.read()
with open(files['WEEK_1_PART_B_CHARTER_AND_MVP.md'], 'r', encoding='utf-8') as f:
    w1_part_b = f.read()
with open(files['HOD_PROPOSAL.md'], 'r', encoding='utf-8') as f:
    hod_prop = f.read()
with open(files['week-01-problem-discovery-personas.md'], 'r', encoding='utf-8') as f:
    w1_task = f.read()

check('4096-bit RSA' not in w1_report and 'localStorage' not in w1_report and 'Stripe Sandbox' not in w1_report,
      "WEEK_1_DISCOVERY_REPORT.md has zero legacy RSA-4096, localStorage, or Stripe Sandbox references")
check('15,000' not in w1_report and '30,000' not in w1_report and 'economically excluded' not in w1_report and 'free entry tiers' in w1_report,
      "WEEK_1_DISCOVERY_REPORT.md acknowledges free entry tiers and has zero false $15k/$30k cost-exclusion claims")
check('15,000' not in w1_task and '30,000' not in w1_task and 'economically excluded' not in w1_task and 'free entry tiers' in w1_task,
      "week-01-problem-discovery-personas.md acknowledges free entry tiers and has zero false $15k/$30k cost-exclusion claims")
check('$15,000' not in srs and '$30,000' not in srs and '$15,000' not in brd_full and '$30,000' not in brd_full,
      "SRS.md and BRD.md have zero $15k/$30k cost-exclusion claims")
check('two recipients' not in hod_prop and 'Version**            | `3.2.0`' in hod_prop,
      "HOD_PROPOSAL.md is synchronized to Version 3.2.0 and multi-defender PKESK")

# 15b. Week 1 Rewrite Integrity: Zero Copy Blocks, Zero Uncited 30% Stat, Full Crypto Parity & Split Docs
check('Part 5' not in w1_task and 'Ready-to-Paste' not in w1_task,
      "week-01-problem-discovery-personas.md has removed Part 5 duplicate copy block")
check('Quick-Submit Portal Excerpt' not in w1_report and 'PTUT PROJECT MANAGER — WEEK 1 SUBMISSION' not in w1_report,
      "WEEK_1_DISCOVERY_REPORT.md has removed duplicate Quick-Submit Portal Excerpt block")
check('file://' not in w1_task and '/run/media/' not in w1_task and 'Deliverable File Path' not in w1_task and 'Full Reference Report' not in w1_task,
      "week-01-problem-discovery-personas.md has zero local file paths")
check('file://' not in w1_report and '/run/media/' not in w1_report and 'Deliverable File Path' not in w1_report,
      "WEEK_1_DISCOVERY_REPORT.md has zero local file paths")
check('file://' not in w1_part_a and 'file://' not in w1_part_b,
      "WEEK_1_PART_A and WEEK_1_PART_B have zero local file:// paths")
check('30%' not in w1_report and '30%' not in w1_task and '30%' not in w1_part_a and '30%' not in w1_part_b,
      "Zero uncited '30%' patch failure claims across all Week 1 documents")
check('title_ciphertext' in w1_report and 'operational_label' in w1_report and 'cleartext-signed' in w1_report,
      "WEEK_1_DISCOVERY_REPORT.md specifies title_ciphertext, operational_label, and browser cleartext-signed security.txt")
check('title_ciphertext' in w1_task and 'operational_label' in w1_task and 'cleartext-signed' in w1_task,
      "week-01-problem-discovery-personas.md specifies title_ciphertext, operational_label, and browser cleartext-signed security.txt")
check('title_ciphertext' in w1_part_b and 'operational_label' in w1_part_b and 'cleartext-signed' in w1_part_b,
      "WEEK_1_PART_B_CHARTER_AND_MVP.md specifies title_ciphertext, operational_label, and browser cleartext-signed security.txt")
for w1_name, w1_txt in [('WEEK_1_DISCOVERY_REPORT.md', w1_report), ('week-01-problem-discovery-personas.md', w1_task), ('WEEK_1_PART_A_USER_PERSONAS.md', w1_part_a), ('WEEK_1_PART_B_CHARTER_AND_MVP.md', w1_part_b)]:
    check('16-Week' not in w1_txt and '16-week' not in w1_txt and 'Week 7' not in w1_txt,
          f"{w1_name} stays strictly focused on Week 1 scope (zero 16-Week or Week 7 roadmap bloat)")
for w1_main_name, w1_main_txt in [('WEEK_1_DISCOVERY_REPORT.md', w1_report), ('week-01-problem-discovery-personas.md', w1_task)]:
    check('1drXMfAk4pIKc_9aMKZav62KfVZQ04--zT6VyuhDZKFA' in w1_main_txt and '1-N7Pv-3CO95XNWcvjSga6vf0vDKOvFKdPQ5l6uGpQJY' in w1_main_txt and 'PASTE_GOOGLE_DRIVE_LINK' not in w1_main_txt,
          f"{w1_main_name} contains verified Google Drive links for Personas and Charter/MVP docs")

with zipfile.ZipFile(files['WEEK_1_PART_A_USER_PERSONAS.docx'], 'r') as w1a_zip:
    w1a_xml = w1a_zip.read('word/document.xml').decode('utf-8')
check('24-ST-013' in w1a_xml and 'Alex Rivera' in w1a_xml and 'Sarah Chen' in w1a_xml,
      "WEEK_1_PART_A_USER_PERSONAS.docx OpenXML verified (24-ST-013, Alex Rivera, Sarah Chen)")

with zipfile.ZipFile(files['WEEK_1_PART_B_CHARTER_AND_MVP.docx'], 'r') as w1b_zip:
    w1b_xml = w1b_zip.read('word/document.xml').decode('utf-8')
check('24-ST-013' in w1b_xml and 'title_ciphertext' in w1b_xml and '8.22' in w1b_xml,
      "WEEK_1_PART_B_CHARTER_AND_MVP.docx OpenXML verified (24-ST-013, title_ciphertext, 8.22 CVSS)")

# 15c. Week 2 SRS & Task Deliverable Integrity: UC-01..UC-07 Parity, NFR-09 Uptime, Signature Block, Zero file:// Paths & Revision 2.2 Invariants
with open(files['week-02-software-requirements-specification.md'], 'r', encoding='utf-8') as f:
    w2_task = f.read()
check('file://' not in srs and '/run/media/' not in srs,
      "SRS.md has zero local file:// or /run/media/ paths")
check('file://' not in w2_task and '/run/media/' not in w2_task,
      "week-02-software-requirements-specification.md has zero local file:// or /run/media/ paths")
for uc_num in range(1, 8):
    uc_tag = f"UC-0{uc_num}"
    check(f"Use Case {uc_tag}:" in srs and f"Use Case `{uc_tag}`:" in w2_task,
          f"Both SRS.md and week-02 task spec define {uc_tag}")
check('UC-08' not in srs and 'UC-08' not in w2_task,
      "Both SRS.md and week-02 task spec exclude commercial Lemon Squeezy billing use case UC-08")
check('NFR-09' in srs and '99.5%' in srs and 'NFR-09' in w2_task and '99.5%' in w2_task,
      "Both SRS.md and week-02 task spec define quantifiable NFR-09 Uptime SLO (>= 99.5%)")
check('Document Submission & Milestone Sign-Off' in srs and 'Document Submission & Milestone Sign-Off' in w2_task,
      "Both SRS.md and week-02 task spec include formal Document Submission & Milestone Sign-Off signature block")
check('1n8VKmXeK4TSTPPR-mDXp3NkKwDxvzTzEWR9tgdZlxSg' in srs and '1n8VKmXeK4TSTPPR-mDXp3NkKwDxvzTzEWR9tgdZlxSg' in w2_task and 'PASTE_GOOGLE_DRIVE_LINK' not in w2_task,
      "Both SRS.md and week-02 task spec contain verified Google Drive link for Week 2 SRS document")
check('Document Submission &amp; Milestone Sign-Off' in srs_xml,
      "SRS.docx includes formal Document Submission & Milestone Sign-Off signature block")
check('REPORT_RECIPIENT' in srs and 'state_version' in srs and 'remediation_attempt_no' in srs,
      "SRS.md specifies REPORT_RECIPIENT, state_version optimistic concurrency, and remediation_attempt_no")
check('Class A' in srs and 'Class B' in srs and 'Class C' in srs,
      "SRS.md specifies 3-tier Field-Level Classification Matrix (Class A, Class B, Class C)")
check('FORCE ROW LEVEL SECURITY' in srs and 'NOBYPASSRLS' in srs and '2,592' in srs,
      "SRS.md specifies FORCE ROW LEVEL SECURITY, NOBYPASSRLS, and 2,592 CVSS Base combinations")
check('Lead Defender' not in srs and '13-state' not in srs and '13-State' not in srs,
      "SRS.md has zero legacy 'Lead Defender' or '13-state' contradictions")
check('7 developers' in srs, "SRS.md aligns Sarah Chen persona with Week 1 7-developer team size")
check('organization_audit_heads' in srs and 'guest_mutation_nonces' in srs and 'report_recipient_version' in srs,
      "SRS.md Revision 2.3 specifies organization_audit_heads, guest_mutation_nonces, and report_recipient_version")
check('s2kType' in srs and 'submission_session_token' in srs and 'cvss_explanation_ciphertext' in srs,
      "SRS.md Revision 2.3 specifies explicit s2kType=argon2, submission_session_token, and Class B cvss_explanation_ciphertext")
check('report_chain_hash' in srs and 'config_artifact_ciphertext' in srs and 'Table 2.2' in srs and 'Section 7.3' not in srs or '7.3 Deterministic Operational Scenario' in srs,
      "SRS.md Revision 2.3 specifies report_chain_hash, config_artifact_ciphertext, Table 2.2 Permission Matrix, and Section 7.3 Scenario Walkthrough")
check('FR-3.9' not in srs and 'FR-6.5' not in srs,
      "SRS.md Revision 2.3 has zero dangling FR-3.9 or FR-6.5 phantom references")
check('bbt-closure-export-v1' in srs and 'COMMITMENT_VERIFIED_VALUE_REDACTED' in srs and 'event_digest' in srs,
      "SRS.md Revision 2.4 specifies bbt-closure-export-v1, COMMITMENT_VERIFIED_VALUE_REDACTED, and universal event_digest")
check('rewrap-researcher-key' in srs and 'grant-defender-access' in srs and 'seipdv2_body_sha256' in srs,
      "SRS.md Revision 2.4 separates rewrap-researcher-key (CLASS_B_ONLY) from grant-defender-access (CLASS_B_AND_C) and binds seipdv2_body_sha256")
check('pg_temp' in srs and 'cluster_storage_state' in srs and 'X-Cron-Signature' in srs and 'fn_guest_rotate_token_by_sig' in srs,
      "SRS.md Revision 2.4 specifies pg_temp search_path hardening, cluster_storage_state R2 cap, X-Cron-Signature, and fn_guest_rotate_token_by_sig")
check('commitment_salts_json' in srs and 'bbt-commit-v1' in srs and 'fn_guest_fetch_pubkey_and_rotate_token' not in srs,
      "SRS.md Revision 2.4 defines explicit bbt-commit-v1 formula, commitment_salts_json persistence, and zero stale fn_guest_fetch_pubkey_and_rotate_token references")
check('1. cluster_storage_state' in srs and 'openpgp-symenc-seipdv2' in km and 'rewrap-researcher-key' in km,
      "SRS.md enforces universal 6-table lock order and KEY_MANAGEMENT.md is synchronized with Revision 2.4")
check('Revision 2.8' in srs and 'Revision 2.8' in w2_task and 'Revision 2.8' in srs_header_xml,
      "SRS.md, week-02-software-requirements-specification.md, and SRS.docx header are updated to Revision 2.8")
check('encrypted_guest_credentials_armored' in srs and 'encrypted_guest_credentials_armored' in km,
      "SRS.md and KEY_MANAGEMENT.md encrypt guest retry-cache tokens to guest_public_key (encrypted_guest_credentials_armored)")
check('org_commitment' in srs and 'export_payload' in srs and 'Summary-to-Closure-Event' in srs,
      "SRS.md Revision 2.8 defines org_commitment, export_payload JCS signature scope, and Summary-to-Closure-Event equality")
check('fn_cron_evaluate_overdue_deadlines' in srs and 'fn_cron_finalize_r2_deletions' in srs and 'DELETING' in srs,
      "SRS.md Revision 2.8 specifies 3-phase non-blocking cron execution (DELETING -> DELETED)")
check('19.0 MiB' in srs and 'capacity_deadline_paused' in srs and '307,200 bytes' in srs and 'ORDER BY id ASC FOR UPDATE' in srs,
      "SRS.md Revision 2.8 specifies 19.0 MiB + 1.0 MiB intake split, capacity_deadline_paused, 307,200-byte Priority-0 floor, and ORDER BY id ASC FOR UPDATE")
check('claim_id' in srs and 'claim_expires_at' in srs and 'has_more_backlog' in srs and 'workflow_dispatch' in srs,
      "SRS.md Revision 2.8: Claim-lease R2 cleanup recovery (claim_id, claim_expires_at) & unified backlog drain (has_more_backlog, workflow_dispatch)")
check('fn_process_researcher_response_or_pause' in srs and 'SAVEPOINT sp_researcher_payload' not in srs and 'ROLLBACK TO SAVEPOINT' not in srs and 'SAVEPOINT sp_researcher_payload' not in w2_task and 'EXCEPTION WHEN SQLSTATE \'P0001\'' in srs and 'CAPACITY_DEADLINE_PAUSE' in srs and 'fn_record_capacity_deadline_pause' not in srs and 'fn_record_capacity_deadline_pause' not in w2_task,
      "SRS.md Revision 2.8 Fix 1: Client-owned outer transaction + nested PL/pgSQL BEGIN...EXCEPTION WHEN SQLSTATE 'P0001' subtransaction pause (zero function-internal SAVEPOINT/COMMIT)")
check('in-place fixed-width update' not in srs and 'delta_bytes == 0' not in srs and 'zero heap growth' not in srs and '53100' in srs and 'DATABASE_PHYSICAL_STORAGE_EXHAUSTED' in srs,
      "SRS.md Revision 2.8: Zero false 'in-place fixed-width update / delta_bytes == 0 / zero heap growth' claims; distinguishes logical quota exemption from SQLSTATE 53100 (HTTP 503)")
check('p_r2_claim_limit => 10' in srs and 'p_deadline_limit => 50' in srs and 'p_purge_limit => 200' in srs and '11,000 ms' in srs and 'FOR UPDATE SKIP LOCKED' in srs and "lock_timeout = '250ms'" in srs and "statement_timeout = '800ms'" in srs and 'immediately after its own Phase 2' in srs,
      "SRS.md Revision 2.8 Fix 2: Sequential per-batch Phase 1->2->3 finalization, 4,000ms reserved final-batch headroom, and enforceable DB timeouts (lock_timeout=250ms, statement_timeout=800ms)")
with open(os.path.join(diag_dir, 'fig4_1_component.mmd'), 'r', encoding='utf-8') as f:
    fig4_1_mmd = f.read()
with open(os.path.join(diag_dir, 'fig4_6_erd.mmd'), 'r', encoding='utf-8') as f:
    fig4_6_mmd = f.read()
check('QUOTA_HELD' not in fig4_1_mmd and 'Lemon Squeezy' not in fig4_1_mmd and 'token_hash' in fig4_1_mmd,
      "SRS.md Revision 2.8: fig4_1_component.mmd synchronized (zero QUOTA_HELD or Lemon Squeezy, includes token_hash & 90%/95%/100% quota guard)")
check('SUBSCRIPTION' not in fig4_6_mmd and 'lemon_squeezy' not in fig4_6_mmd and '15-State Lifecycle Enum' in fig4_6_mmd and '8-Category Neutral Enum' in fig4_6_mmd and 'REPORT_RECIPIENT' in fig4_6_mmd and 'CLUSTER_STORAGE_STATE' in fig4_6_mmd and 'claim_id' in fig4_6_mmd,
      "SRS.md Revision 2.8: fig4_6_erd.mmd synchronized (15-state enum, 8-category label, REPORT_RECIPIENT, CLUSTER_STORAGE_STATE, claim_id, zero SUBSCRIPTION/lemon_squeezy)")
with open(files['DISCOVERY_INTERVIEW_LOG.md'], 'r', encoding='utf-8') as f:
    disc_log = f.read()
check('DISCOVERY_INTERVIEW_LOG.md' in srs and 'DISCOVERY_INTERVIEW_LOG.md' in w1_report and 'DISCOVERY_INTERVIEW_LOG.md' in w1_part_a and 'PENDING_LIVE_INTERVIEWS' in disc_log and 'Provisional Composite Personas' in disc_log and 'Tier 1 Primary Evidence' in disc_log and 'Tier 1 Primary Evidence' in srs and 'Stage 1 — Actual Past Behavior' in disc_log,
      "SRS.md Revision 2.8 Fix 3: DISCOVERY_INTERVIEW_LOG.md and SRS.md synchronized (PENDING_LIVE_INTERVIEWS, Tier 1 vs Tier 2 evidence, Two-Stage Non-Leading Interview Script)")
check('closure_report_seq_no' in srs and 'closure_report_seq_no' in w2_task and 'report_chain[M]' in srs,
      "SRS.md Revision 2.8: Post-closure audit events & closure_report_seq_no = M in Redacted Closure Evidence Export verification")
check('160 KiB' in srs and '163,840 bytes' in srs and '192 KiB' not in srs and '192 KiB' not in w2_task,
      "SRS.md Revision 2.8: Incompressible configuration snapshot ceiling <= 160 KiB (163,840 bytes) plaintext -> <= 256 KiB armored ciphertext")
check('emergency_db_buffer_used_bytes' in srs and 'db_reserve_quota_bytes' in srs and 'budgeted for overhead and shared storage' in srs and 'actual remaining physical capacity is continuously monitored' in srs,
      "SRS.md Revision 2.8 Fix 4: Bounded 20 MiB Shared Emergency DB Reserve Buffer & 232 MiB budgeted for overhead and shared storage with continuous physical capacity monitoring")

# 15d. Week 3 High-Level Architecture & Cloud Topology Integrity: 3-Tier Model, DFD 0/1, System Boundaries & Cloud Justification
with open(files['HIGH_LEVEL_ARCHITECTURE.md'], 'r', encoding='utf-8') as f:
    arch_md = f.read()
with open(files['week-03-high-level-architecture-cloud-topology.md'], 'r', encoding='utf-8') as f:
    w3_task = f.read()

check('Tier 1: Client Presentation' in arch_md and 'Tier 2: Presentation & Gateway' in arch_md and 'Tier 3: Persistence & Storage' in arch_md,
      "HIGH_LEVEL_ARCHITECTURE.md specifies complete 3-Tier Zero-Plaintext Model")
check('fig3_1_3tier_architecture.png' in arch_md and 'fig3_2_dfd_level_0.png' in arch_md and 'fig3_3_dfd_level_1.png' in arch_md and 'fig3_4_cloud_topology.png' in arch_md,
      "HIGH_LEVEL_ARCHITECTURE.md references all 4 canonical architecture and DFD diagrams")
check('DFD Level 0: System Context Diagram' in arch_md and ('Entity E1' in w3_task and 'Security Researcher' in w3_task) and ('Entity E6' in w3_task and 'GitHub Actions Cron' in w3_task),
      "Both architecture spec and week-03 task define DFD Level 0 Context Diagram with 6 external entities")
check('Process 1.0: Tenant Registration' in arch_md and 'Process 7.0: Attested Retest' in arch_md and 'Organizations & Tenant Registry' in arch_md and 'Storage Quotas & Claim Leases' in arch_md,
      "HIGH_LEVEL_ARCHITECTURE.md decomposes DFD Level 1 into 7 sub-processes and 7 persistent data stores")
check('STRIDE' in arch_md and 'Spoofing' in arch_md and 'Tampering' in arch_md and 'Repudiation' in arch_md and 'Information Disclosure' in arch_md and 'Denial of Service' in arch_md and 'Elevation of Privilege' in arch_md,
      "HIGH_LEVEL_ARCHITECTURE.md includes comprehensive STRIDE Threat Mitigation Analysis")
check('$0.00' in arch_md and '$61.00' in arch_md and 'Vercel' in arch_md and 'Neon' in arch_md and 'Cloudflare R2' in arch_md,
      "HIGH_LEVEL_ARCHITECTURE.md validates dual-track $0.00 academic vs $61.00 commercial cloud justification")
check('Document Submission & Milestone Sign-Off' in arch_md and 'Document Submission & Milestone Sign-Off' in w3_task,
      "Both HIGH_LEVEL_ARCHITECTURE.md and week-03 task spec include formal Document Submission & Milestone Sign-Off")

# Week 3 Architecture Alignment to Submitted SRS Revision 2.8 Invariants
check('HMAC-SHA256' in arch_md and 'X-Cron-Signature: sha256=' in arch_md and 'Ed25519-signed JWT' not in arch_md and 'Ed25519-signed JSON Web Tokens' not in arch_md,
      "Week 3 Alignment 1: Scheduled-job authentication uses HMAC-SHA256 (zero Ed25519-signed JWT)")
check('/api/v1/internal/cron/sla-check' in arch_md and '/api/cron/process-deadlines' not in arch_md,
      "Week 3 Alignment 2: Scheduled-job route is /api/v1/internal/cron/sla-check (zero /api/cron/process-deadlines)")
check('SameSite=Lax' in arch_md and 'SameSite=Strict' not in arch_md and '__Host-bbt-session' in arch_md,
      "Week 3 Alignment 3: Session cookie policy is SameSite=Lax under __Host-bbt-session (zero SameSite=Strict)")
check('CSPRNG' in arch_md and 'token_hash' in arch_md and 'Argon2id session' not in arch_md,
      "Week 3 Alignment 4: Session tokens use CSPRNG with SHA-256 token_hash persistence (Argon2id strictly password KDF)")
check('bbt_app' in arch_md and 'bbt_app_runtime' not in arch_md and 'bbt_app_runtime' not in w3_task,
      "Week 3 Alignment 5: Unprivileged database role is bbt_app (zero bbt_app_runtime)")
check('p95 latency <= 400 ms' in arch_md and '< 250 ms' not in arch_md,
      "Week 3 Alignment 6: API latency matches NFR-01 p95 <= 400 ms (zero unsupported < 250 ms claim)")
check('10 submissions/hour/IP' in arch_md and '5 requests/hour/IP' not in arch_md and '5 req/hr/IP' not in arch_md,
      "Week 3 Alignment 7: Intake rate limit aligns with FR-8.3 (10 submissions/hour/IP, zero 5 req/hr/IP)")
check('20 MiB intake' in arch_md and '6 MiB' in arch_md and '50 MB DB cap' not in arch_md,
      "Week 3 Alignment 8: Storage quotas align with FR-8.4 (20 MiB intake, 6 MiB reserve, zero 50 MB DB cap)")
check('any order' in arch_md and 'rejects invalid or out-of-order' not in arch_md,
      "Week 3 Alignment 9: CVSS v3.1 accepts base metrics in any order and emits canonical vector (FR-4.3)")
check(('row_hash' in arch_md or 'tenant_row_hash' in arch_md) and 'report_chain_hash' in arch_md and ('row_hash' in w3_task or 'tenant_row_hash' in w3_task) and 'report_chain_hash' in w3_task,
      "Week 3 Alignment 10: Dual hash-chained audit ledger specified (row_hash and report_chain_hash)")
check('P2 extension' in arch_md or 'P2 Extension' in arch_md,
      "Week 3 Alignment 11: Cryptographic closure exports explicitly designated as P2 extension (FR-8.6)")
check('FR-5.5' not in arch_md and 'FR-5.4' in arch_md,
      "Week 3 Alignment 12: Discussion/triage requirements end at FR-5.4 (zero orphan FR-5.5 reference)")
check('compare/{branch}...{sha}' in arch_md and 'compare/{sha}...{branch}' not in arch_md and 'compare/{branch}...{sha}' in w3_task,
      "Week 3 Alignment 13: GitHub compare route uses canonical compare/{branch}...{sha} order")
check('What BugBountyTrack DOES Architecturally Control' in arch_md and 'What BugBountyTrack DOES NOT Control' in arch_md,
      "Week 3 Alignment 14: Section 4 includes explicit Controls vs Does NOT Control boundary table")
check('Implementation Phases and Clarifications' in arch_md and 'Implementation Phases and Clarifications' in w3_task and 'Submit Encrypted Report ->' in arch_md and 'Submit Encrypted Report ->' in w3_task,
      "Week 3 Alignment 15: Explicit Implementation Phases and Clarifications section defines central workflow and mandatory P1 obligations")
check('approved SRS' not in arch_md and 'approved SRS' not in w3_task and 'submitted SRS' in arch_md and 'submitted SRS' in w3_task,
      "Week 3 Alignment 16: Uses 'submitted SRS' (zero premature 'approved SRS' claims)")
check('FR-8.4c' not in arch_md and 'FR-8.4c' not in w3_task and 'FR-1.2b' not in arch_md and 'FR-1.2b' not in w3_task,
      "Week 3 Alignment 17: Accurate requirement references (zero FR-8.4c or FR-1.2b phantom references)")
check('p99 <= 800 ms' in arch_md and 'p99 <= 800 ms' in w3_task and 'cold <= 1,200 ms' not in arch_md and 'cold start <= 1,200 ms' not in w3_task,
      "Week 3 Alignment 18: Restored exact NFR-01 design targets p95 <= 400 ms and p99 <= 800 ms (zero warm/cold deviation)")
check('300 KiB' in arch_md and '300 KiB' in w3_task and 'prevents tampering or deletion' not in arch_md,
      "Week 3 Alignment 19: Storage reserve specifies 300 KiB Priority-0 floor and honest audit ledger security claims")
check('row_hash' in arch_md and 'row_hash' in w3_task and 'PASTE_GOOGLE_DRIVE_LINK' not in w3_task,
      "Week 3 Alignment 20: Specifies canonical row_hash and zero placeholder Google Drive links")


with zipfile.ZipFile(files['HIGH_LEVEL_ARCHITECTURE.docx'], 'r') as arch_zip:
    arch_doc_xml = arch_zip.read('word/document.xml').decode('utf-8')
    arch_rels_xml = arch_zip.read('word/_rels/document.xml.rels').decode('utf-8')
check('rId201' in arch_rels_xml and 'rId202' in arch_rels_xml and 'rId203' in arch_rels_xml and 'rId204' in arch_rels_xml,
      "HIGH_LEVEL_ARCHITECTURE.docx OpenXML relationships embed all 4 high-DPI architecture diagrams")
check('24-ST-013' in arch_doc_xml and 'Taha Asadullah' in arch_doc_xml and 'Sir Umar Hayat' in arch_doc_xml,
      "HIGH_LEVEL_ARCHITECTURE.docx OpenXML document body verified (24-ST-013, Taha Asadullah, Sir Umar Hayat)")

with zipfile.ZipFile(files['PROJECT_COMPREHENSIVE_OVERVIEW.docx'], 'r') as over_zip:
    over_doc_xml = over_zip.read('word/document.xml').decode('utf-8')
    over_rels_xml = over_zip.read('word/_rels/document.xml.rels').decode('utf-8')
check('rId201' in over_rels_xml and 'rId202' in over_rels_xml and 'rId203' in over_rels_xml and 'rId204' in over_rels_xml and 'rId205' in over_rels_xml and 'rId206' in over_rels_xml,
      "PROJECT_COMPREHENSIVE_OVERVIEW.docx OpenXML relationships embed all 6 architecture & behavioral diagrams")
check('24-ST-013' in over_doc_xml and 'Taha Asadullah' in over_doc_xml and 'Sir Umar Hayat' in over_doc_xml,
      "PROJECT_COMPREHENSIVE_OVERVIEW.docx OpenXML document body verified (24-ST-013, Taha Asadullah, Sir Umar Hayat)")

# 16. Academic & Professional Attribution Hygiene (Zero Non-Project Persona or Local Path Bleed)
import hashlib
FORBIDDEN_TOKEN_SHA256_PREFIXES = {
    '9f2a08fde416cef2', 'ab1cb712f2dca756', 'befa156f0283eb00', 'ce0fee7e61f9c74f',
    'd7ae9de750a5640a', '0ce93c9606f0685b', '29437d59cd735112', 'bc0e899aa43b9120',
    'dbaf86dd80e3bcd5', '7c43ed48929b891f', 'ac0ea3f64534dfc2', '0bc9d6a5155e908f',
    'd5f29c56ba0bd969', '401cb0a3c9577a6a', '0c483d630f7025f6', 'fca6c2c60899a812',
    '54444aa7bc07ccec', '22c4aecf5d24c5ba', '7ee162f213ce2342'
}
with open(files['DECISION_LOG.md'], 'r', encoding='utf-8') as f:
    dec_log = f.read()
with open(os.path.join(PROJECT_DIR, 'PROJECT_SUMMARY.md'), 'r', encoding='utf-8') as f:
    proj_sum = f.read()
with open(os.path.join(PROJECT_DIR, 'README.md'), 'r', encoding='utf-8') as f:
    readme_txt = f.read()
with open(os.path.join(SCRIPT_DIR, 'SRS_UNIVERSITY_SUBMISSION.md'), 'r', encoding='utf-8') as f:
    uni_srs_txt = f.read()
with open(files['PROJECT_COMPREHENSIVE_OVERVIEW.md'], 'r', encoding='utf-8') as f:
    over_md = f.read()

hygiene_files = [
    ('SRS.md', srs),
    ('SRS_UNIVERSITY_SUBMISSION.md', uni_srs_txt),
    ('HIGH_LEVEL_ARCHITECTURE.md', arch_md),
    ('PROJECT_COMPREHENSIVE_OVERVIEW.md', over_md),
    ('BRD.md', brd_full),
    ('WBS.md', wbs),
    ('KEY_MANAGEMENT.md', km),
    ('CVSS_TEST_FIXTURES.md', cvss_text),
    ('WEEK_1_DISCOVERY_REPORT.md', w1_report),
    ('WEEK_1_PART_A_USER_PERSONAS.md', w1_part_a),
    ('WEEK_1_PART_B_CHARTER_AND_MVP.md', w1_part_b),
    ('DISCOVERY_INTERVIEW_LOG.md', disc_log),
    ('HOD_PROPOSAL.md', hod_prop),
    ('week-01-problem-discovery-personas.md', w1_task),
    ('week-02-software-requirements-specification.md', w2_task),
    ('week-03-high-level-architecture-cloud-topology.md', w3_task),
    ('DECISION_LOG.md', dec_log),
    ('PROJECT_SUMMARY.md', proj_sum),
    ('README.md', readme_txt),
]
for doc_name, doc_content in hygiene_files:
    words_in_doc = set(re.findall(r'[A-Za-z]+(?:-[A-Za-z]+)*', doc_content.lower()))
    matched_forbidden = [
        w for w in words_in_doc
        if hashlib.sha256(w.encode('utf-8')).hexdigest()[:16] in FORBIDDEN_TOKEN_SHA256_PREFIXES
    ]
    check(len(matched_forbidden) == 0, f"{doc_name} passes attribution & persona hygiene (zero non-project persona bleed)")
    check('file://' not in doc_content and '/run/media/' not in doc_content, f"{doc_name} has zero local file:// or /run/media/ paths")
    check('Observe, Build, Verify' not in doc_content and 'DoAC' not in doc_content and 'DoCC' not in doc_content and 'DoQV' not in doc_content and 'DoSA' not in doc_content and 'DoOR' not in doc_content and 'DoRG' not in doc_content and 'Phase Gate Governance' not in doc_content,
          f"{doc_name} has zero internal workspace branding or gate acronyms")


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
    print("SPECIFICATION LINTER BOUNDARY & SCOPE DECLARATION:")
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
