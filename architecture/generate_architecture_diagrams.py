#!/usr/bin/env python3
"""
BugBountyTrack — High-Level Architecture & Cloud Topology Diagram Generator
Renders high-resolution PNG and SVG diagrams from architecture/diagrams/*.mmd using mmdc.
"""

import os
import sys
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DIAGRAMS_DIR = os.path.join(SCRIPT_DIR, "diagrams")
TOOLS_DIR = os.path.join(PROJECT_DIR, "requirements", "tools")

MMDC_PATH = os.path.join(TOOLS_DIR, "node_modules", ".bin", "mmdc")
PUPPETEER_CONFIG = os.path.join(TOOLS_DIR, "puppeteer-config.json")
MERMAID_CONFIG = os.path.join(TOOLS_DIR, "mermaid-config.json")

DIAGRAMS = [
    "fig3_1_3tier_architecture",
    "fig3_2_dfd_level_0",
    "fig3_3_dfd_level_1",
    "fig3_4_cloud_topology",
]


def render_diagram(stem):
    mmd_path = os.path.join(DIAGRAMS_DIR, f"{stem}.mmd")
    png_path = os.path.join(DIAGRAMS_DIR, f"{stem}.png")
    svg_path = os.path.join(DIAGRAMS_DIR, f"{stem}.svg")

    if not os.path.exists(mmd_path):
        print(f"[ERROR] Source not found: {mmd_path}")
        return False

    # 1. Render PNG at 3x scale for crisp OpenXML Word embedding
    cmd_png = [
        MMDC_PATH,
        "-p", PUPPETEER_CONFIG,
        "-c", MERMAID_CONFIG,
        "-i", mmd_path,
        "-o", png_path,
        "-b", "white",
        "-s", "3",
    ]
    res_png = subprocess.run(cmd_png, capture_output=True, text=True)
    if res_png.returncode != 0:
        print(f"[FAIL] PNG render failed for {stem}:\n{res_png.stderr}")
        return False

    # 2. Render SVG
    cmd_svg = [
        MMDC_PATH,
        "-p", PUPPETEER_CONFIG,
        "-c", MERMAID_CONFIG,
        "-i", mmd_path,
        "-o", svg_path,
        "-b", "white",
    ]
    res_svg = subprocess.run(cmd_svg, capture_output=True, text=True)
    if res_svg.returncode != 0:
        print(f"[FAIL] SVG render failed for {stem}:\n{res_svg.stderr}")
        return False

    png_size = os.path.getsize(png_path)
    svg_size = os.path.getsize(svg_path)
    print(f"[PASS] {stem}: PNG ({png_size:,} bytes) | SVG ({svg_size:,} bytes)")
    return True


def main():
    if not os.path.exists(MMDC_PATH):
        print(f"[ERROR] mmdc not found at {MMDC_PATH}")
        sys.exit(1)

    print("=" * 80)
    print("BUGBOUNTYTRACK WEEK 3 ARCHITECTURE DIAGRAM RENDERER")
    print("=" * 80)

    success_count = 0
    for stem in DIAGRAMS:
        if render_diagram(stem):
            success_count += 1

    print("=" * 80)
    print(f"Rendered {success_count}/{len(DIAGRAMS)} architecture diagrams successfully.")
    print("=" * 80)

    if success_count != len(DIAGRAMS):
        sys.exit(1)


if __name__ == "__main__":
    main()
