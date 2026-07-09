# gstn-caruso.github.io

A blog. Every entry is a reading page and nothing else: no trackers, no
analytics, eight lines of JavaScript, and one stylesheet.

Read it in **[castellano](https://gstn-caruso.github.io/)** or in
**[English](https://gstn-caruso.github.io/en/)**.

## How it is put together

Jekyll turns the repository into the site on every push to `main`, via
`.github/workflows/pages.yml`. There is nothing to build by hand and no Gemfile
to keep current — the workflow uses `actions/jekyll-build-pages`, which brings
its own Jekyll.

```
index.md               the index, in Spanish  →  /
en/index.md            the index, in English  →  /en/
feed.xml, en/feed.xml  one Atom feed per language

_data/entries.yml      every entry, in both languages
_data/strings.yml      the chrome: nav labels, colophon, skip link

_layouts/house.html    <head>, the skip link, the colophon, the language script
_layouts/index.html    the list of entries
_layouts/article.html  an entry written here
_layouts/dpbs.html     the Ingalls mirror, which brings its own stylesheet
_layouts/feed.xml      both feeds
_includes/lang-nav.html

design-principles-behind-smalltalk/
                       the mirror itself  →  /design-principles-behind-smalltalk/

assets/css/house.css   the whole design
assets/fonts/          Charis, subset
tools/                 where assets/fonts/ comes from, and what guards it
```

This is a *user site*, so it is served from the root and has no `baseurl`. The
project pages under the same account keep their own, and are untouched by any
of this.

## The design

The first entry is a mirror of *Design Principles Behind Smalltalk*, whose
Figure 1 draws two beings joined by two arcs. The solid arc is *explicit
communication* — the words actually said. The dashed arc is *implicit
communication* — the shared context that makes the words mean anything.

That article's page turned the figure into its rule system. This site inherits
it, and the rules carry information rather than decorating:

| rule | what it marks |
|---|---|
| solid | the thing itself — the site's name, an entry, a heading |
| dashed | the context around it — dates, blurbs, captions, the colophon |

### Type

One family to read in: **Charis**, the free descendant of Matthew Carter's
Charter, which he cut in 1987 for 300dpi printers — the coarse output Smalltalk
was first read on.

Monospace means one thing and one thing only: *this is code*. Never a label,
never a caption. Rouge marks up the tokens inside a code block and nothing
colours them, because monospace has already said what there is to say.

The measure is 66 characters, which Bringhurst calls ideal for a single column.
Note that `1ch` is the width of `0`, and in Charis that is `0.563em` — wider
than the average lowercase letter — so `66ch` would set about 75 characters.
The CSS says `55ch`. That number was measured in a browser, not guessed.

The prose is set ragged right. Browsers have no Knuth-Plass line breaker, so
justifying would only open rivers of white space. Hyphenation switches on below
`32rem`, where the measure gets short enough that the rag would otherwise turn
ugly.

### The year hangs in the margin

Not a number. A running count would renumber every entry below the next thing
published, and a number that changes is a number that lies. The year an entry
was written never moves. It is printed only when it differs from the entry
above, the way an archive prints it.

## The fonts, and what guards them

`tools/subset-fonts.sh` builds `assets/fonts/` from an upstream Charis release.
The binaries are committed; the script is why you can check them instead of
believing them.

Two things it gets right that are easy to get wrong:

- **Small capitals fold both ways.** `smcp` turns lowercase into small caps;
  `c2sc` turns capitals into small caps. `font-variant-caps: all-small-caps`
  asks for both. Subset with only `smcp` and every capital in an eyebrow stays
  full height, towering over the small caps beside it — legibly, quietly, wrong.
- **The f-ligatures survive.** `font-variant-ligatures: common-ligatures` needs
  the `f_i` and `f_l` glyphs to still be in the font, not merely the `liga`
  feature to still be listed.

The script asserts both, and asserts kerning, by reading the lookups rather than
the glyph names — `pyftsubset` writes a `post` table of format 3.0, so the fi
ligature comes out the other side called `glyph00196`.

Charis has no `tnum`. It does not need one: its lining figures are already
tabular, all 1153/2048 of an em wide. `font-variant-numeric: tabular-nums` in
the stylesheet is therefore a no-op here, and load-bearing for the Georgia
fallback, whose figures are old-style and proportional.

`tools/charset.txt` fixes what the fonts carry: ASCII, Latin-1, and the
punctuation prose wants — 210 characters. A blog cannot subset to the exact text
it has, the way a finished article can, because the next entry brings characters
the last one never needed. And a character the font lacks does not announce
itself: the browser sets that one word in a system serif, mid-sentence, and the
reader sees a seam they cannot name.

So `tools/check-charset.py` reads every built page and fails if it finds one.
The workflow runs it before it deploys.

```sh
python3 tools/check-charset.py _site
```

## Adding an entry

An entry is a reading page. Some are written here; some live in a repository of
their own. The index does not care which — only the URL differs.

**One that lives elsewhere:** add it to `_data/entries.yml` with `away: true`.
Nothing else. The index draws it with an arrow, and the feed points at the
address it actually answers at.

**One written here:** put it at `<slug>/index.md` with `layout: article` and
`permalink: /<slug>/`, then name it in `_data/entries.yml` too. Its front matter
carries `lang`, `title`, `eyebrow`, `description`, and `translation`.

Every entry in `_data/entries.yml` needs an `en:` and an `es:` block — title,
eyebrow, blurb, url. Use real typography in them: they are YAML, not markdown,
so kramdown never gets a chance to turn `'` into `’` for you.

## Adding a language

Add its block to `_data/strings.yml`, add a block per entry in
`_data/entries.yml`, copy `index.md` and `feed.xml` into `<lang>/`, and point
every page's `translation` at its counterpart.

Then check the new language's characters are in `tools/charset.txt`. Anything
outside Latin-1 will need it grown, and the fonts rebuilt.

## Building locally

```sh
gem install jekyll kramdown-parser-gfm
jekyll serve
```

Local Jekyll is 4.x; the workflow's is the one the `github-pages` gem pins. The
site uses no plugins, so they agree.

## Credits

Type is [Charis](https://software.sil.org/charis/) by SIL Global, used under the
SIL Open Font License 1.1. The license travels with the fonts, in
`assets/fonts/OFL.txt`.

The rule system is lifted from *Design Principles Behind Smalltalk*, by Daniel
H. H. Ingalls, and from the figure Dwight Hughes recreated for it.
