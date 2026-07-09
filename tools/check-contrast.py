#!/usr/bin/env python3
"""Every colour pair on this site clears the contrast it owes the reader.

A grey that reads fine on the laptop you chose it on is a grey that vanishes
on a phone in sunlight, or under the eyes of the half of readers over forty
whose lenses have yellowed. WCAG puts a number on it, so the number is checked
here rather than trusted.

    python3 tools/check-contrast.py

Two files carry the palette: the house stylesheet, and the article's inlined
one. They are meant to be the same eight colours. Nothing but this check makes
them stay that way, so it compares them before it measures anything.

Needs nothing but the standard library. The workflow runs it before it deploys.
"""

import pathlib
import re
import sys

# --- the criteria -------------------------------------------------------
#
# 1.4.3 Contrast (Minimum), AA: text carries 4.5:1 against its background.
# Large text may take 3:1, and none of this site's small colours are only
# ever large, so the strict number applies throughout.
#
# 1.4.11 Non-text Contrast, AA: 3:1 for a graphical object you need in order
# to understand the content. house.css says of its rules: "It carries
# information. It is not decoration." That sentence is what puts them here.
# Solid means the thing itself, dashed means the context around it, and a
# reader who cannot tell the two apart has lost what the rules were for.
#
# The focus ring is also 1.4.11, and it is drawn in --accent, which the text
# rule already holds to the stricter 4.5:1. It needs no line of its own.
#
# The language toggle is not here. Its link used to be told from the text
# beside it by hue alone, and hue alone cannot be fixed by choosing a better
# hue: the two sit at the same luminance. It is underlined instead, so colour
# is no longer the only thing distinguishing it, and 1.4.1 is satisfied
# without a contrast floor between them.

TEXT, GRAPHIC = 4.5, 3.0

PAIRS = [
    ("ink",       "paper",       TEXT,    "body text"),
    ("ink-soft",  "paper",       TEXT,    "standfirst, blurbs, eyebrows, colophon"),
    ("ink-faint", "paper",       TEXT,    "the principle numbers, list markers"),
    ("accent",    "paper",       TEXT,    "links, the year, the focus ring"),
    ("ink",       "code-bg",     TEXT,    "code"),
    ("ink",       "accent-tint", TEXT,    "a principle addressed by its number"),
    ("rule",      "paper",       GRAPHIC, "the rules: solid explicit, dashed implicit"),
]

SOURCES = {
    "house": pathlib.Path("assets/css/house.css"),
    "article": pathlib.Path("_layouts/dpbs.html"),
}


def luminance(hex_colour):
    """Relative luminance, per WCAG 2.x."""
    h = hex_colour.lstrip("#")
    channels = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    linear = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
              for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    lighter, darker = max(la, lb), min(la, lb)
    return (lighter + 0.05) / (darker + 0.05)


def palettes(css):
    """The light and dark :root blocks, as {token: hex}.

    The print block overrides the palette to pure black on pure white, which
    passes by construction and describes a medium with no backlight. It is
    dropped before anything is read.
    """
    css = css.split("@media print")[0]
    blocks = re.findall(r":root\s*\{([^}]*)\}", css)
    if len(blocks) != 2:
        sys.exit(f"contrast: expected a light and a dark :root, found {len(blocks)}")
    return [dict(re.findall(r"--([a-z-]+):\s*(#[0-9a-fA-F]{6})", block))
            for block in blocks]


def main():
    read = {}
    for name, path in SOURCES.items():
        if not path.exists():
            sys.exit(f"contrast: {path} is missing")
        read[name] = palettes(path.read_text(encoding="utf-8"))

    # One palette, written twice. Say so before measuring half of it.
    for theme, (a, b) in enumerate(zip(read["house"], read["article"])):
        if a != b:
            drifted = {k for k in a.keys() | b.keys() if a.get(k) != b.get(k)}
            name = ("light", "dark")[theme]
            print(f"contrast: the {name} palettes have drifted apart", file=sys.stderr)
            for token in sorted(drifted):
                print(f"    --{token}: {a.get(token, '—')} in {SOURCES['house']}, "
                      f"{b.get(token, '—')} in {SOURCES['article']}", file=sys.stderr)
            return 1

    failures = 0
    for theme, palette in zip(("light", "dark"), read["house"]):
        print(f"  {theme}")
        for fg, bg, needs, what in PAIRS:
            missing = [t for t in (fg, bg) if t not in palette]
            if missing:
                print(f"    ??  --{', --'.join(missing)} is not in the {theme} palette")
                failures += 1
                continue
            ratio = contrast(palette[fg], palette[bg])
            ok = ratio >= needs
            failures += not ok
            print(f"    {'ok  ' if ok else 'FAIL'} {ratio:5.2f}:1  "
                  f"(needs {needs})  {fg} on {bg} — {what}")

    if failures:
        print(f"\ncontrast: {failures} pair{'s' if failures > 1 else ''} "
              f"below threshold", file=sys.stderr)
        return 1
    print("\ncontrast: every pair clears WCAG 2.2 AA")
    return 0


if __name__ == "__main__":
    sys.exit(main())
