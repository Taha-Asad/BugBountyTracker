#!/usr/bin/env python3
"""
BugBountyTrack — Automated High-Resolution Diagram Generator (Version 3.2.0)
Extracts the canonical Mermaid architecture diagrams directly from requirements/SRS.md
and renders pixel-perfect, high-resolution PNG and SVG artifacts using mmdc and Chrome.
"""

import os
import sys
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SRS_PATH = os.path.join(SCRIPT_DIR, "SRS.md")
DIAGRAMS_DIR = os.path.join(SCRIPT_DIR, "diagrams")
TOOLS_DIR = os.path.join(SCRIPT_DIR, "tools")

os.makedirs(DIAGRAMS_DIR, exist_ok=True)
os.makedirs(TOOLS_DIR, exist_ok=True)

MMDC_PATH = os.path.join(TOOLS_DIR, "node_modules", ".bin", "mmdc")
PUPPETEER_CONFIG = os.path.join(TOOLS_DIR, "puppeteer-config.json")
MERMAID_CONFIG = os.path.join(TOOLS_DIR, "mermaid-config.json")

# Ensure puppeteer config exists
if not os.path.exists(PUPPETEER_CONFIG):
    with open(PUPPETEER_CONFIG, "w", encoding="utf-8") as f:
        f.write('''{
  "executablePath": "/usr/bin/google-chrome-stable",
  "args": ["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage", "--disable-gpu"]
}
''')

# Write university-standard monochrome Times New Roman Mermaid config
with open(MERMAID_CONFIG, "w", encoding="utf-8") as f:
    f.write('''{
  "theme": "base",
  "fontFamily": "\\"Times New Roman\\", Times, serif",
  "themeVariables": {
    "fontFamily": "\\"Times New Roman\\", Times, serif",
    "fontSize": "15px",
    "primaryColor": "#ffffff",
    "primaryTextColor": "#000000",
    "primaryBorderColor": "#000000",
    "lineColor": "#000000",
    "secondaryColor": "#f4f4f4",
    "tertiaryColor": "#ffffff",
    "mainBkg": "#ffffff",
    "secondBkg": "#f4f4f4",
    "nodeBorder": "#000000",
    "clusterBkg": "#fafafa",
    "clusterBorder": "#000000",
    "defaultLinkColor": "#000000",
    "titleColor": "#000000",
    "edgeLabelBackground": "#ffffff",
    "actorBkg": "#ffffff",
    "actorBorder": "#000000",
    "actorTextColor": "#000000",
    "actorLineColor": "#000000",
    "signalColor": "#000000",
    "signalTextColor": "#000000",
    "labelBoxBkgColor": "#f4f4f4",
    "labelBoxBorderColor": "#000000",
    "labelTextColor": "#000000",
    "loopTextColor": "#000000",
    "noteBorderColor": "#000000",
    "noteBkgColor": "#f4f4f4",
    "noteTextColor": "#000000",
    "activationBorderColor": "#000000",
    "activationBkgColor": "#eaeaea",
    "sequenceNumberColor": "#ffffff",
    "attributeBackgroundColorOdd": "#ffffff",
    "attributeBackgroundColorEven": "#f4f4f4"
  },
  "flowchart": { "useMaxWidth": false, "htmlLabels": true, "curve": "basis", "padding": 14 },
  "sequence": { "useMaxWidth": false, "wrap": false, "messageMargin": 36, "boxMargin": 10 },
  "er": { "useMaxWidth": false, "layoutDirection": "TB", "minEntityWidth": 100, "minEntityHeight": 70, "entityPadding": 12 },
  "state": { "useMaxWidth": false }
}
''')

SECTIONS = [
    ("Figure 4.1)", "fig4_2_usecase"),
    ("Figure 4.2)", "fig4_3_seq_submission"),
    ("Figure 4.3)", "fig4_4_seq_decryption"),
    ("Figure 4.4)", "fig4_5_statemachine"),
]

def main():
    if not os.path.exists(SRS_PATH):
        print(f"Error: SRS.md not found at {SRS_PATH}")
        sys.exit(1)

    with open(SRS_PATH, "r", encoding="utf-8") as f:
        srs_content = f.read()

    if not os.path.exists(MMDC_PATH):
        print(f"Error: mmdc executable not found at {MMDC_PATH}.")
        print("Please run: cd requirements/tools && npm install @mermaid-js/mermaid-cli")
        sys.exit(1)

    print("=" * 80)
    print("BUGBOUNTYTRACK CANONICAL DIAGRAM GENERATOR (VERSION 3.2.0)")
    print("Rendering high-resolution diagrams directly from SRS.md Mermaid specifications")
    print("=" * 80)

    success_count = 0
    for heading, file_stem in SECTIONS:
        idx = srs_content.find(f"### 4.")
        # Find the specific section heading containing the Figure marker
        import re
        m = re.search(rf"^###\s+4\.\d+.*{re.escape(heading)}", srs_content, re.MULTILINE)
        if not m:
            print(f"[FAIL] Heading containing '{heading}' not found in SRS.md!")
            continue
        idx = m.start()

        m_start = srs_content.find("```mermaid", idx)
        if m_start == -1:
            print(f"[FAIL] Mermaid block not found under '{heading}'!")
            continue

        m_end = srs_content.find("```", m_start + 10)
        mermaid_code = srs_content[m_start + 10:m_end].strip()

        mmd_file = os.path.join(DIAGRAMS_DIR, f"{file_stem}.mmd")
        with open(mmd_file, "w", encoding="utf-8") as f:
            f.write(mermaid_code + "\n")

        png_out = os.path.join(DIAGRAMS_DIR, f"{file_stem}.png")
        svg_out = os.path.join(DIAGRAMS_DIR, f"{file_stem}.svg")

        # 1. Render PNG (3x scale for high-DPI Word document embedding)
        cmd_png = [MMDC_PATH, "-p", PUPPETEER_CONFIG, "-c", MERMAID_CONFIG, "-i", mmd_file, "-o", png_out, "-b", "white", "-s", "3"]
        res_png = subprocess.run(cmd_png, capture_output=True, text=True)
        if res_png.returncode != 0:
            print(f"[FAIL] PNG render failed for {file_stem}:\n{res_png.stderr}")
            continue

        # 2. Render SVG
        cmd_svg = [MMDC_PATH, "-p", PUPPETEER_CONFIG, "-c", MERMAID_CONFIG, "-i", mmd_file, "-o", svg_out, "-b", "white"]
        res_svg = subprocess.run(cmd_svg, capture_output=True, text=True)
        if res_svg.returncode != 0:
            print(f"[FAIL] SVG render failed for {file_stem}:\n{res_svg.stderr}")
            continue

        png_size = os.path.getsize(png_out)
        svg_size = os.path.getsize(svg_out)
        print(f"[PASS] {file_stem}: PNG ({png_size:,} bytes) | SVG ({svg_size:,} bytes)")
        success_count += 1

    print("-" * 80)
    print(f"Generated {success_count}/{len(SECTIONS)} diagrams successfully.")
    if success_count == len(SECTIONS):
        print("ALL DIAGRAMS SYNCHRONIZED AND UP TO DATE!")
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())
