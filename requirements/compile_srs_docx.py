import zipfile, os, re, xml.sax.saxutils as saxutils

def escape(txt):
    return saxutils.escape(str(txt))

def clean_text(txt):
    if not txt:
        return ""
    t = txt
    t = t.replace(r'\ge', '≥')
    t = t.replace(r'\le', '≤')
    t = t.replace(r'\times', '×')
    t = t.replace(r'\text{', '').replace(r'}', '')
    t = t.replace(r'\$', '$')
    t = re.sub(r'\$([^$]+)\$', r'\1', t)
    t = t.replace('$$', '')
    return t

def parse_runs(text):
    text = clean_text(text)
    tokens = re.split(r'(\*\*.*?\*\*|`.*?`|\*.*?\*)', text)
    runs = []
    for tok in tokens:
        if not tok:
            continue
        if tok.startswith('**') and tok.endswith('**') and len(tok) >= 4:
            runs.append((tok[2:-2], True, False, False))
        elif tok.startswith('`') and tok.endswith('`') and len(tok) >= 2:
            runs.append((tok[1:-1], False, False, True))
        elif tok.startswith('*') and tok.endswith('*') and len(tok) >= 2:
            runs.append((tok[1:-1], False, True, False))
        else:
            runs.append((tok, False, False, False))
    return runs

def make_p_with_runs(runs, style='Normal', color='222222', sz=20, space_before=60, space_after=60, jc='left', is_heading=False, left_indent=0):
    h_style = f'<w:pStyle w:val="{style}"/>' if is_heading else ''
    ind_xml = f'<w:ind w:left="{left_indent}"/>' if left_indent > 0 else ''
    r_xmls = []
    for r_text, bold, italic, code in runs:
        r_text_escaped = escape(r_text)
        b_tag = '<w:b/>' if bold else ''
        i_tag = '<w:i/>' if italic else ''
        f_tag = '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>' if code else '<w:rFonts w:ascii="Lexend" w:hAnsi="Lexend"/>'
        c_tag = '<w:color w:val="9C4146"/>' if code else f'<w:color w:val="{color}"/>'
        r_xmls.append(
            f'<w:r>'
            f'<w:rPr>{f_tag}{b_tag}{i_tag}{c_tag}<w:sz w:val="{sz}"/></w:rPr>'
            f'<w:t xml:space="preserve">{r_text_escaped}</w:t>'
            f'</w:r>'
        )
    return (
        f'<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f'<w:pPr>{h_style}{ind_xml}<w:spacing w:before="{space_before}" w:after="{space_after}"/><w:jc w:val="{jc}"/></w:pPr>'
        f'{"".join(r_xmls)}'
        f'</w:p>'
    )

def make_simple_p(text, style='Normal', bold=False, italic=False, color='222222', sz=20, space_before=60, space_after=60, jc='left', is_heading=False, left_indent=0):
    runs = parse_runs(text)
    if bold:
        runs = [(t, True, i, c) for t, b, i, c in runs]
    if italic:
        runs = [(t, b, True, c) for t, b, i, c in runs]
    return make_p_with_runs(runs, style=style, color=color, sz=sz, space_before=space_before, space_after=space_after, jc=jc, is_heading=is_heading, left_indent=left_indent)

def make_drawing(rId, docPr_id, name, cx=5500000, cy=2800000):
    return (
        f'<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f'<w:pPr><w:jc w:val="center"/><w:spacing w:before="160" w:after="80"/></w:pPr>'
        f'<w:r>'
        f'<w:drawing>'
        f'<wp:inline xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" distT="0" distB="0" distL="0" distR="0">'
        f'<wp:extent cx="{cx}" cy="{cy}"/>'
        f'<wp:docPr id="{docPr_id}" name="{escape(name)}"/>'
        f'<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        f'<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        f'<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        f'<pic:nvPicPr>'
        f'<pic:cNvPr id="0" name="{escape(name)}"/>'
        f'<pic:cNvPicPr/>'
        f'</pic:nvPicPr>'
        f'<pic:blipFill>'
        f'<a:blip xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:embed="{rId}"/>'
        f'<a:stretch><a:fillRect/></a:stretch>'
        f'</pic:blipFill>'
        f'<pic:spPr>'
        f'<a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        f'</pic:spPr>'
        f'</pic:pic>'
        f'</a:graphicData>'
        f'</a:graphic>'
        f'</wp:inline>'
        f'</w:drawing>'
        f'</w:r>'
        f'</w:p>'
    )

def make_table(headers, rows, total_width=9500, hdr_bg="E3EFCB", border_col="D1E3A5"):
    num_cols = len(headers) if headers else (len(rows[0]) if rows else 1)
    col_lens = [len(h) for h in headers] if headers else [1]*num_cols
    for row in rows:
        for idx, cell in enumerate(row):
            if idx < len(col_lens):
                col_lens[idx] = max(col_lens[idx], len(cell))
            else:
                col_lens.append(len(cell))
    
    total_len = sum(col_lens) if sum(col_lens) > 0 else 1
    
    col_widths = []
    if num_cols == 2:
        col_widths = [3000, total_width - 3000]
    elif num_cols == 3:
        col_widths = [2500, 3500, total_width - 6000]
    elif num_cols == 4:
        col_widths = [1500, 2600, 3000, total_width - 7100]
    elif num_cols == 5:
        col_widths = [1200, 2200, 1400, 2500, total_width - 7300]
    elif num_cols == 6:
        # For State Transition Table
        col_widths = [1300, 1600, 1100, 2100, 1500, total_width - 7600]
    else:
        assigned = 0
        for l in col_lens[:-1]:
            w = int(total_width * (l / total_len))
            w = max(w, 1000)
            col_widths.append(w)
            assigned += w
        col_widths.append(max(total_width - assigned, 1000))

    tbl_xml = []
    tbl_xml.append(f'<w:tbl xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">')
    tbl_xml.append(f'<w:tblPr><w:tblW w:w="{total_width}" w:type="dxa"/><w:jc w:val="center"/>')
    tbl_xml.append(f'<w:tblBorders>'
                   f'<w:top w:val="single" w:sz="4" w:space="0" w:color="{border_col}"/>'
                   f'<w:left w:val="single" w:sz="4" w:space="0" w:color="{border_col}"/>'
                   f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="{border_col}"/>'
                   f'<w:right w:val="single" w:sz="4" w:space="0" w:color="{border_col}"/>'
                   f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{border_col}"/>'
                   f'<w:insideV w:val="single" w:sz="4" w:space="0" w:color="{border_col}"/>'
                   f'</w:tblBorders></w:tblPr>')
    
    tbl_xml.append('<w:tblGrid>')
    for w in col_widths:
        tbl_xml.append(f'<w:gridCol w:w="{w}"/>')
    tbl_xml.append('</w:tblGrid>')

    if headers:
        h_cells = []
        for idx, h in enumerate(headers):
            runs = parse_runs(h)
            p_xml = make_p_with_runs([(r[0], True, r[2], r[3]) for r in runs], color="1B2A1E", sz=18, space_before=40, space_after=40)
            w = col_widths[idx]
            h_cells.append(
                f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/>'
                f'<w:shd w:val="clear" w:fill="{hdr_bg}"/>'
                f'<w:tcMar><w:top w:w="80" w:type="dxa"/><w:bottom w:w="80" w:type="dxa"/><w:left w:w="100" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tcMar>'
                f'</w:tcPr>{p_xml}</w:tc>'
            )
        tbl_xml.append(f'<w:tr><w:trPr><w:tblHeader/></w:trPr>{"".join(h_cells)}</w:tr>')

    for row_idx, row in enumerate(rows):
        b_cells = []
        row_bg = "F9FBF6" if row_idx % 2 == 1 else "FFFFFF"
        for idx, cell in enumerate(row):
            w = col_widths[idx] if idx < len(col_widths) else 1200
            runs = parse_runs(cell)
            is_first_col = (idx == 0 and not headers)
            if is_first_col:
                runs = [(r[0], True, r[2], r[3]) for r in runs]
            p_xml = make_p_with_runs(runs, color="222222", sz=17, space_before=30, space_after=30)
            shd_xml = f'<w:shd w:val="clear" w:fill="{row_bg}"/>' if row_bg != "FFFFFF" else ''
            b_cells.append(
                f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/>{shd_xml}'
                f'<w:tcMar><w:top w:w="60" w:type="dxa"/><w:bottom w:w="60" w:type="dxa"/><w:left w:w="100" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tcMar>'
                f'</w:tcPr>{p_xml}</w:tc>'
            )
        tbl_xml.append(f'<w:tr>{"".join(b_cells)}</w:tr>')
    tbl_xml.append('</w:tbl>')
    return ''.join(tbl_xml)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))

srs_md_path = os.path.join(SCRIPT_DIR, 'SRS.md')
with open(srs_md_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

body_parts = []

# Title & Subtitles - Added ONCE here, avoiding duplicate title headers
body_parts.append(make_simple_p("Punjab Tianjin University of Technology", bold=False, color="555555", sz=22, space_before=200, space_after=40, jc="center"))
body_parts.append(make_simple_p("Department of Software Engineering Technology", bold=False, color="555555", sz=20, space_before=20, space_after=40, jc="center"))
body_parts.append(make_simple_p("FINAL YEAR PROJECT (FYP) ENGINEERING SPECIFICATION", bold=True, color="5A6652", sz=24, space_before=20, space_after=60, jc="center"))
body_parts.append(make_simple_p("SOFTWARE REQUIREMENTS SPECIFICATION (SRS)", bold=True, color="386B24", sz=40, space_before=60, space_after=80, jc="center"))
body_parts.append(make_simple_p("Project: BugBountyTrack", bold=True, color="2B4C1A", sz=26, space_before=40, space_after=40, jc="center"))
body_parts.append(make_simple_p("A Multi-Tenant Vulnerability Disclosure Platform with Cryptographic Payload Isolation and Evidence-Based Remediation Traceability", bold=False, color="555555", sz=20, space_before=20, space_after=160, jc="center"))

i = 0
in_mermaid = False
in_toc = False

# Skip lines 1 to 7 from SRS.md (which are duplicate titles) so we start directly at the metadata table
while i < len(lines):
    if lines[i].strip().startswith('| Academic & Engineering Parameter'):
        break
    i += 1

diagram_map = {
    "Figure 4.1": ("rId201", 201, "Figure 4.1: BugBountyTrack 3-Tier Decoupled Component Architecture", 5500000, 2811111),
    "Figure 4.2": ("rId202", 202, "Figure 4.2: BugBountyTrack Use Case Model & Actor Roles", 5500000, 2933333),
    "Figure 4.3": ("rId203", 203, "Figure 4.3: Sequence: Browser-Side OpenPGP Encrypted Submission", 5500000, 2494186),
    "Figure 4.4": ("rId204", 204, "Figure 4.4: Sequence: In-Browser Decryption & Confidential Conversation", 5500000, 2625000),
    "Figure 4.5": ("rId205", 205, "Figure 4.5: Remediation & Attested Retest Lifecycle State Machine", 5500000, 2811111),
    "Figure 4.6": ("rId206", 206, "Figure 4.6: Relational Prisma ERD & Multi-Tenant Model", 5500000, 3108695),
}

inserted_diagrams = set()

while i < len(lines):
    line = lines[i].rstrip('\r\n')
    sline = line.strip()
    if not sline:
        i += 1
        continue
    
    # Check if we are in Mermaid block
    if sline.startswith('```mermaid'):
        in_mermaid = True
        i += 1
        continue
    if in_mermaid:
        if sline.startswith('```'):
            in_mermaid = False
        i += 1
        continue
    
    # Check for TOC
    if sline == '## Table of Contents':
        in_toc = True
        body_parts.append(make_simple_p("Table of Contents", style="Heading1", bold=True, color="386B24", sz=26, space_before=240, space_after=80, is_heading=True))
        i += 1
        continue
    if in_toc and sline.startswith('## 1.'):
        in_toc = False

    # Diagram insertion check (ONLY in Section 4 and outside TOC)
    if not in_toc and sline.startswith('### 4.'):
        inserted_diagram = False
        for fig_key, (rId, dId, dName, cx, cy) in diagram_map.items():
            if fig_key in sline and fig_key not in inserted_diagrams:
                inserted_diagrams.add(fig_key)
                body_parts.append(make_simple_p(sline.replace('#', '').strip(), style="Heading2", bold=True, color="2B4C1A", sz=22, space_before=180, space_after=60, is_heading=True))
                body_parts.append(make_drawing(rId, dId, dName, cx, cy))
                body_parts.append(make_simple_p(f"[{dName}]", italic=True, color="555555", sz=17, space_before=40, space_after=120, jc="center"))
                inserted_diagram = True
                break
        if inserted_diagram:
            i += 1
            continue

    if sline == '---':
        i += 1
        continue
    
    # Heading 1
    if sline.startswith('## '):
        h1_text = sline[3:].strip()
        body_parts.append(make_simple_p(h1_text, style="Heading1", bold=True, color="386B24", sz=26, space_before=240, space_after=80, is_heading=True))
        i += 1
        continue

    # Heading 2
    if sline.startswith('### '):
        h2_text = sline[4:].strip()
        body_parts.append(make_simple_p(h2_text, style="Heading2", bold=True, color="2B4C1A", sz=22, space_before=180, space_after=60, is_heading=True))
        i += 1
        continue

    # Heading 3 / 4
    if sline.startswith('#### '):
        h3_text = sline[5:].strip()
        body_parts.append(make_simple_p(h3_text, style="Heading3", bold=True, color="1B2A1E", sz=20, space_before=140, space_after=40, is_heading=True))
        i += 1
        continue

    # Table parsing
    if sline.startswith('|') and sline.endswith('|'):
        tbl_lines = []
        while i < len(lines) and lines[i].strip().startswith('|') and lines[i].strip().endswith('|'):
            tbl_lines.append(lines[i].strip())
            i += 1
        
        headers = []
        rows = []
        for t_idx, tl in enumerate(tbl_lines):
            cells = [c.strip() for c in tl.split('|')[1:-1]]
            if t_idx == 0:
                headers = cells
            elif t_idx == 1 and all(set(c).issubset({'-', ':', ' '}) for c in cells):
                continue
            else:
                rows.append(cells)
        
        body_parts.append(make_table(headers, rows))
        body_parts.append(make_simple_p("", space_before=40, space_after=40))
        continue

    # Bullet points / TOC items
    if in_toc:
        if re.match(r'^\d+\.\s+', sline):
            body_parts.append(make_simple_p(sline, bold=True, color="2B4C1A", sz=20, space_before=60, space_after=20))
            i += 1
            continue
        elif sline.startswith('- ') or sline.startswith('• '):
            b_text = sline[2:].strip()
            body_parts.append(make_simple_p(b_text, color="444444", sz=19, space_before=15, space_after=15, left_indent=360))
            i += 1
            continue

    if sline.startswith('* ') or sline.startswith('- '):
        b_text = sline[2:].strip()
        body_parts.append(make_simple_p(f"•  {b_text}", color="222222", sz=20, space_before=40, space_after=40))
        i += 1
        continue

    if re.match(r'^\d+\.\s+', sline):
        body_parts.append(make_simple_p(sline, color="222222", sz=20, space_before=40, space_after=40))
        i += 1
        continue

    # Standard Paragraph
    body_parts.append(make_simple_p(sline, color="222222", sz=20, space_before=60, space_after=60))
    i += 1

print(f"Parsed {len(lines)} lines into {len(body_parts)} body elements.")
print(f"Inserted diagrams: {sorted(list(inserted_diagrams))}")

# Preserve sectPr from original SRS.docx
template_path = os.path.join(PROJECT_DIR, 'Resources', 'SRS.docx')
with zipfile.ZipFile(template_path, 'r') as zin:
    # Filter out template media files so word/media/ only contains our exact 6 diagrams
    file_map = {name: zin.read(name) for name in zin.namelist() if not name.startswith('word/media/')}

orig_doc = file_map['word/document.xml'].decode('utf-8')
sectPr_match = re.search(r'<w:sectPr.*?</w:sectPr>', orig_doc)
sectPr_xml = sectPr_match.group(0) if sectPr_match else (
    '<w:sectPr>'
    '<w:headerReference w:type="default" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:id="rId1"/>'
    '<w:footerReference w:type="default" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:id="rId2"/>'
    '<w:pgSz w:w="11906" w:h="16838"/>'
    '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720"/>'
    '</w:sectPr>'
)

doc_xml = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">\n'
    f'<w:body>{"".join(body_parts)}{sectPr_xml}</w:body>\n'
    '</w:document>'
)

# Build updated document.xml.rels with rId201..rId206
rels_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>
  <Relationship Id="rId5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>
  <Relationship Id="rId201" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/fig4_1_component.png"/>
  <Relationship Id="rId202" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/fig4_2_usecase.png"/>
  <Relationship Id="rId203" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/fig4_3_seq_submission.png"/>
  <Relationship Id="rId204" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/fig4_4_seq_decryption.png"/>
  <Relationship Id="rId205" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/fig4_5_statemachine.png"/>
  <Relationship Id="rId206" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/fig4_6_erd.png"/>
</Relationships>'''

diagram_files = {
    'word/media/fig4_1_component.png': os.path.join(SCRIPT_DIR, 'diagrams', 'fig4_1_component.png'),
    'word/media/fig4_2_usecase.png': os.path.join(SCRIPT_DIR, 'diagrams', 'fig4_2_usecase.png'),
    'word/media/fig4_3_seq_submission.png': os.path.join(SCRIPT_DIR, 'diagrams', 'fig4_3_seq_submission.png'),
    'word/media/fig4_4_seq_decryption.png': os.path.join(SCRIPT_DIR, 'diagrams', 'fig4_4_seq_decryption.png'),
    'word/media/fig4_5_statemachine.png': os.path.join(SCRIPT_DIR, 'diagrams', 'fig4_5_statemachine.png'),
    'word/media/fig4_6_erd.png': os.path.join(SCRIPT_DIR, 'diagrams', 'fig4_6_erd.png'),
}

file_map['word/document.xml'] = doc_xml.encode('utf-8')
file_map['word/_rels/document.xml.rels'] = rels_xml.encode('utf-8')

for zip_path, local_path in diagram_files.items():
    if os.path.exists(local_path):
        with open(local_path, 'rb') as img_f:
            file_map[zip_path] = img_f.read()
    else:
        print(f"WARNING: Image {local_path} not found!")

target_docx = os.path.join(SCRIPT_DIR, 'SRS.docx')
with zipfile.ZipFile(target_docx, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
    for name, content in file_map.items():
        zout.writestr(name, content)

print(f"Successfully generated {target_docx} ({os.path.getsize(target_docx)} bytes)")
