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

# Ensure puppeteer config exists
if not os.path.exists(PUPPETEER_CONFIG):
    with open(PUPPETEER_CONFIG, "w", encoding="utf-8") as f:
        f.write('''{
  "executablePath": "/usr/bin/google-chrome-stable",
  "args": ["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage", "--disable-gpu"]
}
''')

SECTIONS = [
    ("### 4.2 Component Architecture Diagram (Figure 4.1)", "fig4_1_component"),
    ("### 4.3 Use Case Model Diagram (Figure 4.2)", "fig4_2_usecase"),
    ("### 4.4 Sequence: Browser-Side OpenPGP Submission (Figure 4.3)", "fig4_3_seq_submission"),
    ("### 4.5 Sequence: In-Browser Decryption & Confidential Conversation (Figure 4.4)", "fig4_4_seq_decryption"),
    ("### 4.6 State Machine: Remediation & Attested Retest Lifecycle (Figure 4.5)", "fig4_5_statemachine"),
    ("### 4.7 Relational Prisma Schema & Domain ERD (Figure 4.6)", "fig4_6_erd"),
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
        idx = srs_content.find(heading)
        if idx == -1:
            print(f"[FAIL] Heading '{heading}' not found in SRS.md!")
            continue

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

        # 1. Render PNG (2x scale for high-DPI Word document embedding)
        cmd_png = [MMDC_PATH, "-p", PUPPETEER_CONFIG, "-i", mmd_file, "-o", png_out, "-b", "white", "-s", "2"]
        res_png = subprocess.run(cmd_png, capture_output=True, text=True)
        if res_png.returncode != 0:
            print(f"[FAIL] PNG render failed for {file_stem}:\n{res_png.stderr}")
            continue

        # 2. Render SVG
        cmd_svg = [MMDC_PATH, "-p", PUPPETEER_CONFIG, "-i", mmd_file, "-o", svg_out, "-b", "white"]
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
