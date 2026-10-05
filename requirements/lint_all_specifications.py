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
print("BUGBOUNTYTRACK SPECIFICATION INTEGRITY LINTER (VERSION 3.1.0)")
print("Level 1 Specification & Cross-Document Traceability Linter")
print("=" * 80)

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

# 1. File existence & minimum size thresholds
for fname, fpath in files.items():
    check(os.path.exists(fpath), f"File exists: {fname}")
    sz = os.path.getsize(fpath) if os.path.exists(fpath) else 0
    check(sz > 5000, f"File size > 5KB: {fname} ({sz} bytes)")

# 2. Check metadata in Markdown specifications
for mdf in ['BRD.md', 'SRS.md', 'WBS.md']:
    p = files[mdf]
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
    check('24-ST-013' in content, f"{mdf} contains Roll No 24-ST-013")
    check('Taha Asadullah' in content, f"{mdf} contains Taha Asadullah")
    check('Sir Umar Hayat' in content, f"{mdf} contains Sir Umar Hayat")
    check('PTUT - PRJ - 089' in content, f"{mdf} contains Project ID PTUT - PRJ - 089")
    # Verify no raw unescaped LaTeX formatting artifacts
    check(r'\text{' not in content, f"{mdf} has no \\text{{}} artifacts")
    check(r'\ge' not in content, f"{mdf} has no \\ge artifacts")
    check(r'\le' not in content, f"{mdf} has no \\le artifacts")

# 3. Check specific requirements in SRS.md
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

# 4. Check CVSS_TEST_FIXTURES.md integrity & vector uniqueness
with open(files['CVSS_TEST_FIXTURES.md'], 'r', encoding='utf-8') as f:
    cvss_text = f.read()

check('FIRST.org' in cvss_text and 'NIST National Vulnerability Database' in cvss_text, "CVSS_TEST_FIXTURES.md cites FIRST.org Examples Guide & NIST NVD")
check('CVE-2021-41773' in cvss_text and '7.5' in cvss_text, "CVSS_TEST_FIXTURES.md correctly attributes CVE-2021-41773 as 7.5 High")

check('24-ST-013' in cvss_text, "CVSS_TEST_FIXTURES.md contains Roll No 24-ST-013")

# Extract and assert uniqueness of CVSS vector strings
vector_pattern = re.compile(r'`(CVSS:3\.1/[^`]+)`')
vectors = vector_pattern.findall(cvss_text)
check(len(vectors) == 45, f"CVSS_TEST_FIXTURES.md contains exactly 45 vectors (found {len(vectors)})")
unique_vectors = set(vectors)
check(len(unique_vectors) == 45, f"All 45 vectors are mathematically unique (found {len(unique_vectors)} unique)")

# 5. Cross-Document WBS Arithmetic & Package Parity
with open(files['WBS.md'], 'r', encoding='utf-8') as f:
    wbs = f.read()

check('236 Hours' in wbs and '28 Hours' in wbs and '264 Hours' in wbs, "WBS.md academic arithmetic: 236h core + 28h buffer = 264h")
check('88 Hours' in wbs and '352 Hours' in wbs, "WBS.md commercial arithmetic: 264h academic + 88h commercial = 352h total")
check('WP-7.1' in wbs and 'WP-7.9' in wbs, "WBS.md contains commercial packages WP-7.1 to WP-7.9")

# 6. Check SRS.docx OpenXML integrity and embedded drawings
with zipfile.ZipFile(files['SRS.docx'], 'r') as srs_zip:
    srs_xml = srs_zip.read('word/document.xml').decode('utf-8')
    media_files = [f for f in srs_zip.namelist() if f.startswith('word/media/')]

check(len(media_files) == 6, f"SRS.docx contains exactly 6 images (found {len(media_files)})")
drawings_in_doc = srs_xml.count('<w:drawing>')
check(drawings_in_doc == 6, f"SRS.docx has exactly 6 <w:drawing> elements (found {drawings_in_doc})")
check('24-ST-013' in srs_xml, "SRS.docx contains Roll No 24-ST-013")
check('Taha Asadullah' in srs_xml, "SRS.docx contains Taha Asadullah")
check(r'\text{' not in srs_xml, "SRS.docx has no \\text{} artifacts")

# 7. Check BRD.docx OpenXML integrity
with zipfile.ZipFile(files['BRD.docx'], 'r') as brd_zip:
    brd_xml = brd_zip.read('word/document.xml').decode('utf-8')
check('24-ST-013' in brd_xml, "BRD.docx contains Roll No 24-ST-013")
check('Taha Asadullah' in brd_xml, "BRD.docx contains Taha Asadullah")
check('Starter' in brd_xml and 'Team' in brd_xml, "BRD.docx contains SaaS pricing tiers")

# 8. Check WBS.xlsx OpenXML integrity, formula consistency & mathematical parity
with zipfile.ZipFile(files['WBS.xlsx'], 'r') as wbs_zip:
    sheet1_xml = wbs_zip.read('xl/worksheets/sheet1.xml').decode('utf-8')
    sheet2_xml = wbs_zip.read('xl/worksheets/sheet2.xml').decode('utf-8')
    sheet3_xml = wbs_zip.read('xl/worksheets/sheet3.xml').decode('utf-8')
    sheet4_xml = wbs_zip.read('xl/worksheets/sheet4.xml').decode('utf-8')
    sheet5_xml = wbs_zip.read('xl/worksheets/sheet5.xml').decode('utf-8')

check('352 Total Hours' in sheet1_xml, "WBS.xlsx Sheet 1 contains 352 Total Hours")
check('24-ST-013' in sheet1_xml, "WBS.xlsx Sheet 1 contains Roll No 24-ST-013")
check('SUM(G2:G35)' in sheet2_xml, "WBS.xlsx Sheet 2 contains formula SUM(G2:G35) spanning all 34 work packages")
check('SUM(F2:F9)' in sheet4_xml, "WBS.xlsx Sheet 4 contains formula SUM(F2:F9) spanning all 8 Sprints")

# Assert that sheet2 calculated total matches 352
match_s2_tot = re.search(r'<c r="G36"[^>]*><f>[^<]+</f><v>(\d+)</v></c>', sheet2_xml)
if match_s2_tot:
    s2_val = int(match_s2_tot.group(1))
    check(s2_val == 352, f"WBS.xlsx Sheet 2 total engineering hours == 352 (computed {s2_val})")
else:
    errors.append("WBS.xlsx Sheet 2 total cell G36 not found")

# Assert that sheet4 calculated total matches 352
match_s4_tot = re.search(r'<c r="F10"[^>]*><f>[^<]+</f><v>(\d+)</v></c>', sheet4_xml)
if match_s4_tot:
    s4_val = int(match_s4_tot.group(1))
    check(s4_val == 352, f"WBS.xlsx Sheet 4 total sprint hours == 352 (computed {s4_val})")
else:
    errors.append("WBS.xlsx Sheet 4 total cell F10 not found")

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
