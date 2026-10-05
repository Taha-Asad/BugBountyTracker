import zipfile, os, re, xml.sax.saxutils as saxutils

def escape(txt):
    return saxutils.escape(str(txt))

def clean_text(txt):
    if not txt:
        return ""
    # Strip LaTeX math artifacts
    t = txt
    t = t.replace(r'\ge', '≥')
    t = t.replace(r'\le', '≤')
    t = t.replace(r'\text{', '').replace(r'}', '')
    t = t.replace(r'\$', '$')
    t = re.sub(r'\$([^$]+)\$', r'\1', t) # strip inline $...$
    t = t.replace('$$', '')
    return t

def parse_runs(text):
    """Parses a string into a list of tuples: (text, is_bold, is_italic, is_code)"""
    text = clean_text(text)
    # Tokenize by bold **...** and code `...`
    # Simple regex-based splitter
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

def make_p_with_runs(runs, style='Normal', color='222222', sz=20, space_before=60, space_after=60, jc='left', is_heading=False):
    h_style = f'<w:pStyle w:val="{style}"/>' if is_heading else ''
    r_xmls = []
    for r_text, bold, italic, code in runs:
        r_text_escaped = escape(r_text)
        b_tag = '<w:b/>' if bold else ''
        i_tag = '<w:i/>' if italic else ''
        f_tag = '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>' if code else '<w:rFonts w:ascii="Lexend" w:hAnsi="Lexend"/>'
        c_tag = f'<w:color w:val="{color}"/>'
        if code:
            c_tag = '<w:color w:val="9C4146"/>'
        r_xmls.append(
            f'<w:r>'
            f'<w:rPr>{f_tag}{b_tag}{i_tag}{c_tag}<w:sz w:val="{sz}"/></w:rPr>'
            f'<w:t xml:space="preserve">{r_text_escaped}</w:t>'
            f'</w:r>'
        )
    return (
        f'<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f'<w:pPr>{h_style}<w:spacing w:before="{space_before}" w:after="{space_after}"/><w:jc w:val="{jc}"/></w:pPr>'
        f'{"".join(r_xmls)}'
        f'</w:p>'
    )

def make_simple_p(text, style='Normal', bold=False, italic=False, color='222222', sz=20, space_before=60, space_after=60, jc='left', is_heading=False):
    runs = parse_runs(text)
    if bold:
        runs = [(t, True, i, c) for t, b, i, c in runs]
    return make_p_with_runs(runs, style=style, color=color, sz=sz, space_before=space_before, space_after=space_after, jc=jc, is_heading=is_heading)

def make_table(headers, rows, total_width=9936, hdr_bg="E3EFCB", border_col="D1E3A5"):
    num_cols = len(headers) if headers else (len(rows[0]) if rows else 1)
    # Estimate column proportions
    col_lens = [len(h) for h in headers] if headers else [1]*num_cols
    for row in rows:
        for idx, cell in enumerate(row):
            if idx < len(col_lens):
                col_lens[idx] = max(col_lens[idx], len(cell))
            else:
                col_lens.append(len(cell))
    
    total_len = sum(col_lens)
    if total_len == 0:
        total_len = 1
    
    # Assign widths proportionally with min width
    col_widths = []
    if num_cols == 2:
        col_widths = [3200, total_width - 3200]
    elif num_cols == 4:
        col_widths = [1600, 2600, 3200, 2536]
    else:
        assigned = 0
        for l in col_lens[:-1]:
            w = int(total_width * (l / total_len))
            w = max(w, 1200)
            col_widths.append(w)
            assigned += w
        col_widths.append(max(total_width - assigned, 1200))

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
            p_xml = make_p_with_runs([(r[0], True, r[2], r[3]) for r in runs], color="1B2A1E", sz=19, space_before=40, space_after=40)
            w = col_widths[idx]
            h_cells.append(
                f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/>'
                f'<w:shd w:val="clear" w:fill="{hdr_bg}"/>'
                f'<w:tcMar><w:top w:w="80" w:type="dxa"/><w:bottom w:w="80" w:type="dxa"/><w:left w:w="120" w:type="dxa"/><w:right w:w="120" w:type="dxa"/></w:tcMar>'
                f'</w:tcPr>{p_xml}</w:tc>'
            )
        tbl_xml.append(f'<w:tr><w:trPr><w:tblHeader/></w:trPr>{"".join(h_cells)}</w:tr>')

    for row_idx, row in enumerate(rows):
        b_cells = []
        row_bg = "F9FBF6" if row_idx % 2 == 1 else "FFFFFF"
        for idx, cell in enumerate(row):
            w = col_widths[idx] if idx < len(col_widths) else 1500
            runs = parse_runs(cell)
            is_first_col = (idx == 0 and not headers)
            if is_first_col:
                runs = [(r[0], True, r[2], r[3]) for r in runs]
            p_xml = make_p_with_runs(runs, color="222222", sz=18, space_before=30, space_after=30)
            shd_xml = f'<w:shd w:val="clear" w:fill="{row_bg}"/>' if row_bg != "FFFFFF" else ''
            b_cells.append(
                f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/>{shd_xml}'
                f'<w:tcMar><w:top w:w="60" w:type="dxa"/><w:bottom w:w="60" w:type="dxa"/><w:left w:w="120" w:type="dxa"/><w:right w:w="120" w:type="dxa"/></w:tcMar>'
                f'</w:tcPr>{p_xml}</w:tc>'
            )
        tbl_xml.append(f'<w:tr>{"".join(b_cells)}</w:tr>')
    tbl_xml.append('</w:tbl>')
    return ''.join(tbl_xml)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))

brd_md_path = os.path.join(SCRIPT_DIR, 'BRD.md')
with open(brd_md_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

body_parts = []
i = 0
while i < len(lines):
    line = lines[i].rstrip('\r\n')
    sline = line.strip()
    if not sline:
        i += 1
        continue
    
    if sline.startswith('# '):
        title = sline[2:].strip()
        body_parts.append(make_simple_p(title, style="Normal", bold=True, color="386B24", sz=40, space_before=300, space_after=80, jc="center"))
        i += 1
        continue
    
    if sline.startswith('## ') and ('Project BugBountyTrack' in sline or 'Document Release' in sline):
        sub = sline[3:].strip()
        body_parts.append(make_simple_p(sub, style="Normal", bold=True, color="5A6652", sz=22, space_before=40, space_after=60, jc="center"))
        i += 1
        continue
    
    if sline.startswith('**Document Release State**:'):
        body_parts.append(make_simple_p(sline, style="Normal", bold=False, color="78827D", sz=19, space_before=20, space_after=40, jc="center"))
        i += 1
        continue

    if sline.startswith('**Standard Compliance**:'):
        body_parts.append(make_simple_p(sline, style="Normal", bold=False, color="78827D", sz=19, space_before=20, space_after=140, jc="center"))
        i += 1
        continue

    if sline == '---':
        i += 1
        continue
    
    if sline.startswith('## '):
        h1_text = sline[3:].strip()
        body_parts.append(make_simple_p(h1_text, style="Heading1", bold=True, color="386B24", sz=26, space_before=240, space_after=80, is_heading=True))
        i += 1
        continue

    if sline.startswith('### '):
        h2_text = sline[4:].strip()
        body_parts.append(make_simple_p(h2_text, style="Heading2", bold=True, color="2B4C1A", sz=22, space_before=180, space_after=60, is_heading=True))
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
        body_parts.append(make_simple_p("", space_before=60, space_after=60))
        continue
    
    # Bullet points
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

# Read template docx to preserve all other files
template_path = os.path.join(PROJECT_DIR, 'Resources', 'BRD.docx')
with zipfile.ZipFile(template_path) as zin:
    file_map = {name: zin.read(name) for name in zin.namelist()}

# Preserve sectPr from original
orig_doc = file_map['word/document.xml'].decode('utf-8')
sectPr_match = re.search(r'<w:sectPr.*?</w:sectPr>', orig_doc)
sectPr_xml = sectPr_match.group(0) if sectPr_match else '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1152" w:right="1152" w:bottom="1152" w:left="1152"/></w:sectPr>'

new_doc_xml = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">\n'
    f'<w:body>{"".join(body_parts)}{sectPr_xml}</w:body>\n'
    '</w:document>'
)

file_map['word/document.xml'] = new_doc_xml.encode('utf-8')

out_path = os.path.join(SCRIPT_DIR, 'BRD.docx')
with zipfile.ZipFile(out_path, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
    for name, content in file_map.items():
        zout.writestr(name, content)

print(f"Generated {out_path} ({os.path.getsize(out_path)} bytes)")
