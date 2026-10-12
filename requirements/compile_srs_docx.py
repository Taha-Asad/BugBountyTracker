#!/usr/bin/env python3
"""
Compiles projects/BugBountyTrack/requirements/SRS.md into a university-standard
Word document (SRS.docx) with:
- Font: Times New Roman across all headings, body text, tables, code blocks, headers, and footers
- Color: Pure black (#000000) across all text, borders, headers, and footers (zero colored accents)
- Margins: 1-inch (1440 dxa) on all sides
- Tables: Full printable width (9360 dxa), solid black 1/2-pt borders, unshaded cells
- Diagrams: All 6 high-DPI monochrome PNG diagrams embedded with exact native aspect ratio (cx/cy)
"""
import os
import re
import shutil
import struct
import zipfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
FONT_NAME = "Times New Roman"
TEXT_COLOR = "000000"
BORDER_COLOR = "000000"

with open(os.path.join(SCRIPT_DIR, "SRS.md"), "r", encoding="utf-8") as f:
    md_text = f.read()


def xml_escape(s):
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def strip_md_links(text):
    """Converts [label](url) to label (or label (url) for external https links)."""
    def repl(m):
        label, url = m.group(1), m.group(2)
        if url.startswith("http://") or url.startswith("https://"):
            if label == url:
                return label
            return f"{label} ({url})"
        return label

    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl, text)


def make_rPr(bold=False, italic=False, sz=22, underline=False):
    b_xml = '<w:b/><w:bCs/>' if bold else '<w:b w:val="0"/><w:bCs w:val="0"/>'
    i_xml = '<w:i/><w:iCs/>' if italic else '<w:i w:val="0"/><w:iCs w:val="0"/>'
    u_xml = '<w:u w:val="single"/>' if underline else '<w:u w:val="none"/>'
    return (
        f"<w:rPr>"
        f'<w:rFonts w:ascii="{FONT_NAME}" w:cs="{FONT_NAME}" w:eastAsia="{FONT_NAME}" w:hAnsi="{FONT_NAME}"/>'
        f"{b_xml}{i_xml}{u_xml}"
        f'<w:color w:val="{TEXT_COLOR}"/>'
        f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>'
        f"</w:rPr>"
    )


def parse_inline_runs(text, base_bold=False, base_italic=False, sz=22):
    """Parses **bold**, `code`, and *italic* into Times New Roman #000000 runs."""
    text = strip_md_links(text)
    tokens = re.split(r"(\*\*.*?\*\*|`.*?`|\*[^\*]+?\*)", text)
    runs = []
    for tok in tokens:
        if not tok:
            continue
        if tok.startswith("**") and tok.endswith("**") and len(tok) > 4:
            content = xml_escape(tok[2:-2])
            rPr = make_rPr(bold=True, italic=base_italic, sz=sz)
            runs.append(f'<w:r>{rPr}<w:t xml:space="preserve">{content}</w:t></w:r>')
        elif tok.startswith("`") and tok.endswith("`") and len(tok) > 2:
            content = xml_escape(tok[1:-1])
            rPr = make_rPr(bold=base_bold, italic=base_italic, sz=sz)
            runs.append(f'<w:r>{rPr}<w:t xml:space="preserve">{content}</w:t></w:r>')
        elif tok.startswith("*") and tok.endswith("*") and len(tok) > 2:
            content = xml_escape(tok[1:-1])
            rPr = make_rPr(bold=base_bold, italic=True, sz=sz)
            runs.append(f'<w:r>{rPr}<w:t xml:space="preserve">{content}</w:t></w:r>')
        else:
            content = xml_escape(tok)
            rPr = make_rPr(bold=base_bold, italic=base_italic, sz=sz)
            runs.append(f'<w:r>{rPr}<w:t xml:space="preserve">{content}</w:t></w:r>')
    return "".join(runs)


def make_p(
    text,
    bold=False,
    italic=False,
    sz=22,
    space_before=60,
    space_after=80,
    jc="left",
    keep_next=False,
    bottom_border=False,
    left_border=False,
    left_indent=0,
    line_spacing=276,
):
    kn = "<w:keepNext/>" if keep_next else ""
    bdr_parts = []
    if bottom_border:
        bdr_parts.append(
            f'<w:bottom w:val="single" w:sz="6" w:space="4" w:color="{BORDER_COLOR}"/>'
        )
    if left_border:
        bdr_parts.append(
            f'<w:left w:val="single" w:sz="12" w:space="8" w:color="{BORDER_COLOR}"/>'
        )
    bdr = f'<w:pBdr>{"".join(bdr_parts)}</w:pBdr>' if bdr_parts else ""
    ind = f'<w:ind w:left="{left_indent}"/>' if left_indent else ""
    pPr = (
        f"<w:pPr>{kn}{bdr}"
        f'<w:spacing w:before="{space_before}" w:after="{space_after}" w:line="{line_spacing}" w:lineRule="auto"/>'
        f"{ind}"
        f'<w:jc w:val="{jc}"/>'
        f"</w:pPr>"
    )
    runs = parse_inline_runs(text, base_bold=bold, base_italic=italic, sz=sz)
    return f"<w:p>{pPr}{runs}</w:p>"


def make_hr_p():
    return (
        "<w:p><w:pPr>"
        f'<w:pBdr><w:bottom w:val="single" w:sz="6" w:space="1" w:color="{BORDER_COLOR}"/></w:pBdr>'
        '<w:spacing w:before="80" w:after="80"/>'
        "</w:pPr></w:p>"
    )


def make_table(rows):
    if not rows:
        return ""
    num_cols = max(len(r) for r in rows)
    total_width = 9360  # 6.5 inches in dxa (twips)

    if num_cols == 2:
        col_widths = [2600, 6760]
    elif num_cols == 3:
        col_widths = [2200, 2600, 4560]
    elif num_cols == 4:
        col_widths = [1400, 2200, 3960, 1800]
    elif num_cols == 5:
        col_widths = [1100, 1800, 2960, 2100, 1400]
    elif num_cols == 6:
        col_widths = [950, 1550, 1800, 1750, 1750, 1560]
    elif num_cols == 7:
        col_widths = [900, 1250, 1500, 1550, 1550, 1550, 1060]
    else:
        w = total_width // num_cols
        col_widths = [w] * num_cols

    grid_cols = "".join(f'<w:gridCol w:w="{w}"/>' for w in col_widths)
    tblPr = (
        "<w:tblPr>"
        f'<w:tblW w:w="{total_width}" w:type="dxa"/>'
        '<w:jc w:val="left"/>'
        "<w:tblBorders>"
        f'<w:top w:val="single" w:sz="6" w:space="0" w:color="{BORDER_COLOR}"/>'
        f'<w:left w:val="single" w:sz="6" w:space="0" w:color="{BORDER_COLOR}"/>'
        f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="{BORDER_COLOR}"/>'
        f'<w:right w:val="single" w:sz="6" w:space="0" w:color="{BORDER_COLOR}"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{BORDER_COLOR}"/>'
        f'<w:insideV w:val="single" w:sz="4" w:space="0" w:color="{BORDER_COLOR}"/>'
        "</w:tblBorders>"
        "<w:tblCellMar>"
        '<w:top w:w="80" w:type="dxa"/>'
        '<w:left w:w="100" w:type="dxa"/>'
        '<w:bottom w:w="80" w:type="dxa"/>'
        '<w:right w:w="100" w:type="dxa"/>'
        "</w:tblCellMar>"
        "</w:tblPr>"
    )

    tr_list = []
    for r_idx, row in enumerate(rows):
        is_header = r_idx == 0
        trPr = "<w:trPr><w:tblHeader/></w:trPr>" if is_header else "<w:trPr/>"
        tc_list = []
        for c_idx in range(num_cols):
            cell_text = row[c_idx].strip() if c_idx < len(row) else ""
            w = col_widths[c_idx]
            tcPr = (
                f"<w:tcPr>"
                f'<w:tcW w:w="{w}" w:type="dxa"/>'
                f'<w:shd w:val="clear" w:color="auto" w:fill="FFFFFF"/>'
                f'<w:vAlign w:val="top"/>'
                f"</w:tcPr>"
            )
            pPr = '<w:pPr><w:spacing w:before="30" w:after="30" w:line="240" w:lineRule="auto"/><w:jc w:val="left"/></w:pPr>'
            runs = parse_inline_runs(
                cell_text, base_bold=is_header, sz=19 if num_cols >= 5 else 20
            )
            tc_list.append(f"<w:tc>{tcPr}<w:p>{pPr}{runs}</w:p></w:tc>")
        tr_list.append(f'<w:tr>{trPr}{"".join(tc_list)}</w:tr>')

    return (
        f"<w:tbl>{tblPr}<w:tblGrid>{grid_cols}</w:tblGrid>{''.join(tr_list)}</w:tbl>"
        + '<w:p><w:pPr><w:spacing w:before="40" w:after="40"/></w:pPr></w:p>'
    )


def get_png_dimensions(png_path):
    """Reads exact (width, height) in pixels from a PNG file's IHDR chunk."""
    with open(png_path, "rb") as f:
        header = f.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"Invalid PNG file: {png_path}")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def make_image_p(rel_id, doc_pr_id, name, png_path):
    """
    Computes exact aspect-ratio-locked EMU dimensions (cx, cy) from the PNG pixel dimensions
    bounded by MAX_CX = 5,852,160 EMU (6.40 inches) and MAX_CY = 6,583,680 EMU (7.20 inches).
    """
    width_px, height_px = get_png_dimensions(png_path)
    max_cx = 5852160  # 6.40 inches in EMUs
    max_cy = 6583680  # 7.20 inches in EMUs

    # Start by fitting to full printable width
    cx = max_cx
    cy = int(round(max_cx * (height_px / float(width_px))))

    # If height exceeds max_cy (e.g., portrait diagram), scale down proportionally
    if cy > max_cy:
        cy = max_cy
        cx = int(round(max_cy * (width_px / float(height_px))))

    return (
        '<w:p><w:pPr><w:spacing w:before="120" w:after="120"/><w:jc w:val="center"/></w:pPr>'
        "<w:r><w:rPr><w:noProof/></w:rPr>"
        '<w:drawing xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<wp:inline distT="0" distB="0" distL="0" distR="0">'
        f'<wp:extent cx="{cx}" cy="{cy}"/>'
        '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
        f'<wp:docPr id="{doc_pr_id}" name="{xml_escape(name)}" descr="{xml_escape(name)}"/>'
        "<wp:cNvGraphicFramePr>"
        '<a:graphicFrameLocks noChangeAspect="1"/>'
        "</wp:cNvGraphicFramePr>"
        "<a:graphic>"
        '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        "<pic:pic>"
        "<pic:nvPicPr>"
        f'<pic:cNvPr id="{doc_pr_id}" name="{xml_escape(name)}"/>'
        '<pic:cNvPicPr><a:picLocks noChangeAspect="1" noChangeArrowheads="1"/></pic:cNvPicPr>'
        "</pic:nvPicPr>"
        "<pic:blipFill>"
        f'<a:blip r:embed="{rel_id}"/>'
        "<a:stretch><a:fillRect/></a:stretch>"
        "</pic:blipFill>"
        "<pic:spPr>"
        f'<a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        "</pic:spPr>"
        "</pic:pic>"
        "</a:graphicData>"
        "</a:graphic>"
        "</wp:inline>"
        "</w:drawing>"
        "</w:r></w:p>"
    )


diagram_files = {
    "rId201": (
        "word/media/fig4_2_usecase.png",
        os.path.join(SCRIPT_DIR, "diagrams", "fig4_2_usecase.png"),
        201,
        "Figure 4.1 System Use Case Diagram",
    ),
    "rId202": (
        "word/media/fig4_3_seq_submission.png",
        os.path.join(SCRIPT_DIR, "diagrams", "fig4_3_seq_submission.png"),
        202,
        "Figure 4.2 Sequence Diagram Submission",
    ),
    "rId203": (
        "word/media/fig4_4_seq_decryption.png",
        os.path.join(SCRIPT_DIR, "diagrams", "fig4_4_seq_decryption.png"),
        203,
        "Figure 4.3 Sequence Diagram Decryption",
    ),
    "rId204": (
        "word/media/fig4_5_statemachine.png",
        os.path.join(SCRIPT_DIR, "diagrams", "fig4_5_statemachine.png"),
        204,
        "Figure 4.4 Report Lifecycle State Machine",
    ),
}

section_diagram_map = {
    "4.2 ": "rId201",
    "4.3 ": "rId202",
    "4.4 ": "rId203",
    "4.5 ": "rId204",
}

lines = md_text.splitlines()
body_parts = []
i = 0
in_code_block = False
code_block_lang = ""
code_block_lines = []
current_section_prefix = None
inserted_diagrams = set()

while i < len(lines):
    line = lines[i]
    sline = line.strip()

    # Handle fenced code blocks
    if sline.startswith("```"):
        if not in_code_block:
            in_code_block = True
            code_block_lang = sline[3:].strip().lower()
            code_block_lines = []
        else:
            in_code_block = False
            if code_block_lang == "mermaid":
                # Replace mermaid block with its corresponding rendered PNG diagram
                if (
                    current_section_prefix
                    and current_section_prefix in section_diagram_map
                ):
                    rid = section_diagram_map[current_section_prefix]
                    if rid not in inserted_diagrams:
                        _, png_path, doc_id, d_name = diagram_files[rid]
                        body_parts.append(make_image_p(rid, doc_id, d_name, png_path))
                        inserted_diagrams.add(rid)
            else:
                # Render non-mermaid code block (e.g., FR-7.1 state transition grammar)
                for cline in code_block_lines:
                    if cline.strip():
                        body_parts.append(
                            make_p(
                                cline.strip(),
                                sz=20,
                                space_before=20,
                                space_after=20,
                                left_border=True,
                                left_indent=360,
                                line_spacing=240,
                            )
                        )
        i += 1
        continue

    if in_code_block:
        code_block_lines.append(line)
        i += 1
        continue

    # Skip markdown image links since we embed the PNG directly via section_diagram_map
    if sline.startswith("!["):
        if current_section_prefix and current_section_prefix in section_diagram_map:
            rid = section_diagram_map[current_section_prefix]
            if rid not in inserted_diagrams:
                _, png_path, doc_id, d_name = diagram_files[rid]
                body_parts.append(make_image_p(rid, doc_id, d_name, png_path))
                inserted_diagrams.add(rid)
        i += 1
        continue

    if not sline:
        i += 1
        continue

    if sline == "---":
        body_parts.append(make_hr_p())
        i += 1
        continue

    # Blockquotes
    if sline.startswith(">"):
        q_text = sline.lstrip(">").strip()
        if q_text:
            body_parts.append(
                make_p(
                    q_text,
                    italic=True,
                    sz=21,
                    space_before=40,
                    space_after=40,
                    left_border=True,
                    left_indent=360,
                )
            )
        i += 1
        continue

    # Markdown Tables
    if sline.startswith("|") and sline.endswith("|"):
        table_lines = []
        while (
            i < len(lines)
            and lines[i].strip().startswith("|")
            and lines[i].strip().endswith("|")
        ):
            table_lines.append(lines[i].strip())
            i += 1
        parsed_rows = []
        for tl in table_lines:
            cells = [c.strip() for c in tl.strip("|").split("|")]
            if all(re.match(r"^[:\-]+$", c) for c in cells if c):
                continue
            parsed_rows.append(cells)
        if parsed_rows:
            body_parts.append(make_table(parsed_rows))
        continue

    # Headings
    if sline.startswith("# "):
        h_text = sline[2:].strip()
        body_parts.append(
            make_p(
                h_text,
                bold=True,
                sz=32,
                space_before=120,
                space_after=120,
                jc="center",
                keep_next=True,
                bottom_border=True,
            )
        )
        i += 1
        continue

    if sline.startswith("## "):
        h_text = sline[3:].strip()
        body_parts.append(
            make_p(
                h_text,
                bold=True,
                sz=28,
                space_before=240,
                space_after=100,
                keep_next=True,
                bottom_border=True,
            )
        )
        i += 1
        continue

    if sline.startswith("### "):
        h_text = sline[4:].strip()
        current_section_prefix = None
        for prefix in section_diagram_map:
            if h_text.startswith(prefix):
                current_section_prefix = prefix
                break
        body_parts.append(
            make_p(
                h_text,
                bold=True,
                sz=24,
                space_before=180,
                space_after=80,
                keep_next=True,
            )
        )
        i += 1
        continue

    if sline.startswith("#### "):
        h_text = sline[5:].strip()
        body_parts.append(
            make_p(
                h_text,
                bold=True,
                sz=22,
                space_before=140,
                space_after=60,
                keep_next=True,
            )
        )
        i += 1
        continue

    # Bullet points
    if sline.startswith("* ") or sline.startswith("- ") or sline.startswith("• "):
        b_text = sline[2:].strip()
        indent = 720 if line.startswith("  ") or line.startswith("\t") else 360
        bullet_char = "◦  " if indent > 360 else "•  "
        body_parts.append(
            make_p(
                f"{bullet_char}{b_text}",
                sz=22,
                space_before=30,
                space_after=30,
                left_indent=indent,
            )
        )
        i += 1
        continue

    # Numbered lists
    if re.match(r"^\d+\.\s+", sline):
        indent = 720 if line.startswith("  ") or line.startswith("\t") else 360
        body_parts.append(
            make_p(
                sline,
                sz=22,
                space_before=30,
                space_after=30,
                left_indent=indent,
            )
        )
        i += 1
        continue

    # Standard Paragraph
    body_parts.append(make_p(sline, sz=22, space_before=60, space_after=80))
    i += 1

print(f"Parsed {len(lines)} lines into {len(body_parts)} body elements.")
print(f"Inserted diagrams: {sorted(list(inserted_diagrams))}")

sectPr_xml = (
    "<w:sectPr>"
    '<w:headerReference w:type="default" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:id="rId1"/>'
    '<w:footerReference w:type="default" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:id="rId2"/>'
    '<w:pgSz w:w="12240" w:h="15840"/>'
    '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>'
    "</w:sectPr>"
)

doc_xml = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">\n'
    f'<w:body>{"".join(body_parts)}{sectPr_xml}</w:body>\n'
    "</w:document>"
)

header_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:hdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:p>
    <w:pPr>
      <w:pBdr><w:bottom w:val="single" w:sz="4" w:space="4" w:color="{BORDER_COLOR}"/></w:pBdr>
      <w:spacing w:before="0" w:after="60"/>
      <w:jc w:val="right"/>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="{FONT_NAME}" w:cs="{FONT_NAME}" w:eastAsia="{FONT_NAME}" w:hAnsi="{FONT_NAME}"/>
        <w:i/>
        <w:color w:val="{TEXT_COLOR}"/>
        <w:sz w:val="18"/><w:szCs w:val="18"/>
      </w:rPr>
      <w:t>BugBountyTrack — IEEE 830 Software Requirements Specification (SRS Revision 2.5)</w:t>
    </w:r>
  </w:p>
</w:hdr>"""

footer_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:p>
    <w:pPr>
      <w:pBdr><w:top w:val="single" w:sz="4" w:space="4" w:color="{BORDER_COLOR}"/></w:pBdr>
      <w:tabs><w:tab w:val="right" w:pos="9360"/></w:tabs>
      <w:spacing w:before="60" w:after="0"/>
      <w:jc w:val="left"/>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="{FONT_NAME}" w:cs="{FONT_NAME}" w:eastAsia="{FONT_NAME}" w:hAnsi="{FONT_NAME}"/>
        <w:i/>
        <w:color w:val="{TEXT_COLOR}"/>
        <w:sz w:val="18"/><w:szCs w:val="18"/>
      </w:rPr>
      <w:t xml:space="preserve">Prepared for Academic &amp; Technical Review — Taha Asadullah</w:t>
    </w:r>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="{FONT_NAME}" w:cs="{FONT_NAME}" w:eastAsia="{FONT_NAME}" w:hAnsi="{FONT_NAME}"/>
        <w:color w:val="{TEXT_COLOR}"/>
        <w:sz w:val="18"/><w:szCs w:val="18"/>
      </w:rPr>
      <w:tab/>
      <w:t xml:space="preserve">Page </w:t>
    </w:r>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="{FONT_NAME}" w:cs="{FONT_NAME}" w:eastAsia="{FONT_NAME}" w:hAnsi="{FONT_NAME}"/>
        <w:color w:val="{TEXT_COLOR}"/>
        <w:sz w:val="18"/><w:szCs w:val="18"/>
      </w:rPr>
      <w:fldChar w:fldCharType="begin"/>
      <w:instrText xml:space="preserve">PAGE</w:instrText>
      <w:fldChar w:fldCharType="separate"/>
      <w:fldChar w:fldCharType="end"/>
    </w:r>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="{FONT_NAME}" w:cs="{FONT_NAME}" w:eastAsia="{FONT_NAME}" w:hAnsi="{FONT_NAME}"/>
        <w:color w:val="{TEXT_COLOR}"/>
        <w:sz w:val="18"/><w:szCs w:val="18"/>
      </w:rPr>
      <w:t xml:space="preserve"> of </w:t>
    </w:r>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="{FONT_NAME}" w:cs="{FONT_NAME}" w:eastAsia="{FONT_NAME}" w:hAnsi="{FONT_NAME}"/>
        <w:color w:val="{TEXT_COLOR}"/>
        <w:sz w:val="18"/><w:szCs w:val="18"/>
      </w:rPr>
      <w:fldChar w:fldCharType="begin"/>
      <w:instrText xml:space="preserve">NUMPAGES</w:instrText>
      <w:fldChar w:fldCharType="separate"/>
      <w:fldChar w:fldCharType="end"/>
    </w:r>
  </w:p>
</w:ftr>"""

styles_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="{FONT_NAME}" w:cs="{FONT_NAME}" w:eastAsia="{FONT_NAME}" w:hAnsi="{FONT_NAME}"/>
        <w:color w:val="{TEXT_COLOR}"/>
        <w:sz w:val="22"/>
        <w:szCs w:val="22"/>
        <w:lang w:val="en-US" w:eastAsia="en-US" w:bidi="ar-SA"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr>
        <w:spacing w:after="80" w:line="276" w:lineRule="auto"/>
      </w:pPr>
    </w:pPrDefault>
  </w:docDefaults>
</w:styles>"""

settings_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:zoom w:percent="100"/>
  <w:defaultTabStop w:val="720"/>
  <w:characterSpacingControl w:val="doNotCompress"/>
  <w:compat>
    <w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/>
  </w:compat>
</w:settings>"""

content_types_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
  <Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>
  <Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>
</Types>"""

root_rels_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

doc_rels_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>
  <Relationship Id="rId201" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/fig4_2_usecase.png"/>
  <Relationship Id="rId202" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/fig4_3_seq_submission.png"/>
  <Relationship Id="rId203" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/fig4_4_seq_decryption.png"/>
  <Relationship Id="rId204" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/fig4_5_statemachine.png"/>
</Relationships>"""

target_docx = os.path.join(SCRIPT_DIR, "SRS.docx")
with zipfile.ZipFile(target_docx, "w", compression=zipfile.ZIP_DEFLATED) as zout:
    zout.writestr("[Content_Types].xml", content_types_xml.encode("utf-8"))
    zout.writestr("_rels/.rels", root_rels_xml.encode("utf-8"))
    zout.writestr("word/document.xml", doc_xml.encode("utf-8"))
    zout.writestr("word/_rels/document.xml.rels", doc_rels_xml.encode("utf-8"))
    zout.writestr("word/styles.xml", styles_xml.encode("utf-8"))
    zout.writestr("word/settings.xml", settings_xml.encode("utf-8"))
    zout.writestr("word/header1.xml", header_xml.encode("utf-8"))
    zout.writestr("word/footer1.xml", footer_xml.encode("utf-8"))
    for rid, (zip_path, local_path, _, _) in diagram_files.items():
        if os.path.exists(local_path):
            with open(local_path, "rb") as img_f:
                zout.writestr(zip_path, img_f.read())
        else:
            raise FileNotFoundError(f"Missing diagram image: {local_path}")

resources_docx = os.path.join(PROJECT_DIR, "Resources", "SRS.docx")
shutil.copy2(target_docx, resources_docx)

print(
    f"Successfully generated {target_docx} ({os.path.getsize(target_docx)} bytes) and synchronized {resources_docx}"
)
