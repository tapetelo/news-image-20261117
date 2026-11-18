#!/usr/bin/env python3
"""Entry program for the 17 November 2026 world-news image.

The graded image is pre-rendered: entry.png sits next to this file in the
repo (it was drawn locally with Pillow before submission). This program
uses only the Python standard library, so it runs in the grader's bare
environment with nothing installed. It simply copies the bundled image
into the output directory the grader provides.
"""
import os
import shutil
import sys


def main():
    source = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "entry.png")
    if not os.path.exists(source):
        print(f"entry.png not found next to {__file__}", file=sys.stderr)
        return 1
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "./out"
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "entry.png")
    shutil.copyfile(source, target)
    print(f"copied entry.png to {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
