import zipfile, os, xml.sax.saxutils as saxutils

def escape(txt):
    return saxutils.escape(str(txt))

def build_cell(ref, style, val, cell_type=None, formula=None):
    if formula is not None:
        v_tag = f'<v>{escape(val)}</v>' if val is not None else '<v/>'
        return f'<c r="{ref}" s="{style}"><f>{formula}</f>{v_tag}</c>'
    if cell_type == 'n':
        return f'<c r="{ref}" s="{style}" t="n"><v>{val}</v></c>'
    return f'<c r="{ref}" s="{style}" t="inlineStr"><is><t>{escape(val)}</t></is></c>'

# 1. Parse WBS.md
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))

wbs_md_path = os.path.join(SCRIPT_DIR, 'WBS.md')
with open(wbs_md_path, 'r', encoding='utf-8') as f:
    wbs_md = f.read()

# Work Packages (Part A Academic 264h + Part B Commercial 160h: 38 items)
wp_rows = []
for line in wbs_md.splitlines():
    s = line.strip()
    if s.startswith('| **WP-') or s.startswith('| **ACAD-'):
        parts = [p.strip() for p in s.split('|')[1:-1]]
        code = parts[0].replace('*', '')
        req_id = parts[1]
        mod = parts[2]
        name = parts[3]
        desc = parts[4].replace(r'\ge', '≥').replace(r'\le', '≤').replace(r'\text{', '').replace('}', '').replace('$', '')
        weeks = parts[5]
        hours = int(parts[6])
        owner = parts[7]
        pred = parts[8]
        status = parts[9].replace('`', '')
        wp_rows.append((code, req_id, mod, name, desc, weeks, hours, owner, pred, status))

print(f"Parsed {len(wp_rows)} work packages, total hours: {sum(w[6] for w in wp_rows)}")

# RACI Matrix
raci_rows = []
in_raci = False
for line in wbs_md.splitlines():
    if '## Sheet 3: RACI' in line:
        in_raci = True
        continue
    if in_raci and line.strip().startswith('## '):
        break
    if in_raci and (line.strip().startswith('| **MOD-') or line.strip().startswith('| **ACAD')):
        parts = [p.strip() for p in line.split('|')[1:-1]]
        code = parts[0].replace('*', '')
        name = parts[1]
        taha = parts[2].replace('*', '')
        supervisor = parts[3]
        panel = parts[4]
        ai_squad = parts[5]
        raci_rows.append((code, name, taha, supervisor, panel, ai_squad))

print(f"Parsed {len(raci_rows)} RACI modules")

# Sprints
sprint_rows = []
in_sprints = False
for line in wbs_md.splitlines():
    if '## Sheet 4: Sprint' in line:
        in_sprints = True
        continue
    if in_sprints and line.strip().startswith('## '):
        break
    if in_sprints and line.strip().startswith('| **Sprint '):
        parts = [p.strip() for p in line.split('|')[1:-1]]
        sid = parts[0].replace('*', '')
        weeks = parts[1]
        target_wp = parts[2]
        deliverable = parts[3]
        gate = parts[4].replace('*', '')
        hours = int(parts[5])
        status = parts[6].replace('`', '')
        sprint_rows.append((sid, weeks, target_wp, deliverable, gate, hours, status))

print(f"Parsed {len(sprint_rows)} Sprints, total sprint hours: {sum(s[5] for s in sprint_rows)}")

# Financial Tiers (Part A Demo)
finance_rows = []
in_finance = False
for line in wbs_md.splitlines():
    if 'Part A: Academic Demonstration' in line:
        in_finance = True
        continue
    if in_finance and 'Part B: Commercial Production' in line:
        break
    if in_finance and line.strip().startswith('| **') and not 'TOTAL DEMO' in line:
        parts = [p.strip() for p in line.split('|')[1:-1]]
        layer = parts[0].replace('*', '')
        vendor = parts[1]
        tier = parts[2]
        quota = parts[3]
        try:
            cost = float(parts[4])
        except:
            cost = 0.0
        finance_rows.append((layer, vendor, tier, quota, cost))

print(f"Parsed {len(finance_rows)} Finance tiers")

# 2. Build Sheet 1 XML (Executive Overview)
s1_rows = [
    (2, [('B2', 1, 'BUGBOUNTYTRACK - WORK BREAKDOWN STRUCTURE (WBS)')]),
    (3, [('B3', 2, 'Final Year Project (FYP) Engineering Charter & Governance Baseline')]),
    (5, [('B5', 3, 'Project Parameter'), ('C5', 3, 'Engineering Specification')]),
    (6, [('B6', 4, 'Project Identifier'), ('C6', 5, 'PTUT - PRJ - 089')]),
    (7, [('B7', 6, 'Project Title'), ('C7', 7, 'BugBountyTrack: Private Bug Bounty & Vulnerability Disclosure Platform')]),
    (8, [('B8', 4, 'Academic Sub-Field'), ('C8', 5, '9. Cybersecurity, Privacy & LegalTech')]),
    (9, [('B9', 6, 'Single Accountable Author'), ('C9', 7, 'Taha Asadullah (Roll No: 24-ST-013)')]),
    (10, [('B10', 4, 'Academic Institution'), ('C10', 5, 'Punjab Tianjin University of Technology (PTUT), Lahore')]),
    (11, [('B11', 6, 'Department'), ('C11', 7, 'Department of Software Engineering Technology')]),
    (12, [('B12', 4, 'Session / Batch / Section'), ('C12', 5, 'Session 2024–2028 / Batch 24-SET-Fall / Section SET-B')]),
    (13, [('B13', 6, 'Official Student Email'), ('C13', 7, '24-st-013@students.ptut.edu.pk')]),
    (14, [('B14', 4, 'Project Supervisor'), ('C14', 5, 'Sir Umar Hayat')]),
    (15, [('B15', 6, 'Client Platform'), ('C15', 7, 'Modern Web (Next.js 14+ App Router, React 18+, TypeScript 5.x, Tailwind CSS, OpenPGP.js)')]),
    (16, [('B16', 4, 'Backend & Persistence'), ('C16', 5, 'Unified Next.js Serverless on Vercel + PostgreSQL 16 on Neon via Prisma ORM (RLS)')]),
    (17, [('B17', 6, 'Planned Workload'), ('C17', 7, '424 Total Hours (264h Academic Baseline + 160h Commercial Launch across 18 Weeks)')]),
    (18, [('B18', 4, 'Release State'), ('C18', 5, 'Commercial Baseline & Academic Evaluation Specification (Version 3.2.0)')]),
]

s1_xml_parts = [
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
    '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetPr><outlinePr summaryBelow="1" summaryRight="1"/><pageSetUpPr/></sheetPr>',
    '<dimension ref="A1:C18"/>',
    '<sheetViews><sheetView showGridLines="1" workbookViewId="0"><selection activeCell="A1" sqref="A1"/></sheetView></sheetViews>',
    '<sheetFormatPr baseColWidth="8" defaultRowHeight="15"/>',
    '<cols><col width="14" customWidth="1" min="1" max="1"/><col width="32" customWidth="1" min="2" max="2"/><col width="88" customWidth="1" min="3" max="3"/></cols>',
    '<sheetData>'
]
for r_num, cells in s1_rows:
    row_str = f'<row r="{r_num}">'
    for ref, st, val in cells:
        row_str += build_cell(ref, st, val)
    row_str += '</row>'
    s1_xml_parts.append(row_str)
s1_xml_parts.append('</sheetData><pageMargins left="0.75" right="0.75" top="1" bottom="1" header="0.5" footer="0.5"/></worksheet>')
sheet1_xml = ''.join(s1_xml_parts)

# 3. Build Sheet 2 XML (Module-Wise WBS)
total_wp_rows = len(wp_rows)
s2_xml_parts = [
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
    '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetPr><outlinePr summaryBelow="1" summaryRight="1"/><pageSetUpPr/></sheetPr>',
    f'<dimension ref="A1:J{total_wp_rows+2}"/>',
    '<sheetViews><sheetView showGridLines="1" workbookViewId="0"><selection activeCell="A1" sqref="A1"/></sheetView></sheetViews>',
    '<sheetFormatPr baseColWidth="8" defaultRowHeight="15"/>',
    '<cols>'
    '<col width="14" customWidth="1" min="1" max="1"/>'
    '<col width="12" customWidth="1" min="2" max="2"/>'
    '<col width="34" customWidth="1" min="3" max="3"/>'
    '<col width="42" customWidth="1" min="4" max="4"/>'
    '<col width="85" customWidth="1" min="5" max="5"/>'
    '<col width="15" customWidth="1" min="6" max="6"/>'
    '<col width="14" customWidth="1" min="7" max="7"/>'
    '<col width="20" customWidth="1" min="8" max="8"/>'
    '<col width="15" customWidth="1" min="9" max="9"/>'
    '<col width="16" customWidth="1" min="10" max="10"/>'
    '</cols>',
    '<sheetData>',
    '<row r="1">' +
    build_cell('A1', 8, 'WBS Code') +
    build_cell('B1', 8, 'Req ID') +
    build_cell('C1', 8, 'Module / Area') +
    build_cell('D1', 8, 'Work Package Name') +
    build_cell('E1', 8, 'Deliverable Scope & Acceptance Criteria') +
    build_cell('F1', 8, 'Start–End Week') +
    build_cell('G1', 8, 'Est. Hours') +
    build_cell('H1', 8, 'Human Owner') +
    build_cell('I1', 8, 'Predecessor') +
    build_cell('J1', 8, 'Status') +
    '</row>'
]

for idx, (code, req_id, mod, name, desc, weeks, hours, owner, pred, status) in enumerate(wp_rows):
    r_num = idx + 2
    if r_num % 2 == 0:
        st_txt = 10
        st_code = 9
    else:
        st_txt = 12
        st_code = 11
    
    r_xml = (f'<row r="{r_num}">' +
             build_cell(f'A{r_num}', st_code, code) +
             build_cell(f'B{r_num}', st_code, req_id) +
             build_cell(f'C{r_num}', st_txt, mod) +
             build_cell(f'D{r_num}', st_txt, name) +
             build_cell(f'E{r_num}', st_txt, desc) +
             build_cell(f'F{r_num}', st_code, weeks) +
             build_cell(f'G{r_num}', st_code, hours, cell_type='n') +
             build_cell(f'H{r_num}', st_code, owner) +
             build_cell(f'I{r_num}', st_code, pred) +
             build_cell(f'J{r_num}', st_code, status) +
             '</row>')
    s2_xml_parts.append(r_xml)

tot_r2 = total_wp_rows + 2
s2_xml_parts.append(f'<row r="{tot_r2}">' +
                    build_cell(f'E{tot_r2}', 13, 'TOTAL ESTIMATED ENGINEERING HOURS:') +
                    build_cell(f'G{tot_r2}', 14, sum(w[6] for w in wp_rows), formula=f'SUM(G2:G{tot_r2-1})') +
                    '</row>')
s2_xml_parts.append('</sheetData><pageMargins left="0.75" right="0.75" top="1" bottom="1" header="0.5" footer="0.5"/></worksheet>')
sheet2_xml = ''.join(s2_xml_parts)

# 4. Build Sheet 3 XML (RACI Matrix)
s3_xml_parts = [
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
    '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetPr><outlinePr summaryBelow="1" summaryRight="1"/><pageSetUpPr/></sheetPr>',
    f'<dimension ref="A1:F{len(raci_rows)+1}"/>',
    '<sheetViews><sheetView showGridLines="1" workbookViewId="0"><selection activeCell="A1" sqref="A1"/></sheetView></sheetViews>',
    '<sheetFormatPr baseColWidth="8" defaultRowHeight="15"/>',
    '<cols>'
    '<col width="15" customWidth="1" min="1" max="1"/>'
    '<col width="45" customWidth="1" min="2" max="2"/>'
    '<col width="28" customWidth="1" min="3" max="3"/>'
    '<col width="24" customWidth="1" min="4" max="4"/>'
    '<col width="24" customWidth="1" min="5" max="5"/>'
    '<col width="42" customWidth="1" min="6" max="6"/>'
    '</cols>',
    '<sheetData>',
    '<row r="1">' +
    build_cell('A1', 15, 'Module Code') +
    build_cell('B1', 15, 'Module Name') +
    build_cell('C1', 15, 'Human Accountable (Taha)') +
    build_cell('D1', 15, 'Supervisor (Sir Umar)') +
    build_cell('E1', 15, 'Faculty Panel (PTUT)') +
    build_cell('F1', 15, 'Internal AI Advisory Squad') +
    '</row>'
]

for idx, (code, name, taha, supervisor, panel, ai_squad) in enumerate(raci_rows):
    r_num = idx + 2
    st_txt = 10 if r_num % 2 == 0 else 12
    st_val = 9 if r_num % 2 == 0 else 11
    r_xml = (f'<row r="{r_num}">' +
             build_cell(f'A{r_num}', st_val, code) +
             build_cell(f'B{r_num}', st_txt, name) +
             build_cell(f'C{r_num}', st_val, taha) +
             build_cell(f'D{r_num}', st_val, supervisor) +
             build_cell(f'E{r_num}', st_val, panel) +
             build_cell(f'F{r_num}', st_txt, ai_squad) +
             '</row>')
    s3_xml_parts.append(r_xml)

s3_xml_parts.append('</sheetData><pageMargins left="0.75" right="0.75" top="1" bottom="1" header="0.5" footer="0.5"/></worksheet>')
sheet3_xml = ''.join(s3_xml_parts)

# 5. Build Sheet 4 XML (Sprint Milestones)
s4_xml_parts = [
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
    '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetPr><outlinePr summaryBelow="1" summaryRight="1"/><pageSetUpPr/></sheetPr>',
    f'<dimension ref="A1:G{len(sprint_rows)+2}"/>',
    '<sheetViews><sheetView showGridLines="1" workbookViewId="0"><selection activeCell="A1" sqref="A1"/></sheetView></sheetViews>',
    '<sheetFormatPr baseColWidth="8" defaultRowHeight="15"/>',
    '<cols>'
    '<col width="14" customWidth="1" min="1" max="1"/>'
    '<col width="18" customWidth="1" min="2" max="2"/>'
    '<col width="34" customWidth="1" min="3" max="3"/>'
    '<col width="75" customWidth="1" min="4" max="4"/>'
    '<col width="36" customWidth="1" min="5" max="5"/>'
    '<col width="16" customWidth="1" min="6" max="6"/>'
    '<col width="16" customWidth="1" min="7" max="7"/>'
    '</cols>',
    '<sheetData>',
    '<row r="1">' +
    build_cell('A1', 15, 'Sprint ID') +
    build_cell('B1', 15, 'Academic Weeks') +
    build_cell('C1', 15, 'Target Work Packages') +
    build_cell('D1', 15, 'Key Engineering Deliverables') +
    build_cell('E1', 15, 'Prerequisite Gates & Evaluation') +
    build_cell('F1', 15, 'Planned Hours') +
    build_cell('G1', 15, 'Status') +
    '</row>'
]

for idx, (sid, weeks, twp, deliv, gate, hours, stat) in enumerate(sprint_rows):
    r_num = idx + 2
    st_txt = 10 if r_num % 2 == 0 else 12
    st_val = 9 if r_num % 2 == 0 else 11
    r_xml = (f'<row r="{r_num}">' +
             build_cell(f'A{r_num}', st_val, sid) +
             build_cell(f'B{r_num}', st_val, weeks) +
             build_cell(f'C{r_num}', st_txt, twp) +
             build_cell(f'D{r_num}', st_txt, deliv) +
             build_cell(f'E{r_num}', st_txt, gate) +
             build_cell(f'F{r_num}', st_val, hours, cell_type='n') +
             build_cell(f'G{r_num}', st_val, stat) +
             '</row>')
    s4_xml_parts.append(r_xml)

tot_r4 = len(sprint_rows) + 2
s4_xml_parts.append(f'<row r="{tot_r4}">' +
                    build_cell(f'E{tot_r4}', 13, 'TOTAL PLANNED SPRINT HOURS:') +
                    build_cell(f'F{tot_r4}', 14, sum(s[5] for s in sprint_rows), formula=f'SUM(F2:F{tot_r4-1})') +
                    '</row>')
s4_xml_parts.append('</sheetData><pageMargins left="0.75" right="0.75" top="1" bottom="1" header="0.5" footer="0.5"/></worksheet>')
sheet4_xml = ''.join(s4_xml_parts)

# 6. Build Sheet 5 XML (Zero-Cost Financial Model)
s5_xml_parts = [
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
    '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetPr><outlinePr summaryBelow="1" summaryRight="1"/><pageSetUpPr/></sheetPr>',
    f'<dimension ref="A1:E{len(finance_rows)+2}"/>',
    '<sheetViews><sheetView showGridLines="1" workbookViewId="0"><selection activeCell="A1" sqref="A1"/></sheetView></sheetViews>',
    '<sheetFormatPr baseColWidth="8" defaultRowHeight="15"/>',
    '<cols>'
    '<col width="34" customWidth="1" min="1" max="1"/>'
    '<col width="30" customWidth="1" min="2" max="2"/>'
    '<col width="36" customWidth="1" min="3" max="3"/>'
    '<col width="55" customWidth="1" min="4" max="4"/>'
    '<col width="24" customWidth="1" min="5" max="5"/>'
    '</cols>',
    '<sheetData>',
    '<row r="1">' +
    build_cell('A1', 15, 'Infrastructure Layer') +
    build_cell('B1', 15, 'Platform Provider') +
    build_cell('C1', 15, 'Provisioned Cloud Tier') +
    build_cell('D1', 15, 'Resource Allocations & Quotas') +
    build_cell('E1', 15, 'Monthly Cost ($USD)') +
    '</row>'
]

for idx, (layer, vendor, tier, quota, cost) in enumerate(finance_rows):
    r_num = idx + 2
    st_txt = 10 if r_num % 2 == 0 else 12
    st_cost = 16 if r_num % 2 == 0 else 17
    r_xml = (f'<row r="{r_num}">' +
             build_cell(f'A{r_num}', st_txt, layer) +
             build_cell(f'B{r_num}', st_txt, vendor) +
             build_cell(f'C{r_num}', st_txt, tier) +
             build_cell(f'D{r_num}', st_txt, quota) +
             build_cell(f'E{r_num}', st_cost, cost, cell_type='n') +
             '</row>')
    s5_xml_parts.append(r_xml)

fin_total_r = len(finance_rows) + 2
s5_xml_parts.append(f'<row r="{fin_total_r}">' +
                    build_cell(f'D{fin_total_r}', 13, 'TOTAL DEMO INFRASTRUCTURE COST:') +
                    build_cell(f'E{fin_total_r}', 18, 0, formula=f'SUM(E2:E{fin_total_r-1})') +
                    '</row>')
s5_xml_parts.append('</sheetData><pageMargins left="0.75" right="0.75" top="1" bottom="1" header="0.5" footer="0.5"/></worksheet>')
sheet5_xml = ''.join(s5_xml_parts)

# 7. Write to WBS.xlsx
target_xlsx = os.path.join(SCRIPT_DIR, 'WBS.xlsx')
sample_xlsx = os.path.join(PROJECT_DIR, 'Resources', 'WBS.xlsx')

with zipfile.ZipFile(sample_xlsx, 'r') as src:
    with zipfile.ZipFile(target_xlsx, 'w', compression=zipfile.ZIP_DEFLATED) as dst:
        for item in src.infolist():
            if item.filename == 'xl/worksheets/sheet1.xml':
                dst.writestr(item, sheet1_xml.encode('utf-8'))
            elif item.filename == 'xl/worksheets/sheet2.xml':
                dst.writestr(item, sheet2_xml.encode('utf-8'))
            elif item.filename == 'xl/worksheets/sheet3.xml':
                dst.writestr(item, sheet3_xml.encode('utf-8'))
            elif item.filename == 'xl/worksheets/sheet4.xml':
                dst.writestr(item, sheet4_xml.encode('utf-8'))
            elif item.filename == 'xl/worksheets/sheet5.xml':
                dst.writestr(item, sheet5_xml.encode('utf-8'))
            else:
                dst.writestr(item, src.read(item.filename))

print(f"Successfully generated {target_xlsx} ({os.path.getsize(target_xlsx)} bytes)")
