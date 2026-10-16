#!/usr/bin/env python3
"""
Compiles projects/BugBountyTrack/architecture/HIGH_LEVEL_ARCHITECTURE.md into a university-standard
Word document (HIGH_LEVEL_ARCHITECTURE.docx) with:
- Font: Times New Roman across all headings, body text, tables, code blocks, headers, and footers
- Color: Pure black (#000000) across all text, borders, headers, and footers (zero colored accents)
- Margins: 1-inch (1440 dxa) on all sides
- Tables: Full printable width (9360 dxa), solid black 1/2-pt borders, unshaded cells
- Diagrams: All 4 high-DPI monochrome PNG diagrams embedded with exact aspect ratio
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
):
    pPr_parts = [
        f'<w:spacing w:before="{space_before}" w:after="{space_after}" w:line="240" w:lineRule="auto"/>',
        f'<w:jc w:val="{jc}"/>',
    ]
    if keep_next:
        pPr_parts.append("<w:keepNext/>")
    if left_indent > 0:
        pPr_parts.append(f'<w:ind w:left="{left_indent}"/>')
    if bottom_border:
        pPr_parts.append(
            f'<w:pBdr><w:bottom w:val="single" w:sz="6" w:space="4" w:color="{BORDER_COLOR}"/></w:pBdr>'
        )
    if left_border:
        pPr_parts.append(
            f'<w:pBdr><w:left w:val="single" w:sz="18" w:space="8" w:color="{BORDER_COLOR}"/></w:pBdr>'
        )

    pPr_xml = f"<w:pPr>{''.join(pPr_parts)}</w:pPr>"
    runs_xml = parse_inline_runs(text, base_bold=bold, base_italic=italic, sz=sz)
    return f"<w:p>{pPr_xml}{runs_xml}</w:p>"


def make_code_block_p(text):
    escaped = xml_escape(text)
    rPr = make_rPr(bold=False, italic=False, sz=18)
    pPr = (
        '<w:pPr>'
        '<w:spacing w:before="0" w:after="0" w:line="200" w:lineRule="auto"/>'
        '<w:ind w:left="360"/>'
        '</w:pPr>'
    )
    return f'<w:p>{pPr}<w:r>{rPr}<w:t xml:space="preserve">{escaped}</w:t></w:r></w:p>'


def make_hr_p():
    return (
        "<w:p>"
        "<w:pPr>"
        f'<w:pBdr><w:bottom w:val="single" w:sz="12" w:space="1" w:color="{BORDER_COLOR}"/></w:pBdr>'
        '<w:spacing w:before="120" w:after="120"/>'
        "</w:pPr>"
        "</w:p>"
    )


def make_table(rows):
    if not rows:
        return ""
    col_count = max(len(r) for r in rows)
    total_w = 9360
    base_w = total_w // col_count
    col_widths = [base_w] * col_count
    col_widths[-1] += total_w - sum(col_widths)

    grid_cols = "".join(f'<w:gridCol w:w="{w}"/>' for w in col_widths)
    tblGrid = f"<w:tblGrid>{grid_cols}</w:tblGrid>"

    tblBorders = (
        f"<w:tblBorders>"
        f'<w:top w:val="single" w:sz="6" w:space="0" w:color="{BORDER_COLOR}"/>'
        f'<w:left w:val="single" w:sz="6" w:space="0" w:color="{BORDER_COLOR}"/>'
        f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="{BORDER_COLOR}"/>'
        f'<w:right w:val="single" w:sz="6" w:space="0" w:color="{BORDER_COLOR}"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{BORDER_COLOR}"/>'
        f'<w:insideV w:val="single" w:sz="4" w:space="0" w:color="{BORDER_COLOR}"/>'
        f"</w:tblBorders>"
    )

    tblPr = (
        f"<w:tblPr>"
        f'<w:tblW w:w="{total_w}" w:type="dxa"/>'
        f"{tblBorders}"
        f'<w:tblLayout w:type="fixed"/>'
        f"<w:tblCellMar>"
        f'<w:top w:w="80" w:type="dxa"/>'
        f'<w:left w:w="120" w:type="dxa"/>'
        f'<w:bottom w:w="80" w:type="dxa"/>'
        f'<w:right w:w="120" w:type="dxa"/>'
        f"</w:tblCellMar>"
        f"</w:tblPr>"
    )

    tbl_rows = []
    for r_idx, row in enumerate(rows):
        is_header = r_idx == 0
        trPr = "<w:trPr>"
        if is_header:
            trPr += "<w:tblHeader/>"
        trPr += '<w:cantSplit/></w:trPr>'

        tc_cells = []
        for c_idx in range(col_count):
            c_text = row[c_idx] if c_idx < len(row) else ""
            c_width = col_widths[c_idx]

            tcBorders = (
                f"<w:tcBorders>"
                f'<w:top w:val="single" w:sz="4" w:color="{BORDER_COLOR}"/>'
                f'<w:left w:val="single" w:sz="4" w:color="{BORDER_COLOR}"/>'
                f'<w:bottom w:val="single" w:sz="4" w:color="{BORDER_COLOR}"/>'
                f'<w:right w:val="single" w:sz="4" w:color="{BORDER_COLOR}"/>'
                f"</w:tcBorders>"
            )

            tcPr = (
                f"<w:tcPr>"
                f'<w:tcW w:w="{c_width}" w:type="dxa"/>'
                f"{tcBorders}"
                f'<w:vAlign w:val="center"/>'
                f"</w:tcPr>"
            )

            pPr = (
                f"<w:pPr>"
                f'<w:spacing w:before="40" w:after="40" w:line="240" w:lineRule="auto"/>'
                f"</w:pPr>"
            )
            runs_xml = parse_inline_runs(c_text, base_bold=is_header, sz=20)
            tc_p = f"<w:p>{pPr}{runs_xml}</w:p>"
            tc_cells.append(f"<w:tc>{tcPr}{tc_p}</w:tc>")

        tbl_rows.append(f"<w:tr>{trPr}{''.join(tc_cells)}</w:tr>")

    return f"<w:tbl>{tblPr}{tblGrid}{''.join(tbl_rows)}</w:tbl>"


def get_image_dimensions(png_path):
    try:
        with open(png_path, "rb") as f:
            data = f.read(24)
            if data[:8] == b"\x89PNG\r\n\x1a\n":
                w, h = struct.unpack(">II", data[16:24])
                return w, h
    except Exception:
        pass
    return 1200, 800


def make_image_p(rel_id, doc_pr_id, name, png_path):
    px_w, px_h = get_image_dimensions(png_path)
    aspect = px_h / float(px_w) if px_w > 0 else 0.75
    cx = 5800000  # full 1-inch margin printable width in EMUs
    cy = int(cx * aspect)
    max_cy = 7500000  # prevent overflowing single portrait page
    if cy > max_cy:
        cy = max_cy
        cx = int(cy / aspect)

    return (
        "<w:p>"
        "<w:pPr>"
        '<w:jc w:val="center"/>'
        '<w:spacing w:before="120" w:after="120"/>'
        "</w:pPr>"
        "<w:r>"
        "<w:drawing>"
        '<wp:inline distT="0" distB="0" distL="0" distR="0" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
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
        "word/media/fig3_1_3tier_architecture.png",
        os.path.join(SCRIPT_DIR, "diagrams", "fig3_1_3tier_architecture.png"),
        201,
        "Figure 3.1 3-Tier Zero-Plaintext Architecture Diagram",
    ),
    "rId202": (
        "word/media/fig3_2_dfd_level_0.png",
        os.path.join(SCRIPT_DIR, "diagrams", "fig3_2_dfd_level_0.png"),
        202,
        "Figure 3.2 DFD Level 0 Context Diagram",
    ),
    "rId203": (
        "word/media/fig3_3_dfd_level_1.png",
        os.path.join(SCRIPT_DIR, "diagrams", "fig3_3_dfd_level_1.png"),
        203,
        "Figure 3.3 DFD Level 1 Functional Decomposition Diagram",
    ),
    "rId204": (
        "word/media/fig3_4_cloud_topology.png",
        os.path.join(SCRIPT_DIR, "diagrams", "fig3_4_cloud_topology.png"),
        204,
        "Figure 3.4 Cloud Infrastructure Topology Diagram",
    ),
}

png_basename_to_rid = {
    "fig3_1_3tier_architecture.png": "rId201",
    "fig3_2_dfd_level_0.png": "rId202",
    "fig3_3_dfd_level_1.png": "rId203",
    "fig3_4_cloud_topology.png": "rId204",
}


def compile_markdown_to_docx(md_source_path, target_docx_path, mirror_docx_path=None):
    with open(md_source_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    lines = md_text.splitlines()
    body_parts = []
    i = 0
    in_code_block = False
    code_block_lines = []
    inserted_diagrams = set()

    while i < len(lines):
        line = lines[i]
        sline = line.strip()

        # Fenced code blocks
        if sline.startswith("```"):
            if not in_code_block:
                in_code_block = True
                code_block_lines = []
            else:
                in_code_block = False
                for c_line in code_block_lines:
                    body_parts.append(make_code_block_p(c_line))
            i += 1
            continue

        if in_code_block:
            code_block_lines.append(line)
            i += 1
            continue

        # Embed PNG diagram on markdown image links
        if sline.startswith("!["):
            rid = None
            for bname, candidate_rid in png_basename_to_rid.items():
                if bname in sline:
                    rid = candidate_rid
                    break
            if rid and rid not in inserted_diagrams:
                _, png_path, doc_id, d_name = diagram_files[rid]
                if rid == "rId203":
                    body_parts.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
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

    print(
        f"[{os.path.basename(md_source_path)}] Parsed {len(lines)} lines into {len(body_parts)} body elements; diagrams: {sorted(list(inserted_diagrams))}"
    )

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

    header_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<w:hdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">\n'
        '<w:p><w:pPr><w:jc w:val="right"/><w:spacing w:after="0"/><w:pBdr><w:bottom w:val="single" w:sz="4" w:space="2" w:color="000000"/></w:pBdr></w:pPr>'
        '<w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:color w:val="000000"/><w:sz w:val="18"/></w:rPr>'
        '<w:t>PTUT - PRJ - 089 | BugBountyTrack — High-Level Architecture &amp; Cloud Topology</w:t></w:r></w:p>\n'
        "</w:hdr>"
    )

    footer_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">\n'
        '<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="60"/><w:pBdr><w:top w:val="single" w:sz="4" w:space="2" w:color="000000"/></w:pBdr></w:pPr>'
        '<w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:color w:val="000000"/><w:sz w:val="18"/></w:rPr>'
        '<w:t>Page </w:t></w:r>'
        '<w:fldSimple w:instr="PAGE"/>'
        '<w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:color w:val="000000"/><w:sz w:val="18"/></w:rPr>'
        '<w:t> of </w:t></w:r>'
        '<w:fldSimple w:instr="NUMPAGES"/>'
        '<w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:color w:val="000000"/><w:sz w:val="18"/></w:rPr>'
        '<w:t>  |  Taha Asadullah (24-ST-013)  |  Week 3 Architecture Specification</w:t></w:r></w:p>\n'
        "</w:ftr>"
    )

    styles_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:cs="Times New Roman" w:eastAsia="Times New Roman" w:hAnsi="Times New Roman"/>
        <w:color w:val="000000"/>
        <w:sz w:val="22"/>
        <w:szCs w:val="22"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr>
        <w:spacing w:before="60" w:after="80" w:line="240" w:lineRule="auto"/>
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
  <Relationship Id="rId201" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/fig3_1_3tier_architecture.png"/>
  <Relationship Id="rId202" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/fig3_2_dfd_level_0.png"/>
  <Relationship Id="rId203" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/fig3_3_dfd_level_1.png"/>
  <Relationship Id="rId204" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/fig3_4_cloud_topology.png"/>
</Relationships>"""

    os.makedirs(os.path.dirname(target_docx_path), exist_ok=True)
    with zipfile.ZipFile(target_docx_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types_xml)
        z.writestr("_rels/.rels", root_rels_xml)
        z.writestr("word/_rels/document.xml.rels", doc_rels_xml)
        z.writestr("word/document.xml", doc_xml)
        z.writestr("word/header1.xml", header_xml)
        z.writestr("word/footer1.xml", footer_xml)
        z.writestr("word/styles.xml", styles_xml)
        z.writestr("word/settings.xml", settings_xml)

        for rid, (arcname, fpath, _, _) in diagram_files.items():
            if os.path.exists(fpath):
                z.write(fpath, arcname)
            else:
                print(f"[WARN] Diagram file missing: {fpath}")

    print(
        f"Successfully generated {target_docx_path} ({os.path.getsize(target_docx_path):,} bytes)"
    )
    if mirror_docx_path:
        os.makedirs(os.path.dirname(mirror_docx_path), exist_ok=True)
        shutil.copy2(target_docx_path, mirror_docx_path)
        print(f"Synchronized copy to {mirror_docx_path}")


def main():
    source_md = os.path.join(SCRIPT_DIR, "HIGH_LEVEL_ARCHITECTURE.md")
    target_docx = os.path.join(SCRIPT_DIR, "HIGH_LEVEL_ARCHITECTURE.docx")
    mirror_docx = os.path.join(PROJECT_DIR, "Resources", "HIGH_LEVEL_ARCHITECTURE.docx")

    compile_markdown_to_docx(source_md, target_docx, mirror_docx)


if __name__ == "__main__":
    main()
