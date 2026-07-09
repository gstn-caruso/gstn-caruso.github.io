#!/usr/bin/env python3
"""Fail if the built site uses a character the fonts do not carry.

A missing glyph does not announce itself. The browser reaches for the next
family in the stack — a system serif, with other proportions and another
colour — and sets that one word in it. On a page whose whole argument is that
its typography is deliberate, the reader sees the seam and cannot name it.

    python3 tools/check-charset.py _site

Needs fontTools. Run tools/subset-fonts.sh if this reports a gap: add the
character to tools/charset.txt first.
"""

import html
import pathlib
import re
import sys
import unicodedata

from fontTools.ttLib import TTFont

FONT = "assets/fonts/charis-400.woff2"

# The page draws with these, and no font is asked to.
IGNORED = set("\t\n\r​﻿")

# Text this check must not read: it is never set in Charis.
STRIPPED = re.compile(
    r"<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>|<!--.*?-->|<[^>]+>",
    re.DOTALL | re.IGNORECASE,
)


def text_of(markup: str) -> str:
    return html.unescape(STRIPPED.sub(" ", markup))


def main() -> int:
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
    covered = set(TTFont(FONT).getBestCmap())

    missing: dict[str, list[str]] = {}
    for page in sorted(root.rglob("*.html")):
        for char in text_of(page.read_text(encoding="utf-8")):
            if ord(char) in covered or char in IGNORED:
                continue
            missing.setdefault(char, []).append(str(page.relative_to(root)))

    if not missing:
        print(f"charset: every character in {root} is in the subset")
        return 0

    print(f"charset: {len(missing)} character(s) would fall back to a system serif\n")
    for char, pages in sorted(missing.items()):
        name = unicodedata.name(char, "unnamed")
        where = ", ".join(sorted(set(pages)))
        print(f"  {char!r}  U+{ord(char):04X}  {name}\n      in {where}")
    print("\nAdd them to tools/charset.txt, then run tools/subset-fonts.sh")
    return 1


if __name__ == "__main__":
    sys.exit(main())
