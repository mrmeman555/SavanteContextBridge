#!/usr/bin/env python3
"""
Savante Context Engineer Pack Builder
======================================
Assembles the Savante Context Engineer file pack for Grok / any project space.
Handles: directory creation, file copying, validation, and reporting.

Usage:
    python3 build_pack.py [--dry-run]
"""

import os
import shutil
import sys
from datetime import datetime

# === CONFIGURATION ===

PACK_ROOT = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = "/home/aaron/Projects/Working0"
SAVANTE_SOURCE = "/mnt/share/IO/inbox/Savente_Context_Engineer"
CA_SOURCE = f"{WORKSPACE}/Active/Sprint_ML_OS_Architect/Context_Architecture"

# Directories to create
DIRS_TO_CREATE = [
    "00_Framework",
    "01_Methods",
    "02_Transcripts",
]

# Files to COPY from workspace into pack
# Format: (source_path, destination_relative_to_pack)
COPY_MAP = [
    # --- 00_Framework ---
    (
        f"{SAVANTE_SOURCE}/Copy-of-Architecting-Deep-Research-Prompts.docx",
        "00_Framework/Architecting_Deep_Research_Prompts.docx",
    ),
    (
        f"{CA_SOURCE}/Context_Architecture_Principles.md",
        "00_Framework/Context_Architecture_Principles.md",
    ),

    # --- 01_Methods ---
    (
        f"{SAVANTE_SOURCE}/2StepDeepResearchPrompting.md",
        "01_Methods/Architects_Roundtable_Recursive_Prompt_Design.md",
    ),
    (
        f"{SAVANTE_SOURCE}/Copy-of-Advanced-Context-Engineering-for-AI-Video.docx",
        "01_Methods/Advanced_Context_Engineering_Video.docx",
    ),

    # --- 02_Transcripts ---
    (
        f"{SAVANTE_SOURCE}/hello-as-a-savante-context-eng-wD_.9HTsQGehxyMbNikP2w.md",
        "02_Transcripts/Genesis_Transcript.md",
    ),
    (
        f"{SAVANTE_SOURCE}/hello-savant-please-give-me-a-5YA.PPDITJiQtiQRP0JY2Q.md",
        "02_Transcripts/Meta_Index_Chat.md",
    ),
]

# Files that should exist after manual writing (bootloader, framing, etc.)
EXPECTED_NEW_FILES = [
    "README.md",
    "BOOTLOADER_GROK.md",
    "CONTEXT_ARCHITECTURE_FRAME.md",
    "PACK_DESIGN.md",
    "CONTENT_INVENTORY.md",
]


def main():
    dry_run = "--dry-run" in sys.argv
    mode = "DRY RUN" if dry_run else "BUILD"

    print(f"\n{'='*60}")
    print(f"  Savante Context Engineer Pack Builder — {mode}")
    print(f"  Target: {PACK_ROOT}")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    errors = []
    copied = 0
    created_dirs = 0

    # Step 1: Create directories
    print("--- Step 1: Creating directories ---")
    for d in DIRS_TO_CREATE:
        full = os.path.join(PACK_ROOT, d)
        if not os.path.exists(full):
            print(f"  [CREATE] {d}/")
            if not dry_run:
                os.makedirs(full, exist_ok=True)
            created_dirs += 1
        else:
            print(f"  [EXISTS] {d}/")

    # Step 2: Copy files
    print("\n--- Step 2: Copying files ---")
    for src, dst_rel in COPY_MAP:
        dst = os.path.join(PACK_ROOT, dst_rel)
        if not os.path.exists(src):
            msg = f"  [MISSING SOURCE] {src}"
            print(msg)
            errors.append(msg)
            continue
        action = "COPY" if not os.path.exists(dst) else "UPDATE"
        print(f"  [{action}] {os.path.basename(src)} → {dst_rel}")
        if not dry_run:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
        copied += 1

    # Step 3: Validate expected new files exist
    print("\n--- Step 3: Validating authored content files ---")
    missing_new = []
    for f in EXPECTED_NEW_FILES:
        full = os.path.join(PACK_ROOT, f)
        if os.path.exists(full):
            print(f"  [  OK  ] {f}")
        else:
            print(f"  [MISSING] {f}")
            missing_new.append(f)

    # Step 4: Count total files
    print("\n--- Step 4: Pack inventory ---")
    total_files = 0
    total_dirs = 0
    for root, dirs, files in os.walk(PACK_ROOT):
        if ".git" in root:
            continue
        for f in files:
            if not f.startswith(".") and f != "build_pack.py":
                total_files += 1
        for d in dirs:
            if not d.startswith("."):
                total_dirs += 1

    # Summary
    print(f"\n{'='*60}")
    print(f"  SUMMARY")
    print(f"{'='*60}")
    print(f"  Directories created: {created_dirs}")
    print(f"  Files copied: {copied}")
    print(f"  Total content files: {total_files}")
    print(f"  Total directories: {total_dirs}")
    if missing_new:
        print(f"\n  ⚠️  MISSING AUTHORED CONTENT ({len(missing_new)}):")
        for f in missing_new:
            print(f"    - {f}")
    if errors:
        print(f"\n  ❌  ERRORS ({len(errors)}):")
        for e in errors:
            print(f"    {e}")
    if not missing_new and not errors:
        print(f"\n  ✅  PACK IS COMPLETE — ready to upload/push")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
