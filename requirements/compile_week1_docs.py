#!/usr/bin/env python3
"""
Compiles WEEK_1_PART_A_USER_PERSONAS.md and WEEK_1_PART_B_CHARTER_AND_MVP.md
into institutional OpenXML Word (.docx) documents in requirements/ and Resources/.
"""
import zipfile, os, re, shutil, xml.sax.saxutils as saxutils

def escape(txt):
    return saxutils.escape(str(txt))

def clean_text(txt):
    if not txt:
        return ""
    t = txt
    t = t.replace(r'\ge', '≥')
    t = t.replace(r'\le', '≤')
    t = t.replace(r'\text{', '').replace(r'}', '')
    t = t.replace(r'\$', '$')
    t = re.sub(r'\$([^$]+)\$', r'\1', t)
    t = t.replace('$$', '')
    return t

def parse_runs(text):
    """Parses a string into a list of tuples: (text, is_bold, is_italic, is_code)"""
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

def make_p_with_runs(runs, style='Normal', color='000000', sz=24, space_before=80, space_after=80, line_spacing=276, jc='left', is_heading=False, left_indent=0):
    h_style = f'<w:pStyle w:val="{style}"/>' if is_heading else ''
    ind_xml = f'<w:ind w:left="{left_indent}"/>' if left_indent > 0 else ''
    r_xmls = []
    for r_text, bold, italic, code in runs:
        r_text_escaped = escape(r_text)
        b_tag = '<w:b/><w:bCs/>' if bold else ''
        i_tag = '<w:i/><w:iCs/>' if italic else ''
        f_tag = '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman" w:eastAsia="Times New Roman"/>'
        c_tag = '<w:color w:val="000000"/>'
        r_xmls.append(
            f'<w:r>'
            f'<w:rPr>{f_tag}{b_tag}{i_tag}{c_tag}<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/></w:rPr>'
            f'<w:t xml:space="preserve">{r_text_escaped}</w:t>'
            f'</w:r>'
        )
    return (
        f'<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f'<w:pPr>{h_style}{ind_xml}<w:spacing w:before="{space_before}" w:after="{space_after}" w:line="{line_spacing}" w:lineRule="auto"/><w:jc w:val="{jc}"/></w:pPr>'
        f'{"".join(r_xmls)}'
        f'</w:p>'
    )

def make_simple_p(text, style='Normal', bold=False, italic=False, color='000000', sz=24, space_before=80, space_after=80, line_spacing=276, jc='left', is_heading=False, left_indent=0):
    runs = parse_runs(text)
    if bold:
        runs = [(t, True, i, c) for t, b, i, c in runs]
    if italic:
        runs = [(t, b, True, c) for t, b, i, c in runs]
    return make_p_with_runs(runs, style=style, color=color, sz=sz, space_before=space_before, space_after=space_after, line_spacing=line_spacing, jc=jc, is_heading=is_heading, left_indent=left_indent)

def make_table(headers, rows, total_width=9360, hdr_bg="FFFFFF", border_col="000000"):
    num_cols = len(headers) if headers else (len(rows[0]) if rows else 1)
    col_lens = [len(h) for h in headers] if headers else [1]*num_cols
    for row in rows:
        for idx, cell in enumerate(row):
            if idx < len(col_lens):
                col_lens[idx] = max(col_lens[idx], len(cell))
            else:
                col_lens.append(len(cell))

    total_len = sum(col_lens) or 1
    col_widths = []
    if num_cols == 2:
        col_widths = [3000, total_width - 3000]
    elif num_cols == 3:
        col_widths = [2400, 3480, 3480]
    elif num_cols == 4:
        col_widths = [1900, 2460, 2600, 2400]
    elif num_cols == 5:
        col_widths = [1050, 1700, 2100, 2150, 2360]
    else:
        assigned = 0
        for l in col_lens[:-1]:
            w = max(int(total_width * (l / total_len)), 1200)
            col_widths.append(w)
            assigned += w
        col_widths.append(max(total_width - assigned, 1200))

    tbl_xml = [
        f'<w:tbl xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">',
        f'<w:tblPr><w:tblW w:w="{total_width}" w:type="dxa"/><w:jc w:val="center"/>',
        f'<w:tblBorders>'
        f'<w:top w:val="single" w:sz="6" w:space="0" w:color="{border_col}"/>'
        f'<w:left w:val="single" w:sz="6" w:space="0" w:color="{border_col}"/>'
        f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="{border_col}"/>'
        f'<w:right w:val="single" w:sz="6" w:space="0" w:color="{border_col}"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{border_col}"/>'
        f'<w:insideV w:val="single" w:sz="4" w:space="0" w:color="{border_col}"/>'
        f'</w:tblBorders></w:tblPr>',
        '<w:tblGrid>'
    ]
    for w in col_widths:
        tbl_xml.append(f'<w:gridCol w:w="{w}"/>')
    tbl_xml.append('</w:tblGrid>')

    if headers:
        h_cells = []
        for idx, h in enumerate(headers):
            runs = parse_runs(h)
            p_xml = make_p_with_runs([(r[0], True, r[2], r[3]) for r in runs], color="000000", sz=22, space_before=40, space_after=40, line_spacing=240)
            w = col_widths[idx]
            h_cells.append(
                f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/>'
                f'<w:tcMar><w:top w:w="80" w:type="dxa"/><w:bottom w:w="80" w:type="dxa"/><w:left w:w="120" w:type="dxa"/><w:right w:w="120" w:type="dxa"/></w:tcMar>'
                f'</w:tcPr>{p_xml}</w:tc>'
            )
        tbl_xml.append(f'<w:tr><w:trPr><w:tblHeader/></w:trPr>{"".join(h_cells)}</w:tr>')

    for row_idx, row in enumerate(rows):
        b_cells = []
        for idx, cell in enumerate(row):
            w = col_widths[idx] if idx < len(col_widths) else 1500
            runs = parse_runs(cell)
            if idx == 0 and not headers:
                runs = [(r[0], True, r[2], r[3]) for r in runs]
            p_xml = make_p_with_runs(runs, color="000000", sz=22, space_before=40, space_after=40, line_spacing=240)
            b_cells.append(
                f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/>'
                f'<w:tcMar><w:top w:w="60" w:type="dxa"/><w:bottom w:w="60" w:type="dxa"/><w:left w:w="120" w:type="dxa"/><w:right w:w="120" w:type="dxa"/></w:tcMar>'
                f'</w:tcPr>{p_xml}</w:tc>'
            )
        tbl_xml.append(f'<w:tr>{"".join(b_cells)}</w:tr>')
    tbl_xml.append('</w:tbl>')
    return ''.join(tbl_xml)

def sanitize_styles_xml(styles_xml_bytes):
    s = styles_xml_bytes.decode('utf-8')
    # Replace all color values in styles.xml with 000000 and strip themeColor/themeShade attributes
    s = re.sub(r'<w:color\b[^/>]*/>', '<w:color w:val="000000"/>', s)
    # Replace all font definitions in styles.xml with Times New Roman
    s = re.sub(
        r'<w:rFonts\b[^/>]*/>',
        '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman" w:eastAsia="Times New Roman"/>',
        s
    )
    return s.encode('utf-8')

def compile_markdown_to_docx(md_path, out_docx_path, template_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    body_parts = []
    i = 0
    while i < len(lines):
        raw_line = lines[i].rstrip('\r\n')
        sline = raw_line.strip()
        if not sline:
            i += 1
            continue

        if sline.startswith('# '):
            title = sline[2:].strip()
            body_parts.append(make_simple_p(title, style="Normal", bold=True, color="000000", sz=32, space_before=240, space_after=80, jc="center"))
            i += 1
            continue

        if sline.startswith('## ') and ('Project BugBountyTrack' in sline):
            sub = sline[3:].strip()
            body_parts.append(make_simple_p(sub, style="Normal", bold=True, color="000000", sz=26, space_before=40, space_after=60, jc="center"))
            i += 1
            continue

        if sline.startswith('**Document Release State**:') or sline.startswith('**Standard Compliance**:'):
            body_parts.append(make_simple_p(sline, style="Normal", bold=False, color="000000", sz=22, space_before=20, space_after=60, jc="center"))
            i += 1
            continue

        if sline == '---':
            i += 1
            continue

        if sline.startswith('#### '):
            h3_text = sline[5:].strip()
            body_parts.append(make_simple_p(h3_text, style="Heading3", bold=True, color="000000", sz=24, space_before=160, space_after=60, is_heading=True))
            i += 1
            continue

        if sline.startswith('### '):
            h2_text = sline[4:].strip()
            body_parts.append(make_simple_p(h2_text, style="Heading2", bold=True, color="000000", sz=26, space_before=200, space_after=80, is_heading=True))
            i += 1
            continue

        if sline.startswith('## '):
            h1_text = sline[3:].strip()
            body_parts.append(make_simple_p(h1_text, style="Heading1", bold=True, color="000000", sz=28, space_before=240, space_after=100, is_heading=True))
            i += 1
            continue

        if sline.startswith('> '):
            q_text = sline[2:].strip()
            body_parts.append(make_simple_p(q_text, color="000000", sz=24, space_before=100, space_after=100, jc="both", left_indent=360))
            i += 1
            continue

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

        if sline.startswith('* ') or sline.startswith('- '):
            b_text = sline[2:].strip()
            indent = 360 if raw_line.startswith('  ') else 0
            bullet = "◦  " if indent > 0 else "•  "
            body_parts.append(make_simple_p(f"{bullet}{b_text}", color="000000", sz=24, space_before=40, space_after=40, jc="both", left_indent=indent))
            i += 1
            continue

        if re.match(r'^\d+\.\s+', sline):
            body_parts.append(make_simple_p(sline, color="000000", sz=24, space_before=40, space_after=40, jc="both"))
            i += 1
            continue

        body_parts.append(make_simple_p(sline, color="000000", sz=24, space_before=80, space_after=80, jc="both"))
        i += 1

    with zipfile.ZipFile(template_path) as zin:
        file_map = {name: zin.read(name) for name in zin.namelist()}

    if 'word/styles.xml' in file_map:
        file_map['word/styles.xml'] = sanitize_styles_xml(file_map['word/styles.xml'])
    if 'word/stylesWithEffects.xml' in file_map:
        file_map['word/stylesWithEffects.xml'] = sanitize_styles_xml(file_map['word/stylesWithEffects.xml'])

    # Standard university 1-inch (1440 dxa) margins on US Letter (12240 x 15840 dxa)
    sectPr_xml = '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/></w:sectPr>'

    new_doc_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">\n'
        f'<w:body>{"".join(body_parts)}{sectPr_xml}</w:body>\n'
        '</w:document>'
    )
    file_map['word/document.xml'] = new_doc_xml.encode('utf-8')

    with zipfile.ZipFile(out_docx_path, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
        for name, content in file_map.items():
            zout.writestr(name, content)

    print(f"Generated {out_docx_path} ({os.path.getsize(out_docx_path)} bytes)")

if __name__ == '__main__':
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
    TEMPLATE = os.path.join(PROJECT_DIR, 'Resources', 'BRD.docx')

    targets = [
        ('WEEK_1_PART_A_USER_PERSONAS.md', 'WEEK_1_PART_A_USER_PERSONAS.docx'),
        ('WEEK_1_PART_B_CHARTER_AND_MVP.md', 'WEEK_1_PART_B_CHARTER_AND_MVP.docx'),
    ]
    for md_name, docx_name in targets:
        md_file = os.path.join(SCRIPT_DIR, md_name)
        docx_file = os.path.join(SCRIPT_DIR, docx_name)
        compile_markdown_to_docx(md_file, docx_file, TEMPLATE)
        res_copy = os.path.join(PROJECT_DIR, 'Resources', docx_name)
        shutil.copy2(docx_file, res_copy)
        print(f"Copied to {res_copy}")
