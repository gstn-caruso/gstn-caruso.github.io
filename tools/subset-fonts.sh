#!/usr/bin/env bash
#
# Rebuild assets/fonts/ from an upstream Charis release.
#
# The fonts in this repo are binaries. This script is where they come from, so
# the claim in the README can be checked instead of believed. Run it when
# tools/charset.txt grows, or when Charis publishes a version worth taking.
#
#   ./tools/subset-fonts.sh
#
# Needs: curl, unzip, pyftsubset (pip install 'fonttools[woff]').

set -euo pipefail

VERSION=7.000
FEATURES=kern,liga,ccmp,mark,mkmk,smcp,c2sc,onum

# smcp turns lowercase into small capitals; c2sc turns uppercase into small
# capitals. CSS `font-variant-caps: all-small-caps` asks for both. Keep only
# smcp — as the font this site descends from did — and every capital letter in
# an eyebrow or a sidehead stays full height, towering over the small caps
# beside it. The bug is quiet, because the text is still legible.
#
# ccmp, mark and mkmk are asked for and then pruned: charset.txt is entirely
# precomposed, so no combining mark survives for them to position. They stay in
# the list so that the day a combining mark is added, it is positioned.
#
# onum is what lets a date sit inside a line of small capitals without towering
# over it. Lining figures are cap height; the small caps around them are not.
#
# Charis has no tnum: its lining figures are already tabular, all 1153/2048 of
# an em wide. `font-variant-numeric: tabular-nums` in the CSS is therefore a
# no-op here — and load-bearing for the Georgia fallback, whose figures are
# old-style and proportional.
#
# Hinting survives. It is 40% of each file — 26 KB instead of 15 — and it is
# what keeps the stems even on Windows, where DirectWrite still grids-fits
# vertically at reading sizes.

cd "$(dirname "$0")/.."
ROOT=$PWD
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

echo "==> Charis $VERSION"
curl -fsSL -o "$WORK/charis.zip" \
  "https://github.com/silnrsi/font-charis/releases/download/v$VERSION/Charis-$VERSION.zip"
unzip -oq "$WORK/charis.zip" -d "$WORK"
SRC=$WORK/Charis-$VERSION

subset () {  # subset <upstream face> <output name>
  pyftsubset "$SRC/$1" \
    --unicodes-file="$ROOT/tools/charset.txt" \
    --layout-features="$FEATURES" \
    --name-IDs=0,1,2,3,4,5,6,13,14 \
    --flavor=woff2 \
    --output-file="$ROOT/assets/fonts/$2"
  printf '    %-24s %6s\n' "$2" "$(du -h "$ROOT/assets/fonts/$2" | cut -f1 | tr -d ' ')"
}

echo "==> subsetting"
subset Charis-Regular.ttf charis-400.woff2
subset Charis-Italic.ttf  charis-400-italic.woff2
subset Charis-Bold.ttf    charis-700.woff2

cp "$SRC/OFL.txt" "$ROOT/assets/fonts/OFL.txt"

echo "==> verifying"
python3 - "$ROOT" <<'PY'
import sys, pathlib
from fontTools.ttLib import TTFont

# Assert on the lookups, not on the glyph names. pyftsubset writes a post table
# of format 3.0, which carries no names at all: the fi ligature comes out the
# other side called glyph00196. Only what the CSS actually asks for is checked.
root = pathlib.Path(sys.argv[1])
ok = True

def lookups_of(font, table, tag):
    if table not in font:
        return []
    gsub = font[table].table
    indices = {i for r in gsub.FeatureList.FeatureRecord if r.FeatureTag == tag
                 for i in r.Feature.LookupListIndex}
    return [gsub.LookupList.Lookup[i] for i in indices]

for face in ("charis-400.woff2", "charis-400-italic.woff2", "charis-700.woff2"):
    font = TTFont(root / "assets/fonts" / face)
    chars = len(font.getBestCmap())
    problems = []

    # all-small-caps needs both halves; oldstyle-nums needs onum.
    for tag in ("smcp", "c2sc", "onum"):
        subs = sum(len(st.mapping) for lk in lookups_of(font, "GSUB", tag) for st in lk.SubTable)
        if not subs:
            problems.append(f"{tag} substitutes nothing")

    # font-variant-ligatures: common-ligatures needs f to lead somewhere.
    ligs = [lig for lk in lookups_of(font, "GSUB", "liga") for st in lk.SubTable
                for lig in st.ligatures.get("f", [])]
    if not ligs:
        problems.append("liga carries no f-ligature")

    if not lookups_of(font, "GPOS", "kern"):
        problems.append("no kerning")

    if problems:
        print(f"    {face}: {'; '.join(problems)}")
        ok = False
    else:
        print(f"    {face}: {chars} chars, small caps both ways, oldstyle figures, "
              f"{len(ligs)} f-ligatures, kerned")

sys.exit(0 if ok else 1)
PY

echo "==> done"
