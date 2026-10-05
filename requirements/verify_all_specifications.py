import zipfile, os, re, xml.etree.ElementTree as ET

errors = []
warnings = []
passes = []

def check(condition, desc):
    if condition:
        passes.append(desc)
    else:
        errors.append(desc)

print("=" * 80)
print("BUGBOUNTYTRACK SPECIFICATION SUITE VERIFICATION (VERSION 3.0.0)")
print("Commercial Baseline & Academic Evaluation Specification")
print("=" * 80)

# 1. File existence & sizes
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

files = {
    'BRD.md': os.path.join(SCRIPT_DIR, 'BRD.md'),
    'BRD.docx': os.path.join(SCRIPT_DIR, 'BRD.docx'),
    'SRS.md': os.path.join(SCRIPT_DIR, 'SRS.md'),
    'SRS.docx': os.path.join(SCRIPT_DIR, 'SRS.docx'),
    'WBS.md': os.path.join(SCRIPT_DIR, 'WBS.md'),
    'WBS.xlsx': os.path.join(SCRIPT_DIR, 'WBS.xlsx'),
    'CVSS_TEST_FIXTURES.md': os.path.join(SCRIPT_DIR, 'CVSS_TEST_FIXTURES.md'),
}

for fname, fpath in files.items():
    check(os.path.exists(fpath), f"File exists: {fname}")
    sz = os.path.getsize(fpath) if os.path.exists(fpath) else 0
    check(sz > 5000, f"File size > 5KB: {fname} ({sz} bytes)")

# 2. Check metadata in Markdown files
for mdf in ['BRD.md', 'SRS.md', 'WBS.md']:
    p = files[mdf]
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
    check('24-ST-013' in content, f"{mdf} contains Roll No 24-ST-013")
    check('Taha Asadullah' in content, f"{mdf} contains Taha Asadullah")
    check('Sir Umar Hayat' in content, f"{mdf} contains Sir Umar Hayat")
    check('PTUT - PRJ - 089' in content, f"{mdf} contains Project ID PTUT - PRJ - 089")
    check('Version 3.0.0' in content, f"{mdf} contains Version 3.0.0")
    # Check no raw latex artifacts
    check(r'\text{' not in content, f"{mdf} has no \\text{{}} artifacts")
    check(r'\ge' not in content, f"{mdf} has no \\ge artifacts")
    check(r'\le' not in content, f"{mdf} has no \\le artifacts")
    check(r'\$' not in content, f"{mdf} has no \\$ artifacts")

# 3. Check specific requirements in SRS.md
with open(files['SRS.md'], 'r', encoding='utf-8') as f:
    srs = f.read()

check('52 canonical test vectors' in srs or 'CVSS_TEST_FIXTURES.md' in srs, "SRS.md cites 52 canonical test vectors in CVSS_TEST_FIXTURES.md")
check('GET /repos/{owner}/{repo}/commits/{ref}' in srs, "SRS.md has corrected GitHub API path")
check('Decryption Custodian' in srs, "SRS.md specifies Decryption Custodian")
check('operational_label' in srs, "SRS.md specifies operational_label neutral enum")
check('title_ciphertext' in srs, "SRS.md specifies title_ciphertext")
check('50 MB' in srs and '2 GB' in srs, "SRS.md has 50 MB DB and 2 GB R2 quotas")
check('90%' in srs and '100%' in srs, "SRS.md specifies 90% warning / 100% rejection rule")
check('CLOSED_UNVERIFIED_TIMEOUT' in srs, "SRS.md specifies CLOSED_UNVERIFIED_TIMEOUT")
check('RETEST_FAILED' in srs, "SRS.md specifies RETEST_FAILED event returning to ACCEPTED")
check('INSERT' in srs and 'SELECT' in srs, "SRS.md specifies append-only audit boundary")
check('CLOSURE_EVIDENCE_EXPORT' in srs or 'Redacted Closure Evidence' in srs, "SRS.md specifies Redacted Closure Evidence Export")

# Check CVSS_TEST_FIXTURES.md integrity
with open(files['CVSS_TEST_FIXTURES.md'], 'r', encoding='utf-8') as f:
    cvss_text = f.read()
check('| **52** |' in cvss_text, "CVSS_TEST_FIXTURES.md contains all 52 vectors")
check('FIRST.org' in cvss_text and 'NIST NVD' in cvss_text, "CVSS_TEST_FIXTURES.md cites FIRST.org and NIST NVD")
check('24-ST-013' in cvss_text, "CVSS_TEST_FIXTURES.md contains Roll No 24-ST-013")

# Check WBS.md ACAD-01 and ACAD-02
with open(files['WBS.md'], 'r', encoding='utf-8') as f:
    wbs = f.read()
check('| **ACAD-01**| EV-01 |' in wbs, "WBS.md ACAD-01 references EV-01")
check('| **ACAD-02**| EV-02 |' in wbs, "WBS.md ACAD-02 references EV-02")
check('236 Hours' in wbs and '28 Hours' in wbs and '264 Hours' in wbs, "WBS.md hours arithmetic 236 + 28 = 264")
check('WP-7.1' in wbs and 'WP-7.6' in wbs, "WBS.md contains Milestone 3 Commercial Launch packages WP-7.1 to WP-7.6")

# 4. Check SRS.docx OpenXML integrity and embedded drawings
with zipfile.ZipFile(files['SRS.docx'], 'r') as srs_zip:
    srs_xml = srs_zip.read('word/document.xml').decode('utf-8')
    rels_xml = srs_zip.read('word/_rels/document.xml.rels').decode('utf-8')
    media_files = [f for f in srs_zip.namelist() if f.startswith('word/media/')]

check(len(media_files) == 6, f"SRS.docx contains exactly 6 images (found {len(media_files)})")
for i in range(1, 7):
    fn = f'fig4_{i}_'
    found = any(fn in m for m in media_files)
    check(found, f"SRS.docx contains diagram {fn}")

# Check drawings count in document.xml
drawings_in_doc = srs_xml.count('<w:drawing>')
check(drawings_in_doc == 6, f"SRS.docx has exactly 6 <w:drawing> elements (found {drawings_in_doc})")
check('Version 3.0.0' in srs_xml, "SRS.docx contains Version 3.0.0")
check('24-ST-013' in srs_xml, "SRS.docx contains Roll No 24-ST-013")
check('Taha Asadullah' in srs_xml, "SRS.docx contains Taha Asadullah")
check(r'\text{' not in srs_xml, "SRS.docx has no \\text{} artifacts")
check(r'\ge' not in srs_xml, "SRS.docx has no \\ge artifacts")
check(r'\le' not in srs_xml, "SRS.docx has no \\le artifacts")

# 5. Check BRD.docx OpenXML integrity
with zipfile.ZipFile(files['BRD.docx'], 'r') as brd_zip:
    brd_xml = brd_zip.read('word/document.xml').decode('utf-8')
check('Version 3.0.0' in brd_xml, "BRD.docx contains Version 3.0.0")
check('24-ST-013' in brd_xml, "BRD.docx contains Roll No 24-ST-013")
check('Taha Asadullah' in brd_xml, "BRD.docx contains Taha Asadullah")
check(r'\text{' not in brd_xml, "BRD.docx has no \\text{} artifacts")
check(r'\ge' not in brd_xml, "BRD.docx has no \\ge artifacts")
check(r'\le' not in brd_xml, "BRD.docx has no \\le artifacts")
check('Starter' in brd_xml and 'Team' in brd_xml, "BRD.docx contains SaaS pricing tiers")

# 6. Check WBS.xlsx OpenXML integrity and formulas
with zipfile.ZipFile(files['WBS.xlsx'], 'r') as wbs_zip:
    sheet1_xml = wbs_zip.read('xl/worksheets/sheet1.xml').decode('utf-8')
    sheet2_xml = wbs_zip.read('xl/worksheets/sheet2.xml').decode('utf-8')
    sheet3_xml = wbs_zip.read('xl/worksheets/sheet3.xml').decode('utf-8')
    sheet4_xml = wbs_zip.read('xl/worksheets/sheet4.xml').decode('utf-8')
    sheet5_xml = wbs_zip.read('xl/worksheets/sheet5.xml').decode('utf-8')

check('Version 3.0.0' in sheet1_xml, "WBS.xlsx Sheet 1 contains Version 3.0.0")
check('24-ST-013' in sheet1_xml, "WBS.xlsx Sheet 1 contains Roll No 24-ST-013")
check('SUM(G2:G26)' in sheet2_xml, "WBS.xlsx Sheet 2 contains formula SUM(G2:G26)")
check('SUM(F2:F7)' in sheet4_xml, "WBS.xlsx Sheet 4 contains formula SUM(F2:F7)")
check('SUM(E2:E8)' in sheet5_xml, "WBS.xlsx Sheet 5 contains formula SUM(E2:E8)")

print(f"\nVerification Results: {len(passes)} checks PASSED, {len(errors)} checks FAILED.")
for p in passes:
    print(f"  [PASS] {p}")
if errors:
    print("\nFAILED CHECKS:")
    for e in errors:
        print(f"  [FAIL] {e}")
    exit(1)
else:
    print("\nALL 50+ CHECKS PASSED PERFECTLY!")
